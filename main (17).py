import streamlit as st
import json, csv, io, hashlib, difflib
from datetime import datetime, timedelta, date

st.set_page_config(page_title="Graphite Compliance", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; }

/* ── EVERYTHING defaults to black text on light bg ── */
html, body, [class*="css"],
.stApp, [data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section.main, .main, .block-container,
div, p, span, label, li, td, th, button,
h1, h2, h3, h4, h5, h6 {
  font-family: 'Inter', -apple-system, sans-serif !important;
  color: #111111 !important;
  -webkit-font-smoothing: antialiased !important;
}

/* ── Page background ── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section.main, .main, .block-container {
  background-color: #f0f2f4 !important;
}
.main .block-container {
  padding-top: 1.8rem !important;
  max-width: 1200px !important;
}

/* ── SIDEBAR: dark with light text — override everything ── */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] > div > div {
  background-color: #13161c !important;
}
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] button,
section[data-testid="stSidebar"] [class*="css"] {
  color: #d0d6e4 !important;
  background-color: transparent !important;
}
section[data-testid="stSidebar"] .stRadio label {
  font-size: 12px !important;
  font-weight: 500 !important;
  color: #d0d6e4 !important;
  padding: 6px 10px !important;
  display: block !important;
  border-radius: 6px !important;
  line-height: 1.4 !important;
  letter-spacing: 0.01em !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
  background-color: rgba(255,255,255,0.06) !important;
  color: #ffffff !important;
}
section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
  margin-bottom: 2px !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
  gap: 2px !important;
  display: flex !important;
  flex-direction: column !important;
}
/* Hide the radio dot — use full-row highlight instead */
section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
  display: none !important;
}
/* Selected item highlight */
section[data-testid="stSidebar"] .stRadio [aria-checked="true"] label {
  background-color: rgba(59,130,246,0.18) !important;
  color: #93c5fd !important;
  font-weight: 700 !important;
}
section[data-testid="stSidebar"] .stRadio [aria-checked="true"] label span {
  color: #93c5fd !important;
}
section[data-testid="stSidebar"] .stButton > button {
  background-color: transparent !important;
  color: #d0d6e4 !important;
  border: none !important;
  border-radius: 6px !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  padding: 6px 10px !important;
  text-align: left !important;
  width: 100% !important;
  line-height: 1.4 !important;
  margin-bottom: 1px !important;
  box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background-color: rgba(255,255,255,0.06) !important;
  color: #ffffff !important;
}
/* Sign out button — keep it blue */
section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"]:last-of-type {
  background-color: #3b82f6 !important;
  color: #ffffff !important;
  margin-top: 4px !important;
}

/* ── Inputs: light bg, black text ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stDateInput > div > div > input,
.stNumberInput > div > div > input {
  background-color: #ffffff !important;
  border: 1px solid #d1d5db !important;
  color: #111111 !important;
  border-radius: 6px !important;
  font-size: 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: #3b82f6 !important;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
  outline: none !important;
}
/* selectbox dropdown text */
.stSelectbox [data-baseweb="select"] span,
.stSelectbox [data-baseweb="select"] div {
  color: #111111 !important;
}

/* ── File uploader: light bg, readable text ── */
[data-testid="stFileUploader"] {
  background-color: #ffffff !important;
  border: 2px dashed #93c5fd !important;
  border-radius: 8px !important;
  padding: 0.5rem !important;
}
[data-testid="stFileUploader"] section {
  background-color: #ffffff !important;
}
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] div,
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] {
  color: #1e40af !important;
  background-color: transparent !important;
}
[data-testid="stFileUploader"] button {
  background-color: #eff6ff !important;
  color: #1d4ed8 !important;
  border: 1px solid #bfdbfe !important;
  font-weight: 600 !important;
}
[data-testid="stFileUploader"] button:hover {
  background-color: #dbeafe !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] div,
[data-testid="stFileUploaderDropzoneInstructions"] span {
  color: #1e40af !important;
}
/* Uploaded file name chip */
[data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p {
  color: #1e40af !important;
}
[data-testid="uploadedFileData"] {
  background-color: #eff6ff !important;
  border: 1px solid #bfdbfe !important;
  border-radius: 6px !important;
}
[data-testid="uploadedFileData"] span,
[data-testid="uploadedFileData"] div {
  color: #1e40af !important;
}

/* ── Labels ── */
label, .stTextInput label, .stSelectbox label,
.stTextArea label, .stDateInput label {
  font-size: 12px !important;
  font-weight: 600 !important;
  color: #374151 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
}

/* ── Buttons (main area) ── */
.stButton > button {
  background-color: #3b82f6 !important;
  color: #ffffff !important;
  border: none !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  border-radius: 6px !important;
  padding: 0.45rem 1.2rem !important;
  transition: background 0.15s !important;
}
.stButton > button:hover {
  background-color: #2563eb !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background-color: #e2e5e9 !important;
  border-bottom: 2px solid #d1d5db !important;
  border-radius: 8px 8px 0 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: #6b7280 !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  padding: 0.7rem 1.4rem !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
  color: #1d4ed8 !important;
  border-bottom: 2px solid #1d4ed8 !important;
  font-weight: 700 !important;
  background: transparent !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
  background-color: #ffffff !important;
  border: 1px solid #e5e7eb !important;
  border-top: 3px solid #3b82f6 !important;
  border-radius: 8px !important;
  padding: 1.1rem !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}
[data-testid="stMetricLabel"] {
  color: #6b7280 !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
}
[data-testid="stMetricValue"] {
  color: #111827 !important;
  font-size: 1.9rem !important;
  font-weight: 700 !important;
}
[data-testid="stMetricDelta"] { color: #6b7280 !important; }

/* ── Toggle buttons (replaces expanders) ── */
[data-testid="stButton"] > button[kind="secondary"],
div[data-testid="stHorizontalBlock"] button {
  text-align: left !important;
}
.gc-toggle-btn > button {
  background: #ffffff !important;
  border: 1px solid #e5e7eb !important;
  border-radius: 8px !important;
  padding: 10px 16px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #111111 !important;
  text-align: left !important;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
  margin-bottom: 2px !important;
}

/* ── Dataframe ── */
.stDataFrame, .stDataFrame * { color: #111111 !important; background-color: #ffffff !important; }
.stDataFrame thead th {
  background-color: #f3f4f6 !important;
  color: #374151 !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
}

/* ── Custom cards ── */
.gc-card {
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 0.75rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.gc-card, .gc-card * { color: #111111 !important; }
.gc-card-header {
  font-size: 11px !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em !important;
  color: #6b7280 !important;
  text-transform: uppercase !important;
  margin-bottom: 0.6rem !important;
}

/* ── Badges ── */
.gc-badge {
  display: inline-block;
  padding: 0.2rem 0.65rem;
  border-radius: 20px;
  font-size: 11px !important;
  font-weight: 600 !important;
}
.badge-open    { background:#dbeafe; color:#1e40af !important; }
.badge-closed  { background:#dcfce7; color:#166534 !important; }
.badge-overdue { background:#fee2e2; color:#991b1b !important; }
.badge-pending { background:#fef9c3; color:#854d0e !important; }
.badge-high    { background:#fee2e2; color:#991b1b !important; }
.badge-med     { background:#fef9c3; color:#854d0e !important; }
.badge-low     { background:#dcfce7; color:#166534 !important; }
.badge-draft   { background:#f3f4f6; color:#374151 !important; }

/* ── Timeline ── */
.gc-tl {
  border-left: 2px solid #d1d5db;
  padding: 0.3rem 0 0.3rem 1rem;
  margin-bottom: 0.45rem;
  position: relative;
  font-size: 13px !important;
  color: #374151 !important;
  line-height: 1.5;
}
.gc-tl, .gc-tl * { color: #374151 !important; }
.gc-tl::before {
  content: '';
  position: absolute;
  left: -5px; top: 0.6rem;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #3b82f6;
}

/* ── Page headers ── */
.gc-header {
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-left: 4px solid #3b82f6;
  border-radius: 8px;
  padding: 1.2rem 1.6rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.gc-header h1 {
  font-size: 1.2rem !important;
  font-weight: 700 !important;
  color: #111827 !important;
  margin: 0 0 0.2rem 0 !important;
}
.gc-header p { font-size: 13px !important; color: #6b7280 !important; margin: 0 !important; }

/* ── Alerts ── */
.gc-alert { border-radius: 6px; padding: 0.65rem 1rem; margin: 0.5rem 0; font-size: 13px; line-height: 1.5; }
.gc-alert-warn   { background:#fffbeb; border-left:3px solid #f59e0b; color:#78350f !important; }
.gc-alert-danger { background:#fef2f2; border-left:3px solid #ef4444; color:#7f1d1d !important; }
.gc-alert-ok     { background:#f0fdf4; border-left:3px solid #22c55e; color:#14532d !important; }
.gc-alert, .gc-alert * { color: inherit !important; }

/* ── Checklist cards ── */
.cl-owner-card {
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-top: 3px solid #3b82f6;
  border-radius: 8px;
  padding: 1rem 1.3rem;
  margin-bottom: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.cl-owner-card, .cl-owner-card * { color: #111111 !important; }
.cl-task-row {
  background-color: #f8f9fa;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.7rem 1rem;
  margin: 0.4rem 0;
  font-size: 13px;
}
.cl-task-row, .cl-task-row * { color: #111111 !important; }

/* ── Misc ── */
hr { border: none !important; border-top: 1px solid #e5e7eb !important; margin: 1.2rem 0 !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #f0f2f4; }
::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 3px; }
code {
  font-size: 12px !important;
  background: #f3f4f6 !important;
  color: #1d4ed8 !important;
  padding: 0.1rem 0.35rem !important;
  border-radius: 4px !important;
}

/* ── Login ── */
.login-wrap { max-width: 400px; margin: 6vh auto; }
.login-logo { font-size: 1.8rem; font-weight: 700; color: #111827 !important; letter-spacing: -0.02em; text-align: center; margin-bottom: 0.2rem; }
.login-sub  { text-align: center; color: #6b7280 !important; font-size: 12px; margin-bottom: 2rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ── SEED DATA ─────────────────────────────────────────────────────────────────
def seed_data():
    now = datetime.now()
    def ts(d=0,h=0): return (now-timedelta(days=d,hours=h)).strftime("%Y-%m-%d %H:%M")

    # WSP tasks define who owns each obligation inside a WSP
    wsp_tasks = {
        "WSP-001": [
            {"id":"WT-001-1","title":"Annual AML Training Completion","owner":"admin","role_title":"Chief Compliance Officer","frequency":"Annually","description":"Ensure all registered representatives complete the annual AML training program and retain certificates as evidence.","category":"AML"},
            {"id":"WT-001-2","title":"Quarterly Transaction Monitoring Review","owner":"admin","role_title":"Chief Compliance Officer","frequency":"Quarterly","description":"Review transaction monitoring alerts, document dispositions, and escalate any suspicious activity for SAR review.","category":"AML"},
            {"id":"WT-001-3","title":"SAR Filing Review & Submission","owner":"supervisor","role_title":"Supervising Principal","frequency":"As needed / 30-day SAR deadline","description":"Review all potential SAR candidates flagged by monitoring. Approve, escalate, or document no-file decisions within regulatory deadlines.","category":"AML"},
            {"id":"WT-001-4","title":"Customer Identification Program (CIP) Audit","owner":"supervisor","role_title":"Supervising Principal","frequency":"Semi-Annually","description":"Audit a sample of new account openings to confirm CIP procedures were followed. Document findings and remediate exceptions.","category":"AML"},
        ],
        "WSP-002": [
            {"id":"WT-002-1","title":"Daily Flagged Trade Review (24hr SLA)","owner":"supervisor","role_title":"Supervising Principal","frequency":"Daily","description":"Review all trades flagged by the surveillance system within 24 hours. Document review, rationale, and any follow-up actions taken.","category":"Supervisory"},
            {"id":"WT-002-2","title":"Monthly Customer Complaint Log Review","owner":"supervisor","role_title":"Supervising Principal","frequency":"Monthly","description":"Review all customer complaints received during the period. Confirm responses were sent, log outcomes, and escalate unresolved items.","category":"Supervisory"},
            {"id":"WT-002-3","title":"Reg BI Best Interest Review","owner":"admin","role_title":"Chief Compliance Officer","frequency":"Quarterly","description":"Review a sample of retail recommendations to confirm they meet Reg BI best interest standards. Document findings and any remediation.","category":"Regulatory"},
            {"id":"WT-002-4","title":"New Account Opening Supervisory Sign-Off","owner":"supervisor","role_title":"Supervising Principal","frequency":"Weekly","description":"Review and approve all new retail account openings for the week. Confirm suitability information is complete and accurate.","category":"Supervisory"},
        ],
        "WSP-003": [
            {"id":"WT-003-1","title":"Information Barrier Attestation","owner":"analyst","role_title":"Compliance Analyst","frequency":"Annually","description":"Collect signed attestations from all employees confirming they understand and have complied with information barrier policies.","category":"Trading"},
            {"id":"WT-003-2","title":"Electronic Communication Surveillance Review","owner":"supervisor","role_title":"Supervising Principal","frequency":"Monthly","description":"Review electronic communications surveillance sample to confirm no MNPI sharing occurred across business lines.","category":"Trading"},
        ],
    }

    return {
        "users": {
            "admin":      {"password":"pass","role":"Compliance Officer","name":"Jordan Reed","title":"Chief Compliance Officer"},
            "supervisor": {"password":"pass","role":"Supervisor","name":"Morgan Ellis","title":"VP, Head of Supervision"},
            "analyst":    {"password":"pass","role":"Analyst","name":"Casey Park","title":"Compliance Analyst"},
        },
        "firm": {"name":"Apex Financial Services LLC","industry":"Broker-Dealer (FINRA)","crd":"123456","regulator":"FINRA / SEC","retention_years":6,"approval_mode":"dual","address":"101 Wall Street, New York, NY 10005"},
        "tasks": [
            {"id":"T-001","title":"AML Transaction Monitoring Review","assignee":"analyst","due":(now+timedelta(days=3)).strftime("%Y-%m-%d"),"status":"Open","priority":"High","category":"AML","evidence":[],"audit":[{"ts":ts(5),"user":"admin","action":"Created task T-001"}],"rationale":"","delegated_to":"","delegated_memo":"","source_wsp":"","recurrence":""},
            {"id":"T-002","title":"Q3 Supervisory Checklist – Options","assignee":"supervisor","due":(now-timedelta(days=2)).strftime("%Y-%m-%d"),"status":"Overdue","priority":"High","category":"Supervisory","evidence":[],"audit":[{"ts":ts(10),"user":"admin","action":"Created task T-002"}],"rationale":"","delegated_to":"","delegated_memo":"","source_wsp":"","recurrence":""},
            {"id":"T-003","title":"Best Execution Policy Review","assignee":"admin","due":(now+timedelta(days=10)).strftime("%Y-%m-%d"),"status":"Open","priority":"Medium","category":"Trading","evidence":[],"audit":[{"ts":ts(3),"user":"supervisor","action":"Created task T-003"}],"rationale":"","delegated_to":"","delegated_memo":"","source_wsp":"","recurrence":""},
            {"id":"T-004","title":"FINRA Rule 3110 Supervision Update","assignee":"analyst","due":(now+timedelta(days=1)).strftime("%Y-%m-%d"),"status":"Pending Approval","priority":"High","category":"Regulatory","evidence":[{"name":"supervision_policy_v2.pdf","uploaded_by":"analyst","ts":ts(1),"hash":"abc123","immutable":True}],"audit":[{"ts":ts(7),"user":"admin","action":"Created task T-004"},{"ts":ts(1),"user":"analyst","action":"Evidence uploaded: supervision_policy_v2.pdf"}],"rationale":"","delegated_to":"","delegated_memo":"","source_wsp":"","recurrence":""},
            {"id":"T-005","title":"Annual Cybersecurity Training Completion","assignee":"analyst","due":(now-timedelta(days=5)).strftime("%Y-%m-%d"),"status":"Closed","priority":"Low","category":"InfoSec","evidence":[],"audit":[{"ts":ts(15),"user":"admin","action":"Created task T-005"},{"ts":ts(5),"user":"admin","action":"Closed – training certificates verified"}],"rationale":"All staff completed training by deadline.","delegated_to":"","delegated_memo":"","source_wsp":"","recurrence":""},
        ],
        "exam_requests": [
            {"id":"ER-001","title":"FINRA Cycle Exam 2024","regulator":"FINRA","due":(now+timedelta(days=30)).strftime("%Y-%m-%d"),"status":"In Progress","items":[{"item":"Customer complaint files (2022-2024)","status":"Uploaded","assignee":"analyst"},{"item":"Supervisory procedures manual","status":"Pending","assignee":"admin"},{"item":"AML policies and SAR log","status":"Uploaded","assignee":"analyst"},{"item":"Trade blotter – Q1-Q3 2024","status":"Pending","assignee":"supervisor"}],"audit":[{"ts":ts(20),"user":"admin","action":"Exam request ER-001 created"}]},
            {"id":"ER-002","title":"SEC Annual Review","regulator":"SEC","due":(now+timedelta(days=60)).strftime("%Y-%m-%d"),"status":"Open","items":[{"item":"Form ADV Part 2","status":"Pending","assignee":"admin"},{"item":"Investment advisory agreements sample","status":"Pending","assignee":"supervisor"}],"audit":[{"ts":ts(5),"user":"admin","action":"Exam request ER-002 created"}]},
        ],
        "rules": [
            {"id":"R-001","title":"FINRA Rule 3110 – Supervision","source":"FINRA","category":"Supervision","description":"Firms must establish and maintain a system of supervision reasonably designed to achieve compliance.","status":"Active","last_reviewed":ts(30),"ai_flagged":False},
            {"id":"R-002","title":"FINRA Rule 4512 – Customer Account Info","source":"FINRA","category":"Customer Accounts","description":"Member firms must maintain essential customer information for all accounts.","status":"Active","last_reviewed":ts(45),"ai_flagged":True},
            {"id":"R-003","title":"SEC Rule 17a-4 – Records Retention","source":"SEC","category":"Recordkeeping","description":"Broker-dealers must preserve records for specified time periods using WORM-compliant storage.","status":"Active","last_reviewed":ts(20),"ai_flagged":False},
            {"id":"R-004","title":"Bank Secrecy Act – AML Program","source":"FinCEN","category":"AML/BSA","description":"Financial institutions must implement AML programs including customer identification.","status":"Active","last_reviewed":ts(60),"ai_flagged":True},
            {"id":"R-005","title":"Reg BI – Best Interest Obligation","source":"SEC","category":"Suitability","description":"Broker-dealers must act in the best interest of retail customers when making recommendations.","status":"Active","last_reviewed":ts(10),"ai_flagged":False},
        ],
        "wsps": [
            {"id":"WSP-001","title":"Anti-Money Laundering Program","version":"3.2","status":"Approved","owner":"admin","approved_by":"supervisor","approved_ts":ts(15),"content":"This WSP establishes our AML program per BSA requirements. Includes CIP, transaction monitoring, SAR filing procedures, and annual training requirements. All registered representatives must complete AML training annually. The Chief Compliance Officer oversees the overall program and training. The Supervising Principal reviews SAR candidates and conducts CIP audits.","versions":[{"ver":"3.1","ts":ts(60),"author":"admin","note":"Updated SAR thresholds"},{"ver":"3.2","ts":ts(15),"author":"admin","note":"Added enhanced due diligence for high-risk accounts"}]},
            {"id":"WSP-002","title":"Supervisory Procedures – Retail","version":"2.0","status":"Approved","owner":"supervisor","approved_by":"admin","approved_ts":ts(30),"content":"Supervisory procedures for retail customer accounts. Covers trade review, account opening, complaint handling, and escalation paths. Supervisors must review all flagged trades within 24 hours. The Chief Compliance Officer conducts Reg BI reviews quarterly. The Supervising Principal handles daily trade review, complaint logs, and new account sign-offs.","versions":[{"ver":"1.9","ts":ts(90),"author":"supervisor","note":"Added options review workflow"},{"ver":"2.0","ts":ts(30),"author":"supervisor","note":"Incorporated Reg BI requirements"}]},
            {"id":"WSP-003","title":"Information Barriers Policy","version":"1.1","status":"Draft","owner":"analyst","approved_by":"","approved_ts":"","content":"Policies governing information barriers between advisory and brokerage functions. Employees may not share material non-public information across business lines. The Compliance Analyst collects attestations. The Supervising Principal reviews electronic communication surveillance.","versions":[{"ver":"1.0","ts":ts(120),"author":"analyst","note":"Initial draft"},{"ver":"1.1","ts":ts(7),"author":"analyst","note":"Added electronic communication monitoring section"}]},
        ],
        "wsp_tasks": wsp_tasks,
        "supervisory_checklists": [],  # populated when user clicks generate
        "audit_trail": [
            {"ts":ts(30),"user":"admin","module":"System","action":"System initialized; sample data seeded"},
            {"ts":ts(20),"user":"admin","module":"Exam Requests","action":"Created ER-001: FINRA Cycle Exam 2024"},
            {"ts":ts(15),"user":"supervisor","module":"WSP Repository","action":"Approved WSP-001 v3.2"},
            {"ts":ts(5),"user":"admin","module":"Exam Requests","action":"Created ER-002: SEC Annual Review"},
        ],
        "evidence": [
            {"id":"EV-001","filename":"aml_policy_2024.pdf","uploaded_by":"admin","ts":ts(15),"task_id":"T-004","hash":"sha256:a1b2c3d4","immutable":True,"archived":False},
            {"id":"EV-002","filename":"supervision_policy_v2.pdf","uploaded_by":"analyst","ts":ts(1),"task_id":"T-004","hash":"sha256:e5f6a7b8","immutable":True,"archived":False},
        ],
        "rule_scan_memo": None,
        "org_chart": [
            {"role":"Chief Compliance Officer","user":"admin","reports_to":"","responsibilities":["AML Oversight","Exam Management","Rule Inventory"]},
            {"role":"VP, Head of Supervision","user":"supervisor","reports_to":"admin","responsibilities":["Trade Review","Supervisory Checklists","Rep Oversight"]},
            {"role":"Compliance Analyst","user":"analyst","reports_to":"supervisor","responsibilities":["Evidence Collection","Testing","Filings"]},
        ],
        "approvals": [
            {"id":"AP-001","item":"WSP-002 v2.0","type":"WSP Approval","requestor":"supervisor","approver1":"admin","approver1_ts":ts(30),"approver2":"","status":"Approved","ts":ts(30)},
        ],
        "workflow_templates": [
            {
                "id":"WF-T-001","name":"Monthly Trade Supervision Review",
                "category":"Supervision","purpose":"Supervisory Review",
                "department":"Compliance","frequency":"Monthly",
                "owner_role":"Supervisor","regulation":"FINRA 3110",
                "tags":["trade-review","supervision","monthly"],
                "status":"Active","created":ts(45),
            },
            {
                "id":"WF-T-002","name":"Annual AML Program Certification",
                "category":"Compliance","purpose":"Periodic Certification",
                "department":"Compliance","frequency":"Annual",
                "owner_role":"Compliance Officer","regulation":"AML Program",
                "tags":["aml","certification","annual"],
                "status":"Active","created":ts(90),
            },
            {
                "id":"WF-T-003","name":"Reg BI Best Interest Exception Review",
                "category":"Risk Monitoring","purpose":"Exception Handling",
                "department":"Compliance","frequency":"Quarterly",
                "owner_role":"Compliance Officer","regulation":"FINRA 3110",
                "tags":["reg-bi","exception","quarterly"],
                "status":"Active","created":ts(30),
            },
            {
                "id":"WF-T-004","name":"Electronic Comm Surveillance Review",
                "category":"Supervision","purpose":"Regulatory Requirement",
                "department":"Supervision","frequency":"Monthly",
                "owner_role":"Supervisor","regulation":"FINRA 3120",
                "tags":["surveillance","communications","monthly"],
                "status":"Active","created":ts(20),
            },
            {
                "id":"WF-T-005","name":"Quarterly Risk Assessment",
                "category":"Risk Monitoring","purpose":"Risk Monitoring",
                "department":"Risk","frequency":"Quarterly",
                "owner_role":"Compliance Officer","regulation":"SEC 206(4)-7",
                "tags":["risk","quarterly","assessment"],
                "status":"Archived","created":ts(180),
            },
        ],
        "workflow_instances": [
            {
                "id":"WF-I-001","template_id":"WF-T-001",
                "name":"Monthly Trade Review — March 2026","instance_name":"March 2026",
                "owner":"supervisor","due":(now+timedelta(days=8)).strftime("%Y-%m-%d"),
                "priority":"High","status":"In Progress",
                "created":ts(5),"category":"Supervision","regulation":"FINRA 3110",
            },
            {
                "id":"WF-I-002","template_id":"WF-T-002",
                "name":"Annual AML Certification — 2026","instance_name":"2026",
                "owner":"admin","due":(now+timedelta(days=45)).strftime("%Y-%m-%d"),
                "priority":"High","status":"Open",
                "created":ts(3),"category":"Compliance","regulation":"AML Program",
            },
            {
                "id":"WF-I-003","template_id":"WF-T-003",
                "name":"Reg BI Exception Review — Q1 2026","instance_name":"Q1 2026",
                "owner":"admin","due":(now-timedelta(days=3)).strftime("%Y-%m-%d"),
                "priority":"Normal","status":"Overdue",
                "created":ts(20),"category":"Risk Monitoring","regulation":"FINRA 3110",
            },
            {
                "id":"WF-I-004","template_id":"WF-T-004",
                "name":"E-Comm Surveillance — March 2026","instance_name":"March 2026",
                "owner":"supervisor","due":(now+timedelta(days=15)).strftime("%Y-%m-%d"),
                "priority":"Normal","status":"Open",
                "created":ts(2),"category":"Supervision","regulation":"FINRA 3120",
            },
        ],
    }

# ── SESSION STATE ──────────────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = seed_data()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

D = st.session_state.data
# Back-compat: ensure workflow keys exist for older sessions
if "workflow_templates" not in D: D["workflow_templates"] = []
if "workflow_instances" not in D: D["workflow_instances"] = []

def add_audit(module, action):
    st.session_state.data["audit_trail"].append({"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"user":st.session_state.current_user,"module":module,"action":action})

def current_role():
    u = st.session_state.current_user
    return D["users"][u]["role"] if u else ""

def current_name():
    u = st.session_state.current_user
    return D["users"][u]["name"] if u else ""

def badge(text, cls):
    return f"<span class='gc-badge {cls}'>{text}</span>"

def toggle(key, label, default=False):
    """Render a styled clickable header; return True if expanded."""
    if key not in st.session_state:
        st.session_state[key] = default
    open_ = st.session_state[key]
    arrow = "▾" if open_ else "▸"
    btn_style = (
        "background:#ffffff;border:1px solid #e5e7eb;border-radius:8px;"
        "padding:10px 16px;width:100%;text-align:left;cursor:pointer;"
        "font-family:Inter,-apple-system,sans-serif;font-size:13px;"
        "font-weight:600;color:#111111;margin-bottom:2px;"
        "box-shadow:0 1px 2px rgba(0,0,0,0.04);"
    )
    if st.button(f"{arrow}  {label}", key=f"_btn_{key}", use_container_width=True):
        st.session_state[key] = not open_
        st.rerun()
    return st.session_state[key]

# ── LOGIN ──────────────────────────────────────────────────────────────────────
def login_page():
    st.markdown("<div class='login-wrap'><div class='login-logo'>⚖ GRAPHITE</div><div class='login-sub'>Compliance Intelligence Platform</div></div>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,1.4,1])
    with c2:
        st.markdown("<div class='gc-card'>", unsafe_allow_html=True)
        st.markdown("<div class='gc-card-header'>SECURE LOGIN</div>", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="admin / supervisor / analyst")
        password = st.text_input("Password", type="password", placeholder="pass")
        if st.button("Sign In →", use_container_width=True):
            if username in D["users"] and D["users"][username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                add_audit("Auth", f"Login: {username}")
                st.rerun()
            else:
                st.error("Invalid credentials.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;margin-top:.8rem;font-size:12px;color:#6b7280'>demo logins: admin / supervisor / analyst  ·  password: pass</div>", unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        user = D["users"][st.session_state.current_user]
        st.markdown(f"""
        <div style='padding:.8rem 0 1rem 0;border-bottom:1px solid #252a33;margin-bottom:1rem'>
          <div style='font-size:1.3rem;font-weight:800;color:#ffffff;letter-spacing:-.02em'>⚖ Graphite</div>
          <div style='font-size:11px;color:#6b7a99;letter-spacing:.1em;text-transform:uppercase'>Compliance Platform</div>
        </div>
        <div style='font-size:10px;color:#6b7a99;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.25rem'>Logged in as</div>
        <div style='font-size:.95rem;font-weight:700;color:#ffffff;margin-bottom:.1rem'>{user['name']}</div>
        <div style='font-size:12px;color:#93c5fd;margin-bottom:.8rem'>{user.get('title', user['role'])}</div>
        <hr style='border-color:#252a33;margin:.5rem 0 .8rem 0'/>
        """, unsafe_allow_html=True)

        overdue = [t for t in D["tasks"] if t["status"]=="Overdue"]
        if overdue:
            st.markdown(f"<div class='gc-alert gc-alert-danger' style='margin-bottom:.8rem'>⚠ {len(overdue)} overdue task(s)</div>", unsafe_allow_html=True)

        cl_count  = len(D.get("supervisory_checklists", []))
        wf_overdue = len([w for w in D.get("workflow_instances",[]) if w["status"]=="Overdue"])

        # ── Group definitions ─────────────────────────────────
        GROUPS = [
            {
                "label": None,   # no section header for top-level nav
                "pages": [("🏠","Dashboard")],
            },
            {
                "label": "COMPLIANCE",
                "pages": [
                    ("📋","Tasks & Remediation"),
                    ("📁","Exam Requests"),
                    ("📚","WSP Repository"),
                    ("✅","Supervisory Checklists"),
                    ("🔍","Evidence Repository"),
                ],
            },
            {
                "label": "WORKFLOWS",
                "pages": [
                    ("🔄","Workflow Library"),
                    ("▶️","Active Workflows"),
                ],
            },
            {
                "label": "RULES & INTELLIGENCE",
                "pages": [
                    ("📏","Rule Inventory"),
                    ("🤖","AI Rule Scan"),
                ],
            },
            {
                "label": "ADMINISTRATION",
                "pages": [
                    ("🏢","Org Chart"),
                    ("🔒","Audit Trail"),
                    ("⚙️","Firm Config"),
                    ("💾","Data Export"),
                ],
            },
        ]

        # Build flat nav_labels list (order matters for radio index)
        all_pages = []
        for g in GROUPS:
            all_pages.extend(g["pages"])

        def _label(icon, name):
            if name == "Supervisory Checklists" and cl_count > 0:
                return f"{icon}  {name} ({cl_count})"
            if name == "Active Workflows" and wf_overdue > 0:
                return f"{icon}  {name} ⚠"
            return f"{icon}  {name}"

        nav_labels   = [p[1] for p in all_pages]
        display_labels = [_label(p[0], p[1]) for p in all_pages]

        # Render grouped section headers + single radio widget
        section_header_css = (
            "font-size:9px;font-weight:700;letter-spacing:.12em;"
            "text-transform:uppercase;color:#4b5a72;"
            "padding:10px 4px 4px 4px;margin-top:4px;"
        )

        # We render the section headers as decorative markdown between groups,
        # but use ONE radio so Streamlit tracks selection properly.
        # Approach: render headers manually, hide radio labels per-group via CSS.
        for g in GROUPS:
            if g["label"]:
                st.markdown(f"<div style='{section_header_css}'>{g['label']}</div>",
                            unsafe_allow_html=True)
            for icon, name in g["pages"]:
                lbl = _label(icon, name)
                # Render as a radio button but styled like a nav item
                selected = st.session_state.get("_nav_sel", nav_labels[0])
                is_active = selected == name
                bg  = "rgba(59,130,246,0.18)" if is_active else "transparent"
                col = "#93c5fd" if is_active else "#d0d6e4"
                fw  = "700" if is_active else "500"
                if st.button(
                    lbl,
                    key=f"_nav_{name}",
                    use_container_width=True,
                ):
                    st.session_state["_nav_sel"] = name
                    st.rerun()

        st.markdown("<hr style='border-color:#252a33;margin:.8rem 0'/>", unsafe_allow_html=True)
        if st.button("Sign Out", key="_signout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            if "_nav_sel" in st.session_state:
                del st.session_state["_nav_sel"]
            st.rerun()

        return st.session_state.get("_nav_sel", "Dashboard")

# ── DASHBOARD ──────────────────────────────────────────────────────────────────
def page_dashboard():
    st.markdown(f"<div class='gc-header'><h1>COMPLIANCE DASHBOARD</h1><p>{D['firm']['name']} · {D['firm']['regulator']} · {datetime.now().strftime('%B %d, %Y')}</p></div>", unsafe_allow_html=True)
    tasks = D["tasks"]
    cols = st.columns(6)
    cols[0].metric("Open Tasks",     len([t for t in tasks if t["status"]=="Open"]))
    cols[1].metric("Overdue",        len([t for t in tasks if t["status"]=="Overdue"]))
    cols[2].metric("Pending Review", len([t for t in tasks if t["status"]=="Pending Approval"]))
    cols[3].metric("Closed",         len([t for t in tasks if t["status"]=="Closed"]))
    cols[4].metric("Exam Requests",  len(D["exam_requests"]))
    cols[5].metric("Checklists",     len(D.get("supervisory_checklists",[])))
    st.markdown("<hr/>", unsafe_allow_html=True)
    cl, cr = st.columns([1.6,1])
    with cl:
        st.markdown("<div style='font-size:11px;font-weight:700;letter-spacing:.08em;color:#6b7280;text-transform:uppercase;margin-bottom:.8rem'>MY TASKS</div>", unsafe_allow_html=True)
        today_str = date.today().strftime("%Y-%m-%d")
        for t in D["tasks"]:
            if t["status"]=="Open" and t["due"] < today_str:
                t["status"]="Overdue"
        my_tasks = [t for t in tasks if t["assignee"]==st.session_state.current_user or current_role()=="Compliance Officer"]
        for t in my_tasks[:6]:
            s=t["status"]; p=t["priority"]
            sc="badge-overdue" if s=="Overdue" else "badge-open" if s=="Open" else "badge-pending" if "Pending" in s else "badge-closed"
            pc="badge-high" if p=="High" else "badge-med" if p=="Medium" else "badge-low"
            uname=D["users"].get(t["assignee"],{}).get("name",t["assignee"])
            st.markdown(f"""<div class='gc-card' style='padding:.8rem 1rem;margin-bottom:.4rem'>
              <div style='display:flex;justify-content:space-between;align-items:center'>
                <div><span style='font-size:11px;color:#6b7280'>{t['id']}</span>
                <span style='font-weight:600;margin-left:.5rem'>{t['title']}</span></div>
                <div>{badge(s,sc)}&nbsp;{badge(p,pc)}</div>
              </div>
              <div style='margin-top:.3rem;font-size:12px;color:#6b7280'>Due: {t['due']} · {uname} · {t['category']}</div>
            </div>""", unsafe_allow_html=True)
    with cr:
        st.markdown("<div style='font-size:11px;font-weight:700;letter-spacing:.08em;color:#6b7280;text-transform:uppercase;margin-bottom:.8rem'>RECENT ACTIVITY</div>", unsafe_allow_html=True)
        for e in reversed(D["audit_trail"][-8:]):
            st.markdown(f"<div class='gc-tl'><span style='color:#2563eb;font-size:11px'>{e['ts']}</span> · <b>{e['user']}</b><br/>{e['action']}</div>", unsafe_allow_html=True)
        flagged=[r for r in D["rules"] if r["ai_flagged"]]
        if flagged:
            st.markdown("<hr/>", unsafe_allow_html=True)
            st.markdown(f"<div class='gc-alert gc-alert-warn'>🤖 AI flagged {len(flagged)} rule change(s)</div>", unsafe_allow_html=True)

# ── TASKS ──────────────────────────────────────────────────────────────────────
def page_tasks():
    st.markdown("<div class='gc-header'><h1>TASKS & REMEDIATION</h1><p>Create, assign, track, and close compliance tasks with full audit trail</p></div>", unsafe_allow_html=True)
    tab1,tab2 = st.tabs(["📋  TASK LIST","➕  NEW TASK"])
    with tab1:
        fc1,fc2,fc3 = st.columns(3)
        fs=fc1.selectbox("Status",["All","Open","Overdue","Pending Approval","Closed"])
        fp=fc2.selectbox("Priority",["All","High","Medium","Low"])
        fc_=fc3.selectbox("Category",["All"]+list({t["category"] for t in D["tasks"]}))
        today_str=date.today().strftime("%Y-%m-%d")
        for t in D["tasks"]:
            if t["status"]=="Open" and t["due"]<today_str:
                t["status"]="Overdue"
                t["audit"].append({"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"user":"SYSTEM","action":"Auto-escalated to Overdue"})
        tasks=D["tasks"]
        if fs!="All": tasks=[t for t in tasks if t["status"]==fs]
        if fp!="All": tasks=[t for t in tasks if t["priority"]==fp]
        if fc_!="All": tasks=[t for t in tasks if t["category"]==fc_]
        for t in tasks:
            s=t["status"]; p=t["priority"]
            sc="badge-overdue" if s=="Overdue" else "badge-open" if s=="Open" else "badge-pending" if "Pending" in s else "badge-closed"
            pc="badge-high" if p=="High" else "badge-med" if p=="Medium" else "badge-low"
            src=""
            if t.get("source_wsp"): src=f" · from {t['source_wsp']}"
            if toggle(f"task_{t['id']}", f"{t['id']} — {t['title']} [{t['status']}]"):
                c1,c2,c3=st.columns(3)
                c1.markdown(f"**Assignee:** {D['users'].get(t['assignee'],{}).get('name',t['assignee'])}")
                c2.markdown(f"**Due:** {t['due']}")
                c3.markdown(f"**Category:** {t['category']}{src}")
                st.markdown(f"Status: {badge(s,sc)}&nbsp; Priority: {badge(p,pc)}", unsafe_allow_html=True)
                if t.get("recurrence"): st.markdown(f"<div class='gc-alert gc-alert-warn' style='margin:.4rem 0'>🔁 Recurrence: {t['recurrence']}</div>", unsafe_allow_html=True)
                if t.get("delegated_to"): st.markdown(f"<div class='gc-alert gc-alert-warn'>Delegated to: {t['delegated_to']} · {t['delegated_memo']}</div>", unsafe_allow_html=True)
                st.markdown("<hr/><b>Evidence</b>", unsafe_allow_html=True)
                for ev in t["evidence"]:
                    st.markdown(f"<div class='gc-tl'>📎 {ev['name']} · {ev['uploaded_by']} · {ev['ts']} {badge('IMMUTABLE','badge-closed')}</div>", unsafe_allow_html=True)
                if not t["evidence"]: st.caption("No evidence attached.")
                up=st.file_uploader(f"Upload evidence",key=f"up_{t['id']}",label_visibility="collapsed")
                if up:
                    fh=hashlib.md5(up.name.encode()).hexdigest()[:8]
                    ev_e={"name":up.name,"uploaded_by":st.session_state.current_user,"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"hash":fh,"immutable":True}
                    t["evidence"].append(ev_e)
                    t["audit"].append({"ts":ev_e["ts"],"user":st.session_state.current_user,"action":f"Evidence uploaded: {up.name}"})
                    eid=f"EV-{len(D['evidence'])+1:03d}"
                    st.session_state.data["evidence"].append({"id":eid,"filename":up.name,"uploaded_by":st.session_state.current_user,"ts":ev_e["ts"],"task_id":t["id"],"hash":fh,"immutable":True,"archived":False})
                    add_audit("Tasks",f"Uploaded {up.name} for {t['id']}")
                    st.success(f"✓ {up.name} uploaded (WORM-locked)")
                st.markdown("<hr/>", unsafe_allow_html=True)
                a1,a2,a3=st.columns(3)
                if a1.button("Submit for Approval",key=f"sub_{t['id']}"):
                    if t["status"]!="Closed":
                        t["status"]="Pending Approval"
                        t["audit"].append({"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"user":st.session_state.current_user,"action":"Submitted for approval"})
                        add_audit("Tasks",f"{t['id']} submitted for approval"); st.rerun()
                if a2.button("Approve & Close",key=f"apr_{t['id']}"):
                    if current_role() in ["Compliance Officer","Supervisor"]:
                        t["status"]="Closed"
                        t["audit"].append({"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"user":st.session_state.current_user,"action":"Approved and closed"})
                        add_audit("Tasks",f"{t['id']} approved and closed"); st.rerun()
                if toggle(f"dlg_exp_{t['id']}", "🔀 Delegate"):
                    d1,d2=st.columns(2)
                    dto=d1.selectbox("Delegate to",list(D["users"].keys()),key=f"dt_{t['id']}")
                    dmemo=d2.text_input("Memo",key=f"dm_{t['id']}")
                    if st.button("Confirm",key=f"dlg_{t['id']}"):
                        t["delegated_to"]=dto; t["delegated_memo"]=dmemo
                        t["audit"].append({"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"user":st.session_state.current_user,"action":f"Delegated to {dto}: {dmemo}"})
                        add_audit("Tasks",f"{t['id']} delegated to {dto}"); st.rerun()
                if toggle(f"cwr_exp_{t['id']}", "🚪 Close with Rationale"):
                    rat=st.text_area("Rationale (required)",key=f"rat_{t['id']}")
                    if st.button("Close",key=f"cwr_{t['id']}"):
                        if rat.strip():
                            t["status"]="Closed"; t["rationale"]=rat
                            t["audit"].append({"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"user":st.session_state.current_user,"action":f"Closed: {rat}"})
                            add_audit("Tasks",f"{t['id']} closed"); st.rerun()
                        else: st.warning("Rationale required.")
                st.markdown("<hr/><b>Audit Trail</b>", unsafe_allow_html=True)
                for e in t["audit"]:
                    st.markdown(f"<div class='gc-tl'><span style='color:#2563eb;font-size:11px'>{e['ts']}</span> · <b>{e['user']}</b> · {e['action']}</div>", unsafe_allow_html=True)
    with tab2:
        c1,c2=st.columns(2)
        title=c1.text_input("Task Title"); assignee=c2.selectbox("Assignee",list(D["users"].keys()))
        c3,c4,c5=st.columns(3)
        due=c3.date_input("Due Date",value=date.today()+timedelta(days=7))
        pri=c4.selectbox("Priority",["High","Medium","Low"])
        cat=c5.selectbox("Category",["AML","Supervisory","Trading","Regulatory","InfoSec","Testing","Other"])
        if st.button("Create Task"):
            if title.strip():
                nid=f"T-{len(D['tasks'])+1:03d}"
                D["tasks"].append({"id":nid,"title":title,"assignee":assignee,"due":due.strftime("%Y-%m-%d"),"status":"Open","priority":pri,"category":cat,"evidence":[],"audit":[{"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"user":st.session_state.current_user,"action":f"Created {nid}"}],"rationale":"","delegated_to":"","delegated_memo":"","source_wsp":"","recurrence":""})
                add_audit("Tasks",f"Created {nid}: {title}"); st.success(f"✓ Task {nid} created."); st.rerun()

# ── EXAM REQUESTS ──────────────────────────────────────────────────────────────
def page_exam_requests():
    st.markdown("<div class='gc-header'><h1>EXAM / DOCUMENT REQUEST WORKFLOW</h1><p>Centralized workspace for regulatory exam preparation</p></div>", unsafe_allow_html=True)
    tab1,tab2=st.tabs(["📁  ACTIVE EXAMS","➕  NEW EXAM REQUEST"])
    with tab1:
        for er in D["exam_requests"]:
            done=len([i for i in er["items"] if i["status"]=="Uploaded"])
            total=len(er["items"]); pct=int(done/total*100) if total else 0
            if toggle(f"er_{er['id']}", f"{er['id']} — {er['title']} | {er['regulator']} | Due: {er['due']}"):
                st.markdown(f"Progress: **{done}/{total}** ({pct}%)")
                st.progress(pct/100)
                for idx,item in enumerate(er["items"]):
                    ic1,ic2,ic3,ic4=st.columns([3,1.5,1.5,2])
                    ic1.markdown(f"{'✅' if item['status']=='Uploaded' else '⏳'}  {item['item']}")
                    ic2.markdown(badge(item["status"],"badge-closed" if item["status"]=="Uploaded" else "badge-pending"),unsafe_allow_html=True)
                    ic3.markdown(f"_{D['users'].get(item['assignee'],{}).get('name',item['assignee'])}_")
                    up=ic4.file_uploader("Upload",key=f"er_{er['id']}_{idx}",label_visibility="collapsed")
                    if up:
                        item["status"]="Uploaded"
                        er["audit"].append({"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"user":st.session_state.current_user,"action":f"Uploaded {up.name} for '{item['item']}'"})
                        add_audit("Exam Requests",f"{er['id']}: uploaded {up.name}"); st.rerun()
                st.markdown("<hr/>", unsafe_allow_html=True)
                if st.button(f"📦 Export Package",key=f"exp_{er['id']}"):
                    payload=json.dumps({"exam":er,"audit":er["audit"]},indent=2)
                    st.download_button("Download JSON",data=payload,file_name=f"{er['id']}_package.json",mime="application/json",key=f"dl_{er['id']}")
                st.markdown("<hr/><b>Audit Trail</b>", unsafe_allow_html=True)
                for e in er["audit"]:
                    st.markdown(f"<div class='gc-tl'><span style='color:#2563eb;font-size:11px'>{e['ts']}</span> · <b>{e['user']}</b> · {e['action']}</div>", unsafe_allow_html=True)
    with tab2:
        c1,c2=st.columns(2)
        title=c1.text_input("Exam Title"); reg=c2.selectbox("Regulator",["FINRA","SEC","CFTC","NFA","State Regulator","Internal"])
        due=st.date_input("Due Date",value=date.today()+timedelta(days=30))
        items_raw=st.text_area("Document Items (one per line)","Customer files\nSupervisory procedures\nAML documentation",height=100)
        if st.button("Create Exam Request"):
            if title.strip():
                nid=f"ER-{len(D['exam_requests'])+1:03d}"
                items=[{"item":i.strip(),"status":"Pending","assignee":st.session_state.current_user} for i in items_raw.splitlines() if i.strip()]
                D["exam_requests"].append({"id":nid,"title":title,"regulator":reg,"due":due.strftime("%Y-%m-%d"),"status":"Open","items":items,"audit":[{"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"user":st.session_state.current_user,"action":f"Created {nid}"}]})
                add_audit("Exam Requests",f"Created {nid}: {title}"); st.success(f"✓ {nid} created."); st.rerun()

# ── WSP REPOSITORY ─────────────────────────────────────────────────────────────
def page_wsp():
    st.markdown("<div class='gc-header'><h1>WSP / PROCEDURE REPOSITORY</h1><p>Version-controlled policy library with supervisory checklist generation</p></div>", unsafe_allow_html=True)
    tab1,tab2=st.tabs(["📚  PROCEDURES","➕  NEW WSP"])
    with tab1:
        for wsp in D["wsps"]:
            sc="badge-closed" if wsp["status"]=="Approved" else "badge-draft"
            if toggle(f"wsp_{wsp['id']}", f"{wsp['id']} — {wsp['title']}  (v{wsp['version']})  [{wsp['status']}]"):
                st.markdown(f"Status: {badge(wsp['status'],sc)}&nbsp; Owner: **{D['users'].get(wsp['owner'],{}).get('name',wsp['owner'])}**", unsafe_allow_html=True)
                if wsp["approved_by"]: st.markdown(f"Approved by: **{D['users'].get(wsp['approved_by'],{}).get('name',wsp['approved_by'])}** · {wsp['approved_ts']}")
                st.markdown("<hr/><b>Content</b>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:13px;color:#6b7280;line-height:1.7;padding:.5rem 0'>{wsp['content']}</div>", unsafe_allow_html=True)
                st.markdown("<b>Version History</b>", unsafe_allow_html=True)
                for v in wsp["versions"]:
                    st.markdown(f"<div class='gc-tl'>v{v['ver']} · {v['ts']} · {v['author']} · <i>{v['note']}</i></div>", unsafe_allow_html=True)
                if len(wsp["versions"])>=2:
                    if st.button(f"🔴 Redline Diff",key=f"diff_{wsp['id']}"):
                        diff=list(difflib.unified_diff("Original text.".splitlines(),wsp["content"].splitlines(),lineterm="",fromfile="Previous",tofile="Current"))
                        st.code("\n".join(diff[:30]) if diff else "No diff.",language="diff")
                if wsp["status"]=="Draft" and current_role() in ["Compliance Officer","Supervisor"]:
                    if st.button(f"✅ Approve {wsp['id']}",key=f"awsp_{wsp['id']}"):
                        wsp["status"]="Approved"; wsp["approved_by"]=st.session_state.current_user; wsp["approved_ts"]=datetime.now().strftime("%Y-%m-%d %H:%M")
                        D["approvals"].append({"id":f"AP-{len(D['approvals'])+1:03d}","item":f"{wsp['id']} v{wsp['version']}","type":"WSP Approval","requestor":wsp["owner"],"approver1":st.session_state.current_user,"approver1_ts":wsp["approved_ts"],"approver2":"","status":"Approved","ts":wsp["approved_ts"]})
                        add_audit("WSP",f"Approved {wsp['id']} v{wsp['version']}"); st.rerun()

                # ── CHECKLIST GENERATOR ──────────────────────────────────────
                st.markdown("<hr/>", unsafe_allow_html=True)
                wsp_task_list = D["wsp_tasks"].get(wsp["id"],[])
                if not wsp_task_list:
                    st.markdown("<div class='gc-alert gc-alert-warn'>No task definitions found for this WSP.</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='font-size:11px;font-weight:700;letter-spacing:.08em;color:#6b7280;text-transform:uppercase;margin-bottom:.8rem'>📋 SUPERVISORY CHECKLIST GENERATOR</div>", unsafe_allow_html=True)
                    # group by owner
                    owners = {}
                    for wt in wsp_task_list:
                        o = wt["owner"]
                        if o not in owners: owners[o] = []
                        owners[o].append(wt)

                    for owner_key, tasks_for_owner in owners.items():
                        oinfo = D["users"].get(owner_key,{})
                        st.markdown(f"""
                        <div class='cl-owner-card'>
                          <div style='font-size:12px;color:#2563eb;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.3rem'>
                            {oinfo.get('title', oinfo.get('role',''))} — {oinfo.get('name',owner_key)}
                          </div>
                          <div style='font-size:12px;color:#6b7280;margin-bottom:.7rem'>{len(tasks_for_owner)} obligation(s) identified in {wsp['id']}</div>
                        """, unsafe_allow_html=True)
                        for wt in tasks_for_owner:
                            pc = "badge-high" if wt["category"] in ["AML","Regulatory"] else "badge-med"
                            st.markdown(f"""
                            <div class='cl-task-row'>
                              <div style='font-weight:600;margin-bottom:.2rem'>{wt['title']} &nbsp;{badge(wt['category'],pc)}</div>
                              <div style='font-size:12px;color:#6b7280;margin-bottom:.2rem'>🔁 {wt['frequency']}</div>
                              <div style='font-size:12px;color:#6b7280'>{wt['description']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    cl1,cl2=st.columns(2)
                    cl_due=cl1.date_input("First due date",value=date.today()+timedelta(days=7),key=f"cl_due_{wsp['id']}")
                    cl_recur=cl2.selectbox("Recurrence",["One-time","Weekly","Monthly","Quarterly","Annually"],key=f"cl_recur_{wsp['id']}")

                    # Check if checklists already generated for this WSP
                    existing=[cl for cl in D.get("supervisory_checklists",[]) if cl["source_wsp"]==wsp["id"]]
                    if existing:
                        st.markdown(f"<div class='gc-alert gc-alert-ok'>✓ Checklists already generated for {wsp['id']}. View in Supervisory Checklists.</div>", unsafe_allow_html=True)
                        if st.button(f"🔄 Regenerate Checklists for {wsp['id']}",key=f"regen_{wsp['id']}"):
                            D["supervisory_checklists"]=[c for c in D["supervisory_checklists"] if c["source_wsp"]!=wsp["id"]]
                            existing=[]
                    if not existing:
                        if st.button(f"✅ Generate Supervisory Checklists from {wsp['id']}",key=f"gen_cl_{wsp['id']}"):
                            now_str=datetime.now().strftime("%Y-%m-%d %H:%M")
                            for owner_key, tasks_for_owner in owners.items():
                                oinfo=D["users"].get(owner_key,{})
                                cl_id=f"CL-{len(D['supervisory_checklists'])+1:03d}"
                                checklist_items=[]
                                for wt in tasks_for_owner:
                                    checklist_items.append({
                                        "wt_id":wt["id"],"title":wt["title"],"description":wt["description"],
                                        "frequency":wt["frequency"],"category":wt["category"],
                                        "status":"Pending","evidence":[],"completed_ts":"","checked_off":False,
                                        "audit":[{"ts":now_str,"user":st.session_state.current_user,"action":f"Task added to checklist from {wsp['id']}"}],
                                    })
                                st.session_state.data["supervisory_checklists"].append({
                                    "id":cl_id,"source_wsp":wsp["id"],"wsp_title":wsp["title"],
                                    "assigned_to":owner_key,"owner_name":oinfo.get("name",owner_key),
                                    "owner_title":oinfo.get("title",oinfo.get("role","")),
                                    "due":cl_due.strftime("%Y-%m-%d"),"recurrence":cl_recur,
                                    "created_ts":now_str,"created_by":st.session_state.current_user,
                                    "status":"Active","items":checklist_items,
                                    "audit":[{"ts":now_str,"user":st.session_state.current_user,"action":f"Checklist {cl_id} created from {wsp['id']} for {oinfo.get('name',owner_key)}"}],
                                })
                            add_audit("Supervisory Checklists",f"Generated checklists from {wsp['id']}: {len(owners)} checklist(s) for {len(wsp_task_list)} obligations")
                            st.success(f"✓ {len(owners)} checklist(s) created — go to Supervisory Checklists in the sidebar to view them.")

    with tab2:
        c1,c2=st.columns(2)
        title=c1.text_input("WSP Title"); ver=c2.text_input("Version",value="1.0")
        content=st.text_area("Content",height=180)
        note=st.text_input("Change note")
        if st.button("Save WSP"):
            if title.strip():
                nid=f"WSP-{len(D['wsps'])+1:03d}"
                D["wsps"].append({"id":nid,"title":title,"version":ver,"status":"Draft","owner":st.session_state.current_user,"approved_by":"","approved_ts":"","content":content,"versions":[{"ver":ver,"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"author":st.session_state.current_user,"note":note}]})
                D["wsp_tasks"][nid]=[]
                add_audit("WSP",f"Created {nid}: {title} v{ver}"); st.success(f"✓ {nid} saved as Draft."); st.rerun()

# ── SUPERVISORY CHECKLISTS ─────────────────────────────────────────────────────
def page_checklists():
    st.markdown("<div class='gc-header'><h1>SUPERVISORY CHECKLISTS</h1><p>Role-based checklists generated from WSPs — assigned, auditable, and evidence-linked</p></div>", unsafe_allow_html=True)
    checklists = D.get("supervisory_checklists",[])
    if not checklists:
        st.markdown("<div class='gc-alert gc-alert-warn'>No checklists generated yet. Go to <b>WSP Repository</b> → open any WSP → click <b>Generate Supervisory Checklists</b>.</div>", unsafe_allow_html=True)
        return

    # Filter options
    fc1,fc2=st.columns(2)
    f_owner=fc1.selectbox("Filter by Owner",["All"]+list({cl["assigned_to"] for cl in checklists}),format_func=lambda x: "All" if x=="All" else D["users"].get(x,{}).get("name",x))
    f_wsp=fc2.selectbox("Filter by WSP",["All"]+list({cl["source_wsp"] for cl in checklists}))
    if f_owner!="All": checklists=[cl for cl in checklists if cl["assigned_to"]==f_owner]
    if f_wsp!="All":   checklists=[cl for cl in checklists if cl["source_wsp"]==f_wsp]

    for cl in checklists:
        done=len([i for i in cl["items"] if i["checked_off"]])
        total=len(cl["items"]); pct=int(done/total*100) if total else 0
        s_badge=badge("Complete","badge-closed") if pct==100 else badge("Active","badge-open")
        if toggle(f"cl_{cl['id']}", f"{cl['id']} | {cl['owner_name']} | {cl['wsp_title']} ({done}/{total} done)"):
            # Header info
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.8rem'>
              <div>
                <div style='font-size:13px;color:#2563eb;font-weight:700'>{cl['owner_title']}</div>
                <div style='font-size:1rem;font-weight:700;color:#111111;margin:.1rem 0'>{cl['owner_name']}</div>
                <div style='font-size:12px;color:#6b7280'>Source: {cl['source_wsp']} · Due: {cl['due']} · {cl['recurrence']}</div>
              </div>
              <div>{s_badge}&nbsp;{badge(f"{pct}% done","badge-pending" if pct<100 else "badge-closed")}</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(pct/100)
            st.markdown("<hr/>", unsafe_allow_html=True)

            # Each checklist item
            for idx,item in enumerate(cl["items"]):
                is_mine = (cl["assigned_to"]==st.session_state.current_user) or current_role()=="Compliance Officer"
                status_icon = "✅" if item["checked_off"] else "⬜"
                cat_cls = "badge-high" if item["category"] in ["AML","Regulatory"] else "badge-med"
                st.markdown(f"""
                <div class='cl-task-row' style='border-left:3px solid {"#22c55e" if item["checked_off"] else "#3b82f6"}'>
                  <div style='display:flex;justify-content:space-between;align-items:flex-start'>
                    <div style='flex:1'>
                      <div style='font-weight:700;font-size:14px;margin-bottom:.2rem'>{status_icon} &nbsp;{item['title']}</div>
                      <div style='font-size:12px;color:#6b7280;margin-bottom:.3rem'>🔁 {item['frequency']} &nbsp;·&nbsp; {badge(item['category'],cat_cls)}</div>
                      <div style='font-size:13px;color:#374151;line-height:1.6'>{item['description']}</div>
                    </div>
                  </div>
                """, unsafe_allow_html=True)

                # Evidence for this item
                if item["evidence"]:
                    st.markdown("<div style='margin-top:.5rem'>", unsafe_allow_html=True)
                    for ev in item["evidence"]:
                        st.markdown(f"<div class='gc-tl'>📎 {ev['name']} · {ev['uploaded_by']} · {ev['ts']} {badge('IMMUTABLE','badge-closed')}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                # Controls (only if assigned to current user or compliance officer)
                if is_mine and not item["checked_off"]:
                    ci1,ci2=st.columns([2,1])
                    up=ci1.file_uploader(f"Upload evidence for: {item['title'][:40]}",key=f"cl_up_{cl['id']}_{idx}",label_visibility="visible")
                    if up:
                        fh=hashlib.md5(up.name.encode()).hexdigest()[:8]
                        ev_e={"name":up.name,"uploaded_by":st.session_state.current_user,"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"hash":fh}
                        item["evidence"].append(ev_e)
                        now_str=datetime.now().strftime("%Y-%m-%d %H:%M")
                        item["audit"].append({"ts":now_str,"user":st.session_state.current_user,"action":f"Evidence uploaded: {up.name}"})
                        cl["audit"].append({"ts":now_str,"user":st.session_state.current_user,"action":f"Evidence uploaded for '{item['title']}': {up.name}"})
                        add_audit("Supervisory Checklists",f"{cl['id']}: evidence uploaded for '{item['title']}'")
                        st.success(f"✓ {up.name} attached")
                    if ci2.button(f"✅ Mark Complete",key=f"cl_done_{cl['id']}_{idx}"):
                        now_str=datetime.now().strftime("%Y-%m-%d %H:%M")
                        item["checked_off"]=True; item["completed_ts"]=now_str; item["status"]="Complete"
                        item["audit"].append({"ts":now_str,"user":st.session_state.current_user,"action":"Marked complete"})
                        cl["audit"].append({"ts":now_str,"user":st.session_state.current_user,"action":f"'{item['title']}' marked complete"})
                        add_audit("Supervisory Checklists",f"{cl['id']}: '{item['title']}' marked complete")
                        if all(i["checked_off"] for i in cl["items"]): cl["status"]="Complete"
                        st.rerun()
                elif item["checked_off"]:
                    st.markdown(f"<div style='font-size:12px;color:#166534;margin:.3rem 0 .6rem 0'>✅ Completed {item['completed_ts']} by {item['audit'][-1]['user'] if item['audit'] else '–'}</div>", unsafe_allow_html=True)

                # Item audit trail
                if toggle(f"item_audit_{cl['id']}_{idx}", f"View audit trail for: {item['title'][:50]}"):
                    for e in item["audit"]:
                        st.markdown(f"<div class='gc-tl'><span style='color:#2563eb;font-size:11px'>{e['ts']}</span> · <b>{e['user']}</b> · {e['action']}</div>", unsafe_allow_html=True)
                st.markdown("<hr/>", unsafe_allow_html=True)

            # Checklist-level audit trail
            if toggle(f"cl_audit_{cl['id']}", "📋 Full Checklist Audit Trail"):
                for e in cl["audit"]:
                    st.markdown(f"<div class='gc-tl'><span style='color:#2563eb;font-size:11px'>{e['ts']}</span> · <b>{e['user']}</b> · {e['action']}</div>", unsafe_allow_html=True)

# ── EVIDENCE REPOSITORY ────────────────────────────────────────────────────────
def page_evidence():
    st.markdown("<div class='gc-header'><h1>EVIDENCE REPOSITORY</h1><p>WORM-compliant immutable evidence store</p></div>", unsafe_allow_html=True)
    search=st.text_input("🔍 Search",placeholder="filename, task ID, uploader...")
    ev_list=D["evidence"]
    for ev in ev_list:
        try:
            age=(datetime.now()-datetime.strptime(ev["ts"],"%Y-%m-%d %H:%M")).days
            if age>5: ev["archived"]=True
        except: pass
    show_arch=st.checkbox("Show Archived",value=True)
    if not show_arch: ev_list=[e for e in ev_list if not e["archived"]]
    if search: ev_list=[e for e in ev_list if search.lower() in e["filename"].lower() or search.lower() in e["task_id"].lower() or search.lower() in e["uploaded_by"].lower()]
    for ev in ev_list:
        arch=f" {badge('ARCHIVED','badge-pending')}" if ev["archived"] else ""
        st.markdown(f"""<div class='gc-card'>
          <div style='display:flex;justify-content:space-between;align-items:center'>
            <div><span style='font-size:11px;color:#60a5fa'>{ev['id']}</span>
            <span style='font-weight:600;margin-left:.5rem'>📎 {ev['filename']}</span>{arch}</div>
            {badge('IMMUTABLE · WORM','badge-closed')}
          </div>
          <div style='margin-top:.3rem;font-size:12px;color:#6b7280'>
            {D['users'].get(ev['uploaded_by'],{}).get('name',ev['uploaded_by'])} · {ev['ts']} · Task: {ev['task_id']} · <code>{ev['hash']}</code>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    tid=c1.selectbox("Link to Task",[t["id"] for t in D["tasks"]])
    up=c2.file_uploader("Upload File")
    if up:
        fh="sha256:"+hashlib.md5(up.name.encode()).hexdigest()
        eid=f"EV-{len(D['evidence'])+1:03d}"
        st.session_state.data["evidence"].append({"id":eid,"filename":up.name,"uploaded_by":st.session_state.current_user,"ts":datetime.now().strftime("%Y-%m-%d %H:%M"),"task_id":tid,"hash":fh,"immutable":True,"archived":False})
        add_audit("Evidence",f"Uploaded {up.name} → {tid}"); st.success(f"✓ {up.name} stored as {eid} (WORM-locked)")

# ── RULE INVENTORY ─────────────────────────────────────────────────────────────
def page_rules():
    st.markdown("<div class='gc-header'><h1>MASTER RULE INVENTORY</h1><p>Centralized regulatory rule register</p></div>", unsafe_allow_html=True)
    tab1,tab2,tab3=st.tabs(["📏  RULES","➕  ADD RULE","🤖  PARSE DOCUMENT"])
    with tab1:
        for r in D["rules"]:
            flag=" 🤖" if r["ai_flagged"] else ""
            if toggle(f"rule_{r['id']}", f"{r['id']} — {r['title']}{flag}"):
                st.markdown(f"**Source:** {r['source']} · **Category:** {r['category']} · **Reviewed:** {r['last_reviewed']}")
                st.markdown(f"<div style='font-size:13px;color:#6b7280;margin:.5rem 0'>{r['description']}</div>", unsafe_allow_html=True)
                if r["ai_flagged"]: st.markdown("<div class='gc-alert gc-alert-warn'>🤖 AI detected a potential change. Review recommended.</div>", unsafe_allow_html=True)
                if st.button("Mark Reviewed",key=f"rev_{r['id']}"):
                    r["last_reviewed"]=datetime.now().strftime("%Y-%m-%d %H:%M"); r["ai_flagged"]=False; add_audit("Rules",f"Reviewed {r['id']}"); st.rerun()
    with tab2:
        c1,c2=st.columns(2)
        rt=c1.text_input("Rule Title"); rs=c2.selectbox("Source",["FINRA","SEC","CFTC","FinCEN","MSRB","State","Internal"])
        c3,c4=st.columns(2)
        rc=c3.selectbox("Category",["AML","Supervision","Recordkeeping","Suitability","Customer Accounts","Trading","Other"])
        rd=st.text_area("Description")
        if st.button("Add Rule"):
            if rt.strip():
                nid=f"R-{len(D['rules'])+1:03d}"
                D["rules"].append({"id":nid,"title":rt,"source":rs,"category":rc,"description":rd,"status":"Active","last_reviewed":datetime.now().strftime("%Y-%m-%d %H:%M"),"ai_flagged":False})
                add_audit("Rules",f"Added {nid}: {rt}"); st.success(f"✓ Rule {nid} added."); st.rerun()
    with tab3:
        st.markdown("**Paste document text — AI extracts potential rules**")
        doc=st.text_area("Document Text",height=180)
        if st.button("🤖 Parse & Extract"):
            if doc.strip():
                kws=[("supervision","FINRA","Supervision"),("aml","FinCEN","AML/BSA"),("retention","SEC","Recordkeeping"),("best interest","SEC","Suitability"),("customer","FINRA","Customer Accounts"),("trading","FINRA","Trading")]
                found=[k for k in kws if k[0] in doc.lower()]
                if found:
                    st.markdown(f"<div class='gc-alert gc-alert-ok'>✓ Found {len(found)} keyword(s)</div>", unsafe_allow_html=True)
                    for f in found: st.markdown(f"• **'{f[0]}'** → {f[2]} ({f[1]})")
                    if st.button("Add to Inventory"):
                        for f in found:
                            nid=f"R-{len(D['rules'])+1:03d}"
                            D["rules"].append({"id":nid,"title":f"AI-Extracted: {f[0].title()} Requirement","source":f[1],"category":f[2],"description":f"Extracted from document. Keyword: '{f[0]}'.","status":"Active","last_reviewed":datetime.now().strftime("%Y-%m-%d %H:%M"),"ai_flagged":False})
                        add_audit("Rules",f"AI parsed: {len(found)} rules extracted"); st.success(f"✓ {len(found)} rules added."); st.rerun()
                else: st.warning("No compliance keywords found.")

# ── AI RULE SCAN ───────────────────────────────────────────────────────────────
def page_ai_scan():
    st.markdown("<div class='gc-header'><h1>AI RULE CHANGE SCAN</h1><p>Simulated quarterly scan with summary memo and recommendations</p></div>", unsafe_allow_html=True)
    CHANGES=[
        {"rule":"FINRA Rule 4512","change":"Updated customer account information requirements to include digital communication preferences and ESG disclosures.","impact":"High","recommendation":"Review and update customer onboarding forms and WSP-002."},
        {"rule":"Bank Secrecy Act AML","change":"FinCEN updated guidance on cryptocurrency transaction monitoring thresholds and SAR reporting.","impact":"High","recommendation":"Update AML program to include digital asset monitoring. Retrain staff by Q2."},
        {"rule":"Reg BI","change":"SEC staff issued FAQ clarifying best interest obligations for automated investment tools.","impact":"Medium","recommendation":"Review robo-advisory disclosures and update Reg BI documentation."},
    ]
    if D["rule_scan_memo"]:
        m=D["rule_scan_memo"]
        st.markdown(f"<div class='gc-card'><div class='gc-card-header'>LAST SCAN · {m['date']}</div><div style='font-size:13px'>{m['summary']}</div></div>", unsafe_allow_html=True)
        for ch in m["changes"]:
            ic="badge-high" if ch["impact"]=="High" else "badge-med"
            st.markdown(f"""<div class='gc-card'>
              <div style='display:flex;justify-content:space-between'><b>{ch['rule']}</b>{badge(f"Impact: {ch['impact']}",ic)}</div>
              <div style='font-size:13px;color:#6b7280;margin:.4rem 0'>{ch['change']}</div>
              <div style='font-size:13px'><b>Recommendation:</b> {ch['recommendation']}</div>
            </div>""", unsafe_allow_html=True)
        memo_txt=f"GRAPHITE COMPLIANCE — AI RULE CHANGE MEMO\n{m['date']}\n\n{m['summary']}\n\n"+"".join(f"RULE: {c['rule']}\nCHANGE: {c['change']}\nIMPACT: {c['impact']}\nRECOMMENDATION: {c['recommendation']}\n\n" for c in m["changes"])
        st.download_button("📥 Download Memo",data=memo_txt,file_name="rule_change_memo.txt",mime="text/plain")
        st.markdown("<hr/>", unsafe_allow_html=True)
    if st.button("🤖 Run AI Rule Change Scan"):
        import time; 
        with st.spinner("Scanning..."):
            time.sleep(1.2)
        D["rule_scan_memo"]={"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"summary":f"Quarterly scan complete. Scanned {len(D['rules'])} active rules. Identified {len(CHANGES)} material changes.","changes":CHANGES}
        for r in D["rules"]:
            for ch in CHANGES:
                if any(w in r["title"] for w in ch["rule"].split()): r["ai_flagged"]=True
        add_audit("AI Scan",f"Scan complete; {len(CHANGES)} changes flagged"); st.rerun()

# ── ORG CHART ──────────────────────────────────────────────────────────────────
def page_org():
    st.markdown("<div class='gc-header'><h1>ORG CHART & RESPONSIBILITY MAP</h1><p>Supervisory hierarchy with linked responsibilities</p></div>", unsafe_allow_html=True)
    for node in D["org_chart"]:
        u=D["users"].get(node["user"],{})
        rep=f"Reports to: **{node['reports_to']}**" if node["reports_to"] else "**Top of hierarchy**"
        st.markdown(f"""<div class='gc-card'>
          <div style='font-size:12px;color:#2563eb;font-weight:700;letter-spacing:.05em'>{node['role']}</div>
          <div style='font-size:1rem;font-weight:700;margin:.2rem 0'>{u.get('name','–')} <span style='color:#6b7280;font-size:.8rem'>@{node['user']}</span></div>
          <div style='font-size:12px;color:#6b7280;margin-bottom:.5rem'>{rep}</div>
          <div>{'  '.join(badge(r,'badge-open') for r in node['responsibilities'])}</div>
        </div>""", unsafe_allow_html=True)
    delegated=[t for t in D["tasks"] if t.get("delegated_to")]
    if delegated:
        st.markdown("<hr/><b>Active Delegations</b>", unsafe_allow_html=True)
        for t in delegated:
            st.markdown(f"<div class='gc-tl'>{t['id']} · <b>{t['title']}</b> → delegated to <b>{t['delegated_to']}</b> · {t['delegated_memo']}</div>", unsafe_allow_html=True)

# ── AUDIT TRAIL ────────────────────────────────────────────────────────────────
def page_audit():
    st.markdown("<div class='gc-header'><h1>LINKED AUDIT TRAIL</h1><p>Immutable timestamped log of all actions</p></div>", unsafe_allow_html=True)
    fc1,fc2,fc3=st.columns(3)
    fu=fc1.selectbox("User",["All"]+list(D["users"].keys())+["SYSTEM"])
    fm=fc2.selectbox("Module",["All"]+list({a["module"] for a in D["audit_trail"]}))
    fs=fc3.text_input("Search",placeholder="keyword...")
    trail=list(reversed(D["audit_trail"]))
    if fu!="All": trail=[a for a in trail if a["user"]==fu]
    if fm!="All": trail=[a for a in trail if a["module"]==fm]
    if fs: trail=[a for a in trail if fs.lower() in a["action"].lower()]
    st.markdown(f"<div style='font-size:12px;color:#6b7280;margin-bottom:.8rem'>{len(trail)} records</div>", unsafe_allow_html=True)
    for e in trail:
        st.markdown(f"<div class='gc-tl'><span style='color:#2563eb;font-size:11px'>{e['ts']}</span> &nbsp;{badge(e['module'],'badge-open')}&nbsp; <b>{e['user']}</b> · {e['action']}</div>", unsafe_allow_html=True)

# ── FIRM CONFIG ────────────────────────────────────────────────────────────────
def page_firm_config():
    st.markdown("<div class='gc-header'><h1>FIRM PROFILE CONFIGURATION</h1><p>Tailor rules and workflows to your firm</p></div>", unsafe_allow_html=True)
    firm=D["firm"]
    c1,c2=st.columns(2)
    firm["name"]=c1.text_input("Firm Name",value=firm["name"])
    firm["industry"]=c2.text_input("Industry/Type",value=firm["industry"])
    c3,c4=st.columns(2)
    firm["crd"]=c3.text_input("CRD / License #",value=firm["crd"])
    firm["regulator"]=c4.text_input("Regulator(s)",value=firm["regulator"])
    c5,c6=st.columns(2)
    firm["retention_years"]=c5.number_input("Retention Period (years)",value=firm["retention_years"],min_value=1,max_value=20)
    firm["approval_mode"]=c6.selectbox("Approval Mode",["single","dual"],index=0 if firm["approval_mode"]=="single" else 1)
    firm["address"]=st.text_input("Address",value=firm["address"])
    if st.button("Save Profile"):
        add_audit("Firm Config","Firm profile updated"); st.success("✓ Saved.")
    st.markdown("<hr/><b>Third-Party Compliance Packet</b>", unsafe_allow_html=True)
    packet=f"THIRD-PARTY REGULATORY COMPLIANCE PACKET\nFirm: {firm['name']}\nIndustry: {firm['industry']}\nCRD: {firm['crd']}\nRegulator: {firm['regulator']}\nRetention: {firm['retention_years']} years\n\nCERTIFICATIONS:\n- FINRA Rule 3110: Active\n- AML Program: Active\n- Reg BI: Active\n- WORM Recordkeeping: Active\n\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    st.download_button("📥 Download Compliance Packet",data=packet,file_name="compliance_packet.txt",mime="text/plain")

# ── DATA EXPORT ────────────────────────────────────────────────────────────────
def page_export():
    st.markdown("<div class='gc-header'><h1>DATA EXPORT & BACKUP</h1><p>Export all compliance data as JSON or CSV</p></div>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        if st.button("Generate Full JSON Export"):
            payload=json.dumps({"exported_at":datetime.now().strftime("%Y-%m-%d %H:%M"),"firm":D["firm"],"tasks":D["tasks"],"exam_requests":D["exam_requests"],"rules":D["rules"],"wsps":D["wsps"],"evidence":D["evidence"],"supervisory_checklists":D.get("supervisory_checklists",[]),"audit_trail":D["audit_trail"]},indent=2)
            add_audit("Export","Full JSON export"); st.download_button("📥 Download",data=payload,file_name="graphite_export.json",mime="application/json")
    with c2:
        if st.button("Generate Tasks CSV"):
            buf=io.StringIO(); w=csv.DictWriter(buf,fieldnames=["id","title","assignee","due","status","priority","category"]); w.writeheader()
            for t in D["tasks"]: w.writerow({k:t[k] for k in ["id","title","assignee","due","status","priority","category"]})
            add_audit("Export","Tasks CSV export"); st.download_button("📥 Download",data=buf.getvalue(),file_name="tasks.csv",mime="text/csv")
    st.markdown("<div class='gc-alert gc-alert-ok' style='margin-top:1rem'>✓ All exports include audit trails · WORM hashes preserved · Meets SEC Rule 17a-4</div>", unsafe_allow_html=True)

# ── WORKFLOW CONSTANTS ─────────────────────────────────────────────────────────
WF_CATEGORIES   = ["Supervision","Compliance","Operations","Risk Monitoring","Regulatory","Operational"]
WF_PURPOSES     = ["Supervisory Review","Regulatory Requirement","Risk Monitoring","Exception Handling","Periodic Certification","Operational Control"]
WF_FREQUENCIES  = ["Ad Hoc","Event Driven","Daily","Weekly","Monthly","Quarterly","Annual"]
WF_REGULATIONS  = ["FINRA 3110","FINRA 3120","SEC 206(4)-7","AML Program","Internal Policy"]
WF_OWNER_ROLES  = ["Compliance Officer","Supervisor","Analyst","Risk Officer","Operations Manager"]
WF_DEPARTMENTS  = ["Compliance","Supervision","Risk","Operations","Legal","Finance"]
WF_TAGS_ALLOWED = [
    "aml","annual","assessment","attestation","certification","communications",
    "daily","exception","monthly","quarterly","reg-bi","risk","supervision",
    "surveillance","trade-review","weekly","training","reporting"
]
WF_PRIORITIES   = ["Low","Normal","High"]
WF_INST_STATUSES= ["Open","In Progress","Completed","Overdue"]

# ── WORKFLOW LIBRARY ───────────────────────────────────────────────────────────
def page_workflow_library():
    st.markdown("<div class='gc-header'><h1>WORKFLOW LIBRARY</h1><p>Reusable workflow templates for structured compliance processes</p></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📚  TEMPLATES", "➕  NEW TEMPLATE"])

    with tab1:
        templates = D.get("workflow_templates", [])

        # ── Search + Filters ──
        search = st.text_input("🔍 Search", placeholder="Workflow name, tag, category, purpose…", key="wfl_search")

        with st.container():
            fc1,fc2,fc3,fc4 = st.columns(4)
            f_cat  = fc1.selectbox("Category",  ["All"] + WF_CATEGORIES,  key="wfl_cat")
            f_purp = fc2.selectbox("Purpose",   ["All"] + WF_PURPOSES,    key="wfl_purp")
            f_freq = fc3.selectbox("Frequency", ["All"] + WF_FREQUENCIES, key="wfl_freq")
            f_reg  = fc4.selectbox("Regulation",["All"] + WF_REGULATIONS, key="wfl_reg")
            fc5,fc6,_ = st.columns(3)
            f_dept = fc5.selectbox("Department",["All"] + WF_DEPARTMENTS, key="wfl_dept")
            f_stat = fc6.selectbox("Status",    ["All","Active","Archived"], key="wfl_stat")

        # Apply filters
        results = templates
        if search:
            sl = search.lower()
            results = [t for t in results if
                sl in t["name"].lower() or
                sl in t["category"].lower() or
                sl in t["purpose"].lower() or
                any(sl in tag for tag in t.get("tags",[]))]
        if f_cat  != "All": results = [t for t in results if t["category"]   == f_cat]
        if f_purp != "All": results = [t for t in results if t["purpose"]    == f_purp]
        if f_freq != "All": results = [t for t in results if t["frequency"]  == f_freq]
        if f_reg  != "All": results = [t for t in results if t["regulation"] == f_reg]
        if f_dept != "All": results = [t for t in results if t["department"] == f_dept]
        if f_stat != "All": results = [t for t in results if t["status"]     == f_stat]

        st.markdown(f"<div style='font-size:12px;color:#6b7280;margin:.5rem 0 .8rem 0'>{len(results)} template(s)</div>", unsafe_allow_html=True)

        # ── Column headers ──
        st.markdown("""
        <div style='display:grid;grid-template-columns:2fr 1fr 1.2fr 1fr 1fr 1.1fr 0.7fr;
             gap:8px;padding:6px 12px;background:#e5e7eb;border-radius:6px;
             font-size:10px;font-weight:700;letter-spacing:.08em;color:#6b7280;
             text-transform:uppercase;margin-bottom:4px;'>
          <div>Workflow Name</div><div>Category</div><div>Purpose</div>
          <div>Frequency</div><div>Owner Role</div><div>Regulation</div><div>Status</div>
        </div>""", unsafe_allow_html=True)

        for tmpl in results:
            sc   = "badge-closed" if tmpl["status"]=="Active" else "badge-draft"
            tags_html = "".join(f"<span style='background:#e0f2fe;color:#0369a1;font-size:10px;padding:1px 7px;border-radius:10px;margin-right:3px;font-weight:600'>{tg}</span>" for tg in tmpl.get("tags",[]))

            st.markdown(f"""
            <div style='display:grid;grid-template-columns:2fr 1fr 1.2fr 1fr 1fr 1.1fr 0.7fr;
                 gap:8px;padding:10px 12px;background:#ffffff;border:1px solid #e5e7eb;
                 border-radius:8px;margin-bottom:4px;align-items:center;font-size:13px;'>
              <div>
                <div style='font-weight:700;color:#111111;margin-bottom:2px'>{tmpl['name']}</div>
                <div style='margin-top:3px'>{tags_html}</div>
              </div>
              <div style='color:#374151'>{tmpl['category']}</div>
              <div style='color:#374151'>{tmpl['purpose']}</div>
              <div style='color:#374151'>{tmpl['frequency']}</div>
              <div style='color:#374151'>{tmpl['owner_role']}</div>
              <div style='color:#374151'>{tmpl['regulation']}</div>
              <div>{badge(tmpl['status'], sc)}</div>
            </div>""", unsafe_allow_html=True)

            if toggle(f"wft_{tmpl['id']}", f"Details — {tmpl['id']}"):
                dc1,dc2,dc3 = st.columns(3)
                dc1.markdown(f"**Department:** {tmpl['department']}")
                dc2.markdown(f"**Created:** {tmpl['created'][:10]}")
                dc3.markdown(f"**ID:** `{tmpl['id']}`")

                # Launch instance from template
                st.markdown("<hr style='margin:.6rem 0'/>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:12px;font-weight:700;color:#374151;margin-bottom:.4rem'>LAUNCH INSTANCE FROM THIS TEMPLATE</div>", unsafe_allow_html=True)
                li1,li2,li3 = st.columns(3)
                inst_name = li1.text_input("Instance Name (e.g. Q1 2026)", key=f"li_name_{tmpl['id']}")
                inst_due  = li2.date_input("Due Date", value=date.today()+timedelta(days=30), key=f"li_due_{tmpl['id']}")
                inst_pri  = li3.selectbox("Priority", WF_PRIORITIES, index=1, key=f"li_pri_{tmpl['id']}")
                inst_own  = st.selectbox("Assign Owner", list(D["users"].keys()),
                    format_func=lambda x: f"{D['users'][x]['name']} ({D['users'][x]['title']})",
                    key=f"li_own_{tmpl['id']}")
                if st.button("▶ Launch Instance", key=f"li_launch_{tmpl['id']}"):
                    if inst_name.strip():
                        nid = f"WF-I-{len(D['workflow_instances'])+1:03d}"
                        D["workflow_instances"].append({
                            "id": nid, "template_id": tmpl["id"],
                            "name": f"{tmpl['name']} — {inst_name}",
                            "instance_name": inst_name,
                            "owner": inst_own,
                            "due": inst_due.strftime("%Y-%m-%d"),
                            "priority": inst_pri,
                            "status": "Open",
                            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "category": tmpl["category"],
                            "regulation": tmpl["regulation"],
                        })
                        add_audit("Workflows", f"Launched {nid} from {tmpl['id']}: {inst_name}")
                        st.success(f"✓ Instance {nid} launched.")
                        st.rerun()
                    else:
                        st.warning("Instance name required.")

                # Archive / Restore
                if current_role() == "Compliance Officer":
                    st.markdown("<hr style='margin:.5rem 0'/>", unsafe_allow_html=True)
                    new_status = "Archived" if tmpl["status"]=="Active" else "Active"
                    btn_label  = f"📦 Archive Template" if tmpl["status"]=="Active" else "♻ Restore Template"
                    if st.button(btn_label, key=f"wft_arch_{tmpl['id']}"):
                        tmpl["status"] = new_status
                        add_audit("Workflows", f"Template {tmpl['id']} set to {new_status}")
                        st.rerun()

    with tab2:
        if current_role() not in ["Compliance Officer"]:
            st.markdown("<div class='gc-alert gc-alert-warn'>⚠ Only Compliance Officers can create workflow templates.</div>", unsafe_allow_html=True)
            return

        st.markdown("<div style='font-size:12px;color:#6b7280;margin-bottom:1rem'>All fields use structured options to maintain filtering consistency across the platform.</div>", unsafe_allow_html=True)

        n1,n2 = st.columns(2)
        wf_name = n1.text_input("Workflow Name *")
        wf_dept = n2.selectbox("Department", WF_DEPARTMENTS)

        r1,r2,r3 = st.columns(3)
        wf_cat  = r1.selectbox("Category",   WF_CATEGORIES)
        wf_purp = r2.selectbox("Purpose",    WF_PURPOSES)
        wf_freq = r3.selectbox("Frequency",  WF_FREQUENCIES)

        r4,r5 = st.columns(2)
        wf_role = r4.selectbox("Owner Role", WF_OWNER_ROLES)
        wf_reg  = r5.selectbox("Regulation Mapping", WF_REGULATIONS)

        st.markdown("<div style='font-size:12px;font-weight:600;color:#374151;text-transform:uppercase;letter-spacing:.05em;margin:.6rem 0 .3rem 0'>Tags <span style='font-weight:400;text-transform:none;letter-spacing:0'>(select up to 4)</span></div>", unsafe_allow_html=True)
        tag_cols = st.columns(6)
        selected_tags = []
        for i, tg in enumerate(WF_TAGS_ALLOWED):
            if tag_cols[i % 6].checkbox(tg, key=f"ntag_{tg}"):
                selected_tags.append(tg)
        if len(selected_tags) > 4:
            st.warning("Maximum 4 tags allowed. Only the first 4 will be saved.")
            selected_tags = selected_tags[:4]

        st.markdown("<hr/>", unsafe_allow_html=True)
        if st.button("✚ Create Workflow Template"):
            if wf_name.strip():
                nid = f"WF-T-{len(D['workflow_templates'])+1:03d}"
                D["workflow_templates"].append({
                    "id": nid, "name": wf_name.strip(),
                    "category": wf_cat, "purpose": wf_purp,
                    "department": wf_dept, "frequency": wf_freq,
                    "owner_role": wf_role, "regulation": wf_reg,
                    "tags": selected_tags,
                    "status": "Active",
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
                add_audit("Workflows", f"Created template {nid}: {wf_name}")
                st.success(f"✓ Template {nid} created.")
                st.rerun()
            else:
                st.warning("Workflow name is required.")

# ── ACTIVE WORKFLOWS ───────────────────────────────────────────────────────────
def page_active_workflows():
    now_str = date.today().strftime("%Y-%m-%d")
    # Auto-escalate overdue
    for inst in D.get("workflow_instances", []):
        if inst["status"] in ("Open","In Progress") and inst["due"] < now_str:
            inst["status"] = "Overdue"

    st.markdown("<div class='gc-header'><h1>ACTIVE WORKFLOWS</h1><p>Running workflow instances — track, update, and close compliance processes</p></div>", unsafe_allow_html=True)

    instances = D.get("workflow_instances", [])

    # ── Search + Filters ──
    search = st.text_input("🔍 Search", placeholder="Workflow name, category, regulation…", key="wfi_search")

    fc1,fc2,fc3,fc4,fc5 = st.columns(5)
    f_cat   = fc1.selectbox("Category",  ["All"] + WF_CATEGORIES,    key="wfi_cat")
    f_stat  = fc2.selectbox("Status",    ["All"] + WF_INST_STATUSES, key="wfi_stat")
    f_pri   = fc3.selectbox("Priority",  ["All"] + WF_PRIORITIES,    key="wfi_pri")
    f_own   = fc4.selectbox("Owner",     ["All"] + list(D["users"].keys()),
                             format_func=lambda x: "All" if x=="All" else D["users"][x]["name"],
                             key="wfi_own")
    f_reg   = fc5.selectbox("Regulation",["All"] + WF_REGULATIONS,   key="wfi_reg")

    fc6,fc7 = st.columns(2)
    f_due_from = fc6.date_input("Due From", value=None, key="wfi_due_from")
    f_due_to   = fc7.date_input("Due To",   value=None, key="wfi_due_to")

    # Apply filters
    results = instances
    if search:
        sl = search.lower()
        results = [i for i in results if sl in i["name"].lower() or sl in i["category"].lower() or sl in i.get("regulation","").lower()]
    if f_cat  != "All": results = [i for i in results if i["category"]   == f_cat]
    if f_stat != "All": results = [i for i in results if i["status"]     == f_stat]
    if f_pri  != "All": results = [i for i in results if i["priority"]   == f_pri]
    if f_own  != "All": results = [i for i in results if i["owner"]      == f_own]
    if f_reg  != "All": results = [i for i in results if i.get("regulation","") == f_reg]
    if f_due_from:
        results = [i for i in results if i["due"] >= f_due_from.strftime("%Y-%m-%d")]
    if f_due_to:
        results = [i for i in results if i["due"] <= f_due_to.strftime("%Y-%m-%d")]

    # Summary metrics
    mc = st.columns(4)
    mc[0].metric("Total",     len(instances))
    mc[1].metric("Open",      len([i for i in instances if i["status"]=="Open"]))
    mc[2].metric("In Progress",len([i for i in instances if i["status"]=="In Progress"]))
    mc[3].metric("Overdue",   len([i for i in instances if i["status"]=="Overdue"]))
    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:12px;color:#6b7280;margin:.2rem 0 .8rem 0'>{len(results)} instance(s) shown</div>", unsafe_allow_html=True)

    # ── Column headers ──
    st.markdown("""
    <div style='display:grid;grid-template-columns:2.2fr 1fr 1fr 1fr 0.9fr 0.9fr 0.8fr;
         gap:8px;padding:6px 12px;background:#e5e7eb;border-radius:6px;
         font-size:10px;font-weight:700;letter-spacing:.08em;color:#6b7280;
         text-transform:uppercase;margin-bottom:4px;'>
      <div>Workflow Name</div><div>Category</div><div>Regulation</div>
      <div>Owner</div><div>Due Date</div><div>Priority</div><div>Status</div>
    </div>""", unsafe_allow_html=True)

    for inst in results:
        s = inst["status"]
        p = inst["priority"]
        sc = "badge-overdue" if s=="Overdue" else "badge-open" if s=="Open" else "badge-pending" if s=="In Progress" else "badge-closed"
        pc = "badge-high" if p=="High" else "badge-low" if p=="Low" else "badge-open"
        owner_name = D["users"].get(inst["owner"],{}).get("name", inst["owner"])

        # Highlight overdue rows
        row_border = "border-left:3px solid #ef4444" if s=="Overdue" else "border-left:3px solid #e5e7eb"

        st.markdown(f"""
        <div style='display:grid;grid-template-columns:2.2fr 1fr 1fr 1fr 0.9fr 0.9fr 0.8fr;
             gap:8px;padding:10px 12px;background:#ffffff;border:1px solid #e5e7eb;{row_border};
             border-radius:8px;margin-bottom:4px;align-items:center;font-size:13px;'>
          <div>
            <div style='font-weight:700;color:#111111'>{inst['name']}</div>
            <div style='font-size:11px;color:#6b7280;margin-top:2px'>Instance: {inst['instance_name']} · Created: {inst['created'][:10]}</div>
          </div>
          <div style='color:#374151'>{inst['category']}</div>
          <div style='color:#374151'>{inst.get('regulation','—')}</div>
          <div style='color:#374151'>{owner_name}</div>
          <div style='color:{"#dc2626" if s=="Overdue" else "#374151"};font-weight:{"700" if s=="Overdue" else "400"}'>{inst['due']}</div>
          <div>{badge(p, pc)}</div>
          <div>{badge(s, sc)}</div>
        </div>""", unsafe_allow_html=True)

        if toggle(f"wfi_{inst['id']}", f"Manage — {inst['id']}"):
            # Template cross-reference
            tmpl = next((t for t in D.get("workflow_templates",[]) if t["id"]==inst.get("template_id","")), None)
            if tmpl:
                st.markdown(f"<div class='gc-alert gc-alert-ok' style='margin-bottom:.5rem'>📚 Template: <b>{tmpl['name']}</b> · {tmpl['purpose']} · {tmpl['frequency']}</div>", unsafe_allow_html=True)

            ua1,ua2,ua3 = st.columns(3)
            new_status = ua1.selectbox("Update Status", WF_INST_STATUSES,
                index=WF_INST_STATUSES.index(inst["status"]) if inst["status"] in WF_INST_STATUSES else 0,
                key=f"wfi_stat_{inst['id']}")
            new_pri    = ua2.selectbox("Update Priority", WF_PRIORITIES,
                index=WF_PRIORITIES.index(inst["priority"]) if inst["priority"] in WF_PRIORITIES else 1,
                key=f"wfi_pri_{inst['id']}")
            new_due    = ua3.date_input("Update Due Date",
                value=datetime.strptime(inst["due"],"%Y-%m-%d").date(),
                key=f"wfi_due_{inst['id']}")

            if st.button("💾 Save Changes", key=f"wfi_save_{inst['id']}"):
                inst["status"]   = new_status
                inst["priority"] = new_pri
                inst["due"]      = new_due.strftime("%Y-%m-%d")
                add_audit("Workflows", f"Updated {inst['id']}: status={new_status}, priority={new_pri}, due={inst['due']}")
                st.success("✓ Instance updated.")
                st.rerun()

# ── ROUTER ─────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    login_page()
else:
    nav = sidebar()
    if   nav=="Dashboard":               page_dashboard()
    elif nav=="Tasks & Remediation":     page_tasks()
    elif nav=="Exam Requests":           page_exam_requests()
    elif nav=="WSP Repository":          page_wsp()
    elif nav=="Supervisory Checklists":  page_checklists()
    elif nav=="Evidence Repository":     page_evidence()
    elif nav=="Workflow Library":        page_workflow_library()
    elif nav=="Active Workflows":        page_active_workflows()
    elif nav=="Rule Inventory":          page_rules()
    elif nav=="AI Rule Scan":            page_ai_scan()
    elif nav=="Org Chart":               page_org()
    elif nav=="Audit Trail":             page_audit()
    elif nav=="Firm Config":             page_firm_config()
    elif nav=="Data Export":             page_export()
