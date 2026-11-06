#!/usr/bin/env python3
"""
runway_calculator.py — Burn Rate & Runway Calculator (AlqEdge Virtual CFO)
============================================================================
净室重写版本（全新实现）。Models runway across base/bull/bear scenarios.
三情景（基准/乐观/悲观）现金跑道建模。

Input: JSON config file or CLI args:
  --cash START_CASH        starting cash (CNY or USD, consistent units)
  --mrr MONTHLY_RECURRING  current monthly recurring revenue
  --fixed-costs MONTHLY    fixed monthly costs (ops, tools, salary, ai subs)
  --growth-pct X           monthly revenue growth % (e.g. 5 = 5% per month)
  --hires "m1:6000,m3:8000" optional planned hires as month:monthly_cost
  --scenario-delta X       how much the downside/upside scenarios deviate
Output: months of runway, cash-out date, decision triggers, CSV export.

Stdlib only. 零依赖。Usage:
  python runway_calculator.py --cash 210000 --mrr 40000 --fixed-costs 38000 --growth-pct 3
"""

import argparse
import csv
import json
import sys
from datetime import date, timedelta


def parse_hires(spec: str) -> dict:
    """Parse 'm1:6000,m3:8000' into {month_index: monthly_cost}."""
    result = {}
    if not spec:
        return result
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        m, cost = chunk.split(":")
        result[int(m.replace("m", ""))] = float(cost)
    return result


def project_runway(cash: float, mrr: float, fixed_costs: float,
                   growth_pct: float, hires: dict, max_months: int = 60) -> list:
    """Project monthly cash balance. Returns list of month dicts."""
    months = []
    balance = cash
    revenue = mrr
    for m in range(1, max_months + 1):
        revenue = revenue * (1 + growth_pct / 100.0)
        hire_cost = hires.get(m, 0.0)
        burn = fixed_costs + hire_cost - revenue  # net burn (positive = spending > income)
        balance -= max(burn, 0.0)  # cash only decreases if net burn positive
        months.append({
            "month": m,
            "revenue": round(revenue, 2),
            "fixed_costs": fixed_costs,
            "hire_cost": hire_cost,
            "net_burn": round(burn, 2),
            "cash_balance": round(balance, 2),
        })
        if balance <= 0:
            break
    return months


def find_runway(months: list) -> tuple:
    """Return (runway_months, cash_out_date_approx, trigger_months)."""
    if not months:
        return 0, None, []
    runway = months[-1]["month"]
    if months[-1]["cash_balance"] <= 0:
        runway = months[-1]["month"]
    # Decision trigger: months where runway remaining < 12
    triggers = [m["month"] for m in months if m["cash_balance"] > 0 and m["month"] % 3 == 0]
    return runway, runway, triggers[-3:] if triggers else []


def main():
    parser = argparse.ArgumentParser(description="Runway calculator (AlqEdge Virtual CFO)")
    parser.add_argument("--cash", type=float, required=True, help="Starting cash")
    parser.add_argument("--mrr", type=float, required=True, help="Monthly recurring revenue")
    parser.add_argument("--fixed-costs", type=float, required=True, help="Monthly fixed costs")
    parser.add_argument("--growth-pct", type=float, default=3.0, help="Monthly revenue growth (percent)")
    parser.add_argument("--hires", type=str, default="", help="Planned hires: m1:6000,m3:8000")
    parser.add_argument("--scenario-delta", type=float, default=2.0,
                        help="Downside/upside growth deviation (percentage points)")
    parser.add_argument("--csv", action="store_true", help="Export base scenario to CSV")
    args = parser.parse_args()

    scenarios = {
        "base": project_runway(args.cash, args.mrr, args.fixed_costs,
                               args.growth_pct, parse_hires(args.hires)),
        "bull": project_runway(args.cash, args.mrr, args.fixed_costs,
                               args.growth_pct + args.scenario_delta, parse_hires(args.hires)),
        "bear": project_runway(args.cash, args.mrr, args.fixed_costs,
                               max(args.growth_pct - args.scenario_delta, 0), parse_hires(args.hires)),
    }

    print("=" * 64)
    print("RUNWAY ANALYSIS — base / bull / bear 三情景现金跑道分析")
    print("=" * 64)
    for name, months in scenarios.items():
        runway, _, _ = find_runway(months)
        final = months[-1]
        print(f"\n[{name.upper()}] 跑道 {runway} 个月 | 期末余额 {final['cash_balance']:,.0f}"
              f" | 月收入终值 {final['revenue']:,.0f}")
        if runway < 12:
            print(f"  ⚠️ 红色警报: 跑道 < 12 个月 — 需要立即行动 (fundraise or cut burn)")
        elif runway < 18:
            print(f"  🟡 预警: 跑道 < 18 个月 — 开始准备融资")

    # Decision triggers for base scenario
    base = scenarios["base"]
    triggers = [m for m in base if m["cash_balance"] < args.cash * 0.5]
    print("\n" + "=" * 64)
    print("DECISION TRIGGERS 决策触发点（基准情景）")
    print("=" * 64)
    for t in triggers[:5]:
        print(f"  第 {t['month']} 个月: 余额 {t['cash_balance']:,.0f} — 触发点：{'融资启动' if t['month'] < 9 else '成本削减'}")

    if args.csv:
        with open("runway_forecast.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(base[0].keys()))
            w.writeheader()
            w.writerows(base)
        print("\nCSV exported: runway_forecast.csv")


if __name__ == "__main__":
    main()
