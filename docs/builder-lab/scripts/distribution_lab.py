#!/usr/bin/env python3
"""Offline external-commerce scenarios and requirement drafts; no live billing."""
from __future__ import annotations
import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from pathlib import Path
import re
import sys


def read_json(path: Path) -> dict:
    value=json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value,dict):
        raise ValueError("Input must be a JSON object")
    return value


def text_field(data: dict,key: str,limit: int=4000) -> str:
    value=data.get(key)
    if not isinstance(value,str) or not value.strip() or len(value)>limit:
        raise ValueError(f"{key} must be nonempty text, at most {limit} characters")
    return value


def number(data: dict, name: str, default: str | None = None) -> Decimal:
    raw = data.get(name, default)
    if isinstance(raw, bool):
        raise ValueError(f"{name} must be numeric")
    try:
        value = Decimal(str(raw))
    except InvalidOperation:
        raise ValueError(f"{name} must be numeric") from None
    if not value.is_finite() or value < 0 or value > Decimal("1000000000000"):
        raise ValueError(f"{name} must be finite, nonnegative and at most 1 trillion")
    return value


def economics(data: dict) -> dict:
    currency = text_field(data, "currency", 3)
    if not re.fullmatch(r"[A-Z]{3}", currency) or data.get("fee_currency") != currency:
        raise ValueError("Use one uppercase currency code and matching fee_currency")
    price = number(data, "price_ex_tax")
    if price == 0:
        raise ValueError("Paid-product scenario requires a positive price")
    rates = {key: number(data, key, None if key == "fee_rate" else "0")
             for key in ("tax_rate", "fee_rate", "refund_rate", "affiliate_rate", "dispute_rate")}
    if any(value > 1 for value in rates.values()):
        raise ValueError("Rates must be between 0 and 1")
    if rates["refund_rate"] + rates["dispute_rate"] > 1:
        raise ValueError("Refunds and lost disputes must represent disjoint orders")
    sales = number(data, "monthly_orders")
    if sales == 0 or sales != sales.to_integral_value():
        raise ValueError("monthly_orders must be a positive integer")
    gross = price * (1 + rates["tax_rate"])
    # Conservative: initial fees and affiliate commissions are retained after refunds.
    payment = gross * rates["fee_rate"] + number(data, "fixed_fee")
    contribution = (price * (1 - rates["refund_rate"]) - payment
                    - price * rates["affiliate_rate"] - number(data, "variable_cost", "0")
                    - number(data, "support_reserve", "0")
                    - rates["dispute_rate"] * (price + number(data, "dispute_fee", "0")))
    month = contribution * sales - number(data, "monthly_maintenance", "0") - number(data, "monthly_acquisition", "0")
    def money(value: Decimal) -> str:
        return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    return {"status": "scenario-only", "currency": currency, "transaction_fee": money(payment),
            "contribution_per_order": money(contribution), "monthly_contribution": money(month),
            "assumptions": ["Fee base includes tax", "Refunded orders retain initial transaction fees",
                            "Affiliate commissions have no assumed refund clawback",
                            "Dispute rate means lost disputes, with principal and dispute fee lost",
                            "Refunded orders and lost disputes are disjoint; initial fees remain",
                            "Orders are an input, not a forecast"],
            "excludes": ["Income tax", "Unspecified payout/FX/platform fees", "Unpriced founder time"]}


def plan(data: dict) -> dict:
    name = text_field(data, "name", 120)
    channels = data.get("channels")
    known = {"openai", "claude", "polar", "gumroad", "whop", "etsy", "stripe"}
    if not isinstance(channels, list) or not channels or any(not isinstance(c, str) or c not in known for c in channels):
        raise ValueError("Choose supported channel names")
    if "openai" in channels and (data.get("openai_commerce") != "usage-only"
            or data.get("directory_candidate_commerce_free") is not True):
        raise ValueError("Explicitly declare a commerce-free OpenAI candidate and usage-only surface; external sales are separate")
    if "etsy" in channels and data.get("artifact_type") != "original-design":
        raise ValueError("Etsy requires separate eligibility review; prompt bundles are excluded")
    requirements = {
        "openai": ["Refresh plugin policy", "Verify developer identity", "Scan skills and metadata", "No digital sales or upgrade promotion", "Record review and publishing separately"],
        "claude": ["Validate native manifest/catalog", "Pin source revision", "Test install and workflow in Claude"],
        "polar": ["Confirm organization plan and country", "Attach managed file or repository benefit", "Test grant/refund/revocation in sandbox", "Keep admin token server-side"],
        "gumroad": ["Choose direct or Discover channel", "Recalculate channel fees", "Inspect buyer download and license"],
        "whop": ["Check enabled fee components", "Test access/refund lifecycle", "Define self-service delivery"],
        "etsy": ["Review original-design eligibility", "Disclose AI use where required", "Exclude prompt bundles"],
        "stripe": ["Choose payment/MoR responsibilities explicitly", "Provide download entitlements", "Test verified webhook replay and refund behavior"]}
    return {"name": name, "status": "draft", "releaseReady": False,
            "channels": [{"channel": c, "state": "not-configured", "requirements": requirements[c]} for c in dict.fromkeys(channels)],
            "requiredEvidence": ["demand", "price", "rights", "hostBehavior", "independentReview", "deliveryLifecycle"]}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("economics","plan"))
    parser.add_argument("source",type=Path)
    args=parser.parse_args()
    try:
        value={"economics":economics,"plan":plan}[args.command](read_json(args.source))
        print(json.dumps(value,indent=2));return 0
    except (ValueError,OSError,KeyError,TypeError,InvalidOperation) as exc:
        print(json.dumps({"status":"fail","error":str(exc)}),file=sys.stderr);return 1


if __name__=="__main__":
    sys.exit(main())
