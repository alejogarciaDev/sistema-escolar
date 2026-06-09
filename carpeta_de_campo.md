# Carpeta de Campo: Sistema Integral de Gestión Institucional

---

## 1. Información General del Proyecto
- **Institución:** Escuela Técnica N°1 "Nuestra Señora del Valle"
- **Nombre del Proyecto:** Sistema de Gestión de Pañol y Ecosistema Institucional
- **Versión Actual:** 1.0.0 (Fase Pañol)
- **Tipo de Documento:** Carpeta de Campo y Especificación Técnica
- **Fecha de Elaboración:** 2026

---

## 2. Introducción y Justificación

El presente proyecto nace de la necesidad de modernizar, digitalizar y optimizar la administración de recursos físicos dentro de la institución educativa. En su fase inicial, el enfoque principal radica en el **Pañol de Herramientas**, un área crítica donde el control manual del inventario, los préstamos y las devoluciones generan cuellos de botella operativos, pérdidas de material y retrasos en las actividades pedagógicas de los talleres.

La implementación de este sistema mitiga los errores humanos a través de la validación en tiempo real, trazabilidad de responsables y automatización de registros, asegurando que el flujo de herramientas entre pañoleros y docentes se desarrolle bajo estándares de alta eficiencia.

El diseño del software ha sido concebido desde una perspectiva de **arquitectura modular y escalable**, lo que permite que el núcleo del sistema sirva como base para integrar futuras áreas de la escuela, como la biblioteca escolar, laboratorios y gestión de expedientes de alumnos, transformándose en una plataforma ERP (Enterprise Resource Planning) institucional.

---

## 3. Objetivos

### 3.1. Objetivo General
Desarrollar e implementar un sistema informático centralizado y escalable que permita la administración integral, control y trazabilidad de los recursos físicos de la institución educativa, comenzando por el pañol y proyectándose a otras dependencias.

### 3.2. Objetivos Específicos
- **Digitalizar el inventario:** Migrar el registro en papel a una base de datos relacional robusta.
- **Trazabilidad estricta:** Registrar fecha, hora, responsable y estado de cada activo prestado o devuelto.
- **Interfaz ergonómica:** Proveer a profesores y alumnos de plataformas intuitivas para agilizar sus solicitudes sin curva de aprendizaje pronunciada.
- **Validación preventiva:** Bloquear solicitudes de préstamos que excedan la capacidad física del inventario en tiempo real.
- **Preparar el terreno para la escalabilidad:** Estructurar el modelo de datos y la API RESTful de tal manera que la adición de un nuevo módulo (ej. Biblioteca) requiera mínimos cambios en el core del sistema.

---

## 4. Arquitectura del Sistema

El sistema sigue el patrón de arquitectura **Cliente-Servidor** mediante el uso de una API RESTful, lo cual desacopla la interfaz de usuario de la lógica de negocio y gestión de datos.

### 4.1. Stack Tecnológico (Backend)
- **Framework:** FastAPI (Python 3.10+). Seleccionado por su alto rendimiento (basado en Starlette y Pydantic) y su capacidad nativa para manejar concurrencia asíncrona (ASGI).
- **Base de Datos:** PostgreSQL. Motor relacional de grado empresarial, elegido por su integridad referencial, soporte para transacciones ACID y manejo óptimo de consultas concurrentes.
- **ORM:** SQLAlchemy. Permite interactuar con la base de datos a través de modelos orientados a objetos, facilitando migraciones y consultas complejas.
- **Seguridad y Autenticación:** Implementación de JSON Web Tokens (JWT) con hashing de contraseñas mediante el algoritmo `bcrypt`. Control estricto de acceso basado en roles (RBAC - Role Based Access Control) definiendo permisos para Administradores, Profesores y Alumnos.

### 4.2. Stack Tecnológico (Frontend)
- **Tecnologías Core:** HTML5 Semántico, CSS3 (con Flexbox/Grid para diseño responsivo) y JavaScript ES6+ (Vanilla JS).
- **Comunicación API:** Uso intensivo de la API `Fetch` nativa del navegador para peticiones asíncronas HTTP, actualización dinámica del DOM (Document Object Model) y renderizado sin recarga de página (Single Page Application Behavior).
- **Diseño de Interfaz (UI/UX):** Estructura basada en modales interactivos, validaciones de formularios en tiempo real y notificaciones contextuales para una experiencia de usuario fluida y libre de errores.

---

## 5. Módulos Operativos (Fase 1: Pañol)

### 5.1. Módulo del Administrador (Pañolero)
- **Gestión Dinámica de Inventario:** Altas, bajas y modificaciones (CRUD) de herramientas. Incluye un sistema de alta secuencial y captura masiva de códigos de barras físicos escaneados mediante hardware de lectura óptica.
- **Monitor de Stock en Tiempo Real:** Dashboard analítico que contrasta el stock total histórico vs. el stock disponible físicamente en estantes.
- **Logística de Entregas y Devoluciones:** 
  - **Entregas Agrupadas:** Consolidación de pedidos generados por los profesores. El sistema elabora listas de "picking" (extracción) para que el operario localice los elementos con rapidez.
  - **Devolución Express (One-Scan Return):** Input asíncrono que procesa el ingreso de una herramienta al inventario automáticamente tras leer su código, liberando la deuda del usuario en el sistema.

### 5.2. Módulo del Profesor
- **Catálogo y Solicitudes:** Interfaz que expone las herramientas y su disponibilidad calculada al milisegundo.
- **Gestor de Pedidos de Taller:** Generación de requisiciones de material sujetas a validación de stock; prevención de colisiones por solicitudes concurrentes de múltiples docentes.
- **Panel de Deudas Activas:** Visor de material no devuelto para control personal.

---

## 6. Plan de Escalabilidad y Expansión Institucional

La concepción arquitectónica del proyecto contempla la inminente expansión hacia otros sectores del colegio. Al estar basado en micro-servicios lógicos y una API RESTful, el sistema base es directamente reciclable.

### 6.1. Fase 2: Módulo de Biblioteca Institucional
El flujo de lógica entre un "Pañol" y una "Biblioteca" es análogo (entidad física prestada a un usuario temporalmente).
**Adaptaciones Requeridas:**
- **Nuevos Modelos de Datos:** Se extenderá SQLAlchemy creando tablas para `Libros`, `Autores`, `Editoriales` y `Categorías_Literarias`.
- **Integración de ISBN:** Reemplazo lógico del campo "Código de Herramienta" por el estándar internacional de libros ISBN o código de barras interno de la biblioteca.
- **Políticas de Préstamo Diferenciadas:** Mientras una herramienta de pañol suele devolverse en el día, el módulo de biblioteca incluirá la lógica de "Fecha de Vencimiento", "Renovaciones" y "Sanciones/Multas" por demoras.
- **Interfaz de Biblioteca:** Un frontend dedicado para bibliotecarios enfocado en la búsqueda catalográfica, y para alumnos, permitiendo reservas de bibliografía de manera remota.

### 6.2. Fase 3: Gestión de Laboratorios e Informática
- Control de netbooks y computadoras asignadas a los carritos tecnológicos.
- Trazabilidad de componentes de robótica (kits Arduino, componentes electrónicos) con control de stock de insumos consumibles (ej. estaño, resistencias) donde no se exige devolución.

### 6.3. Fase 4: Ecosistema Digital Alumno-Profesor
- Emisión de reportes unificados donde preceptores y directivos puedan visualizar si un alumno adeuda libros en biblioteca, herramientas en taller o componentes en laboratorio, facilitando procesos administrativos a fin de ciclo lectivo.

---

## 7. Requerimientos de Despliegue (Deployment)

Para poner en producción el sistema, se documenta la siguiente infraestructura necesaria:

- **Servidor Local / VPS (Virtual Private Server):** Sistema Operativo Ubuntu Server 22.04 LTS o superior.
- **Web Server / Reverse Proxy:** Nginx o Traefik para gestionar el tráfico HTTP/HTTPS y derivarlo a Uvicorn (servidor ASGI de Python).
- **Proceso en Segundo Plano:** Uso de `systemd` o `pm2` para garantizar que la API del backend se reinicie automáticamente ante fallos.
- **Túneles Seguros:** Implementación de **Cloudflare Tunnels** (`cloudflared`) para exponer el servidor local a internet sin necesidad de abrir puertos en el firewall institucional, garantizando alta seguridad y mitigación DDoS.
- **Backups:** Cronjobs programados para generar volcados automáticos de la base de datos PostgreSQL (`pg_dump`) de manera diaria y encriptada.

---

## 8. Conclusiones

El **Sistema de Gestión de Pañol** no es únicamente una solución a un problema logístico actual, sino la piedra angular funcional de un entorno informático de grado administrativo que posiciona a la Escuela Técnica N°1 "Nuestra Señora del Valle" a la vanguardia tecnológica. Su código limpio, documentación rigurosa y diseño pensado en la abstracción aseguran que la inversión de tiempo y recursos de desarrollo redituará en años de operatividad ininterrumpida y un crecimiento orgánico hacia todos los departamentos del establecimiento.
