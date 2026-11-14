
import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Kedah District Visualization",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# LOAD DATASETS
# ==========================================

@st.cache_data
def load_data():

    income_df = pd.read_csv("kedah_merged_2024.csv")

    population_df = pd.read_csv(
        "kedah_population_2020_2024.csv"
    )

    return income_df, population_df


try:
    df_income, df_population = load_data()

except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()


# ==========================================
# TITLE
# ==========================================

st.title("📊 Kedah District Visualization")

st.markdown(
    "### Scientific Visualization of Household Income, "
    "Poverty and Population in Kedah"
)

st.markdown(
    "This dashboard analyzes household income, "
    "poverty and population patterns across districts in Kedah."
)

st.divider()


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Visualization",
    [
        "Dashboard Overview",
        "Objective 1 - Household Income",
        "Objective 2 - Income and Poverty",
        "Objective 3 - Population"
    ]
)


# ==========================================
# PREPARE INCOME DATA
# ==========================================

if "state" in df_income.columns:
    df_income["state"] = df_income["state"].astype(str).str.strip()

if "district" in df_income.columns:
    df_income["district"] = df_income["district"].astype(str).str.strip()

# Filter Kedah
if "state" in df_income.columns:
    df_income = df_income[
        df_income["state"].str.lower() == "kedah"
    ].copy()

df_income = df_income.dropna(
    subset=["district"]
)

df_income["District"] = df_income["district"]


# ==========================================
# PREPARE POPULATION DATA
# ==========================================

df_population["district"] = (
    df_population["district"].astype(str).str.strip()
)

if "state" in df_population.columns:
    df_population["state"] = (
        df_population["state"].astype(str).str.strip()
    )

    df_population = df_population[
        df_population["state"].str.lower() == "kedah"
    ].copy()

if "year" not in df_population.columns:
    if "date" in df_population.columns:
        df_population["year"] = pd.to_datetime(
            df_population["date"]
        ).dt.year
    else:
        st.error("Population dataset has no year or date column.")
        st.stop()

df_population["year"] = pd.to_numeric(
    df_population["year"], errors="coerce"
)

df_population["population"] = pd.to_numeric(
    df_population["population"], errors="coerce"
)

df_population = df_population[
    df_population["year"].between(2020, 2024)
].copy()

df_population["District"] = df_population["district"]


# ==========================================
# DASHBOARD OVERVIEW
# ==========================================

if page == "Dashboard Overview":

    st.header("Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Study Area",
        "Kedah"
    )

    col2.metric(
        "Income Data Year",
        "2024"
    )

    col3.metric(
        "Population Period",
        "2020–2024"
    )

    st.divider()

    st.subheader("Research Objectives")

    st.markdown("""
    **Objective 1**

    To analyze differences in mean household income
    across districts in Kedah in 2024.

    **Objective 2**

    To examine the relationship between mean household
    income and absolute poverty rates across districts
    in Kedah in 2024.

    **Objective 3**

    To analyze population distribution patterns and
    changes across districts in Kedah from 2020 to 2024.
    """)


# ==========================================
# OBJECTIVE 1 - HOUSEHOLD INCOME
# ==========================================

elif page == "Objective 1 - Household Income":

    st.header("Objective 1: Household Income")

    st.write(
        "Analysis of mean household income across "
        "districts in Kedah (2024)."
    )

    data1 = df_income.dropna(
        subset=["income_mean"]
    ).copy()

    data1["income_mean"] = pd.to_numeric(
        data1["income_mean"], errors="coerce"
    )

    data1 = data1.dropna(subset=["income_mean"])

    data1 = data1.groupby(
        "District", as_index=False
    )["income_mean"].mean()

    data1 = data1.sort_values(
        "income_mean", ascending=True
    )

    if not data1.empty:

        highest = data1.iloc[-1]
        lowest = data1.iloc[0]

        c1, c2 = st.columns(2)

        c1.metric(
            "Highest Mean Income",
            f"RM {highest['income_mean']:,.2f}",
            highest["District"]
        )

        c2.metric(
            "Lowest Mean Income",
            f"RM {lowest['income_mean']:,.2f}",
            lowest["District"]
        )

        fig1 = px.bar(
            data1,
            x="income_mean",
            y="District",
            orientation="h",
            color="income_mean",
            color_continuous_scale="Blues",
            labels={
                "income_mean": "Mean Household Income (RM)",
                "District": "District"
            },
            title="Mean Household Income by District in Kedah (2024)"
        )

        fig1.update_layout(
            template="plotly_white",
            height=550,
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        st.subheader("Interpretation")

        st.write(
            "The bar chart compares mean household income "
            "across districts in Kedah. The highest and lowest "
            "values show the differences in household income "
            "between districts."
        )

        st.dataframe(data1, use_container_width=True)


# ==========================================
# OBJECTIVE 2 - INCOME AND POVERTY
# ==========================================

elif page == "Objective 2 - Income and Poverty":

    st.header("Objective 2: Income and Poverty")

    st.write(
        "Relationship between mean household income "
        "and absolute poverty across districts in Kedah (2024)."
    )

    data2 = df_income.dropna(
        subset=["income_mean", "poverty_absolute"]
    ).copy()

    data2["income_mean"] = pd.to_numeric(
        data2["income_mean"], errors="coerce"
    )

    data2["poverty_absolute"] = pd.to_numeric(
        data2["poverty_absolute"], errors="coerce"
    )

    data2 = data2.dropna(
        subset=["income_mean", "poverty_absolute"]
    )

    data2 = data2.groupby(
        "District", as_index=False
    )[
        ["income_mean", "poverty_absolute"]
    ].mean()

    if len(data2) >= 2:

        correlation = data2[
            ["income_mean", "poverty_absolute"]
        ].corr().iloc[0, 1]

        st.metric(
            "Pearson Correlation",
            f"{correlation:.3f}"
        )

        fig2 = px.scatter(
            data2,
            x="income_mean",
            y="poverty_absolute",
            hover_name="District",
            trendline="ols",
            color="poverty_absolute",
            color_continuous_scale="RdYlBu_r",
            labels={
                "income_mean": "Mean Household Income (RM)",
                "poverty_absolute": "Absolute Poverty Rate (%)"
            },
            title="Relationship Between Household Income and Absolute Poverty (2024)"
        )

        fig2.update_traces(
            marker=dict(
                size=13,
                line=dict(width=1, color="black")
            ),
            selector=dict(mode="markers")
        )

        fig2.update_layout(
            template="plotly_white",
            height=550
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.subheader("Interpretation")

        st.write(
            "The scatter plot illustrates the relationship "
            "between mean household income and absolute "
            "poverty rates across districts. The direction "
            "of the trendline and Pearson correlation "
            "indicate the strength and direction of the "
            "linear relationship."
        )

        st.dataframe(data2, use_container_width=True)

    else:
        st.warning("Not enough valid observations for correlation analysis.")


# ==========================================
# OBJECTIVE 3 - POPULATION
# ==========================================

elif page == "Objective 3 - Population":

    st.header("Objective 3: Population Distribution")

    st.write(
        "Population distribution and changes across "
        "districts in Kedah (2020–2024)."
    )

    data3 = df_population.dropna(
        subset=["District", "year", "population"]
    ).copy()

    data3 = data3.groupby(
        ["District", "year"],
        as_index=False
    )["population"].mean()

    pivot = data3.pivot(
        index="District",
        columns="year",
        values="population"
    )

    pivot = pivot.reindex(
        columns=[2020, 2021, 2022, 2023, 2024]
    )

    if not pivot.empty:

        fig3 = px.imshow(
            pivot,
            color_continuous_scale="YlGnBu",
            aspect="auto",
            labels={
                "x": "Year",
                "y": "District",
                "color": "Population"
            },
            title="Population Distribution by District in Kedah (2020–2024)"
        )

        fig3.update_layout(
            template="plotly_white",
            height=500
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        st.subheader("Interpretation")

        st.write(
            "The heatmap presents population distribution "
            "across districts in Kedah over five years. "
            "Differences in colour intensity represent "
            "variations in population size between "
            "districts and across the study period."
        )

        st.dataframe(
            data3,
            use_container_width=True
        )

    else:
        st.warning("No population records available.")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Scientific Visualization | Household Income, "
    "Poverty and Population in Kedah | 2020–2024"
)

