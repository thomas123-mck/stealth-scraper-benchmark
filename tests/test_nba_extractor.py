"""
Unit tests for NBA Live In-Game Micro-Betting Data Extraction Suite.
Validates odds conversion math, payload normalization, export formats, and schema integrity.
"""

import os
import tempfile
import unittest

from nba_microbetting_extractor import (
    NBAMicrobettingExtractor,
    american_to_decimal,
    american_to_probability,
)


class TestNBAMicrobettingExtractor(unittest.TestCase):
    def test_american_to_decimal_positive(self):
        self.assertEqual(american_to_decimal(+100), 2.0)
        self.assertEqual(american_to_decimal(+150), 2.5)
        self.assertEqual(american_to_decimal(+200), 3.0)

    def test_american_to_decimal_negative(self):
        self.assertEqual(american_to_decimal(-100), 2.0)
        self.assertEqual(american_to_decimal(-200), 1.5)
        self.assertEqual(american_to_decimal(-400), 1.25)

    def test_american_to_probability_accuracy(self):
        # Even money (+100 or -100) -> 50%
        self.assertEqual(american_to_probability(+100), 50.0)
        self.assertEqual(american_to_probability(-100), 50.0)
        # -200 -> 200 / 300 = 66.67%
        self.assertEqual(american_to_probability(-200), 66.67)
        # +200 -> 100 / 300 = 33.33%
        self.assertEqual(american_to_probability(+200), 33.33)

    def test_benchmark_simulation_payload_schema(self):
        extractor = NBAMicrobettingExtractor()
        records = extractor.get_benchmark_simulation_payload()

        self.assertGreater(len(records), 0)
        required_keys = {
            "timestamp_utc",
            "game_id",
            "game_name",
            "game_clock",
            "is_live",
            "category",
            "subcategory",
            "market_name",
            "outcome_name",
            "american_odds",
            "decimal_odds",
            "implied_probability_pct",
            "odds_provider",
        }
        for r in records:
            self.assertTrue(required_keys.issubset(set(r.keys())))
            self.assertIn(r["market_name"], ["Next Field Goal Type", "Method of Next Basket", "Next Team to Score"])
            self.assertIsInstance(r["american_odds"], int)
            self.assertGreater(r["decimal_odds"], 1.0)
            self.assertGreater(r["implied_probability_pct"], 0.0)

    def test_export_csv_and_json(self):
        extractor = NBAMicrobettingExtractor()
        records = extractor.get_benchmark_simulation_payload()

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test_feed.csv")
            json_path = os.path.join(tmpdir, "test_feed.json")

            extractor.export_csv(records, csv_path)
            extractor.export_json(records, json_path)

            self.assertTrue(os.path.exists(csv_path))
            self.assertTrue(os.path.exists(json_path))
            self.assertGreater(os.path.getsize(csv_path), 500)
            self.assertGreater(os.path.getsize(json_path), 500)


if __name__ == "__main__":
    unittest.main()
