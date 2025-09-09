from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Usuario
from schemas import UsuarioCreate, UsuarioOut
from passlib.hash import bcrypt
import cloudinary
import cloudinary.uploader
import os

router = APIRouter(prefix="/usuario", tags=["usuario"])

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UsuarioOut)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    hashed_password = bcrypt.hash(user.senha)
    new_user = Usuario(nome=user.nome, email=user.email, senha=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if not db_user or not bcrypt.verify(user.senha, db_user.senha):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    return {
        "message": "Login bem-sucedido",
        "user_id": db_user.id,
        "nome": db_user.nome,
        "email": db_user.email,
        "is_admin": db_user.is_admin,
        "avatar_url": db_user.avatar_url,
    }


@router.get("/get_lista", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.put("/update/{user_id}")
def update_user(
    user_id: int,
    nome: str = Form(None),
    email: str = Form(None),
    senha: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        return {"error": "Usuário não encontrado"}

    if nome:
        user.nome = nome
    if email:
        user.email = email
    if senha:
        user.senha = bcrypt.hash(senha)

    if file:
        result = cloudinary.uploader.upload(file.file, folder="trajeto_cultural/avatars")
        user.avatar_url = result["secure_url"]

    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "avatar_url": user.avatar_url
    }
