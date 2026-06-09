# Carpeta de Campo: Sistema de Gestión de Oficina de Alumnos y Campus Virtual

---

## 1. Información General del Proyecto
- **Institución:** Escuela Técnica N°1 "Nuestra Señora del Valle"
- **Nombre del Proyecto:** Sistema de Gestión Digital para Oficina de Alumnos y Campus Virtual
- **Versión Actual:** 1.0.0 (Módulo Académico)
- **Tipo de Documento:** Carpeta de Campo y Especificación Funcional/Técnica
- **Fecha de Elaboración:** 2026

---

## 2. Introducción y Justificación

La administración académica y la interacción pedagógica en la Escuela Técnica N°1 "Nuestra Señora del Valle" requieren de herramientas ágiles que superen el manejo tradicional de expedientes físicos e interacciones informales. El **Sistema de Gestión de Oficina de Alumnos y Campus Virtual** surge con el propósito de centralizar y digitalizar la información de los estudiantes (legajos, asignación de materias, documentación) y complementar la cursada mediante un aula virtual moderna.

Este sistema reduce la carga administrativa del personal de secretaría y preceptores, agiliza la comunicación de consignas por parte de los docentes y provee a los alumnos de un repositorio oficial donde descargar apuntes y subir sus entregas, adaptándose a las necesidades de la educación técnica profesional contemporánea.

---

## 3. Objetivos

### 3.1. Objetivo General
Desarrollar una plataforma digital integrada que optimice la gestión de legajos estudiantiles, la matriculación en asignaturas y el seguimiento del progreso académico en un Campus Virtual para la comunidad educativa.

### 3.2. Objetivos Específicos
- **Legajo Digital Único:** Reemplazar el archivo en papel con registros digitales del estudiante, incluyendo sus datos personales, materias cursadas y archivos adjuntos (fotocopia de DNI, certificados).
- **Campus Virtual Desacoplado:** Habilitar un canal asíncrono para que los docentes publiquen material didáctico, asignen tareas y evalúen de manera virtual.
- **Gestión Jerárquica de Permisos:** Garantizar la confidencialidad mediante roles específicos (Administrador/Preceptor, Profesor, Alumno).
- **Operación Local y Robusta:** Permitir la ejecución local completa (en la notebook de exposición o servidores internos) mediante base de datos SQLite y empaquetado en Docker.

---

## 4. Arquitectura del Sistema y Stack Tecnológico

La plataforma adopta una arquitectura modular basada en micro-servicios lógicos a nivel de API, facilitando el mantenimiento y la escalabilidad del sistema académico.

### 4.1. Componentes Backend (FastAPI / Python)
- **Servicio Académico e Independiente:** Corre de forma dedicada (por defecto en el puerto `8002` en modo de Campus) para no interferir con otros servicios de la institución.
- **Base de Datos:** SQLite / PostgreSQL a través de SQLAlchemy ORM. Permite registrar las entidades `Alumno`, `Materia`, `Inscripcion`, `Tarea`, `Entrega` e `Informacion Academica`.
- **Seguridad (JWT):** Autenticación mediante Tokens Web de JSON cifrados por bcrypt para el control de accesos a la entrega de tareas y visualización de expedientes.

### 4.2. Interfaz Frontend (HTML5 / CSS3 / Vanilla JS)
- Estructura y diseño responsivo adaptado para pantallas de notebooks y dispositivos móviles.
- Carga dinámica mediante peticiones asíncronas con la API `Fetch` de Javascript, lo cual elimina recargas innecesarias y agiliza la experiencia en redes escolares limitadas.

---

## 5. Módulos Operativos

### 5.1. Módulo de Oficina de Alumnos (Preceptor / Administrador)
- **Gestión de Legajos:** Alta y actualización de estudiantes con sus respectivos legajos académicos.
- **Inscripción a Materias:** Asignación masiva y matriculación de alumnos en las distintas asignaturas del plan de estudio de la escuela técnica.
- **Repositorio de Documentos:** Almacenamiento seguro de archivos institucionales asociados al legajo del estudiante.

### 5.2. Módulo del Profesor (Campus Virtual)
- **Creación de Tareas:** Permite a los docentes publicar actividades con títulos, descripciones, fechas límite y adjuntar archivos de soporte.
- **Calificación y Feedback:** Espacio dedicado para revisar las entregas en PDF o imágenes de los alumnos y registrar su nota y comentarios.

### 5.3. Módulo del Alumno
- **Panel de Cursada:** Visualización de las materias en las cuales está inscrito y las tareas pendientes.
- **Subida de Entregas:** Interfaz interactiva para adjuntar archivos correspondientes a las consignas solicitadas por los docentes.

---

## 6. Bitácora de Desarrollo e Historial de Carga Horaria

Como alumno de escuela técnica, el desarrollo de este proyecto se estructuró en dos grandes fases de trabajo: una fase de desarrollo intensivo inicial (aprovechando jornadas de taller, contraturnos y fines de semana dedicados al 100%) y una posterior fase de pulido, depuración y empaquetado final adaptada a la carga de clases regulares.

Dado que ambos sistemas (Alumnos/Campus y Pañol) comparten el núcleo del frontend y el sistema de inicio de sesión, el diseño de la estructura web base y el sistema de autenticación fueron desarrollados como componentes compartidos reutilizables, los cuales requirieron de múltiples iteraciones. El Aula y el Campus Virtual fueron las últimas funcionalidades implementadas en el proyecto.

### Resumen de Distribución de Tiempos:
*   **Fase 1: Desarrollo Intensivo (21/04 al 27/06)**: Trabajo full-time de investigación y codificación básica. Dedicación de hasta **10 horas o más por día** en días de taller/diseño y fines de semana libres (~240 horas estimadas en este módulo).
*   **Fase 2: Estabilización y Pulido (28/06 al presente)**: Ajustado al horario escolar normal. Dedicación de **2 horas semanales** de lunes a viernes, y jornadas intensivas de **10 horas los domingos** (~100 horas estimadas en este módulo).
*   **Carga Horaria Total Estimada en este Módulo:** **340 horas reloj**.

### Bitácora Cronológica:

| Fecha / Periodo | Actividad Realizada | Horas Estimadas | Detalle Técnico / Logros |
| :--- | :--- | :--- | :--- |
| **21/04 - 30/04** | Diseño de la Estructura Web General y Estilos | 40 hs (Jornadas de 10 hs) | Creación de las plantillas HTML básicas, paleta de colores CSS centralizada, diseño responsivo general y estructura compartida de barra de navegación y pie de página. |
| **01/05 - 15/05** | Desarrollo del Sistema de Autenticación y Roles | 60 hs (Multiples versiones) | Implementación inicial del sistema de Auth. Se rehicieron y refactorizaron 3 versiones del backend y el login frontend hasta alcanzar el control de roles seguro con JWT y bcrypt que funciona hoy. |
| **16/05 - 31/05** | Backend Académico y base de datos de Alumnos | 60 hs (Jornadas intensivas) | Creación de esquemas relacionales para alumnos, materias y legajos académicos. Endpoints de control y persistencia CRUD básica. |
| **01/06 - 15/06** | Desarrollo del Frontend de la Oficina de Alumnos | 50 hs (Jornadas intensivas) | Unión de la estructura web general con llamadas API para listar alumnos, crear inscripciones y gestionar la carga de datos escolares. |
| **16/06 - 27/06** | Pruebas y estabilización de Oficina de Alumnos | 30 hs (Jornadas de 10 hs) | Depuración de validaciones de formularios y correcciones de consistencia de legajos en la base de datos local. |
| **28/06 - 15/07** | Desarrollo Completo del Aula y Campus Virtual | 24 hs (2 hs de semana + 10 hs domingos) | **Última funcionalidad core agregada.** Lógica para que los profesores creen tareas y alumnos suban archivos de entregas digitales en formato PDF e imagen. |
| **16/07 - Presente** | Dockerización y puesta a punto local | 26 hs (2 hs de semana + 10 hs domingos) | Armado del contenedor Docker independiente para el campus, configuración de variables de entorno y creación de scripts PowerShell de automatización. |

---

## 7. Conclusión

El **Sistema de Gestión de Oficina de Alumnos y Campus Virtual** representa un salto de calidad en los procesos administrativos y educativos de la Escuela Técnica N°1 "Nuestra Señora del Valle". Al centralizar el historial académico y la comunicación pedagógica en una arquitectura digital moderna y ligera, se sientan las bases para un colegio inteligente, eficiente y preparado para los desafíos formativos del siglo XXI.
