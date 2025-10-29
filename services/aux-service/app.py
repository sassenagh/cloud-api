from flask import Flask, jsonify, request
import os
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

AUX_VERSION = os.getenv("AUX_VERSION", "0.1.0")
AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")

# AWS clients
s3_client = boto3.client("s3", region_name=AWS_REGION)
ssm_client = boto3.client("ssm", region_name=AWS_REGION)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "aux_version": AUX_VERSION})


@app.route("/list-buckets", methods=["GET"])
def list_buckets():
    """S3 buckets"""
    try:
        response = s3_client.list_buckets()
        buckets = [{"name": b["Name"]} for b in response.get("Buckets", [])]
    except ClientError as e:
        return jsonify({"error": str(e), "aux_version": AUX_VERSION}), 500

    return jsonify({"buckets": buckets, "aux_version": AUX_VERSION})


@app.route("/list-parameters", methods=["GET"])
def list_parameters():
    """All parameters from Parameter Store"""
    try:
        response = ssm_client.describe_parameters()
        parameters = [{"name": p["Name"]} for p in response.get("Parameters", [])]
    except ClientError as e:
        return jsonify({"error": str(e), "aux_version": AUX_VERSION}), 500

    return jsonify({"parameters": parameters, "aux_version": AUX_VERSION})


@app.route("/get-parameter", methods=["GET"])
def get_parameter():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "name query parameter is required"}), 400
    try:
        response = ssm_client.get_parameter(Name=name, WithDecryption=True)
        value = response["Parameter"]["Value"]
    except ClientError as e:
        return jsonify({"error": str(e), "aux_version": AUX_VERSION}), 500

    return jsonify({"name": name, "value": value, "aux_version": AUX_VERSION})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
