from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, engine

class User(Base):
    __tablename__ = 'users'
    
    name: Mapped[str]
    surname: Mapped[str] 
    username: Mapped[str] =mapped_column(unique=True) 
    password: Mapped[str]

if __name__ == '__main__':
    Base.metadata.create_all(engine)