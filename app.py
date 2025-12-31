import streamlit as st
import pickle
import pandas as pd
import os
import matplotlib.pyplot as plt


st.set_page_config(page_title="Heart Disease Prediction", layout="centered")
st.title("❤️ Heart Disease Prediction")

tab1, tab2, tab3, tab4 = st.tabs(
    ['Predict', 'Bulk Predict', 'Model Information', 'About Me']
)

# -------------------- MODEL CONFIG --------------------
algorithm = [
    "Decision Tree Classifier",
    "Logistic Regression",
    "Random Forest Classifier",
    "Support Vector Machine"
]

modelnames = [
    'tree.pkl',
    'LogisticRegression.pkl',
    'RandomForest.pkl',
    'SVM.pkl'
]


# -------------------- PREDICTION FUNCTION --------------------
def predict_heart_disease(data):
    predictions = []

    for modelname in modelnames:
        if not os.path.exists(modelname) or os.path.getsize(modelname) == 0:
            predictions.append("Model Error")
            continue

        try:
            with open(modelname, "rb") as file:
                model = pickle.load(file)
                pred = model.predict(data)
                predictions.append(pred[0])
        except Exception:
            predictions.append("Model Error")

    return predictions


# -------------------- TAB 1 : SINGLE PREDICTION --------------------
with tab1:
    st.header("🧑‍⚕️ Single Patient Prediction")

    # ---------------- INPUTS ----------------
    age = st.number_input("Age (years)", 0, 150, 25)
    sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Male" if x else "Female")
    chest_pain = st.selectbox(
        "Chest Pain Type",
        [0, 1, 2, 3],
        format_func=lambda x: {
            0: "Typical Angina",
            1: "Atypical Angina",
            2: "Non-Anginal Pain",
            3: "Asymptomatic"
        }[x]
    )
    resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 0, 300, 120)
    cholesterol = st.number_input("Cholesterol (mg/dl)", 0, 1000, 200)
    fasting_bs = st.selectbox(
        "Fasting Blood Sugar > 120 mg/dl",
        [0, 1],
        format_func=lambda x: "Yes" if x else "No"
    )
    resting_ecg = st.selectbox(
        "Resting ECG",
        [0, 1, 2],
        format_func=lambda x: {
            0: "Normal",
            1: "ST-T wave abnormality",
            2: "Left ventricular hypertrophy"
        }[x]
    )
    max_hr = st.number_input("Maximum Heart Rate Achieved", 60, 202, 150)
    exercise_angina = st.selectbox(
        "Exercise Induced Angina",
        [0, 1],
        format_func=lambda x: "Yes" if x else "No"
    )
    oldpeak = st.number_input("Oldpeak", 0.0, 10.0, 1.0, step=0.1)
    st_slope = st.selectbox(
        "ST Slope",
        [0, 1, 2],
        format_func=lambda x: {
            0: "Upsloping",
            1: "Flat",
            2: "Downsloping"
        }[x]
    )

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

    # ---------------- PREDICTION ----------------
    if st.button("🔍 Submit"):
        st.subheader("📊 Prediction Results")
        st.markdown("---")

        results = predict_heart_disease(input_data)

        valid_preds = [r for r in results if r in [0, 1]]
        risk_percentage = (sum(valid_preds) / len(valid_preds)) * 100 if valid_preds else 0

        # ---------- SIDE BY SIDE GRAPH ----------
        col1, col2 = st.columns(2)

        with col1:
            fig1, ax1 = plt.subplots()
            ax1.bar(algorithm, valid_preds)
            ax1.set_ylim(0, 1)
            ax1.set_title("Model-wise Prediction")
            ax1.set_ylabel("0 = No Disease | 1 = Disease")
            st.pyplot(fig1)

        with col2:
            fig2, ax2 = plt.subplots()
            ax2.pie(
                [risk_percentage, 100 - risk_percentage],
                labels=["Risk", "No Risk"],
                autopct="%1.1f%%",
                startangle=90
            )
            ax2.set_title("Overall Risk Agreement")
            st.pyplot(fig2)

        st.markdown("---")

        # ---------- MODEL OUTPUT ----------
        for model_name, prediction in zip(algorithm, results):
            st.markdown(f"### 🧠 {model_name}")

            if prediction == "Model Error":
                st.warning("⚠️ Model could not be loaded")
            elif prediction == 0:
                st.success("✅ No Heart Disease Detected")
            else:
                st.error("🚨 Heart Disease Detected")

        st.markdown("---")

        # ---------- DEEP PATIENT FEEDBACK ----------
        st.subheader("🩺 Patient Health Insight")

        st.metric("Overall Risk Percentage", f"{risk_percentage:.1f}%")

        if risk_percentage >= 60:
            st.error("""
            🔴 **High Risk Detected**

            Multiple models indicate a strong possibility of heart disease.
            It is strongly recommended to consult a cardiologist.
            """)
        elif risk_percentage >= 30:
            st.warning("""
            🟡 **Moderate Risk Detected**

            Some indicators suggest possible heart-related issues.
            Lifestyle changes and medical consultation are advised.
            """)
        else:
            st.success("""
            🟢 **Low Risk Detected**

            Current indicators suggest low heart disease risk.
            Maintain a healthy lifestyle and regular checkups.
            """)

        st.markdown("""
        **Health Tips**
        - Maintain healthy cholesterol levels
        - Exercise regularly
        - Avoid smoking
        - Monitor blood pressure
        - Follow a balanced diet
        """)
# -------------------- TAB 2 : BULK PREDICTION --------------------

with tab2:
    st.header("📂 Bulk Heart Disease Prediction")

    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=["csv"]
    )

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.subheader("📄 Uploaded Data Preview")
            st.dataframe(df.head())

            REQUIRED_COLUMNS = [
                'Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol',
                'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina',
                'Oldpeak', 'ST_Slope'
            ]

            if not all(col in df.columns for col in REQUIRED_COLUMNS):
                st.error("❌ CSV does not contain required columns")
            else:
                if st.button("🚀 Predict for CSV"):
                    results = predict_heart_disease(df)

                    for model_name, prediction in zip(algorithm, results):
                        df[model_name] = prediction

                    st.subheader("✅ Prediction Results")
                    st.dataframe(df)

                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "⬇️ Download Results CSV",
                        csv,
                        "heart_disease_predictions.csv",
                        "text/csv"
                    )

        except Exception as e:
            st.error(f"⚠️ Error processing file: {e}")




with tab3:
    st.header("🧠 Model Information")

    # ---------- MODEL DESCRIPTION ----------
    st.markdown("""
    ### Models Used in This Project

    **1️⃣ Decision Tree Classifier**
    - Easy to interpret
    - Fast training
    - Prone to overfitting

    **2️⃣ Logistic Regression**
    - Linear model
    - Works well with binary classification
    - Interpretable coefficients

    **3️⃣ Random Forest Classifier**
    - Ensemble of decision trees
    - High accuracy
    - Handles overfitting well

    **4️⃣ Support Vector Machine (SVM)**
    - Effective in high-dimensional space
    - Memory efficient
    - Works well with clear margin separation
    """)

    st.markdown("---")

    # ---------- DATASET INFO ----------
    st.markdown("""
    ### Dataset
    - Clinical heart disease dataset
    - Features include age, blood pressure, cholesterol, ECG, etc.
    - Target: Presence or absence of heart disease
    """)

    st.markdown("---")

    # ---------- MODEL ACCURACY DATA ----------
    model_accuracy = {
        "Decision Tree": 0.84,
        "Logistic Regression": 0.86,
        "Random Forest": 0.91,
        "SVM": 0.88
    }

    models = list(model_accuracy.keys())
    accuracy = list(model_accuracy.values())

    # ---------- BAR GRAPH ----------
    st.subheader("📊 Model Accuracy Comparison (Bar Chart)")

    fig1, ax1 = plt.subplots()
    ax1.bar(models, accuracy)
    ax1.set_xlabel("Models")
    ax1.set_ylabel("Accuracy")
    ax1.set_ylim(0, 1)
    ax1.set_title("Accuracy of Different Models")

    st.pyplot(fig1)

    # ---------- LINE GRAPH ----------
    st.subheader("📈 Model Accuracy Trend (Line Chart)")

    fig2, ax2 = plt.subplots()
    ax2.plot(models, accuracy, marker='o')
    ax2.set_xlabel("Models")
    ax2.set_ylabel("Accuracy")
    ax2.set_ylim(0, 1)
    ax2.set_title("Accuracy Trend Across Models")

    st.pyplot(fig2)

with tab4:
    st.header("👨‍💻 About Me")

    st.markdown("""
    **Purbashis Behera**

    - Software Engineer with experience in **application development**
    - Strong interest in **Machine Learning & Data Science**
    - Built this project to apply ML models to real-world healthcare data

    **Skills**
    - Python, Pandas, NumPy
    - Scikit-learn
    - Streamlit
    - Machine Learning Algorithms

    **Goal**
    - Transition into ML / AI-focused roles
    - Build intelligent, data-driven systems
    """)

    st.markdown("---")
    st.markdown("📧 **Contact:** purbashis@example.com")
