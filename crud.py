from sqlalchemy.orm import Session
import models

def crear_grupo(db: Session, grupo):
    db_grupo = models.Grupo(nombre=grupo.nombre)
    db.add(db_grupo)
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

def obtener_grupos(db: Session):
    return db.query(models.Grupo).all()

def crear_persona(db: Session, persona):
    db_persona = models.Persona(nombre=persona.nombre, grupo_id=persona.grupo_id)
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

def crear_gasto(db: Session, gasto):
    db_gasto = models.Gasto(
        descripcion=gasto.descripcion,
        monto=gasto.monto,
        pagador_id=gasto.pagador_id,
        grupo_id=gasto.grupo_id
    )
    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto
