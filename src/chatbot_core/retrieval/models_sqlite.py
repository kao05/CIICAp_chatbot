# Definición de Modelos ORM (SQLAlchemy)
# Vamos a realizar una base de datos de prueba intentando imitar la del CIICAp

# src/chatbot_core/retrieval/models_sqlite.py
from typing import Optional
from sqlalchemy import String, Text, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# 1. Clase Base para todos los modelos
class Base(DeclarativeBase):
    pass

# 2. Modelo de Programas Académicos (Maestrías/Doctorados)
class ProgramaAcademico(Base):
    __tablename__ = "programas_academicos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    nivel: Mapped[str] = mapped_column(String(50))  # Ej: 'Maestría', 'Doctorado'
    descripcion: Mapped[str] = mapped_column(Text)
    requisitos: Mapped[str] = mapped_column(Text)

    # Relación con investigadores
    investigadores: Mapped[list["Investigador"]] = relationship(back_populates="programa")


# 3. Modelo de Investigadores del CIICAp
class Investigador(Base):
    __tablename__ = "investigadores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    linea_investigacion: Mapped[str] = mapped_column(String(200))
    correo: Mapped[str] = mapped_column(String(100))
    programa_id: Mapped[Optional[int]] = mapped_column(ForeignKey("programas_academicos.id"))

    programa: Mapped[Optional[ProgramaAcademico]] = relationship(back_populates="investigadores")