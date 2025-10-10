from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import ObraVisitada
from schemas import ObraVisitadaCreate, ObraVisitadaOut
from routers.usuario import get_db
from obter_conquista import AchievementService


router = APIRouter(prefix="/obravisitada", tags=["obravisitada"])

@router.post("/register", response_model=ObraVisitadaOut)
def register_obra_visitada(obra_visitada: ObraVisitadaCreate, db: Session = Depends(get_db)):
    db_obra = db.query(ObraVisitada).filter(
        ObraVisitada.id_obra == obra_visitada.id_obra,
        ObraVisitada.id_usuario == obra_visitada.id_usuario
    ).first()

    if db_obra:
        raise HTTPException(status_code=400, detail="Obra já visitada")

    nova_obra_visitada = ObraVisitada(
        id_obra=obra_visitada.id_obra,
        id_usuario=obra_visitada.id_usuario
    )
    db.add(nova_obra_visitada)
    db.commit()
    db.refresh(nova_obra_visitada)
    service = AchievementService(userId=obra_visitada.id_usuario)
    service.testa_por_numero_de_obras_visitadas()
    return nova_obra_visitada

@router.get("/get_lista", response_model=list[ObraVisitadaOut])
def listar_obras_visitadas(id_usuario: int, db: Session = Depends(get_db)):
    return db.query(ObraVisitada).filter(ObraVisitada.id_usuario == id_usuario).all()


@router.get("/get_obra_visitada", response_model=ObraVisitadaOut)
def get_obra_visitada(id_obra: int, id_usuario: int, db: Session = Depends(get_db)):
    obra_visitada = db.query(ObraVisitada).filter(ObraVisitada.id_obra == id_obra
                                                and ObraVisitada.id_usuario == id_usuario).first()
    if not obra_visitada:
        raise HTTPException(status_code=404, detail="Obra não visitada")
    return obra_visitada