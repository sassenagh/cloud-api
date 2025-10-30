# 🌩️ Cloud API

This repository implements a **microservices-based cloud project** built with **Python (Flask)**, **Terraform**, **Kubernetes**, **Argo CD**, and **GitHub Actions (OIDC)**.  
It’s designed for a full CI/CD pipeline from source to AWS deployment, with modular infrastructure and environment separation (`dev` / `prod`).

---

## 🏗️ Project Overview

This project includes:

| Layer                      | Description                                                                 |
|---------------------------|------------------------------------------------------------------------------|
| **Infrastructure (Terraform)** | Creates AWS S3 buckets, Parameter Store keys, and IAM service accounts.     |
| **Microservices (Flask)**      | `main-api` and `aux-service`, communicating via internal network or Kubernetes service. |
| **CI/CD (GitHub Actions)**     | Builds and pushes Docker images to ECR using OpenID Connect (no static credentials). |
| **Deployment (Kubernetes)**    | Deploys both services using ConfigMaps, Secrets, and Namespaces for `dev` and `prod`. |

---

## 🧩 Architecture

+-------------------------------+
| main-api (Flask) |
| - /buckets, /parameters |
| - Calls aux-service |
+---------------+---------------+
|
v
+-------------------------------+
| aux-service (Flask) |
| - Interacts with AWS APIs |
| - Lists S3, ParameterStore |
+-------------------------------+

Managed via Kubernetes (dev / prod namespaces)
Provisioned AWS Resources (via Terraform)

---

## 🗂️ Repository Structure

cloud-api/
├── services/
│ ├── main-api/
│ │ ├── app.py
│ │ ├── requirements.txt
│ │ └── Dockerfile
│ └── aux-service/
│ ├── app.py
│ ├── requirements.txt
│ └── Dockerfile
├── terraform/
│ ├── modules/
│ │ ├── s3_bucket/
│ │ ├── parameter_store/
│ │ └── iam_service_role/
│ └── envs/
│ ├── dev/
│ └── prod/
├── k8s/
│ ├── main-api/
│ │ ├── deployment.yaml
│ │ ├── service.yaml
│ │ ├── ingress.yaml
│ │ ├── configmap-dev.yaml
│ │ ├── configmap-prod.yaml
│ │ ├── secrets-dev.yaml
│ │ └── secrets-prod.yaml
│ └── aux-service/
│ ├── deployment.yaml
│ ├── service.yaml
│ ├── configmap-dev.yaml
│ ├── configmap-prod.yaml
│ ├── secrets-dev.yaml
│ └── secrets-prod.yaml
├── .github/
│ └── workflows/
│ └── ci-build-push.yaml
├── docker-compose.yml
├── Makefile
└── README.md


---

## 🚀 Setup Instructions

### 1️⃣ Prerequisites
Make sure you have:
- Docker & Docker Desktop (Kubernetes enabled)
- Terraform ≥ 1.3
- AWS CLI configured (or OIDC role ready)
- kubectl & (optionally) Argo CD
- GitHub repository with **OIDC role** configured in AWS

### 2️⃣ Infrastructure Setup (Terraform)
You can test infrastructure locally (without real AWS credentials):
```bash
docker run --rm -it \
  -v $(pwd)/terraform:/workspace \
  -w /workspace/envs/dev \
  -e AWS_ACCESS_KEY_ID=fake \
  -e AWS_SECRET_ACCESS_KEY=fake \
  -e AWS_DEFAULT_REGION=eu-west-1 \
  hashicorp/terraform:1.13.4 init
```

To plan or apply (only with real credentials):
```bash
  terraform plan
  terraform apply
```

## ⚙️ Important Notes

AWS_ROLE_ARN must be added as a repository secret before executing any GitHub Action workflow.

AWS_REGION can be set in environment variables or parameterized via workflow_dispatch in GitHub Actions.

Each service has its own Dockerfile inside the services/ directory:

services/main-api/Dockerfile

services/aux-service/Dockerfile

Docker images are versioned with :latest and the commit SHA for traceability.

## ✅ Tip: Make sure you’ve run make build at least once before deploying to ensure Docker images are up to date.


## 🧩 Development & Production Setup

### 🚀 Start the development environment
```bash
make up
```

### 🚀 Start the production environment
```bash
make ENV=prod up
```

### 📜 View logs
```bash
make logs
```

### 🛑 Stop all containers
```bash
make down
```

### 3️⃣ Local Development with Docker Compose
You can run both services locally for dev environment:
```bash
  export APP_ENV=dev
  docker compose up --build
```

Visit:

Main API: http://localhost:5000/health
Aux Service: http://localhost:5001/health

### 4️⃣ Kubernetes Deployment (Local or Cloud)

If using Docker Desktop (with Kubernetes enabled):
```bash
  kubectl apply -f k8s/aux-service/ -n dev
  kubectl apply -f k8s/main-api/ -n dev
  kubectl get pods --all-namespaces
```
Expose a service to test it:
```bash
  kubectl port-forward svc/main-api 5000:80
```
Then open http://localhost:5000/health


### 5️⃣ CI/CD (GitHub Actions + ECR)

The workflow .github/workflows/ci-build-push.yml:

Uses OIDC to authenticate to AWS securely (no static keys)

Builds and pushes both Docker images to ECR

Can be triggered automatically on push main or manually

Set these GitHub secrets before running:

| Secret Name   | Description |
|----------------|-------------|
| `AWS_ROLE_ARN` | ARN of IAM role trusted for OIDC (e.g., `arn:aws:iam::123456789012:role/cloud-api-github-oidc-role`) |
| `AWS_REGION`   | AWS region (e.g., `eu-west-1`) |
| `ECR_REGISTRY` | ECR registry URI (e.g., `123456789012.dkr.ecr.eu-west-1.amazonaws.com`) |


Example of workflow section
```yaml
- name: Configure AWS credentials via OIDC
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
    aws-region: ${{ secrets.AWS_REGION }}
```

## 🧾 License

MIT License © 2025 — sassenagh
