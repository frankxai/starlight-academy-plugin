"""Scenario arithmetic and honest distribution boundaries."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

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

    def test_lost_disputes_include_principal_and_fee(self):
        value = scenario()
        value.update(dispute_rate='0.1', dispute_fee='15')
        self.assertEqual(lab.economics(value)['monthly_contribution'], '175.63')
        value['refund_rate'] = '1'
        with self.assertRaises(ValueError):
            lab.economics(value)

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
        result = lab.plan({"name": "Research Brief", "channels": ["openai", "polar", "whop"],
                           "openai_commerce": "usage-only", "directory_candidate_commerce_free": True})
        self.assertFalse(result["releaseReady"])
        self.assertIn("independentReview", result["requiredEvidence"])

    def test_openai_digital_upsell_is_blocked(self):
        with self.assertRaises(ValueError):
            lab.plan({"name": "Research Brief", "channels": ["openai"], "openai_commerce": "digital-upsell"})

    def test_ambiguous_openai_commerce_defaults_are_rejected(self):
        with self.assertRaises(ValueError):
            lab.plan({"name": "Research Brief", "channels": ["openai", "polar"]})

    def test_etsy_prompt_bundle_is_blocked(self):
        with self.assertRaises(ValueError):
            lab.plan({"name": "Prompt Pack", "channels": ["etsy"], "artifact_type": "prompt-bundle"})

    def test_original_design_has_eligibility_review(self):
        result = lab.plan({"name": "Original workbook", "channels": ["etsy"], "artifact_type": "original-design"})
        self.assertFalse(result["releaseReady"])
        self.assertIn("eligibility", result["channels"][0]["requirements"][0])

    def test_missing_polar_classification_is_unresolved(self):
        for fields in ({}, {"polar_offer_categories": []}):
            with self.subTest(fields=fields):
                result = lab.plan({"name": "Unclassified offer", "channels": ["polar"], **fields})
                self.assertEqual(result["channels"][0]["eligibility"]["state"], "classification-required")
                self.assertEqual(result["channels"][0]["eligibility"]["providerApproval"], "not-verified")
                self.assertIn("channelEligibility", result["requiredEvidence"])
                self.assertFalse(result["releaseReady"])

    def test_ai_and_ebook_require_closer_review_even_when_also_software(self):
        for category in ("ai-generation", "ebook"):
            with self.subTest(category=category):
                result = lab.plan({"name": "Mixed offer", "channels": ["polar", "polar"],
                                   "polar_offer_categories": ["software", category, category]})
                self.assertEqual(len(result["channels"]), 1)
                eligibility = result["channels"][0]["eligibility"]
                self.assertEqual(eligibility["state"], "closer-review-required")
                self.assertEqual(eligibility["declaredCategories"], ["software", category])
                self.assertEqual(eligibility["providerApproval"], "not-verified")
                self.assertFalse(result["releaseReady"])

    def test_ordinary_categories_do_not_establish_approval(self):
        for category in ("software", "digital-download", "premium-content"):
            with self.subTest(category=category):
                result = lab.plan({"name": "Declared offer", "channels": ["polar"],
                                   "polar_offer_categories": [category], "approved": True, "releaseReady": True})
                self.assertEqual(result["channels"][0]["eligibility"]["state"], "category-review-required")
                self.assertEqual(result["channels"][0]["eligibility"]["providerApproval"], "not-verified")
                self.assertFalse(result["releaseReady"])

    def test_prohibited_polar_categories_refuse_the_entire_draft(self):
        for category in ("third-party-marketplace", "physical-goods", "human-services", "get-rich-scheme"):
            with self.subTest(category=category), self.assertRaisesRegex(ValueError, "Polar AUP prohibits"):
                lab.plan({"name": "Ineligible offer", "channels": ["gumroad", "polar"],
                          "polar_offer_categories": ["software", "ai-generation", category]})

    def test_malformed_or_unknown_polar_categories_are_not_accepted_as_software(self):
        for value in (None, True, "software", {"software": True}, [None], [False], [["software"]],
                      [""], [" Software "], ["unlisted-category"]):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "polar_offer_categories"):
                lab.plan({"name": "Malformed offer", "channels": ["polar"], "polar_offer_categories": value})

    def test_other_channels_do_not_inherit_polar_eligibility(self):
        result = lab.plan({"name": "Separate channel", "channels": ["gumroad", "claude"],
                           "polar_offer_categories": ["human-services"]})
        self.assertEqual([row["channel"] for row in result["channels"]], ["gumroad", "claude"])
        self.assertTrue(all("eligibility" not in row for row in result["channels"]))
        self.assertNotIn("channelEligibility", result["requiredEvidence"])
        self.assertFalse(result["releaseReady"])

    def test_cli_refusal_emits_no_partial_draft_and_can_recover(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "offer.json"
            offer = {"name": "Resale proposal", "channels": ["gumroad", "polar"],
                     "polar_offer_categories": ["third-party-marketplace"]}
            source.write_text(json.dumps(offer), encoding="utf-8")
            refused = subprocess.run([sys.executable, "-B", str(MODULE), "plan", str(source)],
                                     capture_output=True, text=True, timeout=10)
            self.assertEqual(refused.returncode, 1)
            self.assertEqual(refused.stdout, "")
            self.assertEqual(json.loads(refused.stderr)["status"], "fail")
            self.assertIn("Polar AUP prohibits", json.loads(refused.stderr)["error"])
            self.assertEqual(json.loads(source.read_text(encoding="utf-8")), offer)
            offer["channels"] = ["gumroad"]
            source.write_text(json.dumps(offer), encoding="utf-8")
            recovered = subprocess.run([sys.executable, "-B", str(MODULE), "plan", str(source)],
                                       capture_output=True, text=True, timeout=10)
            self.assertEqual(recovered.returncode, 0)
            self.assertEqual(recovered.stderr, "")
            draft = json.loads(recovered.stdout)
            self.assertEqual(draft["channels"][0]["state"], "not-configured")
            self.assertFalse(draft["releaseReady"])


if __name__ == "__main__":
    unittest.main()
