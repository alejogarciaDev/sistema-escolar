# USERS
from app.modules.users.users.models import User
from app.modules.users.roles.models import Role
from app.modules.users.permissions.models import Permission

# PAÑOL
from app.modules.panol.categories.models import Category
from app.modules.panol.loans.models import Loan
from app.modules.panol.orders.models import Order
from app.modules.panol.orders.items.models import OrderItem

# ACADÉMICO
from app.modules.academico.alumnos.models import Alumno, AlumnoHistorial
from app.modules.academico.materias.models import Materia
from app.modules.academico.archivos.models import Archivo

# CAMPUS VIRTUAL
from app.modules.campus.models import Tarea, Entrega, Calificacion, MaterialEstudio, DocumentoAlumno, DocumentoCompartido, CompartidoPermiso