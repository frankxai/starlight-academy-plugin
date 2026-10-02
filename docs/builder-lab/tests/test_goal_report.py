import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
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
        self.assertEqual(sum(t[field] for field in lab.TOKEN_FIELDS), t["processed_tokens"])
        rendered = lab.markdown(lab.project(self.goals, self.evidence))
        self.assertIn("ordinary input 2; cache writes 20; cache reads 30; generated output 10; processed 62", rendered)
        self.assertNotIn("fresh input 22", rendered)

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

    def test_mixed_cost_bases_have_separate_subtotals(self):
        self.evidence['runs'].append(dict(self.run, id='estimate', source_sha256='b' * 64,
                                         cost_basis='estimate', api_equivalent_usd='0.20'))
        result = self.report()
        self.assertIsNone(result['api_equivalent_usd_known_subset'])
        self.assertEqual(result['api_equivalent_usd_by_cost_basis'], {'estimate': '0.200000', 'list': '0.100000'})

    def test_partial_invoice_prose_names_coverage(self):
        self.run.update(invoiced_cash_usd='0', invoice_evidence_url=URL, invoice_id='example-invoice')
        self.evidence['runs'].append(dict(self.run, id='missing', source_sha256='b' * 64, invoiced_cash_usd=None))
        result = self.report()
        self.assertEqual(result['missing_invoice_receipts'], 1)
        output = lab.markdown(lab.project(self.goals, self.evidence))
        self.assertIn('Invoiced cash, known subset: 0 USD', output)
        self.assertIn('runs without invoice evidence: 1', output)

    def test_repeated_invoice_attribution_is_rejected(self):
        self.run.update(invoiced_cash_usd='10', invoice_evidence_url=URL, invoice_id='same-invoice')
        self.evidence['runs'].append(dict(self.run, id='run2', source_sha256='b' * 64))
        with self.assertRaises(ValueError):
            self.report()

    def test_sanitized_real_cli_receipt_preserves_native_basis(self):
        result = lab.import_claude(Path(__file__).parent / 'fixtures/claude-cli-review.json', 'G1', 'native-fixture', URL)
        self.assertEqual(result['cost_basis'], 'list')
        self.assertEqual(result['thinking_tokens_included_in_output'], 18060)
        self.assertEqual(result['output_tokens'], 20227)
        self.assertIsNone(result['invoiced_cash_usd'])

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
        self.evidence['observed_at'] = '2026-10-31T23:59:00Z'
        self.evidence["financials"] = [{"goal_id": "G1", "currency": "EUR", "net_receipts_ex_tax_refunds": "1000",
                                       "variable_cash_cost": "200", "allocated_investment_cash": "400", "source_url": URL,
                                       "period_start": "2026-10-01", "period_end": "2026-10-31",
                                       "reconciled_by": "Example reconciler", "reconciled_at": "2026-10-31T23:00:00Z"}]
        self.assertEqual(self.report()["cash_roi"]["roi_percent"], "100.00")
        self.assertEqual(self.report()['cash_roi']['status'], 'calculated-from-supplied-cash')
        self.evidence["financials"][0]["allocated_investment_cash"] = "0"
        self.assertEqual(self.report()["cash_roi"]["status"], "undefined")
        self.evidence["financials"][0]["allocated_investment_cash"] = None
        self.assertEqual(self.report()["cash_roi"]["status"], "unknown")

    def test_refund_dominated_period_and_period_proof(self):
        self.evidence['observed_at'] = '2026-10-31T23:59:00Z'
        entry = {"goal_id": "G1", "currency": "EUR", "net_receipts_ex_tax_refunds": "-100",
                 "variable_cash_cost": "20", "allocated_investment_cash": "100", "source_url": URL,
                 "period_start": "2026-10-01", "period_end": "2026-10-31",
                 "reconciled_by": "Example reconciler", "reconciled_at": "2026-10-31T23:00:00Z"}
        self.evidence["financials"] = [entry]
        self.assertEqual(self.report()["cash_roi"]["roi_percent"], "-220.00")
        entry["period_end"] = "2026-09-01"
        with self.assertRaises(ValueError):
            self.report()

    def test_missing_or_future_financial_attestation_fails(self):
        entry = {'goal_id': 'G1', 'currency': 'EUR', 'net_receipts_ex_tax_refunds': '10',
                 'variable_cash_cost': '1', 'allocated_investment_cash': '1', 'source_url': URL,
                 'period_start': '2026-09-01', 'period_end': '2026-09-30'}
        self.evidence['financials'] = [entry]
        with self.assertRaises(ValueError):
            self.report()
        entry.update(reconciled_by='Example reconciler', reconciled_at='2026-10-02T23:00:00Z')
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

    def native_eval(self):
        return {"schemaVersion": 1, "claudeVersion": "2.1.287", "partial": False,
                "costUsd": 0.22, "cases": [{"name": "contract", "promptMarkdown": "private source text",
                "arms": {"with": [{"costUsd": 0.10, "judgeCostUsd": 0.02,
                                    "tracePath": "Z:/never-open/private-credentials.json", "error": None}],
                         "without": [{"costUsd": 0.10, "judgeCostUsd": 0, "error": None}]}}]}

    def import_eval(self, data, prefix="native"):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "native.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return lab.import_claude_eval(path, "G1", prefix, URL)

    def test_native_eval_preserves_cost_and_unknown_tokens_without_reading_trace(self):
        result = self.import_eval(self.native_eval())
        self.assertEqual(result["native_agent_runs_observed"], 2)
        self.evidence["runs"] = result["runs"]
        report = self.report()
        self.assertEqual(report["api_equivalent_usd_known_subset"], "0.220000")
        self.assertEqual(report["missing_token_receipts"], 2)
        self.assertIsNone(report["tokens_known_complete_subset"])
        self.assertIsNone(report["invoiced_cash_usd_known_subset"])
        serialized = json.dumps(result)
        self.assertNotIn("private source text", serialized)
        self.assertNotIn("private-credentials.json", serialized)

    def test_native_eval_failed_and_partial_runs_keep_cost_receipts(self):
        data = self.native_eval()
        data["partial"] = True
        data["cases"][0]["arms"]["with"][0]["error"] = "private failure explanation"
        result = self.import_eval(data)
        self.assertTrue(result["suite_partial"])
        self.assertEqual(result["runs"][0]["native_outcome"], "run-error")
        self.assertEqual(result["runs"][0]["api_equivalent_usd"], "0.12")
        self.assertNotIn("private failure explanation", json.dumps(result))

    def test_native_eval_duplicate_import_renaming_cannot_double_count(self):
        data = self.native_eval()
        first = self.import_eval(data)
        renamed = self.import_eval(data, "renamed")
        self.assertEqual(first["runs"][0]["source_sha256"], renamed["runs"][0]["source_sha256"])
        self.evidence["runs"] = first["runs"] + renamed["runs"]
        with self.assertRaises(ValueError):
            self.report()

    def test_native_eval_unknown_cost_stays_unknown(self):
        data = self.native_eval()
        data["costUsd"] = None
        del data["cases"][0]["arms"]["with"][0]["judgeCostUsd"]
        result = self.import_eval(data)
        self.assertIsNone(result["runs"][0]["api_equivalent_usd"])
        self.assertTrue(all(result["runs"][0][field] is None for field in lab.TOKEN_FIELDS))

    def test_deeply_nested_input_is_refused_by_all_imports(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'deep.json'
            source.write_bytes(b'[' * 200000)
            for operation in [lambda: lab.read_json(source),
                              lambda: lab.import_claude(source, 'G1', 'deep', URL),
                              lambda: lab.import_claude_eval(source, 'G1', 'deep', URL)]:
                with self.subTest(operation=operation):
                    with self.assertRaisesRegex(ValueError, 'nesting'):
                        operation()

    def test_sanitized_real_native_eval_cost_receipt(self):
        source = Path(__file__).parent / 'fixtures/claude-eval-costs-2.1.287.json'
        result = lab.import_claude_eval(source, 'G1', 'real-eval', URL)
        self.assertEqual(result['native_agent_runs_observed'], 16)
        self.assertLess(abs(sum(lab.money(r['api_equivalent_usd']) for r in result['runs']) - lab.money('0.4237956')), lab.money('0.000000000001'))
        self.assertTrue(all(r[field] is None for r in result['runs'] for field in lab.TOKEN_FIELDS))
        self.assertNotIn('tracePath', source.read_text())

    def test_native_eval_reserialized_parent_preserves_identity(self):
        data = self.native_eval()
        first = self.import_eval(data)
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'pretty.json'
            source.write_text(json.dumps(data, indent=4, sort_keys=True), encoding='utf-8')
            second = lab.import_claude_eval(source, 'G1', 'renamed', URL)
        self.assertNotEqual(first['runs'][0]['parent_source_sha256'], second['runs'][0]['parent_source_sha256'])
        self.assertEqual(first['runs'][0]['source_sha256'], second['runs'][0]['source_sha256'])
        self.evidence['runs'] = first['runs'] + second['runs']
        with self.assertRaises(ValueError):
            self.report()

    def test_actual_usage_must_replace_the_same_native_run_id(self):
        aggregate = self.import_eval(self.native_eval())['runs'][0]
        actual = dict(self.run, id=aggregate['id'], source_sha256='b' * 64)
        self.evidence['runs'] = [aggregate, actual]
        with self.assertRaises(ValueError):
            self.report()
        self.evidence['runs'] = [actual]
        self.assertEqual(self.report()['complete_token_receipts'], 1)

    def test_native_eval_inconsistent_summary_schema_and_arms_fail(self):
        original = self.native_eval()
        alternatives = []
        mismatch = copy.deepcopy(original)
        mismatch["costUsd"] = 1
        alternatives.append(mismatch)
        boolean_schema = copy.deepcopy(original)
        boolean_schema["schemaVersion"] = True
        alternatives.append(boolean_schema)
        bad_arm = copy.deepcopy(original)
        bad_arm["cases"][0]["arms"]["unknown"] = []
        alternatives.append(bad_arm)
        bad_partial = copy.deepcopy(original)
        bad_partial["partial"] = "false"
        alternatives.append(bad_partial)
        duplicate = copy.deepcopy(original)
        duplicate["cases"].append(copy.deepcopy(duplicate["cases"][0]))
        alternatives.append(duplicate)
        for data in alternatives:
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    self.import_eval(data)

    def codex_events(self, thread="controlled-thread"):
        # Counts copied from the completed 0.1.5 native trial, 2 October 2026.
        return [{"type": "thread.started", "thread_id": thread}, {"type": "turn.started"},
                {"type": "item.completed", "item": {"type": "agent_message", "text": "private source"}},
                {"type": "turn.completed", "usage": {"input_tokens": 1102987,
                 "cached_input_tokens": 1030400, "cache_write_input_tokens": 0,
                 "output_tokens": 4117, "reasoning_output_tokens": 404}}]

    def import_codex(self, events, run_id="codex", pretty=False):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "native.jsonl"
            # JSONL events remain single-line, even when reserialized.
            source.write_text("\n".join(json.dumps(event, sort_keys=pretty) for event in events)
                              + ("\n\n" if pretty else "\n"), encoding="utf-8")
            return lab.import_codex(source, "G1", run_id, URL)

    def test_codex_real_terminal_counts_are_disjoint_and_unpriced(self):
        row = self.import_codex(self.codex_events())
        self.evidence["runs"] = [row]
        result = self.report()
        self.assertEqual(result["complete_token_receipts"], 1)
        self.assertEqual(row["native_input_tokens_including_cache"], 1102987)
        self.assertEqual(row["input_tokens"], 72587)
        self.assertEqual(row["thinking_tokens_included_in_output"], 404)
        self.assertEqual(result["tokens_known_complete_subset"]["processed_tokens"], 1107104)
        self.assertIsNone(result["api_equivalent_usd_known_subset"])
        self.assertIsNone(result["invoiced_cash_usd_known_subset"])

    def test_codex_explicit_cache_writes_are_separated_from_inclusive_input(self):
        events = self.codex_events()
        events[-1]["usage"]["cache_write_input_tokens"] = 200
        row = self.import_codex(events)
        self.assertEqual(row["input_tokens"], 72387)
        self.assertEqual(row["cache_creation_input_tokens"], 200)
        self.assertEqual(sum(row[field] for field in lab.TOKEN_FIELDS), 1107104)

    def test_codex_missing_usage_stays_unknown_without_a_schema_default(self):
        for field in ["cache_write_input_tokens", "cached_input_tokens", "input_tokens", "output_tokens"]:
            with self.subTest(field=field):
                events = self.codex_events()
                del events[-1]["usage"][field]
                row = self.import_codex(events)
                self.evidence["runs"] = [row]
                self.assertEqual(self.report()["missing_token_receipts"], 1)
                self.assertIsNone(self.report()["tokens_known_complete_subset"])
                if field != "output_tokens":
                    self.assertIsNone(row["input_tokens"])
        events = self.codex_events()
        del events[-1]["usage"]["reasoning_output_tokens"]
        self.assertIsNone(self.import_codex(events)["thinking_tokens_included_in_output"])

    def test_codex_no_content_thread_or_unattested_cost_leaks(self):
        events = self.codex_events(thread="private-thread-identifier")
        events[2]["item"]["command"] = "Z:/private/credentials.json"
        events[-1].update(total_cost_usd=99, model="private model")
        events[-1]["usage"]["invoice"] = "private invoice"
        row = self.import_codex(events)
        encoded = json.dumps(row)
        for private in ["private source", "private-thread-identifier", "credentials.json", "private invoice", "private model"]:
            self.assertNotIn(private, encoded)
        self.assertIsNone(row["api_equivalent_usd"])
        self.assertIsNone(row["invoiced_cash_usd"])

    def test_codex_replayed_content_or_serialization_cannot_be_relabelled(self):
        events = self.codex_events()
        first = self.import_codex(events)
        events[2]["item"]["text"] = "different ignored content"
        second = self.import_codex(events, "renamed", pretty=True)
        self.assertNotEqual(first["source_bytes_sha256"], second["source_bytes_sha256"])
        self.assertEqual(first["source_sha256"], second["source_sha256"])
        self.evidence["runs"] = [first, second]
        with self.assertRaises(ValueError):
            self.report()
        self.evidence["runs"] = [first, self.import_codex(self.codex_events("another-thread"), "different")]
        self.assertEqual(self.report()["complete_token_receipts"], 2)

    def test_codex_bad_numbers_and_impossible_usage_are_refused(self):
        for field, value in [("input_tokens", True), ("output_tokens", -1), ("output_tokens", 1.5),
                             ("cache_write_input_tokens", 10**12 + 1), ("cached_input_tokens", 1102988),
                             ("cache_write_input_tokens", 72588), ("reasoning_output_tokens", 4118)]:
            with self.subTest(field=field, value=value):
                events = self.codex_events()
                events[-1]["usage"][field] = value
                with self.assertRaises(ValueError):
                    self.import_codex(events)
        events = self.codex_events()
        events[-1]["usage"] = {}
        with self.assertRaises(ValueError):
            self.import_codex(events)

    def test_codex_incomplete_failed_multiturn_and_out_of_order_are_refused(self):
        complete = self.codex_events()
        alternatives = [[], complete[:-1], complete + [complete[-1]], complete + [{"type": "turn.started"}],
                        [complete[1], complete[0], *complete[2:]],
                        [complete[0], complete[1], complete[0], *complete[2:]],
                        [complete[0], complete[1], {"type": "turn.failed"}, complete[-1]],
                        [complete[0], complete[1], {"type": "turn.started"}, complete[-1]],
                        [complete[0], complete[2], complete[1], complete[-1]],
                        [complete[0], complete[1], ["invalid object"], complete[-1]]]
        for events in alternatives:
            with self.subTest(events=events):
                with self.assertRaises(ValueError):
                    self.import_codex(events)

    def test_codex_bounded_stream_and_ambiguous_json_are_refused(self):
        cases = [b"x" * (lab.MAX_INPUT + 1), b"[" * 200000, b"\xff", b'{"type":"thread.started",',
                 b'{"type":"thread.started","type":"turn.started","thread_id":"x"}\n',
                 b'{"type":"thread.started","thread_id":"x"}\n{"type":"turn.started"}\n' + b'{"type":"error"}\n' * 10000]
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "bad.jsonl"
            for raw in cases:
                with self.subTest(size=len(raw)):
                    source.write_bytes(raw)
                    with self.assertRaises(ValueError):
                        lab.import_codex(source, "G1", "bad", URL)

    def test_codex_cli_roundtrip_and_truncated_receipt_exit(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "native.jsonl"
            events = self.codex_events()
            source.write_text("\n".join(json.dumps(event) for event in events), encoding="utf-8")
            command = [sys.executable, "-B", str(Path(__file__).parents[1] / "scripts/goal_report.py"),
                       "import-codex", str(source), "--goal", "G1", "--id", "cli", "--source-url", URL]
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["input_tokens"], 72587)
            source.write_text("\n".join(json.dumps(event) for event in events[:-1]), encoding="utf-8")
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("private source", result.stderr)


if __name__ == "__main__":
    unittest.main()
