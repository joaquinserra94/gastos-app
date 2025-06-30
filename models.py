from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)

    personas = relationship("Persona", back_populates="grupo")
    gastos = relationship("Gasto", back_populates="grupo")

class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    grupo_id = Column(Integer, ForeignKey("grupos.id"))

    grupo = relationship("Grupo", back_populates="personas")
    gastos = relationship("Gasto", back_populates="pagador")

class Gasto(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    monto = Column(Float)

    pagador_id = Column(Integer, ForeignKey("personas.id"))
    grupo_id = Column(Integer, ForeignKey("grupos.id"))

    pagador = relationship("Persona", back_populates="gastos")
    grupo = relationship("Grupo", back_populates="gastos")

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    deudor_id = Column(Integer, ForeignKey("personas.id"))
    acreedor_id = Column(Integer, ForeignKey("personas.id"))
    grupo_id = Column(Integer, ForeignKey("grupos.id"))
    monto = Column(Float)
    fecha = Column(DateTime, default=datetime.utcnow)

    grupo = relationship("Grupo")
