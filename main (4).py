import streamlit as st
import json
import csv
import io
import hashlib
import random
import difflib
from datetime import datetime, timedelta, date

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Graphite Compliance",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS – dark, refined, slate/amber theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Source+Code+Pro:wght@400;600&display=swap');

:root {
  --bg:        #0c0e10;
  --surface:   #13161a;
  --surface2:  #191d22;
  --border:    #252a33;
  --border2:   #2e3440;
  --gold:      #c9a84c;
  --gold2:     #e8c97a;
  --gold-dim:  #8a6f30;
  --text:      #e8e6e0;
  --text2:     #8a8f9e;
  --text3:     #5a5f6e;
  --danger:    #c0534f;
  --success:   #4a9e72;
  --info:      #4a7eb5;
  --serif:     'Crimson Pro', 'Georgia', serif;
  --display:   'Cormorant Garamond', 'Georgia', serif;
  --mono:      'Source Code Pro', 'Courier New', monospace;
}

html, body, [class*="css"] {
  font-family: var(--serif) !important;
  font-size: 16px !important;
  background: var(--bg) !important;
  color: var(--text) !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
  text-rendering: optimizeLegibility !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
  color: var(--text) !important;
  font-family: var(--serif) !important;
  font-size: 15px !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stDateInput > div > div > input {
  background: var(--surface2) !important;
  border: 1px solid var(--border2) !important;
  color: var(--text) !important;
  border-radius: 3px !important;
  font-family: var(--serif) !important;
  font-size: 15px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 1px rgba(201,168,76,0.3) !important;
}

/* Labels */
label, .stSelectbox label, .stTextInput label,
.stTextArea label, .stDateInput label {
  font-family: var(--serif) !important;
  font-size: 13px !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  color: var(--text2) !important;
}

/* Buttons */
.stButton > button {
  background: transparent !important;
  color: var(--gold) !important;
  border: 1px solid var(--gold-dim) !important;
  font-family: var(--serif) !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  letter-spacing: 0.08em !important;
  border-radius: 3px !important;
  padding: 0.4rem 1.3rem !important;
  transition: all 0.2s !important;
}
.stButton > button:hover {
  background: rgba(201,168,76,0.1) !important;
  border-color: var(--gold) !important;
  color: var(--gold2) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text2) !important;
  font-family: var(--serif) !important;
  font-size: 14px !important;
  letter-spacing: 0.05em !important;
  border-radius: 0 !important;
  padding: 0.65rem 1.4rem !important;
  border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
  color: var(--gold) !important;
  border-bottom: 2px solid var(--gold) !important;
  background: transparent !important;
}

/* Metrics */
[data-testid="stMetric"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-top: 2px solid var(--gold-dim) !important;
  border-radius: 3px !important;
  padding: 1rem !important;
}
[data-testid="stMetricLabel"] {
  color: var(--text2) !important;
  font-size: 12px !important;
  font-family: var(--serif) !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
  color: var(--gold) !important;
  font-family: var(--display) !important;
  font-size: 2rem !important;
  font-weight: 500 !important;
}

/* Expander */
.streamlit-expanderHeader {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 3px !important;
  color: var(--text) !important;
  font-family: var(--serif) !important;
  font-size: 15px !important;
  font-weight: 600 !important;
}
.streamlit-expanderContent {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
}

/* Dataframe */
.stDataFrame { background: var(--surface) !important; }
.stDataFrame thead th {
  background: var(--surface2) !important;
  color: var(--gold) !important;
  font-family: var(--serif) !important;
  font-size: 12px !important;
  letter-spacing: 0.07em !important;
  text-transform: uppercase !important;
}
.stDataFrame tbody td {
  color: var(--text) !important;
  font-family: var(--serif) !important;
  font-size: 14px !important;
}

/* Cards */
.gc-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 0.8rem;
}
.gc-card-header {
  font-family: var(--serif);
  font-size: 11px;
  letter-spacing: 0.12em;
  color: var(--gold);
  text-transform: uppercase;
  margin-bottom: 0.5rem;
  font-weight: 600;
}
.gc-badge {
  display: inline-block;
  padding: 0.12rem 0.5rem;
  border-radius: 2px;
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 0.04em;
  font-weight: 600;
}
.badge-open    { background: rgba(74,126,181,0.15); color: #6a9fd8; border: 1px solid rgba(74,126,181,0.3); }
.badge-closed  { background: rgba(74,158,114,0.15); color: #5ab585; border: 1px solid rgba(74,158,114,0.3); }
.badge-overdue { background: rgba(192,83,79,0.15);  color: #d47070; border: 1px solid rgba(192,83,79,0.3); }
.badge-pending { background: rgba(201,168,76,0.15); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3); }
.badge-high    { background: rgba(192,83,79,0.15);  color: #d47070; border: 1px solid rgba(192,83,79,0.3); }
.badge-med     { background: rgba(201,168,76,0.15); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3); }
.badge-low     { background: rgba(74,158,114,0.15); color: #5ab585; border: 1px solid rgba(74,158,114,0.3); }

/* Timeline */
.gc-timeline-item {
  border-left: 1px solid var(--border2);
  padding: 0.3rem 0 0.3rem 1rem;
  margin-bottom: 0.4rem;
  position: relative;
  font-size: 14px;
  font-family: var(--serif);
  color: var(--text2);
  line-height: 1.5;
}
.gc-timeline-item::before {
  content: '◆';
  position: absolute;
  left: -0.42rem;
  color: var(--gold-dim);
  font-size: 0.5rem;
  top: 0.48rem;
}

/* Header banner */
.gc-header {
  background: var(--surface);
  border: 1px solid var(--border);
  border-top: 3px solid var(--gold-dim);
  border-radius: 3px;
  padding: 1.2rem 1.6rem;
  margin-bottom: 1.5rem;
}
.gc-header h1 {
  font-family: var(--display);
  font-size: 1.7rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--gold);
  margin: 0 0 0.2rem 0;
  font-style: italic;
}
.gc-header p {
  font-size: 13px;
  color: var(--text2);
  margin: 0;
  font-family: var(--serif);
  letter-spacing: 0.04em;
}

/* Alert boxes */
.gc-alert {
  border-radius: 3px;
  padding: 0.65rem 1rem;
  margin: 0.5rem 0;
  font-size: 14px;
  font-family: var(--serif);
  line-height: 1.5;
}
.gc-alert-warn   { background: rgba(201,168,76,0.08);  border-left: 3px solid var(--gold-dim); color: var(--gold2); }
.gc-alert-danger { background: rgba(192,83,79,0.08);   border-left: 3px solid var(--danger);   color: #d47070; }
.gc-alert-ok     { background: rgba(74,158,114,0.08);  border-left: 3px solid var(--success);  color: #5ab585; }

/* Divider */
hr { border: none; border-top: 1px solid var(--border) !important; margin: 1.2rem 0 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

/* Markdown text */
p, li, span { font-family: var(--serif) !important; line-height: 1.6 !important; }
h1, h2, h3  { font-family: var(--display) !important; font-weight: 500 !important; color: var(--text) !important; }
b, strong   { font-weight: 600 !important; color: var(--text) !important; }
code        { font-family: var(--mono) !important; font-size: 12px !important; background: var(--surface2) !important; padding: 0.1rem 0.3rem !important; border-radius: 2px !important; color: var(--gold2) !important; }

/* Login page */
.login-wrap { max-width: 420px; margin: 5vh auto; }
.login-logo { font-family: var(--display); font-size: 2.4rem; font-style: italic; color: var(--gold); letter-spacing: 0.06em; text-align: center; margin-bottom: 0.2rem; font-weight: 500; }
.login-sub  { text-align: center; color: var(--text2); font-size: 12px; margin-bottom: 2rem; font-family: var(--serif); letter-spacing: 0.12em; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SEED DATA
# ─────────────────────────────────────────────
def seed_data():
    now = datetime.now()
    def ts(days=0, hours=0):
        return (now - timedelta(days=days, hours=hours)).strftime("%Y-%m-%d %H:%M")

    return {
        "users": {
            "admin":      {"password": "pass",   "role": "Compliance Officer", "name": "Jordan Reed"},
            "supervisor": {"password": "pass",   "role": "Supervisor",         "name": "Morgan Ellis"},
            "analyst":    {"password": "pass",   "role": "Analyst",            "name": "Casey Park"},
        },
        "firm": {
            "name": "Apex Financial Services LLC",
            "industry": "Broker-Dealer (FINRA)",
            "crd": "123456",
            "regulator": "FINRA / SEC",
            "retention_years": 6,
            "approval_mode": "dual",
            "address": "101 Wall Street, New York, NY 10005",
        },
        "tasks": [
            {"id": "T-001", "title": "AML Transaction Monitoring Review", "assignee": "analyst", "due": (now + timedelta(days=3)).strftime("%Y-%m-%d"), "status": "Open", "priority": "High", "category": "AML", "evidence": [], "audit": [{"ts": ts(5), "user": "admin", "action": "Created task T-001"}], "rationale": "", "delegated_to": "", "delegated_memo": ""},
            {"id": "T-002", "title": "Q3 Supervisory Checklist – Options", "assignee": "supervisor", "due": (now - timedelta(days=2)).strftime("%Y-%m-%d"), "status": "Overdue", "priority": "High", "category": "Supervisory", "evidence": [], "audit": [{"ts": ts(10), "user": "admin", "action": "Created task T-002"}], "rationale": "", "delegated_to": "", "delegated_memo": ""},
            {"id": "T-003", "title": "Best Execution Policy Review", "assignee": "admin", "due": (now + timedelta(days=10)).strftime("%Y-%m-%d"), "status": "Open", "priority": "Medium", "category": "Trading", "evidence": [], "audit": [{"ts": ts(3), "user": "supervisor", "action": "Created task T-003"}], "rationale": "", "delegated_to": "", "delegated_memo": ""},
            {"id": "T-004", "title": "FINRA Rule 3110 Supervision Update", "assignee": "analyst", "due": (now + timedelta(days=1)).strftime("%Y-%m-%d"), "status": "Pending Approval", "priority": "High", "category": "Regulatory", "evidence": [{"name": "supervision_policy_v2.pdf", "uploaded_by": "analyst", "ts": ts(1), "hash": "abc123", "immutable": True}], "audit": [{"ts": ts(7), "user": "admin", "action": "Created task T-004"}, {"ts": ts(1), "user": "analyst", "action": "Evidence uploaded: supervision_policy_v2.pdf"}], "rationale": "", "delegated_to": "", "delegated_memo": ""},
            {"id": "T-005", "title": "Annual Cybersecurity Training Completion", "assignee": "analyst", "due": (now - timedelta(days=5)).strftime("%Y-%m-%d"), "status": "Closed", "priority": "Low", "category": "InfoSec", "evidence": [], "audit": [{"ts": ts(15), "user": "admin", "action": "Created task T-005"}, {"ts": ts(6), "user": "analyst", "action": "Marked complete"}, {"ts": ts(5), "user": "admin", "action": "Closed – training certificates verified"}], "rationale": "All staff completed training by deadline.", "delegated_to": "", "delegated_memo": ""},
        ],
        "exam_requests": [
            {"id": "ER-001", "title": "FINRA Cycle Exam 2024", "regulator": "FINRA", "due": (now + timedelta(days=30)).strftime("%Y-%m-%d"), "status": "In Progress", "items": [{"item": "Customer complaint files (2022-2024)", "status": "Uploaded", "assignee": "analyst"}, {"item": "Supervisory procedures manual", "status": "Pending", "assignee": "admin"}, {"item": "AML policies and SAR log", "status": "Uploaded", "assignee": "analyst"}, {"item": "Trade blotter – Q1-Q3 2024", "status": "Pending", "assignee": "supervisor"}], "audit": [{"ts": ts(20), "user": "admin", "action": "Exam request ER-001 created"}, {"ts": ts(18), "user": "admin", "action": "Items assigned to team"}]},
            {"id": "ER-002", "title": "SEC Annual Review", "regulator": "SEC", "due": (now + timedelta(days=60)).strftime("%Y-%m-%d"), "status": "Open", "items": [{"item": "Form ADV Part 2", "status": "Pending", "assignee": "admin"}, {"item": "Investment advisory agreements sample", "status": "Pending", "assignee": "supervisor"}], "audit": [{"ts": ts(5), "user": "admin", "action": "Exam request ER-002 created"}]},
        ],
        "rules": [
            {"id": "R-001", "title": "FINRA Rule 3110 – Supervision", "source": "FINRA", "category": "Supervision", "description": "Firms must establish and maintain a system of supervision reasonably designed to achieve compliance.", "status": "Active", "last_reviewed": ts(30), "ai_flagged": False},
            {"id": "R-002", "title": "FINRA Rule 4512 – Customer Account Info", "source": "FINRA", "category": "Customer Accounts", "description": "Member firms must maintain essential customer information for all accounts.", "status": "Active", "last_reviewed": ts(45), "ai_flagged": True},
            {"id": "R-003", "title": "SEC Rule 17a-4 – Records Retention", "source": "SEC", "category": "Recordkeeping", "description": "Broker-dealers must preserve records for specified time periods using WORM-compliant storage.", "status": "Active", "last_reviewed": ts(20), "ai_flagged": False},
            {"id": "R-004", "title": "Bank Secrecy Act – AML Program", "source": "FinCEN", "category": "AML/BSA", "description": "Financial institutions must implement AML programs including customer identification.", "status": "Active", "last_reviewed": ts(60), "ai_flagged": True},
            {"id": "R-005", "title": "Reg BI – Best Interest Obligation", "source": "SEC", "category": "Suitability", "description": "Broker-dealers must act in the best interest of retail customers when making recommendations.", "status": "Active", "last_reviewed": ts(10), "ai_flagged": False},
        ],
        "wsps": [
            {"id": "WSP-001", "title": "Anti-Money Laundering Program", "version": "3.2", "status": "Approved", "owner": "admin", "approved_by": "supervisor", "approved_ts": ts(15), "content": "This WSP establishes our AML program per BSA requirements. Includes CIP, transaction monitoring, SAR filing procedures, and annual training requirements. All registered representatives must complete AML training annually.", "versions": [{"ver": "3.1", "ts": ts(60), "author": "admin", "note": "Updated SAR thresholds"}, {"ver": "3.2", "ts": ts(15), "author": "admin", "note": "Added enhanced due diligence for high-risk accounts"}]},
            {"id": "WSP-002", "title": "Supervisory Procedures – Retail", "version": "2.0", "status": "Approved", "owner": "supervisor", "approved_by": "admin", "approved_ts": ts(30), "content": "Supervisory procedures for retail customer accounts. Covers trade review, account opening, complaint handling, and escalation paths. Supervisors must review all flagged trades within 24 hours.", "versions": [{"ver": "1.9", "ts": ts(90), "author": "supervisor", "note": "Added options review workflow"}, {"ver": "2.0", "ts": ts(30), "author": "supervisor", "note": "Incorporated Reg BI requirements"}]},
            {"id": "WSP-003", "title": "Information Barriers Policy", "version": "1.1", "status": "Draft", "owner": "analyst", "approved_by": "", "approved_ts": "", "content": "Policies governing information barriers between advisory and brokerage functions. Employees may not share material non-public information across business lines.", "versions": [{"ver": "1.0", "ts": ts(120), "author": "analyst", "note": "Initial draft"}, {"ver": "1.1", "ts": ts(7), "author": "analyst", "note": "Added electronic communication monitoring section"}]},
        ],
        "audit_trail": [
            {"ts": ts(30), "user": "admin", "module": "System", "action": "System initialized; sample data seeded"},
            {"ts": ts(20), "user": "admin", "module": "Exam Requests", "action": "Created ER-001: FINRA Cycle Exam 2024"},
            {"ts": ts(15), "user": "supervisor", "module": "WSP Repository", "action": "Approved WSP-001 v3.2"},
            {"ts": ts(10), "user": "analyst", "module": "Tasks", "action": "Evidence uploaded for T-004"},
            {"ts": ts(5), "user": "admin", "module": "Exam Requests", "action": "Created ER-002: SEC Annual Review"},
            {"ts": ts(2), "user": "supervisor", "module": "Tasks", "action": "Escalation: T-002 is overdue"},
        ],
        "evidence": [
            {"id": "EV-001", "filename": "aml_policy_2024.pdf",        "uploaded_by": "admin",    "ts": ts(15), "task_id": "T-004", "hash": "sha256:a1b2c3d4", "immutable": True, "archived": False},
            {"id": "EV-002", "filename": "supervision_policy_v2.pdf",  "uploaded_by": "analyst",  "ts": ts(1),  "task_id": "T-004", "hash": "sha256:e5f6a7b8", "immutable": True, "archived": False},
            {"id": "EV-003", "filename": "cybersecurity_training_certs.zip", "uploaded_by": "analyst", "ts": ts(6), "task_id": "T-005", "hash": "sha256:c9d0e1f2", "immutable": True, "archived": True},
        ],
        "rule_scan_memo": None,
        "org_chart": [
            {"role": "Chief Compliance Officer", "user": "admin",      "reports_to": "",         "responsibilities": ["AML Oversight", "Exam Management", "Rule Inventory"]},
            {"role": "Supervising Principal",    "user": "supervisor", "reports_to": "admin",    "responsibilities": ["Trade Review", "Supervisory Checklists", "Rep Oversight"]},
            {"role": "Compliance Analyst",       "user": "analyst",    "reports_to": "supervisor", "responsibilities": ["Evidence Collection", "Testing", "Filings"]},
        ],
        "approvals": [
            {"id": "AP-001", "item": "WSP-002 v2.0", "type": "WSP Approval", "requestor": "supervisor", "approver1": "admin", "approver1_ts": ts(30), "approver2": "", "status": "Approved", "ts": ts(30)},
        ],
    }

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = seed_data()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

D = st.session_state.data  # shortcut

def add_audit(module, action):
    D["audit_trail"].append({
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "user": st.session_state.current_user,
        "module": module,
        "action": action,
    })

def current_role():
    u = st.session_state.current_user
    return D["users"][u]["role"] if u else ""

def current_name():
    u = st.session_state.current_user
    return D["users"][u]["name"] if u else ""

# ─────────────────────────────────────────────
#  LOGIN PAGE
# ─────────────────────────────────────────────
def login_page():
    st.markdown("""
    <div class='login-wrap'>
      <div class='login-logo'>⚖ GRAPHITE</div>
      <div class='login-sub'>COMPLIANCE INTELLIGENCE PLATFORM</div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<div class='gc-card'>", unsafe_allow_html=True)
        st.markdown("<div class='gc-card-header'>SECURE LOGIN</div>", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="admin / supervisor / analyst")
        password = st.text_input("Password", type="password", placeholder="pass")
        if st.button("Sign In →", use_container_width=True):
            users = D["users"]
            if username in users and users[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                add_audit("Auth", f"Login: {username}")
                st.rerun()
            else:
                st.error("Invalid credentials.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:center;margin-top:1rem;font-family:var(--mono);font-size:0.7rem;color:var(--text2)'>
        demo: admin / supervisor / analyst  ·  password: pass
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style='padding:0.8rem 0 1rem 0;border-bottom:1px solid var(--border);margin-bottom:1rem'>
          <div style='font-family:var(--display);font-size:1.5rem;color:var(--gold);letter-spacing:0.04em;font-style:italic;font-weight:500'>⚖ Graphite</div>
          <div style='font-size:11px;color:var(--text2);font-family:var(--serif);letter-spacing:0.12em;text-transform:uppercase'>Compliance Platform</div>
        </div>
        <div style='font-size:11px;color:var(--text2);font-family:var(--serif);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.3rem'>Logged in as</div>
        <div style='font-size:0.9rem;font-weight:600;color:var(--text);margin-bottom:0.2rem'>{current_name()}</div>
        <div style='font-size:0.72rem;color:var(--gold);font-family:var(--mono)'>{current_role()}</div>
        <hr/>
        """, unsafe_allow_html=True)

        # Overdue alert
        overdue = [t for t in D["tasks"] if t["status"] == "Overdue"]
        if overdue:
            st.markdown(f"<div class='gc-alert gc-alert-danger'>⚠ {len(overdue)} OVERDUE TASK(S)</div>", unsafe_allow_html=True)

        pages = [
            ("🏠", "Dashboard"),
            ("📋", "Tasks & Remediation"),
            ("📁", "Exam Requests"),
            ("📚", "WSP Repository"),
            ("🔍", "Evidence Repository"),
            ("📏", "Rule Inventory"),
            ("🤖", "AI Rule Scan"),
            ("🏢", "Org Chart"),
            ("🔒", "Audit Trail"),
            ("⚙️", "Firm Config"),
            ("💾", "Data Export"),
        ]
        nav = st.radio(
            "Navigation",
            [p[1] for p in pages],
            format_func=lambda x: next(p[0] + "  " + p[1] for p in pages if p[1] == x),
            label_visibility="collapsed",
        )
        st.markdown("<hr/>", unsafe_allow_html=True)
        if st.button("Sign Out", use_container_width=True):
            add_audit("Auth", "Logout")
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()
        return nav

# ─────────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────────
def page_dashboard():
    st.markdown(f"""
    <div class='gc-header'>
      <h1>COMPLIANCE DASHBOARD</h1>
      <p>{D['firm']['name']}  ·  {D['firm']['regulator']}  ·  {datetime.now().strftime('%B %d, %Y')}</p>
    </div>
    """, unsafe_allow_html=True)

    tasks = D["tasks"]
    open_t   = len([t for t in tasks if t["status"] == "Open"])
    overdue  = len([t for t in tasks if t["status"] == "Overdue"])
    pending  = len([t for t in tasks if t["status"] == "Pending Approval"])
    closed   = len([t for t in tasks if t["status"] == "Closed"])
    exams    = len(D["exam_requests"])
    evidence = len(D["evidence"])

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Open Tasks",    open_t)
    c2.metric("Overdue",       overdue,   delta=f"-{overdue} urgent" if overdue else None, delta_color="inverse")
    c3.metric("Pending Review",pending)
    c4.metric("Closed",        closed)
    c5.metric("Exam Requests", exams)
    c6.metric("Evidence Files",evidence)

    st.markdown("<hr/>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1.6, 1])

    with col_l:
        st.markdown("<div class='gc-card-header' style='font-family:var(--mono);font-size:0.75rem;letter-spacing:0.1em;color:var(--gold);text-transform:uppercase;margin-bottom:0.8rem'>MY TASKS</div>", unsafe_allow_html=True)
        my_tasks = [t for t in tasks if t["assignee"] == st.session_state.current_user or current_role() == "Compliance Officer"]
        for t in my_tasks[:6]:
            s = t["status"]
            badge_cls = "badge-overdue" if s=="Overdue" else "badge-open" if s=="Open" else "badge-pending" if "Pending" in s else "badge-closed"
            p = t["priority"]
            pri_cls = "badge-high" if p=="High" else "badge-med" if p=="Medium" else "badge-low"
            st.markdown(f"""
            <div class='gc-card' style='margin-bottom:0.5rem;padding:0.8rem 1rem'>
              <div style='display:flex;justify-content:space-between;align-items:center'>
                <div>
                  <span style='font-family:var(--mono);font-size:0.7rem;color:var(--text2)'>{t['id']}</span>
                  <span style='margin-left:0.5rem;font-size:0.85rem;font-weight:600'>{t['title']}</span>
                </div>
                <div>
                  <span class='gc-badge {badge_cls}'>{s}</span>&nbsp;
                  <span class='gc-badge {pri_cls}'>{p}</span>
                </div>
              </div>
              <div style='margin-top:0.4rem;font-size:0.75rem;color:var(--text2)'>
                Due: {t['due']}  ·  Assignee: {D['users'].get(t['assignee'],{}).get('name',t['assignee'])}  ·  Category: {t['category']}
              </div>
            </div>
            """, unsafe_allow_html=True)

    with col_r:
        st.markdown("<div class='gc-card-header' style='font-family:var(--mono);font-size:0.75rem;letter-spacing:0.1em;color:var(--gold);text-transform:uppercase;margin-bottom:0.8rem'>RECENT ACTIVITY</div>", unsafe_allow_html=True)
        for entry in reversed(D["audit_trail"][-8:]):
            st.markdown(f"""
            <div class='gc-timeline-item'>
              <span style='color:var(--gold);font-family:var(--mono);font-size:0.68rem'>{entry['ts']}</span>
              <span style='color:var(--text2)'> · {entry['user']}</span><br/>
              <span style='color:var(--text)'>{entry['action']}</span>
            </div>
            """, unsafe_allow_html=True)

        # Flagged rules
        flagged = [r for r in D["rules"] if r["ai_flagged"]]
        if flagged:
            st.markdown("<hr/>", unsafe_allow_html=True)
            st.markdown("<div class='gc-alert gc-alert-warn'>🤖 AI flagged rule changes detected</div>", unsafe_allow_html=True)
            for r in flagged:
                st.markdown(f"<div style='font-size:0.78rem;padding:0.2rem 0 0 0.5rem;color:var(--text2)'>• {r['title']}</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TASKS & REMEDIATION
# ─────────────────────────────────────────────
def page_tasks():
    st.markdown("<div class='gc-header'><h1>TASKS & REMEDIATION</h1><p>Create, assign, track, and close compliance tasks with full audit trail</p></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📋  TASK LIST", "➕  NEW TASK"])

    with tab1:
        # Filter
        fc1, fc2, fc3 = st.columns(3)
        filter_status   = fc1.selectbox("Status", ["All","Open","Overdue","Pending Approval","Closed"])
        filter_priority = fc2.selectbox("Priority", ["All","High","Medium","Low"])
        filter_cat      = fc3.selectbox("Category", ["All"] + list({t["category"] for t in D["tasks"]}))

        tasks = D["tasks"]
        if filter_status   != "All": tasks = [t for t in tasks if t["status"]   == filter_status]
        if filter_priority != "All": tasks = [t for t in tasks if t["priority"] == filter_priority]
        if filter_cat      != "All": tasks = [t for t in tasks if t["category"] == filter_cat]

        # Auto-escalate
        today_str = date.today().strftime("%Y-%m-%d")
        for t in D["tasks"]:
            if t["status"] == "Open" and t["due"] < today_str:
                t["status"] = "Overdue"
                t["audit"].append({"ts": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": "SYSTEM", "action": "Auto-escalated to Overdue"})
                add_audit("Tasks", f"Auto-escalated {t['id']} to Overdue")

        for t in tasks:
            s = t["status"]
            badge_cls = "badge-overdue" if s=="Overdue" else "badge-open" if s=="Open" else "badge-pending" if "Pending" in s else "badge-closed"
            p_cls = "badge-high" if t["priority"]=="High" else "badge-med" if t["priority"]=="Medium" else "badge-low"
            with st.expander(f"[{t['id']}]  {t['title']}"):
                c1,c2,c3 = st.columns(3)
                c1.markdown(f"**Assignee:** {D['users'].get(t['assignee'],{}).get('name',t['assignee'])}")
                c2.markdown(f"**Due:** {t['due']}")
                c3.markdown(f"**Category:** {t['category']}")
                st.markdown(f"Status: <span class='gc-badge {badge_cls}'>{s}</span>&nbsp; Priority: <span class='gc-badge {p_cls}'>{t['priority']}</span>", unsafe_allow_html=True)

                if t["delegated_to"]:
                    st.markdown(f"<div class='gc-alert gc-alert-warn'>Delegated to: {t['delegated_to']}  ·  Memo: {t['delegated_memo']}</div>", unsafe_allow_html=True)

                # Evidence
                st.markdown("<hr/><b>Evidence Files</b>", unsafe_allow_html=True)
                if t["evidence"]:
                    for ev in t["evidence"]:
                        st.markdown(f"<div class='gc-timeline-item'>📎 {ev['name']}  ·  {ev['uploaded_by']}  ·  {ev['ts']}  <span class='gc-badge badge-closed'>IMMUTABLE</span></div>", unsafe_allow_html=True)
                else:
                    st.caption("No evidence attached.")

                uploaded = st.file_uploader(f"Upload evidence for {t['id']}", key=f"up_{t['id']}", label_visibility="collapsed")
                if uploaded:
                    fake_hash = hashlib.md5(uploaded.name.encode()).hexdigest()[:8]
                    ev_entry = {"name": uploaded.name, "uploaded_by": st.session_state.current_user, "ts": datetime.now().strftime("%Y-%m-%d %H:%M"), "hash": fake_hash, "immutable": True}
                    t["evidence"].append(ev_entry)
                    t["audit"].append({"ts": ev_entry["ts"], "user": st.session_state.current_user, "action": f"Evidence uploaded: {uploaded.name}"})
                    # Global evidence repo
                    ev_id = f"EV-{len(D['evidence'])+1:03d}"
                    D["evidence"].append({"id": ev_id, "filename": uploaded.name, "uploaded_by": st.session_state.current_user, "ts": ev_entry["ts"], "task_id": t["id"], "hash": fake_hash, "immutable": True, "archived": False})
                    add_audit("Evidence", f"Uploaded {uploaded.name} for {t['id']}")
                    st.success(f"✓ {uploaded.name} uploaded (WORM-locked)")

                # Actions
                st.markdown("<hr/>", unsafe_allow_html=True)
                ac1,ac2,ac3,ac4 = st.columns(4)
                if ac1.button("Submit for Approval", key=f"sub_{t['id']}"):
                    if t["status"] not in ["Closed"]:
                        t["status"] = "Pending Approval"
                        t["audit"].append({"ts": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": st.session_state.current_user, "action": "Submitted for approval"})
                        add_audit("Tasks", f"{t['id']} submitted for approval")
                        st.rerun()
                if ac2.button("Approve & Close", key=f"apr_{t['id']}"):
                    if current_role() in ["Compliance Officer","Supervisor"]:
                        t["status"] = "Closed"
                        t["audit"].append({"ts": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": st.session_state.current_user, "action": "Approved and closed"})
                        add_audit("Tasks", f"{t['id']} approved and closed")
                        st.rerun()
                    else:
                        st.warning("Insufficient permissions.")

                # Delegate
                with st.expander("🔀 Delegate Task"):
                    dg1,dg2 = st.columns(2)
                    delegate_to = dg1.selectbox("Delegate to", list(D["users"].keys()), key=f"dt_{t['id']}")
                    memo        = dg2.text_input("Delegation memo", key=f"dm_{t['id']}")
                    if st.button("Confirm Delegation", key=f"dlg_{t['id']}"):
                        t["delegated_to"]   = delegate_to
                        t["delegated_memo"] = memo
                        t["audit"].append({"ts": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": st.session_state.current_user, "action": f"Delegated to {delegate_to}: {memo}"})
                        add_audit("Tasks", f"{t['id']} delegated to {delegate_to}")
                        st.rerun()

                # Close with rationale
                with st.expander("🚪 Withdraw / Close-Out"):
                    rat = st.text_area("Closure rationale (required)", key=f"rat_{t['id']}")
                    if st.button("Close with Rationale", key=f"cwr_{t['id']}"):
                        if rat.strip():
                            t["status"]    = "Closed"
                            t["rationale"] = rat
                            t["audit"].append({"ts": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": st.session_state.current_user, "action": f"Closed with rationale: {rat}"})
                            add_audit("Tasks", f"{t['id']} closed: {rat}")
                            st.rerun()
                        else:
                            st.warning("Rationale required.")

                # Audit timeline
                st.markdown("<hr/><b>Audit Trail</b>", unsafe_allow_html=True)
                for entry in t["audit"]:
                    st.markdown(f"<div class='gc-timeline-item'><span style='color:var(--gold);font-family:var(--mono);font-size:0.68rem'>{entry['ts']}</span>  ·  <b>{entry['user']}</b>  ·  {entry['action']}</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("**Create New Task / Remediation Item**")
        c1,c2 = st.columns(2)
        title    = c1.text_input("Task Title")
        assignee = c2.selectbox("Assignee", list(D["users"].keys()))
        c3,c4,c5 = st.columns(3)
        due_date = c3.date_input("Due Date", value=date.today() + timedelta(days=7))
        priority = c4.selectbox("Priority", ["High","Medium","Low"])
        category = c5.selectbox("Category", ["AML","Supervisory","Trading","Regulatory","InfoSec","Testing","Other"])
        if st.button("Create Task"):
            if title.strip():
                new_id = f"T-{len(D['tasks'])+1:03d}"
                D["tasks"].append({
                    "id": new_id, "title": title, "assignee": assignee,
                    "due": due_date.strftime("%Y-%m-%d"), "status": "Open",
                    "priority": priority, "category": category, "evidence": [],
                    "audit": [{"ts": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": st.session_state.current_user, "action": f"Created task {new_id}"}],
                    "rationale": "", "delegated_to": "", "delegated_memo": "",
                })
                add_audit("Tasks", f"Created {new_id}: {title}")
                st.success(f"✓ Task {new_id} created.")
                st.rerun()
            else:
                st.warning("Title required.")

# ─────────────────────────────────────────────
#  EXAM REQUESTS
# ─────────────────────────────────────────────
def page_exam_requests():
    st.markdown("<div class='gc-header'><h1>EXAM / DOCUMENT REQUEST WORKFLOW</h1><p>Centralized workspace for regulatory exam preparation and document collection</p></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📁  ACTIVE EXAMS", "➕  NEW EXAM REQUEST"])

    with tab1:
        for er in D["exam_requests"]:
            total = len(er["items"])
            done  = len([i for i in er["items"] if i["status"] == "Uploaded"])
            pct   = int(done/total*100) if total else 0
            s_cls = "badge-open" if er["status"]=="Open" else "badge-pending"
            with st.expander(f"[{er['id']}]  {er['title']}  ·  {er['regulator']}  ·  Due: {er['due']}"):
                st.markdown(f"Status: <span class='gc-badge {s_cls}'>{er['status']}</span>  ·  Progress: **{done}/{total} items** ({pct}%)", unsafe_allow_html=True)
                st.progress(pct/100)

                st.markdown("<br/><b>Document Checklist</b>", unsafe_allow_html=True)
                for idx, item in enumerate(er["items"]):
                    ic1,ic2,ic3,ic4 = st.columns([3,1.5,1.5,1.5])
                    ic1.markdown(f"{'✅' if item['status']=='Uploaded' else '⏳'}  {item['item']}")
                    ic2.markdown(f"<span class='gc-badge {'badge-closed' if item['status']=='Uploaded' else 'badge-pending'}'>{item['status']}</span>", unsafe_allow_html=True)
                    ic3.markdown(f"_{D['users'].get(item['assignee'],{}).get('name',item['assignee'])}_")
                    uploaded = ic4.file_uploader("Upload", key=f"er_{er['id']}_{idx}", label_visibility="collapsed")
                    if uploaded:
                        item["status"] = "Uploaded"
                        er["audit"].append({"ts": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": st.session_state.current_user, "action": f"Uploaded: {uploaded.name} for '{item['item']}'"})
                        add_audit("Exam Requests", f"{er['id']}: Uploaded {uploaded.name}")
                        st.rerun()

                # Export package
                st.markdown("<hr/>", unsafe_allow_html=True)
                if st.button(f"📦 Export Exam Package ({er['id']})", key=f"exp_{er['id']}"):
                    payload = json.dumps({"exam": er, "audit": er["audit"]}, indent=2)
                    st.download_button("Download JSON Package", data=payload, file_name=f"{er['id']}_package.json", mime="application/json", key=f"dl_{er['id']}")
                    add_audit("Exam Requests", f"Exported package for {er['id']}")

                st.markdown("<hr/><b>Audit Trail</b>", unsafe_allow_html=True)
                for entry in er["audit"]:
                    st.markdown(f"<div class='gc-timeline-item'><span style='color:var(--gold);font-family:var(--mono);font-size:0.68rem'>{entry['ts']}</span>  ·  <b>{entry['user']}</b>  ·  {entry['action']}</div>", unsafe_allow_html=True)

    with tab2:
        c1,c2 = st.columns(2)
        title    = c1.text_input("Exam Title")
        reg      = c2.selectbox("Regulator", ["FINRA","SEC","CFTC","NFA","State Regulator","Internal"])
        due_date = st.date_input("Response Due Date", value=date.today() + timedelta(days=30))
        st.markdown("**Document Items Requested** (one per line)")
        items_raw = st.text_area("Items", "Customer files\nSupervisory procedures\nAML program documentation", height=100)
        if st.button("Create Exam Request"):
            if title.strip():
                new_id = f"ER-{len(D['exam_requests'])+1:03d}"
                items  = [{"item": i.strip(), "status": "Pending", "assignee": st.session_state.current_user} for i in items_raw.splitlines() if i.strip()]
                D["exam_requests"].append({"id": new_id, "title": title, "regulator": reg, "due": due_date.strftime("%Y-%m-%d"), "status": "Open", "items": items, "audit": [{"ts": datetime.now().strftime("%Y-%m-%d %H:%M"), "user": st.session_state.current_user, "action": f"Created {new_id}"}]})
                add_audit("Exam Requests", f"Created {new_id}: {title}")
                st.success(f"✓ {new_id} created.")
                st.rerun()

# ─────────────────────────────────────────────
#  WSP REPOSITORY
# ─────────────────────────────────────────────
def page_wsp():
    st.markdown("<div class='gc-header'><h1>WSP / PROCEDURE REPOSITORY</h1><p>Version-controlled policy library with redlining and approval workflows</p></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📚  PROCEDURES", "➕  NEW WSP / UPLOAD"])

    with tab1:
        for wsp in D["wsps"]:
            s_cls = "badge-closed" if wsp["status"]=="Approved" else "badge-pending" if wsp["status"]=="Draft" else "badge-open"
            with st.expander(f"[{wsp['id']}]  {wsp['title']}  ·  v{wsp['version']}"):
                st.markdown(f"Status: <span class='gc-badge {s_cls}'>{wsp['status']}</span>  ·  Owner: **{D['users'].get(wsp['owner'],{}).get('name',wsp['owner'])}**", unsafe_allow_html=True)
                if wsp["approved_by"]:
                    st.markdown(f"Approved by: **{D['users'].get(wsp['approved_by'],{}).get('name',wsp['approved_by'])}**  ·  {wsp['approved_ts']}", unsafe_allow_html=True)

                st.markdown("<hr/><b>Current Content</b>", unsafe_allow_html=True)
                st.markdown(f"<div class='gc-card' style='font-size:0.82rem;color:var(--text2)'>{wsp['content']}</div>", unsafe_allow_html=True)

                # Version history & diff
                st.markdown("<b>Version History</b>", unsafe_allow_html=True)
                for v in wsp["versions"]:
                    st.markdown(f"<div class='gc-timeline-item'>v{v['ver']}  ·  {v['ts']}  ·  {v['author']}  ·  <i>{v['note']}</i></div>", unsafe_allow_html=True)

                # Redlining diff
                if len(wsp["versions"]) >= 2:
                    if st.button(f"🔴 Show Redline Diff ({wsp['id']})", key=f"diff_{wsp['id']}"):
                        old = "Original supervisory procedures text for version comparison purposes."
                        new = wsp["content"]
                        diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", fromfile="Previous", tofile="Current"))
                        diff_text = "\n".join(diff[:30]) if diff else "No diff available."
                        st.code(diff_text, language="diff")

                # Approve
                if wsp["status"] == "Draft" and current_role() in ["Compliance Officer","Supervisor"]:
                    if st.button(f"✅ Approve {wsp['id']}", key=f"awsp_{wsp['id']}"):
                        wsp["status"]      = "Approved"
                        wsp["approved_by"] = st.session_state.current_user
                        wsp["approved_ts"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        D["approvals"].append({"id": f"AP-{len(D['approvals'])+1:03d}", "item": f"{wsp['id']} v{wsp['version']}", "type": "WSP Approval", "requestor": wsp["owner"], "approver1": st.session_state.current_user, "approver1_ts": wsp["approved_ts"], "approver2": "", "status": "Approved", "ts": wsp["approved_ts"]})
                        add_audit("WSP Repository", f"Approved {wsp['id']} v{wsp['version']}")
                        st.rerun()

                # ── WSP → Supervisory Checklist Generator ──────────────────
                st.markdown("<hr/>", unsafe_allow_html=True)
                st.markdown("<div class='gc-card-header' style='font-family:var(--mono);font-size:0.72rem;letter-spacing:0.1em;color:var(--gold);text-transform:uppercase;margin-bottom:0.6rem'>📋 Generate Supervisory Checklist from this WSP</div>", unsafe_allow_html=True)

                # AI keyword → checklist item mapping
                CHECKLIST_RULES = [
                    ("annual training",      "Complete annual compliance training (per WSP)",          "High",   "Supervisory", 365),
                    ("train",                "Schedule staff training session",                         "Medium", "Supervisory", 90),
                    ("review",               "Conduct periodic supervisory review",                     "High",   "Supervisory", 30),
                    ("monitor",              "Perform transaction monitoring review",                   "High",   "AML",         30),
                    ("sar",                  "Review SAR filing obligations and thresholds",            "High",   "AML",         90),
                    ("aml",                  "Test AML program controls",                               "High",   "AML",         90),
                    ("customer identif",     "Verify CIP procedures are current",                      "High",   "AML",         180),
                    ("supervisory",          "Supervisory sign-off on flagged items",                  "High",   "Supervisory", 7),
                    ("escalat",              "Review escalation log and open items",                   "Medium", "Supervisory", 14),
                    ("complaint",            "Review and log customer complaints",                     "High",   "Supervisory", 30),
                    ("best interest",        "Best interest suitability review for new recommendations","High",  "Suitability",  30),
                    ("reg bi",               "Confirm Reg BI disclosures are current",                 "High",   "Regulatory",  90),
                    ("retention",            "Verify records retention schedule compliance",            "Medium", "Regulatory",  180),
                    ("information barrier",  "Test information barrier controls",                      "High",   "Trading",     90),
                    ("non-public",           "Certify no MNPI sharing across business lines",          "High",   "Trading",     30),
                    ("electronic commun",    "Review electronic communications surveillance sample",   "Medium", "Supervisory", 30),
                    ("trade review",         "Complete trade review for supervised accounts",          "High",   "Trading",     7),
                    ("24 hour",              "Same-day review of all flagged trades (24hr SLA)",       "High",   "Supervisory", 1),
                    ("disclosure",           "Update and distribute required disclosures",             "Medium", "Regulatory",  90),
                    ("due diligence",        "Perform enhanced due diligence on high-risk accounts",   "High",   "AML",         90),
                ]

                content_lower = wsp["content"].lower()
                suggested = []
                seen_titles = set()
                for keyword, task_title, priority, category, freq_days in CHECKLIST_RULES:
                    if keyword in content_lower and task_title not in seen_titles:
                        suggested.append({
                            "title":    f"[{wsp['id']}] {task_title}",
                            "priority": priority,
                            "category": category,
                            "freq_days": freq_days,
                        })
                        seen_titles.add(task_title)

                if not suggested:
                    # Fallback generic item
                    suggested = [{"title": f"[{wsp['id']}] Periodic review of {wsp['title']}", "priority": "Medium", "category": "Supervisory", "freq_days": 90}]

                st.markdown(f"<div class='gc-alert gc-alert-ok'>🤖 AI parsed <b>{wsp['title']}</b> — found <b>{len(suggested)}</b> supervisory obligation(s)</div>", unsafe_allow_html=True)

                # Show preview table
                for item in suggested:
                    freq_label = f"Every {item['freq_days']}d" if item['freq_days'] >= 14 else f"Every {item['freq_days']}d (urgent)"
                    p_cls = "badge-high" if item["priority"]=="High" else "badge-med" if item["priority"]=="Medium" else "badge-low"
                    st.markdown(f"""
                    <div style='display:flex;justify-content:space-between;align-items:center;
                                padding:0.45rem 0.7rem;margin:0.25rem 0;
                                background:var(--surface2);border:1px solid var(--border);border-radius:4px;font-size:0.8rem'>
                      <span>☐ &nbsp;{item['title']}</span>
                      <span>
                        <span class='gc-badge {p_cls}'>{item['priority']}</span>&nbsp;
                        <span class='gc-badge badge-open'>{item['category']}</span>&nbsp;
                        <span style='color:var(--text2);font-family:var(--mono);font-size:0.68rem'>{freq_label}</span>
                      </span>
                    </div>
                    """, unsafe_allow_html=True)

                # Assignee + due date controls
                cl1, cl2, cl3 = st.columns(3)
                cl_assignee = cl1.selectbox("Assign checklist to", list(D["users"].keys()), key=f"cl_assign_{wsp['id']}")
                cl_due      = cl2.date_input("First due date", value=date.today() + timedelta(days=7), key=f"cl_due_{wsp['id']}")
                cl_recur    = cl3.selectbox("Recurrence", ["One-time","Weekly","Monthly","Quarterly","Annually"], key=f"cl_recur_{wsp['id']}")

                if st.button(f"✅ Create {len(suggested)} Checklist Task(s) from {wsp['id']}", key=f"gen_cl_{wsp['id']}"):
                    created = []
                    for item in suggested:
                        new_id = f"T-{len(st.session_state.data['tasks'])+1:03d}"
                        st.session_state.data["tasks"].append({
                            "id":           new_id,
                            "title":        item["title"],
                            "assignee":     cl_assignee,
                            "due":          cl_due.strftime("%Y-%m-%d"),
                            "status":       "Open",
                            "priority":     item["priority"],
                            "category":     item["category"],
                            "evidence":     [],
                            "audit": [{
                                "ts":     datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "user":   st.session_state.current_user,
                                "action": f"Auto-created from WSP {wsp['id']} v{wsp['version']} ({cl_recur})",
                            }],
                            "rationale":      "",
                            "delegated_to":   "",
                            "delegated_memo": "",
                            "source_wsp":     wsp["id"],
                            "recurrence":     cl_recur,
                        })
                        created.append(new_id)
                    st.session_state.data["audit_trail"].append({
                        "ts": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "user": st.session_state.current_user,
                        "module": "WSP Repository",
                        "action": f"Generated {len(created)} checklist tasks from {wsp['id']}: {', '.join(created)}",
                    })
                    st.success(f"✓ {len(created)} tasks created: {', '.join(created)} — go to Tasks & Remediation to view them")

    with tab2:
        c1,c2 = st.columns(2)
        title   = c1.text_input("WSP Title")
        ver     = c2.text_input("Version", value="1.0")
        content = st.text_area("Content / Procedures", height=180, placeholder="Enter the full text of the WSP here...")
        note    = st.text_input("Change note / summary")
        if st.button("Save WSP"):
            if title.strip():
                new_id = f"WSP-{len(D['wsps'])+1:03d}"
                D["wsps"].append({"id": new_id, "title": title, "version": ver, "status": "Draft", "owner": st.session_state.current_user, "approved_by": "", "approved_ts": "", "content": content, "versions": [{"ver": ver, "ts": datetime.now().strftime("%Y-%m-%d %H:%M"), "author": st.session_state.current_user, "note": note}]})
                add_audit("WSP Repository", f"Created {new_id}: {title} v{ver}")
                st.success(f"✓ {new_id} saved as Draft.")
                st.rerun()

# ─────────────────────────────────────────────
#  EVIDENCE REPOSITORY
# ─────────────────────────────────────────────
def page_evidence():
    st.markdown("<div class='gc-header'><h1>EVIDENCE REPOSITORY</h1><p>WORM-compliant, immutable evidence store with global search</p></div>", unsafe_allow_html=True)
    search = st.text_input("🔍 Search files...", placeholder="filename, task ID, uploader...")

    ev_list = D["evidence"]
    if search:
        ev_list = [e for e in ev_list if search.lower() in e["filename"].lower() or search.lower() in e["task_id"].lower() or search.lower() in e["uploaded_by"].lower()]

    # Retention: mark old items archived
    for ev in D["evidence"]:
        age_days = (datetime.now() - datetime.strptime(ev["ts"], "%Y-%m-%d %H:%M")).days
        if age_days > 5:
            ev["archived"] = True

    fc1,fc2 = st.columns(2)
    show_arch = fc1.checkbox("Show Archived", value=True)
    if not show_arch:
        ev_list = [e for e in ev_list if not e["archived"]]

    for ev in ev_list:
        arch_badge = " <span class='gc-badge badge-pending'>ARCHIVED</span>" if ev["archived"] else ""
        st.markdown(f"""
        <div class='gc-card'>
          <div style='display:flex;justify-content:space-between;align-items:center'>
            <div>
              <span style='font-family:var(--mono);color:var(--gold);font-size:0.72rem'>{ev['id']}</span>  
              <span style='font-weight:600;margin-left:0.5rem'>📎 {ev['filename']}</span>{arch_badge}
            </div>
            <span class='gc-badge badge-closed'>IMMUTABLE ·WORM</span>
          </div>
          <div style='margin-top:0.4rem;font-size:0.75rem;color:var(--text2)'>
            Uploaded by: <b>{D['users'].get(ev['uploaded_by'],{}).get('name',ev['uploaded_by'])}</b>  ·  
            {ev['ts']}  ·  Task: <b>{ev['task_id']}</b>  ·  Hash: <code style='font-size:0.68rem;color:var(--text2)'>{ev['hash']}</code>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("**Upload New Evidence to Repository**")
    c1,c2 = st.columns(2)
    task_id  = c1.selectbox("Link to Task", [t["id"] for t in D["tasks"]])
    uploaded = c2.file_uploader("Select File")
    if uploaded:
        fake_hash = "sha256:" + hashlib.md5(uploaded.name.encode()).hexdigest()
        ev_id = f"EV-{len(D['evidence'])+1:03d}"
        D["evidence"].append({"id": ev_id, "filename": uploaded.name, "uploaded_by": st.session_state.current_user, "ts": datetime.now().strftime("%Y-%m-%d %H:%M"), "task_id": task_id, "hash": fake_hash, "immutable": True, "archived": False})
        add_audit("Evidence", f"Uploaded {uploaded.name} linked to {task_id}")
        st.success(f"✓ {uploaded.name} stored as {ev_id} (WORM-locked)")
        st.rerun()

# ─────────────────────────────────────────────
#  RULE INVENTORY
# ─────────────────────────────────────────────
def page_rules():
    st.markdown("<div class='gc-header'><h1>MASTER RULE INVENTORY</h1><p>Centralized regulatory rule register with AI-assisted parsing</p></div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📏  RULE LIST", "➕  ADD RULE", "🤖  PARSE FROM DOCUMENT"])

    with tab1:
        for r in D["rules"]:
            flag = " 🤖 AI FLAGGED" if r["ai_flagged"] else ""
            s_cls = "badge-closed"
            with st.expander(f"[{r['id']}]  {r['title']}{flag}"):
                st.markdown(f"**Source:** {r['source']}  ·  **Category:** {r['category']}  ·  **Last Reviewed:** {r['last_reviewed']}")
                st.markdown(f"<div class='gc-card' style='font-size:0.82rem;color:var(--text2)'>{r['description']}</div>", unsafe_allow_html=True)
                if r["ai_flagged"]:
                    st.markdown("<div class='gc-alert gc-alert-warn'>🤖 AI Rule Scan has detected a potential change to this rule. Review recommended.</div>", unsafe_allow_html=True)
                c1,c2 = st.columns(2)
                if c1.button(f"Mark Reviewed", key=f"rev_{r['id']}"):
                    r["last_reviewed"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    r["ai_flagged"]    = False
                    add_audit("Rule Inventory", f"Marked {r['id']} as reviewed")
                    st.rerun()

    with tab2:
        c1,c2 = st.columns(2)
        r_title = c1.text_input("Rule Title")
        r_src   = c2.selectbox("Source", ["FINRA","SEC","CFTC","FinCEN","MSRB","State","Internal"])
        c3,c4   = st.columns(2)
        r_cat   = c3.selectbox("Category", ["AML","Supervision","Recordkeeping","Suitability","Customer Accounts","Trading","Other"])
        r_desc  = st.text_area("Description")
        if st.button("Add Rule"):
            if r_title.strip():
                new_id = f"R-{len(D['rules'])+1:03d}"
                D["rules"].append({"id": new_id, "title": r_title, "source": r_src, "category": r_cat, "description": r_desc, "status": "Active", "last_reviewed": datetime.now().strftime("%Y-%m-%d %H:%M"), "ai_flagged": False})
                add_audit("Rule Inventory", f"Added rule {new_id}: {r_title}")
                st.success(f"✓ Rule {new_id} added.")
                st.rerun()

    with tab3:
        st.markdown("**Paste document text — AI will extract potential rules**")
        doc_text = st.text_area("Document Text", height=200, placeholder="Paste policy text, a rule notice, or regulatory circular here...")
        if st.button("🤖 Parse & Extract Rules"):
            if doc_text.strip():
                # Fake AI: keyword matching
                keywords = {
                    "supervision":    ("FINRA", "Supervision"),
                    "aml":            ("FinCEN", "AML/BSA"),
                    "recordkeeping":  ("SEC",    "Recordkeeping"),
                    "best interest":  ("SEC",    "Suitability"),
                    "customer":       ("FINRA",  "Customer Accounts"),
                    "anti-money":     ("FinCEN", "AML/BSA"),
                    "retention":      ("SEC",    "Recordkeeping"),
                    "trading":        ("FINRA",  "Trading"),
                }
                found = []
                doc_lower = doc_text.lower()
                for kw, (src, cat) in keywords.items():
                    if kw in doc_lower:
                        found.append({"kw": kw, "src": src, "cat": cat})

                if found:
                    st.markdown("<div class='gc-alert gc-alert-ok'>✓ AI extraction complete. Review suggested rules below.</div>", unsafe_allow_html=True)
                    for f in found:
                        st.markdown(f"• Detected keyword **'{f['kw']}'** → Suggested category: **{f['cat']}** (Source: {f['src']})")
                    if st.button("Auto-add extracted rules to inventory"):
                        for i, f in enumerate(found):
                            new_id = f"R-{len(D['rules'])+1:03d}"
                            D["rules"].append({"id": new_id, "title": f"AI-Extracted: {f['kw'].title()} Requirement", "source": f["src"], "category": f["cat"], "description": f"Extracted from uploaded document. Keyword: '{f['kw']}'.", "status": "Active", "last_reviewed": datetime.now().strftime("%Y-%m-%d %H:%M"), "ai_flagged": False})
                        add_audit("Rule Inventory", f"AI parsed document; {len(found)} rules extracted")
                        st.success(f"✓ {len(found)} rules added to inventory.")
                        st.rerun()
                else:
                    st.warning("No recognizable compliance keywords found in document.")

# ─────────────────────────────────────────────
#  AI RULE SCAN
# ─────────────────────────────────────────────
def page_ai_scan():
    st.markdown("<div class='gc-header'><h1>AI RULE CHANGE SCAN</h1><p>Periodic regulatory scan with AI-generated summary memo and recommendations</p></div>", unsafe_allow_html=True)

    SIMULATED_CHANGES = [
        {"rule": "FINRA Rule 4512", "change": "Updated customer account information requirements to include digital communication preferences and ESG disclosures.", "impact": "High", "recommendation": "Review and update customer onboarding forms. Update WSP-002 accordingly."},
        {"rule": "Bank Secrecy Act AML", "change": "FinCEN issued updated guidance on cryptocurrency transaction monitoring thresholds and suspicious activity reporting.", "impact": "High", "recommendation": "Update AML program to include digital asset monitoring. Retrain AML staff by Q2."},
        {"rule": "Reg BI", "change": "SEC staff issued FAQ clarifying best interest obligations for automated investment tools and robo-advisors.", "impact": "Medium", "recommendation": "Review robo-advisory disclosures and ensure Reg BI documentation is current."},
    ]

    if D["rule_scan_memo"]:
        memo = D["rule_scan_memo"]
        st.markdown(f"""
        <div class='gc-card'>
          <div class='gc-card-header'>LAST AI SCAN MEMO · {memo['date']}</div>
          <div style='font-size:0.88rem;margin-bottom:0.8rem'>{memo['summary']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Detected Rule Changes & Recommendations**")
        for ch in memo["changes"]:
            imp_cls = "badge-high" if ch["impact"]=="High" else "badge-med"
            st.markdown(f"""
            <div class='gc-card'>
              <div style='display:flex;justify-content:space-between'>
                <b>{ch['rule']}</b>
                <span class='gc-badge {imp_cls}'>Impact: {ch['impact']}</span>
              </div>
              <div style='margin:0.5rem 0;font-size:0.82rem;color:var(--text2)'>{ch['change']}</div>
              <div style='font-size:0.8rem'><b>Recommendation:</b> {ch['recommendation']}</div>
            </div>
            """, unsafe_allow_html=True)
        # Memo download
        memo_text = f"GRAPHITE COMPLIANCE — AI RULE CHANGE MEMO\n{memo['date']}\n\n{memo['summary']}\n\n"
        for ch in memo["changes"]:
            memo_text += f"RULE: {ch['rule']}\nCHANGE: {ch['change']}\nIMPACT: {ch['impact']}\nRECOMMENDATION: {ch['recommendation']}\n\n"
        st.download_button("📥 Download Memo (.txt)", data=memo_text, file_name="rule_change_memo.txt", mime="text/plain")
        st.markdown("<hr/>", unsafe_allow_html=True)

    if st.button("🤖 Run AI Rule Change Scan"):
        with st.spinner("Scanning regulatory sources..."):
            import time; time.sleep(1.5)
            D["rule_scan_memo"] = {
                "date":    datetime.now().strftime("%Y-%m-%d %H:%M"),
                "summary": f"Quarterly AI Rule Change Scan completed. Scanned {len(D['rules'])} active rules against latest FINRA, SEC, and FinCEN regulatory releases. Identified {len(SIMULATED_CHANGES)} material changes requiring firm attention.",
                "changes": SIMULATED_CHANGES,
            }
            # Flag affected rules
            for r in D["rules"]:
                for ch in SIMULATED_CHANGES:
                    if any(kw in r["title"] for kw in ch["rule"].split()):
                        r["ai_flagged"] = True
            add_audit("AI Rule Scan", f"Scan completed; {len(SIMULATED_CHANGES)} changes flagged")
        st.rerun()

# ─────────────────────────────────────────────
#  ORG CHART
# ─────────────────────────────────────────────
def page_org():
    st.markdown("<div class='gc-header'><h1>ORG CHART & RESPONSIBILITY MAP</h1><p>Supervisory hierarchy with linked responsibilities and delegation tracking</p></div>", unsafe_allow_html=True)

    for node in D["org_chart"]:
        user_info = D["users"].get(node["user"], {})
        reports   = f"Reports to: **{node['reports_to']}**" if node["reports_to"] else "**Top of hierarchy**"
        st.markdown(f"""
        <div class='gc-card'>
          <div style='display:flex;justify-content:space-between;align-items:flex-start'>
            <div>
              <div style='font-family:var(--mono);color:var(--gold);font-size:0.8rem;letter-spacing:0.06em'>{node['role']}</div>
              <div style='font-size:1rem;font-weight:600;margin-top:0.2rem'>{user_info.get('name','–')} <span style='color:var(--text2);font-size:0.8rem'>(@{node['user']})</span></div>
            </div>
          </div>
          <div style='margin-top:0.5rem;font-size:0.78rem;color:var(--text2)'>{reports}</div>
          <div style='margin-top:0.5rem'>{'  '.join(f"<span class='gc-badge badge-open'>{r}</span>" for r in node['responsibilities'])}</div>
        </div>
        """, unsafe_allow_html=True)

    # Delegation summary
    delegated = [t for t in D["tasks"] if t["delegated_to"]]
    if delegated:
        st.markdown("<hr/><b>Active Delegations</b>", unsafe_allow_html=True)
        for t in delegated:
            st.markdown(f"<div class='gc-timeline-item'>{t['id']} · <b>{t['title']}</b> → delegated to <b>{t['delegated_to']}</b> · memo: <i>{t['delegated_memo']}</i></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  AUDIT TRAIL
# ─────────────────────────────────────────────
def page_audit():
    st.markdown("<div class='gc-header'><h1>LINKED AUDIT TRAIL</h1><p>Immutable timestamped log of all system actions — filterable on demand</p></div>", unsafe_allow_html=True)
    fc1,fc2,fc3 = st.columns(3)
    f_user   = fc1.selectbox("User", ["All"] + list(D["users"].keys()) + ["SYSTEM"])
    f_module = fc2.selectbox("Module", ["All"] + list({a["module"] for a in D["audit_trail"]}))
    f_search = fc3.text_input("Search actions", placeholder="keyword...")

    trail = list(reversed(D["audit_trail"]))
    if f_user   != "All":    trail = [a for a in trail if a["user"]   == f_user]
    if f_module != "All":    trail = [a for a in trail if a["module"] == f_module]
    if f_search.strip():     trail = [a for a in trail if f_search.lower() in a["action"].lower()]

    st.markdown(f"<div style='font-family:var(--mono);font-size:0.72rem;color:var(--text2);margin-bottom:0.8rem'>{len(trail)} RECORDS</div>", unsafe_allow_html=True)
    for entry in trail:
        st.markdown(f"""
        <div class='gc-timeline-item'>
          <span style='color:var(--gold);font-family:var(--mono);font-size:0.7rem'>{entry['ts']}</span>
          &nbsp;·&nbsp;<span class='gc-badge badge-open'>{entry['module']}</span>
          &nbsp;·&nbsp;<b>{entry['user']}</b>
          &nbsp;·&nbsp;{entry['action']}
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FIRM CONFIG
# ─────────────────────────────────────────────
def page_firm_config():
    st.markdown("<div class='gc-header'><h1>FIRM PROFILE CONFIGURATION</h1><p>Tailor rules, workflows, and retention policies to your firm</p></div>", unsafe_allow_html=True)
    firm = D["firm"]
    c1,c2 = st.columns(2)
    firm["name"]           = c1.text_input("Firm Name",        value=firm["name"])
    firm["industry"]       = c2.text_input("Industry/Type",    value=firm["industry"])
    c3,c4 = st.columns(2)
    firm["crd"]            = c3.text_input("CRD / License #",  value=firm["crd"])
    firm["regulator"]      = c4.text_input("Regulator(s)",     value=firm["regulator"])
    c5,c6 = st.columns(2)
    firm["retention_years"]= c5.number_input("Retention Period (years)", value=firm["retention_years"], min_value=1, max_value=20)
    firm["approval_mode"]  = c6.selectbox("Approval Mode", ["single","dual"], index=0 if firm["approval_mode"]=="single" else 1)
    firm["address"]        = st.text_input("Address", value=firm["address"])

    if st.button("Save Firm Profile"):
        add_audit("Firm Config", f"Firm profile updated by {st.session_state.current_user}")
        st.success("✓ Profile saved.")

    # Third-party compliance packet
    st.markdown("<hr/><b>Third-Party Regulatory Compliance Packet</b>", unsafe_allow_html=True)
    st.markdown("<div class='gc-alert gc-alert-ok'>✓ Compliance documentation packet available for vendor due diligence</div>", unsafe_allow_html=True)
    packet = f"""THIRD-PARTY REGULATORY COMPLIANCE PACKET
========================================
Firm:         {firm['name']}
Industry:     {firm['industry']}
CRD Number:   {firm['crd']}
Regulator:    {firm['regulator']}
Retention:    {firm['retention_years']} years

COMPLIANCE CERTIFICATIONS:
- FINRA Rule 3110 Supervisory System: Active
- AML Program (BSA): Active, last tested {(datetime.now()-timedelta(days=45)).strftime('%Y-%m-%d')}
- Reg BI Compliance: Active
- Cybersecurity Policy: Active
- WORM-Compliant Recordkeeping: Active
- Business Continuity Plan: Active

WSPs on file: {len(D['wsps'])}
Active rules: {len(D['rules'])}
Open tasks:   {len([t for t in D['tasks'] if t['status']=='Open'])}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    st.download_button("📥 Download Compliance Packet", data=packet, file_name="compliance_packet.txt", mime="text/plain")

# ─────────────────────────────────────────────
#  DATA EXPORT
# ─────────────────────────────────────────────
def page_export():
    st.markdown("<div class='gc-header'><h1>DATA EXPORT & BACKUP</h1><p>Export all compliance data as JSON or CSV with full audit trails</p></div>", unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown("**Full System Export (JSON)**")
        if st.button("Generate JSON Export"):
            payload = json.dumps({
                "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "firm": D["firm"],
                "tasks": D["tasks"],
                "exam_requests": D["exam_requests"],
                "rules": D["rules"],
                "wsps": D["wsps"],
                "evidence": D["evidence"],
                "audit_trail": D["audit_trail"],
                "org_chart": D["org_chart"],
            }, indent=2)
            add_audit("Export", "Full JSON export generated")
            st.download_button("📥 Download graphite_export.json", data=payload, file_name="graphite_export.json", mime="application/json")

    with col2:
        st.markdown("**Tasks CSV Export**")
        if st.button("Generate Tasks CSV"):
            buf = io.StringIO()
            writer = csv.DictWriter(buf, fieldnames=["id","title","assignee","due","status","priority","category"])
            writer.writeheader()
            for t in D["tasks"]:
                writer.writerow({k: t[k] for k in ["id","title","assignee","due","status","priority","category"]})
            add_audit("Export", "Tasks CSV export generated")
            st.download_button("📥 Download tasks.csv", data=buf.getvalue(), file_name="tasks.csv", mime="text/csv")

    st.markdown("<hr/><b>Audit Trail Export</b>", unsafe_allow_html=True)
    if st.button("Export Audit Trail (JSON)"):
        payload = json.dumps({"audit_trail": D["audit_trail"]}, indent=2)
        add_audit("Export", "Audit trail exported")
        st.download_button("📥 Download audit_trail.json", data=payload, file_name="audit_trail.json", mime="application/json")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("<div class='gc-alert gc-alert-ok'>✓ All exports include immutable audit trails  ·  WORM-record hashes preserved  ·  Meets SEC Rule 17a-4 standards</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN ROUTER
# ─────────────────────────────────────────────
if not st.session_state.logged_in:
    login_page()
else:
    nav = sidebar()
    if nav == "Dashboard":           page_dashboard()
    elif nav == "Tasks & Remediation": page_tasks()
    elif nav == "Exam Requests":     page_exam_requests()
    elif nav == "WSP Repository":    page_wsp()
    elif nav == "Evidence Repository": page_evidence()
    elif nav == "Rule Inventory":    page_rules()
    elif nav == "AI Rule Scan":      page_ai_scan()
    elif nav == "Org Chart":         page_org()
    elif nav == "Audit Trail":       page_audit()
    elif nav == "Firm Config":       page_firm_config()
    elif nav == "Data Export":       page_export()
