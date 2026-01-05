# 🔐 Web Log Anomaly Detection (SOC-Grade)

An AI-powered **SOC-style Web Log Anomaly Detection System** that analyzes HTTP access logs using a **hybrid detection approach** combining **unsupervised machine learning** and **rule-based security heuristics**.

This project simulates how modern **Security Operations Centers (SOC)** detect suspicious web activity, enrich alerts with context, and assign confidence scores for analyst decision-making.

---

## 👤 Author

**Saumya Singh**  
Cybersecurity & SOC Enthusiast  
GitHub: https://github.com/saumyabhandarii

---

## 🎯 Project Objectives

- Detect anomalous and malicious web requests from access logs  
- Mimic real-world **SIEM / SOC detection pipelines**
- Combine **ML-based anomaly detection** with **security rules**
- Provide **explainable alerts** with reasons and confidence levels
- Build a **resume-worthy cybersecurity project**

---

---

## 🧠 Detection Techniques Used

### 🔹 Machine Learning (Unsupervised)
- Isolation Forest
- Local Outlier Factor (LOF)
- One-Class SVM
- TF-IDF Vectorization for log text

### 🔹 Rule-Based Security Logic
- Sensitive endpoint access (`/admin`, `/login`, `/wp-admin`)
- Path traversal attempts (`../`)
- High-risk HTTP methods (`POST`, `PUT`, `DELETE`)
- Error response patterns (`4xx`, `5xx`)
- Invalid or malformed log rejection

---

## 📊 Output Format (SOC-Style)

Each log entry is classified with:
- **Status**: Normal / Anomaly / Rejected
- **Protocol**: HTTP / HTTPS
- **Reason**: Human-readable explanation
- **Confidence Score**: Percentage likelihood of malicious behavior

---

## 🖥️ Tech Stack

- **Backend**: Python, Flask
- **ML Stack**: scikit-learn, NumPy, joblib
- **Frontend**: HTML, CSS (Dark SOC-style UI)
- **Models**: Pre-trained `.pkl` models
- **Environment**: Python Virtual Environment

---

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/saumyabhandarii/Web-Log-Analysis.git
cd Web-Log-Analysis
2️⃣ Create & Activate Virtual Environment
python -m venv .venv
.venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Flask App
cd flask_app
python app.py

5️⃣ Open in Browser
http://127.0.0.1:5000/

🧪 Sample Log Input
127.0.0.1 - - [10/Oct/2025:13:55:36 +0000] "GET /index.html HTTP/1.1" 200
192.168.1.10 - - [10/Oct/2025:13:56:01 +0000] "POST /login HTTP/1.1" 401
203.0.113.5 - - [10/Oct/2025:13:57:15 +0000] "GET /admin HTTP/1.1" 403
198.51.100.23 - - [10/Oct/2025:13:58:42 +0000] "GET /../../etc/passwd HTTP/1.1" 404

⚠️ Notes on Model Versions

Models were trained using scikit-learn 1.6.0

Running on newer versions may show warnings but functionality remains intact

For full compatibility:

pip install scikit-learn==1.6.0

🔮 Future Enhancements

Severity levels (LOW / MEDIUM / HIGH)

MITRE ATT&CK technique mapping

Alert deduplication & incident grouping

CSV / JSON export for SOC reporting

Baseline learning to reduce false positives

Dashboard analytics & charts

📌 Why This Project Matters

This project demonstrates:

Real SOC detection logic

Hybrid ML + rule-based security design

Explainable anomaly detection

Practical cybersecurity engineering skills

It is not a toy project — it reflects real-world SOC workflows.
## 🏗️ Architecture Overview

