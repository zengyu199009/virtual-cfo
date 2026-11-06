#!/usr/bin/env python3
"""
fundraising_model.py — Fundraising Model (AlqEdge Virtual CFO)
============================================================================
净室重写版本（全新实现）。Dilution, cap table, multi-round projections.
稀释、股权表、多轮融资预测。

Input: JSON config file or CLI args:
  --valuation-pre 5000000          pre-money valuation
  --raise-amount 1000000           amount to raise
  --option-pool 0.10               post-money option pool (0.10 = 10%)
  --rounds "seed:1.5m:2m,series-a:10m:5m"  future rounds: name:pre:raise (optional)
Output: founder ownership after each round, dilution table, cap table summary.

Stdlib only. 零依赖。Usage:
  python fundraising_model.py --valuation-pre 5000000 --raise-amount 1000000 --option-pool 0.10
"""

import argparse
import json
import sys


def parse_rounds(spec: str) -> list:
    """Parse 'name:pre:raise,name2:pre2:raise2' into list of dicts."""
    result = []
    if not spec:
        return result
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split(":")
        if len(parts) != 3:
            continue
        name, pre, raise_amt = parts
        result.append({"name": name, "pre": float(pre) * 1_000_000 if "m" in pre.lower() or "k" in pre.lower() else float(pre),
                       "raise": float(raise_amt) * 1_000_000 if "m" in raise_amt.lower() or "k" in raise_amt.lower() else float(raise_amt)})
    return result


def main():
    parser = argparse.ArgumentParser(description="Fundraising model (AlqEdge Virtual CFO)")
    parser.add_argument("--valuation-pre", type=float, required=True, help="Pre-money valuation")
    parser.add_argument("--raise-amount", type=float, required=True, help="Amount to raise")
    parser.add_argument("--option-pool", type=float, default=0.10, help="Post-money option pool (0.10 = 10 percent)")
    parser.add_argument("--rounds", type=str, default="", help="Future rounds: seed:1.5m:2m,series-a:10m:5m")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    future_rounds = parse_rounds(args.rounds)

    # Founder starts with 100% before any dilution (assume fully owned).
    founder_pct = 1.0
    post_money = args.valuation_pre + args.raise_amount

    # Investor takes raise/post-money; option pool dilutes everyone pro-rata.
    investor_pct = args.raise_amount / post_money
    pool_pct = args.option_pool

    # After round + pool: founder = (1 - investor - pool) scaled by post-round shares.
    # Simplification: pool is created at round, dilutes founder and investor pro-rata.
    founder_after = founder_pct * (1 - investor_pct) * (1 - pool_pct)
    investor_after = investor_pct * (1 - pool_pct)
    pool_after = pool_pct

    lines = []
    lines.append("=" * 64)
    lines.append("FUNDRAISING MODEL — dilution / cap table 融资稀释模型")
    lines.append("=" * 64)
    lines.append(f"投前估值: {args.valuation_pre:,.0f}")
    lines.append(f"本轮融资: {args.raise_amount:,.0f}")
    lines.append(f"投后估值: {post_money:,.0f}")
    lines.append(f"投资人占股 (本轮): {investor_pct:.1%}")
    lines.append(f"期权池: {pool_pct:.1%}")
    lines.append("")
    lines.append("本轮后股权表 (cap table):")
    lines.append(f"  创始人: {founder_after:.1%}")
    lines.append(f"  投资人: {investor_after:.1%}")
    lines.append(f"  期权池: {pool_after:.1%}")
    lines.append(f"  合计: {founder_after + investor_after + pool_after:.1%}")

    if founder_after < 0.5:
        lines.append("")
        lines.append("🔴 警告: 本轮后创始人持股 < 50% — 失去控股权，谨慎")
    elif founder_after < 0.6:
        lines.append("")
        lines.append("🟡 提示: 本轮后创始人持股 50-60% — 控股权在边缘")

    # Future rounds projection
    if future_rounds:
        lines.append("")
        lines.append("未来轮次预测 (假设无新增期权池):")
        current = founder_after
        for rd in future_rounds:
            pre = rd["pre"]
            raise_amt = rd["raise"]
            if pre <= 0:
                continue
            new_investor = raise_amt / (pre + raise_amt)
            current = current * (1 - new_investor)
            lines.append(f"  {rd['name']}: 投前 {pre:,.0f} / 融 {raise_amt:,.0f} → 创始人稀释至 {current:.1%}")
        lines.append("")
        lines.append(f"📌 最终创始人持股 (含未来轮): {current:.1%}")

    if args.json:
        print(json.dumps({
            "pre_money": args.valuation_pre,
            "raise": args.raise_amount,
            "post_money": post_money,
            "founder_after": round(founder_after, 4),
            "investor_after": round(investor_after, 4),
            "pool": pool_pct,
            "future_rounds": future_rounds,
        }, ensure_ascii=False, indent=2))
    else:
        print("\n".join(lines))


if __name__ == "__main__":
    main()
