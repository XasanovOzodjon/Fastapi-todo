from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.models import User
from datetime import date


def create_user(session: Session, username: str, password: str, first_name: str, last_name: str | None, birth_date: date | None, email: str | None, phone: str | None, is_admin: bool) -> User:
    user = User(
        username=username,
        hashed_password=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        phone=phone,
        email=email,
        is_admin=is_admin
        )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

