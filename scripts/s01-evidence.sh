#!/usr/bin/env bash

set -u

ROOT_DIR="/Users/aldocallaticona/Pagatu"
SERVICE_DIR="$ROOT_DIR/Services/pagatu-orden-ms"

header() {
  printf '\033[2J\033[3J\033[H'
  printf '\033[1;36mS01  /  %s\033[0m\n' "$1"
  printf '\033[2mAldo Calla Ticona  ·  %s\033[0m\n\n' "$(date '+%d-%m-%Y · %H:%M %Z')"
}

case "${1:-}" in
  domain)
    header "DOMINIO DEL MICROSERVICIO"
    cd "$SERVICE_DIR" || exit 1
    printf '\033[1;33mCapas implementadas\033[0m\n'
    find src/main/java/pe/edu/upeu/orden -mindepth 1 -maxdepth 1 -type d -exec basename {} \; \
      | sort \
      | paste -d '  ' - -
    printf '\n\033[1;33mMigración versionada con Flyway\033[0m\n'
    printf 'V1__create_orden_tables.sql  ·  %s bytes\n' \
      "$(wc -c < src/main/resources/db/migration/V1__create_orden_tables.sql | tr -d ' ')"
    printf '\n\033[1;33mTablas definidas\033[0m\n'
    grep '^CREATE TABLE' src/main/resources/db/migration/V1__create_orden_tables.sql
    ;;

  runtime)
    header "RUNTIME DEV VERIFICADO"
    cd "$SERVICE_DIR" || exit 1
    printf '\033[1;33mHerramientas\033[0m\n'
    JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home ./mvnw -version \
      | sed -n '1p;3p' \
      | sed 's/, runtime:.*//'
    printf '\n\033[1;33mFlyway + PostgreSQL\033[0m\n'
    docker exec pagatu-postgres-orden-dev psql -U pagatu -d pagatu_orden_db -P pager=off \
      -c 'SELECT installed_rank, version, description, success FROM flyway_schema_history;'
    printf '\033[1;33mAplicación Spring Boot\033[0m\n'
    lsof -nP -iTCP:8080 -sTCP:LISTEN | sed -n '1,2p'
    curl -sS http://localhost:8080/actuator/health \
      | jq '{status, database:.components.db.details.database, db:.components.db.status}'
    ;;

  database)
    header "POSTGRESQL · DATOS PERSISTIDOS"
    docker exec pagatu-postgres-orden-dev psql -U pagatu -d pagatu_orden_db -P pager=off \
      -c '\dt' \
      -c 'SELECT id, id_cliente, estado, tipo_comprobante, metodo_pago, momento_pago, total FROM ordenes ORDER BY id;' \
      -c 'SELECT id, id_orden, id_producto, cantidad, precio_unitario FROM orden_detalles ORDER BY id;'
    ;;

  api)
    header "API REST · CRUD Y OPENAPI"
    printf '\033[1;33mGET /api/v1/ordenes/2\033[0m\n'
    curl -sS http://localhost:8080/api/v1/ordenes/2 \
      | jq '{id,clienteId,estado,tipoComprobante,metodoPago,momentoPago,total,detalle:{productoId:.detalles[0].productoId,cantidad:.detalles[0].cantidad,precioUnitario:.detalles[0].precioUnitario}}'
    printf '\n\033[1;33mValidación y recurso inexistente\033[0m\n'
    printf 'POST incompleto  → HTTP '
    curl -sS -o /dev/null -w '%{http_code}\n' -X POST http://localhost:8080/api/v1/ordenes \
      -H 'Content-Type: application/json' -d '{}'
    printf 'GET /99999      → HTTP '
    curl -sS -o /dev/null -w '%{http_code}\n' http://localhost:8080/api/v1/ordenes/99999
    printf '\n\033[1;33mContrato OpenAPI activo\033[0m\n'
    curl -sS http://localhost:8080/v3/api-docs \
      | jq -r '.paths | to_entries[] | "\(.key)  [\(.value | keys | join(", ") | ascii_upcase)]"'
    ;;

  scale)
    header "ESCALAMIENTO HORIZONTAL"
    printf '\033[1;33mDos procesos Java independientes\033[0m\n'
    lsof -nP -iTCP:8080 -sTCP:LISTEN | sed -n '1,2p'
    lsof -nP -iTCP:8081 -sTCP:LISTEN | sed -n '2p'
    printf '\n\033[1;33mMisma API · puertos distintos\033[0m\n'
    for port in 8080 8081; do
      saludo=$(curl -sS "http://localhost:$port/saludo")
      estado=$(curl -sS "http://localhost:$port/actuator/health" | jq -r '.status')
      db=$(curl -sS "http://localhost:$port/actuator/health" | jq -r '.components.db.status')
      metrics=$(curl -sS -o /dev/null -w '%{http_code}' "http://localhost:$port/actuator/metrics")
      printf ':%s  %-29s  health=%s  db=%s  metrics=%s\n' "$port" "$saludo" "$estado" "$db" "$metrics"
    done
    printf '\n\033[1;32m✓ Instancias stateless compartiendo PostgreSQL DEV\033[0m\n'
    ;;

  *)
    printf 'Uso: %s {domain|runtime|database|api|scale}\n' "$0" >&2
    exit 2
    ;;
esac
