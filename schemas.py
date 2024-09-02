from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    # items: list[Task] = []

    class Config:
        from_attributes = True

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
    owner_id: int

    class Config:
        from_attributes = True
        