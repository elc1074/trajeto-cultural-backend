from models import Conquista
from schemas import ConquistaCreate
from sqlalchemy.orm import Session
from database import SessionLocal
import pandas as pd

def create_conquista(db: Session, achievement: ConquistaCreate):
    db_conquista = Conquista(nome=achievement.nome, 
                        descricao=achievement.descricao, 
                        pontos=achievement.pontos)
    
    db.add(db_conquista)
    db.commit()
    db.refresh(db_conquista)
    return db_conquista

def update_conquista(db: Session, nome: str, new_achievement: ConquistaCreate):
    db_conquista = db.query(Conquista).filter(Conquista.nome == nome).first()
    
    if db_conquista:
        db_conquista.descricao = new_achievement.descricao
        db_conquista.pontos = new_achievement.pontos
        
        db.commit()
        db.refresh(db_conquista)
        
    return db_conquista

def delete_conquista(db: Session, nome: str):
    db_conquista = db.query(Conquista).filter(Conquista.nome == nome).first()
    
    if db_conquista:
        db.delete(db_conquista)
        db.commit()
        return True
    
    return False


if __name__ == "__main__":
    conquistas = pd.read_csv("conquistas.csv")

    session = SessionLocal()
    
    for conquista in conquistas.itertuples():
        achievement = ConquistaCreate(nome=str(conquista[1]), descricao=str(conquista[2]), pontos=int(conquista[3]))
        create_conquista(db=session, achievement=achievement)