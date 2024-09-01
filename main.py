from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import uvicorn
from database import SessionLocal, engine
import models
import schemas
import crud

# Создание всех таблиц в базе данных
models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Get Tasks")


# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Маршрут для создания новой задачи
@app.post("/tasks/", response_model=schemas.Task)
def create_task(
    task: Annotated[schemas.TaskCreate, Depends()], db: Session = Depends(get_db)
):
    return crud.create_task(db=db, task=task)


# Маршрут для получения списка задач
@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
