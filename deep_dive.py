import pandas as pd
import numpy as np

df = pd.read_csv("Notification_Engine_Analytics - vw_notification_analytics.csv", low_memory=False)

with open("deep_dive_report.txt", "w", encoding="utf-8") as f:
    f.write("=== DEEP DIVE: WHATSAPP BY TEMPLATE ===\n")
    wa = df[df['channel'] == 'whatsapp']
    ct_wa = pd.crosstab(wa['template_name'], wa['error_message'].fillna('SUCCESS (SENT)'), margins=True)
    f.write(ct_wa.to_string() + "\n\n")

    f.write("=== DEEP DIVE: EMAIL BY TEMPLATE ===\n")
    em = df[df['channel'] == 'email']
    ct_em = pd.crosstab(em['template_name'], em['error_message'].fillna('SUCCESS (SENT)'), margins=True)
    f.write(ct_em.to_string() + "\n\n")

    f.write("=== DEEP DIVE: PUSH BY TEMPLATE ===\n")
    pu = df[df['channel'] == 'push']
    ct_pu = pd.crosstab(pu['template_name'], pu['error_message'].fillna('SUCCESS (SENT)'), margins=True)
    f.write(ct_pu.to_string() + "\n\n")

    f.write("=== NOTIFICATION-LEVEL DELIVERY OUTCOMES ===\n")
    notif_summary = df.groupby('notification_id').agg(
        trigger=('trigger_type', 'first'),
        template=('template_name', 'first'),
        candidate_id=('candidate_id', 'first'),
        candidate_name=('candidate_name', 'first'),
        date=('notification_date', 'first'),
        channels_requested=('requested_channels', 'first'),
        sent_count=('sent_flag', 'sum'),
        failed_count=('failed_flag', 'sum'),
        skipped_count=('skipped_flag', 'sum'),
        has_sent=('sent_flag', lambda x: int(x.sum() > 0))
    ).reset_index()

    f.write(f"Total Unique Notifications: {len(notif_summary)}\n")
    f.write(f"Notifications Reached (>=1 sent): {notif_summary['has_sent'].sum()} ({notif_summary['has_sent'].mean()*100:.2f}%)\n")
    f.write(f"Notifications Dropped (0 sent): {(notif_summary['has_sent'] == 0).sum()} ({(1-notif_summary['has_sent'].mean())*100:.2f}%)\n\n")

    f.write("=== NOTIFICATION REACHABILITY BY TRIGGER TYPE ===\n")
    reach_by_trig = notif_summary.groupby('trigger').agg(
        total=('notification_id', 'count'),
        reached=('has_sent', 'sum'),
        dropped=('has_sent', lambda x: (x == 0).sum()),
        reach_rate=('has_sent', lambda x: round(x.mean() * 100, 2))
    )
    f.write(reach_by_trig.to_string() + "\n\n")

    f.write("=== NOTIFICATION REACHABILITY BY DATE ===\n")
    reach_by_date = notif_summary.groupby('date').agg(
        total=('notification_id', 'count'),
        reached=('has_sent', 'sum'),
        dropped=('has_sent', lambda x: (x == 0).sum()),
        reach_rate=('has_sent', lambda x: round(x.mean() * 100, 2))
    )
    f.write(reach_by_date.to_string() + "\n\n")

    f.write("=== CANDIDATE-LEVEL REACHABILITY ===\n")
    cand_summary = notif_summary.groupby('candidate_id').agg(
        total_notifications=('notification_id', 'count'),
        any_reached=('has_sent', 'max'),
        all_reached=('has_sent', 'min')
    )
    f.write(f"Total Candidates: {len(cand_summary)}\n")
    f.write(f"Candidates reached at least once: {cand_summary['any_reached'].sum()} ({cand_summary['any_reached'].mean()*100:.2f}%)\n")
    f.write(f"Candidates NEVER reached: {(cand_summary['any_reached'] == 0).sum()} ({(1-cand_summary['any_reached'].mean())*100:.2f}%)\n")

print("Deep dive report written successfully!")
