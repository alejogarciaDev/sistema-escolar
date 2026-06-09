import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
import app.core.models

from app.modules.campus.routes import router as campus_router
from app.modules.academico.archivos.routes import router as archivos_router
from app.modules.academico.materias.routes import router as materias_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Virtual - Servicio Independiente")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(campus_router)
app.include_router(archivos_router)
app.include_router(materias_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
