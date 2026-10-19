# Script de pruebas para ejecutar tus consultas
import sys
from pathlib import Path

# Añadir la carpeta 'src' al PYTHONPATH dinámicamente
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from chatbot_core.retrieval.models_sqlite import Base, ProgramaAcademico, Investigador

# 1. Configurar la base de datos SQLite local
DB_PATH = "data/ciicap_mock.db"
os.makedirs("data", exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# Crear las tablas definidas en los modelos
Base.metadata.create_all(engine)


def poblar_datos_prueba():
    """Inserta datos de prueba simulando la BD del CIICAp."""
    with Session(engine) as session:
        # Verificar si ya existen datos
        if session.scalars(select(ProgramaAcademico)).first():
            return

        # Insertar Programas
        m_ia = ProgramaAcademico(
            nombre="Maestría en Ingeniería y Ciencias Aplicadas",
            nivel="Maestría",
            descripcion="Programa enfocado en inteligencia artificial, procesamiento de señales y optimización.",
            requisitos="Título de licenciatura, promedio mínimo de 8.0, examen de admisión."
        )
        d_ia = ProgramaAcademico(
            nombre="Doctorado en Ciencias Aplicadas",
            nivel="Doctorado",
            descripcion="Investigación de alto nivel en ciencias aplicadas y tecnología.",
            requisitos="Grado de maestría, propuesta de tesis, entrevista con comité."
        )

        session.add_all([m_ia, d_ia])
        session.commit()

        # Insertar Investigadores
        inv1 = Investigador(
            nombre="Dr. Arturo C.I.",
            linea_investigacion="Procesamiento de Lenguaje Natural y RAG",
            correo="arturo@ciicap.uaem.mx",
            programa=m_ia
        )
        inv2 = Investigador(
            nombre="Dra. Elena Ramos",
            linea_investigacion="Visión por Computadora y Robótica",
            correo="elena.ramos@ciicap.uaem.mx",
            programa=m_ia
        )

        session.add_all([inv1, inv2])
        session.commit()
        print("✅ Base de datos simulada inicializada con éxito.")


# ------------------------------------------------------------------
# EJERCICIOS DE CONSULTA (Lo que te pidió practicar tu profesor)
# ------------------------------------------------------------------

def practica_consultas():
    poblar_datos_prueba()

    with Session(engine) as session:
        print("\n--- 1. CONSULTA COMPLETA (select(Model)) ---")
        stmt = select(ProgramaAcademico)
        programas = session.scalars(stmt).all()
        for prog in programas:
            print(f"[{prog.nivel}] {prog.nombre}")

        print("\n--- 2. FILTRADO CON WHERE ---")
        stmt_filtrado = select(Investigador).where(
            Investigador.linea_investigacion.like("%Lenguaje Natural%")
        )
        investigador = session.scalars(stmt_filtrado).first()
        if investigador:
            print(f"Investigador encontrado: {investigador.nombre} - Línea: {investigador.linea_investigacion}")

        print("\n--- 3. SELECCIÓN DE COLUMNAS ESPECÍFICAS (GeeksForGeeks Ref) ---")
        # En lugar de traer todo el objeto, traemos solo los campos de interés para el RAG
        stmt_columnas = select(Investigador.nombre, Investigador.correo)
        resultados = session.execute(stmt_columnas).all()
        for nombre, correo in resultados:
            print(f"Nombre: {nombre} | Correo: {correo}")

        print("\n--- 4. CONSULTA CON RELACIONES (JOINs) ---")
        # Traer el programa y sus investigadores asociados
        stmt_join = select(ProgramaAcademico).where(ProgramaAcademico.nivel == "Maestría")
        maestria = session.scalars(stmt_join).first()
        if maestria:
            print(f"Programa: {maestria.nombre}")
            for inv in maestria.investigadores:
                print(f"  -> Docente: {inv.nombre}")


if __name__ == "__main__":
    practica_consultas()