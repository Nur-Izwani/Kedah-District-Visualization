
# ============================================================
# KEDAH DATA INSIGHTS
# JIE42403 - SCIENTIFIC VISUALIZATION
# Household Income and Population Analysis
# Study Area: Kedah, Malaysia
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from textwrap import dedent

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Kedah Data Insights",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. PROFESSIONAL CSS DESIGN
# ============================================================

st.markdown(dedent("""
<style>

.stApp {
    background-color: #F3F6FC;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg, #123B63 0%, #087E8B 100%
    );
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-header {
    background: linear-gradient(
        110deg, #123B63, #087E8B, #19A7A1
    );
    padding: 32px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.main-header h1 {
    color: white;
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 8px;
}

.main-header p {
    color: #E5F6FF;
    font-size: 15px;
    margin-bottom: 4px;
}

.section-title {
    color: #123B63;
    font-size: 25px;
    font-weight: 750;
    margin-top: 15px;
    margin-bottom: 12px;
}

.objective-card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border-left: 5px solid #13A8A8;
    box-shadow: 0 3px 12px rgba(20,50,80,0.05);
    margin-bottom: 20px;
}

.objective-label {
    color: #087E8B;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.objective-text {
    color: #26374A;
    font-size: 15px;
    line-height: 1.7;
}

.summary-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #DCE6F2;
    box-shadow: 0 3px 12px rgba(20,50,80,0.06);
    min-height: 125px;
    height: 100%;
}

.summary-label {
    color: #64748B;
    font-size: 13px;
    font-weight: 650;
}

.summary-value {
    color: #123B63;
    font-size: 24px;
    font-weight: 800;
    margin-top: 12px;
    overflow-wrap: anywhere;
}

.summary-detail {
    color: #64748B;
    font-size: 12px;
    margin-top: 6px;
}

.insight-card {
    background: #E8F4FF;
    border-left: 4px solid #1565C0;
    padding: 17px;
    border-radius: 10px;
    color: #123B63;
    line-height: 1.7;
    margin-top: 15px;
    margin-bottom: 15px;
}

div[data-testid="stPlotlyChart"] {
    background: white;
    border-radius: 14px;
    padding: 12px;
    border: 1px solid #E2E8F0;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #DCE6F2;
    padding: 15px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    font-weight: 600;
}

</style>
"""), unsafe_allow_html=True)


# ============================================================
# 3. LOAD DATASETS
# ============================================================

@st.cache_data
def load_data():

    income = pd.read_csv(
        "kedah_merged_2024.csv"
    )

    population = pd.read_csv(
        "kedah_population_2020_2024.csv"
    )

    return income, population


try:

    df_income, df_population = load_data()

except Exception as error:

    st.error(f"Dataset loading error: {error}")

    st.info(
        "Please ensure both CSV files are uploaded "
        "to the same GitHub repository as app.py."
    )

    st.stop()


# ============================================================
# 4. DATA CLEANING
# ============================================================

df_income.columns = df_income.columns.str.strip()
df_population.columns = df_population.columns.str.strip()

# Check required columns

required_income = [
    "state", "district", "income_mean"
]

required_population = [
    "state", "district", "population"
]

missing_income = [
    col for col in required_income
    if col not in df_income.columns
]

missing_population = [
    col for col in required_population
    if col not in df_population.columns
]

if missing_income or missing_population:

    st.error(
        f"Missing income columns: {missing_income}. "
        f"Missing population columns: {missing_population}."
    )

    st.stop()


# Convert numerical columns

df_income["income_mean"] = pd.to_numeric(
    df_income["income_mean"],
    errors="coerce"
)

df_population["population"] = pd.to_numeric(
    df_population["population"],
    errors="coerce"
)


# Create year column

def prepare_year(data):

    data = data.copy()

    if "date" in data.columns:

        data["date"] = pd.to_datetime(
            data["date"],
            errors="coerce"
        )

        data["year"] = data["date"].dt.year

    elif "year" in data.columns:

        data["year"] = pd.to_numeric(
            data["year"],
            errors="coerce"
        )

    else:

        raise ValueError(
            "Dataset must contain a date or year column."
        )

    return data


try:

    df_income = prepare_year(df_income)
    df_population = prepare_year(df_population)

except ValueError as error:

    st.error(str(error))
    st.stop()


# Filter Kedah

df_income = df_income[
    df_income["state"].astype(str).str.strip().str.lower()
    == "kedah"
].copy()

df_population = df_population[
    df_population["state"].astype(str).str.strip().str.lower()
    == "kedah"
].copy()


# ============================================================
# 5. FILTER OVERALL DEMOGRAPHIC
# ============================================================

def filter_overall(data):

    data = data.copy()

    filters = {
        "sex": "both",
        "age": "overall",
        "ethnicity": "overall"
    }

    for column, value in filters.items():

        if column in data.columns:

            values = (
                data[column]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            if value in values.unique():

                data = data[
                    values == value
                ].copy()

    return data


df_income = filter_overall(df_income)
df_population = filter_overall(df_population)


# Filter years

df_income = df_income[
    df_income["year"] == 2024
].copy()

df_population = df_population[
    df_population["year"].between(2020, 2024)
].copy()


# ============================================================
# 6. GRAPH 1 DATA
# ============================================================

df_income_graph = df_income.dropna(
    subset=["district", "income_mean"]
).copy()

df_income_graph = (
    df_income_graph.groupby(
        "district",
        as_index=False
    )["income_mean"].mean()
)

df_income_graph = df_income_graph.sort_values(
    "income_mean",
    ascending=True
)


# ============================================================
# 7. GRAPH 2 DATA - MERGE
# ============================================================

df_income_2024 = df_income[
    ["state", "district", "income_mean"]
].copy()

df_population_2024 = df_population[
    df_population["year"] == 2024
][
    ["state", "district", "population"]
].copy()


# Group district records

df_income_2024 = (
    df_income_2024.groupby(
        ["state", "district"],
        as_index=False
    )["income_mean"].mean()
)

df_population_2024 = (
    df_population_2024.groupby(
        ["state", "district"],
        as_index=False
    )["population"].mean()
)


# Merge by state and district

df_scatter = pd.merge(
    df_population_2024,
    df_income_2024,
    on=["state", "district"],
    how="inner"
)

df_scatter["district_label"] = (
    df_scatter["district"].astype(str)
    + " ("
    + df_scatter["state"].astype(str)
    + ")"
)

df_scatter = df_scatter.dropna(
    subset=["population", "income_mean"]
)


# ============================================================
# 8. GRAPH 3 DATA
# ============================================================

df_population_graph = df_population.dropna(
    subset=["district", "population", "year"]
).copy()

df_population_graph = (
    df_population_graph.groupby(
        ["district", "year"],
        as_index=False
    )["population"].mean()
)

df_population_graph = df_population_graph.sort_values(
    ["district", "year"]
)


# ============================================================
# 9. COLOUR PALETTE
# ============================================================

district_colors = px.colors.qualitative.Bold

chart_theme = {
    "template": "plotly_white",
    "paper_bgcolor": "white",
    "plot_bgcolor": "white",
    "font": {
        "family": "Arial",
        "size": 12,
        "color": "#26374A"
    }
}


# ============================================================
# 10. HTML COMPONENT FUNCTIONS
# ============================================================

def summary_card(label, value, detail, color):

    html = dedent(f"""
    <div class="summary-card"
         style="border-top: 5px solid {color};">

        <div class="summary-label">{label}</div>

        <div class="summary-value">{value}</div>

        <div class="summary-detail">{detail}</div>

    </div>
    """).strip()

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def objective_card(objective):

    html = dedent(f"""
    <div class="objective-card">

        <div class="objective-label">
            OBJECTIVE STATEMENT
        </div>

        <div class="objective-text">
            {objective}
        </div>

    </div>
    """).strip()

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def insight_card(text):

    html = dedent(f"""
    <div class="insight-card">
        {text}
    </div>
    """).strip()

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# 11. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown(
    "# KEDAH DATA INSIGHTS"
)

st.sidebar.caption(
    "Scientific Visualization Dashboard"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        ":material/dashboard: Dashboard Overview",
        ":material/account_balance_wallet: Objective 1 - Income",
        ":material/scatter_plot: Objective 2 - Scatter Plot",
        ":material/show_chart: Objective 3 - Population"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("""
### STUDY INFORMATION

**Study Area:** Kedah, Malaysia

**Income Data:** 2024

**Population Data:** 2020–2024

**Analysis:** District Level
""")

st.sidebar.caption(
    "JIE42403 | Scientific Visualization"
)


# ============================================================
# 12. MAIN HEADER
# ============================================================

st.markdown(dedent("""
<div class="main-header">

    <h1>KEDAH DATA INSIGHTS</h1>

    <p>
        Household Income, Population and District Analysis
    </p>

    <p>
        SCIENTIFIC VISUALIZATION | KEDAH, MALAYSIA
    </p>

</div>
"""), unsafe_allow_html=True)


# ============================================================
# PAGE 1 - DASHBOARD OVERVIEW
# ============================================================

if "Dashboard Overview" in page:

    st.markdown(
        ":material/dashboard: ## Dashboard Overview"
    )

    st.write(
        "Explore household income and population patterns "
        "across districts in Kedah, Malaysia."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Study Area",
        "Kedah"
    )

    col2.metric(
        "Income Reference",
        "2024"
    )

    col3.metric(
        "Population Period",
        "2020–2024"
    )

    st.divider()

    st.subheader(
        ":material/target: Research Objectives"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(dedent("""
        <div class="objective-card">

            <h3 style="color:#1565C0;">
                Household Income
            </h3>

            <p>
                Examine differences in mean household
                income across districts in Kedah in 2024.
            </p>

            <b>Horizontal Bar Chart</b>

        </div>
        """), unsafe_allow_html=True)

    with c2:

        st.markdown(dedent("""
        <div class="objective-card">

            <h3 style="color:#E53935;">
                Population and Income
            </h3>

            <p>
                Examine the relationship between district
                population and mean household income in 2024.
            </p>

            <b>Scatter Plot</b>

        </div>
        """), unsafe_allow_html=True)

    with c3:

        st.markdown(dedent("""
        <div class="objective-card">

            <h3 style="color:#00897B;">
                Population Trends
            </h3>

            <p>
                Analyze population trends across districts
                in Kedah from 2020 to 2024.
            </p>

            <b>Line Chart</b>

        </div>
        """), unsafe_allow_html=True)

    st.divider()

    st.subheader(
        ":material/database: Dataset Preview"
    )

    tab1, tab2 = st.tabs([
        "Income Dataset",
        "Population Dataset"
    ])

    with tab1:

        st.dataframe(
            df_income.head(10),
            use_container_width=True,
            hide_index=True
        )

    with tab2:

        st.dataframe(
            df_population.head(10),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PAGE 2 - OBJECTIVE 1: INCOME
# ============================================================

elif "Objective 1" in page:

    st.markdown(
        ":material/account_balance_wallet: ## OBJECTIVE 1: HOUSEHOLD INCOME"
    )

    objective_card(
        "To examine the differences in mean household "
        "income across districts in Kedah in 2024."
    )

    if not df_income_graph.empty:

        highest = df_income_graph.iloc[-1]
        lowest = df_income_graph.iloc[0]

        average = df_income_graph["income_mean"].mean()

        income_gap = (
            highest["income_mean"]
            - lowest["income_mean"]
        )

        # SUMMARY BOX

        st.subheader(
            ":material/insights: Summary Box"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            summary_card(
                "Highest Income",
                f"RM {highest['income_mean']:,.0f}",
                highest["district"],
                "#1565C0"
            )

        with col2:
            summary_card(
                "Lowest Income",
                f"RM {lowest['income_mean']:,.0f}",
                lowest["district"],
                "#E53935"
            )

        with col3:
            summary_card(
                "Average Income",
                f"RM {average:,.0f}",
                "Across districts",
                "#00897B"
            )

        with col4:
            summary_card(
                "Income Gap",
                f"RM {income_gap:,.0f}",
                "Highest minus lowest",
                "#F57C00"
            )

        st.divider()

        # ORIGINAL GRAPH 1

        st.subheader(
            ":material/bar_chart: Visualization 1"
        )

        fig1 = px.bar(
            df_income_graph,
            x="income_mean",
            y="district",
            orientation="h",
            text="income_mean",
            color="district",
            color_discrete_sequence=district_colors,
            labels={
                "income_mean": "Mean Household Income (RM)",
                "district": "District"
            }
        )

        fig1.update_traces(
            texttemplate="RM %{text:,.0f}",
            textposition="outside",
            textfont=dict(
                size=11,
                color="black"
            ),
            marker_line_color="white",
            marker_line_width=1.2,
            cliponaxis=False
        )

        fig1.update_layout(
            **chart_theme,
            title=dict(
                text="<b>Mean Household Income by District in Kedah (2024)</b>",
                x=0.5,
                font=dict(size=19, color="#123B63")
            ),
            showlegend=False,
            height=max(480, len(df_income_graph) * 48),
            margin=dict(
                l=100, r=120, t=90, b=70
            ),
            xaxis=dict(
                title="Mean Household Income (RM)",
                tickformat=",.0f",
                gridcolor="#E1E8F0"
            ),
            yaxis=dict(
                title="District",
                tickfont=dict(size=12)
            )
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        # INTERPRETATION

        st.subheader(
            ":material/analytics: Interpretation and Discussion"
        )

        st.markdown(f"""
        The horizontal bar chart shows differences in mean
        household income across districts in Kedah in 2024.
        {highest['district']} recorded the highest mean
        household income at RM {highest['income_mean']:,.2f},
        while {lowest['district']} recorded the lowest at
        RM {lowest['income_mean']:,.2f}.

        The income gap of RM {income_gap:,.2f} indicates
        variation in household income between the highest
        and lowest districts. These differences may reflect
        variations in employment opportunities, economic
        activities and local development. However, mean
        household income alone cannot explain all aspects
        of household economic well-being.
        """)

        with st.expander("View Detailed Income Data"):

            st.dataframe(
                df_income_graph.sort_values(
                    "income_mean",
                    ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )

    else:

        st.warning("No valid income records found.")


# ============================================================
# PAGE 3 - OBJECTIVE 2: SCATTER PLOT
# ============================================================

elif "Objective 2" in page:

    st.markdown(
        ":material/scatter_plot: ## OBJECTIVE 2: POPULATION VS INCOME"
    )

    objective_card(
        "To examine the relationship between district "
        "population and mean household income in Kedah in 2024."
    )

    if len(df_scatter) >= 2:

        correlation = df_scatter[
            ["population", "income_mean"]
        ].corr().iloc[0, 1]

        highest_population = df_scatter.loc[
            df_scatter["population"].idxmax()
        ]

        highest_income = df_scatter.loc[
            df_scatter["income_mean"].idxmax()
        ]

        if abs(correlation) < 0.3:
            strength = "Weak"
        elif abs(correlation) < 0.7:
            strength = "Moderate"
        else:
            strength = "Strong"

        if correlation > 0:
            direction = "Positive"
        elif correlation < 0:
            direction = "Negative"
        else:
            direction = "No linear relationship"

        # SUMMARY BOX

        st.subheader(
            ":material/insights: Summary Box"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            summary_card(
                "Pearson Correlation",
                f"{correlation:.3f}",
                f"{strength} relationship",
                "#1565C0"
            )

        with col2:
            summary_card(
                "Districts Analyzed",
                str(len(df_scatter)),
                "Matched observations",
                "#00897B"
            )

        with col3:
            summary_card(
                "Highest Population",
                f"{highest_population['population']:,.0f}",
                highest_population["district"],
                "#E53935"
            )

        with col4:
            summary_card(
                "Highest Income",
                f"RM {highest_income['income_mean']:,.0f}",
                highest_income["district"],
                "#F57C00"
            )

        insight_card(
            f"The Pearson correlation coefficient is "
            f"{correlation:.3f}, indicating a "
            f"{strength.lower()} {direction.lower()} "
            f"linear relationship."
        )

        st.divider()

        # ORIGINAL GRAPH 2

        st.subheader(
            ":material/scatter_plot: Visualization 2"
        )

        fig2 = px.scatter(
            df_scatter,
            x="population",
            y="income_mean",
            color="district_label",
            hover_name="district",
            hover_data={
                "state": True,
                "population": ":,.1f",
                "income_mean": ":,.0f",
                "district_label": False
            },
            color_discrete_sequence=district_colors,
            labels={
                "population": "Population (Thousands)",
                "income_mean": "Mean Household Income (RM)",
                "district_label": "District"
            }
        )

        fig2.update_traces(
            marker=dict(
                size=12,
                opacity=0.9,
                line=dict(
                    width=1.2,
                    color="black"
                )
            )
        )

        fig2.update_layout(
            **chart_theme,
            title=dict(
                text="<b>District Population vs Mean Household Income in Kedah (2024)</b>",
                x=0.5,
                font=dict(size=18, color="#123B63")
            ),
            height=620,
            margin=dict(
                l=80, r=190, t=90, b=75
            ),
            xaxis=dict(
                title="Population (Thousands)",
                tickformat=",.0f",
                gridcolor="#D9E2F0"
            ),
            yaxis=dict(
                title="Mean Household Income (RM)",
                tickformat=",.0f",
                gridcolor="#D9E2F0"
            ),
            legend=dict(
                title="District",
                orientation="v",
                x=1.02,
                y=1,
                bgcolor="white",
                bordercolor="#DCE6F2",
                borderwidth=1,
                font=dict(size=10)
            ),
            hovermode="closest"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # INTERPRETATION

        st.subheader(
            ":material/analytics: Interpretation and Discussion"
        )

        st.markdown(f"""
        The scatter plot illustrates the relationship between
        district population and mean household income in
        Kedah in 2024. Each point represents one district.
        The Pearson correlation coefficient is
        {correlation:.3f}, indicating a {strength.lower()}
        {direction.lower()} linear relationship.

        A positive relationship means that both variables
        tend to increase together, whereas a negative
        relationship indicates an opposite pattern.
        The distribution of individual points also helps
        identify districts that differ from the general
        pattern. However, correlation does not establish
        causation, and other socioeconomic factors may
        influence household income.
        """)

        with st.expander("View Detailed Scatter Data"):

            st.dataframe(
                df_scatter,
                use_container_width=True,
                hide_index=True
            )

    else:

        st.warning(
            "Not enough matched district records "
            "to calculate the relationship."
        )


# ============================================================
# PAGE 4 - OBJECTIVE 3: POPULATION TRENDS
# ============================================================

elif "Objective 3" in page:

    st.markdown(
        ":material/show_chart: ## OBJECTIVE 3: POPULATION TRENDS"
    )

    objective_card(
        "To analyze population trends across districts "
        "in Kedah from 2020 to 2024."
    )

    if not df_population_graph.empty:

        first_year = int(
            df_population_graph["year"].min()
        )

        last_year = int(
            df_population_graph["year"].max()
        )

        first_total = df_population_graph[
            df_population_graph["year"] == first_year
        ]["population"].sum()

        last_total = df_population_graph[
            df_population_graph["year"] == last_year
        ]["population"].sum()

        population_change = (
            last_total - first_total
        )

        percentage_change = (
            population_change / first_total * 100
            if first_total != 0 else 0
        )

        latest_data = df_population_graph[
            df_population_graph["year"] == last_year
        ]

        highest_latest = latest_data.loc[
            latest_data["population"].idxmax()
        ]

        # SUMMARY BOX

        st.subheader(
            ":material/insights: Summary Box"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            summary_card(
                f"Population {first_year}",
                f"{first_total:,.0f}",
                "Combined district values",
                "#1565C0"
            )

        with col2:
            summary_card(
                f"Population {last_year}",
                f"{last_total:,.0f}",
                "Combined district values",
                "#00897B"
            )

        with col3:
            summary_card(
                "Population Change",
                f"{population_change:+,.0f}",
                "Change across study period",
                "#E53935"
            )

        with col4:
            summary_card(
                "Percentage Change",
                f"{percentage_change:+.2f}%",
                "2020 to 2024",
                "#F57C00"
            )

        insight_card(
            f"District with the highest population in "
            f"{last_year}: {highest_latest['district']} "
            f"({highest_latest['population']:,.0f})."
        )

        st.divider()

        # ORIGINAL GRAPH 3

        st.subheader(
            ":material/show_chart: Visualization 3"
        )

        fig3 = px.line(
            df_population_graph,
            x="year",
            y="population",
            color="district",
            markers=True,
            color_discrete_sequence=district_colors,
            labels={
                "year": "Year",
                "population": "Population (Thousands)",
                "district": "District"
            }
        )

        fig3.update_traces(
            line=dict(width=3),
            marker=dict(
                size=9,
                line=dict(
                    color="white",
                    width=1.5
                )
            )
        )

        fig3.update_layout(
            **chart_theme,
            title=dict(
                text="<b>Population Trends by District in Kedah (2020–2024)</b>",
                x=0.5,
                font=dict(size=19, color="#123B63")
            ),
            height=650,
            margin=dict(
                l=85, r=120, t=90, b=75
            ),
            xaxis=dict(
                title="Year",
                tickmode="linear",
                dtick=1,
                gridcolor="#D9E2F0"
            ),
            yaxis=dict(
                title="Population (Thousands)",
                tickformat=",.0f",
                gridcolor="#D9E2F0"
            ),
            legend=dict(
                title="District",
                bgcolor="white",
                bordercolor="#DCE6F2",
                borderwidth=1
            ),
            hovermode="x unified"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # INTERPRETATION

        st.subheader(
            ":material/analytics: Interpretation and Discussion"
        )

        if population_change > 0:
            trend_word = "increased"
        elif population_change < 0:
            trend_word = "decreased"
        else:
            trend_word = "remained unchanged"

        st.markdown(f"""
        The line chart presents population trends across
        districts in Kedah from {first_year} to {last_year}.
        Each coloured line represents a district, while
        the markers indicate population values for
        individual years.

        The combined population values across the included
        districts {trend_word} by
        {abs(population_change):,.0f}, equivalent to
        {percentage_change:+.2f}% between the first and
        latest year. Differences in line direction and
        slope reveal variations in population changes
        between districts. These patterns are useful for
        understanding population distribution and may
        support planning for public facilities and
        infrastructure.
        """)

        with st.expander("View Detailed Population Data"):

            st.dataframe(
                df_population_graph,
                use_container_width=True,
                hide_index=True
            )

    else:

        st.warning(
            "No population records found."
        )


# ============================================================
# 13. FOOTER
# ============================================================

st.divider()

st.markdown(dedent("""
<div style="
    text-align:center;
    padding:22px;
    color:#64748B;
">

    <h4 style="color:#123B63;">
        KEDAH DATA INSIGHTS
    </h4>

    Scientific Visualization Project

    <br>

    Household Income and Population Analysis

    <br>

    2020–2024 | Kedah, Malaysia

</div>
"""), unsafe_allow_html=True)
