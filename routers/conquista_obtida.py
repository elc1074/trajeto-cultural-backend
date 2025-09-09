from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ConquistaObtida
from schemas import ConquistaObtidaCreate, ConquistaObtidaOut

router = APIRouter(prefix="/conquistaobtida", tags=["conquistaobtida"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=ConquistaObtidaOut)
def register(achievement: ConquistaObtidaCreate, db: Session = Depends(get_db)):
    db_conquista = db.query(ConquistaObtida).filter(ConquistaObtida.id_conquista == achievement.id_conquista 
                                            and ConquistaObtida.id_usuario == achievement.id_usuario).first()
    if db_conquista:
        raise HTTPException(status_code=400, detail="Conquista já obtida")

    new_achievement = ConquistaObtida(id_conquista=achievement.id_conquista, id_usuario=achievement.id_usuario)
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)
    return new_achievement

@router.get("/get_lista", response_model=list[ConquistaObtidaOut])
def listar_conquistas_obtidas(db: Session = Depends(get_db)):
    return db.query(ConquistaObtida).all()