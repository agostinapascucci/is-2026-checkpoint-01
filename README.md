# is-2026-checkpoint-01
Repositorio destinado al Trabajo Práctico Checkpoint 01 para la cátedra Ingeniería y Calidad de Software - Comisión S41 - Año 2026

## Descripción

TeamBoard es una aplicación compuesta por frontend, backend y base de datos PostgreSQL, ejecutada con Docker Compose.

El proyecto también incluye Portainer como panel de monitoreo para administrar y visualizar los contenedores del entorno local.

## Requisitos

- Docker
- Docker Compose
- Archivo `.env` creado a partir de `.env.example`

El archivo `.env` debe definir las variables necesarias para levantar los servicios. Para Portainer, debe incluir:

```env
PORTAINER_PORT=9000
```

También deben estar definidas las variables de PostgreSQL y los puertos del frontend y backend.

## Levantar el proyecto

Desde la raíz del repositorio, ejecutar:

```bash
docker compose up -d
```

Para verificar los contenedores activos:

```bash
docker compose ps
```

Los servicios esperados son:

- `teamboard-frontend`
- `teamboard-backend`
- `teamboard-database`
- `teamboard-portainer`

Para detener el proyecto:

```bash
docker compose down
```

## Portainer

Portainer es una herramienta web para monitorear y administrar contenedores Docker. En este proyecto se utiliza para visualizar el estado del stack local de TeamBoard.

El servicio está definido en `docker-compose.yml` con la imagen `portainer/portainer-ce` y utiliza un volumen persistente para conservar su configuración.

También monta el socket de Docker:

```text
/var/run/docker.sock
```

Esto permite que Portainer pueda detectar y administrar los contenedores locales.

## Acceso a Portainer

Con el proyecto levantado, acceder desde el navegador a:

```text
http://localhost:${PORTAINER_PORT}
```

Si `PORTAINER_PORT=9000`, la URL es:

```text
http://localhost:9000
```

## Primera configuración de Portainer

Al ingresar por primera vez:

1. Crear el usuario administrador.
2. Seleccionar el entorno Docker local.
3. Confirmar la conexión con el entorno local.
4. Ingresar al panel de contenedores.

Desde Portainer se deben poder ver los contenedores:

- `teamboard-frontend`
- `teamboard-backend`
- `teamboard-database`
- `teamboard-portainer`

## Evidencia y capturas

Las capturas deben agregarse cuando estén disponibles.

Placeholders sugeridos:

- Captura de acceso a Portainer: `portainer/captura-acceso-portainer.png`
- Captura del entorno Docker local seleccionado: `portainer/captura-entorno-local.png`
- Captura de contenedores visibles: `portainer/captura-contenedores.png`

Hasta que existan las imágenes, esta sección queda como referencia para completar la evidencia del checkpoint.
