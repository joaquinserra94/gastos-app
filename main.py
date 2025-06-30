from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models
import crud
from pydantic import BaseModel
from typing import List
from datetime import datetime


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

class GastoOut(BaseModel):
    id: int
    descripcion: str
    monto: float
    pagador_id: int
    grupo_id: int

    class Config:
        orm_mode = True


class PagoCreate(BaseModel):
    deudor_id: int
    acreedor_id: int
    grupo_id: int
    monto: float

class PagoOut(PagoCreate):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True



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

@app.get("/gastos/", response_model=List[GastoOut])
def listar_gastos(grupo_id: int, db: Session = Depends(get_db)):
    return crud.obtener_gastos_por_grupo(db=db, grupo_id=grupo_id)

@app.get("/grupos/{grupo_id}/resumen")
def resumen_grupo(grupo_id: int, db: Session = Depends(get_db)):
    return crud.calcular_resumen_grupo(db=db, grupo_id=grupo_id)

@app.get("/grupos/{grupo_id}/personas/resumen")
def resumen_por_persona(grupo_id: int, db: Session = Depends(get_db)):
    return crud.resumen_individual(db=db, grupo_id=grupo_id)

@app.get("/grupos/{grupo_id}/liquidacion")
def liquidacion(grupo_id: int, db: Session = Depends(get_db)):
    return crud.calcular_liquidacion(db=db, grupo_id=grupo_id)

@app.post("/pagos/", response_model=PagoOut)
def registrar_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    return crud.registrar_pago(db=db, pago=pago)

@app.get("/pagos/", response_model=List[PagoOut])
def listar_pagos(grupo_id: int, db: Session = Depends(get_db)):
    return crud.obtener_pagos(db=db, grupo_id=grupo_id)


# Crear las tablas
models.Base.metadata.create_all(bind=engine)

