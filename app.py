"""
Marketing Campaign Performance & ROAS Optimization Analytics
A consultant-grade case study: are businesses overspending on Google Ads?
"""

import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Marketing ROAS Optimization | Analytics Case Study",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PLATFORM_COLORS = {
    "Google Ads": "#5B9BFF",
    "Meta Ads": "#4F8EF7",
    "TikTok Ads": "#FF3B69",
}

BG        = "#0d1117"
BG_ALT    = "#161b28"
CARD_BG   = "#1a2033"
BORDER    = "#2a3350"
TEXT      = "#e6e9ef"
MUTED     = "#8b95a8"
ACCENT_GREEN  = "#4ADE80"
ACCENT_AMBER  = "#f0b429"

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {BG}; }}
    .main .block-container {{padding-top: 1.5rem; max-width: 1200px;}}

    /* ---- Hero metric tickers (custom HTML cards) ---- */
    .hero-metric {{
        background: linear-gradient(135deg, #141a2e 0%, #1c2440 100%);
        border: 1px solid {BORDER}; border-top: 2px solid {ACCENT_GREEN};
        padding: 1.4rem 1.6rem; border-radius: 12px; color: {TEXT};
        text-align: center; height: 100%;
    }}
    .hero-metric p.label {{font-size: 0.78rem; color: {MUTED}; margin: 0; letter-spacing: 0.04em;}}
    .hero-metric h1 {{font-size: 2.1rem; margin: 0.25rem 0; color: {ACCENT_GREEN};}}
    .hero-metric p.sub {{font-size: 0.82rem; color: {MUTED}; margin: 0;}}

    /* ---- Frame native st.metric() widgets the same way ---- */
    [data-testid="stMetric"] {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-top: 2px solid {ACCENT_GREEN};
        border-radius: 10px;
        padding: 0.9rem 1.1rem 0.7rem 1.1rem;
    }}
    [data-testid="stMetricLabel"] {{color: {MUTED} !important; font-size: 0.78rem !important;}}
    [data-testid="stMetricValue"] {{color: {TEXT} !important; font-size: 1.55rem !important;}}
    [data-testid="stMetricDelta"] {{font-size: 0.85rem !important;}}

    /* ---- Q&A / caveat cards ---- */
    .qa-card {{
        background: {CARD_BG}; border: 1px solid {BORDER}; border-left: 4px solid #5B9BFF;
        color: {TEXT};
        padding: 1rem 1.3rem; border-radius: 8px; margin-bottom: 0.8rem;
    }}
    .caveat-box {{
        background: #241d0f; border: 1px solid #4a3a17; border-left: 4px solid {ACCENT_AMBER};
        color: {TEXT};
        padding: 0.9rem 1.2rem; border-radius: 8px; font-size: 0.9rem;
    }}

    .stTabs [data-baseweb="tab"] {{font-size: 1rem; font-weight: 600; color: {MUTED};}}
    .stTabs [aria-selected="true"] {{color: {TEXT} !important;}}

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {{ background-color: {BG_ALT}; }}
    .side-box {{
        background: {CARD_BG}; border: 1px solid {BORDER};
        border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 0.8rem;
    }}
    .side-box .side-label {{
        font-size: 0.68rem; font-weight: 700; color: {ACCENT_GREEN};
        letter-spacing: 0.08em; text-transform: uppercase;
        display: block; margin-bottom: 0.4rem;
    }}
    .side-box p, .side-box li {{font-size: 0.85rem; color: {TEXT}; margin: 0.15rem 0;}}
    .side-box ul {{margin: 0.3rem 0 0 0; padding-left: 1.1rem;}}
    .chip-row {{display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.3rem;}}
    .chip {{
        background: {BG_ALT}; border: 1px solid {BORDER}; color: {MUTED};
        font-size: 0.72rem; padding: 0.18rem 0.55rem; border-radius: 5px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_all_data():
    data = {}
    files = {
        "step2": "dashboard_data/step2_channel_benchmarking.json",
        "step3": "dashboard_data/step3_spend_response.json",
        "step4b": "dashboard_data/step4b_constrained_scenarios.json",
        "step5": "dashboard_data/step5_robustness.json",
        "step6": "dashboard_data/step6_causal_platform_effect.json",
        "step7": "dashboard_data/step7_funnel_decomposition.json",
    }
    for key, path in files.items():
        with open(path) as f:
            data[key] = json.load(f)
    return data


data = load_all_data()
platforms = ["Google Ads", "Meta Ads", "TikTok Ads"]


def mm_curve(spend, vmax, k):
    return vmax * spend / (k + spend)


def apply_dark(fig, **extra_layout):
    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=CARD_BG,
        font_color=TEXT,
        xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
        yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
        legend=dict(font_color=TEXT),
        **extra_layout,
    )
    return fig


with st.sidebar:
    st.markdown("## 📊 ROAS Optimizer")
    st.caption("Marketing Analytics Case Study")

    st.markdown(
        """
        <div class="side-box">
        <span class="side-label">The Question</span>
        <p>A full-funnel case study answering what every performance
        marketer asks: <b>which channel deserves the next marketing
        dollar?</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="side-box">
        <span class="side-label">Dataset</span>
        <ul>
        <li>1,800 campaign-day records</li>
        <li>Google Ads · Meta Ads · TikTok Ads</li>
        <li>5 industries · 7 countries</li>
        <li>Full year 2024</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="side-box">
        <span class="side-label">Methods</span>
        <ul>
        <li>Non-parametric hypothesis testing</li>
        <li>Bootstrap confidence intervals</li>
        <li>Log-log elasticity regression</li>
        <li>Constrained budget optimization</li>
        <li>Causal-adjustment regression (HC3)</li>
        <li>Funnel decomposition</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="side-box">
        <span class="side-label">Tech Stack</span>
        <div class="chip-row">
        <span class="chip">Python</span><span class="chip">Pandas</span>
        <span class="chip">SciPy</span><span class="chip">Statsmodels</span>
        <span class="chip">Plotly</span><span class="chip">Streamlit</span>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("[↗ GitHub Repository](#)")


st.title("📊 Marketing Campaign Performance & ROAS Optimization")
st.markdown(
    "##### A data-driven case study on multi-channel ad budget allocation "
    "across Google Ads, Meta Ads, and TikTok Ads"
)
st.markdown("---")
st.caption(
    f"📅 Analysis based on a fixed dataset snapshot (Jan 1 – Dec 30, 2024, 1,800 records). "
    f"This is a static portfolio case study, not a live-connected dashboard — "
    f"for a live version connected to your actual ad accounts, this would pull "
    f"real-time data via the Google Ads / Meta / TikTok APIs."
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["🎯 Executive Summary", "📈 Statistical Evidence", "⚙️ Budget Optimizer", "🔬 Methodology & Limitations"]
)
with tab1:
    st.markdown("#### Question: Is this business overspending on Google Ads?")
    st.markdown(
        '<div class="qa-card"><b>Answer:</b> The evidence strongly suggests yes. '
        "Google Ads receives 57% of total ad budget while delivering the lowest "
        "return of the three channels analyzed.</div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    rec = data["step4b"]["scenarios"]["cap_25pct"]
    with c1:
        st.markdown(
            f"""<div class="hero-metric"><p class="label">PROJECTED ANNUAL UPLIFT</p>
            <h1>${rec['uplift_annualized']/1e6:.1f}M</h1>
            <p class="sub">at the same total ad spend</p></div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="hero-metric"><p class="label">REVENUE UPLIFT (PHASE 1)</p>
            <h1>+{rec['uplift_pct']:.1f}%</h1>
            <p class="sub">with a conservative ±25% reallocation</p></div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""<div class="hero-metric"><p class="label">STATISTICAL CONFIDENCE</p>
            <h1>p < 0.001</h1>
            <p class="sub">channel gap confirmed across 5 industries, 7 countries</p></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1.1, 1])

    with col_left:
        st.markdown("##### Blended ROAS by Channel (95% Bootstrap CI)")
        boot = data["step2"]["bootstrap_blended_roas"]
        fig = go.Figure()
        for p in platforms:
            b = boot[p]
            fig.add_trace(
                go.Bar(
                    x=[p], y=[b["point"]],
                    error_y=dict(type="data", symmetric=False,
                                 array=[b["ci_high"] - b["point"]],
                                 arrayminus=[b["point"] - b["ci_low"]]),
                    marker_color=PLATFORM_COLORS[p], name=p, showlegend=False,
                    text=[f"{b['point']:.2f}x"], textposition="outside",
                )
            )
        fig.update_layout(height=380, yaxis_title="Blended ROAS (Revenue / Spend)", margin=dict(t=20, b=20))
        apply_dark(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("##### Current Budget Allocation vs. Revenue Share")
        current_spend = data["step4b"]["current_spend"]
        total_spend = sum(current_spend.values())
        boot = data["step2"]["bootstrap_blended_roas"]
        revenue_est = {p: current_spend[p] * boot[p]["point"] for p in platforms}
        total_rev = sum(revenue_est.values())

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name="% of Ad Spend",
            x=platforms, y=[current_spend[p] / total_spend * 100 for p in platforms],
            marker_color="#5a6478",
        ))
        fig2.add_trace(go.Bar(
            name="% of Revenue Generated",
            x=platforms, y=[revenue_est[p] / total_rev * 100 for p in platforms],
            marker_color=ACCENT_GREEN,
        ))
        fig2.update_layout(
            barmode="group", height=380, yaxis_title="% share",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            margin=dict(t=40, b=20),
        )
        apply_dark(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        """
        <div class="caveat-box">
        <b>⚠️ Caveat:</b> This analysis identifies a strong, statistically robust
        <i>association</i> between platform and revenue performance, adjusted for
        observable campaign characteristics (industry, country, campaign type,
        seasonality). It does not constitute a randomized controlled experiment —
        unobserved factors such as creative quality, audience targeting maturity,
        or bidding strategy could also contribute to the gap. See the
        <b>Methodology & Limitations</b> tab for full detail.
        </div>
        """,
        unsafe_allow_html=True,
    )
with tab2:
    st.markdown("###  Is the Channel Gap Statistically Real?")
    kw = data["step2"]["kruskal_wallis_platform"]
    colA, colB = st.columns([1, 1.4])
    with colA:
        st.metric("Kruskal-Wallis H-statistic", f"{kw['H']:.1f}")
        st.metric("p-value", f"{kw['p_value']:.2e}")
        st.metric("Effect size (ε²)", f"{kw['epsilon_sq']:.3f}", help="0.01 small · 0.08 medium · 0.26+ large")
        st.caption(
            "A non-parametric test (appropriate given ROAS's right-skewed "
            "distribution) confirms the difference in ROAS across platforms "
            "is not due to random noise."
        )
    with colB:
        st.markdown("**Pairwise comparisons (Bonferroni-adjusted)**")
        pw_df = pd.DataFrame(data["step2"]["pairwise_platform"])
        pw_df["p_adj"] = pw_df["p_adj"].apply(lambda x: f"{x:.2e}")
        pw_df["significant"] = pw_df["significant"].map({True: "✅ Significant", False: "❌ Not significant"})
        pw_df.columns = ["Comparison", "Adjusted p-value", "Result"]
        st.dataframe(pw_df, hide_index=True, use_container_width=True)

    st.markdown("---")
    st.markdown("### Does This Hold After Controlling for Confounders?")
    st.caption(
        "A regression-adjusted model controls for industry, country, campaign "
        "type, and month — isolating the platform effect from composition bias."
    )
    comp = data["step6"]["comparison"]
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name="Naive (unadjusted)", x=["Meta Ads", "TikTok Ads"],
                           y=[comp["Meta_Ads"]["naive_pct_vs_google"], comp["TikTok_Ads"]["naive_pct_vs_google"]],
                           marker_color="#5a6478"))
    fig3.add_trace(go.Bar(name="Adjusted (controls added)", x=["Meta Ads", "TikTok Ads"],
                           y=[comp["Meta_Ads"]["adjusted_pct_vs_google"], comp["TikTok_Ads"]["adjusted_pct_vs_google"]],
                           marker_color="#5B9BFF"))
    fig3.update_layout(
        barmode="group", height=380,
        yaxis_title="% revenue difference vs. Google Ads",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=40),
    )
    apply_dark(fig3)
    st.plotly_chart(fig3, use_container_width=True)
    st.info(
        "**Reading this chart:** the naive and adjusted bars are nearly identical "
        "(TikTok: 110.8% → 110.6%, Meta: 35.7% → 36.9%). The platform effect "
        "remains highly significant *after controlling for observable campaign "
        "characteristics* — evidence the gap is not simply an artifact of which "
        "industries or countries happen to use each platform more."
    )

    st.markdown("---")
    st.markdown("### Does the Pattern Hold Across Every Slice of the Business?")
    view = st.radio("Break down by:", ["Industry", "Country", "Half-Year"], horizontal=True)
    key_map = {"Industry": "by_industry", "Country": "by_country", "Half-Year": "by_half_year"}
    breakdown = data["step5"][key_map[view]]
    bdf = pd.DataFrame(breakdown)
    fig4 = px.imshow(
        bdf.T, text_auto=".2f", color_continuous_scale="RdYlGn",
        labels=dict(color="Blended ROAS"), aspect="auto",
    )
    fig4.update_layout(height=320, margin=dict(t=20))
    apply_dark(fig4)
    fig4.update_layout(coloraxis_colorbar=dict(tickfont=dict(color=TEXT)))
    st.plotly_chart(fig4, use_container_width=True)
    n_slices = bdf.shape[0]
    tiktok_wins = (bdf.idxmax(axis=1) == "TikTok Ads").sum()
    st.success(
        f"**TikTok Ads leads in {tiktok_wins}/{n_slices} {view.lower()} segments.** "
        "No reversal is observed anywhere — a strong indication this is not a "
        "Simpson's Paradox artifact of aggregation."
    )
with tab3:
    st.markdown("### Interactive Budget Reallocation Simulator")
    st.caption(
        "Drag the slider to control how aggressively you'd reallocate budget "
        "away from the current (spend-weighted) allocation. Higher caps unlock "
        "more theoretical upside but carry more real-world execution risk."
    )

    cap_options = [15, 25, 35, 50, 100]
    cap_choice = st.select_slider(
        "Maximum reallocation per channel",
        options=cap_options, value=25,
        format_func=lambda x: f"±{x}%" + (" (unconstrained)" if x == 100 else ""),
    )
    scenario = data["step4b"]["scenarios"][f"cap_{cap_choice}pct"]
    current = data["step4b"]["current_spend"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Projected daily revenue", f"${scenario['predicted_revenue']:,.0f}",
               f"+${scenario['uplift_daily']:,.0f}")
    c2.metric("Revenue uplift", f"+{scenario['uplift_pct']:.1f}%")
    c3.metric("Annualized impact", f"${scenario['uplift_annualized']/1e6:.2f}M/year")

    if cap_choice == 100:
        st.warning(
            "⚠️ At an unconstrained cap, the optimizer pushes Google Ads down "
            "~83% and TikTok Ads up ~100% — a mathematically optimal but "
            "operationally unrealistic corner solution. No agency would execute "
            "a shift this abrupt in practice; algorithms need a re-learning "
            "period and concentration risk increases. Shown here for reference only."
        )

    st.markdown("##### Recommended Allocation")
    alloc_df = pd.DataFrame({
        "Platform": platforms,
        "Current ($/day)": [current[p] for p in platforms],
        "Recommended ($/day)": [scenario["allocation"][p] for p in platforms],
    })

    fig5 = go.Figure()
    fig5.add_trace(go.Bar(name="Current", x=platforms, y=alloc_df["Current ($/day)"], marker_color="#5a6478"))
    fig5.add_trace(go.Bar(name="Recommended", x=platforms, y=alloc_df["Recommended ($/day)"],
                           marker_color=[PLATFORM_COLORS[p] for p in platforms]))
    fig5.update_layout(barmode="group", height=380, yaxis_title="Daily ad spend ($)",
                        legend=dict(orientation="h", yanchor="bottom", y=1.02), margin=dict(t=40))
    apply_dark(fig5)
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")
    st.markdown("##### Spend–Response Curves (Diminishing Returns Check)")
    st.caption(
        "Fitted saturation curves (Michaelis-Menten) show none of the three "
        "channels have reached their ceiling at current spend levels — the "
        "revenue gap is driven by differing channel efficiency, not by Google "
        "being 'maxed out'."
    )
    fig6 = go.Figure()
    for p in platforms:
        params = data["step3"]["saturation_curve_params"][p]
        cur_spend = data["step3"]["marginal_roas"][p]["avg_daily_spend"]
        x_smooth = np.linspace(1, cur_spend * 3, 100)
        y_smooth = mm_curve(x_smooth, params["vmax"], params["k"])
        fig6.add_trace(go.Scatter(x=x_smooth, y=y_smooth, mode="lines", name=p,
                                    line=dict(color=PLATFORM_COLORS[p], width=3)))
        fig6.add_trace(go.Scatter(
            x=[cur_spend], y=[mm_curve(cur_spend, params["vmax"], params["k"])],
            mode="markers", marker=dict(size=11, color=PLATFORM_COLORS[p], symbol="diamond"),
            showlegend=False, hovertext=[f"{p} — current spend"],
        ))
    fig6.update_layout(height=420, xaxis_title="Daily ad spend ($)", yaxis_title="Predicted daily revenue ($)",
                        legend=dict(orientation="h", yanchor="bottom", y=1.02), margin=dict(t=40))
    apply_dark(fig6)
    st.plotly_chart(fig6, use_container_width=True)

with tab4:
    st.markdown("### Why Is TikTok Outperforming? A Funnel Decomposition")
    st.caption(
        "ROAS = CVR × AOV / CPC. Decomposing the ROAS gap into its funnel "
        "components reveals *where* the advantage comes from — critical for "
        "deciding whether to reallocate budget, fix creative, or adjust bidding."
    )

    decomp = data["step7"]["decomposition_tiktok_vs_google"]
    fig7 = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=["CPC advantage", "CVR advantage", "AOV difference", "Total ROAS gap"],
        y=[decomp["cpc_contribution_pct"], decomp["cvr_contribution_pct"],
           decomp["aov_contribution_pct"], 0],
        text=[f"{decomp['cpc_contribution_pct']:.0f}%", f"{decomp['cvr_contribution_pct']:.0f}%",
              f"{decomp['aov_contribution_pct']:.0f}%", f"{decomp['total_gap_pct']:.0f}%"],
        textposition="outside",
        connector={"line": {"color": BORDER}},
        decreasing={"marker": {"color": "#ef4444"}},
        increasing={"marker": {"color": "#5B9BFF"}},
        totals={"marker": {"color": "#FF3B69"}},
    ))
    fig7.update_layout(height=420, title="TikTok Ads vs. Google Ads — ROAS Gap Decomposition (% contribution)",
                        margin=dict(t=60))
    apply_dark(fig7)
    st.plotly_chart(fig7, use_container_width=True)

    st.info(
        "**95% of TikTok's ROAS advantage comes from a lower cost-per-click "
        "(CPC), not from better conversion rates or higher order values.** "
        "TikTok CPC ($1.02) is 53% cheaper than Google CPC ($2.16), while CVR "
        "(4.7% vs 4.5%) and AOV ($165 vs $168) are nearly identical across "
        "channels. One plausible explanation is that TikTok's lower CPC "
        "reflects a less saturated advertising auction environment — though "
        "this dataset does not include bid density or competitor-count data "
        "to confirm that mechanism directly."
    )

    st.markdown("---")
    st.markdown("### Full Methodology")
    with st.expander("Step-by-step analytical pipeline", expanded=False):
        st.markdown(
            """
1. **Data audit** — structural validation of 1,800 campaign-day records (0 missing values, full-year 2024 coverage, 3 platforms × 5 industries × 7 countries).
2. **Channel benchmarking** — Kruskal-Wallis test + Bonferroni-corrected pairwise Mann-Whitney U tests + 10,000-resample bootstrap confidence intervals on blended ROAS.
3. **Spend–response modeling** — log-log elasticity regression and Michaelis-Menten saturation curve fitting per platform to test for diminishing returns.
4. **Budget optimization** — constrained optimization (SLSQP) maximizing predicted revenue at fixed total budget, with realistic per-channel reallocation caps (15%–50%) to avoid unrealistic corner solutions.
5. **Robustness checks** — re-ran the comparison across every industry, country, and half-year slice to rule out Simpson's Paradox / composition bias.
6. **Causal-adjustment regression** — OLS with HC3 robust standard errors, controlling for industry, country, campaign type, and month fixed effects, comparing naive vs. adjusted platform coefficients.
7. **Funnel decomposition** — log-additive decomposition of ROAS = CVR × AOV / CPC to isolate which funnel stage drives the performance gap.
            """
        )

    with st.expander("⚠️ Limitations (read before applying to a real budget)", expanded=True):
        st.markdown(
            """
- **Association, not proof of causation.** The regression controls for observable
  campaign characteristics (industry, country, campaign type, month) but not for
  unobserved factors — creative quality, audience targeting maturity, brand strength,
  bidding strategy, or campaign objective. The platform effect is best described as
  *"remaining highly significant after controlling for observable factors,"* not as
  a proven causal effect.
- **The "auction saturation" explanation is a hypothesis, not a finding.** The
  dataset has no measure of bid density, impression share, or competitor count.
- **Simulated/aggregated dataset.** This is a public marketing-performance dataset,
  not a live client account — real accounts carry platform-specific tracking
  discrepancies, attribution windows, and view-through conversions not modeled here.
- **Optimization assumes the fitted elasticity curves extrapolate reasonably**
  within the observed spend range; caps were added specifically to avoid
  unrealistic corner-solution recommendations (see Budget Optimizer tab).
            """
        )

    st.markdown("---")
    st.caption(
        "Built as a portfolio case study demonstrating end-to-end marketing "
        "analytics: descriptive statistics → hypothesis testing → optimization "
        "→ robustness validation → causal-adjustment modeling → mechanism analysis."
    )

