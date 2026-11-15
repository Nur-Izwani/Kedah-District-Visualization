
# ============================================================
# PAGE 3: VISUALIZATION 2 - POVERTY AND INCOME
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

    # --------------------------------------------------------
    # FILTER DATA
    # --------------------------------------------------------
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

    # --------------------------------------------------------
    # SUMMARY BOXES
    # --------------------------------------------------------
    s1, s2, s3 = st.columns(3, gap="large")

    with s1:
        summary_card(
            ":material/trending_down: Relationship",
            "Negative correlation",
            "Higher poverty is associated with lower income",
            BLUE
        )

    with s2:
        summary_card(
            ":material/bar_chart: Poverty Rate 0%–15%",
            "Income around RM4,000–RM8,000",
            "Observed income range for districts in this group",
            TEAL
        )

    with s3:
        summary_card(
            ":material/warning: Poverty Rate Above 30%",
            "Income around RM3,000–RM5,000",
            "Observed income range for districts in this group",
            ORANGE
        )

    # --------------------------------------------------------
    # GRAPH: SCATTER PLOT WITH TRENDLINE
    # --------------------------------------------------------
    st.markdown(
        "### :material/search: Absolute Poverty vs Mean Household Income"
    )

    fig2 = px.scatter(
        poverty_view,
        x="poverty_absolute",
        y="income_mean",
        color="year_label",
        trendline="ols",
        trendline_scope="trace",
        hover_name="district_label",
        hover_data={
            "state": True,
            "district": True,
            "year_label": True,
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
    # INTERPRETATION AND DISCUSSION
    # --------------------------------------------------------
    st.markdown(
        "### :material/description: Interpretation and Discussion"
    )

    correlation = poverty_view[
        ["poverty_absolute", "income_mean"]
    ].corr().iloc[0, 1]

    if pd.isna(correlation):
        correlation_point = (
            "The correlation could not be calculated from the selected data."
        )
    elif correlation < 0:
        correlation_point = (
            f"The Pearson correlation value of {correlation:.3f} "
            "shows a negative relationship between absolute poverty "
            "and mean household income."
        )
    elif correlation > 0:
        correlation_point = (
            f"The Pearson correlation value of {correlation:.3f} "
            "shows a positive relationship between absolute poverty "
            "and mean household income."
        )
    else:
        correlation_point = (
            "The Pearson correlation value of 0 indicates no linear relationship."
        )

    interpretation_points = [
        correlation_point,
        "Both 2022 and 2024 show the relationship between absolute poverty rates and mean household income.",
        "Most districts with poverty rates between 0% and 15% recorded mean household income around RM4,000–RM8,000.",
        "Districts with poverty rates above 30% generally recorded lower mean household income, around RM3,000–RM5,000.",
        "The downward trendline indicates that districts with higher poverty rates tend to have lower household income.",
        "This finding shows an association between poverty and household income, but it does not prove that one directly causes the other."
    ]

    interpretation_box(interpretation_points)

    # --------------------------------------------------------
    # DATA TABLE
    # --------------------------------------------------------
    with st.expander(":material/table_view: View poverty and income data"):

        st.dataframe(
            poverty_view[
                [
                    "state",
                    "district",
                    "year",
                    "income_mean",
                    "poverty_absolute"
                ]
            ].sort_values(
                ["state", "district", "year"]
            ),
            use_container_width=True,
            hide_index=True
        )
