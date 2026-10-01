"""Behavior checks: preservation, package integrity and honest release boundaries."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

MODULE = Path(__file__).parents[1] / "scripts/distribution_lab.py"
SPEC = importlib.util.spec_from_file_location("distribution_lab", MODULE)
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


def scenario():
    return {"currency": "USD", "fee_currency": "USD", "price_ex_tax": "30",
            "tax_rate": "0.25", "fee_rate": "0.065", "fixed_fee": "0.50",
            "refund_rate": "0.1", "monthly_orders": 10, "monthly_maintenance": "20"}


class EconomicsTests(unittest.TestCase):
    def test_tax_in_fee_base_and_nonrefunded_fees(self):
        result = lab.economics(scenario())
        self.assertEqual(result["transaction_fee"], "2.94")
        self.assertEqual(result["contribution_per_order"], "24.06")
        self.assertEqual(result["monthly_contribution"], "220.63")
        self.assertEqual(result["status"], "scenario-only")

    def test_zero_and_complete_refund_boundaries(self):
        value = scenario()
        value["refund_rate"] = "1"
        self.assertLess(float(lab.economics(value)["contribution_per_order"]), 0)
        value["refund_rate"] = "0"
        self.assertEqual(lab.economics(value)["contribution_per_order"], "27.06")

    def test_costs_reduce_contribution(self):
        value = scenario()
        value.update(affiliate_rate="0.1", variable_cost="1", support_reserve="2", monthly_acquisition="50")
        self.assertEqual(lab.economics(value)["monthly_contribution"], "110.63")

    def test_invalid_values_and_currency_mismatch_fail(self):
        for key, invalid in (("fee_currency", "EUR"), ("refund_rate", "1.1"),
                             ("price_ex_tax", "NaN"), ("monthly_orders", "0"),
                             ("price_ex_tax", "1e1000"),
                             ("monthly_orders", "1.5"), ("fixed_fee", True), ("tax_rate", "-1")):
            with self.subTest(key=key, invalid=invalid), self.assertRaises(ValueError):
                value = scenario()
                value[key] = invalid
                lab.economics(value)

    def test_missing_fee_rate_does_not_assume_free_payments(self):
        value = scenario()
        del value["fee_rate"]
        with self.assertRaises(ValueError):
            lab.economics(value)


class PlanTests(unittest.TestCase):
    def test_plan_never_claims_release_readiness(self):
        result = lab.plan({"name": "Research Brief", "channels": ["openai", "polar", "whop"]})
        self.assertFalse(result["releaseReady"])
        self.assertIn("independentReview", result["requiredEvidence"])

    def test_openai_digital_upsell_is_blocked(self):
        with self.assertRaises(ValueError):
            lab.plan({"name": "Research Brief", "channels": ["openai"], "openai_commerce": "digital-upsell"})

    def test_etsy_prompt_bundle_is_blocked(self):
        with self.assertRaises(ValueError):
            lab.plan({"name": "Prompt Pack", "channels": ["etsy"], "artifact_type": "prompt-bundle"})

    def test_original_design_has_eligibility_review(self):
        result = lab.plan({"name": "Original workbook", "channels": ["etsy"], "artifact_type": "original-design"})
        self.assertFalse(result["releaseReady"])
        self.assertIn("eligibility", result["channels"][0]["requirements"][0])


if __name__ == "__main__":
    unittest.main()
