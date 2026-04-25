import streamlit as st
import pickle
import os
import pandas as pd
# (Import moved below to ensure st.set_page_config runs first)

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Salary Predictor · AI-Powered",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

from users import verify_user, register_user, delete_user, load_users, change_password
base_dir = os.path.dirname(__file__)

model_path = os.path.join(base_dir, '../model/model.pkl')

# ─── Session State ────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    
    st.session_state.role = "user"

# ─── Load Model & Columns ────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'model', 'model.pkl')
columns_path = os.path.join(BASE_DIR, 'model', 'columns.pkl')
data_path = os.path.join(BASE_DIR, 'data', 'salary_data.csv')

@st.cache_resource
def load_model():
    m = pickle.load(open(model_path, 'rb'))
    c = pickle.load(open(columns_path, 'rb'))
    return m, c

@st.cache_data
def load_data():
    data = pd.read_csv(data_path)
    data.columns = data.columns.str.strip()
    return data

# ─── Custom CSS ───────────────────────────────────────────────────────────────
def local_css():
    st.markdown("""
<style>
    /* ── Import Google Font ─────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Root Variables ─────────────────────────────────────────── */
    :root {
        --bg-primary: #0a0a0a;
        --bg-secondary: #0f0f0f;
        --bg-card: rgba(15, 15, 15, 0.7);
        --bg-card-hover: rgba(20, 20, 20, 0.85);
        --border-card: rgba(124, 58, 237, 0.15);
        --border-glow: rgba(124, 58, 237, 0.4);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-violet: #7c3aed;
        --accent-deep: #5b21b6;
        --accent-glow: #a78bfa;
        --gradient-main: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%);
        --gradient-warm: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
        --gradient-cool: linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%);
        --shadow-glow: 0 0 45px rgba(124, 58, 237, 0.25);
        --shadow-card: 0 30px 70px rgba(0, 0, 0, 0.95);
    }

    /* ── Global Styles ──────────────────────────────────────────── */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stApp > header {
        background: transparent !important;
    }

    /* ── Sidebar ────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050505 0%, #11081a 100%) !important;
        border-right: 1px solid var(--border-card) !important;
    }

    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-primary) !important;
    }

    /* ── Main Container Padding ─────────────────────────────────── */
    .block-container {
        padding-top: 2rem !important;
        max-width: 1200px !important;
    }

    /* ── Hero Title ─────────────────────────────────────────────── */
    .hero-title {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }

    .hero-title h1 {
        font-family: 'Inter', sans-serif !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: var(--gradient-main);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.03em;
        margin-bottom: 0 !important;
        line-height: 1.1 !important;
        text-shadow: 0 20px 40px rgba(0, 0, 0, 0.8);
    }

    .hero-subtitle {
        text-align: center;
        color: var(--text-secondary) !important;
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 0.5rem;
        margin-bottom: 2rem;
        letter-spacing: 0.02em;
    }

    .gradient-line {
        height: 3px;
        width: 120px;
        margin: 0.75rem auto 0 auto;
        background: var(--gradient-main);
        border-radius: 4px;
    }

    /* ── Glass Card ──────────────────────────────────────────────── */
    .glass-card {
        background: var(--bg-card) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border-card);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9), inset 0 0 30px rgba(0, 0, 0, 0.6);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: var(--border-glow);
        box-shadow: var(--shadow-glow), 0 30px 80px rgba(0, 0, 0, 1);
        transform: translateY(-2px);
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .card-header-icon {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }

    .card-header-text {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
    }

    /* ── Prediction Result ──────────────────────────────────────── */
    .result-container {
        text-align: center;
        padding: 2rem 1rem;
    }

    .result-label {
        font-size: 0.95rem;
        font-weight: 500;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.75rem;
    }

    .result-salary {
        font-family: 'Inter', sans-serif !important;
        font-size: 3.2rem;
        font-weight: 900;
        background: var(--gradient-cool);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
        margin-bottom: 0.5rem;
        text-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
    }

    .result-subtitle {
        font-size: 0.85rem;
        color: var(--text-muted);
        font-weight: 400;
    }

    /* ── Stat Pill ───────────────────────────────────────────────── */
    .stat-row {
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .stat-pill {
        flex: 1;
        background: rgba(124, 58, 237, 0.1);
        border: 1px solid rgba(124, 58, 237, 0.15);
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stat-pill:hover {
        background: rgba(124, 58, 237, 0.18);
        border-color: rgba(124, 58, 237, 0.35);
        transform: translateY(-2px);
    }

    .stat-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.2;
    }

    .stat-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.25rem;
    }

    /* ── Input Styling ──────────────────────────────────────────── */
    .stSlider > div > div > div > div {
        background: var(--gradient-main) !important;
    }

    .stSlider label, .stSelectbox label, .stNumberInput label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.02em !important;
    }

    div[data-baseweb="select"] > div {
        background: rgba(20, 20, 20, 0.8) !important;
        border-color: rgba(124, 58, 237, 0.25) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }

    .stNumberInput input {
        background: rgba(20, 20, 20, 0.8) !important;
        border-color: rgba(124, 58, 237, 0.25) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }

    /* ── Button ─────────────────────────────────────────────────── */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.85rem 2rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4) !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(124, 58, 237, 0.6), 0 0 0 4px rgba(0,0,0,0.3) !important;
        background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%) !important;
    }

    /* ── Tabs ───────────────────────────────────────────────────── */
    .stTabs [aria-selected="true"] {
        background: rgba(124, 58, 237, 0.1) !important;
        color: var(--accent-violet) !important;
    }

    /* ── Scrollbar ──────────────────────────────────────────────── */
    ::-webkit-scrollbar-thumb {
        background: rgba(124, 58, 237, 0.35);
        border-radius: 10px;
    }

    /* ── Footer ─────────────────────────────────────────────────── */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: var(--text-muted);
        font-size: 0.8rem;
    }

    /* ── Mobile Responsiveness ───────────────────────────────────── */
    @media (max-width: 768px) {
        .hero-title h1 { font-size: 1.8rem !important; }
        .result-salary { font-size: 2.2rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ─── Login Screen ─────────────────────────────────────────────────────────────
def login_screen():
    local_css()
    
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # Hero Background & Alignment
    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card animate-fade-in">', unsafe_allow_html=True)
        
        if st.session_state.auth_mode == "login":
            st.markdown("""
            <div style="text-align:center; margin-bottom: 1.5rem;">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🔐</div>
                <h1 style="color:white; font-size: 2rem; margin-bottom: 0.5rem;">Salary Predictor</h1>
                <p style="color:#94a3b8; font-size: 0.9rem;">Sign in to access your AI Dashboard</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="Enter username")
                password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
                submit = st.form_submit_button("Sign In to Dashboard", use_container_width=True)
                
                if submit:
                    if verify_user(username, password):
                        st.session_state.logged_in = True
                        st.success("Access Granted! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")
            
            st.markdown("<div style='text-align:center; margin-top:1rem;'>", unsafe_allow_html=True)
            if st.button("New here? Create an account", key="go_to_signup"):
                st.session_state.auth_mode = "signup"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="text-align:center; margin-bottom: 1.5rem;">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">📝</div>
                <h1 style="color:white; font-size: 2rem; margin-bottom: 0.5rem;">Join the Platform</h1>
                <p style="color:#94a3b8; font-size: 0.9rem;">Start your professional AI journey</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("signup_form"):
                new_user = st.text_input("👤 New Username", placeholder="Choose a username")
                new_pass = st.text_input("🔑 New Password", type="password", placeholder="Choose a password")
                confirm_pass = st.text_input("🛡️ Confirm Password", type="password", placeholder="Repeat password")
                signup_submit = st.form_submit_button("Create My Account", use_container_width=True)
                
                if signup_submit:
                    if not new_user or not new_pass:
                        st.error("All fields are required!")
                    elif new_pass != confirm_pass:
                        st.error("Passwords do not match!")
                    elif len(new_pass) < 4:
                        st.error("Password must be at least 4 characters.")
                    else:
                        success, res = register_user(new_user, new_pass)
                        if success:
                            st.success(f"🎊 {res}")
                        else:
                            st.error(f"⚠️ {res}")
            
            st.markdown("<div style='text-align:center; margin-top:1rem;'>", unsafe_allow_html=True)
            if st.button("Already have an account? Log in", key="go_to_login"):
                st.session_state.auth_mode = "login"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ─── Main App ─────────────────────────────────────────────────────────────────
def main_app():
    local_css()
    
    model, columns = load_model()
    df = load_data()
    
    # ─── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 1rem 0;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">💰</div>
            <h2 style="margin: 0; font-size: 1.3rem; font-weight: 700;">Salary Predictor</h2>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.8rem; color: #64748b;">AI-Powered Insights</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align:center; padding: 0.5rem; background: rgba(124, 58, 237, 0.1); border-radius: 10px; margin-bottom: 1rem;">
            <p style="margin:0; font-size: 0.8rem; color: #a78bfa; font-weight: 600;">
                {"👑 ADMIN ACCESS" if st.session_state.role == "admin" else "👤 USER ACCESS"}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

        st.markdown("---")
        with st.expander("⚙️ Account Settings"):
            st.markdown(f"**User**: {st.session_state.get('username', 'Guest')}")
            with st.form("change_pwd_form"):
                new_pwd = st.text_input("New Password", type="password")
                if st.form_submit_button("Update Password"):
                    if len(new_pwd) >= 4:
                        success, msg = change_password(st.session_state.username, new_pwd)
                        if success: st.success(msg)
                        else: st.error(msg)
                    else: st.error("Too short!")

        st.markdown("---")
        st.markdown("### 📊 About")
        st.markdown("""
        This tool uses a **Random Forest** machine learning model trained on salary data.
        """)

        st.markdown("---")
        st.markdown("### 📈 Model Stats")
        total_samples = len(df)
        avg_salary = df['Salary'].mean()
        max_salary = df['Salary'].max()
        st.metric("Training Samples", f"{total_samples}")
        st.metric("Avg Salary", f"₹{avg_salary:,.0f}")
        st.metric("Max Salary", f"₹{max_salary:,.0f}")

    # ─── Hero Section ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-title animate-fade-in">
        <h1>💰 Salary Predictor</h1>
        <div class="gradient-line"></div>
    </div>
    <p class="hero-subtitle animate-fade-in">
        Predict salaries with AI · Powered by Machine Learning
    </p>
    """, unsafe_allow_html=True)

    # ─── Main Layout ──────────────────────────────────────────────────────────
    col_input, col_spacer, col_result = st.columns([5, 0.5, 5])

    with col_input:
        st.markdown("""
        <div class="glass-card animate-fade-in">
            <div class="card-header">
                <div class="card-header-icon" style="background: rgba(124,58,237,0.15);">🎯</div>
                <span class="card-header-text">Enter Details</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        experience = st.slider("⏳ Years of Experience", 0, 15, 3, 1)
        education = st.selectbox("🎓 Education Level", ["Graduate", "Postgraduate", "PhD"])
        role = st.selectbox("💼 Job Role", ["Software Engineer", "Data Analyst", "Data Scientist"])
        location = st.selectbox("📍 Location", ["Kolkata", "Delhi", "Bangalore", "Hyderabad", "Mumbai", "Pune"])
        
        st.markdown("<div style='height: 0.75rem'></div>", unsafe_allow_html=True)
        predict_clicked = st.button("🚀 Predict Salary", use_container_width=True)

    with col_result:
        st.markdown("""
        <div class="glass-card animate-fade-in">
            <div class="card-header">
                <div class="card-header-icon" style="background: rgba(109,40,217,0.15);">📊</div>
                <span class="card-header-text">Prediction Result</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if predict_clicked:
            input_data = pd.DataFrame({
                "Experience": [experience],
                "Education": [education],
                "Role": [role],
                "Location": [location],
            })
            input_encoded = pd.get_dummies(input_data).reindex(columns=columns, fill_value=0)
            prediction = model.predict(input_encoded)[0]
            
            st.markdown(f"""
            <div class="result-container animate-fade-in">
                <div class="result-label">Estimated Annual Salary</div>
                <div class="result-salary">₹ {prediction:,.0f}</div>
                <div class="result-subtitle">Based on your profile & market data</div>
            </div>
            """, unsafe_allow_html=True)

            percentile = (df['Salary'] < prediction).mean() * 100
            st.markdown(f"""
            <div class="stat-row animate-fade-in">
                <div class="stat-pill">
                    <div class="stat-value">{experience}</div>
                    <div class="stat-label">Yrs Exp</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-value">{percentile:.0f}%</div>
                    <div class="stat-label">Percentile</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-value">₹{prediction - avg_salary:+,.0f}</div>
                    <div class="stat-label">vs Average</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ─── Smart Suggestions ───
            st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)
            st.markdown("### 💡 AI Insights")
            
            suggestions = [
                ("🎓", "Education Boost", "Completing a Postgraduate degree could increase your projected salary by ~18%.", education == "Graduate"),
                ("📜", "Certification", "Obtaining niche certifications could accelerate your progression to a Senior role.", experience < 5),
                ("📍", "Market Shift", "Moving to Bangalore or Mumbai could potentially increase your market value by ~12%.", location in ["Kolkata", "Delhi"])
            ]
            
            for icon, title, text, condition in suggestions:
                if condition:
                    st.markdown(f"""
                    <div style="background: rgba(124, 58, 237, 0.08); padding: 1rem; border-left: 4px solid var(--accent-violet); border-radius: 8px; margin-bottom: 0.75rem;">
                        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                        <strong style="color: var(--text-primary);">{title}</strong><br>
                        <span style="color: var(--text-secondary); font-size: 0.85rem;">{text}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            # ─── Download Report ───
            st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
            user_name = st.session_state.get('username', 'Guest')
            report_text = f"""
            SALARY PREDICTION REPORT
            =======================
            Generated for: {user_name}
            -----------------------
            Role: {role}
            Experience: {experience} years
            Education: {education}
            Location: {location}
            -----------------------
            ESTIMATED SALARY: ₹ {prediction:,.0f}
            Percentile: {percentile:.1f}%
            vs Market Average: ₹{prediction - avg_salary:+,.0f}
            -----------------------
            Generated on: Professional AI Platform v2.0
            """
            
            st.download_button(
                label="📥 Download My Prediction Report",
                data=report_text,
                file_name=f"salary_report_{user_name}_{role.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.markdown("""
            <div class="result-container">
                <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.3;">🎯</div>
                <div class="result-label">Ready to Predict</div>
            </div>
            """, unsafe_allow_html=True)

    # ─── Dataset Preview ─────────────────────────────────────────────────────────
    st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

    with st.expander("📋 View Training Dataset", expanded=False):
        st.dataframe(
            df.style.format({'Salary': '₹{:,.0f}'}),
            use_container_width=True,
            hide_index=True,
        )

    # ─── Admin Control Tower ──────────────────────────────────────────────────────
    if st.session_state.role == "admin":
        st.markdown("<div style='height: 2.5rem'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card-header animate-fade-in" style="justify-content: center;">
            <div class="card-header-icon" style="background: rgba(124,58,237,0.15);">⚙️</div>
            <span class="card-header-text">Admin Control Tower</span>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="glass-card animate-fade-in">', unsafe_allow_html=True)
            
            adm_col_users, adm_col_data = st.columns(2)
            
            with adm_col_users:
                st.markdown("### 👥 User Registry")
                all_users = load_users()
                for uname, udata in all_users.items():
                    u_col, d_col = st.columns([3, 1])
                    u_col.markdown(f"- **{uname}** ({'👑' if udata['role'] == 'admin' else '👤'})")
                    if uname != "admin":
                        if d_col.button("🗑️", key=f"del_{uname}"):
                            success, msg = delete_user(uname)
                            if success:
                                st.toast(msg, icon="🗑️")
                                st.rerun()
                            else:
                                st.error(msg)
                
                if st.button("➕ Add New User"):
                    st.toast("Opening user creator...", icon="👤")
            
            with adm_col_data:
                st.markdown("### 💾 Data Ops")
                st.download_button(
                    label="📥 Export Salary Data (CSV)",
                    data=df.to_csv(index=False),
                    file_name="salary_export_admin.csv",
                    mime="text/csv",
                )
                if st.button("🗑️ Clear Cache"):
                    st.cache_data.clear()
                    st.cache_resource.clear()
                    st.toast("System cache cleared!")

            st.markdown('</div>', unsafe_allow_html=True)

    # ─── Insights Section ─────────────────────────────────────────────────────
    st.markdown("<div style='height: 2.5rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card-header animate-fade-in" style="justify-content: center;">
        <div class="card-header-icon" style="background: rgba(236,72,153,0.15);">🌐</div>
        <span class="card-header-text">Market Intelligence</span>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Experience", "🎓 Education", "📍 Location", "🥧 Role Distribution"])

    with tab1:
        st.bar_chart(df.groupby('Experience')['Salary'].mean(), color='#8b5cf6')
    with tab2:
        st.bar_chart(df.groupby('Education')['Salary'].mean(), color='#06b6d4')
    with tab3:
        st.bar_chart(df.groupby('Location')['Salary'].mean(), color='#10b981')
    with tab4:
        # Role distribution using bar_chart for compatibility
        role_counts = df['Role'].value_counts()
        st.write("Market Demand (Job Role Distribution)")
        st.bar_chart(role_counts, color='#ec4899')

    # ─── Footer ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="footer">
        ⚡ Salary Predictor v2.0 · Powered by Random Forest ML Model
    </div>
    """, unsafe_allow_html=True)

# ─── App Logic ────────────────────────────────────────────────────────────────
try:
    if st.session_state.logged_in:
        main_app()
    else:
        login_screen()
except Exception as e:
    st.error(f"⚠️ Startup Error: {e}")
    st.info("Check if your model and data files are in the right folders.")