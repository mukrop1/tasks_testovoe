from pydantic import BaseModel

# Базовая схема задачи
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool | None = False

# Схема для создания задачи
class TaskCreate(TaskBase):
    pass

# Схема для отображения задачи
class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True
        