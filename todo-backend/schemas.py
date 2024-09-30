from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    creator_id: int

class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creator_id: int

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = None

class ProjectCreate(ProjectBase):
    creator_id: int

class Project(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    creator_id: int
    progress: Optional[int]
    status: Optional[str]

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: str
    points: Optional[int] = None
    schedule: Optional[str] = None
    project_id: Optional[int] = None

class TaskCreate(TaskBase):
    creator_id: int
    assignee_id: Optional[int] = None

class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    creator_id: int
    assignee_id: Optional[int] = None