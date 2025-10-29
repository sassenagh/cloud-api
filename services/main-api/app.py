from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

MAIN_VERSION = "0.1.0"
AUX_URL = os.environ.get("AUX_SERVICE_URL", "http://aux-service:5001")  # puerto real de aux

def safe_aux_get(path):
    """GET request to aux-service, returns void if an error happnens"""
    try:
        resp = requests.get(f"{AUX_URL}{path}", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except (requests.exceptions.RequestException, ValueError):
        return {"aux_version": "unknown", "error": "failed to reach aux-service"}

@app.route("/health")
def health():
    return jsonify({"status": "ok", "main_version": MAIN_VERSION})

@app.route("/buckets")
def list_buckets():
    aux_data = safe_aux_get("/list-buckets")
    return jsonify({
        "main_version": MAIN_VERSION,
        "aux_version": aux_data.get("aux_version"),
        "buckets": aux_data.get("buckets"),
    })

@app.route("/parameters")
def list_parameters():
    aux_data = safe_aux_get("/list-parameters")
    return jsonify({
        "main_version": MAIN_VERSION,
        "aux_version": aux_data.get("aux_version"),
        "parameters": aux_data.get("parameters"),
    })

@app.route("/parameter/<name>")
def get_parameter(name):
    aux_data = safe_aux_get(f"/get-parameter?name={name}")
    return jsonify({
        "main_version": MAIN_VERSION,
        "aux_version": aux_data.get("aux_version"),
        "value": aux_data.get("value"),
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
