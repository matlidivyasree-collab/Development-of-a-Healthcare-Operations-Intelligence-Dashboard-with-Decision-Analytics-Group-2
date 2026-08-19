# ================================================================
# STYLING helpers specific to the Health Programs & Population
# Vulnerability page.
#
# Deliberately does NOT include the original apply_theme() from this
# dashboard's own submission — the shared src/styling.py already
# injects sidebar/background/KPI-card CSS app-wide (inject_css()),
# and calling a second, competing global stylesheet here would risk
# fighting it. Only the chart palette + style_chart() helper (which
# just themes individual Plotly figures, not the page chrome) are
# kept, values matched to the same brand palette used everywhere
# else in the app.
# ================================================================

NAVY = "#17324D"
TEAL = "#0F6B78"
BACKGROUND = "#F5F7FA"
CARD = "#FFFFFF"
CHARCOAL = "#000000"
SLATE = "#47586B"
GREEN = "#16855B"
AMBER = "#C98A00"
RED = "#C43D3D"

CATEGORY_COLOURS = [TEAL, NAVY, AMBER, GREEN, SLATE, RED, "#4C8FA8", "#8A6D3B"]

# Risk scale — Low = Green (safe), Medium = Yellow (warning), High = Red
# (critical). Matches the RISK_HEATMAP_SCALE used elsewhere in the app so
# every risk-coded chart/heatmap in the suite reads the same way.
RISK_SCALE = [
    [0.0, "#C9EAD3"],   # Low / safe -> green
    [0.5, "#FFE9A8"],   # Medium / warning -> yellow
    [1.0, "#F6B4AE"],   # High / critical -> red
]
VULNERABILITY_SCALE = [BACKGROUND, "#7FB8C4", TEAL, NAVY]


def style_chart(fig):
    """Applied to every chart on this page so they share one look."""
    fig.update_layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font_color=CHARCOAL,
        title_font_color=NAVY,
        margin=dict(t=60, b=60),
    )
    fig.update_xaxes(gridcolor="#E3E8EF", zerolinecolor="#E3E8EF")
    fig.update_yaxes(gridcolor="#E3E8EF", zerolinecolor="#E3E8EF")
    return fig
