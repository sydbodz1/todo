from typing import List
from fastapi import APIRouter, HTTPException
import schemas, crud

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    return crud.create_user(user)

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int):
    db_user = crud.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate):
    return crud.create_category(category)

@router.get("/categories/", response_model=List[schemas.Category])
def read_categories():
    return crud.get_categories()

@router.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate):
    return crud.create_project(project)

@router.get("/projects/", response_model=List[schemas.Project])
def read_projects():
    return crud.get_projects()

@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate):
    return crud.create_task(task)

@router.get("/tasks/", response_model=List[schemas.Task])
def read_tasks():
    return crud.get_tasks()