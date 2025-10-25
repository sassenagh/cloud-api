from flask import Flask, jsonify, request
import os

app = Flask(__name__)

AUX_VERSION = os.getenv("AUX_VERSION", "0.1.0")


@app.route("/health", methods=["GET"])
def health():
    """Comprueba si el servicio está vivo"""
    return jsonify({
        "status": "ok",
        "aux_version": AUX_VERSION
    })


@app.route("/list-buckets", methods=["GET"])
def list_buckets():
    """Devuelve una lista simulada de buckets S3"""
    buckets = ["mock-bucket-1", "mock-bucket-2"]
    return jsonify({
        "buckets": buckets,
        "aux_version": AUX_VERSION
    })


@app.route("/list-parameters", methods=["GET"])
def list_parameters():
    """Devuelve una lista simulada de parámetros en SSM"""
    parameters = ["/app/config/db_url", "/app/config/secret_key"]
    return jsonify({
        "parameters": parameters,
        "aux_version": AUX_VERSION
    })


@app.route("/get-parameter", methods=["GET"])
def get_parameter():
    """Devuelve un parámetro específico"""
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "name query parameter is required"}), 400

    value = f"mock-value-for-{name}"
    return jsonify({
        "name": name,
        "value": value,
        "aux_version": AUX_VERSION
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, threaded=False)
