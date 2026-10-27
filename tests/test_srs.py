"""SM-2 scheduler, day boundary and today's queue.   python -m unittest discover tests"""

import os
import time
import unittest
from datetime import datetime, timedelta

os.environ["TZ"] = "Asia/Manila"
if hasattr(time, "tzset"):
    time.tzset()

from app.models.study import CardState, CardStateKind as S, Rating, ReviewLogEntry, StudySettings  # noqa: E402
from app.services.srs.queue import build_queue, new_seen_today, next_card  # noqa: E402
from app.services.srs.scheduler import day_start, interval_label  # noqa: E402
from app.services.srs.sm2 import Sm2Scheduler  # noqa: E402


def at(text: str) -> datetime:
    """A local wall-clock time as an aware datetime."""
    return datetime.fromisoformat(text).astimezone()


class DayBoundaryTest(unittest.TestCase):
    def test_day_starts_at_four(self):
        self.assertEqual(day_start(at("2026-10-18T03:59")).date().isoformat(), "2026-10-17")
        self.assertEqual(day_start(at("2026-10-18T04:00")).date().isoformat(), "2026-10-18")
        self.assertEqual(day_start(at("2026-10-18T23:30")).hour, 4)

    def test_labels(self):
        self.assertEqual(interval_label(60), "1 min")
        self.assertEqual(interval_label(600), "10 min")
        self.assertEqual(interval_label(86400 * 3), "3 d")


class LearningTest(unittest.TestCase):
    def setUp(self):
        self.s = Sm2Scheduler(StudySettings())
        self.now = at("2026-10-18T10:00")
        self.new = CardState("k1")

    def test_new_again_is_one_minute(self):
        after = self.s.answer(self.new, Rating.AGAIN, self.now)
        self.assertEqual(after.state, S.LEARNING)
        self.assertEqual(after.due - self.now, timedelta(minutes=1))

    def test_new_good_then_good_graduates_to_one_day(self):
        one = self.s.answer(self.new, Rating.GOOD, self.now)
        self.assertEqual((one.state, one.step), (S.LEARNING, 1))
        self.assertEqual(one.due - self.now, timedelta(minutes=10))
        two = self.s.answer(one, Rating.GOOD, self.now + timedelta(minutes=10))
        self.assertEqual(two.state, S.REVIEW)
        self.assertEqual(two.interval_days, 1)
        self.assertEqual(two.due, day_start(self.now) + timedelta(days=1))   # tomorrow 04:00

    def test_new_easy_graduates_to_four_days(self):
        after = self.s.answer(self.new, Rating.EASY, self.now)
        self.assertEqual(after.state, S.REVIEW)
        self.assertIn(after.interval_days, (4, 3, 5))        # 4 days, fuzz may move it one day
        self.assertEqual(after.ease, 2.5)

    def test_hard_on_first_step_is_between_the_steps(self):
        after = self.s.answer(self.new, Rating.HARD, self.now)
        self.assertEqual(after.due - self.now, timedelta(minutes=5.5))

    def test_learning_again_restarts(self):
        one = self.s.answer(self.new, Rating.GOOD, self.now)
        again = self.s.answer(one, Rating.AGAIN, self.now)
        self.assertEqual(again.step, 0)
        self.assertEqual(again.due - self.now, timedelta(minutes=1))


class ReviewTest(unittest.TestCase):
    def setUp(self):
        self.s = Sm2Scheduler(StudySettings())
        self.now = at("2026-10-18T10:00")
        self.card = CardState("review-card", state=S.REVIEW, interval_days=10, ease=2.5,
                              due=self.now, reps=5)

    def test_again_is_a_lapse(self):
        after = self.s.answer(self.card, Rating.AGAIN, self.now)
        self.assertEqual(after.state, S.RELEARNING)
        self.assertEqual(after.lapses, 1)
        self.assertAlmostEqual(after.ease, 2.3)
        self.assertEqual(after.interval_days, 5)
        self.assertEqual(after.due - self.now, timedelta(minutes=10))

    def test_ease_never_below_minimum(self):
        low = self.card.copy(ease=1.35)
        self.assertAlmostEqual(self.s.answer(low, Rating.AGAIN, self.now).ease, 1.3)
        self.assertAlmostEqual(self.s.answer(low, Rating.HARD, self.now).ease, 1.3)

    def test_relearning_good_returns_to_review_with_half_interval(self):
        lapse = self.s.answer(self.card, Rating.AGAIN, self.now)
        back = self.s.answer(lapse, Rating.GOOD, self.now + timedelta(minutes=10))
        self.assertEqual(back.state, S.REVIEW)
        self.assertAlmostEqual(back.interval_days, 5, delta=1)

    def test_hard_good_easy_grow(self):
        hard = self.s.answer(self.card, Rating.HARD, self.now)
        good = self.s.answer(self.card, Rating.GOOD, self.now)
        easy = self.s.answer(self.card, Rating.EASY, self.now)
        self.assertAlmostEqual(hard.interval_days, 12, delta=1)
        self.assertAlmostEqual(good.interval_days, 25, delta=2)
        self.assertAlmostEqual(easy.interval_days, 32.5, delta=2)
        self.assertLess(hard.interval_days, good.interval_days)
        self.assertLess(good.interval_days, easy.interval_days)
        self.assertAlmostEqual(hard.ease, 2.35)
        self.assertAlmostEqual(good.ease, 2.5)
        self.assertAlmostEqual(easy.ease, 2.65)

    def test_fuzz_is_stable_and_small(self):
        a = self.s.answer(self.card, Rating.GOOD, self.now)
        b = self.s.answer(self.card, Rating.GOOD, self.now + timedelta(hours=2))
        self.assertEqual(a.interval_days, b.interval_days)          # same card, same day
        self.assertLessEqual(abs(a.interval_days - 25), 2)

    def test_due_is_at_day_start(self):
        good = self.s.answer(self.card, Rating.GOOD, self.now)
        self.assertEqual(good.due.hour, 4)

    def test_preview_labels(self):
        labels = self.s.preview(CardState("x"), self.now)
        self.assertEqual(labels[Rating.AGAIN], "1 min")
        self.assertEqual(labels[Rating.GOOD], "10 min")
        self.assertTrue(labels[Rating.EASY].endswith("d"))


class QueueTest(unittest.TestCase):
    def setUp(self):
        self.now = at("2026-10-18T10:00")
        self.settings = StudySettings(new_per_day=2, max_reviews=2)

    def test_order_learning_then_reviews_then_new(self):
        states = {
            "learn": CardState("learn", state=S.LEARNING, due=self.now - timedelta(minutes=1)),
            "rev_old": CardState("rev_old", state=S.REVIEW, due=self.now - timedelta(days=3)),
            "rev_new": CardState("rev_new", state=S.REVIEW, due=self.now - timedelta(days=1)),
            "rev_late": CardState("rev_late", state=S.REVIEW, due=self.now - timedelta(hours=1)),
            "future": CardState("future", state=S.REVIEW, due=self.now + timedelta(days=2)),
            "susp": CardState("susp", state=S.SUSPENDED),
        }
        keys = ["n1", "rev_new", "n2", "learn", "rev_old", "future", "susp", "n3", "rev_late"]
        q = build_queue(keys, states, self.settings, [], self.now)
        self.assertEqual(q.order, ["learn", "rev_old", "rev_new", "n1", "n2"])   # caps: 2 reviews, 2 new

    def test_new_cards_seen_today_count(self):
        log = [ReviewLogEntry("n1", 3, self.now - timedelta(hours=1), state_before="new"),
               ReviewLogEntry("n1", 3, self.now - timedelta(minutes=50), state_before="learning"),
               ReviewLogEntry("old", 3, self.now - timedelta(days=1), state_before="new")]
        self.assertEqual(new_seen_today(log, self.now), 1)
        q = build_queue(["a", "b", "c"], {}, self.settings, log, self.now)
        self.assertEqual(q.new, ["a"])

    def test_learning_due_soon_is_shown_when_nothing_else(self):
        states = {"l": CardState("l", state=S.LEARNING, due=self.now + timedelta(minutes=8))}
        q = build_queue(["l"], states, self.settings, [], self.now)
        self.assertEqual(q.order, [])
        self.assertEqual(next_card(q, states, self.now), "l")
        far = {"l": CardState("l", state=S.LEARNING, due=self.now + timedelta(hours=2))}
        q2 = build_queue(["l"], far, self.settings, [], self.now)
        self.assertIsNone(next_card(q2, far, self.now))


if __name__ == "__main__":
    unittest.main()
