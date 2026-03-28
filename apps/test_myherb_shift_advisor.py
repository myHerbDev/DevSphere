import unittest

from myherb_shift_advisor import PillarAssessment, generate_shift_report


class ShiftAdvisorTests(unittest.TestCase):
    def test_report_generation(self):
        assessments = [
            PillarAssessment("energy", 80),
            PillarAssessment("water", 70),
            PillarAssessment("waste", 60),
            PillarAssessment("packaging", 65),
            PillarAssessment("supply_chain", 75),
            PillarAssessment("community", 85),
        ]

        report = generate_shift_report(assessments)

        self.assertEqual(report.tier, "Progressing")
        self.assertAlmostEqual(report.weighted_score, 71.75)
        self.assertEqual(len(report.priorities), 3)

    def test_invalid_weight_sum(self):
        assessments = [
            PillarAssessment("energy", 80),
            PillarAssessment("water", 70),
            PillarAssessment("waste", 60),
            PillarAssessment("packaging", 65),
            PillarAssessment("supply_chain", 75),
            PillarAssessment("community", 85),
        ]

        with self.assertRaises(ValueError):
            generate_shift_report(
                assessments,
                {
                    "energy": 0.1,
                    "water": 0.1,
                    "waste": 0.1,
                    "packaging": 0.1,
                    "supply_chain": 0.1,
                    "community": 0.1,
                },
            )


if __name__ == "__main__":
    unittest.main()
