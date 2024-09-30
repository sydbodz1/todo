import schemas
from database import get_connection

# User CRUD
def create_user(user: schemas.UserCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id, username, email, created_at, updated_at",
                (user.username, user.email, user.password)
            )
            result = cur.fetchone()
            if result is None:
                return None
            conn.commit()
            return schemas.User(
                id=result[0],
                username=result[1],
                email=result[2],
                created_at=result[3],
                updated_at=result[4]
            )

def get_user(user_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, username, email, created_at, updated_at FROM users WHERE id = %s",
                (user_id,)
            )
            result = cur.fetchone()
            if result is None:
                return None
            return schemas.User(
                id=result[0],
                username=result[1],
                email=result[2],
                created_at=result[3],
                updated_at=result[4]
            )

# Category CRUD
def create_category(category: schemas.CategoryCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO categories (name, creator_id) VALUES (%s, %s) RETURNING id, name, creator_id",
                (category.name, category.creator_id)
            )
            conn.commit()
            result = cur.fetchone()
            return schemas.Category(id=result[0], name=result[1], creator_id=result[2])

def get_categories():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, creator_id FROM categories")
            results = cur.fetchall()
            return [schemas.Category(id=row[0], name=row[1], creator_id=row[2]) for row in results]

# Project CRUD
def create_project(project: schemas.ProjectCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO projects (title, description, category_id, creator_id) VALUES (%s, %s, %s, %s) RETURNING id, title, description, category_id, creator_id, status, progress",
                (project.title, project.description, project.category_id, project.creator_id)
            )
            conn.commit()
            result = cur.fetchone()
            print(cur)
            print(result)
            return schemas.Project(
                id=result[0],
                title=result[1],
                description=result[2],
                category_id=result[3],
                creator_id=result[4],
                status=result[5],
                progress=result[6]
            )

def get_projects():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, description, category_id, creator_id, status, progress FROM projects")
            results = cur.fetchall()
            print(results)
            return [
                schemas.Project(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    category_id=row[3],
                    creator_id=row[4],
                    status=row[5],
                    progress=row[6]
                )
                for row in results
            ]

# Task CRUD
def create_task(task: schemas.TaskCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title, description, created_at, updated_at, deadline, status, points, schedule, project_id, creator_id, assignee_id) "
                "VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s) "
                "RETURNING id, title, description, created_at, updated_at, deadline, status, points, schedule, project_id, creator_id, assignee_id",
                (task.title, task.description, task.deadline, task.status, task.points, task.schedule, task.project_id, task.creator_id, task.assignee_id)
            )
            conn.commit()
            result = cur.fetchone()
            return schemas.Task(
                id=result[0],
                title=result[1],
                description=result[2],
                created_at=result[3],
                updated_at=result[4],
                deadline=result[5],
                status=result[6],
                points=result[7],
                schedule=result[8],
                project_id=result[9],
                creator_id=result[10],
                assignee_id=result[11]
            )

def get_tasks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, description, created_at, updated_at, deadline, status, points, schedule, project_id, creator_id, assignee_id FROM tasks")
            results = cur.fetchall()
            return [
                schemas.Task(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    created_at=row[3],
                    updated_at=row[4],
                    deadline=row[5],
                    status=row[6],
                    points=row[7],
                    schedule=row[8],
                    project_id=row[9],
                    creator_id=row[10],
                    assignee_id=row[11]
                )
                for row in results
            ]
