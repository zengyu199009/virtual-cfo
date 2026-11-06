# Virtual CFO

**Strategic financial leadership for one-person companies and early startups — the financial brain you'd otherwise pay $150+/hour to rent.**

This skill turns any agent (Claude Code, Cursor, OpenClaw, Codex…) into a CFO-grade financial analyst: runway & burn analysis, unit economics, fundraising readiness, pricing decisions, and board-level financial packages — backed by **2026 real baseline data** and **zero-dependency Python calculators**.

## What it does

| Area | What it covers |
|---|---|
| Runway & Burn | Gross/net burn, burn multiple, scenarios, decision triggers |
| Unit Economics | LTV by cohort, CAC by channel, payback periods |
| Fundraising | Timing, valuation, dilution, term sheets, data room |
| Pricing & Margins | Cost structure, gross margin targets, price testing |
| Board Financials | Board pack structure, budget vs actual, asks |
| Cash Management | Treasury, AR/AP optimization, runway extension |

Every output shows the calculation, not just the answer — and every conclusion is tagged 🟢 verified / 🟡 medium / 🔴 assumed.

## Why it exists

One-person companies and 1-5 person startups can't afford a real CFO ($150-500/hour, or $1k-10k/month). Most founders run on gut feel: *"we have maybe 8 months of runway"*, *"I think our unit economics are fine"* — until an investor or a board member asks for the actual math.

This skill gives you the actual math. It uses **real 2026 baseline benchmarks** (not generic startup folklore) and runs deterministic Python calculators, so the numbers it produces are reproducible.

## What's included

```
SKILL.md                          The skill (bilingual EN/ZH)
scripts/runway_calculator.py      Runway & burn scenarios
scripts/unit_economics_analyzer.py  LTV/CAC/cohort analysis
scripts/fundraising_model.py      Raise sizing & dilution model
references/saas-financial-baselines.md  2026 real baseline targets
docs/demo-report.html             Real output sample (open in browser)
```

## Real output

See a real generated board-level report here → **[demo-report.html](docs/demo-report.html)** (open in browser; this is actual output from the scripts with sample company data).

## Install

Requires any agent that can load a SKILL.md (Claude Code, Cursor, OpenClaw, Codex, etc.).

```bash
# Option A: one-line via skills.sh
npx skills add zengyu199009/virtual-cfo

# Option B: manual
git clone https://github.com/zengyu199009/virtual-cfo.git
# copy the folder into your skills directory, or reference SKILL.md directly
```

The three scripts only use Python 3 stdlib — no pip installs.

## Pro version

The GitHub repo is the **Lite version** — fully functional, MIT licensed. The **Pro version ($9 one-time)** adds:

- **Board-level report templates** (investor-ready, bilingual EN/ZH)
- **Expanded industry baselines** (SaaS / marketplace / hardware / agency)
- **Private financial health checklist** + scenario templates
- **Priority updates & support**

👉 **[Buy Pro — $9 one-time](https://pancake.waffo.ai/store/zengyu-ai-skills-9d6ik0c1/product/PROD_7UxIz1AH2Nu5jLqqblhNGC?type=onetime&currency=USD)**

## License

MIT — use it, modify it, ship it. If it saves you from one bad funding decision, it paid for itself.

---

*Built by AlqEdge · from 8 weeks of real startup financial monitoring practice*
