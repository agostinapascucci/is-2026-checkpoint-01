CREATE TABLE IF NOT EXISTS members (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    legajo VARCHAR(20) NOT NULL,
    feature VARCHAR(100) NOT NULL,
    servicio VARCHAR(100) NOT NULL,
    estado VARCHAR(50) NOT NULL
);

INSERT INTO members (nombre, apellido, legajo, feature, servicio, estado)
VALUES
    ('Agostina', 'Pascucci', '33347', 'Coordinación, Infraestructura Base y README', 'compose/readme', 'running'),
    ('Agustina', 'Egüen', '33191', 'Frontend — Página Web con HTML y JavaScript', 'frontend', 'running'),
    ('Joaquin', 'Montes', '33459', 'Backend — API REST con Python y Flask', 'backend', 'running'),
    ('Santiago', 'Talavera', '33167', 'Base de Datos con PostgreSQL', 'database', 'running'),
    ('Nicolas', 'Perez', '33177', 'Panel de Monitoreo con Portainer', 'portainer', 'running'),
    ('Justina', 'Smith', '33346', 'Feature adicional', 'sin definir', 'running');