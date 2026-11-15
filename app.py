
# ============================================================
# MALAYSIA DATA INSIGHTS
# JIE42403 - SCIENTIFIC VISUALIZATION
# Study Area: Malaysia
# Analysis Level: State and District
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
    page_title="Malaysia Data Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. DESIGN AND CSS
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
# 3. LOAD THREE DATASETS
# ============================================================

@st.cache_data
def load_data():

    income = pd.read_csv("hh_income_district.csv")

    poverty = pd.read_csv("hh_poverty_district.csv")

    population = pd.read_csv("population_district.csv")

    return income, poverty, population


try:

    df_income, df_poverty, df_population = load_data()

except Exception as error:

    st.error(f"Dataset loading error: {error}")

    st.info(
        "Please ensure all three CSV files are uploaded "
        "to the same GitHub repository as app.py."
    )

    st.stop()


# ============================================================
# 4. DATA PREPROCESSING
# ============================================================

# Clean column names
for data in [df_income, df_poverty, df_population]:

    data.columns = data.columns.str.strip().str.lower()

    for col in ["state", "district"]:

        if col in data.columns:

            data[col] = (
                data[col].astype("string").str.strip()
            )

    if "date" in data.columns:

        data["date"] = pd.to_datetime(
            data["date"], errors="coerce"
        )

        data["year"] = data["date"].dt.year


# Filter population demographic categories
def filter_population(data):

    for col, value in {
        "sex": "both",
        "age": "overall",
        "ethnicity": "overall"
    }.items():

        if col in data.columns:

            data = data[
                data[col].astype(str).str.strip().str.lower()
                == value
            ].copy()

    return data


df_population = filter_population(df_population)


# Convert numerical variables
numeric_columns = {
    "income": [
        "income_mean",
        "income_median"
    ],
    "poverty": [
        "poverty_absolute",
        "poverty_relative"
    ],
    "population": [
        "population"
    ]
}

for col in numeric_columns["income"]:

    if col in df_income.columns:

        df_income[col] = pd.to_numeric(
            df_income[col], errors="coerce"
        )

for col in numeric_columns["poverty"]:

    if col in df_poverty.columns:

        df_poverty[col] = pd.to_numeric(
            df_poverty[col], errors="coerce"
        )

df_population["population"] = pd.to_numeric(
    df_population["population"], errors="coerce"
)


# Filter required years
df_income = df_income[
    df_income["year"].isin([2022, 2024])
].copy()

df_poverty = df_poverty[
    df_poverty["year"].isin([2022, 2024])
].copy()

df_population = df_population[
    df_population["year"].between(2020, 2024)
].copy()


# Remove incomplete geographical records
for name, data in {
    "Income": df_income,
    "Poverty": df_poverty,
    "Population": df_population
}.items():

    data.dropna(
        subset=["state", "district", "year"],
        inplace=True
    )


# ============================================================
# 5. COMMON SETTINGS
# ============================================================

BLUE = "#3984D6"
TEAL = "#16B8A6"
NAVY = "#123B63"
ORANGE = "#F59E0B"
RED = "#E53935"

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

# District label to avoid duplicate district names
for data in [df_income, df_poverty, df_population]:

    data["district_label"] = (
        data["district"].astype(str)
        + " ("
        + data["state"].astype(str)
        + ")"
    )


# ============================================================
# 6. SUMMARY CARD FUNCTION
# ============================================================

def summary_card(label, value, detail, color):

    st.markdown(
        f"""
        <div class="summary-card"
             style="border-top:4px solid {color};">

            <div class="summary-label">{label}</div>

            <div class="summary-value">{value}</div>

            <div class="summary-detail">{detail}</div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 7. PREPARE OBJECTIVE 1 DATA
# ============================================================

df_income_grouped = (
    df_income
    .dropna(subset=["income_mean"])
    .groupby(
        ["state", "district", "year"],
        as_index=False
    )["income_mean"]
    .mean()
)

df_income_pivot = df_income_grouped.pivot_table(
    index=["state", "district"],
    columns="year",
    values="income_mean"
).reset_index()

# Only matched districts
if 2022 in df_income_pivot.columns and 2024 in df_income_pivot.columns:

    df_dumbbell = df_income_pivot.dropna(
        subset=[2022, 2024]
    ).copy()

else:

    df_dumbbell = pd.DataFrame()


if not df_dumbbell.empty:

    df_dumbbell["change"] = (
        df_dumbbell[2024] - df_dumbbell[2022]
    )

    df_dumbbell["change_percent"] = (
        df_dumbbell["change"]
        / df_dumbbell[2022].replace(0, np.nan)
        * 100
    )

    df_dumbbell["district_label"] = (
        df_dumbbell["district"]
        + " ("
        + df_dumbbell["state"]
        + ")"
    )


# ============================================================
# 8. PREPARE OBJECTIVE 2 DATA
# ============================================================

income_for_merge = (
    df_income
    .dropna(subset=["income_mean"])
    .groupby(
        ["state", "district", "year"],
        as_index=False
    )["income_mean"]
    .mean()
)

poverty_for_merge = (
    df_poverty
    .dropna(subset=["poverty_absolute"])
    .groupby(
        ["state", "district", "year"],
        as_index=False
    )["poverty_absolute"]
    .mean()
)

df_scatter = pd.merge(
    income_for_merge,
    poverty_for_merge,
    on=["state", "district", "year"],
    how="inner",
    validate="one_to_one"
)

df_scatter["district_label"] = (
    df_scatter["district"]
    + " ("
    + df_scatter["state"]
    + ")"
)


# ============================================================
# 9. PREPARE OBJECTIVE 3 DATA
# ============================================================

df_population_graph = (
    df_population
    .dropna(subset=["population"])
    .groupby(
        ["state", "district", "year"],
        as_index=False
    )["population"]
    .mean()
)

df_population_graph["district_label"] = (
    df_population_graph["district"]
    + " ("
    + df_population_graph["state"]
    + ")"
)

df_population_graph = df_population_graph.sort_values(
    ["state", "district", "year"]
)


# ============================================================
# 10. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown("# MALAYSIA DATA INSIGHTS")

st.sidebar.caption(
    "Scientific Visualization Dashboard"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Visualization 1 - Income",
        "Visualization 2 - Poverty",
        "Visualization 3 - Population"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### STUDY INFORMATION")

st.sidebar.markdown("""
**Study Area:** Malaysia

**Analysis Level:** State and District

**Income & Poverty:** 2022–2024

**Population:** 2020–2024
""")

st.sidebar.caption(
    "JIE42403 | Scientific Visualization"
)


# ============================================================
# 11. MAIN HEADER
# ============================================================

st.markdown("""
<div class="main-header">

<h1>MALAYSIA DATA INSIGHTS</h1>

<p>
Household Income, Poverty and Population Analysis
</p>

<p>
SCIENTIFIC VISUALIZATION | MALAYSIA
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# PAGE 1: DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown(
        '<div class="section-title">'
        'Dashboard Overview'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "This dashboard explores household income, "
        "poverty and population patterns across "
        "states and districts in Malaysia."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Study Area",
        "Malaysia"
    )

    c2.metric(
        "Income & Poverty",
        "2022–2024"
    )

    c3.metric(
        "Population",
        "2020–2024"
    )

    c4.metric(
        "States Available",
        df_population["state"].nunique()
    )

    st.divider()

    st.subheader("Research Objectives")

    obj1, obj2, obj3 = st.columns(3)

    with obj1:

        st.markdown("""
        <div class="objective-card">

        <h3 style="color:#3984D6;">
        Objective 1
        </h3>

        <p>
        To compare changes in mean household income
        across districts in Malaysia by state
        between 2022 and 2024.
        </p>

        <b>Dumbbell Plot</b>

        </div>
        """, unsafe_allow_html=True)

    with obj2:

        st.markdown("""
        <div class="objective-card">

        <h3 style="color:#16B8A6;">
        Objective 2
        </h3>

        <p>
        To examine the relationship between absolute
        poverty rates and mean household income
        across districts in Malaysia.
        </p>

        <b>Scatter Plot with Trendline</b>

        </div>
        """, unsafe_allow_html=True)

    with obj3:

        st.markdown("""
        <div class="objective-card">

        <h3 style="color:#F59E0B;">
        Objective 3
        </h3>

        <p>
        To analyze population distribution,
        differences and trends across districts
        in Malaysia from 2020 to 2024.
        </p>

        <b>Heatmap, Box Plot and Line Chart</b>

        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Dataset Information")

    tab1, tab2, tab3 = st.tabs([
        "Household Income",
        "Household Poverty",
        "Population"
    ])

    with tab1:

        st.write("Household income records available for 2022 and 2024.")

        st.dataframe(
            df_income.head(10),
            use_container_width=True,
            hide_index=True
        )

    with tab2:

        st.write("Household poverty records available for 2022 and 2024.")

        st.dataframe(
            df_poverty.head(10),
            use_container_width=True,
            hide_index=True
        )

    with tab3:

        st.write("Population records from 2020 to 2024.")

        st.dataframe(
            df_population.head(10),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PAGE 2: VISUALIZATION 1 - HOUSEHOLD INCOME
# ============================================================

elif page == "Visualization 1 - Income":

    st.markdown(
        '<div class="section-title">'
        'VISUALIZATION 1: HOUSEHOLD INCOME'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="objective-card">

    <b>Objective Statement</b>

    <p>
    To compare changes in mean household income
    across districts in Malaysia by state
    between 2022 and 2024.
    </p>

    </div>
    """, unsafe_allow_html=True)

    if not df_dumbbell.empty:

        # State dropdown
        states = sorted(df_dumbbell["state"].unique())

        selected_state = st.selectbox(
            "Select State",
            ["All States"] + states
        )

        if selected_state == "All States":

            income_view = df_dumbbell.copy()

        else:

            income_view = df_dumbbell[
                df_dumbbell["state"] == selected_state
            ].copy()

        # Summary
        highest = income_view.loc[
            income_view["2024"].idxmax()
        ]

        lowest = income_view.loc[
            income_view["2024"].idxmin()
        ]

        average_change = income_view["change"].mean()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            summary_card(
                "Districts Analysed",
                f"{len(income_view)}",
                "Matched 2022 and 2024",
                BLUE
            )

        with col2:

            summary_card(
                "Highest Income (2024)",
                f"RM {highest[2024]:,.0f}",
                highest["district"],
                TEAL
            )

        with col3:

            summary_card(
                "Lowest Income (2024)",
                f"RM {lowest[2024]:,.0f}",
                lowest["district"],
                RED
            )

        with col4:

            summary_card(
                "Average Change",
                f"RM {average_change:+,.0f}",
                "2024 compared with 2022",
                ORANGE
            )

        st.divider()

        st.subheader("Visualization 1: Dumbbell Plot")

        # Sort districts
        income_view = income_view.sort_values(
            ["state", "district"]
        ).reset_index(drop=True)

        income_view["label"] = (
            income_view["district"]
            + " ("
            + income_view["state"]
            + ")"
        )

        fig1 = go.Figure()

        # Connecting lines
        for _, row in income_view.iterrows():

            fig1.add_trace(
                go.Scatter(
                    x=[row[2022], row[2024]],
                    y=[row["label"], row["label"]],
                    mode="lines",
                    line=dict(
                        color="#B8C5D1",
                        width=3
                    ),
                    showlegend=False,
                    hoverinfo="skip"
                )
            )

        # 2022 markers
        fig1.add_trace(
            go.Scatter(
                x=income_view[2022],
                y=income_view["label"],
                mode="markers",
                name="2022",
                marker=dict(
                    color=BLUE,
                    size=10,
                    line=dict(color="black", width=1)
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Year: 2022<br>"
                    "Income: RM %{x:,.0f}"
                    "<extra></extra>"
                )
            )
        )

        # 2024 markers
        fig1.add_trace(
            go.Scatter(
                x=income_view[2024],
                y=income_view["label"],
                mode="markers",
                name="2024",
                marker=dict(
                    color=TEAL,
                    size=10,
                    line=dict(color="black", width=1)
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Year: 2024<br>"
                    "Income: RM %{x:,.0f}"
                    "<extra></extra>"
                )
            )
        )

        fig1.update_layout(
            **chart_theme,

            title=dict(
                text="<b>Mean Household Income by District (2022 vs 2024)</b>",
                x=0.5,
                font=dict(size=18, color=NAVY)
            ),

            height=max(550, len(income_view) * 32),

            legend=dict(
                title="Year",
                orientation="v",
                x=1.02,
                y=0.5,
                yanchor="middle"
            ),

            margin=dict(
                l=180,
                r=150,
                t=100,
                b=80
            )
        )

        fig1.update_xaxes(
            title="Mean Household Income (RM)",
            tickformat=",.0f",
            showline=True,
            linewidth=2,
            linecolor="black",
            mirror=True,
            showgrid=True,
            gridcolor="#DCE3EA"
        )

        fig1.update_yaxes(
            title="District",
            showline=True,
            linewidth=2,
            linecolor="black",
            mirror=True,
            showgrid=True,
            gridcolor="#E8EDF2",
            autorange="reversed"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        # Interpretation
        st.subheader("Interpretation and Discussion")

        increase_count = int(
            (income_view["change"] > 0).sum()
        )

        decrease_count = int(
            (income_view["change"] < 0).sum()
        )

        st.markdown(f"""
        The dumbbell plot compares mean household income
        across districts between 2022 and 2024.

        Among the displayed districts, {increase_count}
        recorded an increase in mean household income,
        while {decrease_count} recorded a decrease.

        The difference between the two markers represents
        the size and direction of income changes. Longer
        connecting lines indicate larger changes, while
        shorter lines indicate smaller changes.
        """)

        with st.expander("View Detailed Income Data"):

            st.dataframe(
                income_view[
                    [
                        "state", "district",
                        2022, 2024,
                        "change", "change_percent"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

    else:

        st.warning(
            "No matched district income records for 2022 and 2024."
        )


# ============================================================
# PAGE 3: VISUALIZATION 2 - POVERTY AND INCOME
# ============================================================

elif page == "Visualization 2 - Poverty":

    st.markdown(
        '<div class="section-title">'
        'VISUALIZATION 2: POVERTY AND INCOME'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="objective-card">

    <b>Objective Statement</b>

    <p>
    To examine the relationship between absolute poverty
    rates and mean household income across districts
    in Malaysia.
    </p>

    </div>
    """, unsafe_allow_html=True)

    if len(df_scatter) >= 2:

        selected_year = st.selectbox(
            "Select Year",
            sorted(
                df_scatter["year"].unique(),
                reverse=True
            )
        )

        scatter_view = df_scatter[
            df_scatter["year"] == selected_year
        ].copy()

        if len(scatter_view) >= 2:

            correlation = scatter_view[
                ["poverty_absolute", "income_mean"]
            ].corr().iloc[0, 1]

            highest_poverty = scatter_view.loc[
                scatter_view["poverty_absolute"].idxmax()
            ]

            lowest_poverty = scatter_view.loc[
                scatter_view["poverty_absolute"].idxmin()
            ]

            if pd.isna(correlation):

                strength = "Not available"
                direction = "Not available"

            else:

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

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                summary_card(
                    "Pearson Correlation",
                    f"{correlation:.3f}",
                    strength,
                    BLUE
                )

            with col2:

                summary_card(
                    "Districts Analysed",
                    str(len(scatter_view)),
                    f"Year {selected_year}",
                    TEAL
                )

            with col3:

                summary_card(
                    "Highest Poverty",
                    f"{highest_poverty['poverty_absolute']:.2f}%",
                    highest_poverty["district"],
                    RED
                )

            with col4:

                summary_card(
                    "Lowest Poverty",
                    f"{lowest_poverty['poverty_absolute']:.2f}%",
                    lowest_poverty["district"],
                    ORANGE
                )

            st.divider()

            st.subheader("Visualization 2: Scatter Plot")

            fig2 = px.scatter(
                scatter_view,
                x="poverty_absolute",
                y="income_mean",
                color="state",
                trendline="ols",
                hover_name="district_label",
                hover_data={
                    "state": True,
                    "district": True,
                    "poverty_absolute": ":.2f",
                    "income_mean": ":,.0f"
                },
                labels={
                    "poverty_absolute": "Absolute Poverty Rate (%)",
                    "income_mean": "Mean Household Income (RM)",
                    "state": "State"
                },
                title=(
                    "Relationship Between Absolute Poverty "
                    f"and Mean Household Income ({selected_year})"
                )
            )

            fig2.update_traces(
                marker=dict(
                    size=11,
                    opacity=0.85,
                    line=dict(
                        color="black",
                        width=0.8
                    )
                ),
                selector=dict(mode="markers")
            )

            fig2.update_layout(
                **chart_theme,
                height=700,
                title=dict(
                    text=(
                        "<b>Absolute Poverty vs Mean Household Income</b>"
                        f"<br><sup>Malaysia | {selected_year}</sup>"
                    ),
                    x=0.5,
                    font=dict(size=18, color=NAVY)
                ),
                legend=dict(
                    title="State",
                    orientation="v",
                    x=1.02,
                    y=0.5,
                    yanchor="middle"
                ),
                margin=dict(
                    l=100,
                    r=180,
                    t=120,
                    b=90
                )
            )

            fig2.update_xaxes(
                title="Absolute Poverty Rate (%)",
                tickformat=",.1f",
                showline=True,
                linewidth=2,
                linecolor="black",
                mirror=True,
                showgrid=True,
                gridcolor="#DCE3EA"
            )

            fig2.update_yaxes(
                title="Mean Household Income (RM)",
                tickformat=",.0f",
                showline=True,
                linewidth=2,
                linecolor="black",
                mirror=True,
                showgrid=True,
                gridcolor="#DCE3EA"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            st.subheader("Interpretation and Discussion")

            st.markdown(f"""
            The scatter plot illustrates the relationship
            between absolute poverty rates and mean household
            income across districts in Malaysia in {selected_year}.

            The Pearson correlation coefficient is
            {correlation:.3f}, indicating a {strength.lower()}
            {direction.lower()} linear relationship.

            The position of each point represents one district.
            The trendline shows the general direction of the
            relationship. A negative correlation indicates
            that higher poverty rates tend to be associated
            with lower mean household income.

            However, correlation does not prove causation.
            """)

            with st.expander("View Detailed Poverty and Income Data"):

                st.dataframe(
                    scatter_view,
                    use_container_width=True,
                    hide_index=True
                )

        else:

            st.warning(
                "Not enough matched records for the selected year."
            )

    else:

        st.warning(
            "No matching income and poverty records found."
        )


# ============================================================
# PAGE 4: VISUALIZATION 3 - POPULATION
# ============================================================

elif page == "Visualization 3 - Population":

    st.markdown(
        '<div class="section-title">'
        'VISUALIZATION 3: POPULATION DISTRIBUTION'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="objective-card">

    <b>Objective Statement</b>

    <p>
    To analyze population distribution, differences and
    trends across districts in Malaysia from 2020 to 2024.
    </p>

    </div>
    """, unsafe_allow_html=True)

    if not df_population_graph.empty:

        # State filter
        states = sorted(
            df_population_graph["state"].unique()
        )

        selected_state = st.selectbox(
            "Select State for Population Analysis",
            ["All States"] + states
        )

        if selected_state == "All States":

            population_view = df_population_graph.copy()

        else:

            population_view = df_population_graph[
                df_population_graph["state"] == selected_state
            ].copy()

        first_year = int(
            population_view["year"].min()
        )

        last_year = int(
            population_view["year"].max()
        )

        first_total = population_view[
            population_view["year"] == first_year
        ]["population"].sum()

        last_total = population_view[
            population_view["year"] == last_year
        ]["population"].sum()

        population_change = last_total - first_total

        percentage_change = (
            population_change / first_total * 100
            if first_total != 0 else 0
        )

        highest_district = population_view[
            population_view["year"] == last_year
        ].nlargest(1, "population")

        lowest_district = population_view[
            population_view["year"] == last_year
        ].nsmallest(1, "population")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            summary_card(
                "Districts Analysed",
                str(population_view["district_label"].nunique()),
                "Available districts",
                BLUE
            )

        with col2:

            summary_card(
                f"Highest Population ({last_year})",
                f"{highest_district.iloc[0]['population']:,.0f}",
                highest_district.iloc[0]["district"],
                TEAL
            )

        with col3:

            summary_card(
                f"Lowest Population ({last_year})",
                f"{lowest_district.iloc[0]['population']:,.0f}",
                lowest_district.iloc[0]["district"],
                RED
            )

        with col4:

            summary_card(
                "Population Change",
                f"{percentage_change:+.2f}%",
                f"{first_year} to {last_year}",
                ORANGE
            )

        st.divider()

        # ----------------------------------------------------
        # VISUALIZATION 3.1: HEATMAP
        # ----------------------------------------------------

        st.subheader("Visualization 3.1: Heatmap")

        st.write(
            "Compare population across the 10 selected districts "
            "from 2020 to 2024."
        )

        latest_population = population_view[
            population_view["year"] == last_year
        ].sort_values(
            "population",
            ascending=False
        )

        top10_labels = latest_population[
            "district_label"
        ].head(10).tolist()

        heatmap_data = population_view[
            population_view["district_label"].isin(top10_labels)
        ].pivot_table(
            index="district_label",
            columns="year",
            values="population",
            aggfunc="mean"
        )

        heatmap_data = heatmap_data.reindex(
            top10_labels
        )

        fig_heatmap = px.imshow(
            heatmap_data,
            aspect="auto",
            color_continuous_scale="YlGnBu",
            labels={
                "x": "Year",
                "y": "District",
                "color": "Population"
            },
            title="Population Heatmap of Top 10 Districts (2020–2024)"
        )

        fig_heatmap.update_layout(
            **chart_theme,
            height=550,
            title=dict(
                text="<b>Population Distribution Heatmap</b>",
                x=0.5,
                font=dict(size=18, color=NAVY)
            ),
            margin=dict(l=180, r=70, t=90, b=80)
        )

        st.plotly_chart(
            fig_heatmap,
            use_container_width=True
        )

        # ----------------------------------------------------
        # VISUALIZATION 3.2: BOX PLOT
        # ----------------------------------------------------

        st.divider()

        st.subheader("Visualization 3.2: Box Plot")

        st.write(
            "Examine population distribution and variation "
            "across all available districts by year."
        )

        fig_box = px.box(
            population_view,
            x="year",
            y="population",
            color="year",
            points="outliers",
            color_discrete_sequence=[
                "#3984D6",
                "#16B8A6",
                "#F59E0B",
                "#8E65C5",
                "#E76F51"
            ],
            labels={
                "year": "Year",
                "population": "Population"
            },
            title="Population Distribution Across Districts (2020–2024)"
        )

        fig_box.update_layout(
            **chart_theme,
            height=600,
            showlegend=False,
            title=dict(
                text="<b>Population Distribution by Year</b>",
                x=0.5,
                font=dict(size=18, color=NAVY)
            ),
            margin=dict(l=100, r=70, t=90, b=80)
        )

        fig_box.update_xaxes(
            title="Year",
            showline=True,
            linewidth=2,
            linecolor="black",
            mirror=True,
            dtick=1,
            showgrid=True,
            gridcolor="#DCE3EA"
        )

        fig_box.update_yaxes(
            title="Population",
            tickformat=",.0f",
            showline=True,
            linewidth=2,
            linecolor="black",
            mirror=True,
            showgrid=True,
            gridcolor="#DCE3EA"
        )

        st.plotly_chart(
            fig_box,
            use_container_width=True
        )

        # ----------------------------------------------------
        # VISUALIZATION 3.3: LINE CHART
        # ----------------------------------------------------

        st.divider()

        st.subheader("Visualization 3.3: Line Chart")

        st.write(
            "Identify population increases and decreases "
            "in the 10 selected districts."
        )

        line_data = population_view[
            population_view["district_label"].isin(top10_labels)
        ].copy()

        fig_line = px.line(
            line_data,
            x="year",
            y="population",
            color="district_label",
            markers=True,
            labels={
                "year": "Year",
                "population": "Population",
                "district_label": "District"
            },
            title="Population Trends in Top 10 Districts (2020–2024)"
        )

        fig_line.update_traces(
            line=dict(width=2.5),
            marker=dict(size=7)
        )

        fig_line.update_layout(
            **chart_theme,
            height=650,
            title=dict(
                text="<b>Population Trends by District</b>",
                x=0.5,
                font=dict(size=18, color=NAVY)
            ),
            legend=dict(
                title="District",
                orientation="v",
                x=1.02,
                y=0.5,
                yanchor="middle"
            ),
            margin=dict(l=100, r=190, t=90, b=80)
        )

        fig_line.update_xaxes(
            title="Year",
            dtick=1,
            showline=True,
            linewidth=2,
            linecolor="black",
            mirror=True,
            showgrid=True,
            gridcolor="#DCE3EA"
        )

        fig_line.update_yaxes(
            title="Population",
            tickformat=",.0f",
            showline=True,
            linewidth=2,
            linecolor="black",
            mirror=True,
            showgrid=True,
            gridcolor="#DCE3EA"
        )

        st.plotly_chart(
            fig_line,
            use_container_width=True
        )

        # ----------------------------------------------------
        # POPULATION INTERPRETATION
        # ----------------------------------------------------

        st.divider()

        st.subheader("Interpretation and Discussion")

        if population_change > 0:
            trend_word = "increased"
        elif population_change < 0:
            trend_word = "decreased"
        else:
            trend_word = "remained unchanged"

        st.markdown(f"""
        The heatmap highlights population differences
        among the 10 selected districts across the
        available years from 2020 to 2024.

        The box plot illustrates the distribution,
        median and variation of population values
        across districts for each year. Individual
        outliers indicate districts with population
        values that differ considerably from the
        overall distribution.

        The line chart shows changes in population
        across the 10 selected districts over time.
        The combined population of the available
        district records {trend_word} by
        {abs(population_change):,.0f} between
        {first_year} and {last_year}
        ({percentage_change:+.2f}%).

        These patterns help explain differences in
        population distribution across Malaysia and
        may support planning for public facilities
        and infrastructure.
        """)

        with st.expander("View Detailed Population Data"):

            st.dataframe(
                population_view.sort_values(
                    ["state", "district", "year"]
                ),
                use_container_width=True,
                hide_index=True
            )

    else:

        st.warning(
            "No valid population records found for 2020–2024."
        )


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
MALAYSIA DATA INSIGHTS
</h4>

JIE42403 | Scientific Visualization

<br>

Household Income, Poverty and Population Analysis

<br>

2020–2024 | Malaysia

</div>
""", unsafe_allow_html=True)
