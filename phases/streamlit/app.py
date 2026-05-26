import pandas as pd
import plotly.express as px
import streamlit as st
from pyathena import connect

st.set_page_config(
    page_title="Calendly Marketing Insights",
    page_icon="📊",
    layout="wide"
)

DATABASE = "calendly_marketing_db"
S3_STAGING_DIR = "s3://calendly-marketing-athena-results/"
REGION = "us-east-1"

@st.cache_data(ttl=300)
def run_query(query):
    conn = connect(
        s3_staging_dir=S3_STAGING_DIR,
        region_name=REGION,
        schema_name=DATABASE
    )
    return pd.read_sql(query, conn)

st.title("📊 Calendly Marketing Insights Dashboard")
st.caption("Marketing bookings, campaign performance, and employee meeting load")

campaign_df = run_query("""
SELECT *
FROM calendly_marketing_db.gold_campaign_performance
""")

daily_df = run_query("""
SELECT *
FROM calendly_marketing_db.gold_daily_booking_trends
""")

employee_df = run_query("""
SELECT *
FROM calendly_marketing_db.gold_employee_performance
""")

total_bookings = int(campaign_df["total_bookings"].sum())
unique_leads = int(campaign_df["unique_leads"].sum())
top_channel = campaign_df.groupby("channel")["total_bookings"].sum().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("Total Bookings", total_bookings)
col2.metric("Unique Leads", unique_leads)
col3.metric("Top Channel", top_channel)

st.divider()

st.header("Campaign Performance")

fig_campaign = px.bar(
    campaign_df,
    x="channel",
    y="total_bookings",
    color="channel",
    title="Total Bookings by Channel"
)
st.plotly_chart(fig_campaign, use_container_width=True)

st.dataframe(campaign_df, use_container_width=True)

st.divider()

st.header("Daily Booking Trends")

fig_daily = px.line(
    daily_df,
    x="meeting_date",
    y="total_bookings",
    color="channel",
    markers=True,
    title="Bookings Trend Over Time"
)
st.plotly_chart(fig_daily, use_container_width=True)

fig_hour = px.bar(
    daily_df,
    x="meeting_hour",
    y="total_bookings",
    color="channel",
    title="Bookings by Hour"
)
st.plotly_chart(fig_hour, use_container_width=True)

st.dataframe(daily_df, use_container_width=True)

st.divider()

st.header("Employee Performance")

fig_employee = px.bar(
    employee_df,
    x="employee_name",
    y="total_meetings",
    color="channel",
    title="Meetings by Employee"
)
st.plotly_chart(fig_employee, use_container_width=True)

st.dataframe(employee_df, use_container_width=True)
