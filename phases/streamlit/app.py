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
def run_query(query: str) -> pd.DataFrame:
    conn = connect(
        s3_staging_dir=S3_STAGING_DIR,
        region_name=REGION,
        schema_name=DATABASE
    )
    return pd.read_sql(query, conn)

campaign_df = run_query("SELECT * FROM gold_campaign_performance")
daily_df = run_query("SELECT * FROM gold_daily_booking_trends")
employee_df = run_query("SELECT * FROM gold_employee_performance")
cpb_df = run_query("SELECT * FROM gold_channel_cpb")

campaign_df["booking_date"] = pd.to_datetime(campaign_df["booking_date"])
daily_df["meeting_date"] = pd.to_datetime(daily_df["meeting_date"])
cpb_df["report_date"] = pd.to_datetime(cpb_df["report_date"])

st.title("📊 Calendly Marketing Insights Dashboard")
st.caption("Marketing bookings, campaign performance, CPB, booking trends, and employee meeting load")

all_channels = sorted(cpb_df["channel"].dropna().unique())

st.sidebar.header("Filters")

selected_channels = st.sidebar.multiselect(
    "Select Channel",
    options=all_channels,
    default=all_channels
)

min_date = cpb_df["report_date"].min()
max_date = cpb_df["report_date"].max()

selected_date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_date_range) == 2:
    start_date, end_date = selected_date_range

    cpb_df = cpb_df[
        (cpb_df["report_date"].dt.date >= start_date) &
        (cpb_df["report_date"].dt.date <= end_date)
    ]

    campaign_df = campaign_df[
        (campaign_df["booking_date"].dt.date >= start_date) &
        (campaign_df["booking_date"].dt.date <= end_date)
    ]

    daily_df = daily_df[
        (daily_df["meeting_date"].dt.date >= start_date) &
        (daily_df["meeting_date"].dt.date <= end_date)
    ]

cpb_df = cpb_df[cpb_df["channel"].isin(selected_channels)]
campaign_df = campaign_df[campaign_df["channel"].isin(selected_channels)]
daily_df = daily_df[daily_df["channel"].isin(selected_channels)]
employee_df = employee_df[employee_df["channel"].isin(selected_channels)]

total_bookings = int(cpb_df["total_bookings"].sum()) if not cpb_df.empty else 0
unique_leads = int(cpb_df["unique_leads"].sum()) if not cpb_df.empty else 0
total_spend = round(float(cpb_df["total_spend"].sum()), 2) if not cpb_df.empty else 0
avg_cpb = round(total_spend / total_bookings, 2) if total_bookings > 0 else 0

top_channel = (
    cpb_df.groupby("channel")["total_bookings"].sum().idxmax()
    if not cpb_df.empty and cpb_df["total_bookings"].sum() > 0
    else "N/A"
)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Bookings", total_bookings)
col2.metric("Unique Leads", unique_leads)
col3.metric("Total Spend", f"${total_spend:,.2f}")
col4.metric("Avg CPB", f"${avg_cpb:,.2f}")
col5.metric("Top Channel", top_channel)

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Campaign Performance",
    "💰 Cost Per Booking",
    "📅 Booking Trends",
    "👥 Employee Load"
])

with tab1:
    st.header("Daily Calls Booked by Source")

    campaign_summary = (
        campaign_df
        .groupby(["booking_date", "channel"], as_index=False)
        .agg(total_bookings=("total_bookings", "sum"))
        .sort_values("booking_date")
    )

    if campaign_summary.empty:
        st.warning("No campaign data available for selected filters.")
    else:
        fig_daily_source = px.line(
            campaign_summary,
            x="booking_date",
            y="total_bookings",
            color="channel",
            markers=True,
            title="Daily Calls Booked by Source"
        )
        st.plotly_chart(fig_daily_source, use_container_width=True)

        channel_summary = (
            campaign_df
            .groupby("channel", as_index=False)
            .agg(
                total_bookings=("total_bookings", "sum"),
                unique_leads=("unique_leads", "sum"),
                unique_events=("unique_events", "sum")
            )
            .sort_values("total_bookings", ascending=False)
        )

        fig_channel = px.bar(
            channel_summary,
            x="channel",
            y="total_bookings",
            color="channel",
            text="total_bookings",
            title="Total Bookings by Channel"
        )
        fig_channel.update_traces(textposition="outside")
        st.plotly_chart(fig_channel, use_container_width=True)

        st.dataframe(channel_summary, use_container_width=True)

with tab2:
    st.header("Cost Per Booking by Channel")

    cpb_summary = (
        cpb_df
        .groupby("channel", as_index=False)
        .agg(
            total_bookings=("total_bookings", "sum"),
            unique_leads=("unique_leads", "sum"),
            total_spend=("total_spend", "sum")
        )
    )

    if cpb_summary.empty:
        st.warning("No CPB data available for selected filters.")
    else:
        cpb_summary["cpb"] = cpb_summary.apply(
            lambda row: round(row["total_spend"] / row["total_bookings"], 2)
            if row["total_bookings"] > 0 else None,
            axis=1
        )

        fig_cpb = px.bar(
            cpb_summary,
            x="channel",
            y="cpb",
            color="channel",
            text="cpb",
            title="Cost Per Booking by Channel"
        )
        fig_cpb.update_traces(textposition="outside")
        st.plotly_chart(fig_cpb, use_container_width=True)

        fig_spend = px.bar(
            cpb_summary,
            x="channel",
            y="total_spend",
            color="channel",
            text="total_spend",
            title="Total Spend by Channel"
        )
        fig_spend.update_traces(textposition="outside")
        st.plotly_chart(fig_spend, use_container_width=True)

        leaderboard = cpb_summary.sort_values(["cpb", "total_bookings"], ascending=[True, False])
        st.subheader("Channel Attribution Leaderboard")
        st.dataframe(leaderboard, use_container_width=True)

with tab3:
    st.header("Bookings Trend Over Time")

    if daily_df.empty:
        st.warning("No booking trend data available for selected filters.")
    else:
        trend_df = (
            daily_df
            .groupby(["meeting_date", "channel"], as_index=False)
            .agg(total_bookings=("total_bookings", "sum"))
            .sort_values("meeting_date")
        )

        fig_trend = px.line(
            trend_df,
            x="meeting_date",
            y="total_bookings",
            color="channel",
            markers=True,
            title="Bookings Trend Over Time"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        hourly_df = (
            daily_df
            .groupby(["meeting_hour", "channel"], as_index=False)
            .agg(total_bookings=("total_bookings", "sum"))
            .sort_values("meeting_hour")
        )

        fig_hour = px.bar(
            hourly_df,
            x="meeting_hour",
            y="total_bookings",
            color="channel",
            text="total_bookings",
            title="Booking Volume by Hour"
        )
        fig_hour.update_traces(textposition="outside")
        st.plotly_chart(fig_hour, use_container_width=True)

        heatmap_df = (
            daily_df
            .groupby(["meeting_day_of_week", "meeting_hour"], as_index=False)
            .agg(total_bookings=("total_bookings", "sum"))
        )

        fig_heatmap = px.density_heatmap(
            heatmap_df,
            x="meeting_hour",
            y="meeting_day_of_week",
            z="total_bookings",
            title="Booking Volume Heatmap: Hour vs Day of Week"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

        st.dataframe(daily_df, use_container_width=True)

with tab4:
    st.header("Meeting Load per Employee")

    if employee_df.empty:
        st.warning("No employee data available for selected filters.")
    else:
        employee_summary = (
            employee_df
            .groupby(["employee_name", "employee_email"], as_index=False)
            .agg(
                total_meetings=("total_meetings", "sum"),
                unique_leads=("unique_leads", "sum")
            )
            .sort_values("total_meetings", ascending=False)
        )

        employee_summary["avg_meetings_per_week"] = employee_summary["total_meetings"]

        emp_col1, emp_col2, emp_col3 = st.columns(3)
        emp_col1.metric("Total Meetings", int(employee_summary["total_meetings"].sum()))
        emp_col2.metric("Max Meetings", int(employee_summary["total_meetings"].max()))
        emp_col3.metric("Min Meetings", int(employee_summary["total_meetings"].min()))

        fig_employee = px.bar(
            employee_summary,
            x="employee_name",
            y="avg_meetings_per_week",
            text="avg_meetings_per_week",
            title="Average Meetings per Week by Employee"
        )
        fig_employee.update_traces(textposition="outside")
        st.plotly_chart(fig_employee, use_container_width=True)

        st.dataframe(employee_summary, use_container_width=True)

st.divider()

with st.expander("Raw Gold Tables"):
    st.subheader("Gold Channel CPB")
    st.dataframe(cpb_df, use_container_width=True)

    st.subheader("Gold Campaign Performance")
    st.dataframe(campaign_df, use_container_width=True)

    st.subheader("Gold Daily Booking Trends")
    st.dataframe(daily_df, use_container_width=True)

    st.subheader("Gold Employee Performance")
    st.dataframe(employee_df, use_container_width=True)
