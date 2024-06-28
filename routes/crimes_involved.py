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


class CrimesInvolved(BaseModel):
    crime_id: int
    criminal_id: int


@router.post("/crimes_involved/")
def create_crimes_involved(crimes_involved: CrimesInvolved):
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        create_crimes_involved_query = """
        INSERT INTO Crimes_Involved (crime_id, criminal_id)
        VALUES (%s, %s)
        """
        cursor.execute(
            create_crimes_involved_query,
            (crimes_involved.crime_id, crimes_involved.criminal_id),
        )
        conn.commit()
        return {"message": "Crimes Involved created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()


@router.get("/crimes_involved/")
def read_crimes_involved():
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    read_crimes_involved_query = "SELECT * FROM Crimes_Involved"
    cursor.execute(read_crimes_involved_query)
    crimes_involved = cursor.fetchall()
    cursor.close()
    conn.close()
    return crimes_involved


@router.get("/crimes_involved/{crime_id}/{criminal_id}")
def read_crimes_involved(crime_id: int, criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    read_crimes_involved_query = (
        "SELECT * FROM Crimes_Involved WHERE crime_id = %s AND criminal_id = %s"
    )
    cursor.execute(read_crimes_involved_query, (crime_id, criminal_id))
    crimes_involved = cursor.fetchone()
    cursor.close()
    conn.close()
    if crimes_involved:
        return crimes_involved
    else:
        raise HTTPException(status_code=404, detail="Crimes Involved not found")


@router.delete("/crimes_involved/{crime_id}/{criminal_id}")
def delete_crimes_involved(crime_id: int, criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    delete_crimes_involved_query = (
        "DELETE FROM Crimes_Involved WHERE crime_id = %s AND criminal_id = %s"
    )
    cursor.execute(delete_crimes_involved_query, (crime_id, criminal_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Crimes Involved deleted successfully"}
