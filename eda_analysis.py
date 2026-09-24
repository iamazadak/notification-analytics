import pandas as pd
import numpy as np
import json
import sys

# Replace standard output with utf-8 writer or write directly to file
df = pd.read_csv("Notification_Engine_Analytics - vw_notification_analytics.csv", low_memory=False)

with open("eda_report.txt", "w", encoding="utf-8") as out:
    def p(text=""):
        out.write(str(text) + "\n")

    p(f"Total Rows (delivery records): {len(df)}")
    p(f"Unique Notifications: {df['notification_id'].nunique()}")
    p(f"Unique External Ref IDs: {df['external_ref_id'].nunique()}")
    p(f"Unique Candidates: {df['candidate_id'].nunique()}")
    p(f"Unique Delivery IDs: {df['delivery_id'].nunique()}")
    p(f"Date Range: {df['notification_date'].min()} to {df['notification_date'].max()}")
    
    p("\n=== STATUS BREAKDOWN ===")
    status_summary = pd.DataFrame({
        'Count': df['status'].value_counts(),
        'Percentage': (df['status'].value_counts(normalize=True) * 100).round(2)
    })
    p(status_summary.to_string())

    p("\n=== CHANNEL BREAKDOWN ===")
    channel_summary = pd.DataFrame({
        'Total Attempts': df['channel'].value_counts(),
        'Percentage': (df['channel'].value_counts(normalize=True) * 100).round(2)
    })
    p(channel_summary.to_string())

    p("\n=== CHANNEL x STATUS CROSS-TABULATION ===")
    ct = pd.crosstab(df['channel'], df['status'], margins=True)
    p(ct.to_string())
    p("\nRow Percentages:")
    ct_pct = pd.crosstab(df['channel'], df['status'], normalize='index').round(4) * 100
    p(ct_pct.to_string())

    p("\n=== TRIGGER TYPE BREAKDOWN ===")
    tt_summary = pd.crosstab(df['trigger_type'], df['status'], margins=True)
    p(tt_summary.to_string())

    p("\n=== REQUESTED CHANNELS COMBINATIONS ===")
    p(df['requested_channels'].value_counts().to_string())

    p("\n=== ERROR MESSAGES (All Unique) ===")
    p(df['error_message'].value_counts(dropna=False).to_string())

    p("\n=== ERROR CODES (All Unique) ===")
    p(df['error_code'].value_counts(dropna=False).to_string())

    p("\n=== ERROR CODE x ERROR MESSAGE ===")
    err_cross = df.groupby(['error_code', 'error_message', 'channel'], dropna=False).size().reset_index(name='count')
    p(err_cross.to_string())

    p("\n=== DISPATCH TO SENT SECONDS (Latency Analysis) ===")
    latency = df['dispatch_to_sent_seconds'].dropna()
    p(f"Valid Latency Counts: {len(latency)}")
    p(latency.describe().to_string())
    p(f"Median: {latency.median()}")
    p(f"P90: {latency.quantile(0.90)}")
    p(f"P95: {latency.quantile(0.95)}")
    p(f"P99: {latency.quantile(0.99)}")
    p("\nLatency by Channel (dispatch_to_sent_seconds):")
    p(df.groupby('channel')['dispatch_to_sent_seconds'].describe().to_string())

    p("\n=== TEMPLATES PERFORMANCE ===")
    p(pd.crosstab(df['template_name'], df['status'], margins=True).to_string())

    p("\n=== CLIENT LOCATIONS ===")
    p(pd.crosstab(df['client_location'].fillna('Unknown / Virtual'), df['status'], margins=True).to_string())

    p("\n=== TRAINER PERFORMANCE ===")
    p(pd.crosstab(df['trainer_name'].fillna('Not Specified'), df['status'], margins=True).to_string())

    p("\n=== TIME ANALYSIS (By Notification Date) ===")
    p(pd.crosstab(df['notification_date'], df['status'], margins=True).to_string())

    p("\n=== TIME ANALYSIS (By Day Name) ===")
    p(pd.crosstab(df['notification_day_name'], df['status'], margins=True).to_string())

    p("\n=== TIME ANALYSIS (By Hour of Day) ===")
    p(pd.crosstab(df['notification_hour'], df['status'], margins=True).to_string())

    p("\n=== MISSING/NULL VALUES PROFILE ===")
    null_profile = pd.DataFrame({
        'Missing Count': df.isnull().sum(),
        'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
    })
    p(null_profile[null_profile['Missing Count'] > 0].to_string())

print("Report written to eda_report.txt successfully!")
