
# ============================================================
# KEDAH DATA INSIGHTS
# SCIENTIFIC VISUALIZATION DASHBOARD
# Study Area: Kedah, Malaysia
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Kedah Data Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #F3F7FC;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg, #123B63, #087E8B
    );
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-header {
    background: linear-gradient(
        110deg, #123B63, #087E8B, #19A7A1
    );
    padding: 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.main-header h1 {
    color: white;
    font-size: 34px;
    font-weight: 800;
}

.main-header p {
    color: #E5F6FF;
    font-size: 15px;
}

.section-header {
    color: #123B63;
    font-size: 25px;
    font-weight: 750;
    margin-top: 15px;
}

.info-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border-left: 5px solid #13A8A8;
    margin-bottom: 15px;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #DCE6F2;
    padding: 17px;
    border-radius: 13px;
}

div[data-testid="stPlotlyChart"] {
    background: white;
    padding: 12px;
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)


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

except Exception as e:

    st.error(f"Dataset loading error: {e}")
    st.stop()


# ============================================================
# 4. DATA CLEANING
# ============================================================

df_income.columns = df_income.columns.str.strip()
df_population.columns = df_population.columns.str.strip()

df_income["date"] = pd.to_datetime(
    df_income["date"], errors="coerce"
)

df_population["date"] = pd.to_datetime(
    df_population["date"], errors="coerce"
)

# Filter Kedah
df_income = df_income[
    df_income["state"].astype(str).str.strip().str.lower()
    == "kedah"
].copy()

df_population = df_population[
    df_population["state"].astype(str).str.strip().str.lower()
    == "kedah"
].copy()

# Filter overall population demographics
def filter_overall(data):

    for col, value in {
        "sex": "both",
        "age": "overall",
        "ethnicity": "overall"
    }.items():

        if col in data.columns:

            data = data[
                data[col].astype(str).str.lower() == value
            ].copy()

    return data


df_income = filter_overall(df_income)
df_population = filter_overall(df_population)

# Convert numeric columns
for col in [
    "income_mean",
    "income_median",
    "poverty_absolute",
    "poverty_relative",
    "population"
]:

    if col in df_income.columns:

        df_income[col] = pd.to_numeric(
            df_income[col], errors="coerce"
        )

df_population["population"] = pd.to_numeric(
    df_population["population"], errors="coerce"
)

# Filter years
df_income = df_income[
    df_income["date"].dt.year == 2024
].copy()

df_population["year"] = (
    df_population["date"].dt.year
)

df_population = df_population[
    df_population["year"].between(2020, 2024)
].copy()


# ============================================================
# 5. GRAPH 1 DATA PREPARATION
# ============================================================

df_income_graph = df_income.dropna(
    subset=["district", "income_mean"]
).copy()

df_income_graph = (
    df_income_graph.groupby(
        "district", as_index=False
    )["income_mean"].mean()
)

df_income_graph = df_income_graph.sort_values(
    "income_mean", ascending=True
)


# ============================================================
# 6. GRAPH 2 DATA PREPARATION
# ============================================================

# Population data 2024
df_pop_2024 = df_population[
    df_population["year"] == 2024
].copy()

# Income data
df_income_2024 = df_income[
    ["state", "district", "date", "income_mean"]
].copy()

# Population data
df_pop_scatter = df_pop_2024[
    ["state", "district", "date", "population"]
].copy()

# Convert numerical values
df_income_2024["income_mean"] = pd.to_numeric(
    df_income_2024["income_mean"],
    errors="coerce"
)

df_pop_scatter["population"] = pd.to_numeric(
    df_pop_scatter["population"],
    errors="coerce"
)

# Remove missing values
df_income_2024 = df_income_2024.dropna(
    subset=["district", "income_mean"]
)

df_pop_scatter = df_pop_scatter.dropna(
    subset=["district", "population"]
)

# Group duplicate records
df_income_2024 = df_income_2024.groupby(
    ["state", "district", "date"],
    as_index=False
)["income_mean"].mean()

df_pop_scatter = df_pop_scatter.groupby(
    ["state", "district", "date"],
    as_index=False
)["population"].mean()

# Merge datasets
df_scatter = pd.merge(
    df_pop_scatter,
    df_income_2024,
    on=["state", "district", "date"],
    how="inner",
    validate="one_to_one"
)

# District label
df_scatter["district_label"] = (
    df_scatter["district"].astype(str)
    + " ("
    + df_scatter["state"].astype(str)
    + ")"
)

df_scatter = df_scatter.sort_values(
    "district_label"
)


# ============================================================
# 7. GRAPH 3 DATA PREPARATION
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
# 8. COLOR PALETTE
# ============================================================

district_colors = [
    "#1565C0",
    "#E53935",
    "#00897B",
    "#8E24AA",
    "#F57C00",
    "#2E7D32",
    "#EC407A",
    "#5C6BC0",
    "#795548",
    "#00ACC1",
    "#9E9D24",
    "#6D4C41",
    "#3949AB",
    "#D81B60",
    "#7CB342"
]

chart_theme = dict(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        family="Arial",
        size=12,
        color="#26374A"
    )
)


# ============================================================
# 9. SIDEBAR
# ============================================================

st.sidebar.markdown("# 📊 KEDAH DATA INSIGHTS")

st.sidebar.caption(
    "Scientific Visualization Dashboard"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "SELECT PAGE",
    [
        "🏠 Home",
        "📊 Objective 1 - Income",
        "🔵 Objective 2 - Scatter Plot",
        "📈 Objective 3 - Population"
    ]
)

st.sidebar.divider()

st.sidebar.markdown(
    """
    **STUDY INFORMATION**

    📍 Kedah, Malaysia

    💰 Income: 2024

    👥 Population: 2020–2024

    📚 District-level analysis
    """
)

st.sidebar.caption(
    "Scientific Visualization Project"
)


# ============================================================
# 10. MAIN HEADER
# ============================================================

st.markdown("""
<div class="main-header">

<h1>📊 KEDAH DATA INSIGHTS</h1>

<p>
Household Income, Population and District Analysis
</p>

<p>
SCIENTIFIC VISUALIZATION | KEDAH, MALAYSIA
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# PAGE 1: HOME
# ============================================================

if page == "🏠 Home":

    st.markdown(
        '<div class="section-header">Dashboard Overview</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore household income and population patterns "
        "across districts in Kedah, Malaysia."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "📍 Districts",
        df_income_graph["district"].nunique()
    )

    c2.metric(
        "💰 Income Year",
        "2024"
    )

    c3.metric(
        "👥 Study Period",
        "2020–2024"
    )

    st.divider()

    st.subheader("🎯 Research Objectives")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="info-card">
        <h3 style="color:#1565C0;">01 💰 Income</h3>
        <p>Analyze differences in mean household income
        across districts in Kedah in 2024.</p>
        <b>Horizontal Bar Chart</b>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="info-card">
        <h3 style="color:#E53935;">02 🔵 Relationship</h3>
        <p>Examine the relationship between district
        population and mean household income in 2024.</p>
        <b>Scatter Plot</b>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="info-card">
        <h3 style="color:#00897B;">03 📈 Population</h3>
        <p>Analyze population trends across districts
        from 2020 to 2024.</p>
        <b>Line Chart</b>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("📂 Dataset Preview")

    tab1, tab2 = st.tabs([
        "Income Dataset",
        "Population Dataset"
    ])

    with tab1:

        st.dataframe(
            df_income.head(10),
            use_container_width=True
        )

    with tab2:

        st.dataframe(
            df_population.head(10),
            use_container_width=True
        )


# ============================================================
# PAGE 2: GRAPH 1 - HORIZONTAL BAR CHART
# ============================================================

elif page == "📊 Objective 1 - Income":

    st.markdown(
        '<div class="section-header">'
        '💰 OBJECTIVE 1: HOUSEHOLD INCOME'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Mean Household Income by District in Kedah (2024)"
    )

    if not df_income_graph.empty:

        highest = df_income_graph.iloc[-1]
        lowest = df_income_graph.iloc[0]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Highest Income",
            f"RM {highest['income_mean']:,.0f}",
            highest["district"]
        )

        col2.metric(
            "Lowest Income",
            f"RM {lowest['income_mean']:,.0f}",
            lowest["district"]
        )

        col3.metric(
            "Income Gap",
            f"RM {highest['income_mean'] - lowest['income_mean']:,.0f}"
        )

        st.divider()

        # ACTUAL GRAPH 1
        fig1 = px.bar(
            df_income_graph,
            x="income_mean",
            y="district",
            orientation="h",
            text="income_mean",
            color="district",
            color_discrete_sequence=district_colors,
            title="Mean Household Income by District in Kedah (2024)",
            labels={
                "income_mean": "Mean Household Income (RM)",
                "district": "District"
            },
            template="plotly_white"
        )

        fig1.update_traces(
            texttemplate="RM %{text:,.0f}",
            textposition="outside",
            textfont=dict(
                size=12,
                color="black"
            ),
            marker=dict(
                line=dict(
                    color="black",
                    width=1
                )
            ),
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
            height=600,
            margin=dict(
                l=100,
                r=120,
                t=100,
                b=80
            ),
            xaxis=dict(
                title="<b>Mean Household Income (RM)</b>",
                tickformat=",.0f",
                showline=True,
                linewidth=2,
                linecolor="black",
                gridcolor="#D9E2F0"
            ),
            yaxis=dict(
                title="<b>District</b>",
                showline=True,
                linewidth=2,
                linecolor="black",
                tickfont=dict(size=12, color="black")
            )
        )

        # DISPLAY GRAPH
        st.plotly_chart(
            fig1,
            use_container_width=True,
            key="graph1"
        )

        st.subheader("🔍 Key Findings")

        st.success(
            f"Highest: {highest['district']} "
            f"(RM {highest['income_mean']:,.2f})"
        )

        st.info(
            f"Lowest: {lowest['district']} "
            f"(RM {lowest['income_mean']:,.2f})"
        )

        st.subheader("📝 Interpretation and Discussion")

        st.markdown("""
        The horizontal bar chart illustrates the differences
        in mean household income across districts in Kedah
        in 2024. The length of each bar represents the
        mean household income recorded in each district.
        The arrangement from the lowest to the highest
        value makes it easier to compare income levels
        across the districts.

        The differences may reflect variations in local
        economic activities, employment opportunities and
        household characteristics. These findings provide
        an overview of income distribution at the district
        level. However, mean income alone does not represent
        the complete economic condition of households.
        """)

        with st.expander("View Detailed Data"):

            st.dataframe(
                df_income_graph.sort_values(
                    "income_mean",
                    ascending=False
                ),
                use_container_width=True
            )

    else:

        st.warning("No income data available.")


# ============================================================
# PAGE 3: GRAPH 2 - SCATTER PLOT
# ============================================================

elif page == "🔵 Objective 2 - Scatter Plot":

    st.markdown(
        '<div class="section-header">'
        '🔵 OBJECTIVE 2: POPULATION VS INCOME'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "District Population vs Mean Household Income in Kedah (2024)"
    )

    if len(df_scatter) >= 2:

        correlation = df_scatter[
            ["population", "income_mean"]
        ].corr().iloc[0, 1]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Districts Analyzed",
            len(df_scatter)
        )

        c2.metric(
            "Pearson Correlation",
            f"{correlation:.3f}"
        )

        direction = (
            "Positive" if correlation > 0
            else "Negative" if correlation < 0
            else "No linear relationship"
        )

        c3.metric(
            "Relationship",
            direction
        )

        st.divider()

        # ACTUAL GRAPH 2
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
            title="District Population vs Mean Household Income in Kedah (2024)",
            labels={
                "population": "Population (Thousands)",
                "income_mean": "Mean Household Income (RM)",
                "district_label": "District"
            },
            template="plotly_white"
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
            height=650,
            width=1100,
            margin=dict(
                l=85,
                r=190,
                t=90,
                b=75
            ),
            xaxis=dict(
                title="<b>Population (Thousands)</b>",
                tickformat=",.0f",
                showline=True,
                linewidth=2,
                linecolor="black",
                mirror=True,
                gridcolor="lightgrey"
            ),
            yaxis=dict(
                title="<b>Mean Household Income (RM)</b>",
                tickformat=",.0f",
                showline=True,
                linewidth=2,
                linecolor="black",
                mirror=True,
                gridcolor="lightgrey"
            ),
            legend=dict(
                title="<b>District</b>",
                orientation="v",
                x=1.02,
                y=1,
                bgcolor="white",
                bordercolor="black",
                borderwidth=1,
                font=dict(size=10)
            ),
            hovermode="closest"
        )

        # DISPLAY GRAPH
        st.plotly_chart(
            fig2,
            use_container_width=True,
            key="graph2"
        )

        st.subheader("🔍 Correlation Analysis")

        if abs(correlation) < 0.3:
            strength = "Weak"
        elif abs(correlation) < 0.7:
            strength = "Moderate"
        else:
            strength = "Strong"

        st.info(
            f"Pearson correlation = {correlation:.3f}. "
            f"This indicates a {strength.lower()} "
            f"{direction.lower()} linear relationship."
        )

        st.subheader("📝 Interpretation and Discussion")

        st.markdown("""
        The scatter plot illustrates the relationship between
        district population and mean household income in
        Kedah in 2024. Each point represents one district.
        The horizontal axis shows population, while the
        vertical axis shows mean household income. The
        distribution of points helps identify patterns
        between the two variables.

        The Pearson correlation coefficient indicates
        the direction and strength of the linear relationship.
        A positive correlation means that both variables
        tend to increase together, while a negative
        correlation indicates an opposite pattern.
        However, correlation does not establish causation.
        """)

        with st.expander("View Detailed Scatter Data"):

            st.dataframe(
                df_scatter,
                use_container_width=True
            )

    else:

        st.warning(
            "Not enough matched district observations "
            "to create the scatter plot."
        )


# ============================================================
# PAGE 4: GRAPH 3 - LINE CHART
# ============================================================

elif page == "📈 Objective 3 - Population":

    st.markdown(
        '<div class="section-header">'
        '📈 OBJECTIVE 3: POPULATION TRENDS'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Population Trends by District in Kedah (2020–2024)"
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

        difference = last_total - first_total

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Starting Year",
            first_year
        )

        c2.metric(
            "Latest Year",
            last_year
        )

        c3.metric(
            "Population Difference",
            f"{difference:,.0f}",
            delta=f"{difference / first_total * 100:.2f}%"
            if first_total else None
        )

        st.divider()

        # ACTUAL GRAPH 3
        fig3 = px.line(
            df_population_graph,
            x="year",
            y="population",
            color="district",
            markers=True,
            color_discrete_sequence=district_colors,
            title="Population Trends by District in Kedah (2020-2024)",
            labels={
                "year": "Year",
                "population": "Population (Thousands)",
                "district": "District"
            },
            template="plotly_white"
        )

        fig3.update_traces(
            line=dict(width=3.5),
            marker=dict(
                size=10,
                line=dict(
                    color="black",
                    width=1.5
                )
            )
        )

        fig3.update_layout(
            **chart_theme,
            title=dict(
                text="<b>Population Trends by District in Kedah (2020-2024)</b>",
                x=0.5,
                font=dict(size=19, color="#123B63")
            ),
            height=700,
            width=1100,
            margin=dict(
                l=90,
                r=120,
                t=100,
                b=80
            ),
            xaxis=dict(
                title="<b>Year</b>",
                tickmode="linear",
                dtick=1,
                showline=True,
                linewidth=2,
                linecolor="black",
                gridcolor="#D9E2F0"
            ),
            yaxis=dict(
                title="<b>Population (Thousands)</b>",
                tickformat=",.0f",
                showline=True,
                linewidth=2,
                linecolor="black",
                gridcolor="#D9E2F0"
            ),
            legend=dict(
                title="<b>District</b>",
                bgcolor="white",
                bordercolor="#B0BEC5",
                borderwidth=1
            ),
            hovermode="x unified"
        )

        # DISPLAY GRAPH
        st.plotly_chart(
            fig3,
            use_container_width=True,
            key="graph3"
        )

        st.subheader("🔍 Key Findings")

        if difference > 0:

            st.success(
                f"The combined population values increased "
                f"by {difference:,.0f} between "
                f"{first_year} and {last_year}."
            )

        elif difference < 0:

            st.warning(
                f"The combined population values decreased "
                f"by {abs(difference):,.0f} between "
                f"{first_year} and {last_year}."
            )

        else:

            st.info(
                "The combined population values remained unchanged."
            )

        st.subheader("📝 Interpretation and Discussion")

        st.markdown("""
        The line chart presents population trends across
        districts in Kedah from 2020 to 2024. Each coloured
        line represents a district, and each marker indicates
        the population recorded for a particular year.
        The direction of the lines helps identify increasing,
        decreasing or relatively stable population patterns.

        These changes provide information about differences
        in population development across districts. Such
        patterns are useful for understanding population
        distribution and supporting planning for public
        facilities, infrastructure and local services.
        """)

        with st.expander("View Detailed Population Data"):

            st.dataframe(
                df_population_graph,
                use_container_width=True
            )

    else:

        st.warning("No population records available.")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    padding:20px;
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
""", unsafe_allow_html=True)
