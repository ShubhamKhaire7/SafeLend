import streamlit as st
import json
import io
import pandas as pd
import plotly.express as px
import math
from prediction_helper import predict, explain_from_inputs, predict_batch, batch_template

# Page configuration
st.set_page_config(
    page_title="SafeLend",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        /* Modern Design System */
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --success-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
            --warning-gradient: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            --danger-gradient: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --card-shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --border-radius: 16px;
            --border-radius-lg: 20px;
            --spacing-xs: 0.5rem;
            --spacing-sm: 0.75rem;
            --spacing-md: 1rem;
            --spacing-lg: 1.5rem;
            --spacing-xl: 2rem;
        }
        
        /* Header Styling */
        .sl-header {
            padding: var(--spacing-lg) var(--spacing-xl);
            background: var(--primary-gradient);
            color: white;
            border-radius: var(--border-radius-lg);
            box-shadow: var(--card-shadow-lg);
            margin-bottom: var(--spacing-xl);
            position: relative;
            overflow: hidden;
        }
        
        .sl-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="%23ffffff" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.3;
            pointer-events: none;
        }
        
        .sl-brand {
            display: flex;
            align-items: center;
            gap: var(--spacing-md);
            position: relative;
            z-index: 1;
        }
        
        .sl-badge {
            font-weight: 800;
            font-size: 1.25rem;
            padding: var(--spacing-sm) var(--spacing-md);
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            width: 60px;
            height: 60px;
        }
        
        .sl-title {
            margin: 0;
            font-weight: 900;
            letter-spacing: -0.025em;
            font-size: 2.5rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            background: linear-gradient(45deg, #ffffff, #f1f5f9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .sl-subtitle {
            margin: var(--spacing-xs) 0 0;
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1rem;
            font-weight: 500;
            position: relative;
            z-index: 1;
        }
        
        /* Card Components */
        .sl-card {
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--card-shadow);
            border: 1px solid rgba(226, 232, 240, 0.8);
            overflow: hidden;
            transition: all 0.2s ease;
        }
        
        .sl-card:hover {
            box-shadow: var(--card-shadow-lg);
            transform: translateY(-2px);
        }
        
        .sl-card-header {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: var(--spacing-md) var(--spacing-lg);
            font-weight: 700;
            font-size: 1.1rem;
            color: #334155;
            border-bottom: 1px solid rgba(226, 232, 240, 0.8);
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
        }
        
        /* Insight Cards */
        .insight-card {
            padding: var(--spacing-md);
            border-radius: var(--border-radius);
            margin-bottom: var(--spacing-sm);
            border-left: 4px solid;
            font-weight: 500;
            line-height: 1.5;
            box-shadow: var(--card-shadow);
        }
        
        .insight-card.success {
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
            border-left-color: #10b981;
            color: #065f46;
        }
        
        .insight-card.warning {
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
            border-left-color: #f59e0b;
            color: #92400e;
        }
        
        .insight-card.danger {
            background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
            border-left-color: #ef4444;
            color: #991b1b;
        }
        
        /* Form Styling */
        .stForm {
            background: white;
            border-radius: var(--border-radius-lg);
            box-shadow: var(--card-shadow);
            border: 1px solid rgba(226, 232, 240, 0.8);
            padding: 0;
        }
        
        .stForm > div {
            padding: var(--spacing-xl);
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        }
        
        /* Metrics Enhancement */
        [data-testid="metric-container"] {
            background: white;
            border: 1px solid rgba(226, 232, 240, 0.8);
            padding: var(--spacing-md);
            border-radius: var(--border-radius);
            box-shadow: var(--card-shadow);
            transition: all 0.2s ease;
        }
        
        [data-testid="metric-container"]:hover {
            box-shadow: var(--card-shadow-lg);
            transform: translateY(-1px);
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: var(--spacing-sm);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: white;
            border-radius: var(--border-radius) var(--border-radius) 0 0;
            border: 1px solid rgba(226, 232, 240, 0.8);
            padding: var(--spacing-sm) var(--spacing-lg);
            font-weight: 600;
        }
        
        /* Button Styling */
        .stButton > button {
            border-radius: var(--border-radius);
            font-weight: 600;
            transition: all 0.2s ease;
            box-shadow: var(--card-shadow);
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: var(--card-shadow-lg);
        }
        
        /* Progress Bar */
        .stProgress .st-bo {
            background: var(--primary-gradient);
            border-radius: 10px;
        }
        
        /* Download Button */
        .stDownloadButton > button {
            background: var(--success-gradient);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            font-weight: 600;
            box-shadow: var(--card-shadow);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .sl-title {
                font-size: 2rem;
            }
            
            .sl-header {
                padding: var(--spacing-md);
            }
            
            .sl-badge {
                width: 50px;
                height: 50px;
                font-size: 1rem;
            }
        }
    </style>
    <div class="sl-header">
        <div class="sl-brand">
            <div class="sl-badge">🛡️</div>
            <div>
                <h1 class="sl-title">SafeLend</h1>
                <div class="sl-subtitle">Advanced Credit Risk Assessment Platform • by <b>Shubham Khaire</b></div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Enhanced Sidebar
with st.sidebar:
    # Overview Section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="margin: 0 0 0.5rem 0; display: flex; align-items: center; gap: 0.5rem;">
            👋 <span>Overview</span>
        </h3>
        <p style="margin: 0; opacity: 0.9; line-height: 1.4;">
            Predict default probability, credit score (300–900), and rating. Includes affordability, compare, and batch scoring.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # How it Works Section
    st.markdown("""
    <div style="
        background: white;
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    ">
        <h4 style="margin: 0 0 0.75rem 0; color: #334155; display: flex; align-items: center; gap: 0.5rem;">
            🧠 <span>How it Works</span>
        </h4>
        <div style="
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 0.75rem;
            border-radius: 8px;
            font-size: 0.9rem;
            color: #475569;
            border-left: 3px solid #667eea;
        ">
            Scaled inputs → ML model → default probability → derived credit score & rating
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Presets Section
    st.markdown("""
    <div style="
        background: white;
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    ">
        <h4 style="margin: 0 0 0.75rem 0; color: #334155; display: flex; align-items: center; gap: 0.5rem;">
            🎯 <span>Quick Presets</span>
        </h4>
    """, unsafe_allow_html=True)
    
    preset = st.selectbox(
        "Choose a profile",
        ["Average Applicant", "Low Risk", "High Risk"],
        index=0,
        help="Select a preset to auto-fill form with typical values"
    )
    
    with st.expander("📋 Model Details", expanded=False):
        st.markdown("""
        **Inputs:** Age, Income, Loan Amount, Tenure, DPD, Delinquency, Utilization, Accounts, Residence, Purpose, Type
        
        **Outputs:** Default Probability, Credit Score (300-900), Rating
        
        **💡 Tips:**
        - Lower utilization & delinquency ratios improve scores
        - Longer tenure reduces EMI burden
        - Secured loans typically have lower risk
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer Section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(226, 232, 240, 0.8);
    ">
        <div style="margin-bottom: 0.5rem; font-size: 0.9rem; color: #64748b;">
            🔐 Local session • ⚠️ Indicative only
        </div>
        <div style="font-weight: 600; color: #334155;">
            👤 Built by Shubham Khaire
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_preset_defaults(profile: str) -> dict:
    if profile == "Low Risk":
        return dict(age=35, income=1800000, loan_amount=600000, loan_tenure_months=24,
                    avg_dpd_per_delinquency=5, num_open_accounts=2, delinquency_ratio=5, credit_utilization_ratio=20,
                    residence_type='Owned', loan_purpose='Home', loan_type='Secured')
    if profile == "High Risk":
        return dict(age=25, income=600000, loan_amount=1200000, loan_tenure_months=48,
                    avg_dpd_per_delinquency=35, num_open_accounts=4, delinquency_ratio=60, credit_utilization_ratio=80,
                    residence_type='Rented', loan_purpose='Personal', loan_type='Unsecured')
    return dict(age=28, income=1200000, loan_amount=900000, loan_tenure_months=36,
                avg_dpd_per_delinquency=20, num_open_accounts=2, delinquency_ratio=30, credit_utilization_ratio=30,
                residence_type='Owned', loan_purpose='Auto', loan_type='Unsecured')

# Form for inputs
defaults = get_preset_defaults(preset)

with st.form("risk_form"):
    # Enhanced form header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.25rem 1.5rem;
        margin: -2rem -2rem 2rem -2rem;
        border-radius: 20px 20px 0 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    ">
        <h2 style="margin: 0; display: flex; align-items: center; gap: 0.75rem; font-size: 1.5rem; font-weight: 700;">
            🧾 <span>Applicant & Loan Details</span>
        </h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1rem;">
            Enter the applicant's information to assess credit risk
        </p>
    </div>
    """, unsafe_allow_html=True)
    # Personal Information Section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
    ">
        <h4 style="margin: 0 0 1rem 0; color: #334155; display: flex; align-items: center; gap: 0.5rem;">
            👤 <span>Personal Information</span>
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input('👶 Age', min_value=18, step=1, max_value=100, value=defaults['age'], help="Applicant age in years")
    with c2:
        income = st.number_input('💰 Annual Income (₹)', min_value=0, value=defaults['income'], help="Annual income in INR", format="%d")
    with c3:
        loan_amount = st.number_input('🏦 Loan Amount (₹)', min_value=0, value=defaults['loan_amount'], help="Sanctioned loan amount in INR", format="%d")

    # Loan Details Section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 4px solid #10b981;
    ">
        <h4 style="margin: 0 0 1rem 0; color: #334155; display: flex; align-items: center; gap: 0.5rem;">
            📋 <span>Loan Details</span>
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    c4, c5, c6 = st.columns(3)
    with c4:
        loan_tenure_months = st.number_input('📅 Loan Tenure (months)', min_value=0, step=1, value=defaults['loan_tenure_months'], help="Loan repayment period")
    with c5:
        avg_dpd_per_delinquency = st.number_input('⏰ Avg DPD', min_value=0, value=defaults['avg_dpd_per_delinquency'], help="Average days past due per delinquency")
    with c6:
        num_open_accounts = st.number_input('📊 Open Accounts', min_value=1, max_value=10, step=1, value=defaults['num_open_accounts'], help="Number of active loan accounts")

    # Credit Profile Section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 4px solid #f59e0b;
    ">
        <h4 style="margin: 0 0 1rem 0; color: #334155; display: flex; align-items: center; gap: 0.5rem;">
            📈 <span>Credit Profile</span>
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    c7, c8, c9 = st.columns(3)
    with c7:
        delinquency_ratio = st.number_input('⚠️ Delinquency Ratio (%)', min_value=0, max_value=100, step=1, value=defaults['delinquency_ratio'], help="Percentage of payments that were late")
    with c8:
        credit_utilization_ratio = st.number_input('💳 Credit Utilization (%)', min_value=0, max_value=100, step=1, value=defaults['credit_utilization_ratio'], help="Percentage of available credit being used")
    with c9:
        residence_type = st.selectbox('🏠 Residence Type', ['Owned', 'Rented', 'Mortgage'], index=['Owned','Rented','Mortgage'].index(defaults['residence_type']), help="Type of residence ownership")

    c10, c11, c12 = st.columns(3)
    with c10:
        loan_purpose = st.selectbox('🎯 Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'], index=['Education','Home','Auto','Personal'].index(defaults['loan_purpose']), help="Primary purpose of the loan")
    with c11:
        loan_type = st.selectbox('🔒 Loan Type', ['Unsecured', 'Secured'], index=['Unsecured','Secured'].index(defaults['loan_type']), help="Whether loan is backed by collateral")
    with c12:
        loan_to_income_ratio = (loan_amount / income) if income else 0
        # Enhanced metric display
        st.markdown("""
        <div style="
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        ">
            <div style="font-size: 0.875rem; color: #64748b; margin-bottom: 0.25rem;">📊 Loan-to-Income</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #334155;">{:.2f}x</div>
        </div>
        """.format(loan_to_income_ratio), unsafe_allow_html=True)

    # Action Buttons
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns([1,1])
    with col_btn1:
        submitted = st.form_submit_button(
            "🔍 Calculate Risk", 
            use_container_width=True,
            help="Analyze credit risk based on provided information"
        )
    with col_btn2:
        reset = st.form_submit_button(
            "♻️ Reset Form", 
            type="secondary", 
            use_container_width=True,
            help="Clear all inputs and start over"
        )

# Handle submission and results
if 'last_result' not in st.session_state:
    st.session_state.last_result = None
if 'last_inputs' not in st.session_state:
    st.session_state.last_inputs = None
    

if reset:
    st.session_state.last_result = None
    st.session_state.last_inputs = None

if submitted:
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                                                delinquency_ratio, credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )
    st.session_state.last_result = (probability, credit_score, rating)
    st.session_state.last_inputs = dict(
        age=age, income=income, loan_amount=loan_amount, loan_tenure_months=loan_tenure_months,
        avg_dpd_per_delinquency=avg_dpd_per_delinquency, delinquency_ratio=delinquency_ratio,
        credit_utilization_ratio=credit_utilization_ratio, num_open_accounts=num_open_accounts,
        residence_type=residence_type, loan_purpose=loan_purpose, loan_type=loan_type,
        loan_to_income_ratio=loan_to_income_ratio
    )

if st.session_state.last_result is not None:
    probability, credit_score, rating = st.session_state.last_result

    # Risk color
    if probability >= 0.40:
        chip_class = "danger"
        rating_emoji = "🚨"
    elif probability >= 0.20:
        chip_class = "warning"
        rating_emoji = "⚠️"
    else:
        chip_class = "success"
        rating_emoji = "✅"

    # Enhanced Results Section
    st.markdown("""
    <div style="
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(226, 232, 240, 0.8);
        overflow: hidden;
        margin: 2rem 0;
    ">
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            text-align: center;
        ">
            <h2 style="margin: 0; font-size: 1.75rem; font-weight: 800;">📊 Risk Assessment Results</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Comprehensive credit risk analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab_results, tab_explain, tab_afford, tab_compare, tab_batch = st.tabs(["📈 Results", "🔍 Explain", "🧮 Affordability", "🆚 Compare", "📦 Batch Scoring"])

    with tab_results:
        # Enhanced metrics with modern cards
        r1, r2, r3 = st.columns(3)
        with r1:
            # Risk probability card
            risk_color = "#ef4444" if probability >= 0.40 else "#f59e0b" if probability >= 0.20 else "#10b981"
            st.markdown(f"""
            <div style="
                background: white;
                border: 2px solid {risk_color};
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                margin-bottom: 1rem;
            ">
                <div style="font-size: 0.875rem; color: #64748b; margin-bottom: 0.5rem; font-weight: 600;">DEFAULT PROBABILITY</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: {risk_color}; margin-bottom: 0.5rem;">{probability:.1%}</div>
                <div style="background: {risk_color}; height: 8px; border-radius: 4px; width: {min(max(int(probability * 100), 5), 100)}%; margin: 0 auto;"></div>
            </div>
            """, unsafe_allow_html=True)
            
        with r2:
            # Credit score card with gradient
            score_color = "#10b981" if credit_score >= 750 else "#f59e0b" if credit_score >= 650 else "#ef4444"
            score_percentage = ((credit_score - 300) / 600) * 100
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, white 0%, #f8fafc 100%);
                border: 2px solid {score_color};
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                margin-bottom: 1rem;
            ">
                <div style="font-size: 0.875rem; color: #64748b; margin-bottom: 0.5rem; font-weight: 600;">CREDIT SCORE</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: {score_color}; margin-bottom: 0.25rem;">{credit_score}</div>
                <div style="font-size: 0.75rem; color: #64748b; margin-bottom: 0.5rem;">300 ⟶ 900</div>
                <div style="background: #e2e8f0; height: 8px; border-radius: 4px; position: relative; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, {score_color}, {score_color}aa); height: 100%; width: {score_percentage:.1f}%; border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with r3:
            # Rating card with emoji
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, white 0%, #f8fafc 100%);
                border: 2px solid #667eea;
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                margin-bottom: 1rem;
            ">
                <div style="font-size: 0.875rem; color: #64748b; margin-bottom: 0.5rem; font-weight: 600;">CREDIT RATING</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: #667eea; margin-bottom: 0.25rem;">{rating}</div>
                <div style="font-size: 2rem; margin-top: 0.5rem;">{rating_emoji}</div>
            </div>
            """, unsafe_allow_html=True)

        # Enhanced download section
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 2rem 0;
            border: 1px solid rgba(226, 232, 240, 0.8);
        ">
            <h4 style="margin: 0 0 1rem 0; color: #334155; display: flex; align-items: center; gap: 0.5rem;">
                📄 <span>Export Results</span>
            </h4>
        """, unsafe_allow_html=True)
        
        report = {
            "inputs": st.session_state.last_inputs,
            "outputs": {"default_probability": round(float(probability), 4), "credit_score": int(credit_score), "rating": rating},
            "timestamp": pd.Timestamp.now().isoformat(),
            "model_version": "SafeLend v1.0"
        }
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download Report (JSON)",
                file_name="safelend_report.json",
                mime="application/json",
                data=json.dumps(report, indent=2),
                use_container_width=True,
                help="Download detailed assessment report"
            )
        with col2:
            # Summary text for copy-paste
            summary_text = f"SafeLend Risk Assessment\n" \
                          f"Default Probability: {probability:.1%}\n" \
                          f"Credit Score: {credit_score}\n" \
                          f"Rating: {rating} {rating_emoji}\n" \
                          f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}"
            st.download_button(
                label="📋 Download Summary (TXT)",
                file_name="safelend_summary.txt",
                mime="text/plain",
                data=summary_text,
                use_container_width=True,
                help="Download quick summary"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)

        # Enhanced insights section
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.25rem 1.5rem;
            border-radius: 16px;
            margin: 2rem 0 1.5rem 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        ">
            <h3 style="margin: 0; display: flex; align-items: center; gap: 0.75rem; font-size: 1.25rem; font-weight: 700;">
                💡 <span>Key Risk Insights</span>
            </h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.95rem;">
                AI-powered analysis of critical risk factors
            </p>
        </div>
        """, unsafe_allow_html=True)
        insights = []
        lti = float(st.session_state.last_inputs.get('loan_to_income_ratio', 0))
        util = float(st.session_state.last_inputs.get('credit_utilization_ratio', 0))
        delinq = float(st.session_state.last_inputs.get('delinquency_ratio', 0))
        avg_dpd = float(st.session_state.last_inputs.get('avg_dpd_per_delinquency', 0))
        open_accts = int(st.session_state.last_inputs.get('num_open_accounts', 0))
        loan_type = str(st.session_state.last_inputs.get('loan_type', 'Unsecured'))
        loan_purpose = str(st.session_state.last_inputs.get('loan_purpose', 'Personal'))

        # Overall risk summary
        if probability < 0.2:
            insights.append("✅ Overall risk appears low based on current inputs.")
        elif probability < 0.4:
            insights.append("⚠️ Moderate risk. Small improvements can meaningfully help approval odds.")
        else:
            insights.append("🚨 Elevated risk. Consider multiple adjustments for a better outcome.")

        # Loan-to-Income
        if lti > 3.0:
            insights.append("📉 Loan‑to‑Income is high (> 3.0×). Try lowering amount or extending tenure.")
        elif lti < 1.0:
            insights.append("📈 Strong Loan‑to‑Income (< 1.0×) suggests good borrowing capacity.")

        # Utilization
        if util >= 80:
            insights.append("🚨 Credit utilization is very high (≥ 80%). Reducing revolving balances is advisable.")
        elif util >= 50:
            insights.append("⚠️ Credit utilization is elevated (50–80%). Paying down balances may improve score.")
        else:
            insights.append("✅ Credit utilization is healthy (< 50%).")

        # Delinquency
        if delinq >= 40:
            insights.append("🚨 High delinquency ratio (≥ 40%). Improving repayment consistency is critical.")
        elif delinq >= 20:
            insights.append("⚠️ Moderate delinquency (20–40%). Stabilizing payments will help.")
        else:
            insights.append("✅ Low delinquency (< 20%).")

        # Average DPD
        if avg_dpd >= 30:
            insights.append("🚨 Average DPD is high (≥ 30). Reducing overdue days lowers default probability.")
        elif avg_dpd <= 10:
            insights.append("✅ Average DPD is low (≤ 10).")

        # Accounts, loan type, purpose
        if open_accts >= 6:
            insights.append("⚠️ Many open accounts (≥ 6). Consolidation may reduce risk perception.")
        elif open_accts <= 2:
            insights.append("✅ Conservative number of open accounts (≤ 2).")

        if loan_type == 'Unsecured':
            insights.append("⚠️ Unsecured loan increases risk compared to secured alternatives.")
        else:
            insights.append("✅ Secured loan type typically carries lower risk.")

        if loan_purpose in ['Personal']:
            insights.append("⚠️ Personal loans often carry higher risk/interest than Home or Education.")

        # Enhanced insights cards with better styling
        max_insights = insights[:4]  # Show up to 4 insights
        
        if len(max_insights) <= 2:
            insight_cols = st.columns(len(max_insights))
        else:
            insight_cols = st.columns(2)
            
        for i, tip in enumerate(max_insights):
            col_index = i % len(insight_cols)
            
            # Determine card styling based on emoji
            if tip.startswith("✅"):
                bg_gradient = "linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)"
                border_color = "#10b981"
                text_color = "#065f46"
                icon_bg = "#10b981"
            elif tip.startswith("⚠️"):
                bg_gradient = "linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)"
                border_color = "#f59e0b"
                text_color = "#92400e"
                icon_bg = "#f59e0b"
            elif tip.startswith("🚨"):
                bg_gradient = "linear-gradient(135deg, #fef2f2 0%, #fecaca 100%)"
                border_color = "#ef4444"
                text_color = "#991b1b"
                icon_bg = "#ef4444"
            else:
                bg_gradient = "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)"
                border_color = "#667eea"
                text_color = "#334155"
                icon_bg = "#667eea"
            
            with insight_cols[col_index]:
                # Extract emoji and text
                parts = tip.split(" ", 1)
                emoji = parts[0] if len(parts) > 1 else "💡"
                text = parts[1] if len(parts) > 1 else tip
                
                st.markdown(f"""
                <div style="
                    background: {bg_gradient};
                    border: 2px solid {border_color};
                    border-radius: 16px;
                    padding: 1.25rem;
                    margin-bottom: 1rem;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                    transition: transform 0.2s ease;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                ">
                    <div style="
                        display: flex;
                        align-items: center;
                        gap: 0.75rem;
                        margin-bottom: 0.75rem;
                    ">
                        <div style="
                            background: {icon_bg};
                            color: white;
                            width: 32px;
                            height: 32px;
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 1rem;
                            font-weight: bold;
                        ">{emoji}</div>
                        <div style="font-weight: 600; color: {text_color}; font-size: 0.9rem;">Risk Factor</div>
                    </div>
                    <div style="
                        color: {text_color};
                        line-height: 1.5;
                        font-weight: 500;
                        flex-grow: 1;
                    ">{text}</div>
                </div>
                """, unsafe_allow_html=True)

    with tab_explain:
        prob_e, score_e, rating_e, contrib_df = explain_from_inputs(
            **{k: st.session_state.last_inputs[k] for k in ['age','income','loan_amount','loan_tenure_months','avg_dpd_per_delinquency','delinquency_ratio','credit_utilization_ratio','num_open_accounts','residence_type','loan_purpose','loan_type']}
        )
        st.caption("Top feature contributions (linear model view).")
        top_k = st.slider("Show top K", 3, 15, 5)
        st.dataframe(contrib_df.head(top_k), use_container_width=True)

    with tab_afford:
        base = st.session_state.last_inputs or {}
        st.caption("Estimate affordability based on income, DTI, interest and tenure.")
        a1, a2, a3, a4 = st.columns(4)
        with a1:
            aff_income = st.number_input("Annual Income (₹)", min_value=0, value=int(base.get('income', income)))
        with a2:
            dti_target = st.slider("Target DTI (%)", 5, 60, 35, 1, help="Percent of monthly income for EMI")
        with a3:
            interest_pa = st.slider("Interest (p.a. %)", 5.0, 24.0, 12.0, 0.5)
        with a4:
            tenure_m = st.number_input("Tenure (months)", min_value=6, value=int(base.get('loan_tenure_months', 36)), step=6)

        monthly_income = aff_income / 12.0
        max_emi = monthly_income * (dti_target / 100.0)
        r = (interest_pa / 100.0) / 12.0
        n = max(tenure_m, 1)
        if r > 0:
            denom = (1 - math.pow(1 + r, -n))
            max_principal = max_emi * (denom / r)
        else:
            max_principal = max_emi * n

        current_principal = float(base.get('loan_amount', loan_amount))
        emi_ratio = min(max(current_principal / max(1.0, max_principal), 0.0), 2.0)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Max Affordable Loan", f"₹{max_principal:,.0f}")
        with m2:
            st.metric("Current Loan", f"₹{current_principal:,.0f}")
        with m3:
            gap = max_principal - current_principal
            st.metric("Affordability Gap", f"₹{gap:,.0f}")
        st.progress(min(int(emi_ratio * 50), 100))

    with tab_compare:
        st.caption("Compare risk across presets.")
        c_left, c_right = st.columns(2)
        with c_left:
            left_preset = st.selectbox("Left preset", ["Average Applicant", "Low Risk", "High Risk"], index=1)
        with c_right:
            right_preset = st.selectbox("Right preset", ["Average Applicant", "Low Risk", "High Risk"], index=2)

        left_defaults = get_preset_defaults(left_preset)
        right_defaults = get_preset_defaults(right_preset)

        lp, ls, lr = predict(
            left_defaults['age'], left_defaults['income'], left_defaults['loan_amount'], left_defaults['loan_tenure_months'],
            left_defaults['avg_dpd_per_delinquency'], left_defaults['delinquency_ratio'], left_defaults['credit_utilization_ratio'],
            left_defaults['num_open_accounts'], left_defaults['residence_type'], left_defaults['loan_purpose'], left_defaults['loan_type']
        )
        rp, rs, rr = predict(
            right_defaults['age'], right_defaults['income'], right_defaults['loan_amount'], right_defaults['loan_tenure_months'],
            right_defaults['avg_dpd_per_delinquency'], right_defaults['delinquency_ratio'], right_defaults['credit_utilization_ratio'],
            right_defaults['num_open_accounts'], right_defaults['residence_type'], right_defaults['loan_purpose'], right_defaults['loan_type']
        )

        comp_df = pd.DataFrame({
            'Preset': [left_preset, right_preset],
            'Default Probability': [float(lp), float(rp)],
            'Credit Score': [int(ls), int(rs)],
        })
        st.dataframe(comp_df, use_container_width=True)
        figc = px.bar(comp_df, x='Preset', y='Default Probability', color='Preset', text=comp_df['Default Probability'].map(lambda v: f"{v:.1%}"))
        figc.update_traces(textposition='outside')
        figc.update_layout(yaxis_tickformat='.0%', margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(figc, use_container_width=True)

    with tab_batch:
        st.caption("Upload a CSV to score multiple applicants at once. Columns should match the app inputs.")
        demo = st.checkbox("Use template", value=False)
        uploaded = st.file_uploader("CSV file", type=["csv"])
        df_in = None
        if demo:
            df_in = batch_template()
        elif uploaded is not None:
            df_in = pd.read_csv(uploaded)
        if df_in is not None:
            st.dataframe(df_in.head(), use_container_width=True)
            try:
                df_out = predict_batch(df_in)
                st.dataframe(df_out, use_container_width=True)
                csv_buf = io.StringIO()
                df_out.to_csv(csv_buf, index=False)
                st.download_button("⬇️ Download Results (CSV)", data=csv_buf.getvalue(), file_name="safelend_batch_results.csv", mime="text/csv")
            except Exception as e:
                st.error(f"Batch scoring failed: {e}")
        

# Footer
st.divider()

# Simple footer with columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0;">
        <div style="margin-bottom: 1rem;">
            <span style="font-size: 2rem;">🛡️</span>
            <h3 style="margin: 0.5rem 0; color: #334155;">SafeLend</h3>
            <p style="margin: 0; color: #64748b; font-size: 0.9rem;">Advanced Credit Risk Assessment</p>
        </div>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 1rem 0;">
        <div style="color: #64748b;">
            <p style="margin: 0.5rem 0;"><strong>Made by Shubham Khaire</strong> • SafeLend © 2025</p>
            <p style="margin: 0; font-size: 0.8rem; color: #94a3b8;">
                ⚠️ This application is for demonstration purposes only and does not constitute financial advice.<br>
                Consult with qualified financial professionals for actual lending decisions.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)





