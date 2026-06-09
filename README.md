# Sistema de Gestión de Pañol - Escuela Técnica N°1 Nuestra Señora del Valle

Este proyecto es un sistema integral de gestión de herramientas (Pañol) desarrollado para digitalizar, organizar y agilizar el préstamo y devolución de equipamiento dentro de la institución. 

## 📋 Características Principales

El sistema está dividido en múltiples módulos e interfaces dependiendo del rol del usuario (Profesores, Alumnos, Administradores de Pañol, etc.), respaldados por una robusta API en el backend.

### Para el Pañolero (Administrador)
- **Gestión de Inventario Dinámico:** Permite dar de alta nuevas herramientas ingresando o escaneando múltiples códigos de barra de forma secuencial.
- **Resumen de Stock en Tiempo Real:** Visualización rápida de herramientas disponibles vs herramientas totales por cada categoría (ej. Martillos: 25/26 disponibles).
- **Entregas Inteligentes:** Los pedidos de los profesores se agrupan automáticamente. Al momento de entregar, el sistema indica exactamente qué herramientas se deben buscar y permite escanearlas para asignarlas rápidamente al profesor solicitante.
- **Devoluciones Express:** Un campo de escaneo directo permite devolver cualquier herramienta al inventario con tan solo leer su código de barras, sin buscar en listas.

### Para el Profesor
- **Solicitud de Herramientas Guiada:** Interfaz simplificada para solicitar herramientas por categoría.
- **Validación Preventiva de Stock:** El sistema impide solicitar una cantidad de herramientas mayor a la disponible físicamente en el pañol, mostrando el stock en tiempo real antes de enviar el pedido.
- **Seguimiento de Préstamos Activos:** Panel personal para visualizar qué herramientas tiene actualmente en su poder el profesor.

---

## 🛠️ Tecnologías Utilizadas

- **Frontend:** HTML5, CSS3 y JavaScript puro (Vanilla JS). Implementación de Flexbox para el diseño responsivo e interfaces dinámicas basadas en modales y peticiones asíncronas.
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python) para la creación de una API RESTful rápida y moderna.
- **Base de Datos:** PostgreSQL a través del ORM SQLAlchemy.
- **Autenticación:** Sistema de seguridad con tokens JWT (`access_token`) y control de roles.

---

## 🚀 Instalación y Ejecución Local

### 1. Requisitos Previos
- Python 3.10+
- PostgreSQL instalado y corriendo.
- Git.

### 2. Configuración del Backend
1. Clonar el repositorio.
2. Ingresar a la carpeta del backend: `cd backend`
3. Crear un entorno virtual: `python -m venv venv`
4. Activar el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
5. Instalar dependencias: `pip install -r requirements.txt` (asegúrese de tener las librerías de FastAPI, Uvicorn, SQLAlchemy y Pydantic instaladas).
6. Configurar la cadena de conexión de la base de datos en `app/core/database.py` o mediante variables de entorno.
7. Iniciar el servidor local:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

### 3. Configuración del Frontend
El frontend consta de archivos estáticos ubicados en `frontend/web_tecnica/public/sistema/`.
1. Para probarlo localmente, puedes usar la extensión "Live Server" de VSCode o un servidor de Python:
   ```bash
   cd frontend/web_tecnica/public
   python -m http.server 3000
   ```
2. Asegúrate de que las URLs de la API en el frontend apunten a tu servidor backend (ej. `http://192.168.1.36:8001` o `http://localhost:8001`).

---

## 🔄 Últimas Actualizaciones y Cambios

- **Carga de códigos por escáner:** Se reemplazó la generación automática de códigos por un sistema de captura masiva. Ahora el pañolero escanea etiquetas reales separadas por comas en un campo de texto y el backend crea el inventario respetando los códigos reales.
- **Agrupación de Pedidos:** Los pedidos de los profesores ahora se unifican visualmente en el panel del pañol. El modal de entrega lista específicamente los requerimientos (ej. *3x Martillos, 2x Pinzas*) para facilitar el trabajo del operador.
- **Validación estricta de stock:** Los profesores ya no pueden generar pedidos que superen el límite de herramientas disponibles. El frontend consulta directamente la vista resumen `/tools/summary/` para bloquear ingresos erróneos en origen.

---

## 👨‍💻 Autoría y Desarrollo

Desarrollado para la **Escuela Técnica N°1 Nuestra Señora del Valle**.
*Sistema optimizado para el manejo preciso y a prueba de errores del inventario institucional.*
