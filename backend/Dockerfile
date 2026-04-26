FROM python:3.12-slim

# Instalación de curl para el healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Layer caching for dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Security: non-root user
RUN useradd -m backenduser
USER backenduser

EXPOSE 5000

# Healthcheck para verificar que el servicio esté respondiendo
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/api/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
