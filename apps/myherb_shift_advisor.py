"""myHerb Sustainability Shift Guidance Prototype.

A lightweight CLI-friendly module that helps organizations assess their
sustainability maturity and receive prioritized next steps.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


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
    """Generate a weighted sustainability shift report.

    Args:
        assessments: List of pillar scores.
        weights: Optional custom weighting by pillar.

    Returns:
        ShiftReport with aggregate score, maturity tier, and top priorities.
    """

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


def demo() -> ShiftReport:
    """Return a sample report for showcasing the application idea."""

    sample = [
        PillarAssessment("energy", 55),
        PillarAssessment("water", 62),
        PillarAssessment("waste", 48),
        PillarAssessment("packaging", 45),
        PillarAssessment("supply_chain", 52),
        PillarAssessment("community", 70),
    ]
    return generate_shift_report(sample)


if __name__ == "__main__":
    report = demo()
    print("myHerb Sustainability Shift Guidance")
    print(f"Weighted Score: {report.weighted_score}")
    print(f"Tier: {report.tier}")
    print("Top priorities:")
    for item in report.priorities:
        print(f"- {item}")
