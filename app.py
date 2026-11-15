# ============================================================
# MALAYSIA DATA INSIGHTS
# Scientific Visualization Dashboard
# Based on the latest Google Colab notebook
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------
# 1. PAGE CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(
    page_title="Malaysia Data Insights",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# 2. CUSTOM DESIGN
# ------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0,0');

    .material-symbols-rounded {
        font-family: 'Material Symbols Rounded';
        font-weight: normal;
        font-style: normal;
        font-size: 1.15em;
        line-height: 1;
        display: inline-flex;
        vertical-align: -0.18em;
        white-space: nowrap;
        direction: ltr;
        -webkit-font-feature-settings: 'liga';
        -webkit-font-smoothing: antialiased;
    }

    .stApp {
        background: #F4F7FC;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #123B63 0%, #087E8B 100%);
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    /* Navigation options styled as rounded cards */
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
        display: flex;
        align-items: center;
        transition: all 0.2s ease;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #263B55;
        border-color: #20C9B5;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: #075B59;
        border: 1.5px solid #20D6C2;
        box-shadow: 0 3px 12px rgba(0, 214, 194, 0.12);
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
        font-weight: 750;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label p {
        font-size: 15px;
        margin: 0;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] input {
        accent-color: #E34B67;
    }

    .hero {
        background: linear-gradient(115deg, #123B63, #087E8B, #19A7A1);
        padding: 30px 34px;
        border-radius: 18px;
        margin-bottom: 22px;
        box-shadow: 0 8px 22px rgba(18, 59, 99, 0.13);
    }

    .hero h1 {
        color: #FFFFFF;
        font-size: 34px;
        font-weight: 800;
        margin: 0;
    }

    .hero p {
        color: #E7F6FF;
        font-size: 15px;
        margin: 8px 0 0 0;
    }

    .section-heading {
        color: #123B63;
        font-size: 25px;
        font-weight: 800;
        margin: 8px 0 12px 0;
    }

    .objective-card {
        background: #FFFFFF;
        border: 1px solid #DCE6F2;
        border-left: 5px solid #16A6A0;
        border-radius: 15px;
        padding: 24px 24px;
        margin: 8px 0 20px 0;
        height: 250px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        box-shadow: 0 3px 12px rgba(18, 59, 99, 0.05);
    }

    .objective-card h4 {
        color: #123B63;
        font-size: 22px;
        font-weight: 750;
        margin: 0 0 20px 0;
    }

    .objective-card p {
        color: #40536A;
        font-size: 16px;
        margin: 0;
        line-height: 1.7;
    }

    @media (max-width: 900px) {
        .objective-card {
            height: auto;
            min-height: 190px;
        }
    }

    .objective-card h4 {
        color: #123B63;
        margin: 0 0 8px 0;
    }

    .objective-card p {
        color: #40536A;
        margin: 0;
        line-height: 1.6;
    }

    /* Compact, polished objective panel for visualization pages */
    .objective-card.objective-compact {
        height: auto;
        min-height: 0;
        padding: 17px 22px 19px 22px;
        margin: 8px 0 18px 0;
        border-left: 5px solid #16A6A0;
        border-radius: 14px;
        background: linear-gradient(115deg, #FFFFFF 0%, #F8FCFF 100%);
        box-shadow: 0 5px 16px rgba(18, 59, 99, 0.07);
        gap: 10px;
    }

    .objective-card.objective-compact .objective-card-heading {
        display: flex;
        align-items: center;
        gap: 9px;
        color: #123B63;
        font-size: 15px;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin-bottom: 2px;
    }

    .objective-card.objective-compact .objective-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 9px;
        background: #E5F7F5;
        color: #0D9488;
        font-size: 20px;
    }

    .objective-card.objective-compact .objective-period {
        margin-left: auto;
        padding: 5px 10px;
        border-radius: 20px;
        background: #EAF2FB;
        color: #315A82;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.2px;
    }

    .objective-card.objective-compact p {
        color: #344B63;
        font-size: 15px;
        line-height: 1.55;
        margin: 0;
    }

    @media (max-width: 640px) {
        .objective-card.objective-compact {
            padding: 15px 16px;
        }
        .objective-card.objective-compact .objective-period {
            font-size: 10px;
            padding: 4px 7px;
        }
    }

    .summary-card {
        background: #FFFFFF;
        border: 1px solid #DCE6F2;
        border-top: 4px solid #3984D6;
        border-radius: 13px;
        padding: 17px 18px;
        min-height: 118px;
        box-shadow: 0 3px 12px rgba(18, 59, 99, 0.05);
    }

    .summary-label {
        color: #64748B;
        font-size: 13px;
        font-weight: 650;
    }

    .summary-value {
        color: #123B63;
        font-size: 25px;
        font-weight: 800;
        margin-top: 7px;
        line-height: 1.2;
    }

    .summary-detail {
        color: #64748B;
        font-size: 12px;
        margin-top: 5px;
    }

    .info-note {
        background: #EAF4FF;
        border-left: 4px solid #3984D6;
        border-radius: 9px;
        padding: 13px 16px;
        color: #23476B;
        margin: 12px 0;
    }

    div[data-testid="stPlotlyChart"] {
        background: #FFFFFF;
        border: 1px solid #E1E8F0;
        border-radius: 14px;
        padding: 10px;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #DCE6F2;
        border-radius: 12px;
        padding: 14px;
    }

    .footer {
        text-align: center;
        color: #64748B;
        padding: 22px 8px 12px 8px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 3. DATA LOADING
#    File names match the current GitHub repository.
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
    st.info(
        "Semak nama fail CSV dalam GitHub. Pastikan ketiga-tiga fail "
        "berada dalam folder yang sama dengan app.py."
    )
    st.stop()

# ------------------------------------------------------------
# 4. DATA PREPROCESSING
#    Follows the latest Colab notebook:
#    Income/Poverty: 2020-2024 source filter
#    Population: 2020-2024, both/overall/overall
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
    missing = [column for column in columns if column not in data.columns]
    if missing:
        st.error(
            f"{dataset_name} dataset is missing these columns: "
            + ", ".join(missing)
        )
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

# Population demographic filter exactly as Colab
df_pop = df_pop[
    (df_pop["year"].between(2020, 2024))
    & (df_pop["sex"].astype(str).str.strip().str.lower() == "both")
    & (df_pop["age"].astype(str).str.strip().str.lower() == "overall")
    & (df_pop["ethnicity"].astype(str).str.strip().str.lower() == "overall")
].copy()

# Income and poverty year range from Colab
df_income = df_income[df_income["year"].between(2020, 2024)].copy()
df_poverty = df_poverty[df_poverty["year"].between(2020, 2024)].copy()

# Convert numeric variables
for col in ["income_mean", "income_median"]:
    if col in df_income.columns:
        df_income[col] = pd.to_numeric(df_income[col], errors="coerce")

for col in ["poverty_absolute", "poverty_relative"]:
    if col in df_poverty.columns:
        df_poverty[col] = pd.to_numeric(df_poverty[col], errors="coerce")

df_pop["population"] = pd.to_numeric(df_pop["population"], errors="coerce")

# ------------------------------------------------------------
# 5. PREPARE VISUALIZATION 1
#    Grouped Horizontal Bar Chart (2022 vs 2024)
#    Same approach as latest Colab notebook
# ------------------------------------------------------------
income_graph = df_income[
    df_income["year"].isin([2022, 2024])
].dropna(subset=["state", "district", "income_mean"]).copy()

income_graph["year_label"] = income_graph["year"].astype(str)

df_graph1 = (
    income_graph
    .groupby(["state", "district", "year_label"], as_index=False)
    ["income_mean"].mean()
)

df_graph1["district_label"] = (
    df_graph1["district"] + " (" + df_graph1["state"] + ")"
)

district_order = (
    df_graph1.groupby("district_label")["income_mean"]
    .mean()
    .sort_values(ascending=True)
    .index.tolist()
)

# ------------------------------------------------------------
# 6. PREPARE VISUALIZATION 2
#    Scatter Plot with Trendline (2022 vs 2024)
# ------------------------------------------------------------
income_scatter = df_income[
    df_income["year"].isin([2022, 2024])
][["state", "district", "year", "income_mean"]].copy()

poverty_scatter = df_poverty[
    df_poverty["year"].isin([2022, 2024])
][["state", "district", "year", "poverty_absolute"]].copy()

income_scatter["year"] = income_scatter["year"].astype(str)
poverty_scatter["year"] = poverty_scatter["year"].astype(str)

income_scatter = income_scatter.dropna(subset=["income_mean"])
poverty_scatter = poverty_scatter.dropna(subset=["poverty_absolute"])

df_graph2 = pd.merge(
    income_scatter,
    poverty_scatter,
    on=["state", "district", "year"],
    how="inner",
    validate="one_to_one"
)

df_graph2["district_label"] = (
    df_graph2["district"] + " (" + df_graph2["state"] + ")"
)

# ------------------------------------------------------------
# 7. PREPARE VISUALIZATION 3
#    Multi-Line Chart (2020-2024)
#    Same approach as latest Colab notebook
# ------------------------------------------------------------
population_graph = df_pop[
    df_pop["year"].between(2020, 2024)
].dropna(
    subset=["state", "district", "population", "date"]
).copy()

df_graph3 = (
    population_graph
    .groupby(["state", "district", "year"], as_index=False)
    ["population"].mean()
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

def style_axes(fig, x_title, y_title, x_format=None, y_format=None):
    fig.update_xaxes(
        title=dict(text=f"<b>{x_title}</b>", font=dict(size=13)),
        showline=True, linewidth=1.8, linecolor="#26374A",
        mirror=True, ticks="outside", tickcolor="#26374A",
        showgrid=True, gridcolor="#DCE3EA", zeroline=False,
        tickformat=x_format
    )
    fig.update_yaxes(
        title=dict(text=f"<b>{y_title}</b>", font=dict(size=13)),
        showline=True, linewidth=1.8, linecolor="#26374A",
        mirror=True, ticks="outside", tickcolor="#26374A",
        showgrid=True, gridcolor="#E8EDF2", zeroline=False,
        tickformat=y_format
    )
    return fig

# ------------------------------------------------------------
# 9. SIDEBAR NAVIGATION
# ------------------------------------------------------------
st.sidebar.markdown(
    """
    <div style="padding:10px 2px 16px 2px;">
        <div style="font-size:23px;font-weight:850;line-height:1.2;">
            <span class="material-symbols-rounded">query_stats</span> MALAYSIA<br>DATA INSIGHTS
        </div>
        <div style="font-size:12px;color:#D8F0F5;margin-top:8px;">
            Scientific Visualization Dashboard
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

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
st.sidebar.markdown("### :material/info: STUDY INFORMATION")
st.sidebar.markdown(
    """
    **Study Area:** Malaysia

    **Analysis Level:** State and District

    **Income & Poverty:** 2022 and 2024

    **Population:** 2020–2024
    """
)
st.sidebar.markdown("---")
st.sidebar.caption("JIE42403 | Scientific Visualization")

# ------------------------------------------------------------
# 10. PAGE HEADER
# ------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1><span class="material-symbols-rounded">query_stats</span> MALAYSIA DATA INSIGHTS</h1>
        <p>Household Income, Poverty and Population Analysis</p>
        <p>Scientific Visualization Project · Malaysia · 2020–2024</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PAGE 1: DASHBOARD
# ============================================================
if page == "Home":

    st.markdown(
        '<div class="section-heading"><span class="material-symbols-rounded">home</span> Dashboard Overview</div>',
        unsafe_allow_html=True
    )
    st.write(
        "This dashboard presents socioeconomic and demographic "
        "patterns across states and districts in Malaysia using "
        "household income, household poverty and population datasets."
    )

    total_states = df_pop["state"].nunique()
    total_districts = df_pop[["state", "district"]].drop_duplicates().shape[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        summary_card(":material/map: States", f"{total_states}", "Population dataset", BLUE)
    with c2:
        summary_card(":material/location_on: Districts", f"{total_districts}", "Population dataset", TEAL)
    with c3:
        summary_card(":material/payments: Income & Poverty", "2022 / 2024", "Comparison years", ORANGE)
    with c4:
        summary_card(":material/groups: Population", "2020–2024", "Five-year study period", PURPLE)

    st.markdown("### :material/track_changes: Research Objectives")

    o1, o2, o3 = st.columns(3)

    with o1:
        st.markdown(
            """
            <div class="objective-card">
                <h4>Objective 1</h4>
                <p>To identify and compare the districts with the highest and lowest mean household income in Malaysia in 2022 and 2024.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with o2:
        st.markdown(
            """
            <div class="objective-card">
                <h4>Objective 2</h4>
                <p>To examine the relationship between absolute poverty and mean household income across districts in Malaysia.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with o3:
        st.markdown(
            """
            <div class="objective-card">
                <h4>Objective 3</h4>
                <p>To analyze population trends across districts in Malaysia from 2020 to 2024.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### :material/folder_open: Dataset Information")
    t1, t2, t3 = st.tabs(
        [":material/payments: Household Income", ":material/trending_down: Household Poverty", ":material/groups: Population"]
    )

    with t1:
        st.caption("Household income dataset · 2020–2024 source filter")
        st.dataframe(df_income.head(10), use_container_width=True, hide_index=True)

    with t2:
        st.caption("Household poverty dataset · 2020–2024 source filter")
        st.dataframe(df_poverty.head(10), use_container_width=True, hide_index=True)

    with t3:
        st.caption("Population dataset · 2020–2024 · both / overall / overall")
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
# PAGE 2: VISUALIZATION 1 - INCOME
# ============================================================
elif page == "Household Income Analysis":

    st.markdown(
        '<div class="section-heading"><span class="material-symbols-rounded">payments</span> Visualization 1 – Household Income</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="objective-card objective-compact">
            <div class="objective-card-heading"><span class="objective-icon material-symbols-rounded">track_changes</span><span>OBJECTIVE 1</span><span class="objective-period">2022 – 2024</span></div>
            <p>To identify and compare the districts with the highest and lowest mean household income in Malaysia in 2022 and 2024.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df_graph1.empty:
        st.warning("No income records are available for 2022 and 2024.")
    else:
        states = sorted(df_graph1["state"].dropna().unique())
        selected_state = st.selectbox(
            ":material/map: Filter by State",
            ["All States"] + states,
            key="income_state_filter"
        )

        # Rank districts separately for 2022 and 2024.
        # The combined list includes each year's Top 10 and Bottom 10 districts.
        income_rank_years = df_graph1[
            df_graph1["year_label"].isin(["2022", "2024"])
        ].dropna(subset=["income_mean"]).copy()

        if selected_state == "All States":
            selected_keys_list = []

            for ranking_year in ["2022", "2024"]:
                year_data = income_rank_years[
                    income_rank_years["year_label"] == ranking_year
                ].copy()

                top10_year = year_data.nlargest(10, "income_mean")
                bottom10_year = year_data.nsmallest(10, "income_mean")

                selected_keys_list.append(
                    pd.concat([top10_year, bottom10_year])[["state", "district"]]
                )

            selected_keys = (
                pd.concat(selected_keys_list)
                .drop_duplicates()
                .reset_index(drop=True)
            )

            income_view = df_graph1.merge(
                selected_keys,
                on=["state", "district"],
                how="inner"
            )

            view_description = (
                "Top 10 highest and Top 10 lowest districts are identified "
                "separately for 2022 and 2024 across Malaysia."
            )
            chart_title = (
                "Top 10 Highest and Lowest Mean Household Income "
                "by District in Malaysia (2022 and 2024)"
            )
            ranking_note = (
                "Districts are ranked separately for each year. The chart "
                "compares 2022 and 2024 values for the combined list of "
                "districts selected from both years."
            )
        else:
            income_view = df_graph1[
                df_graph1["state"] == selected_state
            ].copy()
            view_description = f"All available districts in {selected_state}."
            chart_title = (
                f"Mean Household Income by District in {selected_state} "
                "(2022 and 2024)"
            )
            ranking_note = (
                f"All available districts in {selected_state} are displayed "
                "for comparison between 2022 and 2024."
            )

        if income_view.empty:
            st.warning("No district income records are available for this selection.")
        else:
            # Summary statistics are based on the 2024 values in the current view.
            current_2024 = income_view[
                income_view["year_label"] == "2024"
            ].dropna(subset=["income_mean"]).copy()

            highest_2024 = current_2024.nlargest(1, "income_mean")
            lowest_2024 = current_2024.nsmallest(1, "income_mean")
            district_count = current_2024[["state", "district"]].drop_duplicates().shape[0]

            s1, s2, s3 = st.columns(3)
            with s1:
                summary_card(
                    ":material/location_on: Districts Displayed",
                    str(district_count),
                    "Up to 40 unique districts selected from yearly Top 10 and Bottom 10 rankings" if selected_state == "All States" else f"All districts in {selected_state}",
                    BLUE
                )
            with s2:
                if not highest_2024.empty:
                    row = highest_2024.iloc[0]
                    summary_card(
                        ":material/emoji_events: Highest Income (2024)",
                        f"RM {row['income_mean']:,.0f}",
                        f"{row['district']}, {row['state']}",
                        TEAL
                    )
            with s3:
                if not lowest_2024.empty:
                    row = lowest_2024.iloc[0]
                    summary_card(
                        ":material/flag: Lowest Income (2024)",
                        f"RM {row['income_mean']:,.0f}",
                        f"{row['district']}, {row['state']}",
                        ORANGE
                    )

            st.markdown("### :material/query_stats: Highest and Lowest Mean Household Income by District")
            st.caption(view_description + " " + ranking_note)

            # Sort districts by their 2024 mean income so the chart reads
            # from lower to higher income, regardless of the filter selected.
            district_order = (
                current_2024.sort_values("income_mean", ascending=True)
                .assign(district_label=lambda x: x["district"] + " (" + x["state"] + ")")["district_label"]
                .tolist()
            )

            # Keep a stable district label in case the dataframe is filtered.
            income_view = income_view.copy()
            income_view["district_label"] = (
                income_view["district"].astype(str)
                + " ("
                + income_view["state"].astype(str)
                + ")"
            )

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
                color_discrete_map={
                    "2022": BLUE,
                    "2024": TEAL
                },
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
                    x=1.02,
                    bgcolor="white",
                    bordercolor="#D0D7DE",
                    borderwidth=1
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

            st.markdown("### :material/description: Interpretation and Discussion")
            inc22 = income_view.loc[
                income_view["year_label"] == "2022", "income_mean"
            ].mean()
            inc24 = income_view.loc[
                income_view["year_label"] == "2024", "income_mean"
            ].mean()

            if pd.notna(inc22) and pd.notna(inc24):
                difference = inc24 - inc22
                if difference > 0:
                    trend = "increased"
                elif difference < 0:
                    trend = "decreased"
                else:
                    trend = "remained unchanged"

                st.write(
                    f"For the districts displayed, the average mean household income "
                    f"{trend} from RM {inc22:,.0f} in 2022 to RM {inc24:,.0f} "
                    f"in 2024, a difference of RM {difference:,.0f}. "
                    f"{ranking_note}"
                )

            with st.expander(":material/table_view: View income data"):
                st.dataframe(
                    income_view[
                        ["state", "district", "year_label", "income_mean"]
                    ].sort_values(["state", "district", "year_label"]),
                    use_container_width=True,
                    hide_index=True
                )

# ============================================================
# PAGE 3: VISUALIZATION 2 - POVERTY AND INCOME
# ============================================================
elif page == "Poverty Analysis":

    st.markdown(
        '<div class="section-heading"><span class="material-symbols-rounded">trending_down</span> Visualization 2 – Poverty and Income</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="objective-card">
            <h4><span class="material-symbols-rounded">track_changes</span> Objective 2</h4>
            <p>To examine the relationship between absolute poverty
            and mean household income across districts in Malaysia.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df_graph2.empty:
        st.warning("No matched income and poverty records are available.")
    else:
        available_years = sorted(
            df_graph2["year"].unique(),
            reverse=True
        )
        selected_year = st.selectbox(
            ":material/calendar_month: Select Year",
            available_years,
            format_func=lambda year: str(year)
        )

        scatter_view = df_graph2[
            df_graph2["year"] == selected_year
        ].copy()

        # State filter
        states = sorted(scatter_view["state"].dropna().unique())
        selected_state = st.selectbox(
            ":material/map: Filter by State",
            ["All States"] + states,
            key="poverty_state"
        )

        if selected_state != "All States":
            scatter_view = scatter_view[
                scatter_view["state"] == selected_state
            ].copy()

        if len(scatter_view) < 2:
            st.warning("At least two districts are needed to show the trendline.")
        else:
            correlation = scatter_view[
                ["poverty_absolute", "income_mean"]
            ].corr().iloc[0, 1]

            high_poverty = scatter_view.loc[
                scatter_view["poverty_absolute"].idxmax()
            ]
            low_poverty = scatter_view.loc[
                scatter_view["poverty_absolute"].idxmin()
            ]

            s1, s2, s3 = st.columns(3)
            with s1:
                summary_card(":material/location_on: Districts Analysed", str(len(scatter_view)),
                             f"Year {selected_year}", BLUE)
            with s2:
                summary_card(":material/trending_up: Pearson Correlation",
                             f"{correlation:.3f}" if pd.notna(correlation) else "N/A",
                             "Income and absolute poverty", TEAL)
            with s3:
                summary_card(":material/warning: Highest Poverty",
                             f"{high_poverty['poverty_absolute']:.2f}%",
                             f"{high_poverty['district']}, {high_poverty['state']}",
                             ORANGE)

            st.markdown("### :material/search: Absolute Poverty vs Mean Household Income")
            st.caption(
                "Each point represents a district. The trendline shows "
                "the overall linear pattern for the selected year."
            )

            fig2 = px.scatter(
                scatter_view,
                x="poverty_absolute",
                y="income_mean",
                color="year",
                trendline="ols",
                trendline_scope="trace",
                hover_name="district_label",
                hover_data={
                    "state": True,
                    "district": True,
                    "poverty_absolute": ":.2f",
                    "income_mean": ":,.0f"
                },
                color_discrete_map={
                    "2022": BLUE,
                    "2024": TEAL
                },
                labels={
                    "poverty_absolute": "Absolute Poverty Rate (%)",
                    "income_mean": "Mean Household Income (RM)",
                    "year": "Year"
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

            fig2.update_layout(
                **plotly_layout,
                height=680,
                title=dict(
                    text=f"<b>Relationship Between Absolute Poverty and Mean Household Income ({selected_year})</b>",
                    x=0.5,
                    xanchor="center",
                    font=dict(size=18, color=NAVY)
                ),
                showlegend=False,
                margin=dict(l=100, r=55, t=95, b=85)
            )
            style_axes(
                fig2,
                "Absolute Poverty Rate (%)",
                "Mean Household Income (RM)",
                x_format=",.1f",
                y_format=",.0f"
            )

            st.plotly_chart(fig2, use_container_width=True)

            st.markdown("### :material/description: Interpretation and Discussion")
            if pd.isna(correlation):
                corr_text = "The correlation could not be calculated."
            elif correlation < 0:
                corr_text = (
                    f"The Pearson correlation is {correlation:.3f}, "
                    "showing a negative linear relationship. Districts "
                    "with higher absolute poverty rates tend to have "
                    "lower mean household income in this dataset."
                )
            elif correlation > 0:
                corr_text = (
                    f"The Pearson correlation is {correlation:.3f}, "
                    "showing a positive linear relationship. Districts "
                    "with higher absolute poverty rates also tend to have "
                    "higher mean household income in this dataset."
                )
            else:
                corr_text = (
                    "The Pearson correlation is 0, indicating no linear "
                    "relationship in this selected data."
                )

            st.write(
                corr_text
                + " Correlation describes association and does not establish causation."
            )

            with st.expander(":material/table_view: View poverty and income data"):
                st.dataframe(
                    scatter_view[
                        ["state", "district", "year",
                         "income_mean", "poverty_absolute"]
                    ].sort_values(["state", "district"]),
                    use_container_width=True,
                    hide_index=True
                )

# ============================================================
# PAGE 4: VISUALIZATION 3 - POPULATION
# ============================================================
elif page == "Population Analysis":

    st.markdown(
        '<div class="section-heading"><span class="material-symbols-rounded">groups</span> Visualization 3 – Population</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="objective-card">
            <h4><span class="material-symbols-rounded">track_changes</span> Objective 3</h4>
            <p>To analyze population trends across districts
            in Malaysia from 2020 to 2024.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df_graph3.empty:
        st.warning("No population records are available for 2020–2024.")
    else:
        states = sorted(df_graph3["state"].dropna().unique())
        selected_state = st.selectbox(
            ":material/map: Filter by State",
            ["All States"] + states
        )

        if selected_state == "All States":
            population_view = df_graph3.copy()
        else:
            population_view = df_graph3[
                df_graph3["state"] == selected_state
            ].copy()

        years = sorted(population_view["year"].unique())
        first_year, last_year = years[0], years[-1]

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
            summary_card(":material/location_on: Districts Analysed", str(total_districts),
                         "Selected geographic coverage", BLUE)
        with s2:
            if not highest.empty:
                row = highest.iloc[0]
                summary_card(":material/emoji_events: Highest Population",
                             f"{row['population']:,.0f}",
                             f"{row['district']}, {row['state']} ({last_year})",
                             TEAL)
        with s3:
            if not lowest.empty:
                row = lowest.iloc[0]
                summary_card(":material/push_pin: Lowest Population",
                             f"{row['population']:,.0f}",
                             f"{row['district']}, {row['state']} ({last_year})",
                             ORANGE)

        st.markdown("### :material/trending_up: Population Trends by District")
        st.caption(
            "Each line represents a district. Line colours represent states. "
            "Use the state filter above to reduce the number of lines."
        )

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

        fig3.update_layout(
            **plotly_layout,
            height=780,
            title=dict(
                text="<b>Population Trends by District in Malaysia (2020–2024)</b>",
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

        st.markdown("### :material/description: Interpretation and Discussion")

        annual_summary = (
            population_view.groupby("year")["population"]
            .mean()
            .reset_index(name="average_population")
        )

        if len(annual_summary) >= 2:
            start_avg = annual_summary.iloc[0]["average_population"]
            end_avg = annual_summary.iloc[-1]["average_population"]
            avg_change = end_avg - start_avg

            if avg_change > 0:
                trend = "increased"
            elif avg_change < 0:
                trend = "decreased"
            else:
                trend = "remained unchanged"

            st.write(
                f"The line chart shows how population changed across "
                f"districts from {first_year} to {last_year}. The average "
                f"district population {trend} from {start_avg:,.0f} to "
                f"{end_avg:,.0f}, a difference of {avg_change:+,.0f}. "
                "The individual lines help identify districts with "
                "increasing, decreasing or relatively stable population patterns."
            )

        with st.expander(":material/table_view: View population summary by year"):
            st.dataframe(
                annual_summary,
                use_container_width=True,
                hide_index=True
            )

        with st.expander(":material/table_view: View population data by district"):
            st.dataframe(
                population_view.sort_values(
                    ["state", "district", "year"]
                ),
                use_container_width=True,
                hide_index=True
            )

# ------------------------------------------------------------
# 11. FOOTER
# ------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        <b style="color:#123B63;">MALAYSIA DATA INSIGHTS</b><br>
        JIE42403 · Scientific Visualization<br>
        Household Income, Poverty and Population Analysis · Malaysia
    </div>
    """,
    unsafe_allow_html=True
)
