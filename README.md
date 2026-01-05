WebLogAnalysis — SOC-Grade Log Anomaly Detection

WebLogAnalysis is a SOC-grade web log analysis system that detects malicious, suspicious, rejected, and legitimate web access logs using a combination of:

Unsupervised Machine Learning

Rule-based security validation

HTTP-aware log analysis

Explainability (reason + confidence)

Analyst-friendly web UI

This project follows real-world SOC / SIEM architecture principles, where ML is used only for anomaly detection, while rules provide validation, explainability, and trust.

🔐 Key Features (What Makes This SOC-Grade)
1️⃣ Hybrid Detection Architecture

Machine Learning (Isolation Forest, LOF, One-Class SVM)
→ Used strictly for anomaly detection

Rule-based engine
→ Used for validation, explanation, and confidence scoring

ML feature space is kept exactly the same as training time to avoid model drift.

2️⃣ Rule-Based Validation (Input Hygiene)

Invalid logs such as:

aaa
abcde
randomtext


are not silently dropped

They are explicitly marked as:

Status: Rejected
Reason: Invalid or unsupported log format
Confidence: 100%


This mirrors real SOC / SIEM behavior.

3️⃣ HTTP-Aware Analysis (Without Breaking ML)

The system extracts (for rules only):

HTTP Method (GET / POST / PUT / DELETE)

Path (/admin, /login, /wp-admin, etc.)

Status codes (401, 403, 500)

Protocol (HTTP / HTTPS)

These fields are NOT fed into ML, but are used for:

Reason tagging

Confidence scoring

Analyst explanations

4️⃣ Explainable Results (Analyst-Friendly)

Every log displayed in the UI includes:

Status: Normal | Anomaly | Rejected

Reason (e.g. Sensitive endpoint access)

Confidence score (dynamic, not hardcoded)

Protocol (HTTP / HTTPS)

No “black-box” output.

5️⃣ File Upload Support (Production-Safe)

Supports .log and .txt files

Handles UTF-8 and Latin-1 encoding

Prevents crashes due to binary or mis-encoded files

Mirrors real log ingestion pipelines

6️⃣ Web UI (SOC-Style)

Paste logs or upload files

Color-coded results:

✅ Normal

❌ Anomaly

⛔ Rejected

Clear visibility — no hidden logs
🚀 Getting Started
Prerequisites

Python 3.8+

pip

Virtual environment (recommended)

Installation

cd WebLogAnalysis
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt

▶️ Running the Application
Start the Flask App
cd flask_app
python app.py


Open browser:

http://127.0.0.1:5000

🧪 Example Inputs & Outputs
Invalid Input
abcde


Output:

Status: Rejected
Reason: Invalid or unsupported log format
Confidence: 100%

Suspicious Access
203.0.113.10 - - [10/Oct/2024:14:10:01] "GET /admin HTTP/1.1" 403


Output:

Status: Anomaly
Reason: Sensitive endpoint access, Error response pattern
Confidence: High (dynamic)

Normal Access
203.0.113.10 - - [10/Oct/2024:14:10:03] "GET /index.html HTTP/1.1" 200


Output:

Status: Normal
Confidence: Low

🧠 Design Philosophy (Important)

ML is not trusted blindly.
ML detects anomalies.
Rules explain them.
UI shows everything.

This design aligns with:

SOC analyst workflows

SIEM platforms (Splunk, Elastic, QRadar)

Interview expectations for security roles

🧩 Future Enhancements

Severity levels (Low / Medium / High / Critical)

MITRE ATT&CK mapping

IP reputation scoring

Alert aggregation

CSV / JSON export

Dashboard metrics