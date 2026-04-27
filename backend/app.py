import os
import psycopg2
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from psycopg2.extras import RealDictCursor
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
Swagger(app, template={
    "info": {
        "title": "TeamBoard API",
        "description": "API REST para gestión del equipo TeamBoard",
        "version": "1.0.0"
    }
})

# DB Config
DB_HOST = os.getenv("POSTGRES_HOST", "database")
DB_NAME = os.getenv("POSTGRES_DB", "teamboard")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        cursor_factory=RealDictCursor
    )

SERVICE_URLS = {
    "frontend":  "http://frontend:8080",
    "backend":   "http://localhost:5000/api/health",
    "database":  None,  # verificado via psycopg2
    "portainer": "http://portainer:9000",
    "compose/readme": None,  # no tiene endpoint propio
}

def check_service_status(servicio):
    # Si el servicio es el backend, ya sabemos que está corriendo
    # porque este mismo código se está ejecutando.
    if servicio == "backend":
        return "running"
        
    url = SERVICE_URLS.get(servicio)
    if url is None:
        return "running"  # asumido o verificado por DB
    try:
        r = requests.get(url, timeout=2)
        return "running" if r.status_code == 200 else "degraded"
    except Exception:
        return "stopped"



@app.route('/api/health')
def health():
    """
    Health check del servicio verificando la base de datos
    ---
    responses:
      200:
        description: Estado del servicio activo y conectado
        schema:
          properties:
            status:
              type: string
              example: active
      500:
        description: Error de conexión con la base de datos
        schema:
          properties:
            status:
              type: string
              example: error
            message:
              type: string
              example: Database disconnected
    """
    try:
        # Intenta conectarse a la base de datos
        conn = get_db_connection()
        conn.close()
        # Si funcionó, devuelve activo
        return jsonify({"status": "active"})
    except Exception:
        # Si falló la conexión, devuelve un error HTTP 500
        return jsonify({"status": "error", "message": "Database disconnected"}), 500


@app.route('/api/info')
def info():
    """
    Información del servicio
    ---
    responses:
      200:
        description: Nombre y versión del servicio
        schema:
          properties:
            service:
              type: string
              example: TeamBoard Backend API
            version:
              type: string
              example: 1.0.0
    """
    return jsonify({
        "service": "TeamBoard Backend API",
        "version": "1.0.0"
    })

@app.route('/api/team')
def get_team():
    """
    Obtener todos los miembros del equipo
    ---
    responses:
      200:
        description: Lista de miembros
        schema:
          type: array
          items:
            $ref: '#/definitions/Member'
      500:
        description: Error interno del servidor
    definitions:
      Member:
        type: object
        properties:
          id:
            type: integer
          nombre:
            type: string
          apellido:
            type: string
          legajo:
            type: string
          feature:
            type: string
          servicio:
            type: string
          estado:
            type: string
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM members')
        members = list(cur.fetchall())
        for m in members:
            m["estado"] = check_service_status(m["servicio"])
        cur.close()
        conn.close()
        return jsonify(members)
    except Exception as e:
        print(f"Error fetching team: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
        
@app.route('/api/team/<int:id>')
def get_member(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM members WHERE id = %s', (id,))
        member = cur.fetchone()
        cur.close()
        conn.close()

        if not member:
            return jsonify({"error": "Member not found"}), 404

        member["estado"] = check_service_status(member["servicio"])
        return jsonify(member)
    except Exception as e:
        print(f"Error fetching member: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
