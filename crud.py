import asyncio
from sqlalchemy.orm import Session
from fastapi import HTTPException
import spellchecker
import models
import schemas


# получение списка задач (с пагинацией(а вдург их много))
def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()

# создание новой задачи с проверкой орфографии
def create_task(db: Session, task: schemas.TaskCreate):
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
    
    db_task = models.Task(title=task.title, description=task.description, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
