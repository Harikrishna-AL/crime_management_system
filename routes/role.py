from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os 

router = APIRouter()
load_dotenv()

config = {
    'dbname': os.getenv('DB_NAME'),
    'user': 'postgres',
    'password': 'hari2430',
    'host': 'localhost',
    'port': os.getenv('DB_PORT')
}

def connect_to_db():
    return psycopg2.connect(**config)

class Role(BaseModel):
    role_name: str
    permission: str

@router.get("/roles/")
def read_roles():
    conn = connect_to_db()
    cursor = conn.cursor()
    read_roles_query = "SELECT * FROM ROLE"
    cursor.execute(read_roles_query)
    roles = cursor.fetchall()
    cursor.close()
    conn.close()
    return roles

@router.post("/roles/")
def create_role(role: Role):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_role_query = """
        INSERT INTO ROLE (role_name, permission)
        VALUES (%s, %s)
        """
        cursor.execute(create_role_query, (role.role_name, role.permission))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Role created successfully"}

    except Exception as err:
        conn.rollback()  # Rollback any changes if an error occurs
        return {"message": f"Error: {err}"}

    finally:
        if conn is not None:
            cursor.close()
            conn.close()

@router.put("/roles/{role_id}")
def update_role(role_id: int, role: Role):
    conn = connect_to_db()
    cursor = conn.cursor()
    update_role_query = """
    UPDATE ROLE
    SET role_name = %s, permission = %s
    WHERE role_id = %s
    """
    cursor.execute(update_role_query, (
        role.role_name, role.permission, role_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Role updated successfully"}

@router.delete("/roles/{role_id}")
def delete_role(role_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_role_query = "DELETE FROM ROLE WHERE role_id = %s"
    cursor.execute(delete_role_query, (role_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Role deleted successfully"}