# Prueba Técnica Desarrollador Python - Cari AI

Proyecto FastAPI preparado para ejecutarse en Docker con recarga automática
para entorno de desarrollo.


## Requisitos

- Docker Desktop instalado
- Docker Compose v2
- Puerto **8000** disponible


## Cómo ejecutar el proyecto

1. Clonar el repositorio
2. Abrir la terminal en la carpeta raíz del proyecto
3. Ejecutar:

docker compose up --build

## Tests

El proyecto incluye tests básicos usando **pytest**.

### Ejecutar tests con Docker

docker-compose run --rm tests


