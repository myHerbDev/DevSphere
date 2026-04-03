import unittest

from myherb_shift_advisor import (
    PillarAssessment,
    generate_shift_report,
    render_report,
    run_watch_mode,
    watch_sample_shift,
)


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

    def test_render_report_contains_basics(self):
        assessments = [
            PillarAssessment("energy", 80),
            PillarAssessment("water", 70),
            PillarAssessment("waste", 60),
            PillarAssessment("packaging", 65),
            PillarAssessment("supply_chain", 75),
            PillarAssessment("community", 85),
        ]
        report = generate_shift_report(assessments)
        output = render_report("Test", report)

        self.assertIn("Weighted Score", output)
        self.assertIn("Top priorities", output)

    def test_watch_mode_has_three_snapshots(self):
        snapshots = list(watch_sample_shift())

        self.assertEqual(len(snapshots), 3)
        self.assertIn("Quarter 1", snapshots[0])
        self.assertIn("Quarter 3", snapshots[-1])

    def test_run_watch_mode_emits_all_snapshots(self):
        seen = []
        run_watch_mode(
            interval_seconds=0,
            loop_forever=False,
            emit=seen.append,
            sleeper=lambda _: None,
        )

        self.assertEqual(len(seen), 3)

    def test_run_watch_mode_rejects_negative_interval(self):
        with self.assertRaises(ValueError):
            run_watch_mode(interval_seconds=-0.5, sleeper=lambda _: None)


if __name__ == "__main__":
    unittest.main()
