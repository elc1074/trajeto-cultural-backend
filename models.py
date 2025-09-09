from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)  
    is_admin = Column(Boolean, default=False)
    avatar_url = Column(String, nullable=True)

    conquistas = relationship("ConquistaObtida", back_populates="usuario")
    obras_visitadas = relationship("ObraVisitada", back_populates="usuario")


class Conquista(Base):
    __tablename__ = "conquistas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)

    usuarios = relationship("ConquistaObtida", back_populates="conquista")


class ConquistaObtida(Base):
    __tablename__ = "conquistas_obtidas"

    id_conquista = Column(Integer, ForeignKey("conquistas.id"), primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)

    usuario = relationship("Usuario", back_populates="conquistas")
    conquista = relationship("Conquista", back_populates="usuarios")


class ObraVisitada(Base):
    __tablename__ = "obras_visitadas"

    id_obra = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)

    usuario = relationship("Usuario", back_populates="obras_visitadas")
