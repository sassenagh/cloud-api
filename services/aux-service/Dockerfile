FROM python:3.11-slim

RUN useradd -m appuser

WORKDIR /app

ENV PIP_NO_INPUT=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_PROGRESS_BAR=off

RUN python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt || true

COPY . .

USER appuser

EXPOSE 5001

CMD ["python", "app.py"]
