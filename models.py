"""
Modelos de Base de Datos - SQLAlchemy ORM
CiberSegurIA - Diagnóstico SGSI Express MVP
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class RespuestaEnum(enum.Enum):
    """Enum para las respuestas posibles del cuestionario"""
    SI = "Si"
    NO = "No"
    PARCIAL = "Parcial"
    NA = "N/A"


class User(Base):
    """Modelo de Usuario/Empresa Cliente"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String(255), nullable=False)
    rut = Column(String(12), unique=True, index=True, nullable=False)
    email_contacto = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    assessments = relationship("Assessment", back_populates="user")

    def __repr__(self):
        return f"<User {self.nombre_empresa} - {self.rut}>"


class Assessment(Base):
    """Modelo de Diagnóstico/Evaluación"""
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    puntaje_final = Column(Float, default=0.0)  # Porcentaje 0-100
    estado = Column(String(50), default="En Progreso")  # En Progreso, Completado

    # Relaciones
    user = relationship("User", back_populates="assessments")
    answers = relationship("Answer", back_populates="assessment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Assessment {self.id} - {self.puntaje_final}%>"


class Question(Base):
    """Modelo de Pregunta del Checklist"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    dominio = Column(String(100), nullable=False)  # Ej: "A.5 Políticas de Seguridad"
    subdominio = Column(String(100))  # Ej: "A.5.1 Dirección de la Gestión"
    pregunta = Column(Text, nullable=False)
    descripcion = Column(Text)  # Descripción adicional/contexto
    peso = Column(Integer, default=1)  # Peso para el cálculo de puntaje (1-5)
    orden = Column(Integer, default=0)  # Para ordenar preguntas en el cuestionario
    referencia_legal = Column(String(255))  # Ej: "Art. 4 Ley 21.663"

    # Relaciones
    answers = relationship("Answer", back_populates="question")

    def __repr__(self):
        return f"<Question {self.id} - {self.dominio}>"


class Answer(Base):
    """Modelo de Respuesta del Cliente"""
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    respuesta = Column(Enum(RespuestaEnum), nullable=False)
    evidencia_adjunta = Column(Text)  # Texto opcional con evidencia/comentarios
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    assessment = relationship("Assessment", back_populates="answers")
    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"<Answer Assessment:{self.assessment_id} Question:{self.question_id} - {self.respuesta}>"
