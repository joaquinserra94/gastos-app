from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models
import crud
from pydantic import BaseModel
from typing import List
from datetime import datetime
from fastapi.responses import JSONResponse

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Iniciar app (¡esto debe ir antes de usar `app`!)
app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

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

class GrupoUpdate(BaseModel):
    nombre: str

class PersonaUpdate(BaseModel):
    nombre: str



# Iniciar app
app = FastAPI()



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

@app.get("/grupos/{grupo_id}")
def obtener_grupo(grupo_id: int, db: Session = Depends(get_db)):
    grupo = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if not grupo:
        return JSONResponse(content={"error": "Grupo no encontrado"}, status_code=404)

    return {
        "id": grupo.id,
        "nombre": grupo.nombre,
        "personas": [{"id": p.id, "nombre": p.nombre} for p in grupo.personas]
    }

@app.put("/grupos/{grupo_id}")
def actualizar_grupo(grupo_id: int, datos: GrupoUpdate, db: Session = Depends(get_db)):
    return crud.editar_grupo(db=db, grupo_id=grupo_id, nuevo_nombre=datos.nombre)

@app.put("/personas/{persona_id}")
def actualizar_persona(persona_id: int, datos: PersonaUpdate, db: Session = Depends(get_db)):
    return crud.editar_persona(db=db, persona_id=persona_id, nuevo_nombre=datos.nombre)

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join("frontend", "index.html"))

# Crear las tablas
models.Base.metadata.create_all(bind=engine)

