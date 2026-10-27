"""SM-2 with learning steps (the scheme Anki popularised).

    new / learning   steps of minutes (1 min, 10 min); Good moves on a step,
                     the last step graduates the card to review (1 day);
                     Easy graduates at once (4 days); Again starts over
    review           Again  -> a lapse: ease -0.20 (not below 1.3), relearn
                               (10 min), and the interval is halved (min 1 d)
                     Hard   -> interval x 1.2, ease -0.15
                     Good   -> interval x ease
                     Easy   -> interval x ease x 1.3, ease +0.15
    relearning       steps of minutes again, then back to review with the
                     halved interval

Review intervals are whole days counted from the start of the study day
(04:00), so a card is due from 04:00 on its day. Intervals of 3 days or
more get a small fuzz (+-5%), the same for the same card on the same day,
so cards learned together don't stay bunched together forever.
"""

import hashlib
from datetime import datetime, timedelta

from app.models.study import CardState, CardStateKind, Rating
from app.services.srs.scheduler import Scheduler, day_number, day_start

S = CardStateKind


class Sm2Scheduler(Scheduler):
    # ------------------------------------------------------------ helpers

    def _minutes(self, steps: list[int], index: int) -> float:
        steps = steps or [1]
        return float(steps[min(index, len(steps) - 1)])

    def _due_in_days(self, now: datetime, days: float, key: str) -> tuple[datetime, float]:
        days = max(1.0, round(days))
        days = self._fuzz(days, key, now)
        return day_start(now, self.settings.day_starts_at_hour) + timedelta(days=days), days

    def _fuzz(self, days: float, key: str, now: datetime) -> float:
        if days < 3:
            return days
        seed = f"{key}:{day_number(now, self.settings.day_starts_at_hour)}".encode()
        unit = int(hashlib.sha256(seed).hexdigest()[:8], 16) / 0xFFFFFFFF     # 0..1, stable
        spread = max(1.0, days * 0.05)
        return float(max(1, round(days + (unit * 2 - 1) * spread)))

    def _graduate(self, state: CardState, now: datetime, days: float, rating: Rating) -> CardState:
        due, days = self._due_in_days(now, days, state.card_key)
        return state.copy(state=S.REVIEW, due=due, interval_days=days, step=0,
                          reps=state.reps + 1, last_rating=int(rating), last_review=now)

    # ------------------------------------------------------------- answer

    def answer(self, state: CardState, rating: Rating, now: datetime) -> CardState:
        rating = Rating(int(rating))
        s = self.settings
        if state.state in (S.NEW, S.LEARNING):
            if state.state == S.NEW:
                state = state.copy(ease=s.start_ease, step=0)
            steps = s.learning_steps or [1]
            if rating == Rating.EASY:
                return self._graduate(state, now, s.easy_days, rating)
            if rating == Rating.AGAIN:
                step = 0
                minutes = self._minutes(steps, 0)
            elif rating == Rating.HARD:
                step = state.step
                here = self._minutes(steps, step)
                after = self._minutes(steps, step + 1) if step + 1 < len(steps) else here * 1.5
                minutes = (here + after) / 2 if step == 0 and len(steps) > 1 else here
            else:                                           # GOOD
                step = state.step + 1
                if step >= len(steps):
                    return self._graduate(state, now, s.graduating_days, rating)
                minutes = self._minutes(steps, step)
            return state.copy(state=S.LEARNING, step=step, due=now + timedelta(minutes=minutes),
                              reps=state.reps + 1, last_rating=int(rating), last_review=now)

        if state.state == S.RELEARNING:
            steps = s.relearn_steps or [10]
            if rating == Rating.AGAIN:
                return state.copy(step=0, due=now + timedelta(minutes=self._minutes(steps, 0)),
                                  reps=state.reps + 1, last_rating=int(rating), last_review=now)
            if rating == Rating.HARD:
                return state.copy(due=now + timedelta(minutes=self._minutes(steps, state.step)),
                                  reps=state.reps + 1, last_rating=int(rating), last_review=now)
            next_step = state.step + 1
            if rating == Rating.GOOD and next_step < len(steps):
                return state.copy(step=next_step,
                                  due=now + timedelta(minutes=self._minutes(steps, next_step)),
                                  reps=state.reps + 1, last_rating=int(rating), last_review=now)
            days = state.interval_days + (1 if rating == Rating.EASY else 0)
            return self._graduate(state, now, max(1.0, days), rating)

        if state.state == S.REVIEW:
            prev = max(1.0, state.interval_days)
            if rating == Rating.AGAIN:
                ease = max(s.min_ease, state.ease - 0.20)
                minutes = self._minutes(s.relearn_steps or [10], 0)
                return state.copy(state=S.RELEARNING, step=0, ease=ease,
                                  interval_days=max(1.0, round(prev * 0.5)),
                                  due=now + timedelta(minutes=minutes), lapses=state.lapses + 1,
                                  reps=state.reps + 1, last_rating=int(rating), last_review=now)
            hard = max(prev * 1.2, prev + 1)
            if rating == Rating.HARD:
                ease = max(s.min_ease, state.ease - 0.15)
                days = hard
            elif rating == Rating.GOOD:
                ease = state.ease
                days = max(prev * state.ease, hard + 1)
            else:                                           # EASY
                ease = state.ease + 0.15
                days = max(prev * state.ease * 1.3, prev * state.ease + 1, hard + 2)
            due, days = self._due_in_days(now, days, state.card_key)
            return state.copy(ease=ease, interval_days=days, due=due, reps=state.reps + 1,
                              last_rating=int(rating), last_review=now)

        return state                                        # suspended: unchanged
