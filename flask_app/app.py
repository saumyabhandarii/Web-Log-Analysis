import joblib
import numpy as np
import re
from flask import Flask, request, jsonify, render_template

# =============================
# Log Validation Regex
# =============================
LOG_PATTERN = re.compile(
    r'^\S+ \S+ \S+ \[[^\]]+\] "\w+ .+ HTTP/\d\.\d" \d+'
)

def is_valid_log(line):
    return bool(LOG_PATTERN.match(line))


# =============================
# Flask App
# =============================
app = Flask(__name__)


# =============================
# Load Models (DO NOT CHANGE)
# =============================
iso_forest = joblib.load('../models/iso_forest_model.pkl')
lof = joblib.load('../models/lof_model.pkl')
oc_svm = joblib.load('../models/oc_svm_model.pkl')
tfidf = joblib.load('../models/tfidf_vectorizer.pkl')


# =============================
# Feature Extraction (ML ONLY)
# =============================
def extract_features(log_data):
    tfidf_features = tfidf.transform(log_data).toarray()
    level_encoded = np.zeros((len(log_data), 1))  # EXACT same as training
    return np.hstack((level_encoded, tfidf_features))


# =============================
# HTTP Parsing (RULES ONLY)
# =============================
def parse_http_features(log):
    try:
        request_part = log.split('"')[1]
        method, path, _ = request_part.split()
        status = int(log.split()[-1])
        protocol = "HTTPS" if "HTTPS" in log else "HTTP"
        return method, path, status, protocol
    except:
        return "UNKNOWN", "/", 0, "N/A"


def get_reason(method, path, status):
    reasons = []

    if path in ["/admin", "/login", "/wp-admin"]:
        reasons.append("Sensitive endpoint access")

    if ".." in path:
        reasons.append("Path traversal attempt")

    if status >= 400:
        reasons.append("Error response pattern")

    if method in ["POST", "PUT", "DELETE"]:
        reasons.append("High-risk HTTP method")

    if not reasons:
        reasons.append("Statistical anomaly")

    return reasons


def calculate_confidence(reasons, rejected=False):
    if rejected:
        return 100

    base = 40
    base += len(reasons) * 15
    return min(base, 98)


# =============================
# SOC-Grade Analyzer
# =============================
def analyze_logs(raw_logs):

    results = []

    # Validate logs first
    valid_logs = []
    index_map = []

    for i, log in enumerate(raw_logs):
        if is_valid_log(log):
            valid_logs.append(log)
            index_map.append(i)
        else:
            results.append({
                "log": log,
                "status": "Rejected",
                "protocol": "N/A",
                "reason": "Invalid or unsupported log format",
                "confidence": 100
            })

    if not valid_logs:
        return results

    # ML prediction (unchanged)
    features = extract_features(valid_logs)
    final_labels = np.array(["Anomaly"] * len(valid_logs))

    pred_iso = iso_forest.predict(features)
    normal_idx = np.where(pred_iso == 1)[0]

    if len(normal_idx) > 0:
        X_refined = features[normal_idx]

        if X_refined.shape[0] >= 2:
            pred_lof = lof.fit_predict(X_refined)
            normal_idx = normal_idx[pred_lof == 1]

        if len(normal_idx) > 0:
            pred_svm = oc_svm.predict(features[normal_idx])
            for i, idx in enumerate(normal_idx):
                if pred_svm[i] == 1:
                    final_labels[idx] = "Normal"

    # Build SOC output
    for i, log in enumerate(valid_logs):
        method, path, status, protocol = parse_http_features(log)
        reasons = get_reason(method, path, status)
        confidence = calculate_confidence(reasons)

        results.append({
            "log": log,
            "status": final_labels[i],
            "protocol": protocol,
            "reason": ", ".join(reasons),
            "confidence": confidence
        })

    return results


# =============================
# Routes
# =============================
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    # ---------- FILE UPLOAD (SAFE DECODING) ----------
    if 'logfile' in request.files:
        file = request.files['logfile']
        filename = file.filename

        if not filename.endswith(('.log', '.txt')):
            return jsonify({"error": "Only .log or .txt files are supported"})

        file_bytes = file.read()

        try:
            logs = file_bytes.decode("utf-8").splitlines()
        except UnicodeDecodeError:
            logs = file_bytes.decode("latin-1", errors="ignore").splitlines()

    # ---------- TEXT INPUT ----------
    elif 'logcontent' in request.form:
        logs = request.form['logcontent'].splitlines()

    else:
        return jsonify({"error": "No input provided"})

    results = analyze_logs(logs)
    return jsonify({"predictions": results})


# =============================
# Run App
# =============================
if __name__ == '__main__':
    app.run(debug=True)
