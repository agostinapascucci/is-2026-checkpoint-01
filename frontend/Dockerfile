# ── Feature 02: Frontend ──────────────────────────────────────
# Imagen base slim con versión fija (buena práctica obligatoria)
FROM python:3.12-slim

# Metadatos del servicio
LABEL maintainer="Sobrinos de Uncle Bob"
LABEL service="teamboard-frontend"

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del sitio estático
COPY html/ ./html/

# Crear usuario no-root y asignarle los archivos
RUN addgroup --system appgroup && \
    adduser  --system --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app

# Cambiar al usuario sin privilegios
USER appuser

# Exponer el puerto del servidor HTTP de Python
EXPOSE 8080

# Health check: verifica que el servidor responda
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080')" || exit 1

# Comando principal: servidor HTTP estático de Python
CMD ["python3", "-m", "http.server", "8080", "--directory", "html"]
