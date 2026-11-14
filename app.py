
# ============================================================
# KEDAH DATA INSIGHTS
# JIE42403 - SCIENTIFIC VISUALIZATION
# Study Area: Kedah, Malaysia
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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
# 2. CUSTOM DESIGN
# ============================================================

st.markdown("""
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
    padding: 30px;
    border-radius: 18px;
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

.section-title {
    color: #123B63;
    font-size: 25px;
    font-weight: 750;
    margin-top: 15px;
}

.summary-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #DCE6F2;
    box-shadow: 0 3px 12px rgba(20,50,80,0.06);
    min-height: 115px;
}

.summary-label {
    color: #64748B;
    font-size: 13px;
    font-weight: 600;
}

.summary-value {
    color: #123B63;
    font-size: 25px;
    font-weight: 800;
    margin-top: 8px;
}

.summary-detail {
    color: #64748B;
    font-size: 12px;
    margin-top: 4px;
}

.objective-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border-left: 5px solid #13A8A8;
    margin-bottom: 20px;
    box-shadow: 0 3px 10px rgba(20,50,80,0.05);
}

div[data-testid="stPlotlyChart"] {
    background: white;
    border-radius: 14px;
    padding: 10px;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #DCE6F2;
    padding: 15px;
    border-radius: 12px;
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

except Exception as error:

    st.error(f"Dataset loading error: {error}")
    st.stop()


# ============================================================
# 4. DATA PREPROCESSING
# ============================================================

# Clean column names
df_income.columns = df_income.columns.str.strip()
df_population.columns = df_population.columns.str.strip()

# Convert date
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

# Filter demographic variables
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

# Convert numerical values
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

# Income: 2024 only
df_income = df_income[
    df_income["date"].dt.year == 2024
].copy()

# Population: 2020-2024
df_population["year"] = (
    df_population["date"].dt.year
)

df_population = df_population[
    df_population["year"].between(2020, 2024)
].copy()


# ============================================================
# 5. GRAPH 1 DATA
# ============================================================

df_income_graph = df_income.dropna(
    subset=["district", "income_mean"]
).copy()

df_income_graph = (
    df_income_graph.groupby(
        "district", as_index=False
    )["income_mean"].mean()
    .sort_values("income_mean", ascending=True)
)


# ============================================================
# 6. GRAPH 2 DATA
# ============================================================

# Prepare income data
df_income_graph2 = df_income.copy()

# Prepare population data
df_population_graph2 = df_population.copy()

# Filter population for 2024
df_population_graph2 = df_population_graph2[
    df_population_graph2["date"].dt.year == 2024
].copy()

# Select columns
df_income_graph2 = df_income_graph2[
    ["state", "district", "date", "income_mean"]
].copy()

df_population_graph2 = df_population_graph2[
    ["state", "district", "date", "population"]
].copy()

# Remove missing values
df_income_graph2 = df_income_graph2.dropna(
    subset=["state", "district", "date", "income_mean"]
)

df_population_graph2 = df_population_graph2.dropna(
    subset=["state", "district", "date", "population"]
)

# Group duplicate district records
df_income_graph2 = (
    df_income_graph2.groupby(
        ["state", "district", "date"],
        as_index=False
    )["income_mean"].mean()
)

df_population_graph2 = (
    df_population_graph2.groupby(
        ["state", "district", "date"],
        as_index=False
    )["population"].mean()
)

# Merge datasets
df_scatter = pd.merge(
    df_population_graph2,
    df_income_graph2,
    on=["state", "district", "date"],
    how="inner",
    validate="one_to_one"
)

# Create district labels
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
# 7. GRAPH 3 DATA
# ============================================================

df_population_graph = df_population.copy()

df_population_graph = df_population_graph.dropna(
    subset=["district", "population", "year"]
)

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
# 9. SUMMARY CARD FUNCTION
# ============================================================

def summary_card(label, value, detail, color):
    """Render a summary card using native Streamlit elements.

    This avoids Markdown interpreting indented HTML as a code block.
    """
    with st.container(border=True):
        st.caption(label)
        st.markdown(
            f"<h2 style='color:{color}; margin:0.25rem 0;'>"
            f"{value}</h2>",
            unsafe_allow_html=True
        )
        st.caption(detail)


# ============================================================
# 10. SIDEBAR NAVIGATION
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
        ":material/account_balance_wallet: Visualization 1",
        ":material/scatter_plot: Visualization 2",
        ":material/show_chart: Visualization 3"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### STUDY INFORMATION")

st.sidebar.markdown("""
**Study Area:** Kedah, Malaysia

**Income:** 2024

**Population:** 2020–2024

**Analysis:** District Level
""")

st.sidebar.caption(
    "JIE42403 | Scientific Visualization"
)


# ============================================================
# 11. MAIN HEADER
# ============================================================

st.markdown("""
<div class="main-header">

<h1>KEDAH DATA INSIGHTS</h1>

<p>
Household Income, Population, Poverty
</p>

<p>
SCIENTIFIC VISUALIZATION | KEDAH, MALAYSIA
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# PAGE 1: DASHBOARD OVERVIEW
# ============================================================

if "Dashboard Overview" in page:

    st.markdown(
        '<div class="section-title">'
        ':material/dashboard: Dashboard Overview'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "This dashboard explores household income, "
        "population and district-level patterns in Kedah."
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

    st.subheader("Research Objectives")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown("""
        <div class="objective-card">
        <h3 style="color:#1565C0;">
        Household Income
        </h3>
        <p>
        To examine differences in mean household income
        across districts in Kedah in 2024.
        </p>
        <b>Horizontal Bar Chart</b>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="objective-card">
        <h3 style="color:#E53935;">
        Population and Income
        </h3>
        <p>
        To examine the relationship between district
        population and mean household income in Kedah in 2024.
        </p>
        <b>Scatter Plot</b>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="objective-card">
        <h3 style="color:#00897B;">
        Population Trends
        </h3>
        <p>
        To analyze population trends across districts
        in Kedah from 2020 to 2024.
        </p>
        <b>Line Chart</b>
        </div>
        """, unsafe_allow_html=True)

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
# PAGE 2: OBJECTIVE 1
# ============================================================

elif "Objective 1" in page:

    st.markdown(
        '<div class="section-title">'
        'OBJECTIVE 1:' 
        '</div>',
        unsafe_allow_html=True
    )

    # OBJECTIVE STATEMENT
    st.markdown(
        """
        <div class="objective-card">
        <b>Objective Statement</b>
        <p>
        To examine the differences in mean household income
        across districts in Kedah in 2024.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not df_income_graph.empty:

        highest = df_income_graph.iloc[-1]
        lowest = df_income_graph.iloc[0]

        average = df_income_graph["income_mean"].mean()

        income_gap = (
            highest["income_mean"] - lowest["income_mean"]
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
            color_discrete_sequence=[
                "#1565C0", "#1976D2", "#1E88E5",
                "#039BE5", "#00ACC1", "#00897B",
                "#43A047", "#7CB342", "#F9A825",
                "#EF6C00", "#D84315", "#8E24AA"
            ],
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
                xanchor="center",
                font=dict(size=20, color="#123B63")
            ),
            showlegend=False,
            xaxis=dict(
                title="Mean Household Income (RM)",
                showline=True,
                linewidth=2,
                linecolor="black",
                tickformat=",.0f",
                showgrid=True,
                gridcolor="#D9E2F0",
                zeroline=False
            ),
            yaxis=dict(
                title="District",
                showline=True,
                linewidth=2,
                linecolor="black",
                tickfont=dict(size=12, color="black")
            ),
            height=600,
            margin=dict(
                l=100, r=120, t=100, b=80
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
# PAGE 3: OBJECTIVE 2
# ============================================================

elif "Objective 2" in page:

    st.markdown(
        '<div class="section-title">'

        'OBJECTIVE 2:'
        '</div>',
        unsafe_allow_html=True
    )

    # OBJECTIVE STATEMENT
    st.markdown("""
    <div class="objective-card">
    <b>Objective Statement</b>
    <p>
    To examine the relationship between district population
    and mean household income in Kedah in 2024.
    </p>
    </div>
    """, unsafe_allow_html=True)

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
                size=11,
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
                xanchor="center",
                font=dict(size=17, color="#123B63")
            ),
            xaxis=dict(
                title="<b>Population (Thousands)</b>",
                showline=True,
                linewidth=2,
                linecolor="black",
                mirror=True,
                tickformat=",.0f",
                showgrid=True,
                gridcolor="lightgrey"
            ),
            yaxis=dict(
                title="<b>Mean Household Income (RM)</b>",
                showline=True,
                linewidth=2,
                linecolor="black",
                mirror=True,
                tickformat=",.0f",
                showgrid=True,
                gridcolor="lightgrey"
            ),
            legend=dict(
                title=dict(text="<b>District</b>"),
                orientation="v",
                y=1,
                x=1.02,
                bgcolor="white",
                bordercolor="black",
                borderwidth=1,
                font=dict(size=10)
            ),
            height=620,
            margin=dict(
                l=85, r=190, t=85, b=75
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
        {direction.lower()} linear relationship between
        the two variables.

        A {direction.lower()} relationship suggests that
        population size and mean household income tend to
        move in the same or opposite direction. The
        distribution of individual points also helps
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
# PAGE 4: OBJECTIVE 3
# ============================================================

elif "Objective 3" in page:

    st.markdown(
        '<div class="section-title">'
        'OBJECTIVE 3:'
        '</div>',
        unsafe_allow_html=True
    )

    # OBJECTIVE STATEMENT
    st.markdown("""
    <div class="objective-card">
    <b>Objective Statement</b>
    <p>
    To analyze population trends across districts
    in Kedah from 2020 to 2024.
    </p>
    </div>
    """, unsafe_allow_html=True)

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

        population_change = last_total - first_total

        percentage_change = (
            population_change / first_total * 100
            if first_total != 0 else 0
        )

        highest_latest = df_population_graph[
            df_population_graph["year"] == last_year
        ].sort_values(
            "population", ascending=False
        ).iloc[0]

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

        st.info(
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
            color_discrete_sequence=[
                "#E53935",
                "#1565C0",
                "#00A6A6",
                "#8E24AA",
                "#F57C00",
                "#2E7D32",
                "#EC407A",
                "#5C6BC0",
                "#795548",
                "#00838F",
                "#9E9D24",
                "#6D4C41"
            ],
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
                xanchor="center",
                font=dict(size=20, color="#123B63")
            ),
            xaxis=dict(
                title="Year",
                tickmode="linear",
                dtick=1,
                showline=True,
                linewidth=2,
                linecolor="black",
                showgrid=True,
                gridcolor="#D9E2F0"
            ),
            yaxis=dict(
                title="Population (Thousands)",
                showline=True,
                linewidth=2,
                linecolor="black",
                tickformat=",.0f",
                showgrid=True,
                gridcolor="#D9E2F0"
            ),
            legend=dict(
                title="District",
                bgcolor="white",
                bordercolor="#B0BEC5",
                borderwidth=1
            ),
            height=650,
            margin=dict(
                l=90, r=120, t=100, b=80
            )
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

        st.warning("No population records found.")


# ============================================================
# 12. FOOTER
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

