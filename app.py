import os
import pickle

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Heart Disease Prediction | AI Diagnostics",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# -------------------- DARK THEME CSS --------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Background - Dark */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 2rem;
    }
    
    /* Glass Morphism Container - Dark */
    .block-container {
        background: rgba(20, 20, 40, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Header Styling - Dark */
    h1 {
        background: linear-gradient(135deg, #e0e0ff 0%, #a0a0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 2px 10px rgba(160, 160, 255, 0.3);
    }
    
    h2, h3 {
        color: #e0e0ff !important;
        font-weight: 600 !important;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(224, 224, 255, 0.8);
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
        font-weight: 300;
    }
    
    section.main > div {
        padding-top: 0rem !important;
    }
    
    .app-title {
        margin-top: 2.2rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.6rem;
        min-height: 3.5rem;
    }
    
    .app-title .heart {
        font-size: 2.4rem;
        line-height: 1;
        display: flex;
        align-items: center;
    }
    
    /* Modern Tab Styling - Dark */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 30, 60, 0.4);
        backdrop-filter: blur(10px);
        padding: 0.8rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        justify-content: start;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(40, 40, 80, 0.5);
        color: rgba(224, 224, 255, 0.7);
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(60, 60, 100, 0.6);
        color: #e0e0ff;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(160, 160, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(80, 80, 150, 0.5), rgba(100, 100, 180, 0.4)) !important;
        color: #e0e0ff !important;
        box-shadow: 0 8px 24px rgba(160, 160, 255, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Input Fields - Dark */
    .stNumberInput > div > div > input {
        background: rgba(40, 40, 80, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        color: #e0e0ff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        transition: all 0.3s ease;
        font-weight: 400;
        font-size: 0.95rem !important;
        height: 48px !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: rgba(160, 160, 255, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(160, 160, 255, 0.2) !important;
        background: rgba(50, 50, 100, 0.6) !important;
        outline: none !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(40, 40, 80, 0.5) !important;
        color: #e0e0ff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }
    
    label {
        color: #e0e0ff !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        margin-bottom: 0.3rem !important;
    }
    
    /* Buttons - Dark */
    .stButton > button {
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%) !important;
        color: #e0e0ff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 36px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
        width: 100%;
        margin-top: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 32px rgba(80, 80, 150, 0.5) !important;
        background: linear-gradient(135deg, #5a6578 0%, #3d4758 100%) !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #805ad5 0%, #553c9a 100%) !important;
        box-shadow: 0 8px 24px rgba(128, 90, 213, 0.4) !important;
    }
    
    /* Panels - Dark */
    .result-panel {
        background: rgba(30, 30, 60, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        min-height: auto;
        display: flex;
        flex-direction: column;
    }
    
    .input-panel {
        background: rgba(30, 30, 60, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Metrics - Dark */
    .stMetric {
        background: rgba(40, 40, 80, 0.5);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    .stMetric label {
        color: rgba(224, 224, 255, 0.8) !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #e0e0ff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    /* Alert Boxes - Dark */
    .stAlert {
        border-radius: 14px !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(56, 142, 60, 0.4), rgba(46, 125, 50, 0.4)) !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 152, 0, 0.4), rgba(245, 124, 0, 0.4)) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(211, 47, 47, 0.4), rgba(198, 40, 40, 0.4)) !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(2, 136, 209, 0.4), rgba(1, 87, 155, 0.4)) !important;
    }
    
    /* DataFrame - Dark */
    .dataframe {
        background: rgba(30, 30, 60, 0.5) !important;
        color: #e0e0ff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .dataframe th {
        background: rgba(40, 40, 80, 0.6) !important;
        color: #e0e0ff !important;
    }
    
    /* File Uploader - Dark */
    .stFileUploader {
        background: rgba(30, 30, 60, 0.4);
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 2rem;
    }
    
    /* Text Colors - Dark */
    p, span, div {
        color: rgba(224, 224, 255, 0.9);
    }
    
    /* Scrollbar - Dark */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 30, 60, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, rgba(80, 80, 150, 0.5), rgba(100, 100, 180, 0.4));
        border-radius: 10px;
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            justify-content: flex-start !important;
            overflow-x: auto !important;
            white-space: nowrap !important;
            padding: 0.4rem 0.3rem !important;
            gap: 6px !important;
            scrollbar-width: none;
        }
        
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            display: none;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 8px 14px !important;
            font-size: 0.8rem !important;
            flex-shrink: 0 !important;
        }
        
        .block-container {
            padding: 1rem !important;
            border-radius: 12px !important;
        }
        
        h1 {
            font-size: 1.8rem !important;
        }
        
        .app-title {
            margin-top: 1.5rem;
        }
        
        .app-title .heart {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown("""
<div class="app-title">
    <div class="heart">❤️</div>
    <h1 style="margin: 0;">Heart Disease Prediction</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("<p class='subtitle'>AI-Powered Clinical Diagnostic Platform</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(
    ['🔍 Predict', '📂 Bulk Predict', '🧠 Model Info', '👨‍💻 About']
)

# -------------------- MODEL CONFIG --------------------
algorithm = [
    "Decision Tree",
    "Logistic Regression",
    "Random Forest",
    "Support Vector Machine"
]

modelnames = [
    'tree.pkl',
    'LogisticRegression.pkl',
    'RandomForest.pkl',
    'SVM.pkl'
]

# -------------------- PREDICTION FUNCTION --------------------
def predict_single(data):
    """Predict for a single patient"""
    predictions = []
    for modelname in modelnames:
        try:
            with open(modelname, "rb") as file:
                model = pickle.load(file)
                pred = model.predict(data)[0]
                predictions.append(pred)
        except:
            predictions.append("Model Error")
    return predictions

def predict_bulk(df):
    """Predict for multiple patients (row-wise)"""
    results = {}
    for modelname, model_file in zip(algorithm, modelnames):
        try:
            with open(model_file, "rb") as file:
                model = pickle.load(file)
                results[modelname] = model.predict(df)
        except:
            results[modelname] = ["Error"] * len(df)
    return results

@st.cache_resource
def load_rf_model():
    with open("RandomForest.pkl", "rb") as f:
        return pickle.load(f)

SEX_MAP = {0: "Female", 1: "Male"}

CHEST_PAIN_MAP = {
    0: "Typical Angina",
    1: "Atypical Angina",
    2: "Non-anginal Pain",
    3: "Asymptomatic"
}

ECG_MAP = {
    0: "Normal",
    1: "ST-T Wave Abnormality",
    2: "Left Ventricular Hypertrophy"
}

SLOPE_MAP = {
    0: "Upsloping",
    1: "Flat",
    2: "Downsloping"
}

def generate_medical_report(input_data, risk_percentage, insights):
    file_name = "heart_disease_report.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "Heart Disease Risk Assessment Report")
    y -= 30
    c.setFont("Helvetica", 11)
    c.drawString(50, y, "Generated by AI Clinical Diagnostic System")
    y -= 40
    c.line(50, y, width - 50, y)

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Patient Summary")
    y -= 20
    c.setFont("Helvetica", 11)

    age = input_data["Age"].values[0]
    sex = SEX_MAP[input_data["Sex"].values[0]]
    cp = CHEST_PAIN_MAP[input_data["ChestPainType"].values[0]]
    bp = input_data["RestingBP"].values[0]
    chol = input_data["Cholesterol"].values[0]
    fbs = "Yes" if input_data["FastingBS"].values[0] == 1 else "No"
    ecg = ECG_MAP[input_data["RestingECG"].values[0]]
    hr = input_data["MaxHR"].values[0]
    angina = "Yes" if input_data["ExerciseAngina"].values[0] == 1 else "No"
    oldpeak = round(input_data["Oldpeak"].values[0], 2)
    slope = SLOPE_MAP[input_data["ST_Slope"].values[0]]

    patient_data = [
        ("Age", f"{age} years"),
        ("Sex", sex),
        ("Chest Pain Type", cp),
        ("Resting Blood Pressure", f"{bp} mm Hg"),
        ("Cholesterol Level", f"{chol} mg/dL"),
        ("Fasting Blood Sugar > 120 mg/dL", fbs),
        ("Resting ECG Result", ecg),
        ("Maximum Heart Rate Achieved", f"{hr} bpm"),
        ("Exercise-Induced Angina", angina),
        ("ST Depression (Oldpeak)", oldpeak),
        ("ST Segment Slope", slope),
    ]

    for label, value in patient_data:
        c.drawString(60, y, f"{label}: {value}")
        y -= 15

    y -= 20
    c.line(50, y, width - 50, y)
    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Overall Risk Assessment")
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y, f"Estimated Heart Disease Risk: {risk_percentage:.1f}%")
    y -= 25
    c.setFont("Helvetica", 11)

    if risk_percentage >= 60:
        conclusion = "High risk detected. Immediate cardiology consultation is strongly recommended."
    elif risk_percentage >= 30:
        conclusion = "Moderate risk detected. Medical follow-up and lifestyle changes are advised."
    else:
        conclusion = "Low risk detected. Maintain a healthy lifestyle and regular checkups."

    c.drawString(60, y, conclusion)

    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Key Observations & Risk Factors")
    y -= 20
    c.setFont("Helvetica", 11)
    for i in insights:
        c.drawString(60, y, f"- {i}")
        y -= 15

    y -= 40
    c.line(50, y, width - 50, y)
    y -= 25
    c.setFont("Helvetica", 9)
    c.drawString(50, y, "Disclaimer: This report is generated by an AI system for educational and screening purposes only.")
    y -= 12
    c.drawString(50, y, "It is not a medical diagnosis. Please consult a certified healthcare professional.")

    c.showPage()
    c.save()
    return file_name

# -------------------- TAB 1 : SINGLE PREDICTION --------------------
with tab1:
    st.markdown("### 🩺 Heart Disease Risk Assessment")
    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown("#### 📋 Patient Information")
        age = st.number_input("Age (years)", 0, 150, 25, key="age")
        sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Male" if x else "Female", key="sex")
        chest_pain = st.selectbox("Chest Pain Type", [0, 1, 2, 3], 
            format_func=lambda x: {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-Anginal Pain", 3: "Asymptomatic"}[x], key="cp")
        resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 0, 300, 120, key="bp")
        cholesterol = st.number_input("Cholesterol (mg/dl)", 0, 1000, 200, key="chol")
        fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1], format_func=lambda x: "Yes" if x else "No", key="fbs")
        resting_ecg = st.selectbox("Resting ECG", [0, 1, 2], 
            format_func=lambda x: {0: "Normal", 1: "ST-T Wave Abnormality", 2: "Left Ventricular Hypertrophy"}[x], key="ecg")
        max_hr = st.number_input("Maximum Heart Rate Achieved (BPM)", 80, 220, 150, step=1, key="hr")
        exercise_angina = st.selectbox("Exercise Induced Angina", [0, 1], format_func=lambda x: "Yes" if x else "No", key="ea")
        oldpeak = st.number_input("Oldpeak", 0.0, 10.0, 1.0, step=0.1, key="op")
        st_slope = st.selectbox("ST Slope", [0, 1, 2], 
            format_func=lambda x: {0: "Upsloping", 1: "Flat", 2: "Downsloping"}[x], key="slope")
        st.markdown("---")
        predict_button = st.button("🔍 PREDICT HEART DISEASE", key="predict_btn")

    with right_col:
        st.markdown("#### 📊 Prediction Results")
        if predict_button:
            input_data = pd.DataFrame({
                'Age': [age], 'Sex': [sex], 'ChestPainType': [chest_pain],
                'RestingBP': [resting_bp], 'Cholesterol': [cholesterol],
                'FastingBS': [fasting_bs], 'RestingECG': [resting_ecg],
                'MaxHR': [max_hr], 'ExerciseAngina': [exercise_angina],
                'Oldpeak': [oldpeak], 'ST_Slope': [st_slope]
            })
            
            results = predict_single(input_data)
            valid_preds = [r for r in results if r in [0, 1]]
            risk_percentage = (sum(valid_preds) / len(valid_preds)) * 100 if valid_preds else 0
            
            st.markdown(f"""
            <div style='text-align: center; padding: 2rem; background: rgba(255, 255, 255, 0.2); 
                 border-radius: 16px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3);
                 margin-bottom: 1.5rem;'>
                <p style='color: white; margin: 0; font-size: 1rem; font-weight: 500;'>OVERALL RISK</p>
                <h1 style='color: white; margin: 0.5rem 0; font-size: 3.5rem; font-weight: 700;'>{risk_percentage:.0f}%</h1>
            </div>
            """, unsafe_allow_html=True)
            
            if risk_percentage >= 60:
                st.error("🔴 **HIGH RISK DETECTED**\n\nImmediate medical consultation strongly recommended.")
            elif risk_percentage >= 30:
                st.warning("🟡 **MODERATE RISK DETECTED**\n\nMedical consultation advised.")
            else:
                st.success("🟢 **LOW RISK DETECTED**\n\nMaintain healthy lifestyle.")
            
            st.markdown("---")
            st.markdown("**Individual Model Predictions:**")
            for model_name, prediction in zip(algorithm, results):
                if prediction == "Model Error":
                    st.warning(f"⚠️ **{model_name}**: Model Error")
                elif prediction == 0:
                    st.success(f"✅ **{model_name}**: No Heart Disease")
                else:
                    st.error(f"🚨 **{model_name}**: Heart Disease Detected")
            
            st.markdown("---")
            fig, ax = plt.subplots(figsize=(7, 4))
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')
            colors = ['#4CAF50' if v == 0 else '#f44336' for v in valid_preds]
            ax.barh(algorithm, valid_preds, color=colors, edgecolor='white', linewidth=2)
            ax.set_xlim(0, 1.2)
            ax.set_xlabel("0 = No Disease | 1 = Disease", color='white', fontsize=9, fontweight='600')
            ax.set_title("Model Predictions", fontsize=12, fontweight='bold', color='white', pad=12)
            ax.tick_params(colors='white', labelsize=8)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('white')
            ax.spines['bottom'].set_color('white')
            ax.grid(axis='x', alpha=0.2, color='white')
            plt.tight_layout()
            st.pyplot(fig)
            
            st.markdown("---")
            st.markdown("**💡 Health Recommendations:**")
            st.markdown("""
            - Schedule comprehensive cardiac evaluation
            - Monitor blood pressure regularly
            - Maintain healthy cholesterol levels
            - Exercise 150+ minutes per week
            """)
            
            st.markdown("---")
            st.subheader("🧠 Model Explainability")
            rf_model = load_rf_model()
            importance = rf_model.feature_importances_
            imp_df = pd.DataFrame({"Feature": input_data.columns, "Importance": importance}).sort_values(by="Importance", ascending=False)
            st.dataframe(imp_df, use_container_width=True)
            
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            fig2.patch.set_facecolor('none')
            ax2.set_facecolor('none')
            ax2.barh(imp_df["Feature"], imp_df["Importance"], color="#667eea")
            ax2.set_title("Feature Importance", color='white')
            ax2.tick_params(colors='white')
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['left'].set_color('white')
            ax2.spines['bottom'].set_color('white')
            ax2.invert_yaxis()
            plt.tight_layout()
            st.pyplot(fig2)
            
            st.markdown("---")
            st.subheader("📄 Download Medical Report")
            insights = [
                "High cholesterol level" if cholesterol > 240 else "Cholesterol within normal range",
                "High blood pressure" if resting_bp > 140 else "Blood pressure within normal range",
                "Exercise-induced angina present" if exercise_angina == 1 else "No exercise-induced angina"
            ]
            pdf_file = generate_medical_report(input_data, risk_percentage, insights)
            with open(pdf_file, "rb") as f:
                st.download_button("⬇️ Download PDF Report", f, file_name="heart_disease_report.pdf", mime="application/pdf")
        else:
            st.info("👈 Enter patient information and click **PREDICT**")

# -------------------- TAB 2 : BULK PREDICTION --------------------
with tab2:
    st.header("📂 Bulk Heart Disease Prediction")
    st.markdown("Upload a CSV file containing patient data for batch predictions")
    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.subheader("📄 Data Preview")
            st.dataframe(df.head(10))
            REQUIRED_COLUMNS = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol',
                'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']
            if not all(col in df.columns for col in REQUIRED_COLUMNS):
                st.error("❌ Missing required columns")
            else:
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("🚀 Run Batch Prediction"):
                        with st.spinner("Processing..."):
                            bulk_results = predict_bulk(df)
                        for model_name, preds in bulk_results.items():
                            df[model_name] = preds
                        st.success("✅ Predictions completed!")
                        st.dataframe(df)
                        csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button("⬇️ Download Results CSV", csv, "predictions.csv", "text/csv")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# -------------------- TAB 3 : MODEL INFO --------------------
with tab3:
    st.header("🧠 Model Information")
    st.markdown("This platform uses four machine learning models for heart disease predictions.")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 1️⃣ Decision Tree
        - Highly interpretable
        - Fast training
        - Works with non-linear relationships
        
        ### 2️⃣ Logistic Regression
        - Linear probabilistic model
        - Binary classification
        - Probability estimates
        """)
    with col2:
        st.markdown("""
        ### 3️⃣ Random Forest
        - Ensemble method
        - High accuracy (~91%)
        - Robust to overfitting
        
        ### 4️⃣ SVM
        - High-dimensional spaces
        - Strong generalization
        - Clear margin separation
        """)

# -------------------- TAB 4 : ABOUT --------------------
with tab4:
    st.header("👨‍💻 About the Developer")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        ### Purbashis Behera
        
        **Software Engineer**  
        **ML & AI Enthusiast**
        
        ---
        
        📧 **Email**  
        purbashis21@gmail.com
        """)

    with col2:
        st.markdown("""
        ### Professional Profile
        
        **Technical Skills**
        - **Programming:** Python, Pandas, NumPy, Scikit-learn
        - **Frameworks:** Streamlit, Flask, TensorFlow
        - **Specialization:** Machine Learning, Data Science, AI Applications
        
        **Core Competencies**
        - Predictive modeling and algorithm development
        - Data preprocessing and feature engineering
        - Model evaluation and optimization
        - End-to-end ML application deployment
        
        **Career Vision**
        
        Passionate about leveraging machine learning and artificial intelligence 
        to solve real-world problems in healthcare and beyond. Committed to building 
        intelligent, data-driven systems that create meaningful impact and improve lives.
        """)

    st.markdown("---")
    
    st.subheader("📌 Project Information")
    st.markdown("""
    **Heart Disease Prediction System** is an AI-powered diagnostic tool that combines 
    multiple machine learning algorithms to provide comprehensive cardiovascular risk assessments.
    
    **Key Features:**
    - Multi-model ensemble approach for robust predictions
    - User-friendly interface for clinical data input
    - Batch processing capability for multiple patients
    - Visual analytics and interpretable results
    
    **Disclaimer:** This tool is designed for educational and research purposes. 
    Always consult qualified healthcare professionals for medical diagnosis and treatment.
    """)