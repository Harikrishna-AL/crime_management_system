from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

router = APIRouter()
load_dotenv()

config = {
    "dbname": os.getenv("DB_NAME"),
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "host": "localhost",
    "port": os.getenv("DB_PORT"),
}


def connect_to_db():
    return psycopg2.connect(**config)


class Criminal(BaseModel):
    name: str
    address: str
    gender: str
    height: str
    date_arrest: str
    date_birth: str


@router.post("/criminals/")
def create_criminal(criminal: Criminal):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_criminal_query = """
        INSERT INTO CRIMINAL (name, address, gender, height, date_arrest, date_birth)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            create_criminal_query,
            (
                criminal.name,
                criminal.address,
                criminal.gender,
                criminal.height,
                criminal.date_arrest,
                criminal.date_birth,
            ),
        )
        conn.commit()
        return {"message": "Criminal created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()


@router.get("/criminals/")
def read_criminals():
    conn = connect_to_db()
    cursor = conn.cursor()
    read_criminals_query = "SELECT * FROM CRIMINAL"
    cursor.execute(read_criminals_query)
    criminals = cursor.fetchall()
    cursor.close()
    conn.close()
    return criminals


@router.get("/criminals/{criminal_id}")
def read_criminal(criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    read_criminal_query = "SELECT * FROM CRIMINAL WHERE criminal_id = %s"
    cursor.execute(read_criminal_query, (criminal_id,))
    criminal = cursor.fetchone()
    cursor.close()
    conn.close()
    if criminal:
        return criminal
    else:
        raise HTTPException(status_code=404, detail="Criminal not found")


@router.put("/criminals/{criminal_id}")
def update_criminal(criminal_id: int, criminal: Criminal):
    conn = connect_to_db()
    cursor = conn.cursor()
    update_criminal_query = """
    UPDATE CRIMINAL
    SET name = %s, address = %s, gender = %s, height = %s, date_arrest = %s, date_birth = %s
    WHERE criminal_id = %s
    """
    cursor.execute(
        update_criminal_query,
        (
            criminal.name,
            criminal.address,
            criminal.gender,
            criminal.height,
            criminal.date_arrest,
            criminal.date_birth,
            criminal_id,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Criminal updated successfully"}


@router.delete("/criminals/{criminal_id}")
def delete_criminal(criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_criminal_query = "DELETE FROM CRIMINAL WHERE criminal_id = %s"
    cursor.execute(delete_criminal_query, (criminal_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Criminal deleted successfully"}
