

database_url = "postgresql://trajeto_cultural_db_user:k1g8Uquxnm05ORdmhr79AZFizdnQIV3q@dpg-d2vd37ripnbc73cil1k0-a.oregon-postgres.render.com/trajeto_cultural_db"

# Exemplo da função de inserção no main.py ou em crud.py
# Lembre-se de importar os módulos necessários
from models import Conquista
from schemas import ConquistaCreate
from sqlalchemy.orm import Session
from database import SessionLocal
import pandas as pd

def create_item(db: Session, achievement: ConquistaCreate):
    db_item = Conquista(nome=achievement.nome, 
                        descricao=achievement.descricao, 
                        pontos=achievement.pontos)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

if __name__ == "__main__":
    conquistas = pd.read_csv("conquistas.csv")

    session = SessionLocal()
    
    for conquista in conquistas.itertuples():
        achievement = ConquistaCreate(nome=conquista[1], descricao=conquista[2], pontos=conquista[3])
        create_item(db=session, achievement=achievement)