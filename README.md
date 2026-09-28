# 📈 Notification Engine Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://notification-analytics.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade **Notification Engine Analytics Dashboard** built in Python and Streamlit, designed from a Senior Data Analyst perspective. It visualizes multi-channel delivery funnels, failure leakages, temporal load dynamics, client demographic segmentation, gateway latency SLAs, and root-cause engineering remediation pathways.

The aesthetic, color palette, scorecard architecture, and layout are directly referenced from executive reporting designs (such as the *Interakt Leads Analytics Dashboard*).

---

## 🚀 Key Features

1. **Executive Scorecards (KPIs & Velocity):**
   - Total Notifications Created, Delivery Attempts (Legs), Candidate Reachability Rate (≥1 Channel), Channel Sent Rate, Average/Median Latency, and Unreached Candidate Blackout Rate.
2. **Funnel & Leakage Analysis:**
   - Dual-perspective pipeline snapshot (Channel Legs vs. Candidate Notifications).
   - Top Drop-off Reasons horizontal bar chart with interactive drill-down expanders.
3. **Time-Series Trends & Influx Heatmap:**
   - Stacked daily volume with dual-axis success rate trendline.
   - Day-of-week influx distribution.
   - 2D Heatmap of Day of Week vs. Hour of Day (12 AM–11 PM UTC/IST) identifying peak morning scheduling batches.
4. **Multi-Channel & Provider Breakdown:**
   - Channel Funnel Breakdown (Email, WhatsApp, Push, SMS) comparing Sent, Failed, and Skipped attempts.
   - Channel performance summary matrix with failure bottleneck tagging.
5. **Demographic & Operational Segmentation:**
   - Delivery performance by Client Location (Pune MIDC, Silvassa, Sangareddy, etc.) and Assigned Trainer.
6. **Trigger Type & Template Disparities:**
   - Contrast analysis revealing why Onsite Class Scheduling achieves **96.7% reachability** while Online Scheduling drops to **25.8%**.
7. **Latency & SLA Velocity Performance:**
   - Distribution histogram and boxplot analysis for `dispatch_to_sent_seconds`.
   - SLA percentile benchmarks (P50, P90, P95, P99, Max outlier).
8. **Root-Cause Diagnostics & Engineering Action Plan:**
   - Structured remediation items for Meta WhatsApp API 131008, Mobile Push Token sync, WMS Email validation, and India TRAI DLT SMS registration.
9. **Interactive Raw Data Explorer & Triage:**
   - Real-time text search (Candidate Name, ID, External Ref), status filtering, and one-click CSV export.
10. **Dedicated WhatsApp Analysis Hub:**
    - End-to-end Meta Cloud API audit decoding Error #131008 (Missing parameters), Error #132018 (Schema format), and Error #132001 (Translation mismatch).
    - 7-Template performance matrix exposing the 97.4% failure rate on online scheduled classes.
    - Hourly batch timing chart isolating the 873 early morning failures (4 AM – 8 AM).
    - Multi-channel ripple effect showing how WhatsApp failure strands 423 students with zero notifications.
    - Side-by-side broken vs. patched JSON payload diff, production Python patch, and live interactive payload validator.
    - Dedicated WhatsApp failure triage table and JIRA-ready CSV export.

---

## 🔍 Plain English Numbers Guide (Everything Sums to 100%)

The dataset operates across **three distinct levels**:

1. **People (884 Unique Candidates):**
   - **525 Reached (59.4%)** received at least one alert.
   - **359 Missed (40.6%)** never received any alert.
   - *Sum: 525 + 359 = 884 Candidates (100%)*

2. **Messages (1,308 Business Alerts):**
   - **885 Delivered (67.7%)** reached the candidate on ≥1 channel.
   - **423 Completely Lost (32.3%)** failed on every channel.
   - *Sum: 885 + 423 = 1,308 Messages (100%)*

3. **Channel Tries (3,924 Delivery Attempts):**
   - System tries ~3 channels per alert (Push, WhatsApp, Email).
   - **917 Sent (23.4%)** successfully accepted by gateway.
   - **1,839 Skipped (46.9%)** due to missing phone tokens or emails.
   - **1,168 Failed (29.8%)** primarily from WhatsApp template error 131008.
   - *Sum: 917 + 1,839 + 1,168 = 3,924 Channel Tries (100%)*

> **Why does 917 Sent Tries ≠ 885 Delivered Messages?**  
> 32 candidates received the message on **both** WhatsApp and Email!  
> Math: 853 single-channel + (32 × 2 dual-channel) = **917 successful tries**. Everything adds up!

### The 3 Core Culprits:
- **WhatsApp Bug (1,090 Failures):** Automated payload omitted class date or trainer name. Fixable in 1 day.
- **Mobile Push Missing Tokens (1,239 Skips):** App never recorded device token on candidate login.
- **Missing Email for Online Students (584 Skips):** Online sign-up didn't ask for email, causing 74.2% of online class alerts to drop completely.

---

## 📦 Project Structure

```
Notification_Engine_Analytics/
├── app.py                                              # Main Streamlit Dashboard Application
├── Notification_Engine_Analytics - vw_notification_analytics.csv  # Raw Dataset
├── Notification_Engine_Data_Analysis_Report.md         # Comprehensive Analytical Report
├── eda_analysis.py                                     # Exploratory Data Analysis Script
├── deep_dive.py                                        # Root-cause Investigation Script
├── requirements.txt                                    # Python Package Dependencies
├── .gitignore                                          # Git Exclusion Rules
└── README.md                                           # Repository Documentation
```

---

## 🛠️ Installation & Quickstart

### Prerequisites
- Python 3.10 or higher
- `pip` package manager

### 1. Clone the Repository
```bash
git clone git@github.com:iamazadak/notification-analytics.git
cd notification-analytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Dashboard
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 🎨 Color Palette & Visual System

Directly aligned with executive report styling:
- **Primary Navy:** `#1a4673`
- **Vibrant Teal (Success/Sent):** `#1f9a89`
- **Ocean Blue:** `#2c79c5`
- **Sky Blue:** `#4885cd`
- **Deep Purple:** `#7e519e`
- **Soft Coral (Failed/Warning):** `#eb7966`
- **Crimson Red:** `#c45f64`
- **Warm Amber (Skipped):** `#cda36f`
- **Slate Text:** `#30333e`

---

## 📄 License
This project is licensed under the MIT License.
