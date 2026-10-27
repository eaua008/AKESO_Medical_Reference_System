import json
import runpy
import sys
import tempfile
import unittest
from pathlib import Path

from app.models.body_part import BodyPartInfo, concept_key, parts_from_json, parts_to_json
from app.repositories.cached_body_part_repository import (
    CachedBodyPartRepository, LocalBodyPartCache,
)
from app.services.body_part_service import BodyPartService

ROOT = Path(__file__).resolve().parents[1]


def row(key, fmas, kind="part", status="published", **extra):
    return {"key": key, "kind": kind, "display_name": key.title(), "fma_ids": fmas,
            "layer": "muscle", "status": status, **extra}


class FakeRemote:
    def __init__(self, version, rows):
        self.version, self.rows, self.fetches = version, rows, 0

    def content_version(self):
        return self.version

    def fetch_published(self):
        self.fetches += 1
        return self.rows


class BodyPartModelTest(unittest.TestCase):
    def test_concept_key_drops_sides_only(self):
        self.assertEqual(concept_key("Long head of LEFT biceps brachii"), "long head of biceps brachii")
        self.assertEqual(concept_key("right  femur"), "femur")

    def test_from_row_cleans_and_round_trips(self):
        info = BodyPartInfo.from_row(row(
            "femur", ["FMA1"], layer="bone",
            details={"type": "long", "joints": " ", "unknown": "x"},
            clinical=[{"text": "Hip fracture", "disease_id": None}, {"text": ""}, "junk"],
            sources=[{"title": "SEER", "url": "https://x.gov"}, {"title": "no url"}]))
        self.assertEqual(info.detail_rows(), [("Type", "long")])
        self.assertEqual([(c.text, c.disease_id) for c in info.clinical], [("Hip fracture", "")])
        self.assertEqual(len(info.sources), 1)
        self.assertFalse(info.is_draft)
        again = parts_from_json(parts_to_json([info]))[0]
        self.assertEqual(again, info)

    def test_damaged_copy_reads_as_empty(self):
        self.assertEqual(parts_from_json("{not json"), [])


class BodyPartLookupTest(unittest.TestCase):
    def service(self, rows):
        repo = type("R", (), {"load": lambda _s: [BodyPartInfo.from_row(r) for r in rows]})()
        return BodyPartService(repo)

    def test_most_specific_entry_wins(self):
        s = self.service([
            row("group:arm_front", ["FMA1", "FMA2", "FMA3"], kind="group"),
            row("biceps brachii", ["FMA1", "FMA2"]),
            row("brachialis", ["FMA3"]),
        ])
        d = s.describe("FMA1", "long head of left biceps brachii")
        self.assertEqual(d.info.key, "biceps brachii")
        self.assertFalse(d.exact)                       # shown as "Part of Biceps brachii"
        self.assertTrue(s.describe("FMA3", "right brachialis").exact)
        self.assertIsNone(s.describe("FMA9", "anything"))
        self.assertIsNone(s.describe("", "no id"))

    def test_group_entries_are_never_exact(self):
        s = self.service([row("group:heart", ["FMA7"], kind="group")])
        self.assertFalse(s.describe("FMA7", "heart").exact)

    def test_drafts_replace_published_for_admins(self):
        s = self.service([row("femur", ["FMA1"], summary_plain="old")])
        self.assertEqual(s.describe("FMA1", "femur").info.summary_plain, "old")
        s.set_drafts([row("femur", ["FMA1"], status="draft", summary_plain="new"),
                      row("tibia", ["FMA2"], status="draft")])
        d = s.describe("FMA1", "left femur")
        self.assertEqual(d.info.summary_plain, "new")
        self.assertTrue(d.info.is_draft)
        self.assertIsNotNone(s.describe("FMA2", "tibia"))

    def test_broken_cache_shows_nothing(self):
        def boom(_s):
            raise OSError("disk")
        s = BodyPartService(type("R", (), {"load": boom})())
        self.assertIsNone(s.describe("FMA1", "femur"))


class BodyPartCacheTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cache = LocalBodyPartCache(Path(self.tmp.name) / "parts.db")

    def tearDown(self):
        self.tmp.cleanup()

    def test_sync_downloads_only_when_the_version_changes(self):
        remote = FakeRemote(5, [row("femur", ["FMA1"])])
        repo = CachedBodyPartRepository(self.cache, lambda: remote)
        self.assertTrue(repo.sync())
        self.assertFalse(repo.sync())
        self.assertEqual(remote.fetches, 1)
        self.assertEqual([p.key for p in repo.load()], ["femur"])
        remote.version, remote.rows = 6, []
        self.assertTrue(repo.sync())                 # an empty set is still a valid copy
        self.assertEqual(repo.load(), [])
        self.assertTrue(self.cache.has_copy())


class Batch01DataTest(unittest.TestCase):
    """The B1 research files load into the app model and every FMA id is in the 3D model."""

    def test_batch_entries_resolve_and_load(self):
        sys.path.insert(0, str(ROOT / "database" / "body_parts_review"))
        try:
            import gen_body_parts as gen
        finally:
            sys.path.pop(0)
        folder = ROOT / "database" / "body_parts_review" / "b01"
        infos = gen.resolve(runpy.run_path(str(folder / "MANIFEST.py"))["ENTRIES"])
        parts = json.loads((ROOT / "assets" / "anatomy" / "parts.json").read_text(encoding="utf-8"))
        model_fmas = {p["fma"] for p in parts.values()}
        rows = []
        for f in sorted(folder.glob("out_*.py")):
            part = runpy.run_path(str(f))["PART"]
            self.assertEqual(gen.check(part, infos[part["key"]]), [], f.name)
            info = infos[part["key"]]
            self.assertTrue(set(info["fma_ids"]) <= model_fmas, f.name)
            rows.append({**info, **{k: v for k, v in part.items() if k not in ("clinical", "sources")},
                         "clinical": [{"text": t, "disease_id": d} for t, d in part["clinical"]],
                         "sources": [{"title": t, "url": u, "licence": l} for t, u, l in part["sources"]]})
        self.assertEqual(len(rows), 54)
        s = BodyPartService(type("R", (), {"load": lambda _s: [BodyPartInfo.from_row(r) for r in rows]})())
        femur = next(p for p in parts.values() if p["name"] == "left femur")
        self.assertTrue(s.describe(femur["fma"], femur["name"]).exact)
        head = next(p for p in parts.values() if p["name"] == "long head of left biceps brachii")
        self.assertEqual(s.describe(head["fma"], head["name"]).info.display_name, "Biceps brachii")
        appendix = next(p for p in parts.values() if p["name"] == "appendix")
        self.assertEqual(s.describe(appendix["fma"], "appendix").info.key, "appendix")  # not the large intestine


if __name__ == "__main__":
    unittest.main()
