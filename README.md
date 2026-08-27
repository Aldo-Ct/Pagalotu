# Pagatu - Sesión S01

Proyecto de la sesión **Construcción de un servicio base para un sistema distribuido**.

## Microservicios

- `pagatu-catalogo-ms`: gestiona categorías y productos del catálogo.
- `pagatu-orden-ms`: gestiona órdenes y sus detalles. Conserva únicamente los identificadores de cliente y producto porque esos datos pertenecen a otros microservicios.

## Requisitos

- Java 21
- Docker Desktop
- Maven Wrapper incluido en cada microservicio

## Config Server en DEV

El catálogo obtiene su configuración de desarrollo desde Spring Cloud Config. Inícialo primero y déjalo activo:

```bash
cd infra/pagatu-config
./mvnw spring-boot:run
```

El Config Server queda disponible en `http://localhost:18888`.

## Catálogo en DEV

```bash
cd Services/pagatu-catalogo-ms
docker compose -f compose-dev.yml up -d
./mvnw spring-boot:run -Dspring-boot.run.arguments=--server.port=8082
```

Servicios disponibles:

- API: `http://localhost:8082/api/v1/categorias` y `http://localhost:8082/api/v1/productos`
- Swagger: `http://localhost:8082/swagger-ui/index.html`
- Health: `http://localhost:8082/actuator/health`
- Metrics: `http://localhost:8082/actuator/metrics`

## Órdenes en DEV

```bash
cd Services/pagatu-orden-ms
docker compose -f compose-dev.yml up -d
./mvnw spring-boot:run
```

Servicios disponibles:

- API: `http://localhost:8080/api/v1/ordenes`
- Swagger: `http://localhost:8080/swagger-ui/index.html`
- Health: `http://localhost:8080/actuator/health`
- Metrics: `http://localhost:8080/actuator/metrics`

Crear una orden:

```bash
curl -X POST http://localhost:8080/api/v1/ordenes \
  -H "Content-Type: application/json" \
  -d '{"clienteId":1,"tipoComprobante":"BOLETA_SIMPLE","metodoPago":"YAPE_PLIN","momentoPago":"ADELANTADO","detalles":[{"productoId":1,"cantidad":2,"precioUnitario":25.50}]}'
```

Listar, consultar, actualizar y eliminar:

```bash
curl http://localhost:8080/api/v1/ordenes
curl http://localhost:8080/api/v1/ordenes/1
curl -X PUT http://localhost:8080/api/v1/ordenes/1 \
  -H "Content-Type: application/json" \
  -d '{"clienteId":1,"tipoComprobante":"BOLETA_CON_DNI","metodoPago":"TRANSFERENCIA","momentoPago":"CONTRA_ENTREGA","detalles":[{"productoId":1,"cantidad":3,"precioUnitario":20.00}]}'
curl -X DELETE http://localhost:8080/api/v1/ordenes/1
```

## Verificar PostgreSQL y Flyway

```bash
docker exec -it pagatu-postgres-orden-dev psql -U pagatu -d pagatu_orden_db -c "\dt"
docker exec -it pagatu-postgres-orden-dev psql -U pagatu -d pagatu_orden_db -c "SELECT * FROM ordenes;"
docker exec -it pagatu-postgres-orden-dev psql -U pagatu -d pagatu_orden_db -c "SELECT * FROM orden_detalles;"
```

## Dos instancias de órdenes

Con la primera instancia activa en `8080`, ejecutar en otra terminal:

```bash
cd Services/pagatu-orden-ms
./mvnw spring-boot:run -Dspring-boot.run.arguments=--server.port=8081
curl http://localhost:8080/saludo
curl http://localhost:8081/saludo
curl http://localhost:8080/actuator/health
curl http://localhost:8081/actuator/health
```

Las dos instancias son stateless y comparten PostgreSQL. El puerto puede cambiar mediante configuración, por lo que un balanceador podrá distribuir tráfico entre varias copias.

## Documentación de evidencia

```bash
mkdocs serve
```

La evidencia individual de S01 se encuentra en `docs/S01_Construccion_Servicio_Base.md`.
