# SaaS Financial Baselines 2026 — Real Data Sources / SaaS 财务基线 2026 — 真实数据源

> 本文件是 Virtual CFO 的「真实数据」核心资产。每个基线值来自公开实测报告（非 AI 生成、非估算）。
> 更新频率：季度刷新。置信度：✅ 高（多方交叉）/ ⚠️ 中（单源）/ ❓ 低（缺口）。
> This file is the "real data" moat of Virtual CFO. Every baseline traces to a published benchmark — not AI guesses.

## 一、核心指标基线（2026 实测，带来源）

| Metric 指标 | 2026 实测值 | 健康判定线 | 来源 |
|---|---|---|---|
| Burn Multiple 烧钱倍数 | 中位数 **$0.12**/净新增$1 ARR；25th $0.00；75th $1.90；90th $5.15 | <1.5x ✅ | Grid 2025-26（130+ 公司真实连接数据） |
| Rule of 40 | 中位数 **15.1**；仅 34.5% 公司达标 | >40 ✅ | Grid 2025-26 |
| Runway 跑道 | 中位数 **13.1 个月**；25th 4.3；75th 20.9；烧钱公司中位数 13 | >12 ✅ / <9 🔴 | Grid 2025-26 |
| NDR 净收入留存 | 中位数 **102%**（私有 B2B）；<50M ARR 段 99.6-100%；上市公司中位数 110% | >110% ✅ / <100% 🔴 | SaaSrise 2026 + Grid + Blossom Street Q1-26 |
| GRR 毛留存 | 中位数 **84%**（Benchmarkit）；92%（垂直 SaaS，SaaSrise） | 追踪趋势 | Benchmarkit 2026 / SaaSrise |
| Gross Margin 毛利率 | 中位数 **75%**（纯 SaaS 82%，SaaS+服务 72%）；AI-native 55-70% | >65% ✅ | SaaSrise 2026 |
| LTV:CAC | 中位数 **3.3x**；Bootstrapped 5.0x；企业销售 3.0x | >3x ✅ | SaaSrise 2026 |
| CAC Payback | 中位数 **16 个月**（2025 年从 18 改善到 16） | <18 ✅ | Benchmarkit 2026 |
| 收入增长（私有 B2B） | 中位数 **22-26%**；SMB 28% / Mid 22% / Enterprise 17%；AI-native 55% | 追踪 | SaaSrise 2026 / Benchmarkit（中位数 20%） |
| 营收/员工 | $130K（<5M ARR）到 $300K+（>100M ARR） | 追踪 | SaaSrise 2026 |
| M&A 估值倍数 | 私有 SaaS 3.8x；Bootstrapped 4.8x；AI-Native 10-15x | — | SaaSrise 2026 |

## 二、数据源清单（改造时全网搜集）

| 数据源 | URL | 免费/付费 | 提供什么 | 怎么用 | 置信度 |
|---|---|---|---|---|---|
| Grid — State of SaaS B2B Benchmarks | withgrid.com/post/state-of-saas-b2b-benchmarks | 免费 | 130+ 公司连接数据（非自报）：burn multiple/Rule of 40/runway/NDR 分位 | 核心基线来源（burn/runway/rule of 40） | ✅ 高 |
| SaaSrise 2026 Benchmarks Report | saasrise.com/blog/saas-benchmark-report-2026 | 免费 | 2,500 家公司 15+ 数据集合成：NRR/churn/margin/LTV:CAC/估值 | 单位经济基线（LTV:CAC/payback/margin） | ✅ 高 |
| Benchmarkit 2026 | benchmarkit.ai | 免费 PDF | 342 家公司：growth/burn/GRR/CAC payback 分段 | 交叉验证基线 | ✅ 高 |
| ScaleXP SaaS Metrics Benchmark 2026 | scalexp.com 报告 | 免费 PDF | 20 指标定义 + 2026 基准 | 指标口径参考 | ⚠️ 中 |
| Blossom Street Ventures Q1-2026 | blossomstreetventures.com | 免费 | 上市 SaaS 公司 NDR/payback/运营利润率 | 上市公司交叉验证 | ✅ 高 |
| SEC EDGAR API | data.sec.gov（官方，无需 key） | 免费 | 所有美国上市公司 10-Q/10-K XBRL 财务数据 | 真实公司数据：算真实 burn/margin/估值倍数 | ✅ 高 |
| SECfinAPI | secfinapi.com | 免费（100 req/天，无卡） | 19,000+ 公司标准化财务 JSON + 40+ 比率 | 脚本可调用的免费财务 API（接 MCP/脚本） | ✅ 高 |
| sec-api.io | sec-api.io | 付费 | 专业 SEC 数据（实时流/XBRL→JSON） | 备选，免费够用就不上 | ⚠️ 中 |
| Tracxn / PitchBook / Crunchbase | tracxn.com 等 | 付费为主 | 创业公司融资/估值数据 | 融资基准（免费版数据有限） | ⚠️ 中 |

## 三、脚本可对接的 API（增值点）

- **SEC EDGAR（免费无 key）**：`https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` → 真实上市 SaaS 公司财务数据，用于「同行基准对比」功能
- **SECfinAPI（免费 key）**：标准化 JSON，100 req/天——「给任意上市公司拉财务比率」的自动化脚本基础

## 四、诚实标注规则

- 每个基线值：🟢 有来源（上表链接）/ 🟡 单源推断 / 🔴 无来源（不能用）
- 数据源链接失效 = 该数据作废，标记待更新
- 季度刷新：每季度重访上述数据源，更新基线表版本号
