import streamlit as st
from snowflake.snowpark.context import get_active_session

# Connect to Snowflake session
session = get_active_session()

# FORCE THE CORRECT DATABASE CONTEXT
session.sql("USE DATABASE ECOMMERCE_PROJECT_DB;").collect()

st.title("Snowflake Executive Sales Analytics Dashboard")
st.markdown(
    "Interactive Snowflake-powered analytics dashboard for monitoring revenue trends, customer behavior, order performance, and business KPIs."
)
# ----------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------
st.sidebar.title("🔍 Dashboard Filters")

# Get available years
year_query = """
SELECT DISTINCT YEAR(O_ORDERDATE) AS ORDER_YEAR
FROM SILVER.ORDERS_INCREMENTAL
ORDER BY ORDER_YEAR;
"""

year_df = session.sql(year_query).to_pandas()

selected_year = st.sidebar.selectbox(
    "Select Year",
    year_df["ORDER_YEAR"]
)
# ----------------------------------------------------
# KPI METRICS
# ----------------------------------------------------

kpi_query = f"""
SELECT
    COUNT(*) AS TOTAL_ORDERS,
    ROUND(SUM(O_TOTALPRICE),2) AS TOTAL_REVENUE,
    ROUND(AVG(O_TOTALPRICE),2) AS AVG_ORDER_VALUE,
    MAX(O_TOTALPRICE) AS HIGHEST_ORDER

FROM SILVER.ORDERS_INCREMENTAL

WHERE YEAR(O_ORDERDATE) = {int(selected_year)}
"""

kpi_df = session.sql(kpi_query).to_pandas()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📦 Total Orders",
    int(kpi_df["TOTAL_ORDERS"][0])
)

col2.metric(
    "💰 Total Revenue",
    f"${kpi_df['TOTAL_REVENUE'][0]:,.0f}"
)

col3.metric(
    "📈 Avg Order Value",
    f"${kpi_df['AVG_ORDER_VALUE'][0]:,.0f}"
)

col4.metric(
    "🏆 Highest Order",
    f"${kpi_df['HIGHEST_ORDER'][0]:,.0f}"
)
# ----------------------------------------------------
# SIDE-BY-SIDE CHARTS
# ----------------------------------------------------

col1, col2 = st.columns(2)

# ----------------------------------------------------
# CHART 1: Monthly Revenue Trend
# ----------------------------------------------------

with col1:

    st.subheader("📆 Monthly Revenue Trends")

    query_1 = f"""
    SELECT
        YEAR(O_ORDERDATE) AS ORDER_YEAR,
        MONTH(O_ORDERDATE) AS ORDER_MONTH,
        ROUND(SUM(O_TOTALPRICE), 2) AS MONTHLY_REVENUE

    FROM SILVER.ORDERS_INCREMENTAL

    WHERE YEAR(O_ORDERDATE) = {int(selected_year)}

    GROUP BY YEAR(O_ORDERDATE), MONTH(O_ORDERDATE)

    ORDER BY ORDER_YEAR, ORDER_MONTH;
    """

    df_1 = session.sql(query_1).to_pandas()

    st.line_chart(
        data=df_1,
        x="ORDER_MONTH",
        y="MONTHLY_REVENUE"
    )

# ----------------------------------------------------
# CHART 2: Weekly Sales Trend
# ----------------------------------------------------

with col2:

    st.subheader("📈 Weekly Sales Trend")

    query_4 = f"""
    SELECT
        WEEK(O_ORDERDATE) AS ORDER_WEEK,
        ROUND(SUM(O_TOTALPRICE), 2) AS WEEKLY_REVENUE

    FROM SILVER.ORDERS_INCREMENTAL

    WHERE YEAR(O_ORDERDATE) = {int(selected_year)}

    GROUP BY WEEK(O_ORDERDATE)

    ORDER BY ORDER_WEEK;
    """

    df_4 = session.sql(query_4).to_pandas()

    st.line_chart(
        data=df_4,
        x="ORDER_WEEK",
        y="WEEKLY_REVENUE"
    )


# ----------------------------------------------------
# SIDE-BY-SIDE METRICS (Status and Top Customers)
# ----------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Revenue by Order Status")
    query_3 = f"""
SELECT
    O_ORDERSTATUS,
    ROUND(SUM(O_TOTALPRICE), 2) AS TOTAL_REVENUE

FROM SILVER.ORDERS_INCREMENTAL

WHERE YEAR(O_ORDERDATE) = {int(selected_year)}

GROUP BY O_ORDERSTATUS

ORDER BY TOTAL_REVENUE DESC;
"""
    df_3 = session.sql(query_3).to_pandas()
    st.bar_chart(data=df_3, x="O_ORDERSTATUS", y="TOTAL_REVENUE")

with col2:
    st.subheader("👥 Top 10 Customers")
    query_2 = f"""
SELECT
    O_CUSTKEY,
    ROUND(SUM(O_TOTALPRICE), 2) AS TOTAL_SPENT

FROM SILVER.ORDERS_INCREMENTAL

WHERE YEAR(O_ORDERDATE) = {int(selected_year)}

GROUP BY O_CUSTKEY

ORDER BY TOTAL_SPENT DESC

LIMIT 10;
"""
    df_2 = session.sql(query_2).to_pandas()
    st.dataframe(df_2, use_container_width=True)

# ----------------------------------------------------
# TABLE: Top 5 Highest Orders
# ----------------------------------------------------
st.subheader("🏆 Top 5 Highest Value Orders")
query_5 = f"""
SELECT
    O_ORDERKEY,
    O_CUSTKEY,
    O_TOTALPRICE

FROM SILVER.ORDERS_INCREMENTAL

WHERE YEAR(O_ORDERDATE) = {int(selected_year)}

ORDER BY O_TOTALPRICE DESC

LIMIT 5;
"""
df_5 = session.sql(query_5).to_pandas()
st.table(df_5)

st.markdown("---")
st.caption("Built using Snowflake, Snowpark, and Streamlit")