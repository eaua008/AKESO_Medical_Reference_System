"""Study Hub sync: two computers, one in-memory "server"."""

import shutil
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.models.study import CardState, CardStateKind, Rating, ReviewLogEntry, StudySettings
from app.repositories.study_local_repository import StudyLocalRepository, iso, now_iso
from app.services.srs.sm2 import Sm2Scheduler
from app.services.study.study_sync import StudySync, replay

UID = "user-1"


class FakeRemote:
    """Enough of SupabaseStudyRepository for sync, with server stamps."""

    def __init__(self):
        self.decks, self.cards, self.states, self.reviews = {}, {}, {}, {}
        self.settings_row = None
        self.clock = 0
        self.review_uploads = 0

    def _stamp(self):
        self.clock += 1
        return f"2026-01-01T00:00:{self.clock:05d}"

    def user_id(self):
        return UID

    def decks_since(self, since):
        return [r for r in self.decks.values() if not since or r["server_updated_at"] > since]

    def official_deck_ids(self):
        return {i for i, r in self.decks.items() if r["origin"] == "official" and r.get("status") == "published"}

    def cards_since(self, since):
        return [r for r in self.cards.values() if not since or r["server_updated_at"] > since]

    def states_since(self, since):
        return [r for r in self.states.values() if not since or r["server_updated_at"] > since]

    def reviews_since(self, since):
        return [r for r in self.reviews.values() if not since or r["server_received_at"] > since]

    def settings(self):
        return self.settings_row

    def upsert_decks(self, rows):
        for r in rows:
            self.decks[r["id"]] = dict(r, server_updated_at=self._stamp())

    def upsert_cards(self, rows):
        for r in rows:
            self.cards[r["id"]] = dict(r, server_updated_at=self._stamp())

    def upsert_states(self, rows):
        for r in rows:
            self.states[r["card_key"]] = dict(r, server_updated_at=self._stamp())

    def push_reviews(self, rows):
        self.review_uploads += 1
        for r in rows:
            if r["client_id"] not in self.reviews:              # on conflict do nothing
                self.reviews[r["client_id"]] = dict(r, server_received_at=self._stamp())

    def upsert_settings(self, row):
        self.settings_row = dict(row)


class SyncTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.server = FakeRemote()
        self.sched = Sm2Scheduler(StudySettings())
        self.a = StudyLocalRepository(UID, self.dir / "a.db")
        self.b = StudyLocalRepository(UID, self.dir / "b.db")
        self.sync_a = StudySync(self.a, self.server, self.sched)
        self.sync_b = StudySync(self.b, self.server, self.sched)
        self.t0 = datetime(2026, 10, 18, 2, 0, tzinfo=timezone.utc)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def review(self, repo, key, rating, minutes):
        """What StudyService does after a rating: log it and store the new state."""
        when = self.t0 + timedelta(minutes=minutes)
        before = repo.states().get(key) or CardState(key)
        after = self.sched.answer(before, Rating(rating), when)
        repo.add_review(ReviewLogEntry(key, rating, when, state_before=before.state.value,
                                       interval_before=before.interval_days,
                                       interval_after=after.interval_days, ease_after=after.ease))
        repo.save_state(after)
        return after

    def test_interleaved_devices_converge(self):
        key = "auto:medicine:amoxicillin:class"
        self.review(self.a, key, 3, 0)          # A: good (learning step 1)
        self.sync_a.sync()
        self.sync_b.sync()
        self.review(self.b, key, 3, 11)          # B: good -> graduates
        self.review(self.a, key, 1, 12)          # A, offline: again
        self.sync_a.sync()
        self.sync_b.sync()
        self.sync_a.sync()
        sa, sb = self.a.states()[key], self.b.states()[key]
        self.assertEqual((sa.state, sa.reps, sa.due), (sb.state, sb.reps, sb.due))
        expected = replay(key, self.a.reviews(card_key=key), self.sched)
        self.assertEqual(sa.state, expected.state)
        self.assertEqual(len(self.server.reviews), 3)

    def test_duplicate_push_is_a_no_op(self):
        key = "card-1"
        self.review(self.a, key, 3, 0)
        entry = self.a.reviews()[0]
        self.sync_a.sync()
        self.assertEqual(len(self.server.reviews), 1)
        # the same review sent again (e.g. the first upload's answer was lost)
        self.server.push_reviews([{"client_id": entry.client_id, "card_key": key, "rating": 3,
                                   "reviewed_at": iso(entry.reviewed_at)}])
        self.assertEqual(len(self.server.reviews), 1)
        self.assertFalse(self.a.add_review(entry, synced=True))            # and locally too
        uploads = self.server.review_uploads
        self.sync_a.sync()
        self.assertEqual(self.server.review_uploads, uploads)               # nothing left to send

    def test_own_deck_edits_newest_wins_and_deletes_travel(self):
        deck = {"id": "d1", "title": "Mine", "origin": "personal", "updated_at": now_iso()}
        self.a.save_deck_row(deck, synced=False)
        self.a.save_card_row({"id": "c1", "deck_id": "d1", "type": "basic", "front": "F", "back": "B",
                              "updated_at": now_iso()}, synced=False)
        self.sync_a.sync()
        self.sync_b.sync()
        self.assertEqual(self.b.deck("d1").title, "Mine")
        self.assertEqual(len(self.b.cards("d1")), 1)
        later = (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat()
        self.b.save_card_row({"id": "c1", "deck_id": "d1", "type": "basic", "front": "F", "back": "B",
                              "updated_at": later, "deleted_at": later}, synced=False)
        self.sync_b.sync()
        self.sync_a.sync()
        self.assertEqual(self.a.cards("d1"), [])

    def test_reset_is_respected_after_sync(self):
        key = "card-2"
        self.review(self.a, key, 3, 0)
        self.review(self.a, key, 3, 11)
        self.sync_a.sync()
        reset_time = iso(self.t0 + timedelta(minutes=30))
        self.a.save_state(CardState(key), synced=False, reset_at=reset_time)
        self.sync_a.sync()
        self.sync_b.sync()
        self.assertEqual(self.b.states()[key].state, CardStateKind.NEW)

    def test_teaching_fields_hinted_and_local_settings_travel_right(self):
        self.a.save_deck_row({"id": "d2", "title": "Mine", "origin": "personal", "updated_at": now_iso()},
                             synced=False)
        self.a.save_card_row({"id": "c2", "deck_id": "d2", "type": "basic", "front": "F", "back": "B",
                              "answer_short": "Short", "explanation": "Why", "distinguish": "X: y",
                              "hint": "Think", "difficulty": "clinical", "updated_at": now_iso()}, synced=False)
        when = self.t0
        self.a.add_review(ReviewLogEntry("c2", 3, when, hinted=True))
        self.b.save_settings(StudySettings(type_answer=True, difficulties=["basic"]))
        self.server.settings_row = {"new_per_day": 5, "max_reviews": 50, "learning_steps": [1],
                                    "relearn_steps": [10], "updated_at": "2099-01-01T00:00:00+00:00"}
        self.b.save_settings(self.b.settings(), synced=True, updated_at="2000-01-01T00:00:00+00:00")
        self.sync_a.sync()
        self.sync_b.sync()
        card = self.b.cards("d2")[0]
        self.assertEqual((card.answer_short, card.explanation, card.distinguish, card.hint, card.difficulty),
                         ("Short", "Why", "X: y", "Think", "clinical"))
        self.assertTrue(self.b.reviews(card_key="c2")[0].hinted)
        settings = self.b.settings()
        self.assertEqual(settings.new_per_day, 5)                            # from the server
        self.assertEqual((settings.type_answer, settings.difficulties), (True, ["basic"]))   # kept here

    def test_unpublished_official_deck_disappears(self):
        self.server.decks["off"] = {"id": "off", "title": "Official", "origin": "official",
                                    "status": "published", "updated_at": now_iso(),
                                    "server_updated_at": self.server._stamp()}
        self.sync_a.sync()
        self.assertIsNotNone(self.a.deck("off"))
        self.server.decks["off"]["status"] = "draft"
        self.sync_a.sync()
        self.assertIsNone(self.a.deck("off"))


if __name__ == "__main__":
    unittest.main()
