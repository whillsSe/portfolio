FROM python:3.11-slim
WORKDIR /app

COPY requirements.text .
COPY shared-keys/ /keys/
RUN pip install --no-cache-dir -r requirements.text

COPY auth/tascal/ .
EXPOSE 8081
CMD ["python","run.py"]