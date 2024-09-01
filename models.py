from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from database import Base

# Определяем модель Task - таблица заданий
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    
# Определим модель Users - таблица юзеров
# class Users(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False)
#     username = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     role_id = Column(Integer, ForeignKey("tasks.id"))
