import asyncio
from sqlalchemy.orm import Session
from fastapi import HTTPException
import spellchecker
import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# получение списка задач (с пагинацией(а вдург их много))
def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()

# создание новой задачи с проверкой орфографии
def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    # Проверяем в поле title.т.к. оно обязательное
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    spelling_results = loop.run_until_complete(spellchecker.check_spelling([task.title]))
    
    # Проверим есть ли ошибки в результате
    if spelling_results and spelling_results[0]:
        errors = spelling_results[0]
        corrections = []
        
        for error in errors:
            word = error['word']
            suggestions = ", ".join(error['s'])
            corrections.append(f"'{word}' -> {suggestions}")
        
        correction_message = "; ".join(corrections)
        raise HTTPException(
            status_code=400, 
            detail=f"Найдены орфографические ошибки в поле title. Возможно, вы имели в виду: {correction_message}."
        )
    
    db_task = models.Task(title=task.title, description=task.description, completed=task.completed, owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
