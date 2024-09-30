import os
import psycopg

def get_connection():
    return psycopg.connect(os.getenv("DATABASE_URL"))

def create_tables():
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    create_categories_table = """
    CREATE TABLE IF NOT EXISTS categories (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        creator_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    create_projects_table = """
    CREATE TABLE IF NOT EXISTS projects (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
        creator_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        progress INTEGER DEFAULT 0,
        status VARCHAR(20) DEFAULT 'not started' CHECK (status IN ('not started', 'in progress', 'completed')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        deadline TIMESTAMP,
        status VARCHAR(20) DEFAULT 'not started' CHECK (status IN ('not started', 'in progress', 'completed', 'on hold')),
        points INTEGER,
        schedule VARCHAR(50),
        project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
        creator_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        assignee_id INTEGER REFERENCES users(id) ON DELETE SET NULL
    );
    """

    create_follows_table = """
    CREATE TABLE IF NOT EXISTS follows (
        follower_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        followed_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        PRIMARY KEY (follower_id, followed_id)
    );
    """

    create_user_categories_table = """
    CREATE TABLE IF NOT EXISTS user_categories (
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
        PRIMARY KEY (user_id, category_id)
    );
    """

    create_user_projects_table = """
    CREATE TABLE IF NOT EXISTS user_projects (
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
        PRIMARY KEY (user_id, project_id)
    );
    """

    create_user_tasks_table = """
    CREATE TABLE IF NOT EXISTS user_tasks (
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
        PRIMARY KEY (user_id, task_id)
    );
    """

    create_comments_table = """
    CREATE TABLE IF NOT EXISTS comments (
        id SERIAL PRIMARY KEY,
        task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(create_users_table)
            cur.execute(create_categories_table)
            cur.execute(create_projects_table)
            cur.execute(create_tasks_table)
            cur.execute(create_follows_table)
            cur.execute(create_user_categories_table)
            cur.execute(create_user_projects_table)
            cur.execute(create_user_tasks_table)
            cur.execute(create_comments_table)
            conn.commit()