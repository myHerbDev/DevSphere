"""myHerb Sustainability Shift Guidance Prototype.

A lightweight CLI module to assess sustainability maturity and recommend
prioritized next steps.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List


PILLARS = (
    "energy",
    "water",
    "waste",
    "packaging",
    "supply_chain",
    "community",
)


@dataclass(frozen=True)
class PillarAssessment:
    """A maturity score for a sustainability pillar (0-100)."""

    name: str
    score: int

    def __post_init__(self) -> None:
        if self.name not in PILLARS:
            raise ValueError(f"Unknown pillar: {self.name}")
        if not 0 <= self.score <= 100:
            raise ValueError("Score must be in the range 0..100")


@dataclass
class ShiftReport:
    weighted_score: float
    tier: str
    priorities: List[str]


def _default_weights() -> Dict[str, float]:
    return {
        "energy": 0.20,
        "water": 0.15,
        "waste": 0.20,
        "packaging": 0.15,
        "supply_chain": 0.20,
        "community": 0.10,
    }


def _tier_from_score(score: float) -> str:
    if score >= 80:
        return "Leader"
    if score >= 60:
        return "Progressing"
    if score >= 40:
        return "Emerging"
    return "Starter"


def generate_shift_report(
    assessments: List[PillarAssessment],
    weights: Dict[str, float] | None = None,
) -> ShiftReport:
    """Generate a weighted sustainability shift report."""

    if len(assessments) != len(PILLARS):
        raise ValueError("All pillars must be assessed exactly once")

    seen = {assessment.name for assessment in assessments}
    if seen != set(PILLARS):
        raise ValueError("Assessments must include each pillar exactly once")

    resolved_weights = weights or _default_weights()
    if set(resolved_weights) != set(PILLARS):
        raise ValueError("Weights must include all pillars")

    total_weight = sum(resolved_weights.values())
    if abs(total_weight - 1.0) > 1e-9:
        raise ValueError("Weights must sum to 1.0")

    score_map = {assessment.name: assessment.score for assessment in assessments}
    weighted_score = sum(score_map[p] * resolved_weights[p] for p in PILLARS)
    tier = _tier_from_score(weighted_score)

    underperforming = sorted(PILLARS, key=lambda p: score_map[p])[:3]
    priorities = [
        f"Increase {pillar.replace('_', ' ')} initiatives (current score: {score_map[pillar]})"
        for pillar in underperforming
    ]

    return ShiftReport(
        weighted_score=round(weighted_score, 2),
        tier=tier,
        priorities=priorities,
    )


def render_report(title: str, report: ShiftReport) -> str:
    """Render a report as a console-friendly text block."""

    priorities = "\n".join(f"- {item}" for item in report.priorities)
    return (
        f"\n{title}\n"
        f"Weighted Score: {report.weighted_score}\n"
        f"Tier: {report.tier}\n"
        "Top priorities:\n"
        f"{priorities}\n"
    )


def _assessments_from_scores(scores: Dict[str, int]) -> List[PillarAssessment]:
    return [PillarAssessment(name=pillar, score=scores[pillar]) for pillar in PILLARS]


def demo() -> ShiftReport:
    """Return a sample report for showcasing the application idea."""

    sample_scores = {
        "energy": 55,
        "water": 62,
        "waste": 48,
        "packaging": 45,
        "supply_chain": 52,
        "community": 70,
    }
    return generate_shift_report(_assessments_from_scores(sample_scores))


def watch_sample_shift() -> Iterable[str]:
    """Yield a simple quarter-by-quarter sustainability journey to watch progress."""

    snapshots = [
        (
            "Quarter 1 (Baseline)",
            {
                "energy": 45,
                "water": 54,
                "waste": 40,
                "packaging": 42,
                "supply_chain": 47,
                "community": 58,
            },
        ),
        (
            "Quarter 2 (Pilot Programs)",
            {
                "energy": 58,
                "water": 60,
                "waste": 52,
                "packaging": 56,
                "supply_chain": 54,
                "community": 65,
            },
        ),
        (
            "Quarter 3 (Scale-Up)",
            {
                "energy": 68,
                "water": 71,
                "waste": 64,
                "packaging": 66,
                "supply_chain": 63,
                "community": 72,
            },
        ),
    ]

    for label, scores in snapshots:
        report = generate_shift_report(_assessments_from_scores(scores))
        yield render_report(f"myHerb Sustainability Shift Guidance - {label}", report)


def run_watch_mode(
    interval_seconds: float = 1.5,
    loop_forever: bool = False,
    emit: Callable[[str], None] = print,
    sleeper: Callable[[float], None] = time.sleep,
) -> None:
    """Stream watch snapshots with a configurable delay."""

    if interval_seconds < 0:
        raise ValueError("Watch interval must be >= 0")

    while True:
        for block in watch_sample_shift():
            emit(block)
            sleeper(interval_seconds)
        if not loop_forever:
            return


def run_interactive_assessment() -> ShiftReport:
    """Collect scores from a user in the terminal and generate a report."""

    print("Enter your score for each pillar (0-100).")
    scores: Dict[str, int] = {}
    for pillar in PILLARS:
        while True:
            raw = input(f"{pillar.replace('_', ' ').title()}: ").strip()
            try:
                score = int(raw)
                assessment = PillarAssessment(name=pillar, score=score)
                scores[pillar] = assessment.score
                break
            except ValueError as error:
                print(f"Invalid input: {error}")

    return generate_shift_report(_assessments_from_scores(scores))


def main() -> None:
    parser = argparse.ArgumentParser(description="myHerb Sustainability Shift Guidance")
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch a quarter-by-quarter demo progression.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enter your own pillar scores in the terminal.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.5,
        help="Delay (seconds) between watch snapshots. Used with --watch.",
    )
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Repeat watch snapshots continuously. Used with --watch.",
    )
    args = parser.parse_args()

    if args.watch:
        run_watch_mode(interval_seconds=args.interval, loop_forever=args.loop)
        return

    if args.interactive:
        report = run_interactive_assessment()
        print(render_report("myHerb Sustainability Shift Guidance - Your Snapshot", report))
        return

    print(render_report("myHerb Sustainability Shift Guidance - Demo", demo()))


if __name__ == "__main__":
    main()
