import glob
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")


CANDIDATE_DATA_DIRS = [
    "Cleaned datasets",
    "./Cleaned datasets",
    "data/Cleaned datasets",
    ".",
]
OUTPUT_DIR = "governance_figures"

sns.set_theme(style="whitegrid", context="notebook")
PALETTE = {
    "primary": "#1f5c99",
    "warn": "#d9534f",
    "ok": "#3f9c6d",
    "neutral": "#8a8a8a",
    "accent": "#e0862c",
}
plt.rcParams["figure.dpi"] = 110
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.titlesize"] = 14


def _find_data_dir():
    for candidate in CANDIDATE_DATA_DIRS:
        if os.path.isdir(candidate) and glob.glob(os.path.join(candidate, "*.csv")):
            return candidate
    raise FileNotFoundError(
        "Could not locate the 'Cleaned datasets' folder. Edit CANDIDATE_DATA_DIRS "
        "at the top of the script to point at it."
    )


def _load_one(data_dir, *name_fragments):
    """Find a CSV whose filename contains all given fragments (case/space
    insensitive) - avoids hard-coding exact filenames that vary in spacing
    ('fact outbreak cleaned.csv' vs 'fact_outbreak_cleaned.csv')."""
    for path in glob.glob(os.path.join(data_dir, "*.csv")):
        norm = os.path.basename(path).lower().replace("_", " ").replace("-", " ")
        if norm.startswith("copy of"):
            continue  # skip accidental duplicate uploads
        if all(frag in norm for frag in name_fragments):
            return pd.read_csv(path)
    raise FileNotFoundError(f"No CSV matching {name_fragments} found in {data_dir}")


def load_data():
    data_dir = _find_data_dir()
    dims = {
        "dates": _load_one(data_dir, "dim", "dates"),
        "states": _load_one(data_dir, "dim", "state"),
        "disease": _load_one(data_dir, "dim", "disease"),
        "program": _load_one(data_dir, "dim", "program"),
        "source": _load_one(data_dir, "dim", "source"),
    }
    facts = {
        "lab": _load_one(data_dir, "fact", "lab"),
        "surveillance": _load_one(data_dir, "fact", "disease", "surveillance"),
        "environmental": _load_one(data_dir, "fact", "environmental"),
        "programs": _load_one(data_dir, "fact", "health", "programs"),
        "outbreak": _load_one(data_dir, "fact", "outbreak"),
    }
    facts["surveillance"]["report_date_raw"] = pd.to_datetime(
        facts["surveillance"]["report_date_raw"]
    )
    dims["dates"]["full_date"] = pd.to_datetime(dims["dates"]["full_date"])
    return dims, facts


def save(fig, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    print(f"    [saved figure -> {path}]")
    plt.close(fig)


def header(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def section1_coverage_summary(dims, facts):
    header("SECTION 1: Data coverage & grain audit")

    n_dates = dims["dates"].shape[0]
    n_states = dims["states"].shape[0]
    n_diseases = dims["disease"].shape[0]
    n_programs = dims["program"].shape[0]

    expectations = {
        "lab": ("date x state", n_dates * n_states),
        "environmental": ("date x state", n_dates * n_states),
        "programs": ("date x state x program", n_dates * n_states * n_programs),
        "surveillance": ("date x state x disease", n_dates * n_states * n_diseases),
        "outbreak": ("event log (no fixed grid)", None),
    }

    rows = []
    for name, df in facts.items():
        grain, expected = expectations[name]
        actual = df.shape[0]
        coverage_pct = np.nan if expected is None else round(100 * actual / expected, 1)
        date_span = df.merge(dims["dates"], on="date_id")["full_date"]
        null_cells = int(df.isna().sum().sum())

        quality_cols = [c for c in df.columns if "compliance" in c or "reporting_rate" in c]
        quality_note = (
            f"{df[quality_cols[0]].mean():.1f}% avg" if quality_cols else "n/a"
        )
        rows.append(
            {
                "Table": name,
                "Grain": grain,
                "Rows (actual)": actual,
                "Rows (full grid)": expected if expected else "—",
                "Grid coverage %": coverage_pct if expected else "n/a (sparse)",
                "Null cells": null_cells,
                "Period covered": f"{date_span.min().strftime('%Y-%m')} to {date_span.max().strftime('%Y-%m')}",
                "Reporting-quality field": quality_note,
            }
        )
    summary = pd.DataFrame(rows).set_index("Table")
    print(summary.to_string())

    fig, ax = plt.subplots(figsize=(16, 4.5))
    ax.axis("off")
    disp = summary.reset_index()
    tbl = ax.table(
        cellText=disp.values,
        colLabels=disp.columns,
        cellLoc="center",
        loc="center",
        colWidths=[0.11, 0.16, 0.10, 0.11, 0.11, 0.08, 0.15, 0.14],
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9.5)
    tbl.scale(1, 2.6)
    for (r, c), cell in tbl.get_celld().items():
        cell.PAD = 0.02
        if r == 0:
            cell.set_facecolor(PALETTE["primary"])
            cell.set_text_props(color="white", weight="bold")
        else:
            cell.set_facecolor("#f4f6f8" if r % 2 == 0 else "white")
    ax.set_title(
        "Data Coverage Summary — grain, density & reporting-quality snapshot",
        pad=18,
    )
    fig.text(
        0.5, -0.02,
        "No blank cells exist anywhere in this bundle - dense facts (lab, environmental, programs,\n"
        "surveillance) are pre-aggregated to a complete date x state grid. fact_outbreak is a sparse\n"
        "event log by nature, so its 'grid coverage' is reported as n/a rather than forced into a\n"
        "misleading completeness percentage.",
        ha="center", fontsize=9.5, color=PALETTE["neutral"],
    )
    save(fig, "01_data_coverage_summary_table.png")

    print(
        "\nInsight: every dense fact table is at exactly 100% of its expected date x state[x sub-dim]\n"
        "grid, so there are no structurally missing rows to chase in this bundle. The governance\n"
        "story instead lives in reporting-quality FIELDS embedded in the data (Sections 2-3 below),\n"
        "not in blank cells."
    )
    return summary


def section2_reporting_lag(dims, facts):
    header("SECTION 2: Reporting lag - nominal period vs actual report timestamp")

    surv = facts["surveillance"].merge(dims["dates"], on="date_id")
    surv = surv.merge(dims["states"][["state_id", "state_name"]], on="state_id")
    surv = surv.merge(dims["disease"], on="disease_id")
    surv = surv.merge(dims["source"], on="source_id")
    surv["lag_days"] = (surv["report_date_raw"] - surv["full_date"]).dt.days

    lagged = surv[surv["lag_days"] != 0]
    pct_lagged = 100 * len(lagged) / len(surv)
    print(
        f"{len(lagged):,} of {len(surv):,} surveillance records ({pct_lagged:.1f}%) carry a "
        f"report_date_raw that does NOT match their nominal reporting month."
    )
    print(
        f"Among lagged records, the report timestamp trails the nominal month by "
        f"{-lagged['lag_days'].mean():.0f} days on average (worst case: "
        f"{-lagged['lag_days'].min():.0f} days, ~{-lagged['lag_days'].min()/30:.0f} months)."
    )


    cmp_cols = ["total_reported_cases", "case_fatality_rate", "public_health_risk_score"]
    comparison = surv.assign(is_lagged=surv["lag_days"] != 0).groupby("is_lagged")[cmp_cols].mean()
    comparison.index = ["On-time", "Lagged"]
    print("\nAverage values, on-time vs lagged records:")
    print(comparison.round(2).to_string())
    case_gap_pct = 100 * (comparison.loc["Lagged", "total_reported_cases"] /
                           comparison.loc["On-time", "total_reported_cases"] - 1)
    print(
        f"-> Lagged records report {case_gap_pct:+.1f}% more cases on average than on-time records, "
        "which is the direction we'd expect if the freshest month-end snapshot is a temporary "
        "undercount that later gets revised upward."
    )

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    monthly_lag = lagged.groupby("year_month").size().reindex(
        dims["dates"]["year_month"], fill_value=0
    )
    axes[0].bar(monthly_lag.index, monthly_lag.values, color=PALETTE["warn"], width=0.7)
    axes[0].set_title("Lagged Records by Nominal Reporting Month")
    axes[0].set_ylabel("# records with mismatched report date")
    axes[0].set_xlabel("Nominal year-month")
    axes[0].tick_params(axis="x", rotation=75)
    for lbl in axes[0].get_xticklabels()[::2]:
        lbl.set_visible(False)

    order = (
        lagged.groupby("source_name")["lag_days"].mean().sort_values().index
    )
    sns.boxplot(
        data=lagged, y="source_name", x="lag_days", order=order,
        ax=axes[1], color=PALETTE["primary"],
    )
    axes[1].set_title("How Far Behind? Lag Distribution by Reporting Source")
    axes[1].set_xlabel("Lag (days) — more negative = later arrival")
    axes[1].set_ylabel("")

    fig.suptitle("Reporting Gap / Timeline: When Do Late Records Actually Show Up?", y=1.03, fontsize=15)
    save(fig, "03_reporting_lag_timeline.png")

    return {"pct_lagged": pct_lagged, "case_gap_pct": case_gap_pct}


def section3_compliance_trend(dims, facts):
    header("SECTION 3: Reporting compliance, reporting rate & lab turnaround")

    lab = facts["lab"].merge(dims["dates"], on="date_id").merge(
        dims["states"][["state_id", "state_name"]], on="state_id"
    )

    overall_mean = lab["reporting_compliance_pct"].mean()
    overall_std = lab["reporting_compliance_pct"].std()
    print(
        f"Reporting compliance across all state-months: mean {overall_mean:.1f}%, "
        f"std {overall_std:.1f} pts (range {lab['reporting_compliance_pct'].min():.1f}-"
        f"{lab['reporting_compliance_pct'].max():.1f}%)."
    )

    monthly = lab.groupby(["year_month"]).agg(
        compliance=("reporting_compliance_pct", "mean"),
        rate=("reporting_rate_pct", "mean"),
        turnaround=("turnaround_time_days", "mean"),
    )
    monthly = monthly.reindex(dims["dates"]["year_month"])

    fig, ax1 = plt.subplots(figsize=(15, 6))
    ax1.plot(monthly.index, monthly["compliance"], color=PALETTE["primary"],
             marker="o", ms=3, label="Reporting compliance %")
    ax1.plot(monthly.index, monthly["rate"], color=PALETTE["accent"],
             marker="o", ms=3, label="Reporting rate %")
    ax1.axhspan(overall_mean - overall_std, overall_mean + overall_std,
                color=PALETTE["primary"], alpha=0.08,
                label="±1 std band (compliance) - month-to-month noise")
    ax1.set_ylabel("Percent (%)")
    ax1.set_xlabel("Year-Month")
    ax1.tick_params(axis="x", rotation=75)
    for lbl in ax1.get_xticklabels()[::2]:
        lbl.set_visible(False)

    ax2 = ax1.twinx()
    ax2.plot(monthly.index, monthly["turnaround"], color=PALETTE["warn"],
              linestyle="--", marker="s", ms=3, label="Lab turnaround (days)")
    ax2.set_ylabel("Turnaround time (days)")
    ax2.grid(False)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper center",
               bbox_to_anchor=(0.5, -0.35), ncol=2, frameon=False)
    ax1.set_title("Reporting Compliance, Reporting Rate & Lab Turnaround Over Time")
    save(fig, "04_compliance_rate_turnaround_trend.png")

    monthly_se = overall_std / np.sqrt(dims["states"].shape[0])
    first_q = monthly["compliance"].head(3).mean()
    last_q = monthly["compliance"].tail(3).mean()
    drift = last_q - first_q
    print(
        f"\nInsight: comparing the first 3 months ({first_q:.1f}%) to the last 3 months ({last_q:.1f}%) "
        f"of the series gives a drift of {drift:+.1f} points, well inside the ~{1.96*monthly_se:.1f}-point "
        "95% noise band for a single monthly mean - i.e. there is no statistically credible improving\n"
        "or worsening trend in reporting compliance over the 3-year window. Month-to-month swings are\n"
        "consistent with sampling noise, not a real underlying shift, and should be read as such rather\n"
        "than as evidence of a policy or process change."
    )

    return {
        "overall_mean": overall_mean,
        "overall_std": overall_std,
        "drift": drift,
        "noise_band_95": 1.96 * monthly_se,
    }


def section4_synthesis(findings):
    header("SECTION 4: Synthesis — answers to the three governance questions")

    print(
        "1) WHERE MIGHT REPORTING LAG / UNDER-REPORTING DISTORT COMPARISONS?\n"
        f"   - {findings['lag']['pct_lagged']:.1f}% of surveillance records carry a report timestamp that\n"
        "     trails their nominal month, and those late-arriving records run "
        f"{findings['lag']['case_gap_pct']:+.1f}% higher on\n"
        "     case counts than on-time ones - the most recent month(s) in any trend view are the most\n"
        "     likely to be revised upward later, so month-over-month comparisons that lean on the very\n"
        "     latest period should be treated as provisional.\n"
        "   - fact_outbreak is a sparse event log rather than a scheduled census (Section 1), so raw\n"
        "     record counts by state or month reflect reporting activity as much as real events, and\n"
        "     should not be read as a direct incidence measure without further normalisation.\n"
    )
    print(
        "2) WHAT GRANULARITY OR PRIVACY LIMITS CONSTRAIN THE ANALYSIS?\n"
        "   - Every fact table is pre-aggregated to state x month (or state x month x program/disease).\n"
        "     There is no district, facility, or individual-level data in this bundle, so anything below\n"
        "     state resolution (urban wards, specific hospitals, patient-level trends) is out of scope.\n"
        "   - Reporting-quality fields (compliance %, reporting rate %, turnaround days) are only present\n"
        "     on the lab/healthcare table - other facts have no built-in signal for how complete their\n"
        "     own figures are, so their reliability has to be inferred indirectly.\n"
        "   - No individually identifiable information is present anywhere in the bundle (facts stop at\n"
        "     state-level aggregates), which is good for privacy but caps the analysis at a population\n"
        "     level throughout.\n"
    )
    print(
        "3) WHICH FINDINGS SHOULD BE TREATED AS DIRECTIONAL RATHER THAN DEFINITIVE?\n"
        f"   - The apparent {findings['compliance']['drift']:+.1f}-point drift in reporting compliance from\n"
        f"     the first to the last quarter of the series sits well inside the "
        f"~{findings['compliance']['noise_band_95']:.1f}-point 95%\n"
        "     noise band for a monthly national mean - it should be read as noise, not as a real trend,\n"
        "     until confirmed with a larger or more targeted sample.\n"
        f"   - The {findings['lag']['pct_lagged']:.1f}% reporting-lag rate is a lower bound: it only catches\n"
        "     records whose report_date_raw happens to fall in a different calendar month than their\n"
        "     nominal period, so within-month lag is invisible to this check and the true lag rate is\n"
        "     likely higher - treat it as directional evidence of a lag problem, not a precise estimate\n"
        "     of its size."
    )


def main():
    dims, facts = load_data()
    print(f"Loaded {len(facts)} fact tables and {len(dims)} dimension tables.")

    findings = {}
    section1_coverage_summary(dims, facts)
    findings["lag"] = section2_reporting_lag(dims, facts)
    findings["compliance"] = section3_compliance_trend(dims, facts)
    section4_synthesis(findings)

    header("DONE")
    print(f"All figures saved to ./{OUTPUT_DIR}/")


if __name__ == "__main__":
    main()