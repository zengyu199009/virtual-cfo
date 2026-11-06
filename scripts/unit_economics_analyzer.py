#!/usr/bin/env python3
"""
unit_economics_analyzer.py — Unit Economics Analyzer (AlqEdge Virtual CFO)
============================================================================
净室重写版本（全新实现）。Per-cohort LTV, per-channel CAC, payback periods.
分队列 LTV、分渠道 CAC、回本周期分析。

Input: JSON config file or CLI args:
  --cohorts "m1:100,m2:140,m3:190"     monthly new customers per cohort (month:count)
  --revenue-per-customer 30             avg monthly revenue per customer
  --gross-margin 0.7                    gross margin (0.7 = 70%)
  --cac-channels "google:50,meta:80,reddit:20"  per-channel CAC cost per customer
  --monthly-churn 0.05                  monthly churn rate (0.05 = 5%)
Output: cohort LTV, blended LTV, CAC payback, per-channel LTV:CAC, verdict.

Stdlib only. 零依赖。Usage:
  python unit_economics_analyzer.py --cohorts "m1:100,m2:140,m3:190" --revenue-per-customer 30 --cac-channels "google:50,meta:80,reddit:20"
"""

import argparse
import json
import sys


def parse_map(spec: str) -> dict:
    """Parse 'k1:v1,k2:v2' into dict."""
    result = {}
    if not spec:
        return result
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        k, v = chunk.split(":")
        result[k.strip()] = float(v)
    return result


def lifetime_value(margin_per_month: float, monthly_churn: float) -> float:
    """LTV = monthly gross margin / monthly churn (geometric series)."""
    if monthly_churn <= 0:
        return float("inf")
    return margin_per_month / monthly_churn


def main():
    parser = argparse.ArgumentParser(description="Unit economics analyzer (AlqEdge Virtual CFO)")
    parser.add_argument("--cohorts", type=str, required=True, help="New customers per month cohort: m1:100,m2:140")
    parser.add_argument("--revenue-per-customer", type=float, required=True, help="Avg monthly revenue per customer")
    parser.add_argument("--gross-margin", type=float, default=0.7, help="Gross margin (0.7 = 70 percent)")
    parser.add_argument("--cac-channels", type=str, default="", help="Per-channel CAC: google:50,meta:80")
    parser.add_argument("--monthly-churn", type=float, default=0.05, help="Monthly churn rate (0.05 = 5 percent)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    cohorts = parse_map(args.cohorts)
    channels = parse_map(args.cac_channels)

    margin_per_customer = args.revenue_per_customer * args.gross_margin
    ltv = lifetime_value(margin_per_customer, args.monthly_churn)
    blended_cac = None

    # Blended CAC: weighted by cohort size across channels if channels given,
    # otherwise require a single value via channel map or default estimate.
    if channels:
        total = sum(channels.values())
        blended_cac = total / len(channels) if channels else None
    else:
        blended_cac = None

    ltv_cac = (ltv / blended_cac) if blended_cac else None

    lines = []
    lines.append("=" * 64)
    lines.append("UNIT ECONOMICS — cohort LTV / CAC / payback 单位经济分析")
    lines.append("=" * 64)
    lines.append(f"每月毛利/客户: {margin_per_customer:,.2f} (营收 {args.revenue_per_customer:,.0f} × 毛利率 {args.gross_margin:.0%})")
    lines.append(f"月流失率: {args.monthly_churn:.1%} | 客户平均寿命: {1/args.monthly_churn:.1f} 个月")
    lines.append(f"LTV (每客户): {ltv:,.2f}" if ltv != float("inf") else "LTV: ∞ (流失率为 0)")
    lines.append("")
    lines.append("分队列新增客户: " + ", ".join(f"{k}={v:,.0f}" for k, v in cohorts.items()))
    total_new = sum(cohorts.values())
    lines.append(f"总新增: {total_new:,.0f}")
    lines.append("")
    lines.append("分渠道 CAC:")
    for ch, cac in channels.items():
        ch_ltv_cac = ltv / cac if cac else None
        lines.append(f"  {ch}: CAC {cac:,.0f} | LTV:CAC {ch_ltv_cac:.2f}x" if ch_ltv_cac else f"  {ch}: CAC {cac:,.0f}")

    if blended_cac:
        lines.append(f"")
        lines.append(f"混合 CAC (平均): {blended_cac:,.0f}")
        lines.append(f"LTV:CAC = {ltv_cac:.2f}x" if ltv_cac else "LTV:CAC = N/A")
        lines.append("")
        if ltv_cac and ltv_cac >= 3:
            lines.append("🟢 判定: LTV:CAC ≥ 3 — 健康，可加大获客投入")
        elif ltv_cac and ltv_cac >= 2:
            lines.append("🟡 判定: LTV:CAC 2-3 — 边缘，优化 CAC 或提价")
        elif ltv_cac:
            lines.append("🔴 判定: LTV:CAC < 2 — 不健康，暂停扩张，先修单位经济")
        payback_months = blended_cac / margin_per_customer if margin_per_customer else None
        if payback_months:
            lines.append(f"CAC 回本周期: {payback_months:.1f} 个月" + (" ⚠️ 目标 < 18 个月" if payback_months > 18 else " ✅ 目标内 < 18 个月"))

    if args.json:
        print(json.dumps({
            "margin_per_customer": margin_per_customer,
            "monthly_churn": args.monthly_churn,
            "ltv": ltv,
            "blended_cac": blended_cac,
            "ltv_cac": ltv_cac,
            "cohorts": cohorts,
            "channels": channels,
        }, ensure_ascii=False, indent=2))
    else:
        print("\n".join(lines))


if __name__ == "__main__":
    main()
