# Carpeta de Campo: Sistema de Gestión de Pañol (Control de Herramientas)

---

## 1. Información General del Proyecto
- **Institución:** Escuela Técnica N°1 "Nuestra Señora del Valle"
- **Nombre del Proyecto:** Sistema Inteligente de Gestión de Pañol e Inventario de Taller
- **Versión Actual:** 1.0.0 (Módulo Pañol)
- **Tipo de Documento:** Carpeta de Campo y Especificación Funcional/Técnica
- **Fecha de Elaboración:** 2026

---

## 2. Introducción y Justificación

El pañol de herramientas es el núcleo operativo de las actividades prácticas en cualquier escuela técnica. En la Escuela Técnica N°1 "Nuestra Señora del Valle", la administración tradicional basada en planillas de papel genera demoras significativas al inicio y cierre de cada clase de taller, dificultades para rastrear herramientas dañadas o extraviadas, y falta de visibilidad del stock real disponible.

El **Sistema de Gestión de Pañol** ha sido diseñado para resolver esta problemática, digitalizando por completo el inventario y automatizando el flujo de préstamos y devoluciones. Mediante la integración de escáneres de códigos de barra y algoritmos de validación preventiva en tiempo real, el sistema asegura una logística interna óptima, permitiendo que los pañoleros y docentes enfoquen sus esfuerzos en las actividades puramente pedagógicas.

---

## 3. Objetivos

### 3.1. Objetivo General
Desarrollar e implementar un sistema digital centrado en la trazabilidad del inventario de pañol, reduciendo pérdidas físicas y automatizando los procesos de solicitud, entrega y devolución de herramientas mediante lectores de códigos de barra.

### 3.2. Objetivos Específicos
- **Control de Inventario Secuencial:** Permitir la carga masiva y secuencial de herramientas escaneando códigos de barra reales.
- **Validación Estricta de Stock:** Evitar la generación de pedidos que excedan el stock disponible en tiempo real en los estantes.
- **Devolución Express (Escaneo Único):** Optimizar el proceso de devolución masiva permitiendo al pañolero registrar el reingreso de cualquier herramienta al sistema con una sola lectura óptica.
- **Trazabilidad Docente-Alumno:** Monitorear en tiempo real qué docente es responsable del equipamiento retirado y qué alumnos están asociados a dichos préstamos.

---

## 4. Arquitectura del Sistema y Stack Tecnológico

El sistema de pañol está estructurado bajo una arquitectura cliente-servidor robusta y asíncrona.

### 4.1. Componentes Backend (FastAPI / Python)
- **Servicio Central:** Corre de forma dedicada (puerto `8001`) gestionando la lógica de categorías, stock, estados de herramientas, órdenes de pedido y préstamos activos.
- **Base de Datos:** SQLite / PostgreSQL con SQLAlchemy ORM. Permite procesar relaciones complejas de inventario (`Tool`, `Category`, `Loan`, `Order`).
- **Seguridad (JWT):** Control de acceso por roles (Pañolero/Admin, Profesor) para garantizar que las solicitudes e inventario solo puedan ser manipulados por personal autorizado.

### 4.2. Interfaz Frontend (HTML5 / CSS3 / Vanilla JS)
- Interfaz web minimalista, ligera y optimizada para el uso rápido en la PC del pañol.
- Integración nativa con entradas de teclado emuladas por lectores de códigos de barra para agilizar los flujos de picking y de devolución rápida sin clics adicionales.

---

## 5. Módulos Operativos

### 5.1. Módulo del Administrador (Pañolero)
- **Gestor de Stock y Alta Masiva:** Panel para crear categorías de herramientas y cargar unidades secuencialmente leyendo sus códigos de barra.
- **Panel de Picking (Entregas Consolidadas):** Agrupa automáticamente los pedidos de herramientas de los profesores y guía visualmente al pañolero en el conteo y asignación de cada unidad.
- **Devolución Rápida (Scan-to-Return):** Input activo que procesa la devolución inmediata de cualquier herramienta con solo escanear su código, liberando la deuda del profesor de forma instantánea.

### 5.2. Módulo del Profesor
- **Solicitud de Material:** Formulario digital simplificado donde el docente selecciona las herramientas y cantidades requeridas para su taller.
- **Restricción Preventiva:** Bloqueo dinámico en el formulario de solicitud cuando se intenta pedir una cantidad de herramientas superior al stock disponible.
- **Estado de Deuda:** Panel personalizado para verificar las herramientas activas que tiene bajo su responsabilidad.

---

## 6. Bitácora de Desarrollo e Historial de Carga Horaria

Como alumno de escuela técnica, el desarrollo de este proyecto se estructuró en dos grandes fases de trabajo: una fase de desarrollo intensivo inicial (aprovechando jornadas de taller, contraturnos y fines de semana dedicados al 100%) y una posterior fase de pulido, depuración y empaquetado final adaptada a la carga de clases regulares.

Dado que ambos sistemas (Alumnos/Campus y Pañol) comparten el núcleo del frontend y el sistema de inicio de sesión, el diseño de la estructura web base y el sistema de autenticación fueron desarrollados como componentes compartidos reutilizables, los cuales requirieron de múltiples iteraciones.

### Resumen de Distribución de Tiempos:
*   **Fase 1: Desarrollo Intensivo (21/04 al 27/06)**: Trabajo full-time de investigación y codificación básica. Dedicación de hasta **10 horas o más por día** en días de taller/diseño y fines de semana libres (~250 horas estimadas en este módulo).
*   **Fase 2: Estabilización y Pulido (28/06 al presente)**: Ajustado al horario escolar normal. Dedicación de **2 horas semanales** de lunes a viernes, y jornadas intensivas de **10 horas los domingos** (~110 horas estimadas en este módulo).
*   **Carga Horaria Total Estimada en este Módulo:** **360 horas reloj**.

### Bitácora Cronológica:

| Fecha / Periodo | Actividad Realizada | Horas Estimadas | Detalle Técnico / Logros |
| :--- | :--- | :--- | :--- |
| **21/04 - 30/04** | Diseño de la Estructura Web General y Estilos | 40 hs (Jornadas de 10 hs) | Maquetación inicial de la plantilla compartida, diseño responsivo general con HTML/CSS e interfaz compartida para el login de usuarios. |
| **01/05 - 15/05** | Desarrollo del Sistema de Autenticación y Roles | 60 hs (Multiples versiones) | Creación e iteración del sistema de Auth y roles. Se escribieron 3 versiones diferentes del código de control JWT y bcrypt antes del actual. |
| **16/05 - 31/05** | Base de Datos y APIs de Inventario de Pañol | 60 hs (Jornadas intensivas) | Modelado SQLAlchemy para categorías (`Category`) y herramientas (`Tool`). Lógica de asignación de códigos de barra secuenciales. |
| **01/06 - 15/06** | Desarrollo de Lógica de Préstamos y Devoluciones | 60 hs (Jornadas intensivas) | Creación de endpoints de solicitud y "devolución express" con lector de códigos. Validaciones del stock en base de datos. |
| **16/06 - 27/06** | Integración de Frontend de Pañol y Lectura Óptica | 30 hs | Unión del diseño web general con las peticiones `Fetch` exclusivas de pañol, y captura automática de eventos de escaneo. |
| **28/06 - 15/07** | Pruebas físicas en el taller del colegio | 26 hs (2 hs de semana + 10 hs domingos) | Pruebas integrales de campo conectando lectores USB reales en computadoras de taller, mitigando latencia y rebotes en el input. |
| **16/07 - Presente** | Dockerización y automatización de inicio local | 54 hs (2 hs de semana + 10 hs domingos) | Integración de base SQLite pre-cargada, Dockerfiles para despliegue unificado y archivos ejecutables .bat para la notebook de exposición. |

---

## 7. Conclusión

El **Sistema de Gestión de Pañol** moderniza y profesionaliza la administración del taller en la Escuela Técnica N°1 "Nuestra Señora del Valle". Al eliminar las ineficiencias de los registros en papel y dotar al pañolero de herramientas de captura óptica automatizada, se asegura el resguardo del patrimonio institucional y un entorno de trabajo coordinado y eficiente para docentes y estudiantes.
