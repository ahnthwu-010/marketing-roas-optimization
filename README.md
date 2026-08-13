# 📊 Marketing Campaign Performance & ROAS Optimization

**Which ad channel deserves your next marketing dollar? This case study answers that question with data — not guesswork.**

> Built for: e-commerce brands, DTC marketers, and agencies running paid ads across 2+ platforms who aren't sure where their budget should go.

[![Live Dashboard](https://img.shields.io/badge/▶%20Try%20the%20Live%20Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)]([YOUR_STREAMLIT_LINK_HERE](https://marketing-roas-optimization-xu2ep2eqjsswede3z6tdtj.streamlit.app/))

![Dashboard Preview](<img width="881" height="407" alt="Image" src="https://github.com/user-attachments/assets/40e24c3a-f128-4e8b-8f3d-8f0f20b2e7d9" />)

---

## The Bottom Line

Analyzing $37K/day in ad spend across Google Ads, Meta Ads, and TikTok Ads, this project found:

> 💰 **This business could earn +$3.2M more per year — without spending an extra dollar — just by shifting budget toward the channels that actually perform better.**

| | |
|---|---|
| **The problem** | 57% of budget goes to the channel with the *worst* return |
| **The proof** | Confirmed across every industry, country, and month tested — not a fluke |
| **The fix** | A safe, phased budget shift (not an all-or-nothing gamble) |
| **The payoff** | +5.5% revenue uplift, ~$3.2M/year, same total spend |

---

## What I Found

- 📉 **Google Ads eats 57% of the budget but returns the least** — $3.47 back per $1 spent, versus $7.62 for TikTok Ads.
- ✅ **This isn't random noise or a fluke of one industry.** The pattern holds across all 5 industries and 7 countries tested.
- 🔍 **It's not because Google is "worn out" from overuse.** None of the three channels have hit a spending ceiling yet — this is about channel efficiency, not saturation.
- 💡 **The real driver is cost-per-click, not audience quality.** TikTok converts visitors at basically the same rate as Google — it's just 53% cheaper to reach them.
- 💰 **A conservative, phased 25% budget shift** (not a risky overnight overhaul) is projected to add **+$3.2M in annual revenue** at zero extra cost.

<p align="center"><img src="YOUR_SCREENSHOT_LINK_HERE" width="700" alt="Dashboard screenshot"></p>

---

## 🖥️ Explore the Interactive Dashboard

**[→ Try it live here](https://marketing-roas-optimization-xu2ep2eqjsswede3z6tdtj.streamlit.app/)** — no signup required.

- **Executive Summary** — the headline numbers at a glance
- **Statistical Evidence** — the proof behind the recommendation
- **Budget Optimizer** — drag a slider to simulate your own reallocation scenario
- **Methodology & Limitations** — full transparency on what the data can (and can't) prove

---

## 👋 About This Analysis

I build data-driven marketing analytics for businesses that are spending real money on ads but don't have a clear read on what's actually working. This project shows the same process I use for client work: test the hypothesis statistically, stress-test it against every possible confound, and tell you honestly what the evidence supports — no overselling.

**Running ads across multiple platforms and want this kind of clarity for your own account?** [Let's talk →](https://www.fiverr.com/users/jade_84/manage_gigs)

---

<details>
<summary><b>🔬 Full Methodology (click to expand)</b></summary>

1. **Data audit** — structural validation of 1,800 campaign-day records (0 missing values).
2. **Channel benchmarking** — Kruskal-Wallis test + Bonferroni-corrected pairwise comparisons + 10,000-resample bootstrap confidence intervals on blended ROAS.
3. **Spend–response modeling** — log-log elasticity regression + Michaelis-Menten saturation curves to test for diminishing returns.
4. **Budget optimization** — constrained optimization (SLSQP) with realistic per-channel reallocation caps, avoiding unrealistic "move 90% of budget overnight" recommendations.
5. **Robustness checks** — re-ran the full comparison across every industry, country, and half-year slice.
6. **Causal-adjustment regression** — OLS with HC3 robust standard errors, controlling for industry, country, campaign type, and month fixed effects.
7. **Funnel decomposition** — log-additive decomposition of ROAS = CVR × AOV / CPC to identify exactly which funnel stage drives the performance gap.

**Dataset:** [Global Ads Performance (Google, Meta, TikTok)](https://www.kaggle.com/datasets/nudratabbas/global-ads-performance-google-meta-tiktok) — Kaggle, 1,800 records, full year 2024.

</details>

<details>
<summary><b>⚠️ Limitations (click to expand)</b></summary>

- **Association, not proof of causation.** The regression controls for observable campaign characteristics but not for unobserved factors (creative quality, bidding strategy, audience targeting maturity).
- **The "auction saturation" explanation for TikTok's lower CPC is a hypothesis**, not a confirmed finding — the dataset has no bid-density or competitor-count data.
- **Public/simulated dataset** — not a live client ad account. Real accounts carry attribution-window and cross-platform tracking discrepancies not modeled here.

</details>

<details>
<summary><b>⚙️ Run Locally</b></summary>

```bash
git clone https://github.com/ahnthwu-010/marketing-roas-optimization.git
cd marketing-roas-optimization
pip install -r requirements.txt
streamlit run app.py
```

**Tech stack:** Python · Pandas · NumPy · SciPy · Statsmodels · Plotly · Streamlit

**Project structure:**

## Project Structure

```text
marketing-roas-optimization/
├── app.py                    # Streamlit dashboard
├── requirements.txt
├── dashboard_data/           # Precomputed analysis artifacts (JSON)
├── scripts/                  # Full analysis pipeline (reproducible)
└── data/                     # Raw dataset (Kaggle)
```
</details>

---

*Built as a portfolio case study. Dataset is public/simulated; findings illustrate methodology, not real business intelligence.*
