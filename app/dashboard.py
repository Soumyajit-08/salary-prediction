import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from app.users import verify_user, register_user, load_users, change_password

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Salary AI · Enterprise Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://localhost:8000/predict"

# ─── Load Data ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'salary_data.csv')
    data = pd.read_csv(data_path)
    data.columns = data.columns.str.strip()
    return data

df = load_data()

# ─── Custom Styles ────────────────────────────────────────────────────────────
def apply_styles():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    :root {
        --primary: #8b5cf6;
        --secondary: #06b6d4;
        --dark-bg: #030712;
        --card-bg: rgba(17, 24, 39, 0.7);
        --glass-border: rgba(255, 255, 255, 0.1);
    }

    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b, #030712) !important;
        font-family: 'Outfit', sans-serif !important;
    }

    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    .glass-card:hover {
        border-color: var(--primary);
        transform: translateY(-5px);
    }

    .stat-metric {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.1));
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid var(--glass-border);
    }

    h1, h2, h3 {
        background: linear-gradient(to right, #fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }

    .stButton > button {
        border-radius: 12px !important;
        background: linear-gradient(90deg, #8b5cf6, #6366f1) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
    }

    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5) !important;
        transform: scale(1.02);
    }
</style>
    """, unsafe_allow_html=True)

# ─── Auth Logic ───────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_ui():
    apply_styles()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.title("💎 Enterprise Auth")
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            if st.button("Access Dashboard", use_container_width=True):
                if verify_user(user, pwd):
                    st.session_state.logged_in = True
                    st.session_state.username = user
                    st.rerun()
                else:
                    st.error("Invalid Credentials")
        
        with tab2:
            n_user = st.text_input("New Username")
            n_pwd = st.text_input("New Password", type="password")
            if st.button("Create Account", use_container_width=True):
                success, msg = register_user(n_user, n_pwd)
                if success: st.success(msg)
                else: st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)

# ─── Main App ─────────────────────────────────────────────────────────────────
def main_ui():
    apply_styles()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👑 Professional Access")
        st.info(f"User: {st.session_state.username}")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Model Info")
        st.write("Model: **Ridge Regression (Pipeline)**")
        st.write("Precision: **High (R2: 0.977)**")
        st.write("Status: **Healthy**")

    # Hero
    st.title("🚀 Salary Intelligence Dashboard")
    st.markdown("Advanced AI-driven compensation analysis for professionals.")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🎯 Prediction Engine")
        exp = st.slider("Years of Experience", 0, 20, 5)
        edu = st.selectbox("Education Level", ["Graduate", "Postgraduate", "PhD"])
        role = st.selectbox("Job Role", sorted(df['Role'].unique()))
        loc = st.selectbox("Location", sorted(df['Location'].unique()))
        
        if st.button("Generate Prediction", use_container_width=True):
            try:
                payload = {
                    "Experience": float(exp),
                    "Education": edu,
                    "Role": role,
                    "Location": loc
                }
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    salary = response.json()['predicted_salary']
                    st.session_state.prediction = salary
                else:
                    st.error("API Connection Error")
            except Exception as e:
                st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 Market Results")
        if "prediction" in st.session_state:
            val = st.session_state.prediction
            st.markdown(f"""
                <div style="text-align:center; padding: 1rem;">
                    <p style="color: #94a3b8; margin-bottom: 0;">Estimated Annual Salary</p>
                    <h2 style="font-size: 3.5rem; margin-top: 0;">₹ {val:,.0f}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Comparison Metrics
            avg = df['Salary'].mean()
            diff = val - avg
            
            m1, m2 = st.columns(2)
            with m1:
                st.markdown(f"""
                    <div class="stat-metric">
                        <small>Vs Market Avg</small><br>
                        <strong style="color: {'#10b981' if diff > 0 else '#ef4444'}; font-size: 1.2rem;">
                            {'+' if diff > 0 else ''}{diff:,.0f}
                        </strong>
                    </div>
                """, unsafe_allow_html=True)
            with m2:
                perc = (df['Salary'] < val).mean() * 100
                st.markdown(f"""
                    <div class="stat-metric">
                        <small>Percentile</small><br>
                        <strong style="color: #8b5cf6; font-size: 1.2rem;">{perc:.1f}%</strong>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="text-align:center; padding: 3rem; opacity: 0.5;">
                    <p>Enter details and click Predict to see results</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Analytics Section
    st.markdown("### 📈 Market Intelligence")
    
    fig2 = px.bar(df.groupby('Location')['Salary'].mean().reset_index(), 
                  x="Location", y="Salary", color="Salary",
                  title="Average Salary by Location",
                  template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

# ─── Router ───────────────────────────────────────────────────────────────────
if st.session_state.logged_in:
    main_ui()
else:
    login_ui()
