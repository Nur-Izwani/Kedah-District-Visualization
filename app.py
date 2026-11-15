
# ============================================================
# SCIENTIFIC VISUALIZATION DASHBOARD
# Malaysia: Household Income, Poverty and Population
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------------------------------------------------
# 1. PAGE CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(
    page_title="Scientific Visualization",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# 2. CUSTOM DESIGN
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded');

.material-symbols-rounded {
    font-family: 'Material Symbols Rounded';
    font-size: 1.15em;
    vertical-align: -0.18em;
}

.stApp {
    background: #F4F7FC;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#123B63 0%,#087E8B 100%);
}

[data-testid="stSidebar"] * {
    color: white;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    display: none !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 9px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: #1E2B42;
    border: 1px solid #34445D;
    border-radius: 14px;
    padding: 10px 14px;
    min-height: 52px;
    width: 100%;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #075B59;
    border: 1.5px solid #20D6C2;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    font-size: 15px;
}

.hero {
    background: linear-gradient(115deg,#123B63 0%,#087E8B 55%,#19A7A1 100%);
    padding: 42px 44px;
    border-radius: 20px;
    margin-bottom: 26px;
    min-height: 178px;
    display: flex;
    align-items: center;
    box-shadow: 0 10px 28px rgba(18,59,99,0.16);
}

.hero h1 {
    color: white;
    font-size: clamp(30px,3vw,43px);
    font-weight: 900;
    letter-spacing: 1.2px;
    margin: 0;
}

.section-heading {
    color: #123B63;
    font-size: 25px;
    font-weight: 800;
    margin: 8px 0 12px 0;
}

.summary-card {
    background: white;
    border: 1px solid #DCE6F2;
    border-top: 4px solid #3984D6;
    border-radius: 14px;
    padding: 22px 24px;
    height: 190px;
    min-height: 190px;
    box-shadow: 0 4px 14px rgba(18,59,99,0.06);
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.summary-label {
    color: #64748B;
    font-size: 14px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 15px;
}

.summary-value {
    color: #123B63;
    font-size: 18px;
    font-weight: 750;
    line-height: 1.55;
}

.summary-detail {
    color: #64748B;
    font-size: 12px;
    line-height: 1.45;
    margin-top: auto;
    padding-top: 10px;
}

.dataset-names {
    font-size: 16px;
    font-weight: 700;
    line-height: 1.65;
}

.objective-card {
    background: white;
    border: 1px solid #DCE6F2;
    border-left: 5px solid #16A6A0;
    border-radius: 14px;
    padding: 17px 22px 19px;
    margin: 8px 0 18px;
    box-shadow: 0 5px 16px rgba(18,59,99,0.07);
}

.objective-card-heading {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #123B63;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 10px;
}

.objective-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 9px;
    background: #E5F7F5;
    color: #0D9488;
}

.objective-period {
    margin-left: auto;
    padding: 5px 10px;
    border-radius: 20px;
    background: #EAF2FB;
    color: #315A82;
    font-size: 11px;
    font-weight: 700;
}

.objective-card p {
    color: #344B63;
    font-size: 15px;
    line-height: 1.6;
    margin: 0;
}

.interpretation-box {
    background: white;
    border: 1px solid #DCE6F2;
    border-left: 4px solid #16A6A0;
    border-radius: 12px;
    padding: 16px 22px;
    margin: 10px 0 20px;
    color: #344B63;
    line-height: 1.8;
}

.interpretation-box ul {
    padding-left: 22px;
    margin: 8px 0 0;
}

.interpretation-box li {
    margin-bottom: 7px;
}

div[data-testid="stPlotlyChart"] {
    background: white;
    border: 1px solid #E1E8F0;
    border-radius: 14px;
    padding: 10px;
}

.footer {
    text-align: center;
    color: #64748B;
    padding: 22px 8px 12px;
    font-size: 12px;
}

@media (max-width: 900px) {
    .summary-card {
        height: auto;
        min-height: 175px;
    }
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 3. DATA LOADING
# ------------------------------------------------------------
@st.cache_data
def load_data():
    income = pd.read_csv("hh_income_district (1).csv")
    poverty = pd.read_csv("hh_poverty_district.csv")
    population = pd.read_csv("population_district (1).csv")
    return income, poverty, population

try:
    df_income, df_poverty, df_pop = load_data()
except Exception as error:
    st.error(f"Dataset loading error: {error}")
    st.info("Check that all three CSV files are in the same folder as app.py.")
    st.stop()

# Standardise column names before validating them.
df_income.columns = df_income.columns.str.strip().str.lower()
df_poverty.columns = df_poverty.columns.str.strip().str.lower()
df_pop.columns = df_pop.columns.str.strip().str.lower()

# ------------------------------------------------------------
# 4. DATA PREPROCESSING
# ------------------------------------------------------------
required_columns = {
    "Income": (df_income, ["state", "district", "date", "income_mean"]),
    "Poverty": (df_poverty, ["state", "district", "date", "poverty_absolute"]),
    "Population": (
        df_pop,
        ["state", "district", "date", "sex", "age", "ethnicity", "population"]
    )
}

for dataset_name, (data, columns) in required_columns.items():
    missing = [c for c in columns if c not in data.columns]
    if missing:
        st.error(f"{dataset_name} dataset is missing: {', '.join(missing)}")
        st.stop()


def clean_base(data):
    data = data.copy()
    data.columns = data.columns.str.strip().str.lower()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["state", "district", "date"]).copy()
    data["state"] = data["state"].astype(str).str.strip()
    data["district"] = data["district"].astype(str).str.strip()
    data["year"] = data["date"].dt.year.astype(int)
    return data


df_income = clean_base(df_income)
df_poverty = clean_base(df_poverty)
df_pop = clean_base(df_pop)

df_income = df_income[df_income["year"].between(2020, 2024)].copy()
df_poverty = df_poverty[df_poverty["year"].between(2020, 2024)].copy()

df_pop = df_pop[
    (df_pop["year"].between(2020, 2024))
    & (df_pop["sex"].astype(str).str.strip().str.lower() == "both")
    & (df_pop["age"].astype(str).str.strip().str.lower() == "overall")
    & (df_pop["ethnicity"].astype(str).str.strip().str.lower() == "overall")
].copy()

for col in ["income_mean", "income_median"]:
    if col in df_income.columns:
        df_income[col] = pd.to_numeric(df_income[col], errors="coerce")

for col in ["poverty_absolute", "poverty_relative"]:
    if col in df_poverty.columns:
        df_poverty[col] = pd.to_numeric(df_poverty[col], errors="coerce")

df_pop["population"] = pd.to_numeric(df_pop["population"], errors="coerce")

# ------------------------------------------------------------
# 5. PREPARE GRAPH 1: HOUSEHOLD INCOME
# ------------------------------------------------------------
income_graph = df_income[
    df_income["year"].isin([2022, 2024])
].dropna(subset=["income_mean"]).copy()

income_graph["year_label"] = income_graph["year"].astype(str)

df_graph1 = (
    income_graph.groupby(
        ["state", "district", "year_label"], as_index=False
    )["income_mean"].mean()
)

df_graph1["district_label"] = (
    df_graph1["district"] + " (" + df_graph1["state"] + ")"
)

# ------------------------------------------------------------
# 6. PREPARE GRAPH 2: POVERTY AND INCOME
# ------------------------------------------------------------
income_scatter = df_income[
    df_income["year"].isin([2022, 2024])
][["state", "district", "year", "income_mean"]].copy()

poverty_scatter = df_poverty[
    df_poverty["year"].isin([2022, 2024])
][["state", "district", "year", "poverty_absolute"]].copy()

# Keep one value for each district and year before merging.
income_scatter = (
    income_scatter.dropna(subset=["income_mean"])
    .groupby(["state", "district", "year"], as_index=False)["income_mean"]
    .mean()
)
poverty_scatter = (
    poverty_scatter.dropna(subset=["poverty_absolute"])
    .groupby(["state", "district", "year"], as_index=False)["poverty_absolute"]
    .mean()
)

income_scatter["year"] = income_scatter["year"].astype(str)
poverty_scatter["year"] = poverty_scatter["year"].astype(str)

df_graph2 = pd.merge(
    income_scatter,
    poverty_scatter,
    on=["state", "district", "year"],
    how="inner"
)

df_graph2["district_label"] = (
    df_graph2["district"] + " (" + df_graph2["state"] + ")"
)

# ------------------------------------------------------------
# 7. PREPARE GRAPH 3: POPULATION
# ------------------------------------------------------------
population_graph = df_pop.dropna(
    subset=["state", "district", "population", "date"]
).copy()

df_graph3 = (
    population_graph.groupby(
        ["state", "district", "year"], as_index=False
    )["population"].mean()
)

df_graph3["district_label"] = (
    df_graph3["district"] + " (" + df_graph3["state"] + ")"
)

# ------------------------------------------------------------
# 8. SHARED DESIGN SETTINGS
# ------------------------------------------------------------
BLUE = "#3984D6"
TEAL = "#16B8A6"
ORANGE = "#F59E0B"
PURPLE = "#8064C8"
NAVY = "#123B63"

plotly_layout = dict(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Arial", size=12, color="#26374A")
)


def summary_card(label, value, detail, accent):
    import re
    label = re.sub(
        r":material/([a-z_]+):",
        r'<span class="material-symbols-rounded">\1</span>',
        label
    )

    st.markdown(
        f"""
        <div class="summary-card" style="border-top-color:{accent};">
            <div class="summary-label">{label}</div>
            <div class="summary-value">{value}</div>
            <div class="summary-detail">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def objective_card(number, icon, period, description):
    st.markdown(
        f"""
        <div class="objective-card">
            <div class="objective-card-heading">
                <span class="objective-icon material-symbols-rounded">{icon}</span>
                <span>OBJECTIVE {number}</span>
                <span class="objective-period">{period}</span>
            </div>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def interpretation_box(points):
    items = "".join(f"<li>{point}</li>" for point in points)
    st.markdown(
        f"""
        <div class="interpretation-box">
            <ul>{items}</ul>
        </div>
        """,
        unsafe_allow_html=True
    )


def style_axes(fig, x_title, y_title, x_format=None, y_format=None):
    fig.update_xaxes(
        title=dict(text=f"<b>{x_title}</b>", font=dict(size=13)),
        showline=True, linewidth=1.8, linecolor="#26374A",
        mirror=True, ticks="outside", showgrid=True,
        gridcolor="#DCE3EA", zeroline=False, tickformat=x_format
    )
    fig.update_yaxes(
        title=dict(text=f"<b>{y_title}</b>", font=dict(size=13)),
        showline=True, linewidth=1.8, linecolor="#26374A",
        mirror=True, ticks="outside", showgrid=True,
        gridcolor="#E8EDF2", zeroline=False, tickformat=y_format
    )
    return fig


# ------------------------------------------------------------
# 9. SIDEBAR NAVIGATION
# ------------------------------------------------------------
st.sidebar.markdown("""
<div style="padding:10px 2px 22px;">
    <div style="font-size:23px;font-weight:900;line-height:1.25;">
        <span class="material-symbols-rounded">query_stats</span><br>
        SCIENTIFIC<br>VISUALIZATION
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### :material/analytics: Select Analysis")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Household Income Analysis",
        "Poverty Analysis",
        "Population Analysis"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.caption("JIE42403 | Scientific Visualization")

# ------------------------------------------------------------
# 10. PAGE HEADER
# ------------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>
        <span class="material-symbols-rounded">query_stats</span>
        SCIENTIFIC VISUALIZATION
    </h1>
</div>
""", unsafe_allow_html=True)

# ============================================================
# PAGE 1: HOME DASHBOARD
# ============================================================
if page == "Home":

    st.markdown("### :material/home: Dashboard Overview")

    c1, c2, c3 = st.columns(3, gap="large")

    with c1:
        summary_card(
            ":material/database: Dataset Names",
            "<span class='dataset-names'>Household Income<br>"
            "Household Poverty<br>Population</span>",
            "Three selected datasets",
            BLUE
        )

    with c2:
        summary_card(
            ":material/public: Study Area",
            "Malaysia",
            "All states and districts",
            TEAL
        )

    with c3:
        summary_card(
            ":material/calendar_month: Study Period",
            "2020–2024",
            "Five-year analysis period",
            PURPLE
        )

    st.markdown("### :material/track_changes: Research Objectives")

    o1, o2, o3 = st.columns(3)

    with o1:
        objective_card(
            1, "payments", "2022 – 2024",
            "To identify and compare the districts with the highest "
            "and lowest mean household income in Malaysia in 2022 and 2024."
        )

    with o2:
        objective_card(
            2, "trending_down", "2022 – 2024",
            "To examine the relationship between absolute poverty "
            "and mean household income across districts in Malaysia."
        )

    with o3:
        objective_card(
            3, "groups", "2020 – 2024",
            "To analyze population trends across districts in Malaysia "
            "from 2020 to 2024."
        )

    st.markdown("### :material/folder_open: Dataset Information")

    t1, t2, t3 = st.tabs([
        ":material/payments: Household Income",
        ":material/trending_down: Household Poverty",
        ":material/groups: Population"
    ])

    with t1:
        st.dataframe(df_income.head(10), use_container_width=True, hide_index=True)

    with t2:
        st.dataframe(df_poverty.head(10), use_container_width=True, hide_index=True)

    with t3:
        st.dataframe(df_pop.head(10), use_container_width=True, hide_index=True)

    st.markdown("### :material/search: Data Coverage")

    coverage = pd.DataFrame({
        "Dataset": ["Household Income", "Household Poverty", "Population"],
        "Available years": [
            ", ".join(map(str, sorted(df_income["year"].unique()))),
            ", ".join(map(str, sorted(df_poverty["year"].unique()))),
            ", ".join(map(str, sorted(df_pop["year"].unique())))
        ],
        "States": [
            df_income["state"].nunique(),
            df_poverty["state"].nunique(),
            df_pop["state"].nunique()
        ],
        "Districts": [
            df_income[["state", "district"]].drop_duplicates().shape[0],
            df_poverty[["state", "district"]].drop_duplicates().shape[0],
            df_pop[["state", "district"]].drop_duplicates().shape[0]
        ]
    })

    st.dataframe(coverage, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 2: HOUSEHOLD INCOME ANALYSIS
# ============================================================
elif page == "Household Income Analysis":

    st.markdown(
        '<div class="section-heading">'
        '<span class="material-symbols-rounded">payments</span> '
        'Visualization 1 – Household Income</div>',
        unsafe_allow_html=True
    )

    objective_card(
        1, "track_changes", "2022 – 2024",
        "To identify and compare the districts with the highest "
        "and lowest mean household income in Malaysia in 2022 and 2024."
    )

    if df_graph1.empty:
        st.warning("No income records are available for 2022 and 2024.")
        st.stop()

    states = sorted(df_graph1["state"].dropna().unique())

    selected_state = st.selectbox(
        ":material/map: Filter by State",
        ["All States"] + states,
        key="income_state_filter"
    )

    income_rank_years = df_graph1.copy()

    if selected_state != "All States":
        income_rank_years = income_rank_years[
            income_rank_years["state"] == selected_state
        ]

    income_view = income_rank_years.copy()

    # Summary values are calculated from the selected area.
    top_records = []
    bottom_records = []

    for year in ["2022", "2024"]:
        year_data = income_rank_years[
            income_rank_years["year_label"] == year
        ]

        if not year_data.empty:
            top_records.append(year_data.nlargest(1, "income_mean").iloc[0])
            bottom_records.append(year_data.nsmallest(1, "income_mean").iloc[0])

    highest_text = "<br>".join(
        f"{r['district']}, {r['state']} ({r['year_label']})"
        for r in top_records
    ) or "No data available"

    highest_values = "<br>".join(
        f"RM{r['income_mean']:,.0f} ({r['year_label']})"
        for r in top_records
    ) or "N/A"

    lowest_text = "<br>".join(
        f"{r['district']}, {r['state']} ({r['year_label']})"
        for r in bottom_records
    ) or "No data available"

    lowest_values = "<br>".join(
        f"RM{r['income_mean']:,.0f} ({r['year_label']})"
        for r in bottom_records
    ) or "N/A"

    s1, s2, s3 = st.columns(3)

    with s1:
        summary_card(
            ":material/emoji_events: Highest Income",
            highest_values,
            highest_text,
            BLUE
        )

    with s2:
        summary_card(
            ":material/flag: Lowest Income",
            lowest_values,
            lowest_text,
            TEAL
        )

    with s3:
        summary_card(
            ":material/calendar_month: Study Period",
            "2022 & 2024",
            "Comparison between two selected years",
            ORANGE
        )

    if selected_state == "All States":

        selected_keys = []

        for year in ["2022", "2024"]:
            year_data = income_view[
                income_view["year_label"] == year
            ]

            selected_keys.append(
                pd.concat([
                    year_data.nlargest(10, "income_mean"),
                    year_data.nsmallest(10, "income_mean")
                ])[["state", "district"]]
            )

        selected_keys = (
            pd.concat(selected_keys)
            .drop_duplicates()
        )

        income_view = income_view.merge(
            selected_keys,
            on=["state", "district"],
            how="inner"
        )

        chart_title = (
            "Top 10 Highest and Lowest Mean Household Income "
            "by District in Malaysia (2022 and 2024)"
        )

    else:
        chart_title = (
            f"Mean Household Income by District in {selected_state} "
            "(2022 and 2024)"
        )

    income_view["district_label"] = (
        income_view["district"] + " (" + income_view["state"] + ")"
    )

    current_2024 = income_view[
        income_view["year_label"] == "2024"
    ]

    district_order = (
        current_2024.sort_values("income_mean")["district_label"].tolist()
    )

    if not district_order:
        district_order = sorted(income_view["district_label"].unique())

    st.markdown("### :material/query_stats: Highest and Lowest Mean Household Income by District")

    fig1 = px.bar(
        income_view,
        x="income_mean",
        y="district_label",
        color="year_label",
        orientation="h",
        barmode="group",
        text="income_mean",
        category_orders={
            "district_label": district_order,
            "year_label": ["2022", "2024"]
        },
        color_discrete_map={"2022": BLUE, "2024": TEAL},
        labels={
            "income_mean": "Mean Household Income (RM)",
            "district_label": "District",
            "year_label": "Year"
        }
    )

    fig1.update_traces(
        texttemplate="RM %{text:,.0f}",
        textposition="outside",
        textfont=dict(size=10, color="#26374A"),
        cliponaxis=False
    )

    fig1.update_layout(
        **plotly_layout,
        height=max(620, len(district_order) * 42),
        title=dict(
            text=f"<b>{chart_title}</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=18, color=NAVY)
        ),
        legend=dict(
            title="<b>Year</b>",
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        ),
        bargap=0.30,
        margin=dict(l=185, r=160, t=95, b=85)
    )

    style_axes(
        fig1,
        "Mean Household Income (RM)",
        "District",
        x_format=",.0f"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # --------------------------------------------------------
    # INTERPRETATION AND DISCUSSION - GRAPH 1
    # --------------------------------------------------------
    st.markdown("### :material/description: Interpretation and Discussion")

    interpretation_box([
        "Sepang, Selangor recorded the highest mean household income in both 2022 and 2024.",
        "The mean household income in Sepang increased from RM13,673 in 2022 to RM15,086 in 2024.",
        "Kecil Lojing, Kelantan recorded the lowest income in 2022, while Pantu, Sarawak recorded the lowest in 2024.",
        "The comparison shows that household income increased in some districts, but the income levels were different across districts.",
        "These differences indicate that household income is not equally distributed among districts in Malaysia."
    ] if selected_state == "All States" else [
        f"The chart compares mean household income across districts in {selected_state} in 2022 and 2024.",
        "The bars show the differences in income levels between districts and between the two selected years.",
        "Districts with longer bars recorded higher mean household income, while shorter bars indicate lower income.",
        "The comparison helps identify changes in household income and differences between districts in the selected state."
    ])

    with st.expander(":material/table_view: View income data"):
        st.dataframe(
            income_view[
                ["state", "district", "year_label", "income_mean"]
            ].sort_values(["state", "district", "year_label"]),
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# PAGE 3: POVERTY ANALYSIS
# ============================================================
elif page == "Poverty Analysis":

    st.markdown(
        '<div class="section-heading">'
        '<span class="material-symbols-rounded">trending_down</span> '
        'Visualization 2 – Poverty and Income</div>',
        unsafe_allow_html=True
    )

    objective_card(
        2, "track_changes", "2022 – 2024",
        "To examine the relationship between absolute poverty "
        "and mean household income across districts in Malaysia."
    )

    if df_graph2.empty:
        st.warning("No matched income and poverty records are available.")
        st.stop()

    poverty_view = df_graph2[
        df_graph2["year"].astype(str).isin(["2022", "2024"])
    ].copy()

    states = sorted(poverty_view["state"].dropna().unique())

    selected_state = st.selectbox(
        ":material/map: Filter by State",
        ["All States"] + states,
        key="poverty_state"
    )

    if selected_state != "All States":
        poverty_view = poverty_view[
            poverty_view["state"] == selected_state
        ].copy()

    if len(poverty_view) < 2:
        st.warning("At least two district-year records are needed.")
        st.stop()

    poverty_view["year_label"] = poverty_view["year"].astype(str)

    correlation = poverty_view[
        ["poverty_absolute", "income_mean"]
    ].corr().iloc[0, 1]

    # Three summary boxes requested for the poverty analysis.
    s1, s2, s3 = st.columns(3)

    with s1:
        summary_card(
            ":material/trending_down: Relationship",
            "Negative relationship",
            "Higher poverty is generally associated with lower household income",
            BLUE
        )

    with s2:
        summary_card(
            ":material/bar_chart: Poverty Rate 0%–15%",
            "RM4,000–RM8,000",
            "Typical mean household income range",
            TEAL
        )

    with s3:
        summary_card(
            ":material/warning: Poverty Rate Above 30%",
            "RM3,000–RM5,000",
            "Typical mean household income range",
            ORANGE
        )

    st.markdown("### :material/search: Absolute Poverty vs Mean Household Income")

    fig2 = px.scatter(
        poverty_view,
        x="poverty_absolute",
        y="income_mean",
        color="year_label",
        hover_name="district_label",
        hover_data={
            "state": True,
            "district": True,
            "year_label": True,
            "poverty_absolute": ":.2f",
            "income_mean": ":,.0f"
        },
        color_discrete_map={"2022": BLUE, "2024": TEAL},
        labels={
            "poverty_absolute": "Absolute Poverty Rate (%)",
            "income_mean": "Mean Household Income (RM)",
            "year_label": "Year"
        }
    )

    fig2.update_traces(
        marker=dict(
            size=12,
            opacity=0.85,
            line=dict(color="#172B4D", width=1.1)
        ),
        selector=dict(mode="markers")
    )

    # Add one linear trendline per year without requiring statsmodels.
    for year_value, line_color in [("2022", BLUE), ("2024", TEAL)]:
        year_data = poverty_view[poverty_view["year_label"] == year_value].dropna(
            subset=["poverty_absolute", "income_mean"]
        )
        if len(year_data) >= 2 and year_data["poverty_absolute"].nunique() >= 2:
            slope, intercept = np.polyfit(
                year_data["poverty_absolute"],
                year_data["income_mean"],
                1
            )
            x_line = np.linspace(
                year_data["poverty_absolute"].min(),
                year_data["poverty_absolute"].max(),
                100
            )
            y_line = slope * x_line + intercept
            fig2.add_scatter(
                x=x_line,
                y=y_line,
                mode="lines",
                name=f"{year_value} Trendline",
                line=dict(color=line_color, width=2, dash="dash"),
                hoverinfo="skip"
            )

    area_title = (
        "Malaysia" if selected_state == "All States"
        else selected_state
    )

    fig2.update_layout(
        **plotly_layout,
        height=680,
        title=dict(
            text=(
                f"<b>Relationship Between Absolute Poverty and Mean "
                f"Household Income in {area_title} (2022 vs 2024)</b>"
            ),
            x=0.5,
            xanchor="center",
            font=dict(size=18, color=NAVY)
        ),
        showlegend=True,
        legend=dict(
            title="Year",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        ),
        margin=dict(l=100, r=130, t=95, b=85)
    )

    style_axes(
        fig2,
        "Absolute Poverty Rate (%)",
        "Mean Household Income (RM)",
        x_format=",.1f",
        y_format=",.0f"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # --------------------------------------------------------
    # INTERPRETATION AND DISCUSSION - GRAPH 2
    # --------------------------------------------------------
    st.markdown("### :material/description: Interpretation and Discussion")

    if pd.isna(correlation):
        correlation_description = "The correlation could not be calculated."
    elif correlation < 0:
        correlation_description = (
            f"The Pearson correlation value of {correlation:.3f} "
            "indicates a negative relationship between absolute poverty "
            "and mean household income."
        )
    elif correlation > 0:
        correlation_description = (
            f"The Pearson correlation value of {correlation:.3f} "
            "indicates a positive relationship between absolute poverty "
            "and mean household income."
        )
    else:
        correlation_description = (
            "The Pearson correlation value of 0 indicates no linear relationship."
        )

    interpretation_box([
        correlation_description,
        "The scatter plot shows the distribution of district records for both 2022 and 2024.",
        "Districts with higher absolute poverty rates generally tend to have lower mean household income.",
        "The trendline helps show the direction of the relationship between poverty and income.",
        "The pattern indicates an association between the two variables, but correlation does not prove causation."
    ])

    with st.expander(":material/table_view: View poverty and income data"):
        st.dataframe(
            poverty_view[
                ["state", "district", "year",
                 "income_mean", "poverty_absolute"]
            ].sort_values(["state", "district", "year"]),
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# PAGE 4: POPULATION ANALYSIS
# ============================================================
elif page == "Population Analysis":

    st.markdown(
        '<div class="section-heading">'
        '<span class="material-symbols-rounded">groups</span> '
        'Visualization 3 – Population</div>',
        unsafe_allow_html=True
    )

    objective_card(
        3, "track_changes", "2020 – 2024",
        "To analyze population trends across districts in Malaysia "
        "from 2020 to 2024."
    )

    if df_graph3.empty:
        st.warning("No population records are available for 2020–2024.")
        st.stop()

    states = sorted(df_graph3["state"].dropna().unique())

    selected_state = st.selectbox(
        ":material/map: Filter by State",
        ["All States"] + states,
        key="population_state"
    )

    if selected_state == "All States":
        population_view = df_graph3.copy()
    else:
        population_view = df_graph3[
            df_graph3["state"] == selected_state
        ].copy()

    if population_view.empty:
        st.warning("No population records are available for this selection.")
        st.stop()

    years = sorted(population_view["year"].unique())
    first_year = years[0]
    last_year = years[-1]

    total_districts = population_view[
        ["state", "district"]
    ].drop_duplicates().shape[0]

    last_year_data = population_view[
        population_view["year"] == last_year
    ]

    highest = last_year_data.nlargest(1, "population")
    lowest = last_year_data.nsmallest(1, "population")

    s1, s2, s3 = st.columns(3)

    with s1:
        summary_card(
            ":material/location_on: Districts Analysed",
            str(total_districts),
            "Selected geographic coverage",
            BLUE
        )

    with s2:
        if not highest.empty:
            row = highest.iloc[0]
            summary_card(
                ":material/emoji_events: Highest Population",
                f"{row['population']:,.0f}",
                f"{row['district']}, {row['state']} ({last_year})",
                TEAL
            )

    with s3:
        if not lowest.empty:
            row = lowest.iloc[0]
            summary_card(
                ":material/push_pin: Lowest Population",
                f"{row['population']:,.0f}",
                f"{row['district']}, {row['state']} ({last_year})",
                ORANGE
            )

    st.markdown("### :material/trending_up: Population Trends by District")

    fig3 = px.line(
        population_view,
        x="year",
        y="population",
        color="state",
        line_group="district_label",
        markers=True,
        hover_name="district_label",
        hover_data={
            "state": True,
            "district": True,
            "year": True,
            "population": ":,.0f"
        },
        labels={
            "year": "Year",
            "population": "Population",
            "state": "State"
        }
    )

    fig3.update_traces(
        line=dict(width=1.8),
        marker=dict(
            size=6,
            line=dict(color="black", width=0.5)
        ),
        opacity=0.78
    )

    area_title = (
        "Malaysia" if selected_state == "All States"
        else selected_state
    )

    fig3.update_layout(
        **plotly_layout,
        height=780,
        title=dict(
            text=f"<b>Population Trends by District in {area_title} "
                 f"(2020–2024)</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=18, color=NAVY)
        ),
        legend=dict(
            title="<b>State</b>",
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            bgcolor="white",
            bordercolor="#D0D7DE",
            borderwidth=1,
            font=dict(size=10)
        ),
        margin=dict(l=95, r=165, t=100, b=85),
        hovermode="closest"
    )

    fig3.update_xaxes(
        title="<b>Year</b>",
        tickmode="linear",
        dtick=1,
        showline=True,
        linewidth=1.8,
        linecolor="#26374A",
        mirror=True,
        ticks="outside",
        showgrid=True,
        gridcolor="#DCE3EA",
        zeroline=False
    )

    fig3.update_yaxes(
        title="<b>Population</b>",
        tickformat=",.0f",
        showline=True,
        linewidth=1.8,
        linecolor="#26374A",
        mirror=True,
        ticks="outside",
        showgrid=True,
        gridcolor="#DCE3EA",
        zeroline=False
    )

    st.plotly_chart(fig3, use_container_width=True)

    # --------------------------------------------------------
    # INTERPRETATION AND DISCUSSION - GRAPH 3
    # --------------------------------------------------------
    st.markdown("### :material/description: Interpretation and Discussion")

    annual_summary = (
        population_view.groupby("year")["population"]
        .mean()
        .reset_index(name="average_population")
    )

    if len(annual_summary) >= 2:
        start_avg = annual_summary.iloc[0]["average_population"]
        end_avg = annual_summary.iloc[-1]["average_population"]

        if end_avg > start_avg:
            overall_trend = "an overall increase"
        elif end_avg < start_avg:
            overall_trend = "an overall decrease"
        else:
            overall_trend = "no overall change"

    else:
        overall_trend = "an unclear overall trend"

    interpretation_points = [
        f"{highest.iloc[0]['district']}, {highest.iloc[0]['state']} recorded the highest population in {last_year}."
        if not highest.empty else "The highest population district could not be identified.",
        f"{lowest.iloc[0]['district']}, {lowest.iloc[0]['state']} recorded the lowest population in {last_year}."
        if not lowest.empty else "The lowest population district could not be identified.",
        f"From {first_year} to {last_year}, the average district population showed {overall_trend}.",
        "The individual lines show that population changes were different across districts.",
        "Some districts experienced population increases, while others showed relatively stable or changing trends over the study period.",
        "These differences indicate that population distribution is not equal across districts in Malaysia."
    ]

    interpretation_box(interpretation_points)

    with st.expander(":material/table_view: View population summary by year"):
        st.dataframe(
            annual_summary,
            use_container_width=True,
            hide_index=True
        )

    with st.expander(":material/table_view: View population data by district"):
        st.dataframe(
            population_view.sort_values(["state", "district", "year"]),
            use_container_width=True,
            hide_index=True
        )

# ------------------------------------------------------------
# 11. FOOTER
# ------------------------------------------------------------
st.markdown("""
<div class="footer">
    <b style="color:#123B63;">SCIENTIFIC VISUALIZATION</b><br>
    JIE42403
</div>
""", unsafe_allow_html=True)
