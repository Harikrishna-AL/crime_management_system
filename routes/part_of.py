from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
from psycopg2.extras import RealDictCursor

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


class PartOf(BaseModel):
    investigation_id: int
    criminal_id: int


@router.post("/part_of/")
def create_part_of(part_of: PartOf):
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        create_part_of_query = """
        INSERT INTO Part_Of (investigation_id, criminal_id)
        VALUES (%s, %s)
        """
        cursor.execute(
            create_part_of_query, (part_of.investigation_id, part_of.criminal_id)
        )
        conn.commit()
        return {"message": "Part Of created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()


@router.get("/part_of/")
def read_part_of():
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    read_part_of_query = "SELECT * FROM Part_Of"
    cursor.execute(read_part_of_query)
    part_of = cursor.fetchall()
    cursor.close()
    conn.close()
    return part_of


@router.get("/part_of/{investigation_id}/{criminal_id}")
def read_part_of(investigation_id: int, criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    read_part_of_query = (
        "SELECT * FROM Part_Of WHERE investigation_id = %s AND criminal_id = %s"
    )
    cursor.execute(read_part_of_query, (investigation_id, criminal_id))
    part_of = cursor.fetchone()
    cursor.close()
    conn.close()
    if part_of:
        return part_of
    else:
        raise HTTPException(status_code=404, detail="Part Of not found")


@router.delete("/part_of/{investigation_id}/{criminal_id}")
def delete_part_of(investigation_id: int, criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    delete_part_of_query = (
        "DELETE FROM Part_Of WHERE investigation_id = %s AND criminal_id = %s"
    )
    cursor.execute(delete_part_of_query, (investigation_id, criminal_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Part Of deleted successfully"}
