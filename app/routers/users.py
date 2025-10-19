from fastapi.routing import APIRouter
from fastapi import Form, HTTPException, status, Depends

from app.core.security import verify_password, generate_token
from app.db.models import User
from app.schemas.user import UserOut
from app.dependencies import get_db
from app.services.user_service import create_user
from datetime import date

router = APIRouter(
    prefix="/users",
    tags=["auth"]
)


@router.post('/register', response_model=UserOut)
def register(
    username: str = Form(min_length=5, max_length=128),
    password: str = Form(min_length=8),
    first_name: str = Form(min_length=1, max_length=128),
    last_name: str = Form(default=None, max_length=128),
    birth_date: date = Form(default=None, max_length=10),
    phone: str = Form(default=None, max_length=15),
    email: str = Form(default=None, max_length=256),
    is_admin: bool = Form(default=False),
    session = Depends(get_db)
):
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists.")
    
    existing_email = session.query(User).filter_by(email=email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already in use.")
    
    return create_user(session, username, password, first_name, last_name, birth_date, email, phone, is_admin)


@router.post('/login')
def login(
    username: str = Form(min_length=5, max_length=128),
    password: str = Form(min_length=8),
    session = Depends(get_db)
):
    existing_user = session.query(User).filter_by(username=username).first()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found.")

    if not verify_password(password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect password.")
    
    data = {
        "sub": existing_user.username,
    }
    token = generate_token(data)
    
    return {'token': token}
