#!/usr/bin/env python3
"""Offline release checks for Builder Lab; no host, directory or cash certification.

Run from any directory with Python 3.10+. Temporary generated artifacts are
removed on exit. No dependencies, network, installation or checkout mutation.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/starlight-builder-lab"
PACKAGE = PLUGIN / "scripts/package_lab.py"
GOALS = ROOT / "docs/builder-lab/scripts/goal_report.py"
REPOSITORY = "https://github.com/frankxai/starlight-academy-plugin.git"


def run_json(script: Path, *args: object, succeeds: bool = True) -> dict:
    result = subprocess.run([sys.executable, "-B", str(script), *(str(a) for a in args)],
                            capture_output=True, text=True, encoding="utf-8", timeout=30)
    if (result.returncode == 0) != succeeds:
        raise ValueError(f"Unexpected exit {result.returncode} from {script.name}: {result.stderr[:1200]}")
    data = json.loads(result.stdout if succeeds else result.stderr)
    if not isinstance(data, dict):
        raise ValueError("Command did not return an object")
    return data


def relative_references(root: Path, scope: Path | None = None) -> int:
    count = 0
    for path in sorted((scope or root).rglob("*.md")):
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            destination = (path.parent / unquote(target.split("#", 1)[0])).resolve()
            if root.resolve() not in destination.parents or not destination.is_file():
                raise ValueError(f"Missing or external local reference in {path.relative_to(root)}")
            count += 1
    return count


def catalogs(root: Path) -> dict:
    name = "starlight-builder-lab"
    codex = json.loads((root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    claude = json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    rows = []
    for catalog in (codex, claude):
        entries = [p for p in catalog["plugins"] if p["name"] == name]
        if len(entries) > 1:
            raise ValueError("Duplicate Builder Lab catalog entry")
        rows.append(entries[0] if entries else None)
    if all(row is None for row in rows):
        return {"status": "candidate-not-listed"}
    if any(row is None for row in rows):
        raise ValueError("Builder Lab catalogs must be registered together")
    portable, native = rows
    if portable["source"] != {"source": "local", "path": "./plugins/starlight-builder-lab"}:
        raise ValueError("Codex Builder Lab source drift")
    source = native["source"]
    if (source.get("source") != "git-subdir" or source.get("url") != REPOSITORY
            or source.get("path") != "plugins/starlight-builder-lab"
            or not re.fullmatch(r"[a-f0-9]{40}", source.get("sha", ""))):
        raise ValueError("Claude Builder Lab must pin an immutable repository revision")
    version = json.loads((root / "plugins/starlight-builder-lab/plugin.json").read_text(encoding="utf-8"))["version"]
    if native.get("version") != version:
        raise ValueError("Catalog version drift")
    return {"status": "structural-pass", "claude_payload_revision": source["sha"],
            "host_install": "not-proven-by-this-check"}


def verify() -> dict:
    checked = run_json(PACKAGE, "check", PLUGIN)
    if checked.get("skills") != 3 or checked.get("hostTests") != "not-run":
        raise ValueError("Unexpected package scope or host claim")
    refs = relative_references(PLUGIN)
    document_refs = relative_references(ROOT, ROOT / 'docs/builder-lab')
    with tempfile.TemporaryDirectory(prefix="builder-release-") as scratch:
        base = Path(scratch)
        generated = base / "research-brief"
        run_json(PACKAGE, "scaffold", PLUGIN / "examples/research-brief.json", generated)
        run_json(PACKAGE, "check", generated)
        before = (generated / "plugin.json").read_bytes()
        run_json(PACKAGE, "scaffold", PLUGIN / "examples/research-brief.json", generated, succeeds=False)
        if (generated / "plugin.json").read_bytes() != before:
            raise ValueError("Existing scaffold was modified")
        first = run_json(PACKAGE, "pack", generated, base / "first.zip")
        restored = base / "restored"
        with zipfile.ZipFile(base / "first.zip") as archive:
            for entry in archive.infolist():
                destination = (restored / entry.filename).resolve()
                if restored.resolve() not in destination.parents:
                    raise ValueError("Generated ZIP path escapes the restoration directory")
                if entry.create_system != 3 or entry.date_time != (2020, 1, 1, 0, 0, 0) or entry.compress_type != zipfile.ZIP_STORED:
                    raise ValueError("Generated ZIP lacks reproducible headers")
        restored_receipt = run_json(PACKAGE, "restore", base / "first.zip", restored, "--sha256", first["sha256"])
        if (restored_receipt["status"] != "restored-structural-pass"
                or restored_receipt["installation"] != "not-performed"
                or (restored / "LICENSE").read_bytes() != (generated / "LICENSE").read_bytes()):
            raise ValueError("Restored source or licence differs from the supplied release")
        run_json(PACKAGE, "check", restored)
        second = run_json(PACKAGE, "pack", restored, base / "second.zip")
        if first["sha256"] != second["sha256"]:
            raise ValueError("Generated archive changes on restore and repack")
        (generated / ".env.production").write_text("fixture only", encoding="utf-8")
        run_json(PACKAGE, "pack", generated, base / "rejected.zip", succeeds=False)
        if (base / "rejected.zip").exists():
            raise ValueError("Rejected archive was created")
        package = run_json(PACKAGE, "pack", PLUGIN, base / "builder.zip")
        with zipfile.ZipFile(base / "builder.zip") as archive:
            if archive.testzip() is not None:
                raise ValueError("Portable artifact has corruption")
            expected = sorted(p.relative_to(PLUGIN).as_posix() for p in PLUGIN.rglob('*') if p.is_file())
            if sorted(archive.namelist()) != expected:
                raise ValueError("Portable artifact differs from the checked plugin-only tree")
        receipt = base / 'usage.json'
        receipt.write_text(json.dumps({'usage': {'input_tokens': 2, 'output_tokens': 10,
                           'cache_creation_input_tokens': 20, 'cache_read_input_tokens': 30},
                           'modelUsage': {'example': {'costBasis': 'list'}}, 'total_cost_usd': 0.1,
                           'result': 'fixture: this response must stay out of the imported receipt'}), encoding='utf-8')
        imported = run_json(GOALS, 'import-claude', receipt, '--goal', 'BL-01', '--id', 'cli-fixture',
                            '--source-url', 'https://github.com/frankxai/starlight-academy-plugin/pull/4')
        if 'result' in imported or imported['invoiced_cash_usd'] is not None:
            raise ValueError('CLI importer exported response content or inferred cash')
        economics = base / 'economics.json'
        economics.write_text(json.dumps({'currency': 'USD', 'fee_currency': 'USD', 'price_ex_tax': '30',
                            'tax_rate': '0.25', 'fee_rate': '0.065', 'fixed_fee': '0.50',
                            'refund_rate': '0.1', 'monthly_orders': 10, 'monthly_maintenance': '20'}), encoding='utf-8')
        distribution = ROOT / 'docs/builder-lab/scripts/distribution_lab.py'
        scenario = run_json(distribution, 'economics', economics)
        if scenario['monthly_contribution'] != '220.63' or scenario['status'] != 'scenario-only':
            raise ValueError('Distribution CLI scenario drift')
        plan = base / 'plan.json'
        plan.write_text(json.dumps({'name': 'CLI fixture', 'channels': ['openai', 'polar'],
                                   'openai_commerce': 'usage-only', 'directory_candidate_commerce_free': True}), encoding='utf-8')
        if run_json(distribution, 'plan', plan)['releaseReady'] is not False:
            raise ValueError('Distribution CLI fabricated release readiness')
    report = run_json(GOALS, "report", ROOT / "docs/builder-lab/goals.json",
                      ROOT / "docs/builder-lab/evidence.json", "--format", "json")
    if len(report["goals"]) != 6:
        raise ValueError("Programme projection must retain all six goals")
    return {"status": "offline-release-checks-pass", "plugin": checked["name"],
            "package_sha256": package["sha256"], "example_sha256": first["sha256"],
            "relative_references_checked": refs, "goals_reported": len(report["goals"]),
            "document_references_checked": document_refs,
            "catalogs": catalogs(ROOT), "host_behavior": "not-proven-by-this-check",
            "restore": "generated-example-checksum-and-license-preserved; not-merchant-delivery",
            "directory_approval": "not-proven-by-this-check", "commerce": "not-proven-by-this-check",
            "secret_scan": "package-heuristic-only; retain full repository secret checks"}


if __name__ == "__main__":
    try:
        print(json.dumps(verify(), indent=2))
    except (ValueError, KeyError, TypeError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"Release check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
