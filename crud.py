from models import Conquista, Usuario
from schemas import ConquistaCreate
from sqlalchemy.orm import Session
from database import SessionLocal
import pandas as pd

def create_conquista(db: Session, achievement: ConquistaCreate):
    nova_conquista = Conquista(nome=achievement.nome, 
                        descricao=achievement.descricao, 
                        pontos=achievement.pontos)
    
    db.add(nova_conquista)
    db.commit()
    db.refresh(nova_conquista)

    return nova_conquista

def update_conquista(db: Session, nome: str, new_achievement: ConquistaCreate):
    db_conquista = db.query(Conquista).filter(Conquista.nome == nome).first()
    
    if db_conquista:
        db_conquista.descricao = new_achievement.descricao
        db_conquista.pontos = new_achievement.pontos
        
        db.commit()
        db.refresh(db_conquista)
        return True
        
    return False

def delete_conquista(db: Session, nome: str):
    db_conquista = db.query(Conquista).filter(Conquista.nome == nome).first()
    
    if db_conquista:
        db.delete(db_conquista)
        db.commit()
        return True
    
    return False

def update_pontos(db: Session, id: int, pontos_adicionais: int):
    db_usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if db_usuario:
        db_usuario.pontos = db_usuario.pontos + pontos_adicionais
        
        db.commit()
        db.refresh(db_usuario)
        return True
    
    return False