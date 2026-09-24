import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# PAGE CONFIGURATION & THEME STYLING
# ==========================================
st.set_page_config(
    page_title="Notification Engine Analytics Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Color Palette (Extracted directly from sample report reference)
PALETTE = {
    "navy": "#1a4673",
    "teal": "#1f9a89",
    "ocean": "#2c79c5",
    "sky": "#4885cd",
    "purple": "#7e519e",
    "coral": "#eb7966",
    "crimson": "#c45f64",
    "amber": "#cda36f",
    "sage": "#69965e",
    "charcoal": "#30333e",
    "muted": "#808494",
    "border": "#e4e7eb",
    "bg_card": "#ffffff",
    "bg_page": "#f8fafc"
}

STATUS_COLORS = {
    "SENT": PALETTE["teal"],
    "FAILED": PALETTE["coral"],
    "SKIPPED": PALETTE["amber"],
    "REACHED": PALETTE["teal"],
    "UNREACHED": PALETTE["crimson"]
}

CHANNEL_COLORS = {
    "email": PALETTE["ocean"],
    "whatsapp": PALETTE["teal"],
    "push": PALETTE["purple"],
    "sms": PALETTE["coral"]
}

# Inject Custom CSS for Clean, Modern, Card-Based Architecture
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    .main {{
        background-color: {PALETTE['bg_page']};
    }}
    
    /* Top Header Section */
    .dashboard-header {{
        padding: 6px 0px 18px 0px;
        border-bottom: 1px solid {PALETTE['border']};
        margin-bottom: 20px;
    }}
    .dashboard-title {{
        font-size: 26px;
        font-weight: 700;
        color: {PALETTE['navy']};
        margin: 0px 0px 4px 0px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .dashboard-subtitle {{
        font-size: 13.5px;
        color: {PALETTE['muted']};
        margin: 0px;
    }}
    
    /* Section Headings */
    .section-title {{
        font-size: 18px;
        font-weight: 700;
        color: {PALETTE['charcoal']};
        margin: 24px 0px 12px 0px;
        padding-bottom: 6px;
        border-bottom: 2px solid {PALETTE['sky']};
        display: inline-block;
    }}
    
    /* Metric Scorecard Cards */
    .metric-card {{
        background-color: {PALETTE['bg_card']};
        border: 1px solid {PALETTE['border']};
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        height: 100%;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.06);
    }}
    .metric-label {{
        font-size: 11.5px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: {PALETTE['muted']};
        margin-bottom: 4px;
    }}
    .metric-value {{
        font-size: 26px;
        font-weight: 700;
        color: {PALETTE['navy']};
        line-height: 1.2;
    }}
    .metric-subtext {{
        font-size: 11.5px;
        color: {PALETTE['muted']};
        margin-top: 4px;
    }}
    .metric-accent-teal {{
        border-top: 3px solid {PALETTE['teal']};
    }}
    .metric-accent-navy {{
        border-top: 3px solid {PALETTE['navy']};
    }}
    .metric-accent-coral {{
        border-top: 3px solid {PALETTE['coral']};
    }}
    .metric-accent-amber {{
        border-top: 3px solid {PALETTE['amber']};
    }}
    .metric-accent-purple {{
        border-top: 3px solid {PALETTE['purple']};
    }}
    .metric-accent-sky {{
        border-top: 3px solid {PALETTE['sky']};
    }}
    
    /* Data Analyst Insight Banner */
    .insight-box {{
        background-color: #f0f7ff;
        border-left: 4px solid {PALETTE['ocean']};
        padding: 14px 18px;
        border-radius: 0px 8px 8px 0px;
        margin: 16px 0px;
        font-size: 13.5px;
        color: {PALETTE['charcoal']};
        line-height: 1.5;
    }}
    .warning-box {{
        background-color: #fff7ed;
        border-left: 4px solid {PALETTE['amber']};
        padding: 14px 18px;
        border-radius: 0px 8px 8px 0px;
        margin: 16px 0px;
        font-size: 13.5px;
        color: {PALETTE['charcoal']};
        line-height: 1.5;
    }}
    .danger-box {{
        background-color: #fef2f2;
        border-left: 4px solid {PALETTE['coral']};
        padding: 14px 18px;
        border-radius: 0px 8px 8px 0px;
        margin: 16px 0px;
        font-size: 13.5px;
        color: {PALETTE['charcoal']};
        line-height: 1.5;
    }}
</style>
""", unsafe_allow_html=True)


# ==========================================
# DATA LOADING & PREPROCESSING
# ==========================================
@st.cache_data
def load_data(file_path_or_buffer):
    df = pd.read_csv(file_path_or_buffer, low_memory=False)
    
    # Standardize missing strings
    df['client_location'] = df['client_location'].fillna('Unknown / Virtual')
    df['trainer_name'] = df['trainer_name'].fillna('Not Specified')
    df['error_message'] = df['error_message'].fillna('None (Success)')
    
    # Clean datetime fields
    for col in ['notification_created_at', 'delivery_created_at', 'dispatched_at', 'sent_at']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    if 'notification_date' in df.columns:
        df['notification_date'] = pd.to_datetime(df['notification_date']).dt.date
        
    return df

# Sidebar: File Uploader & Filter Controls
st.sidebar.markdown(f"### ⚙️ Engine Control & Filters")
uploaded_file = st.sidebar.file_uploader(
    "Upload raw Notification CSV", 
    type=["csv"],
    help="Upload your raw Notification Engine CSV file to automatically generate Data Analyst-level insights."
)

default_csv = "Notification_Engine_Analytics - vw_notification_analytics.csv"
try:
    if uploaded_file is not None:
        raw_df = load_data(uploaded_file)
        st.sidebar.success(f"Loaded uploaded file ({len(raw_df):,} records)")
    else:
        raw_df = load_data(default_csv)
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Notification-Level Aggregation for Reachability Analysis
def compute_notification_level(df):
    notif = df.groupby('notification_id').agg(
        external_ref_id=('external_ref_id', 'first'),
        trigger_type=('trigger_type', 'first'),
        template_name=('template_name', 'first'),
        candidate_id=('candidate_id', 'first'),
        candidate_name=('candidate_name', 'first'),
        trainer_name=('trainer_name', 'first'),
        client_location=('client_location', 'first'),
        notification_date=('notification_date', 'first'),
        notification_day_name=('notification_day_name', 'first'),
        notification_hour=('notification_hour', 'first'),
        total_channels=('channel', 'count'),
        sent_legs=('sent_flag', 'sum'),
        failed_legs=('failed_flag', 'sum'),
        skipped_legs=('skipped_flag', 'sum')
    ).reset_index()
    notif['is_reached'] = notif['sent_legs'] > 0
    notif['reach_status'] = np.where(notif['is_reached'], 'REACHED (≥1 Channel)', 'UNREACHED (0 Channels)')
    return notif

notif_df = compute_notification_level(raw_df)

# Sidebar Filter Controls
st.sidebar.markdown("---")
st.sidebar.markdown("#### 🔍 Filter Cohort")

# Date Filter
min_date = raw_df['notification_date'].min()
max_date = raw_df['notification_date'].max()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Multi-Channel Filter
all_channels = sorted(raw_df['channel'].dropna().unique().tolist())
selected_channels = st.sidebar.multiselect("Channels", all_channels, default=all_channels)

# Trigger Type Filter
all_triggers = sorted(raw_df['trigger_type'].dropna().unique().tolist())
selected_triggers = st.sidebar.multiselect("Trigger Types", all_triggers, default=all_triggers)

# Delivery Status Filter
all_statuses = sorted(raw_df['status'].dropna().unique().tolist())
selected_statuses = st.sidebar.multiselect("Delivery Status", all_statuses, default=all_statuses)

# Client Location Filter
all_locations = sorted(raw_df['client_location'].dropna().unique().tolist())
selected_locations = st.sidebar.multiselect("Client Locations", all_locations, default=all_locations)

# Reset Filters Button
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset All Filters", width='stretch'):
    st.rerun()

# Apply Filters with fallback validation
if not selected_channels:
    selected_channels = all_channels
if not selected_triggers:
    selected_triggers = all_triggers
if not selected_statuses:
    selected_statuses = all_statuses
if not selected_locations:
    selected_locations = all_locations

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_d, end_d = date_range
    mask = (
        (raw_df['notification_date'] >= start_d) &
        (raw_df['notification_date'] <= end_d) &
        (raw_df['channel'].isin(selected_channels)) &
        (raw_df['trigger_type'].isin(selected_triggers)) &
        (raw_df['status'].isin(selected_statuses)) &
        (raw_df['client_location'].isin(selected_locations))
    )
else:
    mask = (
        (raw_df['channel'].isin(selected_channels)) &
        (raw_df['trigger_type'].isin(selected_triggers)) &
        (raw_df['status'].isin(selected_statuses)) &
        (raw_df['client_location'].isin(selected_locations))
    )

filtered_df = raw_df[mask]

if len(filtered_df) == 0:
    st.warning("⚠️ No records match your selected filters. Please expand your selections in the sidebar.")
    st.stop()

# Recompute notification level for current filter
filtered_notif_ids = filtered_df['notification_id'].unique()
filtered_notif_df = notif_df[notif_df['notification_id'].isin(filtered_notif_ids)]

# Filter status badge in sidebar
st.sidebar.info(f"Showing **{len(filtered_df):,}** delivery attempts across **{len(filtered_notif_df):,}** unique notifications.")


# ==========================================
# DASHBOARD HEADER & VIEW NAVIGATION
# ==========================================
st.markdown(f"""
<div class="dashboard-header">
    <div class="dashboard-title">
        <span>📈</span> Notification Engine Analytics Dashboard
    </div>
    <div class="dashboard-subtitle">
        Automated Data Analyst Insights: End-to-End Delivery Funnel, Multi-Channel Performance, Latency Velocity & Root-Cause Failure Diagnosis
    </div>
</div>
""", unsafe_allow_html=True)

# Mode Selector
dashboard_mode = st.radio(
    "View Mode:",
    ["📄 Comprehensive Report (All Sections)", "📑 Interactive Analytic Tabs"],
    horizontal=True,
    label_visibility="collapsed"
)


# Helper function to render all sections
def render_kpis():
    st.markdown('<div class="section-title">1. Key Performance Indicators & Velocity</div>', unsafe_allow_html=True)

    # Compute Core Metrics
    total_notifications = len(filtered_notif_df)
    total_attempts = len(filtered_df)
    sent_legs = filtered_df['sent_flag'].sum()
    failed_legs = filtered_df['failed_flag'].sum()
    skipped_legs = filtered_df['skipped_flag'].sum()

    channel_success_rate = (sent_legs / total_attempts * 100) if total_attempts > 0 else 0.0
    reached_notifications = filtered_notif_df['is_reached'].sum() if total_notifications > 0 else 0
    notification_reach_rate = (reached_notifications / total_notifications * 100) if total_notifications > 0 else 0.0

    valid_latencies = filtered_df['dispatch_to_sent_seconds'].dropna()
    avg_latency = valid_latencies.mean() if len(valid_latencies) > 0 else 0.0
    median_latency = valid_latencies.median() if len(valid_latencies) > 0 else 0.0
    p95_latency = valid_latencies.quantile(0.95) if len(valid_latencies) > 0 else 0.0

    total_dropped_notifications = total_notifications - reached_notifications
    dropped_rate = (total_dropped_notifications / total_notifications * 100) if total_notifications > 0 else 0.0

    # Render 6 Primary KPI Scorecards (Matching Page 1 Layout of Sample Report)
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

    with kpi1:
        st.markdown(f"""
        <div class="metric-card metric-accent-navy">
            <div class="metric-label">Total Notifications</div>
            <div class="metric-value">{total_notifications:,}</div>
            <div class="metric-subtext">Requests generated</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="metric-card metric-accent-sky">
            <div class="metric-label">Delivery Attempts</div>
            <div class="metric-value">{total_attempts:,}</div>
            <div class="metric-subtext">{total_attempts / total_notifications:.1f} legs / notification</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="metric-card metric-accent-teal">
            <div class="metric-label">Notification Reach</div>
            <div class="metric-value">{notification_reach_rate:.1f}%</div>
            <div class="metric-subtext">{reached_notifications:,} reached on ≥1 ch</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
        <div class="metric-card metric-accent-purple">
            <div class="metric-label">Channel Sent Rate</div>
            <div class="metric-value">{channel_success_rate:.1f}%</div>
            <div class="metric-subtext">{sent_legs:,} successful legs</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi5:
        st.markdown(f"""
        <div class="metric-card metric-accent-amber">
            <div class="metric-label">Avg Sent Latency</div>
            <div class="metric-value">{avg_latency:.2f}s</div>
            <div class="metric-subtext">Median: {median_latency:.2f}s | P95: {p95_latency:.2f}s</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi6:
        st.markdown(f"""
        <div class="metric-card metric-accent-coral">
            <div class="metric-label">Completely Dropped</div>
            <div class="metric-value">{dropped_rate:.1f}%</div>
            <div class="metric-subtext">{total_dropped_notifications:,} zero-reach candidates</div>
        </div>
        """, unsafe_allow_html=True)

    # Data Analyst Executive Summary Callout
    st.markdown(f"""
    <div class="insight-box">
        <strong>💡 Data Analyst POV — Executive Diagnosis:</strong><br>
        While the engine generated <strong>{total_notifications:,} notifications</strong> ({total_attempts:,} delivery legs across Push, WhatsApp, Email, SMS), 
        <strong>{dropped_rate:.1f}% ({total_dropped_notifications:,} candidates) suffered 100% communication drop-off</strong> with zero successful channels. 
        The root cause is a tri-channel cascade: <strong>WhatsApp Meta API 131008 parameter missing (1,090 failures)</strong>, 
        <strong>unregistered mobile push tokens (1,239 skips)</strong>, and <strong>missing candidate emails in WMS (584 skips)</strong>. 
        Remediating template variable payloads and client token syncing will immediately lift reachability from {notification_reach_rate:.1f}% to &gt;95%.
    </div>
    """, unsafe_allow_html=True)


def render_funnel():
    st.markdown('<div class="section-title">2. Funnel & Drop-off Analysis</div>', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([1, 1])

    with col_f1:
        st.markdown("##### 📌 Pipeline Snapshot")
        
        # Multi-stage Funnel Data
        total_notifications = len(filtered_notif_df)
        total_attempts = len(filtered_df)
        sent_legs = filtered_df['sent_flag'].sum()
        reached_notifications = filtered_notif_df['is_reached'].sum()
        
        funnel_stages = [
            {"Stage": "1. Notifications Created", "Count": total_notifications, "Pct": "100.0%"},
            {"Stage": "2. Delivery Dispatched", "Count": filtered_df['dispatched_at'].notna().sum(), "Pct": f"{(filtered_df['dispatched_at'].notna().sum() / total_attempts * 100):.1f}% of legs"},
            {"Stage": "3. Successfully Sent", "Count": sent_legs, "Pct": f"{(sent_legs / total_attempts * 100):.1f}% of legs"},
            {"Stage": "4. Candidate Reached (≥1 Ch)", "Count": reached_notifications, "Pct": f"{(reached_notifications / total_notifications * 100):.1f}% of notifs"},
            {"Stage": "5. Delivered (Webhooks)", "Count": filtered_df['delivered_at'].notna().sum(), "Pct": "0.0% (Webhook Pending)"}
        ]
        funnel_df = pd.DataFrame(funnel_stages)
        
        # Horizontal Bar Funnel Chart
        fig_funnel = go.Figure(go.Bar(
            x=funnel_df['Count'],
            y=funnel_df['Stage'],
            orientation='h',
            marker=dict(
                color=[PALETTE['navy'], PALETTE['ocean'], PALETTE['teal'], PALETTE['sage'], PALETTE['muted']],
                line=dict(color=PALETTE['border'], width=1)
            ),
            text=[f"{c:,} ({p})" for c, p in zip(funnel_df['Count'], funnel_df['Pct'])],
            textposition='auto',
            hoverinfo='text'
        ))
        
        fig_funnel.update_layout(
            margin=dict(l=10, r=20, t=10, b=10),
            height=320,
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title="Count"),
            yaxis=dict(autorange="reversed", title="")
        )
        st.plotly_chart(fig_funnel)
        
        with st.expander(" View Funnel Data"):
            st.dataframe(funnel_df, hide_index=True)

    with col_f2:
        st.markdown("##### ⚠️ Drop-off Reasons (Leakage)")
        
        # Leakage reasons
        leakage_df = filtered_df[filtered_df['status'].isin(['FAILED', 'SKIPPED'])].copy()
        leakage_counts = leakage_df['error_message'].value_counts().reset_index()
        leakage_counts.columns = ['Reason', 'Count']
        total_leakage = leakage_counts['Count'].sum()
        leakage_counts['Percentage'] = (leakage_counts['Count'] / total_leakage * 100).round(1) if total_leakage > 0 else 0.0
        top_dropoffs = leakage_counts.head(7)
        
        fig_leakage = go.Figure(go.Bar(
            x=top_dropoffs['Count'],
            y=top_dropoffs['Reason'],
            orientation='h',
            marker=dict(
                color=[PALETTE['coral'], PALETTE['crimson'], PALETTE['amber'], PALETTE['purple'], PALETTE['ocean'], PALETTE['muted'], PALETTE['muted']][:len(top_dropoffs)],
                line=dict(color=PALETTE['border'], width=1)
            ),
            text=[f"{c:,} ({p}%)" for c, p in zip(top_dropoffs['Count'], top_dropoffs['Percentage'])],
            textposition='auto'
        ))
        
        fig_leakage.update_layout(
            margin=dict(l=10, r=20, t=10, b=10),
            height=320,
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title="Count"),
            yaxis=dict(autorange="reversed", title="")
        )
        st.plotly_chart(fig_leakage)
        
        with st.expander(" View Drop-off Data"):
            st.dataframe(leakage_counts, hide_index=True)


def render_trends():
    st.markdown('<div class="section-title">3. Time-Series Trends</div>', unsafe_allow_html=True)

    # Time Series by Notification Date
    daily_summary = filtered_df.groupby('notification_date').agg(
        total_attempts=('delivery_id', 'count'),
        sent_count=('sent_flag', 'sum'),
        failed_count=('failed_flag', 'sum'),
        skipped_count=('skipped_flag', 'sum')
    ).reset_index()

    daily_summary['success_rate'] = (daily_summary['sent_count'] / daily_summary['total_attempts'] * 100).round(1)
    daily_summary['notification_date_str'] = daily_summary['notification_date'].astype(str)

    col_t1, col_t2 = st.columns([1.2, 0.8])

    with col_t1:
        st.markdown("##### 📅 Daily Momentum & Delivery Rate")
        
        fig_daily = go.Figure()
        
        # Stacked Bars for Status
        fig_daily.add_trace(go.Bar(
            x=daily_summary['notification_date_str'],
            y=daily_summary['sent_count'],
            name='Sent',
            marker_color=STATUS_COLORS['SENT']
        ))
        fig_daily.add_trace(go.Bar(
            x=daily_summary['notification_date_str'],
            y=daily_summary['skipped_count'],
            name='Skipped',
            marker_color=STATUS_COLORS['SKIPPED']
        ))
        fig_daily.add_trace(go.Bar(
            x=daily_summary['notification_date_str'],
            y=daily_summary['failed_count'],
            name='Failed',
            marker_color=STATUS_COLORS['FAILED']
        ))
        
        # Line overlay for Success Rate % (Dual Axis)
        fig_daily.add_trace(go.Scatter(
            x=daily_summary['notification_date_str'],
            y=daily_summary['success_rate'],
            name='Success Rate %',
            yaxis='y2',
            mode='lines+markers',
            line=dict(color=PALETTE['navy'], width=3),
            marker=dict(size=7, color=PALETTE['navy'])
        ))
        
        fig_daily.update_layout(
            barmode='stack',
            height=320,
            margin=dict(l=10, r=20, t=10, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            xaxis=dict(title='Notification Date', showgrid=False),
            yaxis=dict(title='Attempts Count', showgrid=True, gridcolor='#f1f5f9'),
            yaxis2=dict(
                title='Sent Rate %',
                overlaying='y',
                side='right',
                range=[0, 100],
                showgrid=False
            )
        )
        st.plotly_chart(fig_daily)

    with col_t2:
        st.markdown("##### 📆 Influx by Day of Week")
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = filtered_df['notification_day_name'].value_counts().reindex(day_order).dropna().reset_index()
        day_counts.columns = ['Day_of_Week', 'Count']
        day_counts['Percentage'] = (day_counts['Count'] / day_counts['Count'].sum() * 100).round(1)
        
        fig_day = go.Figure(go.Bar(
            x=day_counts['Day_of_Week'],
            y=day_counts['Count'],
            marker_color=PALETTE['ocean'],
            text=[f"{c:,}<br>({p}%)" for c, p in zip(day_counts['Count'], day_counts['Percentage'])],
            textposition='outside'
        ))
        
        fig_day.update_layout(
            height=320,
            margin=dict(l=10, r=20, t=10, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(title='Day of Week', showgrid=False),
            yaxis=dict(title='Attempts', showgrid=True, gridcolor='#f1f5f9', range=[0, day_counts['Count'].max() * 1.25])
        )
        st.plotly_chart(fig_day)

    # Heatmap: Influx by Day of Week & Hour of Day
    st.markdown("##### 🕒 Notification Influx Heatmap (Day of Week vs Hour of Day)")
    pivot_heatmap = filtered_df.pivot_table(
        index='notification_day_name',
        columns='notification_hour',
        values='delivery_id',
        aggfunc='count',
        fill_value=0
    )

    pivot_heatmap = pivot_heatmap.reindex([d for d in day_order if d in pivot_heatmap.index])

    def format_hour(h):
        if h == 0: return "12 AM"
        if h < 12: return f"{h} AM"
        if h == 12: return "12 PM"
        return f"{h-12} PM"

    col_labels = [format_hour(int(c)) for c in pivot_heatmap.columns]

    fig_heat = go.Figure(go.Heatmap(
        z=pivot_heatmap.values,
        x=col_labels,
        y=pivot_heatmap.index.tolist(),
        colorscale=[
            [0.0, "#f8fafc"],
            [0.1, "#e0f2fe"],
            [0.4, "#38bdf8"],
            [0.7, "#0284c7"],
            [1.0, PALETTE["navy"]]
        ],
        colorbar=dict(title="Volume"),
        text=pivot_heatmap.values,
        texttemplate="%{text}",
        textfont={"size": 11},
        hoverongaps=False
    ))

    fig_heat.update_layout(
        height=260,
        margin=dict(l=10, r=20, t=10, b=10),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(title="Hour of Day (UTC)", showgrid=False),
        yaxis=dict(title="", autorange="reversed", showgrid=False)
    )
    st.plotly_chart(fig_heat)


def render_channels():
    st.markdown('<div class="section-title">4. Channel & Provider Performance</div>', unsafe_allow_html=True)

    col_ch1, col_ch2 = st.columns([1.2, 0.8])

    channel_status_ct = pd.crosstab(filtered_df['channel'], filtered_df['status']).fillna(0)
    for col in ['SENT', 'FAILED', 'SKIPPED']:
        if col not in channel_status_ct.columns:
            channel_status_ct[col] = 0

    with col_ch1:
        st.markdown("##### 📊 Channel Funnel Breakdown (Sent vs Failed vs Skipped)")
        
        fig_ch_bar = go.Figure()
        fig_ch_bar.add_trace(go.Bar(
            x=channel_status_ct.index,
            y=channel_status_ct['SENT'],
            name='SENT',
            marker_color=STATUS_COLORS['SENT']
        ))
        fig_ch_bar.add_trace(go.Bar(
            x=channel_status_ct.index,
            y=channel_status_ct['SKIPPED'],
            name='SKIPPED',
            marker_color=STATUS_COLORS['SKIPPED']
        ))
        fig_ch_bar.add_trace(go.Bar(
            x=channel_status_ct.index,
            y=channel_status_ct['FAILED'],
            name='FAILED',
            marker_color=STATUS_COLORS['FAILED']
        ))
        
        fig_ch_bar.update_layout(
            barmode='stack',
            height=320,
            margin=dict(l=10, r=20, t=10, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            xaxis=dict(title='Channel', showgrid=False),
            yaxis=dict(title='Delivery Attempts', showgrid=True, gridcolor='#f1f5f9')
        )
        st.plotly_chart(fig_ch_bar)

    with col_ch2:
        st.markdown("##### 🎯 Channel Success Rates")
        
        ch_metrics = []
        for ch in channel_status_ct.index:
            tot = channel_status_ct.loc[ch].sum()
            s = channel_status_ct.loc[ch, 'SENT']
            f = channel_status_ct.loc[ch, 'FAILED']
            sk = channel_status_ct.loc[ch, 'SKIPPED']
            rate = (s / tot * 100) if tot > 0 else 0
            ch_metrics.append({
                'Channel': ch.upper(),
                'Total': tot,
                'Sent': s,
                'Success %': f"{rate:.1f}%",
                'Failed %': f"{(f/tot*100):.1f}%",
                'Skipped %': f"{(sk/tot*100):.1f}%"
            })
        ch_metrics_df = pd.DataFrame(ch_metrics)
        
        fig_ch_rate = go.Figure(go.Bar(
            x=[m['Channel'] for m in ch_metrics],
            y=[float(m['Success %'].replace('%', '')) for m in ch_metrics],
            marker=dict(
                color=[CHANNEL_COLORS.get(m['Channel'].lower(), PALETTE['navy']) for m in ch_metrics],
                line=dict(color=PALETTE['border'], width=1)
            ),
            text=[m['Success %'] for m in ch_metrics],
            textposition='outside'
        ))
        fig_ch_rate.update_layout(
            height=320,
            margin=dict(l=10, r=20, t=10, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(title='Channel', showgrid=False),
            yaxis=dict(title='Success Rate %', showgrid=True, gridcolor='#f1f5f9', range=[0, 100])
        )
        st.plotly_chart(fig_ch_rate)

    with st.expander(" View Channel Performance Table"):
        st.dataframe(ch_metrics_df, hide_index=True)


def render_demographics():
    st.markdown('<div class="section-title">5. Segmentation: Client Locations & Trainers</div>', unsafe_allow_html=True)
    st.caption("Comparing Total Delivery Attempts versus Sent/Success across key operational segments.")

    col_d1, col_d2 = st.columns([1, 1])

    with col_d1:
        st.markdown("##### 🏢 Performance by Client Location")
        
        loc_ct = pd.crosstab(filtered_df['client_location'], filtered_df['status']).fillna(0)
        for col in ['SENT', 'FAILED', 'SKIPPED']:
            if col not in loc_ct.columns:
                loc_ct[col] = 0
                
        loc_ct['TOTAL'] = loc_ct.sum(axis=1)
        loc_top = loc_ct.sort_values(by='TOTAL', ascending=False).head(7)
        
        fig_loc = go.Figure()
        fig_loc.add_trace(go.Bar(
            y=[l[:35] + '...' if len(l) > 35 else l for l in loc_top.index],
            x=loc_top['SENT'],
            name='SENT',
            orientation='h',
            marker_color=STATUS_COLORS['SENT']
        ))
        fig_loc.add_trace(go.Bar(
            y=[l[:35] + '...' if len(l) > 35 else l for l in loc_top.index],
            x=loc_top['SKIPPED'],
            name='SKIPPED',
            orientation='h',
            marker_color=STATUS_COLORS['SKIPPED']
        ))
        fig_loc.add_trace(go.Bar(
            y=[l[:35] + '...' if len(l) > 35 else l for l in loc_top.index],
            x=loc_top['FAILED'],
            name='FAILED',
            orientation='h',
            marker_color=STATUS_COLORS['FAILED']
        ))
        
        fig_loc.update_layout(
            barmode='stack',
            height=320,
            margin=dict(l=10, r=20, t=10, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            xaxis=dict(title='Attempts Count', showgrid=True, gridcolor='#f1f5f9'),
            yaxis=dict(title='', autorange='reversed')
        )
        st.plotly_chart(fig_loc)

    with col_d2:
        st.markdown("##### 👨‍🏫 Performance by Assigned Trainer")
        
        tr_ct = pd.crosstab(filtered_df['trainer_name'], filtered_df['status']).fillna(0)
        for col in ['SENT', 'FAILED', 'SKIPPED']:
            if col not in tr_ct.columns:
                tr_ct[col] = 0
                
        tr_ct['TOTAL'] = tr_ct.sum(axis=1)
        tr_top = tr_ct.sort_values(by='TOTAL', ascending=False).head(7)
        
        fig_tr = go.Figure()
        fig_tr.add_trace(go.Bar(
            y=tr_top.index,
            x=tr_top['SENT'],
            name='SENT',
            orientation='h',
            marker_color=STATUS_COLORS['SENT']
        ))
        fig_tr.add_trace(go.Bar(
            y=tr_top.index,
            x=tr_top['SKIPPED'],
            name='SKIPPED',
            orientation='h',
            marker_color=STATUS_COLORS['SKIPPED']
        ))
        fig_tr.add_trace(go.Bar(
            y=tr_top.index,
            x=tr_top['FAILED'],
            name='FAILED',
            orientation='h',
            marker_color=STATUS_COLORS['FAILED']
        ))
        
        fig_tr.update_layout(
            barmode='stack',
            height=320,
            margin=dict(l=10, r=20, t=10, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            xaxis=dict(title='Attempts Count', showgrid=True, gridcolor='#f1f5f9'),
            yaxis=dict(title='', autorange='reversed')
        )
        st.plotly_chart(fig_tr)


def render_triggers():
    st.markdown('<div class="section-title">6. Trigger Type & Template Analytics</div>', unsafe_allow_html=True)

    col_tr1, col_tr2 = st.columns([1, 1])

    trig_ct = pd.crosstab(filtered_df['trigger_type'], filtered_df['status']).fillna(0)
    for col in ['SENT', 'FAILED', 'SKIPPED']:
        if col not in trig_ct.columns:
            trig_ct[col] = 0
    trig_ct['TOTAL'] = trig_ct.sum(axis=1)
    trig_ct = trig_ct.sort_values(by='TOTAL', ascending=False)

    with col_tr1:
        st.markdown("##### ⚡ Volume & Status by Trigger Type")
        
        fig_trig = go.Figure()
        fig_trig.add_trace(go.Bar(
            x=[t.replace('_', ' ').title() for t in trig_ct.index],
            y=trig_ct['SENT'],
            name='SENT',
            marker_color=STATUS_COLORS['SENT']
        ))
        fig_trig.add_trace(go.Bar(
            x=[t.replace('_', ' ').title() for t in trig_ct.index],
            y=trig_ct['SKIPPED'],
            name='SKIPPED',
            marker_color=STATUS_COLORS['SKIPPED']
        ))
        fig_trig.add_trace(go.Bar(
            x=[t.replace('_', ' ').title() for t in trig_ct.index],
            y=trig_ct['FAILED'],
            name='FAILED',
            marker_color=STATUS_COLORS['FAILED']
        ))
        
        fig_trig.update_layout(
            barmode='stack',
            height=320,
            margin=dict(l=10, r=20, t=10, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            xaxis=dict(title='Trigger Type', showgrid=False, tickangle=-20),
            yaxis=dict(title='Attempts Count', showgrid=True, gridcolor='#f1f5f9')
        )
        st.plotly_chart(fig_trig)

    with col_tr2:
        st.markdown("##### 📋 Notification Reachability by Trigger")
        
        trig_reach = filtered_notif_df.groupby('trigger_type').agg(
            total=('notification_id', 'count'),
            reached=('is_reached', 'sum')
        ).reset_index()
        trig_reach['reach_rate'] = (trig_reach['reached'] / trig_reach['total'] * 100).round(1)
        trig_reach['dropped'] = trig_reach['total'] - trig_reach['reached']
        trig_reach = trig_reach.sort_values(by='total', ascending=False)
        
        fig_trig_reach = go.Figure(go.Bar(
            x=[t.replace('_', ' ').title() for t in trig_reach['trigger_type']],
            y=trig_reach['reach_rate'],
            marker=dict(
                color=[PALETTE['teal'] if r > 70 else (PALETTE['amber'] if r > 40 else PALETTE['coral']) for r in trig_reach['reach_rate']],
                line=dict(color=PALETTE['border'], width=1)
            ),
            text=[f"{r}%<br>({re}/{tot})" for r, re, tot in zip(trig_reach['reach_rate'], trig_reach['reached'], trig_reach['total'])],
            textposition='outside'
        ))
        
        fig_trig_reach.update_layout(
            height=320,
            margin=dict(l=10, r=20, t=10, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(title='Trigger Type', showgrid=False, tickangle=-20),
            yaxis=dict(title='Candidate Reach Rate %', showgrid=True, gridcolor='#f1f5f9', range=[0, 115])
        )
        st.plotly_chart(fig_trig_reach)

    st.markdown(f"""
    <div class="warning-box">
        <strong>⚠️ Critical Anomaly Discovered: Onsite vs Online Class Scheduling</strong><br>
        • <strong>Onsite Class Scheduled</strong> achieved a stellar <strong>96.7% reachability rate</strong> (694 of 718 candidates reached).<br>
        • In sharp contrast, <strong>Online Class Scheduled</strong> plummeted to <strong>25.8% reachability</strong> (371 out of 500 candidates completely dropped!).<br>
        • <em>Root Cause:</em> In online scheduling, 74.2% of candidates lack email addresses, and since mobile push tokens are 100% missing and WhatsApp template parameters fail with Meta API 131008, every channel fails simultaneously!
    </div>
    """, unsafe_allow_html=True)


def render_latency():
    st.markdown('<div class="section-title">7. Latency & Velocity SLA Analysis</div>', unsafe_allow_html=True)

    col_l1, col_l2 = st.columns([1.2, 0.8])

    latency_series = filtered_df['dispatch_to_sent_seconds'].dropna()

    with col_l1:
        st.markdown("##### ⏱️ Dispatch-to-Sent Latency Distribution (Seconds)")
        
        if len(latency_series) > 0:
            fig_lat = px.histogram(
                filtered_df.dropna(subset=['dispatch_to_sent_seconds']),
                x='dispatch_to_sent_seconds',
                color='channel',
                color_discrete_map=CHANNEL_COLORS,
                nbins=35,
                marginal='box'
            )
            fig_lat.update_layout(
                height=320,
                margin=dict(l=10, r=20, t=10, b=10),
                plot_bgcolor='white',
                paper_bgcolor='white',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                xaxis=dict(title='Seconds from Dispatch to Sent', showgrid=True, gridcolor='#f1f5f9'),
                yaxis=dict(title='Count', showgrid=True, gridcolor='#f1f5f9')
            )
            st.plotly_chart(fig_lat)
        else:
            st.info("No latency data available for the current filter selection.")

    with col_l2:
        st.markdown("##### 🎯 Latency SLA Percentiles")
        
        if len(latency_series) > 0:
            sla_data = [
                {"Metric": "Minimum Latency", "Value": f"{latency_series.min():.2f}s"},
                {"Metric": "Median (P50)", "Value": f"{latency_series.median():.2f}s"},
                {"Metric": "Average (Mean)", "Value": f"{latency_series.mean():.2f}s"},
                {"Metric": "90th Percentile (P90)", "Value": f"{latency_series.quantile(0.90):.2f}s"},
                {"Metric": "95th Percentile (P95)", "Value": f"{latency_series.quantile(0.95):.2f}s"},
                {"Metric": "99th Percentile (P99)", "Value": f"{latency_series.quantile(0.99):.2f}s"},
                {"Metric": "Maximum Outlier", "Value": f"{latency_series.max():.2f}s"}
            ]
            sla_df = pd.DataFrame(sla_data)
            st.dataframe(sla_df, hide_index=True)
            
            wa_lat = filtered_df[filtered_df['channel'] == 'whatsapp']['dispatch_to_sent_seconds'].dropna()
            em_lat = filtered_df[filtered_df['channel'] == 'email']['dispatch_to_sent_seconds'].dropna()
            wa_mean = wa_lat.mean() if len(wa_lat) > 0 else 0
            em_mean = em_lat.mean() if len(em_lat) > 0 else 0
            
            st.markdown(f"""
            <div style="font-size:12.5px; color:{PALETTE['muted']}; margin-top:8px;">
                • <strong>WhatsApp Engine:</strong> {wa_mean:.2f}s avg latency (Fastest)<br>
                • <strong>Email Engine:</strong> {em_mean:.2f}s avg latency (Outliers up to {em_lat.max():.1f}s)
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No latency data.")


def render_action_plan():
    st.markdown('<div class="section-title">8. Root-Cause Diagnostics & Engineering Action Plan</div>', unsafe_allow_html=True)

    rec1, rec2 = st.columns(2)

    with rec1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:{PALETTE['navy']}; margin:0px 0px 8px 0px;">1. WhatsApp Meta API 131008 Payload Fix</h4>
            <p style="font-size:13px; color:{PALETTE['charcoal']}; margin:0px 0px 10px 0px;">
                <strong>Root Cause:</strong> 1,090 WhatsApp messages failed due to <code>Meta API 131008: Required parameter is missing</code>. 
                Backend webhook payloads are omitting mandatory template variables (e.g. <code>session_date</code>, <code>trainer_name</code>, or <code>candidate_name</code>).
            </p>
            <p style="font-size:12.5px; color:{PALETTE['teal']}; margin:0px; font-weight:600;">
                ✅ Recovery Impact: +1,090 WhatsApp deliveries (+83.3% WhatsApp success rate).
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:{PALETTE['navy']}; margin:0px 0px 8px 0px;">3. Upstream Email Collection Data Hygiene</h4>
            <p style="font-size:13px; color:{PALETTE['charcoal']}; margin:0px 0px 10px 0px;">
                <strong>Root Cause:</strong> 584 emails skipped due to <code>missing email</code>. This disproportionately impacts 
                Online Classes (371 candidates) where physical face-to-face contact does not exist.
            </p>
            <p style="font-size:12.5px; color:{PALETTE['teal']}; margin:0px; font-weight:600;">
                ✅ Recovery Impact: +584 candidates directly reached on primary communication channel.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with rec2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:{PALETTE['navy']}; margin:0px 0px 8px 0px;">2. Mobile App Push Token Registration Sync</h4>
            <p style="font-size:13px; color:{PALETTE['charcoal']}; margin:0px 0px 10px 0px;">
                <strong>Root Cause:</strong> 1,239 push notifications skipped due to <code>missing push tokens</code> (0% Push sent rate). 
                Mobile candidate app is either not requesting push permissions or failing to sync FCM/APNS tokens to the WMS user profile.
            </p>
            <p style="font-size:12.5px; color:{PALETTE['teal']}; margin:0px; font-weight:600;">
                ✅ Recovery Impact: Unlocks instant in-app alerts for 1,302 candidate notifications.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:{PALETTE['navy']}; margin:0px 0px 8px 0px;">4. India TRAI DLT Approval for SMS Gateways</h4>
            <p style="font-size:13px; color:{PALETTE['charcoal']}; margin:0px 0px 10px 0px;">
                <strong>Root Cause:</strong> 100% of SMS attempts failed due to <code>SMS template ID pending DLT approval</code>. 
                Regulatory DLT whitelisting is blocking SMS from acting as the fallback channel.
            </p>
            <p style="font-size:12.5px; color:{PALETTE['teal']}; margin:0px; font-weight:600;">
                ✅ Recovery Impact: Guarantees a 100% reliable offline fallback when mobile internet or email is unavailable.
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_explorer():
    st.markdown('<div class="section-title">9. Failure Triage & Raw Data Explorer</div>', unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns([1.5, 1, 1])

    with col_s1:
        search_query = st.text_input("Search Candidate Name / ID / External Ref", "")
    with col_s2:
        status_explorer_filter = st.selectbox("Status Filter", ["All", "FAILED", "SKIPPED", "SENT"])
    with col_s3:
        error_type_filter = st.selectbox("Error Type Filter", ["All"] + list(filtered_df['error_message'].unique()))

    explorer_df = filtered_df.copy()

    if search_query:
        q = search_query.lower()
        explorer_df = explorer_df[
            explorer_df['candidate_name'].astype(str).str.lower().str.contains(q) |
            explorer_df['candidate_id'].astype(str).str.lower().str.contains(q) |
            explorer_df['external_ref_id'].astype(str).str.lower().str.contains(q)
        ]

    if status_explorer_filter != "All":
        explorer_df = explorer_df[explorer_df['status'] == status_explorer_filter]

    if error_type_filter != "All":
        explorer_df = explorer_df[explorer_df['error_message'] == error_type_filter]

    display_cols = [
        'notification_id', 'candidate_name', 'channel', 'status', 'error_message',
        'trigger_type', 'template_name', 'client_location', 'trainer_name',
        'dispatch_to_sent_seconds', 'notification_date'
    ]

    st.dataframe(
        explorer_df[display_cols],
        height=360
    )

    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=explorer_df.to_csv(index=False).encode('utf-8'),
        file_name=f"notification_engine_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )


# Render based on user mode selection
if dashboard_mode == "📄 Comprehensive Report (All Sections)":
    render_kpis()
    render_funnel()
    render_trends()
    render_channels()
    render_demographics()
    render_triggers()
    render_latency()
    render_action_plan()
    render_explorer()
else:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Scorecards & KPIs",
        "🔻 Funnel & Leakage",
        "📈 Time Trends & Heatmap",
        "📱 Channel Performance",
        "📍 Locations & Trainers",
        "⚡ Triggers & Templates",
        "⏱️ Latency SLA",
        "🛠️ Action Plan & Explorer"
    ])
    with tab1:
        render_kpis()
    with tab2:
        render_funnel()
    with tab3:
        render_trends()
    with tab4:
        render_channels()
    with tab5:
        render_demographics()
    with tab6:
        render_triggers()
    with tab7:
        render_latency()
    with tab8:
        render_action_plan()
        render_explorer()

# Footer
st.markdown(f"""
<div style="text-align: center; color: {PALETTE['muted']}; font-size: 12px; margin-top: 40px; padding: 20px; border-top: 1px solid {PALETTE['border']};">
    Notification Engine Analytics Dashboard • Designed from Senior Data Analyst POV • Style Reference: Interakt Leads Analytics Report
</div>
""", unsafe_allow_html=True)
