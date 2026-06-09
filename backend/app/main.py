from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine

import app.core.models

from app.modules.academico.alumnos.routes import router as alumnos_router
from app.modules.panol.categories.routes import router as categories_router
from app.modules.panol.loans.routes import router as loans_router
from app.modules.panol.orders.routes import router as orders_router
from app.modules.users.users.routes import router as users_router
from app.modules.users.roles.routes import router as roles_router
from app.modules.users.permissions.routes import router as permissions_router
from app.modules.auth.routes import router as auth_router
from app.modules.notifications.routes import router as notifications_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Pañol PRO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alumnos_router)
app.include_router(categories_router)
app.include_router(loans_router)
app.include_router(orders_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(permissions_router)
app.include_router(auth_router)
app.include_router(notifications_router)
