FROM python:3.11-slim
WORKDIR /app

COPY requirements.text .
COPY shared-keys/public_key.pem /keys/public_key.pem
RUN pip install --no-cache-dir -r requirements.text

COPY api/tascal/ .
EXPOSE 8080
CMD ["python","run.py"]