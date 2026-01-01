# ❤️ Heart Disease Prediction System (ML + Streamlit)

An AI-powered clinical decision support system that predicts heart disease risk using multiple machine learning models.  
The application provides **real-time predictions**, **model explainability**, and **auto-generated medical reports** in a user-friendly web interface.

---

## 🚀 Live Demo

 [Heart Disease Prediction App](https://heart-failure-prediction-ml-by-purbashis.streamlit.app/)


---

## 🧠 Project Overview

This project uses an ensemble of machine learning models to assess the risk of heart disease based on clinical and physiological parameters such as age, blood pressure, cholesterol levels, ECG results, and exercise-induced angina.

The goal is to provide:
- Quick screening support
- Clear risk interpretation
- Explainable ML outputs
- Clinically readable reports

---

## 🛠️ Tech Stack

- **Language:** Python
- **Machine Learning:** Scikit-learn
- **Models:**  
  - Logistic Regression  
  - Decision Tree  
  - Random Forest  
  - Support Vector Machine (SVM)
- **Web Framework:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib
- **Reporting:** ReportLab (PDF generation)
- **Deployment:** Streamlit Cloud

---

## 📊 Features

### 🔍 Single Patient Prediction
- Input patient clinical details
- Predict heart disease risk using multiple models
- Displays individual model predictions
- Shows overall risk percentage

### 📂 Bulk Prediction
- Upload CSV file with patient data
- Batch predictions for multiple patients
- Download prediction results as CSV

### 🧠 Model Explainability
- Uses **Random Forest feature importance** for clear and stable explainability
- Displays feature contribution rankings
- Designed for production reliability

> ℹ️ SHAP explainability was used during offline model analysis.  
> Feature importance is used in the deployed application for stability and clarity.

### 📄 Auto-Generated Medical Report (PDF)
- Human-readable patient summary
- Interpreted clinical values (not raw encodings)
- Risk assessment and key observations
- Doctor-friendly format
- Downloadable prescription-style report

---

## 📈 Model Performance

| Model | Accuracy |
|-----|---------|
| Decision Tree | ~84% |
| Logistic Regression | ~86% |
| Random Forest | ~91% |
| Support Vector Machine | ~88% |

---

## 📊 Input Features

- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate
- Exercise-Induced Angina
- Oldpeak (ST Depression)
- ST Segment Slope

---

## ⚠️ Disclaimer

This application is intended for **educational and research purposes only**.  
It is **not a medical diagnostic tool**.  
Always consult a qualified healthcare professional for medical decisions.

---

## 👨‍💻 Author

**Purbashis Behera**  
Software Engineer | Machine Learning & AI Enthusiast  

📧 Email: purbashis21@gmail.com  

🔗 **LinkedIn:** [purbashis-behera](https://www.linkedin.com/in/purbashis-behera-079a07190/)


---

## ⭐ If you find this project useful
Please consider giving it a ⭐ on GitHub!
