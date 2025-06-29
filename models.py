from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

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
