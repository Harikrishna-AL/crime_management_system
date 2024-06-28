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


class Investigation(BaseModel):
    evidence: str
    suspects: str
    fir_id: int


@router.post("/investigations/")
def create_investigation(investigation: Investigation):
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        create_investigation_query = """
        INSERT INTO INVESTIGATION (evidence, suspects, fir_id)
        VALUES (%s, %s, %s)
        """
        cursor.execute(
            create_investigation_query,
            (investigation.evidence, investigation.suspects, investigation.fir_id),
        )
        conn.commit()
        return {"message": "Investigation created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()


@router.get("/investigations/")
def read_investigations():
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    read_investigations_query = "SELECT * FROM INVESTIGATION"
    cursor.execute(read_investigations_query)
    investigations = cursor.fetchall()
    cursor.close()
    conn.close()
    return investigations


@router.get("/investigations/{investigation_id}")
def read_investigation(investigation_id: int):
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    read_investigation_query = "SELECT * FROM INVESTIGATION WHERE investigation_id = %s"
    cursor.execute(read_investigation_query, (investigation_id,))
    investigation = cursor.fetchone()
    cursor.close()
    conn.close()
    if investigation:
        return investigation
    else:
        raise HTTPException(status_code=404, detail="Investigation not found")


@router.put("/investigations/{investigation_id}")
def update_investigation(investigation_id: int, investigation: Investigation):
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    update_investigation_query = """
    UPDATE INVESTIGATION
    SET evidence = %s, suspects = %s, fir_id = %s
    WHERE investigation_id = %s
    """
    cursor.execute(
        update_investigation_query,
        (
            investigation.evidence,
            investigation.suspects,
            investigation.fir_id,
            investigation_id,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Investigation updated successfully"}


@router.delete("/investigations/{investigation_id}")
def delete_investigation(investigation_id: int):
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    delete_investigation_query = "DELETE FROM INVESTIGATION WHERE investigation_id = %s"
    cursor.execute(delete_investigation_query, (investigation_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Investigation deleted successfully"}
