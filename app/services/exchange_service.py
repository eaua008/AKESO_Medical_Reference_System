"""Business rules for Clinical Exchange.

Validation and the patient-data check run here first, so the student gets
the message straight away; the database checks everything again.
"""

import html
import json
from dataclasses import asdict
from pathlib import Path
from typing import Callable, Optional

from app.models.account import friendly_time
from app.models.exchange import (
    CASE, QUESTION, Draft, FeedPost, MemberProfile, ModItem, Notification, PostDetail,
    ProfileCard, Tag,
)
from app.models.notebook import INTERACTION_CASE, SYMPTOM_CASE, NotebookItem
from app.repositories.account_errors import AccountError
from app.repositories.exchange_repository import ExchangeRepository
from app.repositories.local_disease_cache import default_cache_path
from app.services.case_reference import label_lists, vignette_template
from app.services.phi_guard import find_phi, phi_message

PAGE_SIZE = 20
MAX_POLL_OPTIONS = 8
MAX_TAGS = 12


class ReferenceIndex:
    """Names from the encyclopedias, for tag and diagnosis pickers."""

    def __init__(self, diseases: Callable[[], list], symptoms: Callable[[], list],
                 medicines: Callable[[], list], body_systems: Callable[[], list]) -> None:
        self._diseases = diseases
        self._symptoms = symptoms
        self._medicines = medicines
        self._body_systems = body_systems

    def diseases(self) -> list[tuple[str, str]]:
        return sorted(((d.id, d.name) for d in self._safe(self._diseases)), key=lambda x: x[1])

    def body_systems(self) -> list[tuple[str, str]]:
        return sorted(((b.id, b.name) for b in self._safe(self._body_systems)), key=lambda x: x[1])

    def tag_options(self) -> list[Tag]:
        tags = [Tag("disease", d.id, d.name) for d in self._safe(self._diseases)]
        tags += [Tag("symptom", s.id, s.name) for s in self._safe(self._symptoms)]
        tags += [Tag("medicine", m.id, m.name) for m in self._safe(self._medicines)]
        tags += [Tag("body_system", b.id, b.name) for b in self._safe(self._body_systems)]
        return sorted(tags, key=lambda t: (t.label.lower(), t.kind))

    def find(self, kind: str, entry_id: str) -> Optional[Tag]:
        return next((t for t in self.tag_options() if t.kind == kind and t.id == entry_id), None)

    @staticmethod
    def _safe(source: Callable[[], list]) -> list:
        try:
            return list(source() or [])
        except Exception:  # noqa: BLE001 - an empty picker beats a crash when offline
            return []


class PostTitleCache:
    """Titles of posts seen, so Bookmarks can show a starred case offline."""

    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_cache_path().with_name("akeso_exchange_titles.json")
        try:
            self._data: dict = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self._data = {}

    def remember(self, post_id: str, title: str, kind: str, excerpt: str) -> None:
        entry = {"title": title, "kind": kind, "excerpt": excerpt[:200]}
        if self._data.get(post_id) != entry:
            self._data[post_id] = entry
            try:
                self._path.parent.mkdir(parents=True, exist_ok=True)
                self._path.write_text(json.dumps(self._data), encoding="utf-8")
            except OSError:
                pass

    def get(self, post_id: str) -> Optional[dict]:
        return self._data.get(post_id)


class ExchangeService:
    def __init__(self, repository: ExchangeRepository, reference: ReferenceIndex,
                 titles: Optional[PostTitleCache] = None) -> None:
        self._repo = repository
        self.reference = reference
        self.titles = titles or PostTitleCache()

    # ------------------------------------------------------------ reading

    def feed(self, tab: str = "newest", tag: Optional[Tag] = None,
             body_system: Optional[str] = None, program: Optional[str] = None,
             search: str = "", offset: int = 0) -> list[FeedPost]:
        rows = self._repo.feed(tab, tag.kind if tag else None, tag.id if tag else None,
                               body_system or None, program or None,
                               search.strip() or None, PAGE_SIZE, offset)
        posts = [FeedPost.from_json(r) for r in rows]
        for post in posts:
            self.titles.remember(post.id, post.title, post.kind, post.excerpt)
        return posts

    def post(self, post_id: str) -> PostDetail:
        detail = PostDetail.from_json(self._repo.post(post_id))
        self.titles.remember(detail.id, detail.title, detail.kind, detail.body or detail.question)
        return detail

    def profile_card(self, handle: str) -> ProfileCard:
        return ProfileCard.from_json(self._repo.profile_card(handle))

    def profile(self, handle: str) -> MemberProfile:
        """A member's profile page (raises AccountError if it is private)."""
        return MemberProfile.from_json(self._repo.profile(handle))

    def follow_user(self, handle: str, on: bool) -> bool:
        return self._repo.follow_user(handle, on)

    def mod_queue(self) -> list[ModItem]:
        return [ModItem.from_json(r) for r in self._repo.mod_queue()]

    # ------------------------------------------------------------ writing

    def check_text(self, *texts: str) -> Optional[str]:
        """The patient-data warning for texts being typed, or None."""
        found = find_phi(*texts)
        return phi_message(found) if found else None

    def validate(self, draft: Draft) -> dict:
        title = " ".join(draft.title.split())
        body = draft.body.strip()
        question = draft.question.strip()
        if len(title) < 5:
            raise AccountError("Give the post a title of at least 5 characters.")
        if len(title) > 140:
            raise AccountError("Keep the title under 140 characters.")
        if draft.kind == CASE and not body:
            raise AccountError("Describe the case (the vignette) before posting.")
        if draft.kind == QUESTION and not body:
            raise AccountError("Write your question before posting.")
        if len(body) > 5000:
            raise AccountError("The description can be at most 5,000 characters.")
        warning = self.check_text(title, body, question, draft.setting or "")
        if warning:
            raise AccountError(warning)
        options = []
        seen = set()
        for option in draft.poll_options:
            label = " ".join((option.get("label") or "").split())[:80]
            key = option.get("disease_id") or label.lower()
            if label and key not in seen:
                seen.add(key)
                options.append({"disease_id": option.get("disease_id") or None, "label": label})
        if len(options) > MAX_POLL_OPTIONS:
            raise AccountError(f"A poll can start with at most {MAX_POLL_OPTIONS} choices.")
        if len(options) == 1:
            raise AccountError("Give the poll at least 2 choices (others can suggest more).")
        tags = list({(t.kind, t.id): t for t in draft.tags}.values())
        if len(tags) > MAX_TAGS:
            raise AccountError(f"Use at most {MAX_TAGS} tags.")
        return {
            "p_kind": draft.kind, "p_title": title, "p_body": body, "p_question": question,
            "p_anonymous": draft.anonymous,
            "p_age_range": draft.age_range if draft.kind == CASE else None,
            "p_sex": draft.sex if draft.kind == CASE else None,
            "p_setting": draft.setting if draft.kind == CASE else None,
            "p_vitals": draft.vitals if draft.kind == CASE else None,
            "p_case": draft.case_data or {}, "p_source": draft.source,
            "p_tags": [t.to_json() for t in tags], "p_poll_options": options,
        }

    def create(self, draft: Draft) -> str:
        return self._repo.create_post(self.validate(draft))

    def edit(self, post: PostDetail, title: str, body: str, question: str, tags: list[Tag]) -> None:
        draft = Draft(kind=post.kind, title=title, body=body, question=question, tags=tags)
        payload = self.validate(draft)
        self._repo.edit_post(post.id, payload["p_title"], payload["p_body"],
                             payload["p_question"], payload["p_tags"])

    def delete(self, post_id: str) -> None:
        self._repo.delete_post(post_id)

    def reply(self, post_id: str, parent_id: Optional[str], body: str, anonymous: bool) -> str:
        body = body.strip()
        if not body:
            raise AccountError("Write a reply first.")
        if len(body) > 3000:
            raise AccountError("Replies can be at most 3,000 characters.")
        warning = self.check_text(body)
        if warning:
            raise AccountError(warning)
        return self._repo.reply(post_id, parent_id, body, anonymous)

    def option_comment(self, post_id: str, option_id: str, body: str, anonymous: bool) -> str:
        """A comment on one poll choice: same rules as a reply."""
        body = body.strip()
        if not body:
            raise AccountError("Write a comment first.")
        if len(body) > 3000:
            raise AccountError("Comments can be at most 3,000 characters.")
        warning = self.check_text(body)
        if warning:
            raise AccountError(warning)
        return self._repo.option_comment(post_id, option_id, body, anonymous)

    def edit_reply(self, reply_id: str, body: str) -> None:
        warning = self.check_text(body)
        if warning:
            raise AccountError(warning)
        if not body.strip():
            raise AccountError("A reply can't be empty. Delete it instead.")
        self._repo.edit_reply(reply_id, body.strip())

    def delete_reply(self, reply_id: str) -> None:
        self._repo.delete_reply(reply_id)

    def vote(self, kind: str, target_id: str, on: bool) -> int:
        return self._repo.vote(kind, target_id, on)

    def best_answer(self, post_id: str, reply_id: Optional[str]) -> None:
        self._repo.best_answer(post_id, reply_id)

    def verify(self, reply_id: str, on: bool) -> None:
        self._repo.verify_reply(reply_id, on)

    def follow(self, post_id: str, on: bool) -> None:
        self._repo.follow(post_id, on)

    # --------------------------------------------------------------- poll

    def suggest(self, post_id: str, disease_id: Optional[str], label: str) -> str:
        label = " ".join((label or "").split())
        if not disease_id and len(label) < 2:
            raise AccountError("Pick a disease from the list or type a diagnosis.")
        return self._repo.poll_suggest(post_id, disease_id or None, label)

    def poll_vote(self, post_id: str, option_id: Optional[str]) -> None:
        self._repo.poll_vote(post_id, option_id)

    def reveal(self, post_id: str, option_id: str, explanation: str) -> None:
        if not option_id:
            raise AccountError("Choose the intended answer.")
        warning = self.check_text(explanation)
        if warning:
            raise AccountError(warning)
        self._repo.poll_reveal(post_id, option_id, explanation.strip())

    # --------------------------------------------------------- moderation

    def report(self, kind: str, target_id: str, reason: str, note: str) -> None:
        self._repo.report(kind, target_id, reason, note.strip())

    def moderate(self, kind: str, target_id: str, action: str, reason: str) -> None:
        self._repo.moderate(kind, target_id, action, reason.strip())

    def dismiss(self, kind: str, target_id: str) -> None:
        self._repo.dismiss_reports(kind, target_id)

    # ------------------------------------------------- drafts from elsewhere

    def draft_for_tag(self, kind: str, entry_id: str) -> Draft:
        """ "Present Case" on a disease, symptom or medicine page."""
        tag = self.reference.find(kind, entry_id)
        draft = Draft(kind=CASE, tags=[tag] if tag else [])
        if tag and kind == "disease":
            draft.title = f"Case: suspected {tag.label}?"
        return draft

    def draft_from_notebook(self, item: NotebookItem,
                            describe_interaction: Optional[Callable[[str, list, list], dict]] = None
                            ) -> Draft:
        """A saved checker case as a post. Only de-identified, structured
        fields travel: age range, sex, vitals, symptoms, medicines."""
        draft = Draft(kind=CASE, title=item.title, attached_from=item.title)
        symptom = item.symptom_data
        interaction = item.interaction_data
        tags: list[Tag] = []
        if symptom.get("symptoms"):
            draft.source = SYMPTOM_CASE
            draft.age_range = symptom.get("age_range")
            draft.sex = symptom.get("sex")
            draft.setting = symptom.get("setting") or None
            draft.vitals = symptom.get("vitals") or None
            labels = label_lists(symptom)
            draft.case_data = {
                "symptoms": [{k: s.get(k) for k in ("symptom_id", "name", "intensity", "onset",
                                                    "pattern", "trend", "duration")}
                             for s in symptom.get("symptoms", [])],
                "comorbidities": labels["comorbidities"], "exposures": labels["exposures"],
                "family_history": labels["family_history"],
            }
            draft.body = symptom.get("vignette") or vignette_template(symptom, draft.setting or "")
            for s in symptom.get("symptoms", []):
                tag = self.reference.find("symptom", s.get("symptom_id", ""))
                if tag:
                    tags.append(tag)
        if interaction.get("candidate_id"):
            draft.source = draft.source or INTERACTION_CASE
            regimen = list(interaction.get("regimen_ids") or [])
            conditions = list(interaction.get("condition_ids") or [])
            described = describe_interaction(interaction["candidate_id"], regimen, conditions) \
                if describe_interaction else {}
            draft.case_data["candidate"] = {"id": interaction["candidate_id"],
                                            "name": described.get("candidate", "")}
            draft.case_data["regimen"] = [{"id": m, "name": n} for m, n in
                                          zip(regimen, described.get("regimen", regimen))]
            draft.case_data["conditions"] = described.get("conditions", conditions)
            if not draft.body:
                names = ", ".join(r["name"] for r in draft.case_data["regimen"])
                draft.body = (f"Adding {draft.case_data['candidate']['name'] or 'a medicine'} "
                              f"to a regimen of {names or 'no other medicines'}"
                              + (f" in a patient with {', '.join(draft.case_data['conditions'])}"
                                 if draft.case_data["conditions"] else "") + ".")
            for medicine_id in [interaction["candidate_id"], *regimen]:
                tag = self.reference.find("medicine", medicine_id)
                if tag:
                    tags.append(tag)
        draft.tags = list({(t.kind, t.id): t for t in tags}.values())[:MAX_TAGS]
        draft.question = "What is your differential, and what would you check next?" \
            if symptom.get("symptoms") else "Is this combination safe? What would you monitor?"
        return draft

    # ----------------------------------------------- copy into the notebook

    @staticmethod
    def notebook_copy(post: PostDetail) -> tuple[str, str]:
        """(title, HTML) for "Save to notebook": the case and its discussion,
        with anonymous authors kept anonymous."""
        e = html.escape
        parts = [f"<h2>{e(post.title)}</h2>",
                 f"<p><i>From Clinical Exchange · {e(post.author.name)} · "
                 f"{e(friendly_time(post.created_at))}</i></p>"]
        details = [x for x in (post.age_range and f"{post.age_range} y/o",
                               post.sex, post.setting) if x]
        if details:
            parts.append(f"<p><b>Patient:</b> {e(', '.join(details))}</p>")
        if post.body:
            parts.append(f"<p>{e(post.body)}</p>")
        if post.question:
            parts.append(f"<p><b>Question:</b> {e(post.question)}</p>")
        if post.poll:
            rows = "".join(
                f"<li>{e(o.label)}" + (f" — {o.votes} votes" if o.votes is not None else "")
                + (" <b>(intended answer)</b>" if o.id == post.poll.revealed_option else "")
                + "</li>" for o in post.poll.options)
            parts.append(f"<p><b>Differential poll</b></p><ul>{rows}</ul>")
            if post.poll.explanation:
                parts.append(f"<p><b>Explanation:</b> {e(post.poll.explanation)}</p>")
        if post.replies:
            parts.append("<h3>Discussion</h3>")
            for reply in post.all_replies():
                if reply.status != "open":
                    continue
                marks = " ".join(m for m in ("★ Best answer" if reply.is_best else "",
                                             "✓ Educator verified" if reply.verified else "") if m)
                parts.append(f"<p><b>{e(reply.author.name)}</b>"
                             + (f" ({e(marks)})" if marks else "")
                             + f": {e(reply.body)}</p>")
        return post.title, "".join(parts)


class NotificationService:
    def __init__(self, repository: ExchangeRepository) -> None:
        self._repo = repository

    def latest(self, before: Optional[int] = None) -> list[Notification]:
        return [Notification.from_json(r) for r in self._repo.notifications(30, before)]

    def unread_count(self) -> int:
        return self._repo.unread_count()

    def mark_read(self, ids: Optional[list[int]] = None) -> None:
        self._repo.mark_read(ids)

    def clear_read(self) -> None:
        self._repo.clear_read()


def draft_json(draft: Draft) -> dict:
    """For debugging and tests."""
    data = asdict(draft)
    data["tags"] = [t.to_json() for t in draft.tags]
    return data
