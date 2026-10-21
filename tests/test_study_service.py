import shutil
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.models.study import Card, CardStateKind, CardType, Choice, Rating
from app.repositories.study_local_repository import StudyLocalRepository
from app.services.study.study_service import StudyService
from tests.test_auto_cards import diseases, medicines


class Clock:
    def __init__(self):
        self.now = datetime(2026, 10, 18, 2, 0, tzinfo=timezone.utc)      # 10:00 in Manila

    def __call__(self):
        return self.now


class ServiceTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.clock = Clock()
        self.service = StudyService(StudyLocalRepository("me", self.dir / "s.db"),
                                    diseases=diseases, medicines=medicines, clock=self.clock)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_make_deck_review_and_undo(self):
        deck = self.service.create_deck("Pharm finals", "pharmacology")
        self.service.save_card(Card("", deck.id, front="Class of amoxicillin?", back="Penicillin"))
        self.service.save_card(Card("", deck.id, type=CardType.MCQ, front="Which is a macrolide?",
                                    choices=[Choice("Azithromycin", True, "Yes."), Choice("Amoxicillin")]))
        with self.assertRaises(ValueError):
            self.service.save_card(Card("", deck.id, type=CardType.CLOZE, cloze_text="no blank"))
        q = self.service.queue(deck.id)
        self.assertEqual(len(q.new), 2)
        key = self.service.next_key(q)
        undo = self.service.answer(key, Rating.GOOD)
        self.assertEqual(self.service.state(key).state, CardStateKind.LEARNING)
        self.service.undo(undo)
        self.assertEqual(self.service.state(key).state, CardStateKind.NEW)
        self.assertEqual(self.service.local.reviews(), [])

    def test_today_counts_and_streak(self):
        auto = self.service.auto()
        deck_id = next(d.id for d in auto.decks if "Antibiotic" in d.title)
        key = self.service.next_key(self.service.queue(deck_id))
        self.service.answer(key, Rating.EASY)                      # graduates for ~4 days
        due, new = self.service.due_today()
        self.assertEqual(due, 0)
        self.assertGreater(new, 0)                                   # the started deck offers new cards
        self.assertEqual(self.service.streak(), 1)
        self.clock.now += timedelta(days=5)
        due, _new = self.service.due_today()
        self.assertEqual(due, 1)
        self.assertEqual(self.service.streak(), 0)                   # missed yesterday

    def test_retired_keys_and_updated_badge(self):
        from app.models.study import CardState
        old = CardState("auto:medicine:amoxicillin:class", state=CardStateKind.REVIEW,
                        due=self.clock.now - timedelta(days=1), interval_days=3)
        self.service.local.save_state(old)
        self.assertEqual(sum(n for _d, n in self.service.forecast(7)), 0)    # the old card is retired
        self.assertEqual(self.service.due_today()[0], 0)
        card = self.service.auto().all_cards()[0]
        self.service.answer(card.card_key, Rating.GOOD)
        self.assertFalse(self.service.is_updated(card))
        card.content_hash = "changed"
        self.assertTrue(self.service.is_updated(card))
        self.assertNotEqual(self.service.state(card.card_key).state, CardStateKind.NEW)   # state kept

    def test_filters_and_hinted(self):
        deck = self.service.create_deck("Mixed")
        basic = self.service.save_card(Card("", deck.id, front="B?", back="B", difficulty="basic"))
        self.service.save_card(Card("", deck.id, front="C?", back="C", difficulty="clinical"))
        self.service.save_card(Card("", deck.id, front="None?", back="N"))        # unset counts as basic
        self.assertEqual(len(self.service.queue(deck.id).new), 3)
        self.assertEqual(len(self.service.queue(deck.id, difficulties=["clinical"]).new), 1)
        self.assertEqual(len(self.service.queue(deck.id, difficulties=["basic"]).new), 2)
        auto = self.service.auto()
        auto_deck = next(d.id for d in auto.decks if "Antibiotic" in d.title)
        only_calc = self.service.queue(auto_deck, families=["rx_calc"])
        fams = {c.family for c in self.service.cards(auto_deck) if c.card_key in only_calc.new}
        self.assertLessEqual(fams, {"rx_calc"})
        self.service.answer(basic.card_key, Rating.GOOD, hinted=True)
        self.assertTrue(self.service.local.reviews(card_key=basic.card_key)[0].hinted)

    def test_teaching_fields_are_checked_and_kept(self):
        deck = self.service.create_deck("Teach")
        with self.assertRaises(ValueError):
            self.service.save_card(Card("", deck.id, front="F", back="B", hint="x" * 201))
        with self.assertRaises(ValueError):
            self.service.save_card(Card("", deck.id, front="F", back="B", difficulty="expert"))
        saved = self.service.save_card(Card("", deck.id, front="F", back="B", answer_short="Short",
                                            explanation="Why", distinguish="X: y", hint="H",
                                            difficulty="advanced"))
        again = self.service.card(saved.card_key)
        self.assertEqual((again.answer_short, again.explanation, again.distinguish, again.hint, again.difficulty),
                         ("Short", "Why", "X: y", "H", "advanced"))

    def test_reset_and_delete(self):
        deck = self.service.create_deck("Temp")
        card = self.service.save_card(Card("", deck.id, front="F", back="B"))
        self.service.answer(card.card_key, Rating.EASY)
        self.service.reset_deck(deck.id)
        self.assertEqual(self.service.state(card.card_key).state, CardStateKind.NEW)
        self.service.delete_deck(deck.id)
        self.assertIsNone(self.service.local.deck(deck.id))
        self.assertEqual(self.service.my_cards_deck().title, "My cards")


if __name__ == "__main__":
    unittest.main()
