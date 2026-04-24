FROM python:3.12-slim

WORKDIR /app

# Layer caching for dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Security: non-root user
RUN useradd -m backenduser
USER backenduser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
