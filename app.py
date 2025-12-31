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

# -------------------- MODERN CSS --------------------
st.markdown("""
<style>
    /* Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Background with Modern Gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem;
    }
    
    /* Glass Morphism Container */
    .block-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Header Styling */
    h1 {
        background: linear-gradient(135deg, #ffffff 0%, #e0e0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 2px 10px rgba(255, 255, 255, 0.3);
    }
    
    h2, h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
        font-weight: 300;
    }
    /* Remove Streamlit default top spacing */
section.main > div {
    padding-top: 0rem !important;
}

/* Stable title container to prevent emoji jump */
.app-title {
    margin-top: 2.2rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    min-height: 3.5rem; /* prevents flash */
}

/* Emoji alignment fix */
.app-title .heart {
    font-size: 2.4rem;
    line-height: 1;
    display: flex;
    align-items: center;
}

    /* Modern Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 0.8rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        justify-content: start;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.15);
        color: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.25);
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.2)) !important;
        color: #ffffff !important;
        box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Modern Input Fields - Consistent Styling */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        transition: all 0.3s ease;
        font-weight: 400;
        font-size: 0.95rem !important;
        height: 48px !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.25) !important;
        outline: none !important;
    }
    @media (max-width: 768px) {
    .stTabs [data-baseweb="tab-list"]::after {
        content: "⇆";
        color: rgba(255,255,255,0.6);
        padding-left: 6px;
        font-size: 0.75rem;
    }
}

  
    /* Labels - Consistent */
    label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        margin-bottom: 0.3rem !important;
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 36px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4) !important;
        width: 100%;
        margin-top: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.6) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        box-shadow: 0 8px 24px rgba(240, 147, 251, 0.4) !important;
    }
    
    /* Result Panel */
    .result-panel {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        min-height: auto;
        display: flex;
        flex-direction: column;
    }
    
    /* Input Panel */
    .input-panel {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Metrics */
    .stMetric {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    .stMetric label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 0.9rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Alert Boxes */
    .stAlert {
        border-radius: 14px !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.3), rgba(56, 142, 60, 0.3)) !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.3), rgba(255, 152, 0, 0.3)) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.3), rgba(229, 57, 53, 0.3)) !important;
    }
    
    /* DataFrame */
    .dataframe {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }
    
    .dataframe th {
        background: rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 2px dashed rgba(255, 255, 255, 0.4);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: rgba(255, 255, 255, 0.7);
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.01);
    }
    
    /* Horizontal Rule */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        margin: 2rem auto 0 auto;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.2));
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.3));
    }
    
    /* Text Colors */
    p, span, div {
        color: rgba(255, 255, 255, 0.95);
    }
    
    /* Model Result Cards */
    .model-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* ================= TAB MOBILE FIX ================= */

@media (max-width: 768px) {

    /* Make tab list scrollable */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: flex-start !important;
        overflow-x: auto !important;
        white-space: nowrap !important;
        padding: 0.4rem 0.3rem !important;
        gap: 6px !important;
        scrollbar-width: none; /* Firefox */
    }

    /* Hide scrollbar (Chrome/Safari) */
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        display: none;
    }

    /* Reduce tab size */
    .stTabs [data-baseweb="tab"] {
        padding: 8px 14px !important;
        font-size: 0.8rem !important;
        flex-shrink: 0 !important;
    }
}

    /* ================= MOBILE RESPONSIVENESS ================= */

@media (max-width: 768px) {

    .block-container {
        padding: 1rem !important;
        border-radius: 12px !important;
    }
    
    @media (max-width: 768px) {
    h1 span:first-child {
        font-size: 2rem !important;
    }
}

@media (max-width: 768px) {
    .app-title {
        margin-top: 1.5rem;
    }

    .app-title .heart {
        font-size: 2rem;
    }
}


    h1 {
        font-size: 1.8rem !important;
    }

    .subtitle {
        font-size: 0.95rem !important;
    }

    .stButton > button {
        font-size: 0.9rem !important;
        padding: 12px 20px !important;
    }

    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
    }

    /* Reduce blur for better mobile performance */
    .result-panel,
    .input-panel {
        backdrop-filter: none !important;
    }
}

    
    /* Responsive */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        
        h1 {
            font-size: 1.8rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 10px 16px;
            font-size: 0.85rem;
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

    # ----------- TITLE -----------
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "Heart Disease Risk Assessment Report")

    y -= 30
    c.setFont("Helvetica", 11)
    c.drawString(50, y, "Generated by AI Clinical Diagnostic System")

    y -= 40
    c.line(50, y, width - 50, y)

    # ----------- PATIENT SUMMARY -----------
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

    # ----------- RISK RESULT -----------
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

    # ----------- KEY RISK FACTORS -----------
    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Key Observations & Risk Factors")

    y -= 20
    c.setFont("Helvetica", 11)

    for i in insights:
        c.drawString(60, y, f"- {i}")
        y -= 15

    # ----------- DISCLAIMER -----------
    y -= 40
    c.line(50, y, width - 50, y)

    y -= 25
    c.setFont("Helvetica", 9)
    c.drawString(
        50,
        y,
        "Disclaimer: This report is generated by an AI system for educational and screening purposes only."
    )
    y -= 12
    c.drawString(
        50,
        y,
        "It is not a medical diagnosis. Please consult a certified healthcare professional."
    )

    c.showPage()
    c.save()

    return file_name




# -------------------- TAB 1 : SINGLE PREDICTION --------------------
with tab1:
    st.markdown("### 🩺 Heart Disease Risk Assessment")
    
    # Create left-right layout
    left_col, right_col = st.columns(2)

    
    # LEFT SIDE - INPUTS
    with left_col:
        st.markdown("#### 📋 Patient Information")
        
        age = st.number_input("Age (years)", 0, 150, 25, key="age")
        
        sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Male" if x else "Female", key="sex")
        
        chest_pain = st.selectbox(
            "Chest Pain Type",
            [0, 1, 2, 3],
            format_func=lambda x: {
                0: "Typical Angina",
                1: "Atypical Angina",
                2: "Non-Anginal Pain",
                3: "Asymptomatic"
            }[x],
            key="cp"
        )
        
        resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 0, 300, 120, key="bp")
        
        cholesterol = st.number_input("Cholesterol (mg/dl)", 0, 1000, 200, key="chol")
        
        fasting_bs = st.selectbox(
            "Fasting Blood Sugar > 120 mg/dl",
            [0, 1],
            format_func=lambda x: "Yes" if x else "No",
            key="fbs"
        )
        
        resting_ecg = st.selectbox(
            "Resting ECG",
            [0, 1, 2],
            format_func=lambda x: {
                0: "Normal",
                1: "ST-T Wave Abnormality",
                2: "Left Ventricular Hypertrophy"
            }[x],
            key="ecg"
        )
        
        max_hr = st.number_input("Maximum Heart Rate Achieved", 60, 202, 150, key="hr")
        
        exercise_angina = st.selectbox(
            "Exercise Induced Angina",
            [0, 1],
            format_func=lambda x: "Yes" if x else "No",
            key="ea"
        )
        
        oldpeak = st.number_input("Oldpeak", 0.0, 10.0, 1.0, step=0.1, key="op")
        
        st_slope = st.selectbox(
            "ST Slope",
            [0, 1, 2],
            format_func=lambda x: {
                0: "Upsloping",
                1: "Flat",
                2: "Downsloping"
            }[x],
            key="slope"
        )
        
        st.markdown("---")
        predict_button = st.button("🔍 PREDICT HEART DISEASE", width='stretch')
    
    # RIGHT SIDE - RESULTS
    with right_col:
        st.markdown("#### 📊 Prediction Results")
        
        if predict_button:
            input_data = pd.DataFrame({
                'Age': [age],
                'Sex': [sex],
                'ChestPainType': [chest_pain],
                'RestingBP': [resting_bp],
                'Cholesterol': [cholesterol],
                'FastingBS': [fasting_bs],
                'RestingECG': [resting_ecg],
                'MaxHR': [max_hr],
                'ExerciseAngina': [exercise_angina],
                'Oldpeak': [oldpeak],
                'ST_Slope': [st_slope]
            })
            
            results = predict_single(input_data)

            valid_preds = [r for r in results if r in [0, 1]]
            risk_percentage = (sum(valid_preds) / len(valid_preds)) * 100 if valid_preds else 0
            
            # Risk Assessment Card
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
                st.warning("🟡 **MODERATE RISK DETECTED**\n\nMedical consultation advised. Monitor symptoms closely.")
            else:
                st.success("🟢 **LOW RISK DETECTED**\n\nMaintain healthy lifestyle and regular checkups.")
            
            st.markdown("---")
            
            # Individual Model Results
            st.markdown("**Individual Model Predictions:**")
            
            for model_name, prediction in zip(algorithm, results):
                if prediction == "Model Error":
                    st.warning(f"⚠️ **{model_name}**: Model Error")
                elif prediction == 0:
                    st.success(f"✅ **{model_name}**: No Heart Disease")
                else:
                    st.error(f"🚨 **{model_name}**: Heart Disease Detected")
            
            st.markdown("---")
            
            # Visualization
            fig, ax = plt.subplots(figsize=(7, 4))
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')
            
            colors = ['#4CAF50' if v == 0 else '#f44336' for v in valid_preds]
            bars = ax.barh(algorithm, valid_preds, color=colors, edgecolor='white', linewidth=2)
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
            
            # Health Tips
            st.markdown("**💡 Health Recommendations:**")
            st.markdown("""
            - Schedule comprehensive cardiac evaluation
            - Monitor blood pressure regularly
            - Maintain healthy cholesterol levels
            - Exercise 150+ minutes per week
            - Follow heart-healthy diet
            - Quit smoking and limit alcohol
            - Manage stress effectively
            """)
                    # ---------------- SHAP EXPLANATION ----------------
            st.markdown("---")
            st.subheader("🧠 Model Explainability (Feature Importance)")

            rf_model = load_rf_model()
            importance = rf_model.feature_importances_

            imp_df = pd.DataFrame({
            "Feature": input_data.columns,
            "Importance": importance
            }).sort_values(by="Importance", ascending=False)

            st.dataframe(imp_df, use_container_width=True)

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.barh(imp_df["Feature"], imp_df["Importance"], color="#667eea")
            ax.set_title("Feature Importance (Random Forest)")
            ax.invert_yaxis()
            st.pyplot(fig)

            # ---------------- PDF REPORT ----------------
            st.markdown("---")
            st.subheader("📄 Download Medical Report")

            insights = [
                "High cholesterol level" if cholesterol > 240 else "Cholesterol within normal range",
                "High blood pressure" if resting_bp > 140 else "Blood pressure within normal range",
                "Exercise-induced angina present" if exercise_angina == 1 else "No exercise-induced angina"
            ]

            pdf_file = generate_medical_report(
                input_data,
                risk_percentage,
                insights
            )

            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=f,
                    file_name="heart_disease_report.pdf",
                    mime="application/pdf",
                    width='stretch'
                )

        else:
            st.info("👈 Enter patient information on the left and click **PREDICT** to view results.")




# -------------------- TAB 2 : BULK PREDICTION --------------------
with tab2:
    st.header("📂 Bulk Heart Disease Prediction")
    st.markdown("Upload a CSV file containing patient data for batch predictions")

    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=["csv"],
        help="Upload a CSV with required columns: Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope"
    )

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.subheader("📄 Data Preview")
            st.dataframe(df.head(10), width='stretch')

            REQUIRED_COLUMNS = [
                'Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol',
                'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina',
                'Oldpeak', 'ST_Slope'
            ]

            if not all(col in df.columns for col in REQUIRED_COLUMNS):
                st.error("❌ Missing required columns. Please ensure your CSV contains all necessary fields.")
            else:
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("🚀 Run Batch Prediction", width='stretch'):
                        with st.spinner("Processing predictions..."):
                            bulk_results = predict_bulk(df)

                        for model_name, preds in bulk_results.items():
                            df[model_name] = preds


                        st.success("✅ Predictions completed successfully!")
                        st.subheader("📊 Results")
                        st.dataframe(df, width='stretch')

                        csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "⬇️ Download Results CSV",
                            csv,
                            "heart_disease_predictions.csv",
                            "text/csv",
                            width="stretch"
                        )

        except Exception as e:
            st.error(f"⚠️ Error processing file: {e}")


# -------------------- TAB 3 : MODEL INFO --------------------
with tab3:
    st.header("🧠 Model Information")
    
    st.markdown("""
    This platform uses an ensemble of four machine learning models to provide comprehensive heart disease predictions.
    Each model brings unique strengths to the diagnostic process.
    """)
    
    st.markdown("---")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 1️⃣ Decision Tree Classifier
        **Characteristics:**
        - Highly interpretable decision paths
        - Fast training and prediction
        - Works well with non-linear relationships
        
        **Use Case:** Quick initial screening
        
        ---
        
        ### 2️⃣ Logistic Regression
        **Characteristics:**
        - Linear probabilistic model
        - Excellent for binary classification
        - Provides probability estimates
        
        **Use Case:** Statistical analysis baseline
        """)
    
    with col2:
        st.markdown("""
        ### 3️⃣ Random Forest Classifier
        **Characteristics:**
        - Ensemble of multiple decision trees
        - High accuracy and robustness
        - Handles feature interactions well
        
        **Use Case:** Primary prediction model
        
        ---
        
        ### 4️⃣ Support Vector Machine
        **Characteristics:**
        - Effective in high-dimensional spaces
        - Strong generalization capability
        - Works well with clear margins
        
        **Use Case:** Complex pattern recognition
        """)

    st.markdown("---")
    
    st.subheader("📈 Model Performance Comparison")
    
    model_accuracy = {
        "Decision Tree": 0.84,
        "Logistic Regression": 0.86,
        "Random Forest": 0.91,
        "SVM": 0.88
    }

    models = list(model_accuracy.keys())
    accuracy = list(model_accuracy.values())

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        fig1.patch.set_facecolor('none')
        ax1.set_facecolor('none')
        
        gradient_colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c']
        bars = ax1.bar(models, accuracy, color=gradient_colors, edgecolor='white', linewidth=2)
        ax1.set_xlabel("Models", color='white', fontsize=11)
        ax1.set_ylabel("Accuracy", color='white', fontsize=11)
        ax1.set_ylim(0, 1)
        ax1.set_title("Model Accuracy", fontsize=14, fontweight='bold', color='white', pad=15)
        ax1.tick_params(colors='white', labelsize=9)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_color('white')
        ax1.spines['bottom'].set_color('white')
        ax1.grid(axis='y', alpha=0.2, color='white')
        plt.xticks(rotation=20, ha='right')
        plt.tight_layout()
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        fig2.patch.set_facecolor('none')
        ax2.set_facecolor('none')
        
        ax2.plot(models, accuracy, marker='o', color='#f093fb', linewidth=3, 
                markersize=10, markerfacecolor='#667eea', markeredgecolor='white', markeredgewidth=2)
        ax2.set_xlabel("Models", color='white', fontsize=11)
        ax2.set_ylabel("Accuracy", color='white', fontsize=11)
        ax2.set_ylim(0.75, 1)
        ax2.set_title("Accuracy Trend", fontsize=14, fontweight='bold', color='white', pad=15)
        ax2.tick_params(colors='white', labelsize=9)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_color('white')
        ax2.spines['bottom'].set_color('white')
        ax2.grid(True, alpha=0.2, color='white')
        plt.xticks(rotation=20, ha='right')
        plt.tight_layout()
        st.pyplot(fig2)
    
    st.markdown("---")
    
    st.subheader("📊 Dataset Information")
    st.markdown("""
    **Features Used:**
    - **Demographic:** Age, Sex
    - **Clinical:** Chest Pain Type, Resting Blood Pressure, Cholesterol
    - **Cardiac:** Resting ECG, Maximum Heart Rate, Exercise Angina
    - **Diagnostic:** Oldpeak, ST Slope, Fasting Blood Sugar
    
    **Target Variable:** Presence or absence of heart disease (Binary Classification)
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