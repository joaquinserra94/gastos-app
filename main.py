from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models
import crud
from pydantic import BaseModel
from typing import List

# Crear sesión de base de datos para cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esquemas de entrada/salida
class GrupoCreate(BaseModel):
    nombre: str

class GrupoOut(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True

class PersonaCreate(BaseModel):
    nombre: str
    grupo_id: int

class GastoCreate(BaseModel):
        descripcion: str
        monto: float
        pagador_id: int
        grupo_id: int


# Iniciar app
app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido a la app de gastos grupales!"}

@app.post("/grupos/")
def crear_grupo(grupo: GrupoCreate, db: Session = Depends(get_db)):
    return crud.crear_grupo(db=db, grupo=grupo)

@app.get("/grupos/", response_model=List[GrupoOut])
def listar_grupos(db: Session = Depends(get_db)):
    return crud.obtener_grupos(db)

@app.post("/personas/")
def crear_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    return crud.crear_persona(db=db, persona=persona)

@app.post("/gastos/")
def crear_gasto(gasto: GastoCreate, db: Session = Depends(get_db)):
    return crud.crear_gasto(db=db, gasto=gasto)


# Crear las tablas
models.Base.metadata.create_all(bind=engine)
