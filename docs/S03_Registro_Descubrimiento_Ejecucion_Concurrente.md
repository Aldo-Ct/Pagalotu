# S03 - Registro, Descubrimiento y Ejecucion Concurrente de Servicios

## Datos del estudiante

- Nombre: Aldo Calla Ticona
- Equipo: Sin grupo - trabajo individual
- Sesion: S03 - Registro, Descubrimiento y Ejecucion Concurrente de Servicios
- Rol o aporte realizado: implementacion y verificacion integral
- Link de GitHub: https://github.com/Aldo-Ct/Pagalotu
- Usuario de ejecucion: `aldocallaticona`
- Fecha de verificacion: 3 de septiembre de 2026

## Resumen del resultado

Se implemento `pagatu-eureka` como servidor de registro y Config Client. Se conectaron
`pagatu-catalogo-ms` y `orden-ms` como clientes de Eureka, cada uno con dos instancias
DEV simultaneas. Catalogo quedo en los puertos 8080 y 8081; ordenes, en 8082 y 8083.
Las cuatro instancias respondieron `UP`, atendieron sus endpoints REST y fueron
descubiertas automaticamente por Prometheus. Promtail envio los archivos de ambos
microservicios a Loki. Tambien se verifico que una instancia eliminada deja de aparecer
en Eureka y en los targets descubiertos sin editar configuracion.

## 1. pagatu-eureka operativo

`pagatu-eureka` consulta Config Server en `localhost:18888` y recibe su configuracion
DEV, incluido el puerto `18761`. Su dashboard y API mostraron las siguientes instancias:

| Aplicacion | Instancia | Puerto | Estado |
|---|---|---:|---|
| PAGATU-CATALOGO-MS | pagatu-catalogo-ms:8080 | 8080 | UP |
| PAGATU-CATALOGO-MS | pagatu-catalogo-ms:8081 | 8081 | UP |
| ORDEN-MS | orden-ms:8082 | 8082 | UP |
| ORDEN-MS | orden-ms:8083 | 8083 | UP |

Comando de evidencia:

```bash
curl -H 'Accept: application/json' http://localhost:18761/eureka/apps
```

## 2. pagatu-orden-ms migrado a Config Client

El `application.yml` local conserva solamente el nombre logico, perfil DEV e importacion
de Config Server. Las propiedades completas se encuentran en:

- `infra/pagatu-config/config-repo/orden-ms-dev.yml`
- `infra/pagatu-config/config-repo/orden-ms-prod.yml`

La entrega por HTTP fue verificada con:

```bash
curl http://localhost:18888/orden-ms/dev
curl http://localhost:18888/orden-ms/prod
```

DEV entrego el puerto fijo 8082 y `defaultZone` en
`http://localhost:18761/eureka`. PROD entrego la URL interna
`http://pagatu-eureka:8761/eureka` y un `instance-id` con valor aleatorio para evitar
colisiones al escalar contenedores.

## 3. pagatu-orden-ms registrado con multiples instancias

Se agrego `spring-cloud-starter-netflix-eureka-client` y se ejecutaron dos procesos:

```bash
java -jar target/pagatu-orden-ms-0.0.1-SNAPSHOT.jar --server.port=8082
java -jar target/pagatu-orden-ms-0.0.1-SNAPSHOT.jar --server.port=8083
```

Ambas instancias respondieron correctamente:

| Verificacion | 8082 | 8083 |
|---|---:|---:|
| `/actuator/health` | 200 / UP | 200 / UP |
| `/api/v1/ordenes` | 200 | 200 |
| `/actuator/prometheus` | 200 | 200 |
| `/v3/api-docs` | 200 | 200 |

La consulta REST devolvio la misma orden persistida desde ambos procesos y cada
respuesta incluyo un `X-Trace-ID` diferente, confirmando ejecucion independiente.

## 4. Comprension del patron

Un consumidor de Eureka trabaja con el nombre logico `ORDEN-MS`, no con una lista
escrita a mano de URLs. Eureka mantiene la relacion actual entre ese nombre y las
instancias 8082 y 8083. El consumidor consulta el registro y recibe las direcciones
vigentes; luego un cliente con balanceo puede seleccionar una de ellas. Que los puertos
sean fijos y elegidos manualmente no cambia el patron: la lista deja de estar incrustada
en el consumidor y pasa a ser informacion dinamica administrada por el registro. Cuando
una instancia se detiene, su direccion desaparece del registro y deja de ser candidata.

## 5. Observabilidad opcional

Se agrego `micrometer-registry-prometheus` a `pagatu-orden-ms` y se expuso el endpoint
Prometheus en DEV y PROD. Sin editar `prometheus-dev.yml`, el descubrimiento por Eureka
encontro cuatro targets `UP`: dos de catalogo y dos de ordenes.

Promtail se amplio con un segundo trabajo y bind mount para
`Services/pagatu-orden-ms/logs/*.log`. La consulta siguiente devolvio dos streams con
logs reales de arranque, consulta del registro y peticiones HTTP:

```logql
{application="pagatu-orden-ms"}
```

## Error o hallazgo tecnico diagnosticado

Al detener de forma controlada la instancia de catalogo en 8081, esta envio a Eureka
su cambio de estado y se desregistro correctamente. En el siguiente refresco de Service
Discovery, Prometheus no dejo el target indefinidamente como `DOWN`: lo elimino de su
lista porque Eureka ya no lo anunciaba. Esto no fue un error de Prometheus. Fue la
consecuencia correcta de combinar desregistro graceful, Eureka y descubrimiento
dinamico. Al reiniciar 8081, Eureka volvio a registrarlo y Prometheus recupero cuatro
targets `UP` sin cambios de configuracion.

## Reflexion tecnica breve

El Gateway de S4 necesita una forma estable de referirse a servicios que pueden cambiar
de puerto o cantidad de instancias. Eureka proporciona esa capa mediante nombres
logicos y un inventario actualizado. El Gateway podra resolver `ORDEN-MS` o
`PAGATU-CATALOGO-MS` sin almacenar direcciones individuales. Esa informacion tambien
permite repartir solicitudes entre varias instancias disponibles. Si una desaparece,
el registro evita que siga siendo seleccionada. Por eso descubrimiento y registro son
prerrequisitos directos del enrutamiento y balanceo de carga.

## Respuestas para defensa

1. `pagatu-eureka` no se registra a si mismo porque es el servidor del registro, no una
   instancia consumidora. Por eso usa `register-with-eureka: false`.
2. Sin `--server.port=8081`, la segunda instancia de catalogo intentaria ocupar 8080 y
   fallaria con `Address already in use`.
3. Ordenes se verifico consultando la API de Eureka, comprobando estado `UP`, puerto e
   `instance-id`, ademas de hacer peticiones HTTP independientes a 8082 y 8083.
4. Si una instancia deja de enviar heartbeat, Eureka termina removiendola. Con apagado
   graceful, el cliente puede desregistrarse inmediatamente.
5. `spring.application.name` identifica el documento de Config Server y tambien el
   nombre logico publicado en Eureka.
6. Prometheus es otro consumidor del registro: consulta Eureka para descubrir targets
   sin una lista manual de direcciones.

## Anexo: feedback de la sesion

1. Aprendizaje principal: un registro convierte varias direcciones fisicas en un nombre
   logico estable y actualizable.
2. Punto inicialmente confuso: diferenciar un target `DOWN` de un target retirado por
   completo cuando Eureka deja de anunciarlo.
3. Pregunta para la siguiente clase: como combinara el Gateway la resolucion por nombre
   con el algoritmo de balanceo de Spring Cloud LoadBalancer.
4. Nivel de comprension: Entendido - lo domino y podria explicarlo.
5. Apoyo que ayudaria: comparar en S4 una ruta fija con una ruta `lb://` observando las
   instancias elegidas.
6. Autoevaluacion: Muy comprometido; se completo tambien el bloque opcional de
   observabilidad.
7. Satisfaccion con la clase: 10/10.

## Nota sobre la evidencia visual

Los valores y capturas del informe proceden de los servicios reales verificados el 3 de
septiembre de 2026 bajo el usuario `aldocallaticona`. Las evidencias se conservaron en
`capturas/originales_s03/`: Eureka, Swagger para los puertos 8080, 8081, 8082 y 8083,
Prometheus con cuatro targets `UP` y Loki con una consulta exitosa para
`{application="pagatu-catalogo-ms"}`. El PDF incluye siete capturas y una evidencia de
terminal que identifica el endpoint, la consulta LogQL, la fecha del sistema y el
resultado `status: success`.
