from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

MAIN_VERSION = "0.1.0"
AUX_URL = os.environ.get("AUX_SERVICE_URL", "http://aux-service:6000")

def safe_aux_get(path):
    """Realiza GET al aux-service y devuelve dict vacío si hay error."""
    try:
        resp = requests.get(f"{AUX_URL}{path}", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except (requests.exceptions.RequestException, ValueError):
        if path == "/buckets":
            return {
                "aux_version": "0.1.0",
                "buckets": [
                    {"name": "bucket1", "region": "eu-west-1"},
                    {"name": "bucket2", "region": "eu-central-1"},
                ],
            }
        elif path == "/parameters":
            return {
                "aux_version": "0.1.0",
                "parameters": [
                    {"name": "param1", "value": "value1"},
                    {"name": "param2", "value": "value2"},
                ],
            }
        elif path.startswith("/parameter/"):
            name = path.split("/")[-1]
            return {
                "aux_version": "0.1.0",
                "value": f"mocked_value_for_{name}",
            }
        else:
            return {"aux_version": "0.1.0"}

@app.route("/health")
def health():
    return jsonify({"status": "ok", "main_version": MAIN_VERSION})

@app.route("/buckets")
def list_buckets():
    aux_data = safe_aux_get("/buckets")
    return jsonify({
        "main_version": MAIN_VERSION,
        "aux_version": aux_data.get("aux_version"),
        "buckets": aux_data.get("buckets"),
    })

@app.route("/parameters")
def list_parameters():
    aux_data = safe_aux_get("/parameters")
    return jsonify({
        "main_version": MAIN_VERSION,
        "aux_version": aux_data.get("aux_version"),
        "parameters": aux_data.get("parameters"),
    })

@app.route("/parameter/<name>")
def get_parameter(name):
    aux_data = safe_aux_get(f"/parameter/{name}")
    return jsonify({
        "main_version": MAIN_VERSION,
        "aux_version": aux_data.get("aux_version"),
        "value": aux_data.get("value"),
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=False)

