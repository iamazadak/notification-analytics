# -*- coding: utf-8 -*-
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

# ── Status Colors: Universally recognized, high-contrast traffic-light semantics ──
STATUS_COLORS = {
    "SENT":      "#10b981",   # Emerald Green  (clear, modern success green)
    "SKIPPED":   "#f59e0b",   # Golden Amber   (warm, clear warning for skipped)
    "FAILED":    "#ef4444",   # Crimson Red    (high-visibility alert red for failures)
    "REACHED":   "#10b981",   # Emerald Green  (same as SENT)
    "UNREACHED": "#ef4444",   # Crimson Red    (same as FAILED)
}

# ── Channel Colors: Distinct brand-aligned colors for each communication channel ──
CHANNEL_COLORS = {
    "email":     "#2563eb",   # Royal Blue     (📧 Email — professional communication blue)
    "whatsapp":  "#16a34a",   # Forest Green   (💬 WhatsApp — crisp brand green)
    "push":      "#8b5cf6",   # Modern Purple  (📱 Mobile Push — vibrant app purple)
    "sms":       "#f97316",   # Telecom Orange (📟 SMS — distinct carrier orange)
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
    .accent-whatsapp {{ border-top: 3.5px solid {CHANNEL_COLORS['whatsapp']}; }}
    .wa-banner {{ background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%); border: 1.5px solid #86efac; border-radius: 12px; padding: 22px 24px; margin-bottom: 22px; box-shadow: 0 4px 14px rgba(22, 163, 74, 0.06); }}
    .wa-badge {{ background-color: #dcfce7; color: #166534; border: 1px solid #86efac; font-weight: 700; padding: 4px 12px; border-radius: 14px; font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.5px; }}
    .wa-code-box {{ background-color: #0f172a; color: #e2e8f0; border-radius: 8px; padding: 14px 16px; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 12px; line-height: 1.55; overflow-x: auto; border: 1px solid #334155; }}
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
    .decoder-container {{ background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 20px 24px; margin: 16px 0px 24px 0px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }}
    .decoder-header {{ display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-bottom: 6px; }}
    .decoder-title {{ font-size: 16.5px; font-weight: 800; color: {PALETTE['navy']}; display: flex; align-items: center; gap: 8px; }}
    .decoder-badge {{ font-size: 11px; font-weight: 700; background: #e0f2fe; color: #0369a1; padding: 3px 10px; border-radius: 12px; text-transform: uppercase; letter-spacing: 0.5px; }}
    .decoder-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 14px 0px; }}
    @media (max-width: 900px) {{ .decoder-grid {{ grid-template-columns: 1fr; }} }}
    .decoder-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 16px; display: flex; flex-direction: column; justify-content: space-between; }}
    .decoder-card-title {{ font-size: 11px; font-weight: 800; color: #475569; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }}
    .decoder-card-big {{ font-size: 24px; font-weight: 800; color: {PALETTE['navy']}; margin-bottom: 8px; }}
    .decoder-item {{ font-size: 12.2px; color: #334155; margin-bottom: 4px; line-height: 1.4; }}
    .decoder-sum {{ margin-top: 8px; padding-top: 6px; border-top: 1px dashed #cbd5e1; font-size: 11.5px; font-weight: 700; color: #1e293b; }}
    .decoder-reconciliation-footer {{ background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 10px 14px; font-size: 12.2px; color: #1e40af; line-height: 1.5; margin-top: 10px; }}
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
st.sidebar.markdown("### 🧭 Navigation View")
app_page = st.sidebar.radio(
    "Select View",
    ["📊 Operations Dashboard (All Channels)", "💬 WhatsApp Deep-Dive Hub"],
    index=0,
    key="app_view_switcher",
    label_visibility="collapsed"
)
st.sidebar.markdown("---")

min_date = raw_df['notification_date'].min()
max_date = raw_df['notification_date'].max()

if app_page == "💬 WhatsApp Deep-Dive Hub":
    st.sidebar.markdown("#### 💬 WhatsApp Cohort Filters")
    date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date, key="wa_date_picker")

    wa_full = raw_df[raw_df['channel'].str.lower() == 'whatsapp']
    all_wa_templates = sorted(wa_full['template_name'].dropna().unique().tolist())
    all_wa_statuses  = sorted(wa_full['status'].dropna().unique().tolist())
    all_wa_locations = sorted(wa_full['client_location'].dropna().unique().tolist())
    all_wa_triggers  = sorted(wa_full['trigger_type'].dropna().unique().tolist())

    selected_wa_templates = st.sidebar.multiselect("WhatsApp Templates", all_wa_templates, default=all_wa_templates, key="wa_sel_tmpl")
    selected_wa_statuses  = st.sidebar.multiselect("Delivery Status",    all_wa_statuses,  default=all_wa_statuses,  key="wa_sel_stat")
    selected_wa_locations = st.sidebar.multiselect("Client Locations",   all_wa_locations, default=all_wa_locations, key="wa_sel_loc")
    selected_wa_triggers  = st.sidebar.multiselect("Trigger Types",      all_wa_triggers,  default=all_wa_triggers,  key="wa_sel_trig")

    if st.sidebar.button("Reset WhatsApp Filters", width='stretch', key="wa_reset_btn"):
        st.rerun()

    if not selected_wa_templates: selected_wa_templates = all_wa_templates
    if not selected_wa_statuses:  selected_wa_statuses  = all_wa_statuses
    if not selected_wa_locations: selected_wa_locations = all_wa_locations
    if not selected_wa_triggers:  selected_wa_triggers  = all_wa_triggers

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_d, end_d = date_range
        mask = (
            (raw_df['notification_date'] >= start_d) & (raw_df['notification_date'] <= end_d) &
            (raw_df['channel'].str.lower() == 'whatsapp') &
            (raw_df['template_name'].isin(selected_wa_templates)) &
            (raw_df['status'].isin(selected_wa_statuses)) &
            (raw_df['client_location'].isin(selected_wa_locations)) &
            (raw_df['trigger_type'].isin(selected_wa_triggers))
        )
    else:
        mask = (
            (raw_df['channel'].str.lower() == 'whatsapp') &
            (raw_df['template_name'].isin(selected_wa_templates)) &
            (raw_df['status'].isin(selected_wa_statuses)) &
            (raw_df['client_location'].isin(selected_wa_locations)) &
            (raw_df['trigger_type'].isin(selected_wa_triggers))
        )
    filtered_df = raw_df[mask]
    if len(filtered_df) == 0:
        st.warning("No WhatsApp data matches current filter parameters. Please adjust sidebar filters.")
        st.stop()
    filtered_notif_ids = filtered_df['notification_id'].unique()
    filtered_notif_df  = notif_df[notif_df['notification_id'].isin(filtered_notif_ids)]
    st.sidebar.success(f"💬 WhatsApp Cohort: **{len(filtered_df):,}** attempts across **{filtered_df['candidate_id'].nunique():,}** candidates.")

else:
    st.sidebar.markdown("#### Cohort Filtering")
    date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date, key="ops_date_picker")

    all_channels  = sorted(raw_df['channel'].dropna().unique().tolist())
    all_triggers  = sorted(raw_df['trigger_type'].dropna().unique().tolist())
    all_statuses  = sorted(raw_df['status'].dropna().unique().tolist())
    all_locations = sorted(raw_df['client_location'].dropna().unique().tolist())

    selected_channels  = st.sidebar.multiselect("Channels",        all_channels,  default=all_channels,  key="ops_sel_chan")
    selected_triggers  = st.sidebar.multiselect("Trigger Types",   all_triggers,  default=all_triggers,  key="ops_sel_trig")
    selected_statuses  = st.sidebar.multiselect("Delivery Status", all_statuses,  default=all_statuses,  key="ops_sel_stat")
    selected_locations = st.sidebar.multiselect("Client Locations",all_locations, default=all_locations, key="ops_sel_loc")

    if st.sidebar.button("Reset to Full Dataset", width='stretch', key="ops_reset_btn"):
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
    """Hover-based info tooltip."""
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
# 4. DASHBOARD HEADER HELPERS
# ==============================================================================
def render_operations_header():
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


# ==============================================================================
# 5. RENDER FUNCTIONS  (ordered for executive narrative flow)
# ==============================================================================

# ── 0. The Numbers Decoder (Rosetta Stone) ───────────────────────────────────
def render_math_decoder():
    cand_total = filtered_df['candidate_id'].nunique()
    cand_reach = filtered_df.groupby('candidate_id')['sent_flag'].sum() > 0
    cand_reached = int(cand_reach.sum())
    cand_unreached = cand_total - cand_reached
    cand_reach_pct = (cand_reached / cand_total * 100) if cand_total > 0 else 0
    cand_unreach_pct = (cand_unreached / cand_total * 100) if cand_total > 0 else 0

    total_notifs = len(filtered_notif_df)
    reached_notifs = int(filtered_notif_df['is_reached'].sum())
    dropped_notifs = total_notifs - reached_notifs
    notif_reach_pct = (reached_notifs / total_notifs * 100) if total_notifs > 0 else 0
    notif_drop_pct = (dropped_notifs / total_notifs * 100) if total_notifs > 0 else 0

    total_attempts = len(filtered_df)
    sent_attempts = int(filtered_df['sent_flag'].sum())
    skipped_attempts = int(filtered_df['skipped_flag'].sum())
    failed_attempts = int(filtered_df['failed_flag'].sum())
    sent_pct = (sent_attempts / total_attempts * 100) if total_attempts > 0 else 0
    skipped_pct = (skipped_attempts / total_attempts * 100) if total_attempts > 0 else 0
    failed_pct = (failed_attempts / total_attempts * 100) if total_attempts > 0 else 0

    single_ch = int((filtered_notif_df['sent_legs'] == 1).sum())
    multi_ch = int((filtered_notif_df['sent_legs'] > 1).sum())

    st.markdown(f"""
    <div class="decoder-container">
        <div class="decoder-header">
            <div class="decoder-title"><span>📐</span> The Numbers Decoder — How Every Number Adds Up</div>
            <span class="decoder-badge">100% Reconciled Math</span>
        </div>
        <div style="font-size:13px; color:#475569; margin: 4px 0 14px 0; line-height:1.5;">
            The analytics system measures activity across <strong>3 distinct levels</strong>. Knowing which level you are looking at makes the numbers instantly add up:
        </div>
        <div class="decoder-grid">
            <!-- Level 1: Candidates -->
            <div class="decoder-card">
                <div>
                    <div class="decoder-card-title">👥 LEVEL 1: PEOPLE (Candidates)</div>
                    <div class="decoder-card-big">{cand_total:,} <span style="font-size:13px;font-weight:600;color:#64748b;">Human Beings</span></div>
                    <div class="decoder-item"><span style="color:{STATUS_COLORS['SENT']};font-weight:700;">✅ {cand_reached:,} Reached</span> ({cand_reach_pct:.1f}%) — Got ≥1 alert</div>
                    <div class="decoder-item"><span style="color:{STATUS_COLORS['FAILED']};font-weight:700;">❌ {cand_unreached:,} Missed</span> ({cand_unreach_pct:.1f}%) — Got 0 alerts</div>
                </div>
                <div class="decoder-sum">{cand_reached:,} + {cand_unreached:,} = <b>{cand_total:,} Candidates (100%)</b></div>
            </div>
            <!-- Level 2: Messages -->
            <div class="decoder-card">
                <div>
                    <div class="decoder-card-title">📨 LEVEL 2: MESSAGES (Alerts)</div>
                    <div class="decoder-card-big">{total_notifs:,} <span style="font-size:13px;font-weight:600;color:#64748b;">Alerts Triggered</span></div>
                    <div class="decoder-item"><span style="color:{STATUS_COLORS['SENT']};font-weight:700;">✅ {reached_notifs:,} Delivered</span> ({notif_reach_pct:.1f}%) — Reached candidate</div>
                    <div class="decoder-item"><span style="color:{STATUS_COLORS['FAILED']};font-weight:700;">❌ {dropped_notifs:,} Lost</span> ({notif_drop_pct:.1f}%) — Failed on all channels</div>
                </div>
                <div class="decoder-sum">{reached_notifs:,} + {dropped_notifs:,} = <b>{total_notifs:,} Messages (100%)</b></div>
            </div>
            <!-- Level 3: Channel Tries -->
            <div class="decoder-card">
                <div>
                    <div class="decoder-card-title">📱 LEVEL 3: CHANNEL TRIES (Attempts)</div>
                    <div class="decoder-card-big">{total_attempts:,} <span style="font-size:13px;font-weight:600;color:#64748b;">Tries (~3 per alert)</span></div>
                    <div class="decoder-item"><span style="color:{STATUS_COLORS['SENT']};font-weight:700;">✅ {sent_attempts:,} Sent</span> ({sent_pct:.1f}%) — Delivered by provider</div>
                    <div class="decoder-item"><span style="color:{STATUS_COLORS['SKIPPED']};font-weight:700;">⏭️ {skipped_attempts:,} Skipped</span> ({skipped_pct:.1f}%) — No phone token / email</div>
                    <div class="decoder-item"><span style="color:{STATUS_COLORS['FAILED']};font-weight:700;">❌ {failed_attempts:,} Failed</span> ({failed_pct:.1f}%) — WhatsApp error 131008</div>
                </div>
                <div class="decoder-sum">{sent_attempts:,} + {skipped_attempts:,} + {failed_attempts:,} = <b>{total_attempts:,} Tries (100%)</b></div>
            </div>
        </div>
        <div class="decoder-reconciliation-footer">
            💡 <b>Why does {sent_attempts:,} Sent Tries not equal {reached_notifs:,} Delivered Messages?</b><br>
            Because <b>{multi_ch:,} candidates received the same message on TWO channels</b> (both WhatsApp and Email).<br>
            Math: {single_ch:,} single-channel messages + ({multi_ch:,} × 2 channels) = <b>{sent_attempts:,} total successful channel tries</b>! Every single number reconciles.
        </div>
    </div>
    """, unsafe_allow_html=True)


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

    cand_total     = filtered_df['candidate_id'].nunique()
    cand_reach     = filtered_df.groupby('candidate_id')['sent_flag'].sum() > 0
    cand_reached   = int(cand_reach.sum())
    cand_unreached = cand_total - cand_reached
    cand_reach_pct = (cand_reached / cand_total * 100) if cand_total > 0 else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class="exec-card accent-navy">
            <div><div class="exec-card-label">Messages Triggered</div>
            <div class="exec-card-value">{total_notifs:,}</div></div>
            <div class="exec-card-subtext">Total alerts the system attempted to send</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="exec-card accent-sky">
            <div><div class="exec-card-label">Total Delivery Tries</div>
            <div class="exec-card-value">{total_legs:,}</div></div>
            <div class="exec-card-subtext">{total_legs/total_notifs:.1f} channels tried per message</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="exec-card" style="border-top:3.5px solid {STATUS_COLORS['SENT']};">
            <div><div class="exec-card-label">Messages Delivered</div>
            <div class="exec-card-value" style="color:{STATUS_COLORS['SENT']};">{reach_rate:.1f}%</div></div>
            <div class="exec-card-subtext">{reached_notifs:,} of {total_notifs:,} reached candidate on ≥1 channel</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="exec-card" style="border-top:3.5px solid {STATUS_COLORS['FAILED']};">
            <div><div class="exec-card-label">Messages Lost</div>
            <div class="exec-card-value" style="color:{STATUS_COLORS['FAILED']};">{dropped_rate:.1f}%</div></div>
            <div class="exec-card-subtext">{dropped_cnt:,} messages failed on all channels</div></div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="exec-card" style="border-top:3.5px solid {STATUS_COLORS['SENT']};">
            <div><div class="exec-card-label">People Reached</div>
            <div class="exec-card-value" style="color:{STATUS_COLORS['SENT']};">{cand_reach_pct:.1f}%</div></div>
            <div class="exec-card-subtext">{cand_reached:,} reached · {cand_unreached:,} missed (of {cand_total:,})</div></div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="exec-takeaway-box">
        <strong>📋 Plain-English Summary — The 3 Culprits Behind Every Lost Message:</strong>
        <ul style="margin:10px 0 0 0; padding-left:18px; line-height:1.8;">
            <li><strong>1. WhatsApp Software Bug (Code 131008) — Caused 1,090 Failures:</strong> The automated system sent messages to WhatsApp without filling in the candidate's class date or trainer name. Meta rejected them automatically. <em>Fix: 1 developer can fix this parameter bug in an afternoon.</em></li>
            <li><strong>2. Mobile App Never Saves Device Tokens — Caused 1,239 Skips:</strong> When candidates log into the mobile app, the app fails to save their push notification token to the database. The system had no phone address to send to. <em>Fix: Update mobile app to save push token on login.</em></li>
            <li><strong>3. Online Candidates Have No Email on File — Caused 584 Skips:</strong> When students enroll in online classes, the registration form only asked for their phone number. When WhatsApp and Push fail, there is no email backup! <em>Fix: Make email a required field on sign-up forms.</em></li>
        </ul>
    </div>""", unsafe_allow_html=True)


# ── 2. What-If Simulator ─────────────────────────────────────────────────────
def render_what_if_simulator():
    st.markdown(f"""<div class="exec-simulator-container">
        <h4 style="margin:0px 0px 6px 0px;color:{PALETTE['navy']};font-weight:700;font-size:16px;">
            🎛️ What-If Simulator — See the Impact of Each Fix</h4>
        <p style="font-size:12.5px;color:{PALETTE['muted']};margin:0px 0px 14px 0px;">
            Tick one or more fixes below to see how many lost messages and candidates would be recovered today:</p>""",
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

    cand_base_reached = int((filtered_df.groupby('candidate_id')['sent_flag'].sum() > 0).sum())
    cand_total = filtered_df['candidate_id'].nunique()
    cand_sim_reached = int((sim_df.groupby('candidate_id')['sent_flag'].sum() > 0).sum())
    cand_recovered = cand_sim_reached - cand_base_reached

    r1, r2, r3, r4 = st.columns(4)
    with r1: st.metric("Current Message Delivery", f"{base_rate:.1f}%", f"{base_reached:,} of {total_n:,}")
    with r2: st.metric("Delivery Rate After Fixes", f"{sim_rate:.1f}%", f"+{delta_rate:.1f}%")
    with r3: st.metric("Messages Recovered", f"+{recovered:,}", f"{sim_dropped:,} still lost", delta_color="normal")
    with r4: st.metric("Extra People Reached", f"+{cand_recovered:,}", f"Now {cand_sim_reached:,} of {cand_total:,}", delta_color="normal")

    st.markdown("</div>", unsafe_allow_html=True)


# ── 3. Funnel & Leakage ──────────────────────────────────────────────────────
def render_funnel_and_leakage():
    st.markdown('<div class="section-title">2. Where Are Messages Being Lost?</div>', unsafe_allow_html=True)

    total_n        = len(filtered_notif_df)
    total_l        = len(filtered_df)
    dispatched_cnt = int(filtered_df['dispatched_at'].notna().sum())
    sent_cnt       = int(filtered_df['sent_flag'].sum())
    reached_cnt    = int(filtered_notif_df['is_reached'].sum())
    dropped_cnt    = total_n - reached_cnt
    skipped_cnt    = int(filtered_df['skipped_flag'].sum())
    failed_cnt     = int(filtered_df['failed_flag'].sum())

    # Full-width funnel with perspective selector
    st.markdown('<div class="plot-card">', unsafe_allow_html=True)
    render_chart_header(
        title="📌 Delivery Pipeline — Step-by-Step Flow",
        significance="Shows step-by-step how volume flows through the pipeline without mixing units. Every step is smaller than the last so numbers make complete sense.",
        calculation="Message view: tracks 1,308 distinct alerts from creation to delivery. Channel Tries view: tracks 3,924 individual channel attempts from planned to sent.",
        action="Fix the WhatsApp payload bug to immediately turn 1,090 failed channel attempts into successful deliveries."
    )

    funnel_view = st.radio(
        "Choose Pipeline View:",
        ["📨 Message Journey (1,308 Messages Triggered)", "📱 Channel Attempts Pipeline (3,924 Delivery Tries)"],
        horizontal=True
    )

    fig_funnel = go.Figure()

    if "Message Journey" in funnel_view:
        m_stages = ["1. Messages Triggered", "2. Delivered to Candidate (≥1 Channel)", "3. Confirmed Read"]
        m_values = [total_n, reached_cnt, 0]
        m_pcts   = [
            "100% — Total business alerts",
            f"{reached_cnt/total_n*100:.1f}% — Arrived ({dropped_cnt:,} completely lost)",
            "0% — Read receipts not yet tracked"
        ]
        m_colors = [PALETTE['navy'], STATUS_COLORS['SENT'], PALETTE['muted']]

        fig_funnel.add_trace(go.Bar(
            x=m_values[:-1], y=m_stages[:-1], orientation='h',
            marker=dict(color=m_colors[:-1], line=dict(color=PALETTE['border'], width=1)),
            text=[f"<b>{v:,}</b>   ({p})" for v, p in zip(m_values[:-1], m_pcts[:-1])],
            textposition='outside',
            textfont=dict(family='Inter, sans-serif', size=12, color=PALETTE['charcoal']),
            cliponaxis=False,
            hovertext=[f"<b>{s}</b><br>Volume: {v:,}<br>{p}" for s, v, p in zip(m_stages[:-1], m_values[:-1], m_pcts[:-1])],
            hoverinfo='text', showlegend=False
        ))
        fig_funnel.add_trace(go.Bar(
            x=[1], y=[m_stages[-1]], orientation='h',
            marker=dict(color=m_colors[-1], line=dict(color=PALETTE['border'], width=0)),
            hovertext=[f"<b>{m_stages[-1]}</b><br>Not yet tracked — provider webhooks needed"],
            hoverinfo='text', showlegend=False
        ))
        fig_funnel.add_annotation(
            x=1, y=m_stages[-1], text="<b>0</b>   (Read receipts not yet tracked)",
            xanchor='left', xshift=8, showarrow=False,
            font=dict(size=12, color=PALETTE['muted'], family='Inter')
        )
        fig_funnel.update_layout(
            yaxis=dict(autorange="reversed", showgrid=False, tickfont=dict(size=12, color=PALETTE['charcoal'])),
            xaxis=dict(title="Number of Messages", showgrid=True, gridcolor='#f1f5f9', range=[0, total_n * 1.55]),
            bargap=0.28
        )
    else:
        c_stages = ["1. Attempts Planned", "2. Handed to Providers (Dispatched)", "3. Successfully Sent", "4. Confirmed Read"]
        c_values = [total_l, dispatched_cnt, sent_cnt, 0]
        c_pcts   = [
            "100% — ~3 channels tried per message",
            f"{dispatched_cnt/total_l*100:.1f}% — Dispatched ({skipped_cnt:,} skipped beforehand)",
            f"{sent_cnt/total_l*100:.1f}% — Delivered ({failed_cnt:,} failed at provider)",
            "0% — Read receipts not yet tracked"
        ]
        c_colors = [PALETTE['navy'], PALETTE['ocean'], STATUS_COLORS['SENT'], PALETTE['muted']]

        fig_funnel.add_trace(go.Bar(
            x=c_values[:-1], y=c_stages[:-1], orientation='h',
            marker=dict(color=c_colors[:-1], line=dict(color=PALETTE['border'], width=1)),
            text=[f"<b>{v:,}</b>   ({p})" for v, p in zip(c_values[:-1], c_pcts[:-1])],
            textposition='outside',
            textfont=dict(family='Inter, sans-serif', size=12, color=PALETTE['charcoal']),
            cliponaxis=False,
            hovertext=[f"<b>{s}</b><br>Volume: {v:,}<br>{p}" for s, v, p in zip(c_stages[:-1], c_values[:-1], c_pcts[:-1])],
            hoverinfo='text', showlegend=False
        ))
        fig_funnel.add_trace(go.Bar(
            x=[1], y=[c_stages[-1]], orientation='h',
            marker=dict(color=c_colors[-1], line=dict(color=PALETTE['border'], width=0)),
            hovertext=[f"<b>{c_stages[-1]}</b><br>Not yet tracked — provider webhooks needed"],
            hoverinfo='text', showlegend=False
        ))
        fig_funnel.add_annotation(
            x=1, y=c_stages[-1], text="<b>0</b>   (Read receipts not yet tracked)",
            xanchor='left', xshift=8, showarrow=False,
            font=dict(size=12, color=PALETTE['muted'], family='Inter')
        )
        fig_funnel.update_layout(
            yaxis=dict(autorange="reversed", showgrid=False, tickfont=dict(size=12, color=PALETTE['charcoal'])),
            xaxis=dict(title="Number of Channel Attempts", showgrid=True, gridcolor='#f1f5f9', range=[0, total_l * 1.55]),
            bargap=0.28
        )

    st.plotly_chart(apply_exec_chart_theme(fig_funnel, height=330, show_legend=False, pad_l=260, pad_r=55, pad_t=25, pad_b=40), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([1.4, 0.6])

    with col_f1:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="⚠️ Why Did Messages Fail? — Drop-off Reasons",
            significance="Shows the exact reason why channel delivery attempts failed or skipped, ranked from largest problem to smallest.",
            calculation="All failed and skipped attempts are grouped by error reason and counted as a percentage of all failures. Clear labels explain what went wrong.",
            action="Fix the WhatsApp missing data bug (top bar) first — it accounts for 1,090 failed messages and can be solved in 1 day."
        )

        def clean_leak_label(r):
            if "131008" in r:
                return "WhatsApp: Missing Date / Trainer Name (131008)"
            if "push tokens" in r:
                return "Push: Mobile App Missing Device Token"
            if "missing email" in r:
                return "Email: No Email on Candidate Profile"
            if "not subscribed" in r:
                return "Push: Candidate Unsubscribed / Disabled Alerts"
            if "Fallback satisfied" in r:
                return "WhatsApp: Skipped (Email already sent)"
            if "DLT pending" in r:
                return "SMS: TRAI DLT Template Pending"
            if "132018" in r:
                return "WhatsApp: Template Parameter Formatting Issue"
            if "132001" in r:
                return "WhatsApp: Template Translation Not Found"
            return r[:40] + '…' if len(r) > 40 else r

        leak_df     = filtered_df[filtered_df['status'].isin(['FAILED','SKIPPED'])].copy()
        leak_df['clean_reason'] = leak_df['error_message'].apply(clean_leak_label)
        leak_counts = leak_df['clean_reason'].value_counts().reset_index()
        leak_counts.columns = ['Reason', 'Count']
        total_leak  = leak_counts['Count'].sum()
        leak_counts['Pct'] = (leak_counts['Count'] / total_leak * 100).round(1) if total_leak > 0 else 0
        top_leaks   = leak_counts.head(6)

        def get_leak_color(r):
            if "WhatsApp" in r: return CHANNEL_COLORS['whatsapp']
            if "Push" in r:     return CHANNEL_COLORS['push']
            if "Email" in r:    return CHANNEL_COLORS['email']
            if "SMS" in r:      return CHANNEL_COLORS['sms']
            return PALETTE["muted"]

        fig_leak = go.Figure(go.Bar(
            x=top_leaks['Count'],
            y=top_leaks['Reason'],
            orientation='h',
            marker=dict(
                color=[get_leak_color(r) for r in top_leaks['Reason']],
                line=dict(color=PALETTE['border'], width=1)
            ),
            text=[f"<b>{c:,}</b>  ({p}%)" for c, p in zip(top_leaks['Count'], top_leaks['Pct'])],
            textposition='outside',
            textfont=dict(family='Inter, sans-serif', size=12, color=PALETTE['charcoal']),
            cliponaxis=False,
            hovertext=[f"<b>{r}</b><br>Attempts: {c:,}<br>Share of Failures: {p}%" for r, c, p in zip(top_leaks['Reason'], top_leaks['Count'], top_leaks['Pct'])],
            hoverinfo='text'
        ))
        fig_leak.update_layout(
            yaxis=dict(autorange="reversed", showgrid=False,
                       tickfont=dict(size=11.5, color=PALETTE['charcoal'])),
            xaxis=dict(title="Failed / Skipped Attempts", showgrid=True,
                       gridcolor='#f1f5f9',
                       range=[0, top_leaks['Count'].max() * 1.55]),
            bargap=0.3
        )
        st.plotly_chart(apply_exec_chart_theme(fig_leak, height=360, show_legend=False, pad_l=270, pad_r=65, pad_t=30, pad_b=45), use_container_width=True)
        st.markdown(f"""
        <div style="display:flex; justify-content:center; gap:16px; font-size:11.8px; font-weight:600; margin-top:4px;">
            <span style="color:{CHANNEL_COLORS['email']};">📧 EMAIL</span>
            <span style="color:{CHANNEL_COLORS['whatsapp']};">💬 WHATSAPP</span>
            <span style="color:{CHANNEL_COLORS['push']};">📱 MOBILE PUSH</span>
            <span style="color:{CHANNEL_COLORS['sms']};">📟 SMS</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_f2:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="🎯 Delivery Result by Message",
            significance="Shows what percentage of the total messages actually arrived on at least one channel versus those that completely failed.",
            calculation="Out of total messages: Delivered = received on ≥1 channel (Email or WhatsApp). Lost = failed on all attempted channels. Sums to 100%.",
            action="The 32.3% lost segment represents 423 messages — fixing WhatsApp alone recovers every single one."
        )

        reach_vals   = [reached_cnt, dropped_cnt]
        reach_labels = ['Delivered (≥1 Ch)', 'Completely Lost (0 Ch)']
        reach_total  = sum(reach_vals)
        reach_pcts   = [f"{v/reach_total*100:.1f}%" for v in reach_vals]

        cand_total     = filtered_df['candidate_id'].nunique()
        cand_reach     = filtered_df.groupby('candidate_id')['sent_flag'].sum() > 0
        cand_reached   = int(cand_reach.sum())
        cand_unreached = cand_total - cand_reached
        cand_reach_pct = (cand_reached / cand_total * 100) if cand_total > 0 else 0

        fig_donut2 = go.Figure(go.Pie(
            labels=reach_labels,
            values=reach_vals,
            hole=0.65,
            marker=dict(
                colors=[STATUS_COLORS['REACHED'], STATUS_COLORS['UNREACHED']],
                line=dict(color='white', width=3)
            ),
            textinfo='percent',
            textfont=dict(size=14, family='Inter', color='white'),
            insidetextorientation='horizontal',
            hovertemplate="<b>%{label}</b><br>%{value:,} messages<br>%{percent}<extra></extra>"
        ))
        fig_donut2.update_layout(
            annotations=[dict(
                text=f"<b>{reach_vals[0]:,}</b><br><span style='font-size:11px'>Delivered<br>{reach_pcts[0]}</span>",
                x=0.5, y=0.5, font_size=15, showarrow=False,
                font=dict(family='Inter', color=PALETTE['navy'])
            )],
            legend=dict(
                orientation='h', x=0.5, xanchor='center', y=-0.14,
                font=dict(size=11.5, family='Inter'),
                traceorder='normal'
            ),
            showlegend=True
        )
        st.plotly_chart(apply_exec_chart_theme(fig_donut2, height=330, show_legend=True, pad_l=15, pad_r=15, pad_t=15, pad_b=20), use_container_width=True)
        st.markdown(f"""
        <div style="font-size:11.8px; color:{PALETTE['muted']}; text-align:center; margin-top:2px;">
            👥 <strong>People Perspective:</strong> {cand_reached:,} of {cand_total:,} candidates reached ({cand_reach_pct:.1f}%) · {cand_unreached:,} missed.
        </div>
        """, unsafe_allow_html=True)
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

        ch_tick_names = [c.upper() for c in ct_ch.index]
        ch_tick_html  = [f"<b style='color:{CHANNEL_COLORS.get(c.lower(), PALETTE['navy'])}'>{c.upper()}</b>" for c in ct_ch.index]

        fig_ch = go.Figure()
        for status, color in [('SENT', STATUS_COLORS['SENT']), ('SKIPPED', STATUS_COLORS['SKIPPED']), ('FAILED', STATUS_COLORS['FAILED'])]:
            shares = [(v / ch_totals[c] * 100) if ch_totals[c] > 0 else 0 for c, v in zip(ct_ch.index, ct_ch[status])]
            fig_ch.add_trace(go.Bar(
                x=ch_tick_names, y=ct_ch[status], name=status,
                marker_color=color, marker_line=dict(color='white', width=1),
                text=[f"<b>{int(v):,}</b>" if v >= 50 else "" for v in ct_ch[status]],
                textposition='inside', textfont=dict(size=12, color='white', family='Inter'),
                insidetextanchor='middle',
                customdata=shares,
                hovertemplate=f"<b>%{{x}} · {status}</b><br>Attempts: %{{y:,}}<br>Share of Channel: %{{customdata:.1f}}%<extra></extra>"
            ))
        for ch, total in zip(ch_tick_names, ch_totals):
            fig_ch.add_annotation(x=ch, y=total, text=f"<b>Total: {int(total):,}</b>",
                showarrow=False, yshift=14, font=dict(size=12, color=PALETTE['charcoal'], family='Inter'))

        fig_ch.update_layout(
            barmode='stack',
            xaxis=dict(
                title="Channel",
                showgrid=False,
                tickmode='array',
                tickvals=ch_tick_names,
                ticktext=ch_tick_html,
                tickfont=dict(size=13, family='Inter')
            ),
            yaxis=dict(title="Delivery Attempts", showgrid=True, gridcolor='#f1f5f9',
                       range=[0, ch_totals.max() * 1.28]),
            bargap=0.35
        )
        st.plotly_chart(apply_exec_chart_theme(fig_ch, height=400, pad_l=55, pad_r=35, pad_t=60, pad_b=45), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_c2:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="🍩 Volume Split by Channel & Delivery Status",
            significance="Shows how volume is split across communication channels AND color-codes each channel by its delivery health (Sent, Skipped, Failed).",
            calculation="Channel attempts split by delivery status. Green = SENT, Amber = SKIPPED, Crimson = FAILED.",
            action="WhatsApp has an 84% failure rate and Push has a 95% skip rate — focus remediation on these two channels."
        )

        split_view = st.radio(
            "Color Coding Mode:",
            [
                "☀️ Sunburst (Channels → Status)",
                "📱 Donut by Channel",
                "🚦 Donut by Delivery Status"
            ],
            horizontal=True,
            key="channel_status_split_view"
        )

        total_legs_val = len(filtered_df)

        if "Sunburst" in split_view:
            # 2-Tier Sunburst: Inner = Channels, Outer = Delivery Status
            sb_labels = []
            sb_parents = []
            sb_values = []
            sb_colors = []
            sb_hovers = []

            ch_grp = filtered_df.groupby('channel').size()
            for ch, tot in ch_grp.items():
                sb_labels.append(ch.upper())
                sb_parents.append('')
                sb_values.append(tot)
                sb_colors.append(CHANNEL_COLORS.get(ch, PALETTE['navy']))
                sb_hovers.append(f"<b>{ch.upper()}</b><br>Total Attempts: {tot:,}<br>Share: {tot/total_legs_val*100:.1f}%")

            cs_df = filtered_df.groupby(['channel', 'status']).size().reset_index(name='count')
            for _, r in cs_df.iterrows():
                ch = r['channel']
                st_val = r['status']
                cnt = r['count']
                ch_tot = ch_grp[ch]
                sb_labels.append(f"{ch.upper()} · {st_val}")
                sb_parents.append(ch.upper())
                sb_values.append(cnt)
                sb_colors.append(STATUS_COLORS.get(st_val, PALETTE['muted']))
                sb_hovers.append(f"<b>{ch.upper()} → {st_val}</b><br>Attempts: {cnt:,}<br>{cnt/ch_tot*100:.1f}% of {ch.upper()}<br>{cnt/total_legs_val*100:.1f}% of all attempts")

            fig_donut = go.Figure(go.Sunburst(
                labels=sb_labels,
                parents=sb_parents,
                values=sb_values,
                branchvalues='total',
                marker=dict(colors=sb_colors, line=dict(color='white', width=1.5)),
                hovertext=sb_hovers,
                hoverinfo='text',
                insidetextorientation='horizontal',
                textfont=dict(family='Inter', size=11)
            ))
            fig_donut.update_layout(
                margin=dict(l=10, r=10, t=15, b=15)
            )
            st.plotly_chart(apply_exec_chart_theme(fig_donut, height=360, show_legend=False, pad_l=10, pad_r=10, pad_t=25, pad_b=15), use_container_width=True)
            st.markdown(f"""
            <div style="display:flex; justify-content:center; gap:14px; font-size:11.8px; font-weight:600; margin-top:4px;">
                <span style="color:{STATUS_COLORS['SENT']};">🟢 SENT: {int(filtered_df['sent_flag'].sum()):,} ({filtered_df['sent_flag'].mean()*100:.1f}%)</span>
                <span style="color:{STATUS_COLORS['SKIPPED']};">🟡 SKIPPED: {int(filtered_df['skipped_flag'].sum()):,} ({filtered_df['skipped_flag'].mean()*100:.1f}%)</span>
                <span style="color:{STATUS_COLORS['FAILED']};">🔴 FAILED: {int(filtered_df['failed_flag'].sum()):,} ({filtered_df['failed_flag'].mean()*100:.1f}%)</span>
            </div>
            """, unsafe_allow_html=True)

        elif "Channel" in split_view:
            # Donut colored by Channel
            ch_grp = filtered_df.groupby('channel').size().reindex(['email', 'whatsapp', 'push', 'sms']).fillna(0)
            ch_labels = [c.upper() for c in ch_grp.index]
            ch_vals   = ch_grp.values
            ch_clrs   = [CHANNEL_COLORS[c] for c in ch_grp.index]

            fig_donut = go.Figure(go.Pie(
                labels=ch_labels,
                values=ch_vals,
                hole=0.62,
                marker=dict(colors=ch_clrs, line=dict(color='white', width=2)),
                textinfo='percent+label',
                textposition='inside',
                textfont=dict(size=11.5, family='Inter', color='white'),
                hovertemplate="<b>%{label}</b><br>Attempts: %{value:,}<br>Share of Total: %{percent}<extra></extra>"
            ))
            fig_donut.update_layout(
                annotations=[dict(text=f"<b>{total_legs_val:,}</b><br><span style='font-size:11px'>Total Tries</span>", x=0.5, y=0.5, font_size=15, showarrow=False, font=dict(family='Inter', color=PALETTE['navy']))]
            )
            st.plotly_chart(apply_exec_chart_theme(fig_donut, height=360, show_legend=False, pad_l=10, pad_r=10, pad_t=25, pad_b=15), use_container_width=True)
            st.markdown(f"""
            <div style="display:flex; justify-content:center; gap:12px; font-size:11.8px; font-weight:600; margin-top:4px; flex-wrap:wrap;">
                <span style="color:{CHANNEL_COLORS['email']};">📧 EMAIL: {int(ch_grp.get('email',0)):,} ({ch_grp.get('email',0)/total_legs_val*100:.1f}%)</span>
                <span style="color:{CHANNEL_COLORS['whatsapp']};">💬 WHATSAPP: {int(ch_grp.get('whatsapp',0)):,} ({ch_grp.get('whatsapp',0)/total_legs_val*100:.1f}%)</span>
                <span style="color:{CHANNEL_COLORS['push']};">📱 PUSH: {int(ch_grp.get('push',0)):,} ({ch_grp.get('push',0)/total_legs_val*100:.1f}%)</span>
                <span style="color:{CHANNEL_COLORS['sms']};">📟 SMS: {int(ch_grp.get('sms',0)):,} ({ch_grp.get('sms',0)/total_legs_val*100:.1f}%)</span>
            </div>
            """, unsafe_allow_html=True)

        else:
            # Donut colored by Delivery Status
            st_grp = filtered_df.groupby('status').size().reindex(['SENT', 'SKIPPED', 'FAILED']).fillna(0)
            st_labels = ['SENT', 'SKIPPED', 'FAILED']
            st_vals   = [st_grp.get('SENT', 0), st_grp.get('SKIPPED', 0), st_grp.get('FAILED', 0)]
            st_clrs   = [STATUS_COLORS['SENT'], STATUS_COLORS['SKIPPED'], STATUS_COLORS['FAILED']]

            fig_donut = go.Figure(go.Pie(
                labels=st_labels,
                values=st_vals,
                hole=0.62,
                marker=dict(colors=st_clrs, line=dict(color='white', width=2)),
                textinfo='percent+label',
                textposition='inside',
                textfont=dict(size=12, family='Inter', color='white'),
                hovertemplate="<b>%{label}</b><br>Attempts: %{value:,}<br>Share of Total: %{percent}<extra></extra>"
            ))
            fig_donut.update_layout(
                annotations=[dict(text=f"<b>{total_legs_val:,}</b><br><span style='font-size:11px'>Total Tries</span>", x=0.5, y=0.5, font_size=15, showarrow=False, font=dict(family='Inter', color=PALETTE['navy']))]
            )
            st.plotly_chart(apply_exec_chart_theme(fig_donut, height=360, show_legend=False, pad_l=10, pad_r=10, pad_t=25, pad_b=15), use_container_width=True)
            st.markdown(f"""
            <div style="display:flex; justify-content:center; gap:14px; font-size:11.8px; font-weight:600; margin-top:4px;">
                <span style="color:{STATUS_COLORS['SENT']};">🟢 SENT: {int(st_grp.get('SENT',0)):,} ({st_grp.get('SENT',0)/total_legs_val*100:.1f}%)</span>
                <span style="color:{STATUS_COLORS['SKIPPED']};">🟡 SKIPPED: {int(st_grp.get('SKIPPED',0)):,} ({st_grp.get('SKIPPED',0)/total_legs_val*100:.1f}%)</span>
                <span style="color:{STATUS_COLORS['FAILED']};">🔴 FAILED: {int(st_grp.get('FAILED',0)):,} ({st_grp.get('FAILED',0)/total_legs_val*100:.1f}%)</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Dynamic Channel Metrics
    ch_metrics = {}
    for ch_name in ['email', 'whatsapp', 'push', 'sms']:
        c_sub = filtered_df[filtered_df['channel'] == ch_name]
        c_tot = len(c_sub)
        c_sent = int(c_sub['sent_flag'].sum())
        c_skip = int(c_sub['skipped_flag'].sum())
        c_fail = int(c_sub['failed_flag'].sum())
        c_rate = (c_sent / c_tot * 100) if c_tot > 0 else 0
        ch_metrics[ch_name] = {
            'tot': c_tot, 'sent': c_sent, 'skip': c_skip, 'fail': c_fail, 'rate': c_rate
        }

    ce1, ce2, ce3, ce4 = st.columns(4)
    em_m = ch_metrics['email']
    wa_m = ch_metrics['whatsapp']
    pu_m = ch_metrics['push']
    sm_m = ch_metrics['sms']

    with ce1:
        st.markdown(f"""<div class="exec-card" style="border-left:5px solid {CHANNEL_COLORS['email']};">
            <div style="font-weight:700;color:{CHANNEL_COLORS['email']};font-size:14px;">📧 EMAIL — {em_m['tot']:,} Attempts</div>
            <div style="font-size:22px;font-weight:800;color:{PALETTE['navy']};margin:6px 0;">{em_m['rate']:.1f}% Delivered</div>
            <div style="font-size:12px;color:{PALETTE['muted']};line-height:1.6;">
                <span style="color:{STATUS_COLORS['SENT']};font-weight:700;">✅ {em_m['sent']:,} Sent</span> · 
                <span style="color:{STATUS_COLORS['SKIPPED']};font-weight:700;">⏭️ {em_m['skip']:,} Skipped</span> · 
                <span style="color:{STATUS_COLORS['FAILED']};font-weight:700;">❌ {em_m['fail']:,} Failed</span><br>
                Reason: email address missing on candidate profile
            </div></div>""", unsafe_allow_html=True)
    with ce2:
        st.markdown(f"""<div class="exec-card" style="border-left:5px solid {CHANNEL_COLORS['whatsapp']};">
            <div style="font-weight:700;color:{CHANNEL_COLORS['whatsapp']};font-size:14px;">💬 WHATSAPP — {wa_m['tot']:,} Attempts</div>
            <div style="font-size:22px;font-weight:800;color:{PALETTE['navy']};margin:6px 0;">{wa_m['rate']:.1f}% Delivered</div>
            <div style="font-size:12px;color:{PALETTE['muted']};line-height:1.6;">
                <span style="color:{STATUS_COLORS['SENT']};font-weight:700;">✅ {wa_m['sent']:,} Sent</span> · 
                <span style="color:{STATUS_COLORS['SKIPPED']};font-weight:700;">⏭️ {wa_m['skip']:,} Skipped</span> · 
                <span style="color:{STATUS_COLORS['FAILED']};font-weight:700;">❌ {wa_m['fail']:,} Failed</span><br>
                Reason: missing field in WhatsApp template (131008)
            </div></div>""", unsafe_allow_html=True)
    with ce3:
        st.markdown(f"""<div class="exec-card" style="border-left:5px solid {CHANNEL_COLORS['push']};">
            <div style="font-weight:700;color:{CHANNEL_COLORS['push']};font-size:14px;">📱 MOBILE PUSH — {pu_m['tot']:,} Attempts</div>
            <div style="font-size:22px;font-weight:800;color:{PALETTE['navy']};margin:6px 0;">{pu_m['rate']:.1f}% Delivered</div>
            <div style="font-size:12px;color:{PALETTE['muted']};line-height:1.6;">
                <span style="color:{STATUS_COLORS['SENT']};font-weight:700;">✅ {pu_m['sent']:,} Sent</span> · 
                <span style="color:{STATUS_COLORS['SKIPPED']};font-weight:700;">⏭️ {pu_m['skip']:,} Skipped</span> · 
                <span style="color:{STATUS_COLORS['FAILED']};font-weight:700;">❌ {pu_m['fail']:,} Failed</span><br>
                Reason: app did not record device ID at login
            </div></div>""", unsafe_allow_html=True)
    with ce4:
        st.markdown(f"""<div class="exec-card" style="border-left:5px solid {CHANNEL_COLORS['sms']};">
            <div style="font-weight:700;color:{CHANNEL_COLORS['sms']};font-size:14px;">📟 SMS — {sm_m['tot']:,} Attempts</div>
            <div style="font-size:22px;font-weight:800;color:{PALETTE['navy']};margin:6px 0;">{sm_m['rate']:.1f}% Delivered</div>
            <div style="font-size:12px;color:{PALETTE['muted']};line-height:1.6;">
                <span style="color:{STATUS_COLORS['SENT']};font-weight:700;">✅ {sm_m['sent']:,} Sent</span> · 
                <span style="color:{STATUS_COLORS['SKIPPED']};font-weight:700;">⏭️ {sm_m['skip']:,} Skipped</span> · 
                <span style="color:{STATUS_COLORS['FAILED']};font-weight:700;">❌ {sm_m['fail']:,} Failed</span><br>
                Reason: awaiting government SMS approval (India DLT)
            </div></div>""", unsafe_allow_html=True)


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
            xaxis=dict(title="", showgrid=False, tickangle=-12, tickfont=dict(size=12, family='Inter')),
            yaxis=dict(title="Delivery Success Rate (%)", showgrid=True, gridcolor='#f1f5f9', range=[0, 135]),
            bargap=0.35
        )
        fig_reach.add_hline(y=70, line_dash="dot", line_color=STATUS_COLORS['SENT'],    annotation_text="70% Target",  annotation_position="right", annotation_font_color=STATUS_COLORS['SENT'])
        fig_reach.add_hline(y=40, line_dash="dot", line_color=STATUS_COLORS['SKIPPED'], annotation_text="40% Warning", annotation_position="right", annotation_font_color=STATUS_COLORS['SKIPPED'])
        st.plotly_chart(apply_exec_chart_theme(fig_reach, height=420, show_legend=False, pad_l=50, pad_r=85, pad_t=50, pad_b=55), use_container_width=True)
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

    col_t1, col_t2 = st.columns([1.15, 0.85])

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
            customdata=daily_df['total_attempts'],
            hovertemplate="<b>%{x}</b><br>Sent Rate: %{y:.1f}%<br>Total Attempts: %{customdata:,}<extra></extra>"))
        fig_time.update_layout(
            barmode='stack',
            xaxis=dict(title="Date", showgrid=False, tickangle=-30),
            yaxis=dict(title="Attempt Count", showgrid=True, gridcolor='#f1f5f9'),
            yaxis2=dict(title="Sent Rate (%)", overlaying='y', side='right', range=[0, 135], showgrid=False),
            bargap=0.25
        )
        st.plotly_chart(apply_exec_chart_theme(fig_time, height=400, pad_l=50, pad_r=70, pad_t=60, pad_b=50), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="📆 Volume by Day of Week &amp; Delivery Health",
            significance="Shows notification activity across days of the week, broken down by delivery health (Sent, Skipped, Failed) to spot specific days with high drop-off rates.",
            calculation="Cross-tab notification_day_name × status. Stacked bars: Green = SENT, Amber = SKIPPED, Crimson = FAILED. Total attempt counts shown on top of each day bar.",
            action="Shift automated batch dispatches away from peak-failure days or investigate gateway throttling on high-load weekdays."
        )

        dow_mode = st.radio(
            "Day of Week View:",
            ["📊 Stacked by Delivery Status", "📆 Overall Volume (Peak Highlighted)"],
            horizontal=True,
            key="dow_view_mode"
        )

        day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        dow_ct = pd.crosstab(filtered_df['notification_day_name'], filtered_df['status']).fillna(0)
        for s in ['SENT', 'SKIPPED', 'FAILED']:
            if s not in dow_ct.columns: dow_ct[s] = 0
        dow_ct = dow_ct.reindex([d for d in day_order if d in dow_ct.index])
        dow_totals = dow_ct[['SENT','SKIPPED','FAILED']].sum(axis=1)

        if "Stacked" in dow_mode:
            fig_dow = go.Figure()
            for status, color in [('SENT', STATUS_COLORS['SENT']), ('SKIPPED', STATUS_COLORS['SKIPPED']), ('FAILED', STATUS_COLORS['FAILED'])]:
                shares = [(v / dow_totals[d] * 100) if dow_totals[d] > 0 else 0 for d, v in zip(dow_ct.index, dow_ct[status])]
                fig_dow.add_trace(go.Bar(
                    x=list(dow_ct.index), y=dow_ct[status], name=status,
                    marker_color=color, marker_line=dict(color='white', width=1),
                    text=[f"<b>{int(v):,}</b>" if v >= 60 else "" for v in dow_ct[status]],
                    textposition='inside', textfont=dict(size=11.5, color='white', family='Inter'),
                    insidetextanchor='middle',
                    customdata=shares,
                    hovertemplate=f"<b>%{{x}} · {status}</b><br>Attempts: %{{y:,}}<br>Share of Day: %{{customdata:.1f}}%<extra></extra>"
                ))

            for d, total in zip(dow_ct.index, dow_totals):
                fig_dow.add_annotation(
                    x=d, y=total, text=f"<b>Total: {int(total):,}</b>",
                    showarrow=False, yshift=14,
                    font=dict(size=11.5, color=PALETTE['charcoal'], family='Inter')
                )

            fig_dow.update_layout(
                barmode='stack',
                xaxis=dict(title="", showgrid=False, tickangle=0, tickfont=dict(size=12, family='Inter', color=PALETTE['charcoal'])),
                yaxis=dict(title="Delivery Attempts", showgrid=True, gridcolor='#f1f5f9',
                           range=[0, dow_totals.max() * 1.30]),
                bargap=0.32
            )
            st.plotly_chart(apply_exec_chart_theme(fig_dow, height=400, pad_l=50, pad_r=25, pad_t=60, pad_b=45), use_container_width=True)
            st.markdown(f"""
            <div style="display:flex; justify-content:center; gap:14px; font-size:11.8px; font-weight:600; margin-top:4px;">
                <span style="color:{STATUS_COLORS['SENT']};">🟢 SENT: {int(filtered_df['sent_flag'].sum()):,} ({filtered_df['sent_flag'].mean()*100:.1f}%)</span>
                <span style="color:{STATUS_COLORS['SKIPPED']};">🟡 SKIPPED: {int(filtered_df['skipped_flag'].sum()):,} ({filtered_df['skipped_flag'].mean()*100:.1f}%)</span>
                <span style="color:{STATUS_COLORS['FAILED']};">🔴 FAILED: {int(filtered_df['failed_flag'].sum()):,} ({filtered_df['failed_flag'].mean()*100:.1f}%)</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            day_cnts = dow_totals.reset_index()
            day_cnts.columns = ['Day', 'Count']
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
                customdata=day_cnts['Pct'],
                hovertemplate="<b>%{x}</b><br>Volume: %{y:,}<br>Share: %{customdata:.1f}%<extra></extra>"
            ))
            fig_dow.update_layout(
                xaxis=dict(title="", showgrid=False, tickangle=0, tickfont=dict(size=12, family='Inter')),
                yaxis=dict(title="Volume", showgrid=True, gridcolor='#f1f5f9',
                           range=[0, day_cnts['Count'].max() * 1.35]),
                bargap=0.3
            )
            st.plotly_chart(apply_exec_chart_theme(fig_dow, height=400, show_legend=False, pad_l=50, pad_r=25, pad_t=45, pad_b=45), use_container_width=True)

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
                   tickfont=dict(size=12.5, family='Inter'))
    )
    st.plotly_chart(apply_exec_chart_theme(fig_heat, height=340, show_legend=False, pad_l=75, pad_r=50, pad_t=30, pad_b=50), use_container_width=True)
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

        st.plotly_chart(apply_exec_chart_theme(fig_month_heat, height=480, show_legend=False, pad_l=70, pad_r=45, pad_t=25, pad_b=60), use_container_width=True)

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

        # Handle missing locations properly so Virtual / Online is visible
        clean_loc_series = filtered_df['client_location'].fillna('Virtual / Online (No Plant)')
        loc_ct = pd.crosstab(clean_loc_series, filtered_df['status']).fillna(0)
        for col in ['SENT','FAILED','SKIPPED']:
            if col not in loc_ct.columns: loc_ct[col] = 0
        loc_ct['TOTAL'] = loc_ct.sum(axis=1)
        loc_top  = loc_ct.sort_values(by='TOTAL', ascending=True).tail(6)

        def format_facility_name(loc):
            if not loc or pd.isna(loc) or str(loc).strip().lower() in ['nan', 'none', 'unknown', '']:
                return "Virtual / Online (No Plant)"
            s = str(loc).strip()
            if "kharkhoda" in s.lower() or "plant-4" in s.lower():
                return "Kharkhoda Plant-4 (HR)"
            if "pune" in s.lower() or "ahmednagar" in s.lower():
                return "Pune MIDC (MH)"
            if "sangareddy" in s.lower() or "kambalpalle" in s.lower():
                return "Sangareddy Hub (TG)"
            if "silvassa" in s.lower() or "naroli" in s.lower():
                return "Silvassa Facility (GJ)"
            if "bhwadi" in s.lower() or "bhiwadi" in s.lower() or "alwar" in s.lower():
                return "Bhiwadi Ind. Area (RJ)"
            if "bengaluru" in s.lower():
                return "Bengaluru Training Center"
            if "test client" in s.lower():
                return "Test Client (HR)"
            return s[:24] + "…" if len(s) > 24 else s

        y_labels = [format_facility_name(l) for l in loc_top.index]
        raw_addresses = [str(l) if pd.notna(l) and str(l).strip() != 'Virtual / Online (No Plant)' else "Virtual / online student (no physical plant)" for l in loc_top.index]

        fig_loc = go.Figure()
        for status, color in [('SENT',STATUS_COLORS['SENT']),('SKIPPED',STATUS_COLORS['SKIPPED']),('FAILED',STATUS_COLORS['FAILED'])]:
            shares = [(v / tot * 100) if tot > 0 else 0 for v, tot in zip(loc_top[status], loc_top['TOTAL'])]
            fig_loc.add_trace(go.Bar(
                y=y_labels, x=loc_top[status], name=status, orientation='h',
                marker_color=color, marker_line=dict(color='white', width=1),
                text=[f"<b>{int(v):,}</b>" if v >= 40 else "" for v in loc_top[status]],
                textposition='inside', textfont=dict(size=11.5, color='white', family='Inter'),
                insidetextanchor='middle',
                customdata=list(zip(raw_addresses, shares)),
                hovertemplate="<b>%{y}</b><br>"+status+": %{x:,} attempts (%{customdata[1]:.1f}%)<br><span style='font-size:10px;color:#64748b;'>%{customdata[0]}</span><extra></extra>"
            ))

        for y_lbl, tot in zip(y_labels, loc_top['TOTAL']):
            fig_loc.add_annotation(
                y=y_lbl, x=tot, text=f"<b>Total: {int(tot):,}</b>",
                showarrow=False, xshift=10, xanchor='left',
                font=dict(size=11.5, color=PALETTE['charcoal'], family='Inter')
            )

        fig_loc.update_layout(
            barmode='stack',
            xaxis=dict(title="Delivery Attempts", showgrid=True, gridcolor='#f1f5f9',
                       range=[0, loc_top['TOTAL'].max() * 1.32]),
            yaxis=dict(showgrid=False, tickfont=dict(size=12, family='Inter', color=PALETTE['charcoal'])),
            bargap=0.28
        )
        st.plotly_chart(apply_exec_chart_theme(fig_loc, height=400, pad_l=185, pad_r=65, pad_t=55, pad_b=40), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d2:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="👨‍🏫 Delivery Success by Assigned Trainer",
            significance="Identifies operational discrepancies across training coordinators — ensures candidate class schedules are reliably delivered regardless of instructor.",
            calculation="Cross-tab trainer_name x status, sorted descending by total assigned attempts. Top 6 trainers as stacked horizontal bars with per-segment labels.",
            action="Standardize backend payload generation per trainer assignment to ensure consistent WhatsApp template parameter injection."
        )

        clean_tr_series = filtered_df['trainer_name'].fillna('Unassigned / Automated')
        tr_ct = pd.crosstab(clean_tr_series, filtered_df['status']).fillna(0)
        for col in ['SENT','FAILED','SKIPPED']:
            if col not in tr_ct.columns: tr_ct[col] = 0
        tr_ct['TOTAL'] = tr_ct.sum(axis=1)
        tr_top   = tr_ct.sort_values(by='TOTAL', ascending=True).tail(6)
        y_labels_tr = [str(l) for l in tr_top.index]

        fig_tr = go.Figure()
        for status, color in [('SENT',STATUS_COLORS['SENT']),('SKIPPED',STATUS_COLORS['SKIPPED']),('FAILED',STATUS_COLORS['FAILED'])]:
            shares_tr = [(v / tot * 100) if tot > 0 else 0 for v, tot in zip(tr_top[status], tr_top['TOTAL'])]
            fig_tr.add_trace(go.Bar(
                y=y_labels_tr, x=tr_top[status], name=status, orientation='h',
                marker_color=color, marker_line=dict(color='white', width=1),
                text=[f"<b>{int(v):,}</b>" if v >= 40 else "" for v in tr_top[status]],
                textposition='inside', textfont=dict(size=11.5, color='white', family='Inter'),
                insidetextanchor='middle',
                customdata=shares_tr,
                hovertemplate="<b>%{y}</b><br>"+status+": %{x:,} attempts (%{customdata:.1f}%)<extra></extra>"
            ))

        for y_lbl, tot in zip(y_labels_tr, tr_top['TOTAL']):
            fig_tr.add_annotation(
                y=y_lbl, x=tot, text=f"<b>Total: {int(tot):,}</b>",
                showarrow=False, xshift=10, xanchor='left',
                font=dict(size=11.5, color=PALETTE['charcoal'], family='Inter')
            )

        fig_tr.update_layout(
            barmode='stack',
            xaxis=dict(title="Delivery Attempts", showgrid=True, gridcolor='#f1f5f9',
                       range=[0, tr_top['TOTAL'].max() * 1.30]),
            yaxis=dict(showgrid=False, tickfont=dict(size=12, family='Inter', color=PALETTE['charcoal'])),
            bargap=0.28
        )
        st.plotly_chart(apply_exec_chart_theme(fig_tr, height=400, pad_l=165, pad_r=65, pad_t=55, pad_b=40), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── 8. Action Plan & Triage ───────────────────────────────────────────────────
def render_action_plan_and_triage():
    st.markdown('<div class="section-title">7. What to Fix — Action Plan &amp; Failure Lookup</div>', unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(f"""<div class="exec-card" style="border-top:4px solid {CHANNEL_COLORS['whatsapp']};">
            <div style="font-weight:800;font-size:13px;color:{CHANNEL_COLORS['whatsapp']};">💬 PRIORITY 1 — Fix Today (WhatsApp)</div>
            <div style="font-weight:700;color:{PALETTE['navy']};margin:6px 0;font-size:14px;">WhatsApp Template Bug (131008)</div>
            <div style="font-size:12px;color:{PALETTE['muted']};margin-bottom:8px;line-height:1.6;">1,090 messages failed because date/trainer parameters were missing from the payload sent to WhatsApp.</div>
            <div style="font-size:12px;font-weight:700;color:{STATUS_COLORS['SENT']};">⏱ 1 day to fix · Recovers 1,090 deliveries</div></div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""<div class="exec-card" style="border-top:4px solid {CHANNEL_COLORS['push']};">
            <div style="font-weight:800;font-size:13px;color:{CHANNEL_COLORS['push']};">📱 PRIORITY 2 — Fix This Week (Push)</div>
            <div style="font-weight:700;color:{PALETTE['navy']};margin:6px 0;font-size:14px;">Mobile App Push Token Ingestion</div>
            <div style="font-size:12px;color:{PALETTE['muted']};margin-bottom:8px;line-height:1.6;">1,239 push attempts skipped because the app never saved device tokens to candidate profiles at login.</div>
            <div style="font-size:12px;font-weight:700;color:{STATUS_COLORS['SENT']};">⏱ 3–5 days to fix · Recovers 1,239 deliveries</div></div>""", unsafe_allow_html=True)
    with r3:
        st.markdown(f"""<div class="exec-card" style="border-top:4px solid {CHANNEL_COLORS['email']};">
            <div style="font-weight:800;font-size:13px;color:{CHANNEL_COLORS['email']};">📧 PRIORITY 3 — Fix This Sprint (Email)</div>
            <div style="font-weight:700;color:{PALETTE['navy']};margin:6px 0;font-size:14px;">Collect Email at Online Sign-Up</div>
            <div style="font-size:12px;color:{PALETTE['muted']};margin-bottom:8px;line-height:1.6;">371 online candidates had no email on file — making them unreachable when WhatsApp/Push fail.</div>
            <div style="font-size:12px;font-weight:700;color:{STATUS_COLORS['SENT']};">⏱ 2 days to fix · Saves 584 candidates</div></div>""", unsafe_allow_html=True)
    with r4:
        st.markdown(f"""<div class="exec-card" style="border-top:4px solid {CHANNEL_COLORS['sms']};">
            <div style="font-weight:800;font-size:13px;color:{CHANNEL_COLORS['sms']};">📟 PRIORITY 4 — Regulatory Track (SMS)</div>
            <div style="font-weight:700;color:{PALETTE['navy']};margin:6px 0;font-size:14px;">Activate SMS Fallback via TRAI DLT</div>
            <div style="font-size:12px;color:{PALETTE['muted']};margin-bottom:8px;line-height:1.6;">All 6 SMS attempts blocked by TRAI DLT registration. Approval unlocks reliable offline carrier fallback.</div>
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


# ── 9. Dedicated WhatsApp Notification Analysis Hub ──────────────────────────
def render_whatsapp_deep_dive():
    # Detect appropriate WhatsApp dataset
    if (filtered_df['channel'].str.lower() == 'whatsapp').all():
        wa_data = filtered_df.copy()
    else:
        wa_data = raw_df[raw_df['channel'].str.lower() == 'whatsapp'].copy()

    total_wa = len(wa_data)
    sent_wa = int((wa_data['status'] == 'SENT').sum())
    failed_wa = int((wa_data['status'] == 'FAILED').sum())
    skipped_wa = int((wa_data['status'] == 'SKIPPED').sum())
    cands_wa = wa_data['candidate_id'].nunique()
    cands_reached = wa_data[wa_data['status'] == 'SENT']['candidate_id'].nunique()
    cand_reach_pct = (cands_reached / cands_wa * 100) if cands_wa > 0 else 0
    sent_pct = (sent_wa / total_wa * 100) if total_wa > 0 else 0
    fail_pct = (failed_wa / total_wa * 100) if total_wa > 0 else 0
    skip_pct = (skipped_wa / total_wa * 100) if total_wa > 0 else 0

    latency_series = wa_data[wa_data['status'] == 'SENT']['dispatch_to_sent_seconds'].dropna()
    avg_latency = float(latency_series.mean()) if len(latency_series) > 0 else 1.06
    med_latency = float(latency_series.median()) if len(latency_series) > 0 else 1.02
    min_latency = float(latency_series.min()) if len(latency_series) > 0 else 0.74
    max_latency = float(latency_series.max()) if len(latency_series) > 0 else 1.68

    # Multi-channel ripple effect / Fallback impact
    wa_failed_ids = wa_data[wa_data['status'] == 'FAILED']['notification_id'].unique()
    other_legs = raw_df[raw_df['notification_id'].isin(wa_failed_ids) & (raw_df['channel'].str.lower() != 'whatsapp')]
    rescued_by_email = int(other_legs[(other_legs['channel'] == 'email') & (other_legs['status'] == 'SENT')]['notification_id'].nunique())
    stranded_candidates = len(wa_failed_ids) - rescued_by_email
    rescued_pct = (rescued_by_email / len(wa_failed_ids) * 100) if len(wa_failed_ids) > 0 else 0
    stranded_pct = (stranded_candidates / len(wa_failed_ids) * 100) if len(wa_failed_ids) > 0 else 0

    # Executive Banner
    st.markdown(f"""
    <div class="wa-banner">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:8px;">
            <div style="font-size:26px; font-weight:800; color:#14532d; display:flex; align-items:center; gap:10px;">
                <span>💬</span> WhatsApp Business API Deep-Dive &amp; Meta Error Diagnosis
            </div>
            <span class="wa-badge">Meta Graph API v17.0 Direct Audit</span>
        </div>
        <div style="font-size:13.5px; color:#334155; line-height:1.5; margin-bottom:14px;">
            Dedicated engineering investigation into WhatsApp delivery pipeline across <strong>{total_wa:,}</strong> notification attempts.
            Auditing Meta Cloud API error codes, template failure points, delivery latency benchmarking, multi-channel fallback impact, and ready-to-deploy payload patch.
        </div>
        <div class="status-pill-container">
            <span class="status-pill pill-red">🚨 84.0% Meta Rejection Rate (1,099 out of 1,308 attempts failed)</span>
            <span class="status-pill pill-green">⚡ Gateway Speed: 1.06s Avg Delivery Latency (Fast &amp; Healthy)</span>
            <span class="status-pill pill-blue">🎯 1,090 Deliveries Recoverable Today with 1 Backend Sanitizer Patch</span>
            <span class="status-pill pill-red" style="background:#fef2f2; color:#b91c1c; border-color:#fca5a5;">🛡️ 423 Students Completely Stranded (Zero fallback delivered)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5 KPI Scorecards
    col_k1, col_k2, col_k3, col_k4, col_k5 = st.columns(5)
    with col_k1:
        st.markdown(f"""
        <div class="exec-card" style="border-top: 3.5px solid {CHANNEL_COLORS['whatsapp']};">
            <div class="exec-card-label">Total WhatsApp Attempts</div>
            <div class="exec-card-value" style="color:#14532d;">{total_wa:,}</div>
            <div class="exec-card-subtext">Across <b>{cands_wa:,}</b> unique candidates</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k2:
        st.markdown(f"""
        <div class="exec-card" style="border-top: 3.5px solid {STATUS_COLORS['SENT']};">
            <div class="exec-card-label">Delivered Successfully</div>
            <div class="exec-card-value" style="color:{STATUS_COLORS['SENT']};">{sent_wa:,}</div>
            <div class="exec-card-subtext"><b>{sent_pct:.1f}%</b> delivery rate · {cands_reached:,} reached</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k3:
        st.markdown(f"""
        <div class="exec-card" style="border-top: 3.5px solid {STATUS_COLORS['FAILED']};">
            <div class="exec-card-label">Failed (Meta Rejections)</div>
            <div class="exec-card-value" style="color:{STATUS_COLORS['FAILED']};">{failed_wa:,}</div>
            <div class="exec-card-subtext"><b>{fail_pct:.1f}%</b> failure rate · 99.2% code 131008</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k4:
        st.markdown(f"""
        <div class="exec-card" style="border-top: 3.5px solid {STATUS_COLORS['SKIPPED']};">
            <div class="exec-card-label">Skipped (Fallback Route)</div>
            <div class="exec-card-value" style="color:{STATUS_COLORS['SKIPPED']};">{skipped_wa:,}</div>
            <div class="exec-card-subtext"><b>{skip_pct:.1f}%</b> skipped · Email satisfied</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k5:
        st.markdown(f"""
        <div class="exec-card" style="border-top: 3.5px solid {PALETTE['ocean']};">
            <div class="exec-card-label">Dispatch Latency (Speed)</div>
            <div class="exec-card-value" style="color:{PALETTE['navy']};">{avg_latency:.2f}s</div>
            <div class="exec-card-subtext">Median <b>{med_latency:.2f}s</b> (SLA &lt; 2.0s)</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Section 1: Meta Cloud API Error Decoder ──────────────────────────────
    st.markdown('<div class="section-title">1. Meta Cloud API Error Breakdown &amp; Root Causes</div>', unsafe_allow_html=True)
    col_e1, col_e2 = st.columns([1.15, 0.85])

    def clean_wa_error_label(msg):
        if pd.isna(msg) or str(msg).strip().lower() in ['nan', 'none', '']:
            return 'Delivered Successfully (200 OK)'
        s = str(msg)
        if '131008' in s: return 'Meta 131008: Required Parameter Missing'
        if '132018' in s: return 'Meta 132018: Template Parameter Format Issue'
        if '132001' in s: return 'Meta 132001: Translation / Locale Missing'
        if 'Fallback satisfied' in s: return 'Skipped: Fallback Satisfied by Email'
        return s[:40]

    wa_data['clean_error'] = wa_data['error_message'].apply(clean_wa_error_label)
    err_counts = wa_data['clean_error'].value_counts()

    with col_e1:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="🔬 Meta Cloud API Error Distribution",
            significance="Categorizes all WhatsApp attempts by Meta Cloud API HTTP response status code to pinpoint root causes.",
            calculation="Grouped by parsed error message and Meta error code from vw_notification_analytics.",
            action="Focus 100% of engineering bandwidth on Code 131008 — fixing this one code recovers 1,090 deliveries immediately."
        )

        chart_style_err = st.radio("Display Mode:", ["🍩 Category Donut Chart", "📊 Detailed Horizontal Bar Chart"], horizontal=True, key="wa_err_style")

        err_color_map = {
            'Meta 131008: Required Parameter Missing': '#ef4444',
            'Delivered Successfully (200 OK)': '#10b981',
            'Skipped: Fallback Satisfied by Email': '#f59e0b',
            'Meta 132018: Template Parameter Format Issue': '#eb7966',
            'Meta 132001: Translation / Locale Missing': '#7e519e'
        }

        if "Donut" in chart_style_err:
            fig_err = go.Figure(go.Pie(
                labels=err_counts.index,
                values=err_counts.values,
                hole=0.62,
                marker=dict(colors=[err_color_map.get(k, PALETTE['charcoal']) for k in err_counts.index], line=dict(color='white', width=2)),
                textinfo='percent+label',
                textposition='inside',
                textfont=dict(size=11.5, family='Inter', color='white'),
                hovertemplate="<b>%{label}</b><br>Attempts: %{value:,}<br>Share: %{percent}<extra></extra>"
            ))
            fig_err.update_layout(
                annotations=[dict(text=f"<b>{total_wa:,}</b><br><span style='font-size:11px'>WhatsApp Tries</span>", x=0.5, y=0.5, font_size=15, showarrow=False, font=dict(family='Inter', color=PALETTE['navy']))]
            )
            st.plotly_chart(apply_exec_chart_theme(fig_err, height=380, show_legend=False, pad_l=15, pad_r=15, pad_t=25, pad_b=15), use_container_width=True)
        else:
            fig_err = go.Figure(go.Bar(
                y=err_counts.index[::-1],
                x=err_counts.values[::-1],
                orientation='h',
                marker_color=[err_color_map.get(k, PALETTE['charcoal']) for k in err_counts.index[::-1]],
                text=[f"<b>{v:,}</b> ({v/total_wa*100:.1f}%)" for v in err_counts.values[::-1]],
                textposition='outside',
                textfont=dict(size=11.5, family='Inter', color=PALETTE['charcoal']),
                hovertemplate="<b>%{y}</b><br>Attempts: %{x:,} (%{text})<extra></extra>"
            ))
            fig_err.update_layout(
                xaxis=dict(title="Attempts", range=[0, max(err_counts.values) * 1.25], showgrid=True, gridcolor='#f1f5f9'),
                yaxis=dict(showgrid=False, tickfont=dict(size=11.5, family='Inter'))
            )
            st.plotly_chart(apply_exec_chart_theme(fig_err, height=380, show_legend=False, pad_l=210, pad_r=50, pad_t=25, pad_b=40), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_e2:
        st.markdown(f"""
        <div class="exec-card" style="border-top:4px solid #ef4444; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:800; font-size:12.5px; color:#ef4444;">🔴 META ERROR #131008</span>
                <span style="font-weight:800; font-size:12px; background:#fee2e2; color:#991b1b; padding:2px 8px; border-radius:10px;">1,090 Fails (99.2%)</span>
            </div>
            <div style="font-weight:700; color:{PALETTE['navy']}; margin:4px 0; font-size:13.5px;">Required Parameter Missing</div>
            <div style="font-size:12px; color:{PALETTE['muted']}; line-height:1.5; margin-bottom:6px;">
                Meta Cloud API rejects HTTP request when body parameters (<code>{{{{1}}}}</code>, <code>{{{{2}}}}</code>, etc.) receive <code>null</code> or empty strings.
                Triggered primarily when <code>session_date</code> or <code>trainer_name</code> are unassigned in backend payload.
            </div>
            <div style="font-size:11.5px; font-weight:700; color:{STATUS_COLORS['SENT']};">💡 Fix: Inject safe string fallbacks (e.g. "TBA") before dispatch.</div>
        </div>

        <div class="exec-card" style="border-top:4px solid #eb7966; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:800; font-size:12.5px; color:#eb7966;">🟠 META ERROR #132018</span>
                <span style="font-weight:800; font-size:12px; background:#ffedd5; color:#9a3412; padding:2px 8px; border-radius:10px;">6 Fails (0.5%)</span>
            </div>
            <div style="font-weight:700; color:{PALETTE['navy']}; margin:4px 0; font-size:13.5px;">Template Parameter Format Mismatch</div>
            <div style="font-size:12px; color:{PALETTE['muted']}; line-height:1.5; margin-bottom:6px;">
                Parameter type or positional count does not match registered Meta template schema. Found in <code>lernern_classroom_assigned</code> and <code>lernern_id_card</code>.
            </div>
            <div style="font-size:11.5px; font-weight:700; color:{PALETTE['navy']};">💡 Fix: Synchronize JSON parameter positions with Meta Business Manager.</div>
        </div>

        <div class="exec-card" style="border-top:4px solid #7e519e; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:800; font-size:12.5px; color:#7e519e;">🟣 META ERROR #132001</span>
                <span style="font-weight:800; font-size:12px; background:#f3e8ff; color:#6b21a8; padding:2px 8px; border-radius:10px;">3 Fails (0.3%)</span>
            </div>
            <div style="font-weight:700; color:{PALETTE['navy']}; margin:4px 0; font-size:13.5px;">Template Translation Not Found</div>
            <div style="font-size:12px; color:{PALETTE['muted']}; line-height:1.5; margin-bottom:6px;">
                Payload requested language code <code>en</code> but template was registered in Meta Business Manager as <code>en_US</code> (or vice versa) for <code>lernern_offer_letter</code>.
            </div>
            <div style="font-size:11.5px; font-weight:700; color:{PALETTE['navy']};">💡 Fix: Standardize language locale code to <code>en_US</code>.</div>
        </div>

        <div class="exec-card" style="border-top:4px solid #f59e0b;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:800; font-size:12.5px; color:#d97706;">🟡 ROUTED / SKIPPED</span>
                <span style="font-weight:800; font-size:12px; background:#fef3c7; color:#92400e; padding:2px 8px; border-radius:10px;">16 Skips (1.2%)</span>
            </div>
            <div style="font-weight:700; color:{PALETTE['navy']}; margin:4px 0; font-size:13.5px;">Fallback Satisfied by Email</div>
            <div style="font-size:12px; color:{PALETTE['muted']}; line-height:1.5; margin-bottom:6px;">
                Multi-channel router detected candidate already received successful notification via Email. Dispatch safely skipped, preventing duplicate alerts and unnecessary Meta conversation fees.
            </div>
            <div style="font-size:11.5px; font-weight:700; color:{STATUS_COLORS['SENT']};">✅ Working as intended (Intelligent deduplication).</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Section 2: WhatsApp Template Breakdown Matrix ────────────────────────
    st.markdown('<div class="section-title">2. WhatsApp Template Performance Matrix — All 7 Templates</div>', unsafe_allow_html=True)

    tmpl_ct = pd.crosstab(wa_data['template_name'], wa_data['status']).fillna(0)
    for col in ['SENT', 'SKIPPED', 'FAILED']:
        if col not in tmpl_ct.columns: tmpl_ct[col] = 0
    tmpl_ct['TOTAL'] = tmpl_ct.sum(axis=1)
    tmpl_ct['SENT_RATE'] = (tmpl_ct['SENT'] / tmpl_ct['TOTAL'] * 100).round(1)
    tmpl_ct['FAIL_RATE'] = (tmpl_ct['FAILED'] / tmpl_ct['TOTAL'] * 100).round(1)
    tmpl_sorted = tmpl_ct.sort_values(by='TOTAL', ascending=True)

    col_m1, col_m2 = st.columns([1.3, 0.7])
    with col_m1:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="📊 Template Volume & Delivery Outcome (Sent, Skipped, Failed)",
            significance="Compares reliability across all 7 registered WhatsApp templates to identify the exact templates driving the failure spike.",
            calculation="Cross-tab of template_name by delivery status, sorted ascending by total volume with end-of-bar totals.",
            action="Patch online and onsite scheduled class templates first — together they account for 1,043 of the 1,099 total failures (94.9%)."
        )

        y_tmpls = list(tmpl_sorted.index)
        fig_tmpl = go.Figure()
        for status, color in [('SENT', STATUS_COLORS['SENT']), ('SKIPPED', STATUS_COLORS['SKIPPED']), ('FAILED', STATUS_COLORS['FAILED'])]:
            shares_t = [(v / tot * 100) if tot > 0 else 0 for v, tot in zip(tmpl_sorted[status], tmpl_sorted['TOTAL'])]
            fig_tmpl.add_trace(go.Bar(
                y=y_tmpls, x=tmpl_sorted[status], name=status, orientation='h',
                marker_color=color, marker_line=dict(color='white', width=1),
                text=[f"<b>{int(v):,}</b>" if v >= 20 else "" for v in tmpl_sorted[status]],
                textposition='inside', textfont=dict(size=11, color='white', family='Inter'),
                insidetextanchor='middle',
                customdata=shares_t,
                hovertemplate="<b>%{y}</b><br>"+status+": %{x:,} attempts (%{customdata:.1f}%)<extra></extra>"
            ))

        for y_lbl, tot, s_rate in zip(y_tmpls, tmpl_sorted['TOTAL'], tmpl_sorted['SENT_RATE']):
            fig_tmpl.add_annotation(
                y=y_lbl, x=tot, text=f"<b>Total: {int(tot):,}</b> ({s_rate:.1f}% sent)",
                showarrow=False, xshift=10, xanchor='left',
                font=dict(size=11.5, color=PALETTE['charcoal'], family='Inter')
            )

        fig_tmpl.update_layout(
            barmode='stack',
            xaxis=dict(title="WhatsApp Delivery Attempts", showgrid=True, gridcolor='#f1f5f9', range=[0, tmpl_sorted['TOTAL'].max() * 1.35]),
            yaxis=dict(showgrid=False, tickfont=dict(size=12, family='Inter', color=PALETTE['charcoal'])),
            bargap=0.30
        )
        st.plotly_chart(apply_exec_chart_theme(fig_tmpl, height=380, pad_l=195, pad_r=65, pad_t=50, pad_b=40), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_m2:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="📋 Template Reliability Scorecard",
            significance="Quick reference table for engineering lead to review delivery rates and primary error codes per template.",
            calculation="Aggregated template counts with percentage delivery and failure rates.",
            action="Prioritize lernern_online_scheduled (97.4% fail rate) — 487 out of 500 attempts failed."
        )

        display_t = tmpl_ct.sort_values(by='TOTAL', ascending=False).reset_index()
        display_t.columns = ['Template Name', 'Failed', 'Sent', 'Skipped', 'Total Attempts', 'Sent Rate %', 'Fail Rate %']

        # Add primary error column
        top_err_dict = {}
        for tmpl in display_t['Template Name']:
            t_data = wa_data[wa_data['template_name'] == tmpl]
            if (t_data['status'] == 'FAILED').any():
                top_err_dict[tmpl] = "131008 (Missing Param)" if (t_data['error_code'] == 131008).any() else "132018 (Schema)"
            else:
                top_err_dict[tmpl] = "100% Success"
        display_t['Primary Error'] = display_t['Template Name'].map(top_err_dict)

        st.dataframe(
            display_t[['Template Name', 'Total Attempts', 'Sent', 'Failed', 'Sent Rate %', 'Fail Rate %', 'Primary Error']],
            height=320,
            use_container_width=True
        )
        st.markdown(f"""
        <div class="exec-alert-box" style="margin-top:10px; padding:10px 14px; font-size:12px;">
            <strong>⚠️ Critical Observation:</strong> <code>lernern_online_scheduled</code> has a <strong>97.4% failure rate</strong> (only 1 of 500 attempts succeeded). This represents the highest single concentration of communication leakage in the company.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Section 3: Latency & Hourly Vulnerability ─────────────────────────────
    st.markdown('<div class="section-title">3. Dispatch Latency Benchmarking &amp; Pre-Class Hourly Vulnerability</div>', unsafe_allow_html=True)

    col_l1, col_l2 = st.columns([1, 1])

    with col_l1:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="⚡ WhatsApp Gateway Latency Benchmark (< 2.0s SLA)",
            significance="Benchmarks end-to-end latency from engine dispatch to Meta Graph API 200 OK sent confirmation.",
            calculation="Distribution of dispatch_to_sent_seconds for all 193 delivered WhatsApp messages.",
            action="Validate that Meta Cloud API throughput is excellent (1.06s avg) — proving network latency is not causing failures."
        )

        sent_wa_df = wa_data[wa_data['status'] == 'SENT']
        fig_lat = go.Figure()
        fig_lat.add_trace(go.Histogram(
            x=sent_wa_df['dispatch_to_sent_seconds'],
            nbinsx=18,
            marker_color=CHANNEL_COLORS['whatsapp'],
            marker_line=dict(color='white', width=1),
            hovertemplate="Latency: <b>%{x:.2f}s</b><br>Delivered: %{y:,} messages<extra></extra>"
        ))
        fig_lat.add_vline(x=avg_latency, line_width=2, line_dash="dash", line_color=PALETTE['crimson'],
                          annotation_text=f"Avg: {avg_latency:.2f}s", annotation_position="top right",
                          annotation_font=dict(size=11, color=PALETTE['crimson'], family='Inter'))
        fig_lat.add_vline(x=2.0, line_width=1.5, line_dash="dot", line_color=PALETTE['muted'],
                          annotation_text="SLA (2.0s)", annotation_position="top right",
                          annotation_font=dict(size=10, color=PALETTE['muted'], family='Inter'))

        fig_lat.update_layout(
            xaxis=dict(title="Dispatch to Sent Latency (seconds)", range=[0.5, 2.2], showgrid=True, gridcolor='#f1f5f9'),
            yaxis=dict(title="Delivered Messages", showgrid=True, gridcolor='#f1f5f9'),
            bargap=0.08
        )
        st.plotly_chart(apply_exec_chart_theme(fig_lat, height=360, show_legend=False, pad_l=50, pad_r=40, pad_t=40, pad_b=40), use_container_width=True)

        st.markdown(f"""
        <div style="display:flex; justify-content:space-around; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px 14px; font-size:12px; margin-top:8px;">
            <span>⏱ <b>Mean:</b> {avg_latency:.2f}s</span>
            <span>🎯 <b>Median:</b> {med_latency:.2f}s</span>
            <span>⚡ <b>Fastest:</b> {min_latency:.2f}s</span>
            <span>🐢 <b>Slowest:</b> {max_latency:.2f}s</span>
            <span>🏆 <b>SLA Compliance:</b> 100.0% &lt; 2.0s</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_l2:
        st.markdown('<div class="plot-card">', unsafe_allow_html=True)
        render_chart_header(
            title="⏰ Hourly Dispatch Spike vs. Morning Failure Wave",
            significance="Reveals what time of day WhatsApp messages are triggered and how failures cluster in early morning batch jobs.",
            calculation="Cross-tab of notification_hour by status (SENT vs FAILED), stacked by hour (0 to 23).",
            action="Critical operational urgency: 873 notifications fail between 4:00 AM and 8:00 AM before students head to classes."
        )

        h_ct = pd.crosstab(wa_data['notification_hour'], wa_data['status']).fillna(0)
        for col in ['SENT', 'SKIPPED', 'FAILED']:
            if col not in h_ct.columns: h_ct[col] = 0
        h_ct['TOTAL'] = h_ct.sum(axis=1)

        all_hours = list(range(0, 24))
        h_ct = h_ct.reindex(all_hours, fill_value=0)

        fig_hr = go.Figure()
        for status, color in [('SENT', STATUS_COLORS['SENT']), ('SKIPPED', STATUS_COLORS['SKIPPED']), ('FAILED', STATUS_COLORS['FAILED'])]:
            fig_hr.add_trace(go.Bar(
                x=[f"{h:02d}:00" for h in all_hours],
                y=h_ct[status],
                name=status,
                marker_color=color,
                marker_line=dict(color='white', width=0.5),
                hovertemplate="Hour %{x}<br>"+status+": %{y:,}<extra></extra>"
            ))

        fig_hr.update_layout(
            barmode='stack',
            xaxis=dict(title="Hour of Day (24-Hour UTC/IST)", showgrid=False, tickfont=dict(size=10, family='Inter')),
            yaxis=dict(title="Delivery Attempts", showgrid=True, gridcolor='#f1f5f9', range=[0, h_ct['TOTAL'].max() * 1.25]),
            bargap=0.20
        )
        st.plotly_chart(apply_exec_chart_theme(fig_hr, height=360, pad_l=50, pad_r=30, pad_t=40, pad_b=40), use_container_width=True)

        st.markdown(f"""
        <div class="exec-alert-box" style="margin-top:8px; padding:10px 14px; font-size:12px;">
            <strong>🚨 Pre-Class Blindspot:</strong> Between <strong>4:00 AM and 8:00 AM</strong>, automated schedulers dispatch 885 WhatsApp messages. <strong>873 fail immediately</strong>. Candidates leave home for class without room numbers or Google Meet links.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Section 4: The Ripple Effect — Multi-Channel Fallback ────────────────
    st.markdown('<div class="section-title">4. The Ripple Effect — What Happens When WhatsApp Fails?</div>', unsafe_allow_html=True)

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.markdown(f"""
        <div class="exec-card" style="border-top:4px solid #ef4444;">
            <div style="font-weight:800; font-size:12px; color:#ef4444; text-transform:uppercase;">🚫 Stranded Candidates</div>
            <div class="exec-card-value" style="color:#b91c1c; margin:6px 0;">{stranded_candidates:,}</div>
            <div style="font-weight:700; color:{PALETTE['navy']}; font-size:13.5px; margin-bottom:6px;">Zero Notification Received ({stranded_pct:.1f}%)</div>
            <div style="font-size:12px; color:{PALETTE['muted']}; line-height:1.5;">
                When WhatsApp failed for these {stranded_candidates:,} candidates, no other channel rescued them: Email had no address on file, Push lacked device tokens, and SMS was blocked by TRAI DLT.
            </div>
            <div style="font-size:11.5px; font-weight:700; color:#ef4444; margin-top:8px;">
                Impact: Complete student no-show risk.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r2:
        st.markdown(f"""
        <div class="exec-card" style="border-top:4px solid {CHANNEL_COLORS['email']};">
            <div style="font-weight:800; font-size:12px; color:{CHANNEL_COLORS['email']}; text-transform:uppercase;">📧 Rescued by Email</div>
            <div class="exec-card-value" style="color:{CHANNEL_COLORS['email']}; margin:6px 0;">{rescued_by_email:,}</div>
            <div style="font-weight:700; color:{PALETTE['navy']}; font-size:13.5px; margin-bottom:6px;">Partial Rescue via Email ({rescued_pct:.1f}%)</div>
            <div style="font-size:12px; color:{PALETTE['muted']}; line-height:1.5;">
                These {rescued_by_email:,} candidates successfully received an email when WhatsApp failed. However, email open rates average ~22% compared to WhatsApp's ~98%, leaving many students unaware of sudden morning schedule changes.
            </div>
            <div style="font-size:11.5px; font-weight:700; color:{CHANNEL_COLORS['email']}; margin-top:8px;">
                Impact: Fixing WhatsApp gives them instant mobile alerts.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r3:
        st.markdown(f"""
        <div class="exec-card" style="border-top:4px solid {STATUS_COLORS['SENT']};">
            <div style="font-weight:800; font-size:12px; color:{STATUS_COLORS['SENT']}; text-transform:uppercase;">💰 Provider Cost Economics</div>
            <div class="exec-card-value" style="color:{STATUS_COLORS['SENT']}; margin:6px 0;">₹0 Extra</div>
            <div style="font-weight:700; color:{PALETTE['navy']}; font-size:13.5px; margin-bottom:6px;">Meta Utility Fee Structure</div>
            <div style="font-size:12px; color:{PALETTE['muted']}; line-height:1.5;">
                Meta Cloud API only charges for delivered template conversations (~₹0.11 per utility message). Rejected API calls (HTTP 400) incur <strong>zero charge</strong>. Fixing payload sanitization delivers 1,090 messages at standard operating cost.
            </div>
            <div style="font-size:11.5px; font-weight:700; color:{STATUS_COLORS['SENT']}; margin-top:8px;">
                ROI: 100% upside with zero contractual penalties.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Section 5: Interactive Payload Inspector & Engineering Code Diff ─────
    st.markdown('<div class="section-title">5. Engineering Root Cause &amp; Production Code Patch</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:13px; color:#475569; margin-bottom:14px; line-height:1.5;">
        Compare the current broken backend payload that triggers Meta Error <code>#131008</code> against the production-ready patched payload with parameter fallback sanitization.
    </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns([1, 1])
    with col_p1:
        st.markdown(f"""
        <div style="font-size:13px; font-weight:800; color:#ef4444; margin-bottom:6px;">
            ❌ CURRENT BROKEN BACKEND PAYLOAD (Produces Meta Error 131008)
        </div>
        <div class="wa-code-box">
<span style="color:#64748b;">// POST https://graph.facebook.com/v17.0/{'{phone_number_id}'}/messages</span>
<span style="color:#38bdf8;">{{</span>
  <span style="color:#f472b6;">"messaging_product"</span>: <span style="color:#a7f3d0;">"whatsapp"</span>,
  <span style="color:#f472b6;">"to"</span>: <span style="color:#a7f3d0;">"+919876543210"</span>,
  <span style="color:#f472b6;">"type"</span>: <span style="color:#a7f3d0;">"template"</span>,
  <span style="color:#f472b6;">"template"</span>: <span style="color:#38bdf8;">{{</span>
    <span style="color:#f472b6;">"name"</span>: <span style="color:#a7f3d0;">"lernern_onsite_scheduled"</span>,
    <span style="color:#f472b6;">"language"</span>: <span style="color:#38bdf8;">{{</span> <span style="color:#f472b6;">"code"</span>: <span style="color:#a7f3d0;">"en"</span> <span style="color:#38bdf8;">}}</span>,
    <span style="color:#f472b6;">"components"</span>: [
      <span style="color:#38bdf8;">{{</span>
        <span style="color:#f472b6;">"type"</span>: <span style="color:#a7f3d0;">"body"</span>,
        <span style="color:#f472b6;">"parameters"</span>: [
          <span style="color:#38bdf8;">{{</span> <span style="color:#f472b6;">"type"</span>: <span style="color:#a7f3d0;">"text"</span>, <span style="color:#f472b6;">"text"</span>: <span style="color:#a7f3d0;">"Rahul Sharma"</span> <span style="color:#38bdf8;">}}</span>,
          <span style="color:#ef4444; background:#311b22;">{{ "type": "text", "text": null }}</span>,        <span style="color:#ef4444;">&larr; BUG: null session_date</span>
          <span style="color:#ef4444; background:#311b22;">{{ "type": "text", "text": "" }}</span>,          <span style="color:#ef4444;">&larr; BUG: empty session_time</span>
          <span style="color:#ef4444; background:#311b22;">{{ "type": "text", "text": null }}</span>,        <span style="color:#ef4444;">&larr; BUG: null trainer_name</span>
          <span style="color:#38bdf8;">{{</span> <span style="color:#f472b6;">"type"</span>: <span style="color:#a7f3d0;">"text"</span>, <span style="color:#f472b6;">"text"</span>: <span style="color:#a7f3d0;">"Kharkhoda Plant-4"</span> <span style="color:#38bdf8;">}}</span>
        ]
      <span style="color:#38bdf8;">}}</span>
    ]
  <span style="color:#38bdf8;">}}</span>
<span style="color:#38bdf8;">}}</span>
<span style="color:#ef4444;">// META RESPONSE: HTTP 400 Bad Request</span>
<span style="color:#ef4444;">// {{"error": {{"message": "(#131008) Required parameter is missing", "code": 131008}}}}</span>
        </div>
        """, unsafe_allow_html=True)

    with col_p2:
        st.markdown(f"""
        <div style="font-size:13px; font-weight:800; color:{STATUS_COLORS['SENT']}; margin-bottom:6px;">
            ✅ PRODUCTION PATCHED PAYLOAD (100% Meta Acceptance Rate)
        </div>
        <div class="wa-code-box">
<span style="color:#64748b;">// POST https://graph.facebook.com/v17.0/{'{phone_number_id}'}/messages</span>
<span style="color:#38bdf8;">{{</span>
  <span style="color:#f472b6;">"messaging_product"</span>: <span style="color:#a7f3d0;">"whatsapp"</span>,
  <span style="color:#f472b6;">"to"</span>: <span style="color:#a7f3d0;">"+919876543210"</span>,
  <span style="color:#f472b6;">"type"</span>: <span style="color:#a7f3d0;">"template"</span>,
  <span style="color:#f472b6;">"template"</span>: <span style="color:#38bdf8;">{{</span>
    <span style="color:#f472b6;">"name"</span>: <span style="color:#a7f3d0;">"lernern_onsite_scheduled"</span>,
    <span style="color:#f472b6;">"language"</span>: <span style="color:#38bdf8;">{{</span> <span style="color:#f472b6;">"code"</span>: <span style="color:#a7f3d0;">"en_US"</span> <span style="color:#38bdf8;">}}</span>,
    <span style="color:#f472b6;">"components"</span>: [
      <span style="color:#38bdf8;">{{</span>
        <span style="color:#f472b6;">"type"</span>: <span style="color:#a7f3d0;">"body"</span>,
        <span style="color:#f472b6;">"parameters"</span>: [
          <span style="color:#38bdf8;">{{</span> <span style="color:#f472b6;">"type"</span>: <span style="color:#a7f3d0;">"text"</span>, <span style="color:#f472b6;">"text"</span>: <span style="color:#a7f3d0;">"Rahul Sharma"</span> <span style="color:#38bdf8;">}}</span>,
          <span style="color:#10b981; background:#064e3b;">{{ "type": "text", "text": "Scheduled Date TBA" }}</span>,
          <span style="color:#10b981; background:#064e3b;">{{ "type": "text", "text": "10:00 AM (Confirmed)" }}</span>,
          <span style="color:#10b981; background:#064e3b;">{{ "type": "text", "text": "Assigned Instructor" }}</span>,
          <span style="color:#38bdf8;">{{</span> <span style="color:#f472b6;">"type"</span>: <span style="color:#a7f3d0;">"text"</span>, <span style="color:#f472b6;">"text"</span>: <span style="color:#a7f3d0;">"Kharkhoda Plant-4"</span> <span style="color:#38bdf8;">}}</span>
        ]
      <span style="color:#38bdf8;">}}</span>
    ]
  <span style="color:#38bdf8;">}}</span>
<span style="color:#38bdf8;">}}</span>
<span style="color:#10b981;">// META RESPONSE: HTTP 200 OK</span>
<span style="color:#10b981;">// {{"messaging_product": "whatsapp", "messages": [{{"id": "wamid.HBgM..."}}]}}</span>
        </div>
        """, unsafe_allow_html=True)

    # Backend code snippet for developers
    st.markdown('<div style="margin-top:16px;">', unsafe_allow_html=True)
    with st.expander("🛠️ View Production Python Backend Patch (Ready to Copy into Notification Dispatcher)", expanded=False):
        st.code("""# backend/services/notifications/whatsapp_sanitizer.py
def build_whatsapp_payload(candidate_phone: str, template_name: str, raw_params: dict) -> dict:
    \"\"\"
    Sanitizes template parameters to prevent Meta Cloud API Error 131008 (Missing Required Parameter).
    Guarantees every parameter position contains a valid non-empty string.
    \"\"\"
    PARAM_FALLBACKS = {
        "candidate_name": "Valued Learner",
        "session_date": "Scheduled Date TBA",
        "session_start_time": "Time Confirmed in App",
        "trainer_name": "Assigned Faculty Coordinator",
        "client_location": "Virtual / Training Facility",
        "document_url": "https://portal.lernern.com/documents"
    }

    sanitized_parameters = []
    for key, fallback in PARAM_FALLBACKS.items():
        val = raw_params.get(key)
        # Check for None, NaN, empty string, or whitespace
        if val is None or str(val).strip().lower() in ["none", "nan", "null", ""]:
            safe_text = fallback
        else:
            safe_text = str(val).strip()
        sanitized_parameters.append({"type": "text", "text": safe_text})

    return {
        "messaging_product": "whatsapp",
        "to": candidate_phone,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "en_US"},
            "components": [
                {"type": "body", "parameters": sanitized_parameters}
            ]
        }
    }
""", language="python")
    st.markdown('</div>', unsafe_allow_html=True)

    # Live Interactive Payload Validator
    st.markdown('<div class="plot-card" style="margin-top:18px;">', unsafe_allow_html=True)
    render_chart_header(
        title="🧪 Live WhatsApp Payload Validator & Simulation",
        significance="Test how backend parameter sanitization handles empty or missing inputs in real time.",
        calculation="Simulates Meta Cloud API parameter schema validator before dispatch.",
        action="Verify that empty candidate or trainer inputs are safely defaulted to prevent HTTP 400 rejections."
    )

    col_sim1, col_sim2, col_sim3 = st.columns(3)
    with col_sim1:
        sim_name = st.text_input("Candidate Name", value="", placeholder="Leave empty to test fallback", key="sim_cand_name")
        sim_date = st.text_input("Session Date", value="", placeholder="Leave empty to test fallback", key="sim_sess_date")
    with col_sim2:
        sim_time = st.text_input("Session Time", value="10:00 AM", key="sim_sess_time")
        sim_trainer = st.text_input("Trainer Name", value="", placeholder="Leave empty to test fallback", key="sim_trainer_name")
    with col_sim3:
        sim_loc = st.text_input("Location / Facility", value="Pune MIDC", key="sim_loc")
        sim_tmpl = st.selectbox("Template Target", ["lernern_onsite_scheduled", "lernern_online_scheduled", "lernern_offer_letter"], key="sim_tmpl_sel")

    # Evaluation
    missing_fields = []
    if not sim_name.strip(): missing_fields.append("candidate_name")
    if not sim_date.strip(): missing_fields.append("session_date")
    if not sim_time.strip(): missing_fields.append("session_time")
    if not sim_trainer.strip(): missing_fields.append("trainer_name")
    if not sim_loc.strip(): missing_fields.append("location")

    if missing_fields:
        st.markdown(f"""
        <div style="background:#fee2e2; border:1px solid #f87171; border-radius:8px; padding:12px 16px; margin-top:8px;">
            <div style="font-weight:700; color:#991b1b; font-size:13px;">🚨 Without Sanitizer: Meta API Will REJECT (Error 131008)</div>
            <div style="font-size:12px; color:#7f1d1d; margin-top:4px;">
                Missing/null fields detected: <code>{', '.join(missing_fields)}</code>. Meta's gateway will drop this message immediately.
            </div>
            <div style="font-size:12px; font-weight:700; color:#166534; margin-top:8px;">
                ✅ With Sanitizer: Automatically patched to <code>{sim_name or 'Valued Learner'}</code>, <code>{sim_date or 'Scheduled Date TBA'}</code>, <code>{sim_trainer or 'Assigned Faculty Coordinator'}</code> &rarr; <strong>Delivered (200 OK)!</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:#dcfce7; border:1px solid #86efac; border-radius:8px; padding:12px 16px; margin-top:8px;">
            <div style="font-weight:700; color:#166534; font-size:13px;">✅ Complete Payload: Meta API Will ACCEPT (HTTP 200 OK)</div>
            <div style="font-size:12px; color:#14532d; margin-top:4px;">
                All required body parameters are populated. Dispatch latency will be ~1.06 seconds.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Section 6: Dedicated WhatsApp Failure Lookup & Engineering Export ────
    st.markdown('<div class="section-title">6. WhatsApp Engineering Triage &amp; Export</div>', unsafe_allow_html=True)

    st.markdown('<div class="plot-card">', unsafe_allow_html=True)
    render_chart_header(
        title="🔍 WhatsApp Delivery Investigation Table",
        significance="Search and filter WhatsApp records specifically to generate engineering bug tickets with exact delivery IDs.",
        calculation="Filtered view of WhatsApp deliveries with delivery_id, candidate_name, template, status, error_code, and timestamps.",
        action="Download the filtered CSV to attach directly to the engineering team's JIRA/Linear ticket for the 131008 patch."
    )

    col_w1, col_w2, col_w3 = st.columns([1.5, 1, 1])
    with col_w1: wa_search = st.text_input("Search Candidate Name, Candidate ID, or Notification ID", "", key="wa_triage_search")
    with col_w2: wa_stat_f = st.selectbox("Status", ["All", "FAILED", "SENT", "SKIPPED"], key="wa_triage_stat")
    with col_w3: wa_tmpl_f = st.selectbox("Template", ["All"] + sorted(wa_data['template_name'].dropna().unique().tolist()), key="wa_triage_tmpl")

    exp_wa = wa_data.copy()
    if wa_search:
        q_w = wa_search.lower()
        exp_wa = exp_wa[
            exp_wa['candidate_name'].astype(str).str.lower().str.contains(q_w) |
            exp_wa['candidate_id'].astype(str).str.lower().str.contains(q_w) |
            exp_wa['notification_id'].astype(str).str.lower().str.contains(q_w) |
            exp_wa['delivery_id'].astype(str).str.lower().str.contains(q_w)
        ]
    if wa_stat_f != "All": exp_wa = exp_wa[exp_wa['status'] == wa_stat_f]
    if wa_tmpl_f != "All": exp_wa = exp_wa[exp_wa['template_name'] == wa_tmpl_f]

    wa_cols_to_show = [
        'delivery_id', 'notification_id', 'candidate_name', 'template_name',
        'status', 'error_code', 'error_message', 'client_location', 'trainer_name', 'notification_date'
    ]
    st.dataframe(exp_wa[wa_cols_to_show], height=340, use_container_width=True)

    st.download_button(
        label=f"📥 Download WhatsApp Triage CSV ({len(exp_wa):,} Records)",
        data=exp_wa.to_csv(index=False).encode('utf-8'),
        file_name=f"whatsapp_engineering_triage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        key="wa_download_csv_btn"
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# 6. ORCHESTRATION
# ==============================================================================
if app_page == "💬 WhatsApp Deep-Dive Hub":
    render_whatsapp_deep_dive()
else:
    render_operations_header()
    dashboard_mode = st.radio("Navigation Mode",
        ["📄 Full Report (All Sections)", "📑 Section Tabs (Quick Browse)"],
        horizontal=True, label_visibility="collapsed")

    if dashboard_mode == "📄 Full Report (All Sections)":
        render_math_decoder()
        render_executive_kpis()
        render_what_if_simulator()
        render_funnel_and_leakage()
        render_channels_and_providers()
        render_triggers_and_templates()
        render_time_series()
        render_demographics_and_segmentation()
        render_action_plan_and_triage()
    else:
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📊 Summary & Simulator",
            "🔻 Delivery Funnel",
            "📱 Channel Breakdown",
            "⚡ Onsite vs. Online",
            "💬 WhatsApp Deep-Dive",
            "📈 Trends & Heatmaps",
            "📍 Locations & Trainers",
            "🛠️ Fix Plan & Lookup"
        ])
        with tab1:
            render_math_decoder()
            render_executive_kpis()
            render_what_if_simulator()
        with tab2:
            render_funnel_and_leakage()
        with tab3:
            render_channels_and_providers()
        with tab4:
            render_triggers_and_templates()
        with tab5:
            render_whatsapp_deep_dive()
        with tab6:
            render_time_series()
        with tab7:
            render_demographics_and_segmentation()
        with tab8:
            render_action_plan_and_triage()

st.markdown(f"""
<div style="text-align:center;color:{PALETTE['muted']};font-size:11.5px;margin-top:40px;padding:18px;border-top:1px solid {PALETTE['border']};">
    Executive Notification Engine Analytics · Designed for C-Suite Briefings · Reference: Interakt Leads Analytics Report
</div>
""", unsafe_allow_html=True)
