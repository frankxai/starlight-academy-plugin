#!/usr/bin/env python3
"""Offline, dated goal/usage projections. GitHub issues retain execution authority.

No network, billing, scheduling, install, Slack send or workflow mutations.
Python 3.10+, standard library only. Missing telemetry is never converted to zero.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

TOKEN_FIELDS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
STATUSES = {"Backlog", "Ready", "In progress", "In review", "Done", "Blocked"}
STATES = {"passed", "pending", "not-run", "blocked", "failed"}
MAX_INPUT = 1024 * 1024
SECRET = re.compile(r"-----BEGIN .*PRIVATE KEY-----|\b(?:sk-(?:proj-|ant-)?|polar_oat_|sk_live_|whsec_|ghp_|github_pat_)[A-Za-z0-9_-]{24,}|\bAKIA[0-9A-Z]{16}\b")


def read_json(path: Path) -> dict:
    with path.open("rb") as source:
        raw = source.read(MAX_INPUT + 1)
    return parse_json(raw)


def parse_json(raw: bytes) -> dict:
    if len(raw) > MAX_INPUT:
        raise ValueError("JSON input exceeds 1 MiB")
    data = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    return data


def text(value: object, limit: int = 1200) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit or SECRET.search(value):
        raise ValueError("Invalid or sensitive display text")
    return value


def issue_url(value: object) -> str:
    value = text(value)
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.query or parsed.username:
        raise ValueError("Evidence must be a GitHub HTTPS URL without credentials/query")
    if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/(?:issues|pull)/[1-9][0-9]*(?:#[A-Za-z0-9_-]+)?", value):
        raise ValueError("Evidence must be a canonical GitHub issue/PR link")
    return value


def money(value: object, signed: bool = False) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("Money cannot be boolean")
    try:
        amount = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError("Invalid money") from exc
    if not amount.is_finite() or (not signed and amount < 0) or abs(amount) > Decimal("1000000000000"):
        raise ValueError("Money must be finite and within its permitted range")
    return amount


def token(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 10**12:
        raise ValueError("Tokens must be nonnegative bounded integers or null")
    return value


def timestamp(value: object) -> datetime:
    result = datetime.fromisoformat(text(value).replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Observation needs an explicit timezone")
    return result


def records(value: object, limit: int) -> list:
    if not isinstance(value, list) or len(value) > limit or any(not isinstance(row, dict) for row in value):
        raise ValueError("Expected bounded object records")
    return value


def validate(goals: dict, evidence: dict) -> None:
    if goals.get("schema") != "starlight.builder_goals.v1" or evidence.get("schema") != "starlight.builder_evidence.v1":
        raise ValueError("Unsupported schema")
    timestamp(goals.get("observed_at"))
    timestamp(evidence.get("observed_at"))
    rows = records(goals.get("goals"), 100)
    if not rows:
        raise ValueError("Expected 1-100 goals")
    ids = set()
    for row in rows:
        key = text(row.get("id"), 64)
        if key in ids:
            raise ValueError("Duplicate goal")
        ids.add(key)
        for field in ("title", "rationale", "owner_role", "agent_state", "measure", "next_gate"):
            text(row.get(field))
        issue_url(row.get("issue_url"))
        date.fromisoformat(text(row.get("target_date")))
        if row.get("status") not in STATUSES:
            raise ValueError("Unknown goal status")
        money(row.get("proposed_api_equivalent_budget_usd"))
        checks = records(row.get("acceptance"), 30)
        if not checks:
            raise ValueError("Expected bounded acceptance criteria")
        check_ids = set()
        for check in checks:
            check_id = text(check.get("id"), 64)
            if check_id in check_ids:
                raise ValueError("Duplicate acceptance criterion")
            check_ids.add(check_id)
            text(check.get("description"))
            if check.get("state") not in STATES:
                raise ValueError("Unknown acceptance state")
            if check["state"] == "passed":
                issue_url(check.get("evidence_url"))
        if row["status"] == "Done" and any(c["state"] != "passed" for c in checks):
            raise ValueError("Done requires all criteria passed")
    runs = records(evidence.get("runs", []), 10000)
    run_ids, hashes, invoice_ids = set(), set(), set()
    for run in runs:
        run_id = text(run.get("id"), 120)
        digest = text(run.get("source_sha256"), 64)
        if run_id in run_ids or digest in hashes:
            raise ValueError("Duplicate run or receipt bytes")
        if not re.fullmatch(r"[a-f0-9]{64}", digest):
            raise ValueError("Invalid receipt digest")
        run_ids.add(run_id)
        hashes.add(digest)
        if run.get("goal_id") not in ids:
            raise ValueError("Run has unknown goal")
        issue_url(run.get("source_url"))
        text(run.get("provider"))
        text(run.get("cost_basis"))
        for field in TOKEN_FIELDS:
            token(run.get(field))
        token(run.get("thinking_tokens_included_in_output"))
        if run.get("thinking_tokens_included_in_output") is not None and run.get("output_tokens") is not None and run["thinking_tokens_included_in_output"] > run["output_tokens"]:
            raise ValueError("Included thinking cannot exceed output")
        money(run.get("api_equivalent_usd"))
        money(run.get("invoiced_cash_usd"))
        if run.get("invoiced_cash_usd") is not None:
            issue_url(run.get("invoice_evidence_url"))
            invoice_id = text(run.get('invoice_id'), 120)
            if invoice_id in invoice_ids:
                raise ValueError('Invoice already attributed; shared invoices require external allocation')
            invoice_ids.add(invoice_id)
    for gap in records(evidence.get("telemetry_gaps", []), 10000):
        if gap.get("goal_id") not in ids:
            raise ValueError("Telemetry gap has unknown goal")
        text(gap.get("reason"))
    financial_ids = set()
    for entry in records(evidence.get("financials", []), 100):
        if entry.get("goal_id") not in ids or entry["goal_id"] in financial_ids:
            raise ValueError("Unknown or duplicate financial goal")
        financial_ids.add(entry["goal_id"])
        if entry.get("currency") != "EUR":
            raise ValueError("This projection requires EUR cash, with explicit external FX reconciliation")
        for field in ("net_receipts_ex_tax_refunds", "variable_cash_cost", "allocated_investment_cash"):
            money(entry.get(field), signed=field == "net_receipts_ex_tax_refunds")
        if any(entry.get(field) is not None for field in ("net_receipts_ex_tax_refunds", "variable_cash_cost", "allocated_investment_cash")):
            issue_url(entry.get("source_url"))
            start = date.fromisoformat(text(entry.get("period_start")))
            end = date.fromisoformat(text(entry.get("period_end")))
            if end < start:
                raise ValueError("Financial period is reversed")
            reconciled_at = timestamp(entry.get("reconciled_at"))
            text(entry.get("reconciled_by"))
            observed = timestamp(evidence["observed_at"])
            if reconciled_at > observed or end > reconciled_at.date():
                raise ValueError("Financial period or reconciliation is later than the evidence snapshot")


def cash_roi(entry: dict | None) -> dict:
    if entry is None:
        return {"status": "unknown", "reason": "No reconciled cash period"}
    sales = money(entry.get("net_receipts_ex_tax_refunds"), signed=True)
    variable = money(entry.get("variable_cash_cost"))
    investment = money(entry.get("allocated_investment_cash"))
    if any(v is None for v in (sales, variable, investment)):
        return {"status": "unknown", "reason": "Cash revenue, variable cost or investment is missing"}
    contribution = sales - variable
    if investment == 0:
        return {"status": "undefined", "contribution_eur": str(contribution), "reason": "Investment denominator is zero"}
    return {"status": "calculated-from-supplied-cash", "contribution_eur": str(contribution),
            "roi_percent": str(((contribution - investment) / investment * 100).quantize(Decimal("0.01"))),
            "source_url": entry["source_url"], "reconciliation": "caller-attested; not independently verified",
            "reconciled_by": entry["reconciled_by"], "reconciled_at": entry["reconciled_at"]}


def project(goals: dict, evidence: dict) -> dict:
    validate(goals, evidence)
    output = {"schema": "starlight.builder_report.v1", "observed_at": goals["observed_at"],
              "evidence_observed_at": evidence["observed_at"], "scope": "Dated supplied evidence; not live-agent telemetry",
              "goals": []}
    for row in goals["goals"]:
        runs = [r for r in evidence.get("runs", []) if r["goal_id"] == row["id"]]
        complete = [r for r in runs if all(r.get(f) is not None for f in TOKEN_FIELDS)]
        totals = {f: sum(r[f] for r in complete) for f in TOKEN_FIELDS}
        costs = [money(r.get("api_equivalent_usd")) for r in runs]
        known_costs = [c for c in costs if c is not None]
        by_basis = {}
        for run, cost in zip(runs, costs):
            if cost is not None:
                basis = run["cost_basis"]
                by_basis[basis] = by_basis.get(basis, Decimal(0)) + cost
        cost_subtotals = {basis: str(value.quantize(Decimal("0.000001"))) for basis, value in sorted(by_basis.items())}
        gaps = [g["reason"] for g in evidence.get("telemetry_gaps", []) if g["goal_id"] == row["id"]]
        # Retain v1 aggregate keys for consumers; these include cache writes.
        # Display the four disjoint TOKEN_FIELDS, never sum an aggregate again.
        totals.update(fresh_input_tokens=totals["input_tokens"] + totals["cache_creation_input_tokens"],
                      fresh_io_tokens=totals["input_tokens"] + totals["cache_creation_input_tokens"] + totals["output_tokens"],
                      processed_tokens=sum(totals[f] for f in TOKEN_FIELDS))
        passed = sum(c["state"] == "passed" for c in row["acceptance"])
        financial = next((e for e in evidence.get("financials", []) if e["goal_id"] == row["id"]), None)
        output["goals"].append({"id": row["id"], "title": row["title"], "issue_url": row["issue_url"],
            "target_date": row["target_date"], "status": row["status"], "agent_state": row["agent_state"],
            "accepted_criteria": passed, "criteria_total": len(row["acceptance"]),
            "known_runs": len(runs), "complete_token_receipts": len(complete),
            "missing_token_receipts": len(runs) - len(complete), "telemetry_gaps": gaps,
            "tokens_known_complete_subset": totals if complete else None,
            "api_equivalent_usd_known_subset": next(iter(cost_subtotals.values())) if len(cost_subtotals) == 1 else None,
            "api_equivalent_usd_by_cost_basis": cost_subtotals,
            "cost_basis": next(iter(cost_subtotals)) if len(cost_subtotals) == 1 else "mixed-or-unavailable",
            "unknown_cost_receipts": len(runs) - len(known_costs),
            "invoiced_cash_usd_known_subset": str(sum((money(r["invoiced_cash_usd"]) for r in runs if r.get("invoiced_cash_usd") is not None), Decimal(0))) if any(r.get("invoiced_cash_usd") is not None for r in runs) else None,
            "missing_invoice_receipts": sum(r.get("invoiced_cash_usd") is None for r in runs),
            "cash_roi": cash_roi(financial), "next_gate": row["next_gate"]})
    return output


def cell(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ").replace("\r", " ").replace("[", "\\[").replace("]", "\\]").replace("`", "\\`").replace("<", "&lt;").replace(">", "&gt;")


def markdown(report: dict) -> str:
    lines = ["# Builder goal evidence report", "", f"Observed: {report['observed_at']}. Evidence snapshot: {report['evidence_observed_at']}.",
             "", report["scope"] + ". Criteria are counts of accepted evidence, not an estimate of effort completed.", "",
             "| Goal | Target | State | Accepted criteria | API-equivalent USD, known subset | Cash ROI |", "| --- | --- | --- | --- | --- | --- |"]
    for row in report["goals"]:
        cost = row["api_equivalent_usd_known_subset"]
        cost = (cost + " (" + cell(row["cost_basis"]) + ")") if cost is not None else "unknown or mixed bases; see detail"
        roi = row["cash_roi"].get("roi_percent", row["cash_roi"]["status"])
        lines.append(f"| [{cell(row['id'])}]({row['issue_url']}) {cell(row['title'])} | {row['target_date']} | {row['status']} | {row['accepted_criteria']}/{row['criteria_total']} | {cost} | {roi} |")
    for row in report["goals"]:
        lines += ["", f"## {cell(row['id'])}", "", f"Agent receipt state: {cell(row['agent_state'])}.", f"Next gate: {cell(row['next_gate'])}."]
        if row["tokens_known_complete_subset"]:
            t = row["tokens_known_complete_subset"]
            lines.append(f"Audited subset: {row['complete_token_receipts']} model receipts; ordinary input {t['input_tokens']:,}; cache writes {t['cache_creation_input_tokens']:,}; cache reads {t['cache_read_input_tokens']:,}; generated output {t['output_tokens']:,}; processed {t['processed_tokens']:,}. Thinking tokens are included in output, never added twice.")
        else:
            lines.append("Token totals unknown: no complete model receipt supplied.")
        lines.append(f"Incomplete token receipts: {row['missing_token_receipts']}; unknown-cost receipts: {row['unknown_cost_receipts']}. Invoiced cash, known subset: {row['invoiced_cash_usd_known_subset'] if row['invoiced_cash_usd_known_subset'] is not None else 'unknown'} USD; runs without invoice evidence: {row['missing_invoice_receipts']}.")
        for basis, cost in row["api_equivalent_usd_by_cost_basis"].items():
            lines.append(f"API-equivalent USD, known subset for {cell(basis)}: {cost}.")
        if row["cash_roi"].get("roi_percent") is not None:
            lines.append("ROI is calculated from caller-attested cash inputs; reconciliation is not independently verified by this tool.")
        for gap in row["telemetry_gaps"]:
            lines.append("Telemetry gap: " + cell(gap) + ".")
    return "\n".join(lines) + "\n"


def import_claude(path: Path, goal: str, run_id: str, source_url: str) -> dict:
    with path.open("rb") as source:
        source_bytes = source.read(MAX_INPUT + 1)
    raw = parse_json(source_bytes)
    usage = raw.get("usage")
    if not isinstance(usage, dict) or raw.get("is_error"):
        raise ValueError("No successful Claude usage receipt")
    models = raw.get("modelUsage", {})
    if not isinstance(models, dict) or any(not isinstance(v, dict) for v in models.values()):
        raise ValueError("Invalid model usage metadata")
    bases = sorted({str(v.get("costBasis", "unknown")) for v in models.values()})
    details = usage.get("output_tokens_details", {})
    if not isinstance(details, dict):
        raise ValueError("Invalid output token details")
    row = {"id": text(run_id), "goal_id": text(goal), "source_url": issue_url(source_url),
           "source_sha256": hashlib.sha256(source_bytes).hexdigest(), "provider": "Anthropic / Claude CLI",
           "cost_basis": text(", ".join(bases) or "unknown"), "api_equivalent_usd": str(money(raw.get("total_cost_usd"))) if raw.get("total_cost_usd") is not None else None,
           "invoiced_cash_usd": None,
           "thinking_tokens_included_in_output": token(details.get("thinking_tokens"))}
    row.update({f: token(usage.get(f)) for f in TOKEN_FIELDS})
    if (row['thinking_tokens_included_in_output'] is not None and row['output_tokens'] is not None
            and row['thinking_tokens_included_in_output'] > row['output_tokens']):
        raise ValueError('Included thinking cannot exceed output')
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    report = commands.add_parser("report")
    report.add_argument("goals", type=Path)
    report.add_argument("evidence", type=Path)
    report.add_argument("--format", choices=("json", "markdown"), default="markdown")
    imp = commands.add_parser("import-claude")
    imp.add_argument("receipt", type=Path)
    imp.add_argument("--goal", required=True)
    imp.add_argument("--id", required=True)
    imp.add_argument("--source-url", required=True)
    args = parser.parse_args()
    try:
        if args.command == "import-claude":
            result = import_claude(args.receipt, args.goal, args.id, args.source_url)
            print(json.dumps(result, indent=2))
        else:
            result = project(read_json(args.goals), read_json(args.evidence))
            print(json.dumps(result, indent=2) if args.format == "json" else markdown(result), end="\n" if args.format == "json" else "")
        return 0
    except (ValueError, KeyError, TypeError, OSError, InvalidOperation) as exc:
        print("Invalid report input: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
