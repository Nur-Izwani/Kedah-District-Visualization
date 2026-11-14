
# ============================================================
# KEDAH DATA INSIGHTS
# Scientific Visualization Dashboard
# Household Income, Population and District Analysis
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
# 2. CUSTOM CSS - COLORFUL PROFESSIONAL DESIGN
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FC;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg, #123B63 0%, #176B87 100%
    );
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    background: linear-gradient(
        100deg, #123B63, #087E8B, #20A4A9
    );
    padding: 28px;
    border-radius: 18px;
    color: white;
    margin-bottom: 22px;
}

.main-title h1 {
    color: white;
    font-size: 34px;
    margin-bottom: 5px;
}

.main-title p {
    color: #E5F6FF;
    font-size: 15px;
}

.section-title {
    color: #123B63;
    font-size: 25px;
    font-weight: 750;
    margin-top: 15px;
}

.info-card {
    background: white;
    border-left: 5px solid #13A8A8;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(20,50,80,0.07);
    margin-bottom: 15px;
}

.summary-card {
    background: white;
    border-radius: 13px;
    padding: 17px;
    border: 1px solid #DCE6F2;
    box-shadow: 0 3px 10px rgba(20,50,80,0.05);
}

.small-note {
    color: #64748B;
    font-size: 13px;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #DCE6F2;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. LOAD DATASETS
# ============================================================

@st.cache_data
def load_datasets():

    income_data = pd.read_csv(
        "kedah_merged_2024.csv"
    )

    population_data = pd.read_csv(
        "kedah_population_2020_2024.csv"
    )

    return income_data, population_data


try:

    df_income, df_population = load_datasets()

except Exception as error:

    st.error(
        f"Unable to load dataset: {error}"
    )

    st.info(
        "Please check the CSV filenames in your GitHub repository."
    )

    st.stop()


# ============================================================
# 4. DATA PREPROCESSING
# ============================================================

# Clean column names
df_income.columns = df_income.columns.str.strip()
df_population.columns = df_population.columns.str.strip()

# Convert dates
if "date" in df_income.columns:

    df_income["date"] = pd.to_datetime(
        df_income["date"], errors="coerce"
    )

if "date" in df_population.columns:

    df_population["date"] = pd.to_datetime(
        df_population["date"], errors="coerce"
    )

# Convert numerical variables
income_numeric = [
    "income_mean",
    "income_median",
    "poverty_absolute",
    "poverty_relative",
    "population"
]

for column in income_numeric:

    if column in df_income.columns:

        df_income[column] = pd.to_numeric(
            df_income[column], errors="coerce"
        )

if "population" in df_population.columns:

    df_population["population"] = pd.to_numeric(
        df_population["population"], errors="coerce"
    )

# Filter Kedah if state column exists
if "state" in df_income.columns:

    df_income = df_income[
        df_income["state"].astype(str).str.strip().str.lower()
        == "kedah"
    ].copy()

if "state" in df_population.columns:

    df_population = df_population[
        df_population["state"].astype(str).str.strip().str.lower()
        == "kedah"
    ].copy()

# Filter 2024 income dataset
if "date" in df_income.columns:

    df_income = df_income[
        df_income["date"].dt.year == 2024
    ].copy()

# Filter population years
if "date" in df_population.columns:

    df_population["year"] = (
        df_population["date"].dt.year
    )

elif "year" in df_population.columns:

    df_population["year"] = pd.to_numeric(
        df_population["year"], errors="coerce"
    )

else:

    st.error("Population dataset does not contain date or year.")

    st.stop()

df_population = df_population[
    df_population["year"].between(2020, 2024)
].copy()


# ============================================================
# 5. FILTER OVERALL DEMOGRAPHIC
# ============================================================

def filter_overall(data):

    filters = {
        "sex": "both",
        "age": "overall",
        "ethnicity": "overall"
    }

    for column, value in filters.items():

        if column in data.columns:

            data = data[
                data[column].astype(str).str.lower() == value
            ].copy()

    return data


df_income = filter_overall(df_income)
df_population = filter_overall(df_population)


# ============================================================
# 6. PREPARE GRAPH 1 DATA
# ============================================================

graph1_data = df_income.dropna(
    subset=["district", "income_mean"]
).copy()

graph1_data = (
    graph1_data.groupby(
        "district", as_index=False
    )["income_mean"].mean()
)

graph1_data = graph1_data.sort_values(
    "income_mean", ascending=True
)


# ============================================================
# 7. PREPARE GRAPH 2 DATA
# ============================================================

graph2_data = df_income.dropna(
    subset=["district", "population", "income_mean"]
).copy()

graph2_data = (
    graph2_data.groupby(
        "district", as_index=False
    )[["population", "income_mean"]].mean()
)

graph2_data["district"] = (
    graph2_data["district"].astype(str)
)

graph2_data = graph2_data.sort_values("district")


# ============================================================
# 8. PREPARE GRAPH 3 DATA
# ============================================================

graph3_data = df_population.dropna(
    subset=["district", "year", "population"]
).copy()

graph3_data = (
    graph3_data.groupby(
        ["district", "year"], as_index=False
    )["population"].mean()
)

graph3_data = graph3_data.sort_values(
    ["district", "year"]
)


# ============================================================
# 9. COLOR PALETTE
# ============================================================

district_colors = [
    "#EF476F",
    "#118AB2",
    "#06D6A0",
    "#FFD166",
    "#845EC2",
    "#FF9671",
    "#00C9A7",
    "#4D8076",
    "#C34A36",
    "#4B4453",
    "#008F7A",
    "#B39CD0"
]

chart_layout = dict(
    template="plotly_white",
    font=dict(
        family="Arial",
        size=12,
        color="#26374A"
    ),
    paper_bgcolor="white",
    plot_bgcolor="white",
    hoverlabel=dict(
        bgcolor="white",
        font_size=13
    )
)


# ============================================================
# 10. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown(
    "# 📊 KEDAH DATA"
)

st.sidebar.caption(
    "Scientific Visualization Dashboard"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "🏠 Dashboard Overview",
        "📊 Objective 1 - Income",
        "🔵 Objective 2 - Scatter Plot",
        "📈 Objective 3 - Population"
    ]
)

st.sidebar.divider()

st.sidebar.markdown(
    "**STUDY INFORMATION**"
)

st.sidebar.markdown(
    """
    📍 Study Area: Kedah

    📅 Income: 2024

    📅 Population: 2020–2024

    📚 Data Source: DOSM
    """
)

st.sidebar.caption(
    "Scientific Visualization Project"
)


# ============================================================
# 11. DASHBOARD HEADER
# ============================================================

def dashboard_header():

    st.markdown("""
    <div class="main-title">

        <h1>📊 KEDAH DATA INSIGHTS</h1>

        <p>
        Household Income, Population and District Analysis
        </p>

        <p>
        SCIENTIFIC VISUALIZATION | KEDAH, MALAYSIA
        </p>

    </div>
    """, unsafe_allow_html=True)


dashboard_header()


# ============================================================
# PAGE 1: DASHBOARD OVERVIEW
# ============================================================

if page == "🏠 Dashboard Overview":

    st.markdown(
        '<div class="section-title">Dashboard Overview</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore household income and population patterns "
        "across districts in Kedah."
    )

    # Key metrics
    col1, col2, col3 = st.columns(3)

    total_districts = graph1_data["district"].nunique()

    col1.metric(
        "📍 Total Districts",
        total_districts
    )

    col2.metric(
        "💰 Income Reference Year",
        "2024"
    )

    col3.metric(
        "👥 Population Period",
        "2020–2024"
    )

    st.divider()

    st.subheader("🎯 Research Objectives")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown("""
        <div class="summary-card">

        <h3 style="color:#118AB2;">01 💰 Income</h3>

        <p>
        To analyze differences in mean household income
        across districts in Kedah in 2024.
        </p>

        <b>Horizontal Bar Chart</b>

        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="summary-card">

        <h3 style="color:#EF476F;">02 🔵 Relationship</h3>

        <p>
        To examine the relationship between district
        population and mean household income in Kedah.
        </p>

        <b>Scatter Plot</b>

        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="summary-card">

        <h3 style="color:#06A77D;">03 📈 Population</h3>

        <p>
        To analyze population trends across districts
        in Kedah from 2020 to 2024.
        </p>

        <b>Line Chart</b>

        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("📌 Study Scope")

    st.info(
        "This study focuses on districts in Kedah, Malaysia. "
        "Household income and population relationships are "
        "examined using district-level data."
    )

    st.subheader("📂 Dataset Preview")

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
# PAGE 2: OBJECTIVE 1 - INCOME
# ============================================================

elif page == "📊 Objective 1 - Income":

    st.markdown(
        '<div class="section-title">'
        '💰 OBJECTIVE 1: HOUSEHOLD INCOME'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Analyze differences in mean household income "
        "across districts in Kedah in 2024."
    )

    if not graph1_data.empty:

        highest = graph1_data.iloc[-1]
        lowest = graph1_data.iloc[0]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Highest Mean Income",
            f"RM {highest['income_mean']:,.0f}",
            highest["district"]
        )

        col2.metric(
            "Lowest Mean Income",
            f"RM {lowest['income_mean']:,.0f}",
            lowest["district"]
        )

        col3.metric(
            "Income Difference",
            f"RM {highest['income_mean'] - lowest['income_mean']:,.0f}"
        )

        st.divider()

        st.subheader(
            "📊 Mean Household Income by District (2024)"
        )

        fig1 = px.bar(
            graph1_data,
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
                color="#26374A"
            ),
            marker_line_color="white",
            marker_line_width=1.2,
            cliponaxis=False
        )

        fig1.update_layout(
            **chart_layout,
            showlegend=False,
            height=max(480, len(graph1_data) * 48),
            margin=dict(l=30, r=120, t=35, b=50),
            xaxis_title="Mean Household Income (RM)",
            yaxis_title="District",
            xaxis=dict(
                tickformat=",",
                gridcolor="#E7EDF5"
            )
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        st.subheader("🔍 Key Findings")

        st.success(
            f"{highest['district']} records the highest "
            f"mean household income at RM "
            f"{highest['income_mean']:,.2f}."
        )

        st.info(
            f"{lowest['district']} records the lowest "
            f"mean household income at RM "
            f"{lowest['income_mean']:,.2f}."
        )

        st.subheader("📝 Interpretation & Discussion")

        st.markdown("""
        The horizontal bar chart illustrates differences
        in mean household income across districts in Kedah
        in 2024. The districts are arranged from the lowest
        to the highest income values, allowing a clear
        comparison of household income levels. The variation
        in bar lengths indicates that household income is
        not equally distributed across all districts.

        These differences may reflect variations in local
        economic activities, employment opportunities and
        household characteristics. However, mean household
        income alone does not explain the full economic
        condition of a district. Other factors, including
        living costs and income distribution, should also
        be considered.
        """)

        with st.expander("View detailed income data"):

            st.dataframe(
                graph1_data.sort_values(
                    "income_mean", ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )

        st.download_button(
            "⬇️ Download Income Data",
            graph1_data.to_csv(index=False).encode("utf-8"),
            "kedah_income_analysis.csv",
            "text/csv"
        )

    else:

        st.warning("No valid household income data found.")


# ============================================================
# PAGE 3: OBJECTIVE 2 - SCATTER PLOT
# ============================================================

elif page == "🔵 Objective 2 - Scatter Plot":

    st.markdown(
        '<div class="section-title">'
        '🔵 OBJECTIVE 2: POPULATION VS INCOME'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Examine the relationship between district population "
        "and mean household income in Kedah in 2024."
    )

    if len(graph2_data) >= 2:

        correlation = graph2_data[
            ["population", "income_mean"]
        ].corr().iloc[0, 1]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Districts Analyzed",
            len(graph2_data)
        )

        col2.metric(
            "Pearson Correlation",
            f"{correlation:.3f}"
        )

        if correlation > 0:
            relationship = "Positive"
        elif correlation < 0:
            relationship = "Negative"
        else:
            relationship = "No linear relationship"

        col3.metric(
            "Relationship Direction",
            relationship
        )

        st.divider()

        st.subheader(
            "📍 District Population vs Mean Household Income"
        )

        fig2 = px.scatter(
            graph2_data,
            x="population",
            y="income_mean",
            color="district",
            hover_name="district",
            size_max=15,
            color_discrete_sequence=district_colors,
            labels={
                "population": "Population (Thousands)",
                "income_mean": "Mean Household Income (RM)",
                "district": "District"
            }
        )

        fig2.update_traces(
            marker=dict(
                size=13,
                opacity=0.9,
                line=dict(
                    width=1.4,
                    color="#26374A"
                )
            )
        )

        fig2.update_layout(
            **chart_layout,
            height=620,
            margin=dict(l=60, r=210, t=35, b=65),
            legend=dict(
                title="District",
                orientation="v",
                x=1.02,
                y=1,
                bgcolor="white",
                bordercolor="#DCE6F2",
                borderwidth=1
            ),
            xaxis=dict(
                title="Population (Thousands)",
                tickformat=",",
                gridcolor="#E7EDF5"
            ),
            yaxis=dict(
                title="Mean Household Income (RM)",
                tickformat=",",
                gridcolor="#E7EDF5"
            )
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.subheader("🔍 Correlation Analysis")

        if abs(correlation) < 0.3:
            strength = "weak"
        elif abs(correlation) < 0.7:
            strength = "moderate"
        else:
            strength = "strong"

        st.info(
            f"The Pearson correlation is {correlation:.3f}, "
            f"indicating a {strength} {relationship.lower()} "
            "linear relationship between district population "
            "and mean household income."
        )

        st.subheader("📝 Interpretation & Discussion")

        st.markdown("""
        The scatter plot presents the relationship between
        district population and mean household income in
        Kedah in 2024. Each point represents a district.
        The horizontal axis indicates population size,
        while the vertical axis represents mean household
        income. The distribution of points helps identify
        whether districts with larger populations also
        tend to have higher or lower mean household income.

        The Pearson correlation coefficient provides a
        numerical indication of the direction and strength
        of the linear relationship. A positive value indicates
        that both variables tend to increase together,
        whereas a negative value indicates an opposite
        relationship. This analysis describes association
        and does not establish that population size causes
        changes in household income.
        """)

        with st.expander("View detailed scatter plot data"):

            st.dataframe(
                graph2_data,
                use_container_width=True,
                hide_index=True
            )

        st.download_button(
            "⬇️ Download Scatter Data",
            graph2_data.to_csv(index=False).encode("utf-8"),
            "kedah_population_income.csv",
            "text/csv"
        )

    else:

        st.warning(
            "At least two valid district records are required."
        )


# ============================================================
# PAGE 4: OBJECTIVE 3 - POPULATION TRENDS
# ============================================================

elif page == "📈 Objective 3 - Population":

    st.markdown(
        '<div class="section-title">'
        '📈 OBJECTIVE 3: POPULATION TRENDS'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Analyze population trends across districts "
        "in Kedah from 2020 to 2024."
    )

    if not graph3_data.empty:

        first_year = graph3_data["year"].min()
        last_year = graph3_data["year"].max()

        first_total = graph3_data[
            graph3_data["year"] == first_year
        ]["population"].sum()

        last_total = graph3_data[
            graph3_data["year"] == last_year
        ]["population"].sum()

        difference = last_total - first_total

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Starting Year",
            int(first_year)
        )

        col2.metric(
            "Latest Year",
            int(last_year)
        )

        col3.metric(
            "Population Difference",
            f"{difference:,.0f}",
            delta=f"{difference / first_total * 100:.2f}%"
            if first_total else None
        )

        st.divider()

        st.subheader(
            "📈 Population Trends by District (2020–2024)"
        )

        fig3 = px.line(
            graph3_data,
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
            **chart_layout,
            height=620,
            margin=dict(l=50, r=180, t=35, b=65),
            legend=dict(
                title="District",
                orientation="v",
                x=1.02,
                y=1,
                bgcolor="white",
                bordercolor="#DCE6F2",
                borderwidth=1
            ),
            xaxis=dict(
                title="Year",
                tickmode="linear",
                dtick=1,
                gridcolor="#E7EDF5"
            ),
            yaxis=dict(
                title="Population (Thousands)",
                tickformat=",",
                gridcolor="#E7EDF5"
            ),
            hovermode="x unified"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        st.subheader("🔍 Key Findings")

        if difference > 0:

            st.success(
                f"The combined population value across "
                f"the displayed districts increased by "
                f"{difference:,.0f} between {first_year} "
                f"and {last_year}."
            )

        elif difference < 0:

            st.warning(
                f"The combined population value across "
                f"the displayed districts decreased by "
                f"{abs(difference):,.0f} between {first_year} "
                f"and {last_year}."
            )

        else:

            st.info(
                "The combined population value was unchanged "
                "between the first and latest year."
            )

        st.subheader("📝 Interpretation & Discussion")

        st.markdown("""
        The line chart illustrates population trends across
        districts in Kedah from 2020 to 2024. Each coloured
        line represents a district, and the markers indicate
        population values for individual years. The direction
        of each line makes it possible to identify increases,
        decreases or relatively stable population patterns.

        Differences in population trends may be associated
        with migration, employment opportunities, urban
        development and demographic changes. These patterns
        are useful for understanding population distribution
        and supporting planning for public facilities,
        infrastructure and local services.
        """)

        with st.expander("View detailed population data"):

            st.dataframe(
                graph3_data,
                use_container_width=True,
                hide_index=True
            )

        st.download_button(
            "⬇️ Download Population Data",
            graph3_data.to_csv(index=False).encode("utf-8"),
            "kedah_population_trends.csv",
            "text/csv"
        )

    else:

        st.warning("No valid population records found.")


# ============================================================
# 12. FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:15px; color:#64748B;">

    <b>KEDAH DATA INSIGHTS</b>

    <br>

    Scientific Visualization Project

    <br>

    Household Income & Population Analysis | 2020–2024

    <br>

    Data source: Department of Statistics Malaysia (DOSM)

    </div>
    """,
    unsafe_allow_html=True
)
