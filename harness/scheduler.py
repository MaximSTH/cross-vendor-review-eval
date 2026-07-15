"""Session scheduler with within-batch condition interleaving (D-012).

Requirement: never a block of one arm, so mid-study vendor updates land on all
arms approximately equally. A1 rides inside the authoring session by definition;
A2 and B are independent review sessions that must follow their case's authoring.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum


class SessionKind(str, Enum):
    AUTHOR_A1 = "author+A1"   # authoring session, ends with in-session self-review
    REVIEW_A2 = "review_A2"   # fresh session, same vendor
    REVIEW_B = "review_B"     # fresh session, other vendor


@dataclass(frozen=True)
class ScheduledSession:
    case_id: str
    kind: SessionKind


_CYCLE = (SessionKind.AUTHOR_A1, SessionKind.REVIEW_A2, SessionKind.REVIEW_B)


def interleave(case_ids: list[str]) -> list[ScheduledSession]:
    """Produce a session order that rotates arms and respects author-first.

    Properties (tested):
      * an A2/B review of a case never precedes that case's authoring session,
      * while more than one kind has pending work, the same kind never runs
        more than twice consecutively.
    """
    authors = deque(case_ids)
    ready: dict[SessionKind, deque[str]] = {
        SessionKind.REVIEW_A2: deque(),
        SessionKind.REVIEW_B: deque(),
    }
    schedule: list[ScheduledSession] = []

    def pending() -> bool:
        return bool(authors or ready[SessionKind.REVIEW_A2] or ready[SessionKind.REVIEW_B])

    i = 0
    while pending():
        progressed = False
        for offset in range(len(_CYCLE)):
            kind = _CYCLE[(i + offset) % len(_CYCLE)]
            if kind is SessionKind.AUTHOR_A1 and authors:
                case = authors.popleft()
                schedule.append(ScheduledSession(case, kind))
                ready[SessionKind.REVIEW_A2].append(case)
                ready[SessionKind.REVIEW_B].append(case)
            elif kind is not SessionKind.AUTHOR_A1 and ready.get(kind):
                schedule.append(ScheduledSession(ready[kind].popleft(), kind))
            else:
                continue
            progressed = True
            i += offset + 1
            break
        if not progressed:  # defensive; cannot happen while pending() is True
            break
    return schedule
