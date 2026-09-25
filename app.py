import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==============================================================================
# 1. PAGE CONFIGURATION & EXECUTIVE THEME
# ==============================================================================
st.set_page_config(
    page_title="Notification Engine Analytics | Executive Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    "bg_page": "#f8fafc",
    "bg_pill_red": "#fee2e2",
    "text_pill_red": "#991b1b",
    "bg_pill_green": "#dcfce7",
    "text_pill_green": "#166534",
    "bg_pill_blue": "#dbeafe",
    "text_pill_blue": "#1e40af"
}

# ── Status: muted, dark tones — consistent everywhere ──
STATUS_COLORS = {
    "SENT":      "#1f9a89",   # teal        (original palette — calm, professional green)
    "FAILED":    "#c45f64",   # crimson     (original palette — darker, not neon red)
    "SKIPPED":   "#cda36f",   # amber       (original palette — warm ochre)
    "REACHED":   "#1f9a89",   # teal        (same as SENT)
    "UNREACHED": "#c45f64",   # crimson     (same as FAILED)
}

# ── Channels: muted, brand-adjacent, distinct from status and each other ──
CHANNEL_COLORS = {
    "email":     "#2c79c5",   # ocean blue      (original palette ocean)
    "whatsapp":  "#3d7a5e",   # dark sage green  (distinct from teal/SENT)
    "push":      "#7e519e",   # muted purple     (original palette)
    "sms":       "#a06040",   # burnt sienna     (dark earthy orange, distinct from amber/coral)
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}
    .main {{ background-color: {PALETTE['bg_page']}; }}
    .exec-header {{ padding: 4px 0px 16px 0px; border-bottom: 1px solid {PALETTE['border']}; margin-bottom: 20px; }}
    .exec-title {{ font-size: 27px; font-weight: 800; color: {PALETTE['navy']}; letter-spacing: -0.5px; margin: 0px 0px 4px 0px; display: flex; align-items: center; gap: 12px; }}
    .exec-subtitle {{ font-size: 13.5px; color: {PALETTE['muted']}; margin: 0px 0px 12px 0px; line-height: 1.4; }}
    .status-pill-container {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 6px; }}
    .status-pill {{ font-size: 11.5px; font-weight: 600; padding: 4px 10px; border-radius: 20px; display: inline-flex; align-items: center; gap: 6px; }}
    .pill-red {{ background-color: {PALETTE['bg_pill_red']}; color: {PALETTE['text_pill_red']}; border: 1px solid #fca5a5; }}
    .pill-green {{ background-color: {PALETTE['bg_pill_green']}; color: {PALETTE['text_pill_green']}; border: 1px solid #86efac; }}
    .pill-blue {{ background-color: {PALETTE['bg_pill_blue']}; color: {PALETTE['text_pill_blue']}; border: 1px solid #93c5fd; }}
    .section-title {{ font-size: 18px; font-weight: 700; color: {PALETTE['charcoal']}; margin: 30px 0px 14px 0px; padding-bottom: 6px; border-bottom: 2px solid {PALETTE['sky']}; display: inline-block; letter-spacing: -0.2px; }}
    .exec-card {{ background-color: {PALETTE['bg_card']}; border: 1px solid {PALETTE['border']}; border-radius: 10px; padding: 18px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.02); transition: transform 0.2s ease, box-shadow 0.2s ease; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }}
    .exec-card:hover {{ transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.08); }}
    .exec-card-label {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: {PALETTE['muted']}; margin-bottom: 4px; }}
    .exec-card-value {{ font-size: 28px; font-weight: 800; color: {PALETTE['navy']}; line-height: 1.15; }}
    .exec-card-subtext {{ font-size: 12px; color: {PALETTE['muted']}; margin-top: 6px; }}
    .accent-navy {{ border-top: 3.5px solid {PALETTE['navy']}; }}
    .accent-sky   {{ border-top: 3.5px solid {PALETTE['sky']}; }}
    .accent-teal  {{ border-top: 3.5px solid {PALETTE['teal']}; }}
    .accent-purple{{ border-top: 3.5px solid {PALETTE['purple']}; }}
    .accent-amber {{ border-top: 3.5px solid {PALETTE['amber']}; }}
    .accent-coral {{ border-top: 3.5px solid {PALETTE['coral']}; }}
    .plot-card {{ background-color: #ffffff; border: 1px solid #e4e7eb; border-radius: 12px; padding: 22px 24px 18px 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.03), 0 6px 14px rgba(0,0,0,0.02); margin-bottom: 22px; position: relative; }}
    .chart-header-row {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; margin-bottom: 6px; }}
    .chart-title {{ font-size: 15.5px; font-weight: 700; color: {PALETTE['charcoal']}; flex: 1; line-height: 1.3; }}
    .info-tooltip-wrapper {{ position: relative; display: inline-flex; align-items: center; flex-shrink: 0; }}
    .info-btn {{ width: 22px; height: 22px; border-radius: 50%; background: {PALETTE['sky']}; color: #ffffff; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; cursor: default; user-select: none; line-height: 1; flex-shrink: 0; border: none; box-shadow: 0 1px 4px rgba(72,133,205,0.35); transition: background 0.15s; }}
    .info-btn:hover {{ background: {PALETTE['navy']}; }}
    .info-tooltip-box {{ visibility: hidden; opacity: 0; position: absolute; right: 28px; top: -6px; width: 310px; background: #ffffff; border: 1px solid {PALETTE['border']}; border-radius: 10px; padding: 14px 16px; box-shadow: 0 8px 28px rgba(0,0,0,0.12); z-index: 9999; transition: opacity 0.18s ease, visibility 0.18s ease; font-size: 12.2px; line-height: 1.55; color: {PALETTE['charcoal']}; pointer-events: none; }}
    .info-tooltip-box::after {{ content: ""; position: absolute; top: 12px; right: -7px; border-width: 6px 0 6px 7px; border-style: solid; border-color: transparent transparent transparent #ffffff; filter: drop-shadow(1px 0 0 {PALETTE['border']}); }}
    .info-tooltip-wrapper:hover .info-tooltip-box {{ visibility: visible; opacity: 1; }}
    .tooltip-heading {{ font-size: 13.5px; font-weight: 700; color: {PALETTE['navy']}; margin-bottom: 10px; }}
    .tooltip-section {{ margin-bottom: 8px; }}
    .tooltip-label {{ font-weight: 700; color: {PALETTE['charcoal']}; }}
    .exec-takeaway-box {{ background-color: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid {PALETTE['navy']}; padding: 14px 18px; border-radius: 0px 8px 8px 0px; margin: 14px 0px; font-size: 13.5px; color: {PALETTE['charcoal']}; line-height: 1.5; }}
    .exec-alert-box {{ background-color: #fff1f2; border: 1px solid #fecdd3; border-left: 4px solid {PALETTE['crimson']}; padding: 16px 20px; border-radius: 0px 8px 8px 0px; margin: 14px 0px; font-size: 13.5px; color: {PALETTE['charcoal']}; line-height: 1.5; }}
    .exec-simulator-container {{ background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%); border: 1px solid #bfdbfe; border-radius: 12px; padding: 20px 24px; margin: 20px 0px; box-shadow: 0 4px 14px rgba(37,99,235,0.06); }}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. DATA PIPELINE
# ==============================================================================
@st.cache_data
def load_and_prepare_data(file_source):
    df = pd.read_csv(file_source, low_memory=False)
    df['client_location'] = df['client_location'].fillna('Unknown / Virtual')
    df['trainer_name']    = df['trainer_name'].fillna('Not Specified')
    df['error_message']   = df['error_message'].fillna('None (Success)')
    for col in ['notification_created_at', 'delivery_created_at', 'dispatched_at', 'sent_at']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    if 'notification_date' in df.columns:
        df['notification_date'] = pd.to_datetime(df['notification_date']).dt.date
    return df


default_csv = "Notification_Engine_Analytics - vw_notification_analytics.csv"

st.sidebar.markdown("### ⚙️ Executive Data Controls")
uploaded_file = st.sidebar.file_uploader("Upload raw Notification CSV", type=["csv"],
    help="Upload your Notification Engine dataset to automatically generate executive analytics.")

try:
    if uploaded_file is not None:
        raw_df = load_and_prepare_data(uploaded_file)
        st.sidebar.success(f"Custom file loaded: {len(raw_df):,} records")
    else:
        raw_df = load_and_prepare_data(default_csv)
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()


def compute_notification_level_metrics(df):
    notif = df.groupby('notification_id').agg(
        external_ref_id=('external_ref_id','first'), trigger_type=('trigger_type','first'),
        template_name=('template_name','first'), candidate_id=('candidate_id','first'),
        candidate_name=('candidate_name','first'), trainer_name=('trainer_name','first'),
        client_location=('client_location','first'), notification_date=('notification_date','first'),
        notification_day_name=('notification_day_name','first'), notification_hour=('notification_hour','first'),
        total_channels=('channel','count'), sent_legs=('sent_flag','sum'),
        failed_legs=('failed_flag','sum'), skipped_legs=('skipped_flag','sum')
    ).reset_index()
    notif['is_reached']   = notif['sent_legs'] > 0
    notif['reach_status'] = np.where(notif['is_reached'], 'REACHED (>=1 Channel)', 'UNREACHED (0 Channels)')
    return notif


notif_df = compute_notification_level_metrics(raw_df)

st.sidebar.markdown("---")
st.sidebar.markdown("#### Cohort Filtering")

min_date = raw_df['notification_date'].min()
max_date = raw_df['notification_date'].max()
date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

all_channels  = sorted(raw_df['channel'].dropna().unique().tolist())
all_triggers  = sorted(raw_df['trigger_type'].dropna().unique().tolist())
all_statuses  = sorted(raw_df['status'].dropna().unique().tolist())
all_locations = sorted(raw_df['client_location'].dropna().unique().tolist())

selected_channels  = st.sidebar.multiselect("Channels",        all_channels,  default=all_channels)
selected_triggers  = st.sidebar.multiselect("Trigger Types",   all_triggers,  default=all_triggers)
selected_statuses  = st.sidebar.multiselect("Delivery Status", all_statuses,  default=all_statuses)
selected_locations = st.sidebar.multiselect("Client Locations",all_locations, default=all_locations)

if st.sidebar.button("Reset to Full Dataset", width='stretch'):
    st.rerun()

if not selected_channels:  selected_channels  = all_channels
if not selected_triggers:  selected_triggers  = all_triggers
if not selected_statuses:  selected_statuses  = all_statuses
if not selected_locations: selected_locations = all_locations

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_d, end_d = date_range
    mask = (
        (raw_df['notification_date'] >= start_d) & (raw_df['notification_date'] <= end_d) &
        (raw_df['channel'].isin(selected_channels)) & (raw_df['trigger_type'].isin(selected_triggers)) &
        (raw_df['status'].isin(selected_statuses)) & (raw_df['client_location'].isin(selected_locations))
    )
else:
    mask = (
        (raw_df['channel'].isin(selected_channels)) & (raw_df['trigger_type'].isin(selected_triggers)) &
        (raw_df['status'].isin(selected_statuses)) & (raw_df['client_location'].isin(selected_locations))
    )

filtered_df = raw_df[mask]

if len(filtered_df) == 0:
    st.warning("No data matches current filter parameters. Please adjust sidebar filters.")
    st.stop()

filtered_notif_ids = filtered_df['notification_id'].unique()
filtered_notif_df  = notif_df[notif_df['notification_id'].isin(filtered_notif_ids)]
st.sidebar.info(f"Cohort: **{len(filtered_df):,}** delivery legs across **{len(filtered_notif_df):,}** unique notifications.")


# ==============================================================================
# 3. HELPERS
# ==============================================================================
def apply_exec_chart_theme(fig, height=350, show_legend=True, pad_l=40, pad_r=30, pad_t=50, pad_b=40):
    fig.update_layout(
        font=dict(family='Inter, -apple-system, sans-serif', size=11.5, color=PALETTE['charcoal']),
        height=height,
        margin=dict(l=pad_l, r=pad_r, t=pad_t, b=pad_b),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        showlegend=show_legend,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                    font=dict(size=11), bgcolor='rgba(255,255,255,0.9)', bordercolor='#e2e8f0', borderwidth=1),
        hoverlabel=dict(bgcolor='#ffffff', font_size=12, font_family='Inter, sans-serif', bordercolor='#e2e8f0')
    )
    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', zeroline=False)
    return fig


def render_chart_header(title, significance, calculation, action):
    """Hover-based 'i' tooltip — no click required."""
    st.markdown(f"""
    <div class="chart-header-row">
        <div class="chart-title">{title}</div>
        <div class="info-tooltip-wrapper">
            <div class="info-btn">i</div>
            <div class="info-tooltip-box">
                <div class="tooltip-heading">About This Chart</div>
                <div class="tooltip-section"><span class="tooltip-label">Significance:</span><br>{significance}</div>
                <div class="tooltip-section"><span class="tooltip-label">How Calculated:</span><br>{calculation}</div>
                <div class="tooltip-section" style="margin-bottom:0"><span class="tooltip-label">Executive Action:</span><br>{action}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# 4. DASHBOARD HEADER
# ==============================================================================
st.markdown(f"""
<div class="exec-header">
    <div class="exec-title"><span>📈</span> Notification Engine Analytics — Operations Dashboard</div>
    <div class="exec-subtitle">A summary of how well the system is reaching candidates across all communication channels — with clear actions to fix what is broken.</div>
    <div class="status-pill-container">
        <span class="status-pill pill-red">🚨 Alert: 1 in 3 candidates received no message at all</span>
        <span class="status-pill pill-green">✅ Speed: Messages are sending in under 3 seconds on average</span>
        <span class="status-pill pill-blue">💡 Quick Win: One WhatsApp fix can recover 1,090 failed deliveries today</span>
    </div>
</div>
""", unsafe_allow_html=True)

dashboard_mode = st.radio("Navigation Mode",
    ["📄 Full Report (All Sections)", "📑 Section Tabs (Quick Browse)"],
    horizontal=True, label_visibility="collapsed")


# ==============================================================================
# 5. RENDER FUNCTIONS  (ordered for executive narrative flow)
# ==============================================================================

# ── 1. KPI Scorecards ────────────────────────────────────────────────────────
def render_executive_kpis():
    st.markdown('<div class="section-title">1. Key Performance Indicators</div>', unsafe_allow_html=True)

    total_notifs   = len(filtered_notif_df)
    total_legs     = len(filtered_df)
    sent_legs_cnt  = int(filtered_df['sent_flag'].sum())
    reached_notifs = int(filtered_notif_df['is_reached'].sum())
    reach_rate     = (reached_notifs / total_notifs * 100) if total_notifs > 0 else 0
    channel_rate   = (sent_legs_cnt  / total_legs   * 100) if total_legs   > 0 else 0
    dropped_cnt    = total_notifs - reached_notifs
    dropped_rate   = (dropped_cnt / total_notifs * 100) if total_notifs > 0 else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class="exec-card accent-navy">
            <div><div class="exec-card-label">Total Notifications Sent</div>
            <div class="exec-card-value">{total_notifs:,}</div></div>
            <div class="exec-card-subtext">Unique candidate alerts triggered by the system</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="exec-card accent-sky">
            <div><div class="exec-card-label">Total Delivery Attempts</div>
            <div class="exec-card-value">{total_legs:,}</div></div>
            <div class="exec-card-subtext">{total_legs/total_notifs:.1f} channels tried per notification</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="exec-card accent-teal">
            <div><div class="exec-card-label">Candidates Reached</div>
            <div class="exec-card-value">{reach_rate:.1f}%</div></div>
            <div class="exec-card-subtext">{reached_notifs:,} people got the message on at least one channel</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="exec-card accent-purple">
            <div><div class="exec-card-label">Successful Delivery Rate</div>
            <div class="exec-card-value">{channel_rate:.1f}%</div></div>
            <div class="exec-card-subtext">{sent_legs_cnt:,} of {total_legs:,} attempts actually delivered</div></div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="exec-card accent-coral">
            <div><div class="exec-card-label">Completely Missed</div>
            <div class="exec-card-value">{dropped_rate:.1f}%</div></div>
            <div class="exec-card-subtext">{dropped_cnt:,} candidates — no message reached them on any channel</div></div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="exec-takeaway-box">
        <strong>📋 Summary — What This Means:</strong>
        <ul style="margin:10px 0 0 0; padding-left:18px; line-height:1.8;">
            <li>The system tries up to <strong>3 channels per candidate</strong> (Push, WhatsApp, Email), but <strong>{dropped_cnt:,} people ({dropped_rate:.1f}%) received nothing at all.</strong></li>
            <li><strong>WhatsApp error (code 131008):</strong> A missing field in the message data caused 1,090 deliveries to fail. One backend fix resolves all of them.</li>
            <li><strong>Mobile Push not working:</strong> 1,239 attempts were skipped because the app never saved the device token when candidates logged in.</li>
            <li><strong>No email address on file:</strong> 584 online candidates were registered without an email, leaving them with no backup contact method.</li>
        </ul>
    </div>""", unsafe_allow_html=True)


# ── 2. What-If Simulator ─────────────────────────────────────────────────────
def render_what_if_simulator():
    st.markdown(f"""<div class="exec-simulator-container">
        <h4 style="margin:0px 0px 6px 0px;color:{PALETTE['navy']};font-weight:700;font-size:16px;">
            🎛️ What-If Simulator — See the Impact of Each Fix</h4>
        <p style="font-size:12.5px;color:{PALETTE['muted']};margin:0px 0px 14px 0px;">
            Tick one or more fixes below to see how many more candidates would be reached if that problem were solved today:</p>""",
        unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns(3)
    with sc1: fix_wa    = st.checkbox("Fix WhatsApp Error (Code 131008)",    value=True,  help="Correct the missing field in WhatsApp messages — recovers 1,090 failed deliveries immediately")
    with sc2: fix_push  = st.checkbox("Save Mobile Push Device Tokens",      value=False, help="Store the device ID when candidates log into the app — unlocks 1,239 push notifications")
    with sc3: fix_email = st.checkbox("Make Email Mandatory at Registration", value=False, help="Require email at online sign-up — gives 584 candidates a backup contact channel")

    sim_df = filtered_df.copy()
    if fix_wa:
        sim_df.loc[(sim_df['channel']=='whatsapp') & (sim_df['error_code']==131008), 'sent_flag'] = 1
    if fix_push:
        sim_df.loc[(sim_df['channel']=='push') & (sim_df['error_message']=='missing push tokens'), 'sent_flag'] = 1
    if fix_email:
        sim_df.loc[(sim_df['channel']=='email') & (sim_df['error_message']=='missing email'), 'sent_flag'] = 1

    sim_notif   = sim_df.groupby('notification_id')['sent_flag'].sum() > 0
    sim_reached = int(sim_notif.sum())
    total_n     = len(sim_notif)
    sim_rate    = (sim_reached / total_n * 100) if total_n > 0 else 0
    base_reached= int(filtered_notif_df['is_reached'].sum())
    base_rate   = (base_reached / total_n * 100) if total_n > 0 else 0
    delta_rate  = sim_rate - base_rate
    sim_dropped = total_n - sim_reached
    recovered   = sim_reached - base_reached

    r1, r2, r3, r4 = st.columns(4)
    with r1: st.metric("Current Reach Rate",     f"{base_rate:.1f}%")
    with r2: st.metric("Reach Rate After Fixes", f"{sim_rate:.1f}%",    f"+{delta_rate:.1f}%")
    with r3: st.metric("Still Unreached",         f"{sim_dropped:,}",   f"-{(total_n-base_reached)-sim_dropped:,}", delta_color="inverse")
    with r4: st.metric("Extra Candidates Reached",f"{recovered:,}")

    st.markdown("</div>", unsafe_allow_html=True)


# ── 3. Funnel & Leakage ──────────────────────────────────────────────────────
def render_funnel_and_leakage():
    st.markdown('<div class="section-title">2. Where Are Messages Being Lost?</div>', unsafe_allow_html=True)

    total_n        = len(filtered_notif_df)
    total_l        = len(filtered_df)
    dispatched_cnt = int(filtered_df['dispatched_at'].notna().sum())
    sent_cnt       = int(filtered_df['sent_flag'].sum())
    reached_cnt    = int(filtered_notif_df['is_reached'].sum())

    # Full-width funnel
    st.markdown('<div class="plot-card">', unsafe_allow_html=True)
    render_chart_header(
        title="📌 End-to-End Message Delivery Journey",
        significance="Shows how many notifications make it through each stage — from the moment one is created to the point a candidate actually receives it. The further the drop, the bigger the problem.",
        calculation="Stage 1: total notifications created · Stage 2: sent to the delivery provider · Stage 3: accepted and dispatched · Stage 4: at least one channel reached the candidate · Stage 5: confirmed read (not yet tracked).",
        action="Set up delivery receipt tracking (webhooks) with your messaging providers to close the visibility gap at Stage 5."
    )

    stages  = ["1. Notifications Created", "2. Handed to Delivery Provider", "3. Successfully Sent", "4. Candidate Received (≥1 Channel)", "5. Confirmed Read"]
    values  = [total_n, dispatched_cnt, sent_cnt, reached_cnt, 0]
    percents= [
        "100% — starting point",
        f"{dispatched_cnt/total_l*100:.1f}% of all attempts handed over",
        f"{sent_cnt/total_l*100:.1f}% successfully delivered",
        f"{reached_cnt/total_n*100:.1f}% of candidates received a message",
        "0% — read receipts not yet tracked"
    ]
    bar_colors = [PALETTE['navy'], PALETTE['ocean'], PALETTE['teal'], PALETTE['sage'], PALETTE['muted']]

    fig_funnel = go.Figure(go.Bar(
        x=values, y=stages, orientation='h',
        marker=dict(color=bar_colors, line=dict(color=PALETTE['border'], width=1)),
        text=[f"<b>{v:,}</b>  —  {p}" if v > 0 else "<b>0</b>  —  No read receipts tracked yet" for v, p in zip(values, percents)],
        textposition='outside',
        textfont=dict(family='Inter, sans-serif', size=12, color=PALETTE['charcoal']),
        cliponaxis=False,
        hovertext=[f"<b>{s}</b><br>Volume: {v:,}<br>{p}" for s, v, p in zip(stages, values, percents)],
        hoverinfo='text'
    ))
    fig_funnel.update_layout(
        yaxis=dict(autorange="reversed", showgrid=False, tickfont=dict(size=12.5, color=PALETTE['charcoal'])),
        xaxis=dict(title="Volume", showgrid=True, gridcolor='#f1f5f9', range=[0, total_n * 1.55]),
        bargap=0.22
    )
    st.plotly_chart(apply_exec_chart_theme(fig_funnel, height=340, show_legend=False, pad_l=55, pad_r=20, pad_t=30, pad_b=45))
    st.markdown('</div>', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([1.4, 0.6])

    with col_f1:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="⚠️ Why Did Messages Fail? — Drop-off Reasons",
            significance="Shows the most common reasons why messages were not delivered. Each bar is a distinct failure category, making it easy to see which problem is causing the most damage.",
            calculation="All failed and skipped attempts are grouped by their error reason. Each group is counted and shown as a percentage of total failures. Sorted from largest to smallest.",
            action="Fix the WhatsApp message data error (top bar) first — it alone accounts for over a third of all failures and can be resolved in a single day."
        )

        leak_df     = filtered_df[filtered_df['status'].isin(['FAILED','SKIPPED'])].copy()
        leak_counts = leak_df['error_message'].value_counts().reset_index()
        leak_counts.columns = ['Reason', 'Count']
        total_leak  = leak_counts['Count'].sum()
        leak_counts['Pct'] = (leak_counts['Count'] / total_leak * 100).round(1) if total_leak > 0 else 0
        top_leaks   = leak_counts.head(6)

        def get_leak_color(r):
            if "Meta API" in r or "131008" in r: return PALETTE["coral"]
            if "push tokens" in r:               return PALETTE["crimson"]
            if "missing email" in r:             return PALETTE["amber"]
            return PALETTE["muted"]

        fig_leak = go.Figure(go.Bar(
            x=top_leaks['Count'],
            y=[r[:42]+'...' if len(r) > 42 else r for r in top_leaks['Reason']],
            orientation='h',
            marker=dict(color=[get_leak_color(r) for r in top_leaks['Reason']], line=dict(color=PALETTE['border'], width=1)),
            text=[f"  {c:,}  ({p}%)" for c, p in zip(top_leaks['Count'], top_leaks['Pct'])],
            textposition='outside',
            textfont=dict(family='Inter, sans-serif', size=11.5, color=PALETTE['charcoal']),
            cliponaxis=False,
            hovertext=[f"<b>{r}</b><br>Failed Attempts: {c:,}<br>Share: {p}%" for r, c, p in zip(top_leaks['Reason'], top_leaks['Count'], top_leaks['Pct'])],
            hoverinfo='text'
        ))
        fig_leak.update_layout(
            yaxis=dict(autorange="reversed", showgrid=False, tickfont=dict(size=11.5)),
            xaxis=dict(title="Number of Failed / Skipped Attempts", showgrid=True, gridcolor='#f1f5f9', range=[0, top_leaks['Count'].max() * 1.4]),
            bargap=0.28
        )
        st.plotly_chart(apply_exec_chart_theme(fig_leak, height=360, show_legend=False, pad_l=55, pad_r=50, pad_t=30, pad_b=45))
        st.markdown('</div>', unsafe_allow_html=True)

    with col_f2:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="🎯 How Many Candidates Were Reached?",
            significance="Shows the simple split between candidates who received at least one message, and those who received nothing at all.",
            calculation="Each notification is checked: if at least one channel (Email, WhatsApp, or Push) delivered successfully, the candidate is marked as Reached. Otherwise, they are marked as Missed.",
            action="The 32% missed segment is the primary target — see Section 7 for the step-by-step fix plan."
        )

        reach_vals = [int(filtered_notif_df['is_reached'].sum()), int((~filtered_notif_df['is_reached']).sum())]
        reach_labels = ['Reached (at least 1 channel)', 'Not Reached (all channels failed)']

        fig_donut2 = go.Figure(go.Pie(
            labels=reach_labels, values=reach_vals, hole=0.62,
            marker=dict(colors=[STATUS_COLORS['REACHED'], STATUS_COLORS['UNREACHED']], line=dict(color='white', width=2)),
            textinfo='label+percent', textfont=dict(size=11.5, family='Inter'),
            hovertemplate="<b>%{label}</b><br>%{value:,} candidates<br>%{percent}<extra></extra>"
        ))
        fig_donut2.update_layout(
            annotations=[dict(text=f"<b>{reach_vals[0]:,}</b><br>Reached", x=0.5, y=0.5, font_size=14, showarrow=False)]
        )
        st.plotly_chart(apply_exec_chart_theme(fig_donut2, height=360, show_legend=False, pad_l=20, pad_r=20, pad_t=30, pad_b=30))
        st.markdown('</div>', unsafe_allow_html=True)


# ── 4. Channel & Provider Matrix ─────────────────────────────────────────────
def render_channels_and_providers():
    st.markdown('<div class="section-title">3. Channel Performance — Email, WhatsApp, Push &amp; SMS</div>', unsafe_allow_html=True)

    ct_ch = pd.crosstab(filtered_df['channel'], filtered_df['status']).fillna(0)
    for col in ['SENT','FAILED','SKIPPED']:
        if col not in ct_ch.columns: ct_ch[col] = 0

    col_c1, col_c2 = st.columns([1.3, 0.7])

    with col_c1:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="📊 Delivery Outcome by Channel — Sent, Skipped, Failed",
            significance="Shows how each channel is performing. This makes it immediately clear which channel is working well and which has a specific problem that needs fixing.",
            calculation="Counts of Sent, Failed, and Skipped attempts are stacked per channel. The total at the top of each bar shows overall volume for that channel.",
            action="WhatsApp has the most failures — fixing the message data error will recover 1,090 deliveries without touching any other channel."
        )

        ch_totals = ct_ch[['SENT','FAILED','SKIPPED']].sum(axis=1)

        fig_ch = go.Figure()
        for status, color in [('SENT', STATUS_COLORS['SENT']), ('SKIPPED', STATUS_COLORS['SKIPPED']), ('FAILED', STATUS_COLORS['FAILED'])]:
            fig_ch.add_trace(go.Bar(
                x=[c.upper() for c in ct_ch.index], y=ct_ch[status], name=status,
                marker_color=color, marker_line=dict(color='white', width=1),
                text=[f"<b>{int(v):,}</b>" if v > 60 else "" for v in ct_ch[status]],
                textposition='inside', textfont=dict(size=12, color='white', family='Inter'),
                insidetextanchor='middle',
                hovertemplate=f"<b>%{{x}}</b><br>{status}: %{{y:,}}<extra></extra>"
            ))
        for ch, total in zip([c.upper() for c in ct_ch.index], ch_totals):
            fig_ch.add_annotation(x=ch, y=total, text=f"<b>Total: {int(total):,}</b>",
                showarrow=False, yshift=14, font=dict(size=12, color=PALETTE['charcoal'], family='Inter'))

        fig_ch.update_layout(
            barmode='stack',
            xaxis=dict(title="Channel", showgrid=False, tickfont=dict(size=13, family='Inter', color=PALETTE['charcoal'])),
            yaxis=dict(title="Delivery Attempts", showgrid=True, gridcolor='#f1f5f9',
                       range=[0, ch_totals.max() * 1.22]),
            bargap=0.35
        )
        st.plotly_chart(apply_exec_chart_theme(fig_ch, height=400, pad_l=50, pad_r=35, pad_t=60, pad_b=45))
        st.markdown('</div>', unsafe_allow_html=True)

    with col_c2:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="🍩 How Is Volume Split Across Channels?",
            significance="Shows which channels carry the most traffic. An even split means good redundancy — if one channel fails, others can pick up the load.",
            calculation="Total delivery attempts counted per channel and shown as a percentage of the overall total.",
            action="SMS is barely being used (0.15% of volume) — investigate whether it can serve as a reliable backup when other channels fail."
        )

        ch_sums = ct_ch.sum(axis=1)
        total_legs_val = int(ch_sums.sum())
        fig_donut = go.Figure(go.Pie(
            labels=[c.upper() for c in ch_sums.index],
            values=ch_sums.values, hole=0.65,
            marker=dict(colors=[CHANNEL_COLORS.get(c.lower(), PALETTE['navy']) for c in ch_sums.index],
                        line=dict(color='white', width=2)),
            textinfo='label+percent', textfont=dict(size=11.5, family='Inter'),
            hovertemplate="<b>%{label}</b><br>Attempts: %{value:,}<br>Share: %{percent}<extra></extra>"
        ))
        fig_donut.update_layout(
            annotations=[dict(text=f"<b>{total_legs_val:,}</b><br>Total Legs", x=0.5, y=0.5, font_size=14, showarrow=False)]
        )
        st.plotly_chart(apply_exec_chart_theme(fig_donut, height=400, show_legend=False, pad_l=20, pad_r=20, pad_t=40, pad_b=30))
        st.markdown('</div>', unsafe_allow_html=True)

    ce1, ce2, ce3, ce4 = st.columns(4)
    with ce1:
        st.markdown(f"""<div class="exec-card" style="border-left:4px solid {CHANNEL_COLORS['email']};">
            <div style="font-weight:700;color:{CHANNEL_COLORS['email']};font-size:14px;">📧 EMAIL — 1,308 Attempts</div>
            <div style="font-size:22px;font-weight:800;color:{PALETTE['navy']};margin:6px 0;">55.4% Delivered</div>
            <div style="font-size:12px;color:{PALETTE['muted']};line-height:1.6;">✅ No failures · ⏭️ 44.6% skipped<br>Reason: email address missing at registration</div></div>""", unsafe_allow_html=True)
    with ce2:
        st.markdown(f"""<div class="exec-card" style="border-left:4px solid {CHANNEL_COLORS['whatsapp']};">
            <div style="font-weight:700;color:{CHANNEL_COLORS['whatsapp']};font-size:14px;">💬 WHATSAPP — 1,308 Attempts</div>
            <div style="font-size:22px;font-weight:800;color:{PALETTE['navy']};margin:6px 0;">14.8% Delivered</div>
            <div style="font-size:12px;color:{PALETTE['muted']};line-height:1.6;">❌ 84% failed · Error code 131008<br>Reason: missing field in the message template</div></div>""", unsafe_allow_html=True)
    with ce3:
        st.markdown(f"""<div class="exec-card" style="border-left:4px solid {CHANNEL_COLORS['push']};">
            <div style="font-weight:700;color:{CHANNEL_COLORS['push']};font-size:14px;">📱 MOBILE PUSH — 1,302 Attempts</div>
            <div style="font-size:22px;font-weight:800;color:{PALETTE['navy']};margin:6px 0;">0.0% Delivered</div>
            <div style="font-size:12px;color:{PALETTE['muted']};line-height:1.6;">⏭️ 95.2% skipped · No device token saved<br>Reason: app did not record device ID at login</div></div>""", unsafe_allow_html=True)
    with ce4:
        st.markdown(f"""<div class="exec-card" style="border-left:4px solid {CHANNEL_COLORS['sms']};">
            <div style="font-weight:700;color:{CHANNEL_COLORS['sms']};font-size:14px;">📟 SMS — 6 Attempts</div>
            <div style="font-size:22px;font-weight:800;color:{PALETTE['navy']};margin:6px 0;">0.0% Delivered</div>
            <div style="font-size:12px;color:{PALETTE['muted']};line-height:1.6;">❌ 100% failed · Regulatory block<br>Reason: awaiting government SMS approval (India)</div></div>""", unsafe_allow_html=True)


# ── 5. Triggers & Templates ───────────────────────────────────────────────────
def render_triggers_and_templates():
    st.markdown('<div class="section-title">4. Onsite vs. Online — Where Is the Gap?</div>', unsafe_allow_html=True)

    trig_reach = filtered_notif_df.groupby('trigger_type').agg(
        total=('notification_id','count'), reached=('is_reached','sum')
    ).reset_index()
    trig_reach['reach_rate'] = (trig_reach['reached'] / trig_reach['total'] * 100).round(1)
    trig_reach['dropped']    = trig_reach['total'] - trig_reach['reached']
    trig_reach = trig_reach.sort_values(by='reach_rate', ascending=False)

    col_tr1, col_tr2 = st.columns([1.3, 0.7])

    with col_tr1:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="⚡ Delivery Success Rate by Class Type",
            significance="Shows what percentage of candidates in each class type (onsite or online) actually received their notification. A low rate means a whole group of candidates is being missed.",
            calculation="For each class type, the success rate = (number of candidates reached ÷ total candidates notified) × 100. Green bars are healthy (above 70%), amber bars need attention (40–70%), red bars are critical (below 40%).",
            action="Online classes have a 25.8% reach rate — far below acceptable. Make email mandatory at online registration to give these candidates a reliable backup channel."
        )

        bar_colors_trig = [STATUS_COLORS['SENT'] if r > 70 else (STATUS_COLORS['SKIPPED'] if r > 40 else STATUS_COLORS['FAILED']) for r in trig_reach['reach_rate']]

        fig_reach = go.Figure(go.Bar(
            x=[t.replace('_',' ').title() for t in trig_reach['trigger_type']],
            y=trig_reach['reach_rate'],
            marker=dict(color=bar_colors_trig, line=dict(color=PALETTE['border'], width=1)),
            text=[f"<b>{r}%</b>  ({re:,} / {tot:,})" for r, re, tot in zip(trig_reach['reach_rate'], trig_reach['reached'], trig_reach['total'])],
            textposition='outside',
            textfont=dict(family='Inter', size=12.5, color=PALETTE['charcoal']),
            cliponaxis=False,
            hovertemplate="<b>%{x}</b><br>Reach Rate: %{y:.1f}%<br>Reached: %{customdata[0]:,} of %{customdata[1]:,}<extra></extra>",
            customdata=list(zip(trig_reach['reached'], trig_reach['total']))
        ))
        fig_reach.update_layout(
            xaxis=dict(title="", showgrid=False, tickangle=-12, tickfont=dict(size=12)),
            yaxis=dict(title="Delivery Success Rate (%)", showgrid=True, gridcolor='#f1f5f9', range=[0, 135]),
            bargap=0.35
        )
        fig_reach.add_hline(y=70, line_dash="dot", line_color=STATUS_COLORS['SENT'],    annotation_text="70% Target",  annotation_position="right", annotation_font_color=STATUS_COLORS['SENT'])
        fig_reach.add_hline(y=40, line_dash="dot", line_color=STATUS_COLORS['SKIPPED'], annotation_text="40% Warning", annotation_position="right", annotation_font_color=STATUS_COLORS['SKIPPED'])
        st.plotly_chart(apply_exec_chart_theme(fig_reach, height=420, show_legend=False, pad_l=50, pad_r=65, pad_t=60, pad_b=50))
        st.markdown('</div>', unsafe_allow_html=True)

    with col_tr2:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="exec-alert-box" style="height:310px;display:flex;flex-direction:column;justify-content:space-around;">
            <div><strong style="font-size:15px;color:{PALETTE['crimson']};">Onsite: 96.7% reached &nbsp;|&nbsp; Online: 25.8% reached</strong><br>
            <span style="font-size:12px;color:{PALETTE['muted']};">3 out of every 4 online candidates received no message at all.</span></div>
            <div style="font-size:12.8px;line-height:1.75;">
                <strong>🏢 Onsite Classes (718 notifications)</strong><br>
                &nbsp;&nbsp;• 694 candidates reached — <strong>96.7% success rate</strong><br>
                &nbsp;&nbsp;• Email collected at in-person sign-up — reliable fallback<br><br>
                <strong>💻 Online Classes (500 notifications)</strong><br>
                &nbsp;&nbsp;• Only 129 reached — <strong>25.8% success rate</strong> (371 missed)<br>
                &nbsp;&nbsp;• Candidates register with only a phone number<br>
                &nbsp;&nbsp;• When WhatsApp and Push both fail, there is no email to fall back on
            </div>
            <div style="font-size:12.5px;font-weight:700;color:{PALETTE['crimson']};">
                ✏️ Fix: Add a mandatory email field to the online registration form.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── 6. Time-Series & Heatmap ──────────────────────────────────────────────────
def render_time_series():
    st.markdown('<div class="section-title">5. When Are Messages Being Sent? — Trends &amp; Patterns</div>', unsafe_allow_html=True)

    daily_df = filtered_df.groupby('notification_date').agg(
        total_attempts=('delivery_id','count'), sent_count=('sent_flag','sum'),
        failed_count=('failed_flag','sum'), skipped_count=('skipped_flag','sum')
    ).reset_index()
    daily_df['success_rate'] = (daily_df['sent_count'] / daily_df['total_attempts'] * 100).round(1)
    daily_df['date_str']     = daily_df['notification_date'].astype(str)

    col_t1, col_t2 = st.columns([1.5, 0.5])

    with col_t1:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="📅 Daily Dispatch Volume &amp; Sent Rate Trend",
            significance="Monitors daily delivery volume and detects temporal quality shifts, carrier outages, or batch scheduling failure events.",
            calculation="Group by notification_date. Left axis: stacked bars — SENT, SKIPPED, FAILED counts. Right axis: Sent Rate% = (Sent/Total Daily) x 100 as dual-axis line with data labels.",
            action="Establish automated alerting if daily sent rate drops below 30% to catch batch processing failures within hours."
        )

        fig_time = go.Figure()
        fig_time.add_trace(go.Bar(x=daily_df['date_str'], y=daily_df['sent_count'], name='Sent',
            marker_color=STATUS_COLORS['SENT'],
            text=[f"<b>{v:,}</b>" if v > 80 else "" for v in daily_df['sent_count']],
            textposition='inside', textfont=dict(size=11, color='white', family='Inter'),
            hovertemplate="<b>%{x}</b><br>Sent: %{y:,}<extra></extra>"))
        fig_time.add_trace(go.Bar(x=daily_df['date_str'], y=daily_df['skipped_count'], name='Skipped',
            marker_color=STATUS_COLORS['SKIPPED'],
            text=[f"<b>{v:,}</b>" if v > 80 else "" for v in daily_df['skipped_count']],
            textposition='inside', textfont=dict(size=11, color='white', family='Inter'),
            hovertemplate="<b>%{x}</b><br>Skipped: %{y:,}<extra></extra>"))
        fig_time.add_trace(go.Bar(x=daily_df['date_str'], y=daily_df['failed_count'], name='Failed',
            marker_color=STATUS_COLORS['FAILED'],
            text=[f"<b>{v:,}</b>" if v > 80 else "" for v in daily_df['failed_count']],
            textposition='inside', textfont=dict(size=11, color='white', family='Inter'),
            hovertemplate="<b>%{x}</b><br>Failed: %{y:,}<extra></extra>"))
        fig_time.add_trace(go.Scatter(x=daily_df['date_str'], y=daily_df['success_rate'],
            name='Sent Rate % (right)', yaxis='y2', mode='lines+markers+text',
            line=dict(color=PALETTE['navy'], width=2.5),
            marker=dict(size=8, color=PALETTE['navy'], line=dict(color='white', width=1.5)),
            text=[f"<b>{r}%</b>" for r in daily_df['success_rate']],
            textposition='top center', textfont=dict(size=11.5, color=PALETTE['navy'], family='Inter'),
            hovertemplate="<b>%{x}</b><br>Sent Rate: %{y:.1f}%<extra></extra>"))
        fig_time.update_layout(
            barmode='stack',
            xaxis=dict(title="Date", showgrid=False, tickangle=-30),
            yaxis=dict(title="Attempt Count", showgrid=True, gridcolor='#f1f5f9'),
            yaxis2=dict(title="Sent Rate (%)", overlaying='y', side='right', range=[0, 130], showgrid=False),
            bargap=0.25
        )
        st.plotly_chart(apply_exec_chart_theme(fig_time, height=400, pad_l=50, pad_r=65, pad_t=60, pad_b=50))
        st.markdown('</div>', unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="📆 Volume by Day of Week",
            significance="Shows which days of the week have the highest notification activity — useful for spotting batch scheduling patterns or peak load days.",
            calculation="Total delivery attempts counted per day name (Monday to Sunday), with each bar labelled by count and share percentage. The busiest day is highlighted.",
            action="Consider spreading large batch sends across the week to avoid overloading the system on peak days."
        )

        day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        day_cnts  = filtered_df['notification_day_name'].value_counts().reindex(day_order).dropna().reset_index()
        day_cnts.columns = ['Day','Count']
        day_cnts['Pct'] = (day_cnts['Count'] / day_cnts['Count'].sum() * 100).round(1)
        max_idx = day_cnts['Count'].idxmax()

        fig_dow = go.Figure(go.Bar(
            x=day_cnts['Day'], y=day_cnts['Count'],
            marker=dict(
                color=[PALETTE['navy'] if i == max_idx else PALETTE['sky'] for i in range(len(day_cnts))],
                line=dict(color=PALETTE['border'], width=1)
            ),
            text=[f"<b>{c:,}</b><br>{p}%" for c, p in zip(day_cnts['Count'], day_cnts['Pct'])],
            textposition='outside', textfont=dict(family='Inter', size=12.5, color=PALETTE['charcoal']),
            cliponaxis=False,
            hovertemplate="<b>%{x}</b><br>Volume: %{y:,}<extra></extra>"
        ))
        fig_dow.update_layout(
            xaxis=dict(title="", showgrid=False, tickangle=-30, tickfont=dict(size=12, family='Inter')),
            yaxis=dict(title="Volume", showgrid=True, gridcolor='#f1f5f9',
                       range=[0, day_cnts['Count'].max() * 1.45]),
            bargap=0.3
        )
        st.plotly_chart(apply_exec_chart_theme(fig_dow, height=400, show_legend=False, pad_l=45, pad_r=25, pad_t=55, pad_b=50))
        st.markdown('</div>', unsafe_allow_html=True)


    # ── Heatmap 1: Day of Week × Hour of Day ──
    st.markdown('<div class="plot-card">', unsafe_allow_html=True)
    render_chart_header(
        title="🕒 Temporal Influx Heatmap — Day of Week × Hour of Day",
        significance="Reveals diurnal scheduling habits and peak dispatch hours where gateway throttling or candidate notification fatigue is most likely to occur.",
        calculation="2D pivot: Index=notification_day_name, Columns=notification_hour (0-23), Values=COUNT(delivery_id). Warm gradient: cream=zero activity, crimson=peak volume.",
        action="Shift automated candidate reminders to 10 AM–2 PM local time to maximize read rates and minimize delivery noise."
    )

    pivot_heat = filtered_df.pivot_table(
        index='notification_day_name', columns='notification_hour',
        values='delivery_id', aggfunc='count', fill_value=0
    )
    pivot_heat = pivot_heat.reindex([d for d in day_order if d in pivot_heat.index])

    def fmt_hr(h):
        if h == 0:   return "12 AM"
        if h < 12:   return f"{h} AM"
        if h == 12:  return "12 PM"
        return f"{h-12} PM"

    # Traffic-light palette: green (low) → yellow-green → amber → orange → red (peak)
    HEAT_COLORSCALE = [
        [0.0,  "#f9fafb"],   # empty / zero
        [0.05, "#5a9e3a"],   # bright green  (low)
        [0.25, "#93c840"],   # yellow-green
        [0.45, "#f5c518"],   # golden amber
        [0.65, "#f28a1e"],   # orange
        [0.82, "#e04a2a"],   # orange-red
        [1.0,  "#b71c1c"],   # deep red (peak)
    ]

    heat_text = [[str(v) if v > 0 else "" for v in row] for row in pivot_heat.values]

    fig_heat = go.Figure(go.Heatmap(
        z=pivot_heat.values,
        x=[fmt_hr(int(c)) for c in pivot_heat.columns],
        y=pivot_heat.index.tolist(),
        colorscale=HEAT_COLORSCALE,
        colorbar=dict(title="Volume", thickness=14, outlinewidth=0),
        text=heat_text, texttemplate="%{text}",
        textfont=dict(size=12, color="#ffffff", family='Inter'),
        hoverongaps=False,
        hovertemplate="<b>%{y} — %{x}</b><br>Volume: %{z:,}<extra></extra>",
        xgap=2, ygap=3
    ))
    fig_heat.update_layout(
        xaxis=dict(title="Dispatch Hour (UTC)", showgrid=False,
                   tickfont=dict(size=11.5, family='Inter'), tickangle=-30),
        yaxis=dict(title="", autorange="reversed", showgrid=False,
                   tickfont=dict(size=13, family='Inter'))
    )
    st.plotly_chart(apply_exec_chart_theme(fig_heat, height=340, show_legend=False, pad_l=60, pad_r=40, pad_t=30, pad_b=50))
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Heatmap 2: Monthly Calendar Heatmap ──
    st.markdown('<div class="plot-card">', unsafe_allow_html=True)
    render_chart_header(
        title="📅 Monthly Calendar Heatmap — Day of Week × Date",
        significance="Provides a calendar-view of daily dispatch intensity within a chosen month, exposing specific high-load dates, weekday clustering patterns, and scheduling batch surges.",
        calculation="Filter by selected Month + Year. Pivot: Index=notification_day_name (Mon–Sun), Columns=notification_day (1–31), Values=COUNT(delivery_id). Each cell shows the actual date number and volume.",
        action="Use this view to identify specific high-volume dates for capacity planning and to schedule maintenance windows on low-volume days."
    )

    # Month / Year selectors
    avail_years  = sorted(filtered_df['notification_year'].dropna().unique().astype(int).tolist(), reverse=True)
    avail_months_map = {}
    for yr in avail_years:
        months_in_yr = filtered_df[filtered_df['notification_year'] == yr]['notification_month_number'].dropna().unique().astype(int).tolist()
        avail_months_map[yr] = sorted(months_in_yr)

    import calendar as cal_lib

    sel_col1, sel_col2, sel_col3 = st.columns([0.22, 0.22, 0.56])
    with sel_col1:
        sel_year  = st.selectbox("📆 Year",  avail_years,  index=0, key="monthly_heat_year")
    with sel_col2:
        month_nums = avail_months_map.get(sel_year, [])
        month_labels = [cal_lib.month_name[m] for m in month_nums]
        sel_month_label = st.selectbox("🗓️ Month", month_labels, index=len(month_labels)-1, key="monthly_heat_month")
        sel_month_num   = month_nums[month_labels.index(sel_month_label)]

    # Filter to selected month+year
    month_df = filtered_df[
        (filtered_df['notification_year']         == sel_year) &
        (filtered_df['notification_month_number'] == sel_month_num)
    ].copy()

    if len(month_df) == 0:
        st.info(f"No data available for {sel_month_label} {sel_year} under the current sidebar filters.")
    else:
        import datetime as dt_mod

        # ── X-axis: date labels "15, Mon" ──
        def make_date_label(day_num):
            try:
                d = dt_mod.date(int(sel_year), int(sel_month_num), int(day_num))
                return f"{int(day_num)}, {d.strftime('%a')}"
            except Exception:
                return str(int(day_num))

        # ── Y-axis: hour labels "12 AM", "1 AM" … "11 PM" ──
        def fmt_hr(h):
            if h == 0:  return "12 AM"
            if h < 12:  return f"{h} AM"
            if h == 12: return "12 PM"
            return f"{h-12} PM"

        # ── Pivot: rows = hour (0-23), cols = day-of-month ──
        month_pivot = month_df.pivot_table(
            index='notification_hour',
            columns='notification_day',
            values='delivery_id',
            aggfunc='count',
            fill_value=0
        )
        # Ensure all 24 hours are present, sorted 0→23
        all_hours = list(range(24))
        month_pivot = month_pivot.reindex(all_hours, fill_value=0)
        # Sort columns (day numbers) ascending
        month_pivot = month_pivot.reindex(sorted(month_pivot.columns), axis=1)

        # X / Y labels
        x_labels  = [make_date_label(d) for d in month_pivot.columns]
        y_labels  = [fmt_hr(h) for h in month_pivot.index]   # 24 hour labels

        # Cell text: show count, blank for zero
        cell_text = [[str(int(v)) if v > 0 else "" for v in row]
                     for row in month_pivot.values]

        fig_month_heat = go.Figure(go.Heatmap(
            z=month_pivot.values,
            x=x_labels,
            y=y_labels,
            colorscale=HEAT_COLORSCALE,
            colorbar=dict(title="Volume", thickness=14, outlinewidth=0,
                          tickfont=dict(size=11, family='Inter')),
            text=cell_text,
            texttemplate="%{text}",
            textfont=dict(size=10, color="#ffffff", family='Inter'),
            hoverongaps=False,
            hovertemplate="<b>%{x}  ·  %{y}</b><br>Notifications: %{z:,}<extra></extra>",
            xgap=2, ygap=2
        ))
        fig_month_heat.update_layout(
            xaxis=dict(
                title=f"{sel_month_label} {sel_year}  —  date, weekday",
                showgrid=False,
                tickfont=dict(size=11.5, family='Inter', color=PALETTE['charcoal']),
                tickangle=-30,
                side='bottom'
            ),
            yaxis=dict(
                title="Hour of Day",
                autorange="reversed",        # 12 AM on top → 11 PM at bottom
                showgrid=False,
                tickfont=dict(size=11.5, family='Inter', color=PALETTE['charcoal'])
            )
        )

        # ── Stats: aggregate by day for the strip metrics ──
        day_agg      = month_df.groupby('notification_day').agg(
                           volume=('delivery_id','count'), sent=('sent_flag','sum')
                       ).reset_index()
        peak_row     = day_agg.loc[day_agg['volume'].idxmax()]
        peak_day_lbl = make_date_label(peak_row['notification_day'])
        peak_day_vol = int(peak_row['volume'])
        total_month_vol = int(day_agg['volume'].sum())
        sent_month      = int(day_agg['sent'].sum())
        sent_pct        = round(sent_month / total_month_vol * 100, 1) if total_month_vol > 0 else 0

        # Mini stat strip
        ms1, ms2, ms3, ms4 = st.columns(4)
        ms1.metric("Total Attempts",    f"{total_month_vol:,}")
        ms2.metric("Successfully Sent", f"{sent_month:,}",   f"{sent_pct}% sent rate")
        ms3.metric("Peak Day",           peak_day_lbl,         f"{peak_day_vol:,} attempts")
        ms4.metric("Active Days",        f"{month_df['notification_day'].nunique()} days")

        st.plotly_chart(apply_exec_chart_theme(fig_month_heat, height=480, show_legend=False, pad_l=65, pad_r=40, pad_t=20, pad_b=55))

    st.markdown('</div>', unsafe_allow_html=True)


# ── 7. Demographics & Segmentation ────────────────────────────────────────────
def render_demographics_and_segmentation():
    st.markdown('<div class="section-title">6. Operational Segmentation — Locations &amp; Trainers</div>', unsafe_allow_html=True)

    col_d1, col_d2 = st.columns([1, 1])

    with col_d1:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="🏢 Volume &amp; Delivery by Client Facility",
            significance="Examines whether communication drop-offs cluster at particular manufacturing plants, regional training hubs, or virtual centers.",
            calculation="Cross-tab client_location x status, sorted descending by total facility volume. Top 6 facilities as stacked horizontal bars with per-segment count labels.",
            action="Target the Unknown/Virtual segment where 88.9% of notifications fail — enforce location tagging at onboarding."
        )

        loc_ct = pd.crosstab(filtered_df['client_location'], filtered_df['status']).fillna(0)
        for col in ['SENT','FAILED','SKIPPED']:
            if col not in loc_ct.columns: loc_ct[col] = 0
        loc_ct['TOTAL'] = loc_ct.sum(axis=1)
        loc_top  = loc_ct.sort_values(by='TOTAL', ascending=True).tail(6)
        y_labels = [l[:30]+'...' if len(l) > 30 else l for l in loc_top.index]

        fig_loc = go.Figure()
        for status, color in [('SENT',STATUS_COLORS['SENT']),('SKIPPED',STATUS_COLORS['SKIPPED']),('FAILED',STATUS_COLORS['FAILED'])]:
            fig_loc.add_trace(go.Bar(
                y=y_labels, x=loc_top[status], name=status, orientation='h',
                marker_color=color, marker_line=dict(color='white', width=1),
                text=[f"<b>{int(v):,}</b>" if v > 50 else "" for v in loc_top[status]],
                textposition='inside', textfont=dict(size=11.5, color='white', family='Inter'),
                insidetextanchor='middle',
                hovertemplate=f"<b>%{{y}}</b><br>{status}: %{{x:,}}<extra></extra>"
            ))
        fig_loc.update_layout(
            barmode='stack',
            xaxis=dict(title="Delivery Attempts", showgrid=True, gridcolor='#f1f5f9'),
            yaxis=dict(showgrid=False, tickfont=dict(size=12)),
            bargap=0.25
        )
        st.plotly_chart(apply_exec_chart_theme(fig_loc, height=400, pad_l=15, pad_r=40, pad_t=55, pad_b=40))
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d2:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="👨‍🏫 Delivery Success by Assigned Trainer",
            significance="Identifies operational discrepancies across training coordinators — ensures candidate class schedules are reliably delivered regardless of instructor.",
            calculation="Cross-tab trainer_name x status, sorted descending by total assigned attempts. Top 6 trainers as stacked horizontal bars with per-segment labels.",
            action="Standardize backend payload generation per trainer assignment to ensure consistent WhatsApp template parameter injection."
        )

        tr_ct = pd.crosstab(filtered_df['trainer_name'], filtered_df['status']).fillna(0)
        for col in ['SENT','FAILED','SKIPPED']:
            if col not in tr_ct.columns: tr_ct[col] = 0
        tr_ct['TOTAL'] = tr_ct.sum(axis=1)
        tr_top   = tr_ct.sort_values(by='TOTAL', ascending=True).tail(6)
        y_labels_tr = [l[:28]+'...' if len(l) > 28 else l for l in tr_top.index]

        fig_tr = go.Figure()
        for status, color in [('SENT',STATUS_COLORS['SENT']),('SKIPPED',STATUS_COLORS['SKIPPED']),('FAILED',STATUS_COLORS['FAILED'])]:
            fig_tr.add_trace(go.Bar(
                y=y_labels_tr, x=tr_top[status], name=status, orientation='h',
                marker_color=color, marker_line=dict(color='white', width=1),
                text=[f"<b>{int(v):,}</b>" if v > 50 else "" for v in tr_top[status]],
                textposition='inside', textfont=dict(size=11.5, color='white', family='Inter'),
                insidetextanchor='middle',
                hovertemplate=f"<b>%{{y}}</b><br>{status}: %{{x:,}}<extra></extra>"
            ))
        fig_tr.update_layout(
            barmode='stack',
            xaxis=dict(title="Delivery Attempts", showgrid=True, gridcolor='#f1f5f9'),
            yaxis=dict(showgrid=False, tickfont=dict(size=12)),
            bargap=0.25
        )
        st.plotly_chart(apply_exec_chart_theme(fig_tr, height=400, pad_l=15, pad_r=40, pad_t=55, pad_b=40))
        st.markdown('</div>', unsafe_allow_html=True)


# ── 8. Action Plan & Triage ───────────────────────────────────────────────────
def render_action_plan_and_triage():
    st.markdown('<div class="section-title">7. What to Fix — Action Plan &amp; Failure Lookup</div>', unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(f"""<div class="exec-card" style="border-top:4px solid {PALETTE['crimson']};">
            <div style="font-weight:800;font-size:13px;color:{PALETTE['crimson']};">🔴 PRIORITY 1 — Fix Today</div>
            <div style="font-weight:700;color:{PALETTE['navy']};margin:6px 0;font-size:14px;">WhatsApp Message Error</div>
            <div style="font-size:12px;color:{PALETTE['muted']};margin-bottom:8px;line-height:1.6;">1,090 messages failed because a required field (date / trainer name) was missing from the WhatsApp template.</div>
            <div style="font-size:12px;font-weight:700;color:{STATUS_COLORS['SENT']};">⏱ 1 day to fix · Recovers 1,090 deliveries</div></div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""<div class="exec-card" style="border-top:4px solid {PALETTE['coral']};">
            <div style="font-weight:800;font-size:13px;color:{PALETTE['coral']};">🟠 PRIORITY 2 — Fix This Week</div>
            <div style="font-weight:700;color:{PALETTE['navy']};margin:6px 0;font-size:14px;">Mobile Push Not Saving Device ID</div>
            <div style="font-size:12px;color:{PALETTE['muted']};margin-bottom:8px;line-height:1.6;">1,239 push attempts were skipped because the app did not record the device token when candidates logged in.</div>
            <div style="font-size:12px;font-weight:700;color:{STATUS_COLORS['SENT']};">⏱ 3–5 days to fix · Recovers 1,239 deliveries</div></div>""", unsafe_allow_html=True)
    with r3:
        st.markdown(f"""<div class="exec-card" style="border-top:4px solid {PALETTE['amber']};">
            <div style="font-weight:800;font-size:13px;color:{PALETTE['amber']};">🟡 PRIORITY 3 — Fix This Sprint</div>
            <div style="font-weight:700;color:{PALETTE['navy']};margin:6px 0;font-size:14px;">Collect Email at Online Registration</div>
            <div style="font-size:12px;color:{PALETTE['muted']};margin-bottom:8px;line-height:1.6;">371 online candidates had no email on file — making them impossible to reach when WhatsApp and Push both failed.</div>
            <div style="font-size:12px;font-weight:700;color:{STATUS_COLORS['SENT']};">⏱ 2 days to fix · Saves 584 candidates</div></div>""", unsafe_allow_html=True)
    with r4:
        st.markdown(f"""<div class="exec-card" style="border-top:4px solid {PALETTE['sky']};">
            <div style="font-weight:800;font-size:13px;color:{PALETTE['sky']};">🔵 PRIORITY 4 — Regulatory Track</div>
            <div style="font-weight:700;color:{PALETTE['navy']};margin:6px 0;font-size:14px;">Activate SMS as Backup Channel</div>
            <div style="font-size:12px;color:{PALETTE['muted']};margin-bottom:8px;line-height:1.6;">All 6 SMS attempts failed due to a pending government approval (India DLT). Once approved, SMS becomes a valuable offline fallback.</div>
            <div style="font-size:12px;font-weight:700;color:{STATUS_COLORS['SENT']};">⏱ ~1 week · Activates full SMS fallback</div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="plot-card" style="margin-top:24px;">', unsafe_allow_html=True)
    render_chart_header(
        title="🔍 Failure Lookup — Search Any Candidate or Delivery",
        significance="Use this to investigate a specific candidate, look up why their message failed, or export a filtered list for the engineering team to act on.",
        calculation="Search by candidate name, ID, or booking reference. Filter by delivery status or failure reason. All results can be downloaded as a CSV file.",
        action="Export the filtered FAILED records and share with the engineering team as a ready-made ticket with the exact error reasons attached."
    )

    col_s1, col_s2, col_s3 = st.columns([1.5, 1, 1])
    with col_s1: search_q = st.text_input("Search by Candidate Name, ID, or Booking Reference", "")
    with col_s2: status_f = st.selectbox("Filter by Status", ["All","FAILED","SKIPPED","SENT"])
    with col_s3: error_f  = st.selectbox("Filter by Failure Reason", ["All"] + list(filtered_df['error_message'].unique()))

    exp_df = filtered_df.copy()
    if search_q:
        q = search_q.lower()
        exp_df = exp_df[
            exp_df['candidate_name'].astype(str).str.lower().str.contains(q) |
            exp_df['candidate_id'].astype(str).str.lower().str.contains(q) |
            exp_df['external_ref_id'].astype(str).str.lower().str.contains(q)
        ]
    if status_f != "All": exp_df = exp_df[exp_df['status'] == status_f]
    if error_f  != "All": exp_df = exp_df[exp_df['error_message'] == error_f]

    cols = ['notification_id','candidate_name','channel','status','error_message',
            'trigger_type','client_location','trainer_name','notification_date']
    st.dataframe(exp_df[cols], height=320, use_container_width=True)
    st.download_button(
        label="📥 Download Triage Data as CSV",
        data=exp_df.to_csv(index=False).encode('utf-8'),
        file_name=f"notification_engine_triage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# 6. ORCHESTRATION
# ==============================================================================
if dashboard_mode == "📄 Full Report (All Sections)":
    render_executive_kpis()
    render_what_if_simulator()
    render_funnel_and_leakage()
    render_channels_and_providers()
    render_triggers_and_templates()
    render_time_series()
    render_demographics_and_segmentation()
    render_action_plan_and_triage()
else:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Summary & Simulator",
        "🔻 Delivery Funnel",
        "📱 Channel Breakdown",
        "⚡ Onsite vs. Online",
        "📈 Trends & Heatmaps",
        "📍 Locations & Trainers",
        "🛠️ Fix Plan & Lookup"
    ])
    with tab1:
        render_executive_kpis()
        render_what_if_simulator()
    with tab2:
        render_funnel_and_leakage()
    with tab3:
        render_channels_and_providers()
    with tab4:
        render_triggers_and_templates()
    with tab5:
        render_time_series()
    with tab6:
        render_demographics_and_segmentation()
    with tab7:
        render_action_plan_and_triage()

st.markdown(f"""
<div style="text-align:center;color:{PALETTE['muted']};font-size:11.5px;margin-top:40px;padding:18px;border-top:1px solid {PALETTE['border']};">
    Executive Notification Engine Analytics · Designed for C-Suite Briefings · Reference: Interakt Leads Analytics Report
</div>
""", unsafe_allow_html=True)
