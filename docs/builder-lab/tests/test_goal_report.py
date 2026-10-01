import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("goal_report", Path(__file__).parents[1] / "scripts/goal_report.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)
URL = "https://github.com/frankxai/starlight-academy-plugin/issues/3"


class GoalReportTests(unittest.TestCase):
    def setUp(self):
        self.goals = {"schema": "starlight.builder_goals.v1", "observed_at": "2026-10-01T20:00:00+02:00", "goals": [
            {"id": "G1", "title": "Prove workflow", "rationale": "Buyer outcome", "owner_role": "Maker pending",
             "agent_state": "handoff", "measure": "One verified result", "next_gate": "Host trial", "issue_url": URL,
             "target_date": "2026-10-08", "status": "In review", "proposed_api_equivalent_budget_usd": "5",
             "acceptance": [{"id": "source", "description": "Source", "state": "passed", "evidence_url": URL},
                            {"id": "host", "description": "Host", "state": "not-run"}]}]}
        self.run = {"id": "run1", "goal_id": "G1", "source_sha256": "a" * 64, "source_url": URL, "provider": "Anthropic",
                    "cost_basis": "list", "input_tokens": 2, "output_tokens": 10, "cache_creation_input_tokens": 20,
                    "cache_read_input_tokens": 30, "thinking_tokens_included_in_output": 8,
                    "api_equivalent_usd": "0.10", "invoiced_cash_usd": None}
        self.evidence = {"schema": "starlight.builder_evidence.v1", "observed_at": "2026-10-01T18:00:00Z", "runs": [self.run],
                         "telemetry_gaps": [{"goal_id": "G1", "reason": "Codex scope unavailable"}], "financials": []}

    def report(self):
        return lab.project(self.goals, self.evidence)["goals"][0]

    def test_cache_and_thinking_not_double_counted(self):
        t = self.report()["tokens_known_complete_subset"]
        self.assertEqual(t["fresh_input_tokens"], 22)
        self.assertEqual(t["fresh_io_tokens"], 32)
        self.assertEqual(t["processed_tokens"], 62)

    def test_duplicate_receipt_under_new_id_rejected(self):
        other = dict(self.run, id="different-id")
        self.evidence["runs"].append(other)
        with self.assertRaises(ValueError):
            self.report()

    def test_unknown_is_not_zero(self):
        self.evidence["runs"] = []
        r = self.report()
        self.assertIsNone(r["api_equivalent_usd_known_subset"])
        self.assertIsNone(r["tokens_known_complete_subset"])
        self.assertEqual(r["cash_roi"]["status"], "unknown")

    def test_partial_receipt_is_excluded_and_counted(self):
        self.run["output_tokens"] = None
        r = self.report()
        self.assertEqual(r["missing_token_receipts"], 1)
        self.assertIsNone(r["tokens_known_complete_subset"])

    def test_mixed_known_cost_and_unknown_cash(self):
        self.evidence["runs"].append(dict(self.run, id="run2", source_sha256="b" * 64, api_equivalent_usd="0.20"))
        self.assertEqual(self.report()["api_equivalent_usd_known_subset"], "0.300000")
        self.assertIsNone(self.report()["invoiced_cash_usd_known_subset"])

    def test_false_done_rejected(self):
        self.goals["goals"][0]["status"] = "Done"
        with self.assertRaises(ValueError):
            self.report()

    def test_missing_passed_proof_rejected(self):
        del self.goals["goals"][0]["acceptance"][0]["evidence_url"]
        with self.assertRaises(ValueError):
            self.report()

    def test_malformed_records_and_impossible_thinking_rejected(self):
        self.goals["goals"][0]["acceptance"] = ["not a record"]
        with self.assertRaises(ValueError):
            self.report()
        self.goals["goals"][0]["acceptance"] = [{"id": "a", "description": "a", "state": "not-run"}]
        self.run["thinking_tokens_included_in_output"] = 11
        with self.assertRaises(ValueError):
            self.report()

    def test_markdown_destination_injection_rejected(self):
        self.goals["goals"][0]["issue_url"] = "https://github.com/x/y/issues/3)[bad](javascript:alert)"
        with self.assertRaises(ValueError):
            self.report()

    def test_bad_money_tokens_and_foreign_goal_rejected(self):
        for changes in [{"api_equivalent_usd": "NaN"}, {"api_equivalent_usd": -1}, {"output_tokens": True}, {"goal_id": "G404"}]:
            with self.subTest(changes=changes):
                self.evidence["runs"] = [dict(self.run, **changes)]
                with self.assertRaises(ValueError):
                    self.report()

    def test_roi_uses_reconciled_cash_only(self):
        self.evidence["financials"] = [{"goal_id": "G1", "currency": "EUR", "net_receipts_ex_tax_refunds": "1000",
                                       "variable_cash_cost": "200", "allocated_investment_cash": "400", "source_url": URL,
                                       "period_start": "2026-10-01", "period_end": "2026-10-31"}]
        self.assertEqual(self.report()["cash_roi"]["roi_percent"], "100.00")
        self.evidence["financials"][0]["allocated_investment_cash"] = "0"
        self.assertEqual(self.report()["cash_roi"]["status"], "undefined")
        self.evidence["financials"][0]["allocated_investment_cash"] = None
        self.assertEqual(self.report()["cash_roi"]["status"], "unknown")

    def test_refund_dominated_period_and_period_proof(self):
        entry = {"goal_id": "G1", "currency": "EUR", "net_receipts_ex_tax_refunds": "-100",
                 "variable_cash_cost": "20", "allocated_investment_cash": "100", "source_url": URL,
                 "period_start": "2026-10-01", "period_end": "2026-10-31"}
        self.evidence["financials"] = [entry]
        self.assertEqual(self.report()["cash_roi"]["roi_percent"], "-220.00")
        entry["period_end"] = "2026-09-01"
        with self.assertRaises(ValueError):
            self.report()

    def test_currency_and_duplicate_financials_rejected(self):
        entry = {"goal_id": "G1", "currency": "USD"}
        self.evidence["financials"] = [entry]
        with self.assertRaises(ValueError):
            self.report()
        entry["currency"] = "EUR"
        self.evidence["financials"].append(copy.deepcopy(entry))
        with self.assertRaises(ValueError):
            self.report()

    def test_markdown_escape_and_timezone(self):
        self.goals["goals"][0]["title"] = "A | [bad](javascript:x) <script>"
        out = lab.markdown(lab.project(self.goals, self.evidence))
        self.assertIn("\\|", out)
        self.assertIn("&lt;script&gt;", out)
        self.goals["observed_at"] = "2026-10-01T18:00:00"
        with self.assertRaises(ValueError):
            self.report()

    def test_import_emits_only_usage_and_provenance(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / "receipt.json"
            p.write_text(json.dumps({"usage": {f: self.run[f] for f in lab.TOKEN_FIELDS}, "result": "private prompt content",
                                     "total_cost_usd": 0.1, "modelUsage": {"model": {"costBasis": "list"}}}), encoding="utf-8")
            result = lab.import_claude(p, "G1", "run1", URL)
            self.assertNotIn("result", result)
            self.assertIsNone(result["invoiced_cash_usd"])
            self.assertEqual(result["cache_creation_input_tokens"], 20)


if __name__ == "__main__":
    unittest.main()
