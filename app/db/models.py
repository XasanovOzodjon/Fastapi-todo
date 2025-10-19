from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Numeric

from app.db.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=128), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String(length=128), nullable=False)
    last_name = Column(String(length=128), nullable=True)
    birth_date = Column(String(length=10), nullable=True)
    phone = Column(String(length=15), nullable=True)
    email = Column(String(length=256), nullable=True, unique=True)
    is_admin = Column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f'User(id={self.id}, username={self.username})'
    

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=128), nullable=False, index=True)
    description = Column(Text, default='')
    status = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String(length=64), nullable=True)
    priority = Column(Integer, nullable=False, default=1)

    def __repr__(self) -> str:
        return f'Task(id={self.id}, name={self.name})'
    