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

---

## 🔍 Data Analyst Key Findings

| Metric | Measured Value | Operational Assessment |
| :--- | :--- | :--- |
| **Total Notification Requests** | 1,308 | Multi-channel engine load |
| **Total Delivery Legs Attempted** | 3,924 | ~3.0 delivery legs per request |
| **Candidate Reachability (≥1 Ch)** | **67.66%** | 885 candidates reached |
| **Complete Drop-off Rate (0 Ch)** | **32.34%** | **423 candidates completely dropped** |
| **Channel-Level Sent Rate** | **23.37%** | 917 of 3,924 attempts sent |
| **Median Dispatch Latency** | **2.91s** | Optimal velocity (< 5s SLA) |
| **P95 Latency SLA** | **3.58s** | Compliant with SLA |

### Critical Root Causes:
- **WhatsApp (84.0% Failure Rate):** 1,090 failures caused by `Meta API 131008: Required parameter is missing`. The backend webhook omits mandatory template parameters.
- **Mobile Push (95.2% Skipped, 0% Sent):** 1,239 skips caused by `missing push tokens` because mobile app device tokens are not synced to the WMS profile database.
- **Email (55.4% Sent, 44.6% Skipped):** 100% reliable when data is present; 584 skipped due to missing email addresses in candidate records.
- **Online vs. Onsite Crisis:** Online candidates only provide mobile numbers. When WhatsApp fails via API parameter error and Push lacks device tokens, missing email results in **100% notification blackout for 74.2% of online candidates**.

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
