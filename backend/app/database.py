from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://admin:2802@localhost/sistema"

engine = create_engine(
    DATABASE_URL,
    echo=True  # opcional (muestra queries)
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


# Para usar en FastAPI después
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
