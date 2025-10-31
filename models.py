from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import DateTime, func, Enum
import enum

class Personas(enum.Enum):
    'Apreciador de arte' = 1
    'Crítico de arte' = 2
    'Crítico de críticos de arte' = 3

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)  
    is_admin = Column(Boolean, default=False)
    avatar_url = Column(String, nullable=True)
    pontos = Column(Integer, default=0)
    persona = Column(Enum(Personas), nullable=False, default=1)

    conquistas = relationship("ConquistaObtida", back_populates="usuario")
    obras_visitadas = relationship("ObraVisitada", back_populates="usuario")


class Conquista(Base):
    __tablename__ = "conquistas"

    nome = Column(String, primary_key=True)
    descricao = Column(String, nullable=False)
    pontos = Column(Integer, nullable=False)
    

    usuarios = relationship("ConquistaObtida", back_populates="conquista")


class ConquistaObtida(Base):
    __tablename__ = "conquistas_obtidas"

    nome_conquista = Column(String, ForeignKey("conquistas.nome"), primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    data_obtida = Column(DateTime, default=func.now())

    usuario = relationship("Usuario", back_populates="conquistas")
    conquista = relationship("Conquista", back_populates="usuarios")


class ObraVisitada(Base):
    __tablename__ = "obras_visitadas"

    id_obra = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)

    usuario = relationship("Usuario", back_populates="obras_visitadas")
