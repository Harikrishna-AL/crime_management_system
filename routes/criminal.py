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


class Criminal(BaseModel):
    first_name: str
    last_name: str
    address: str
    city: str
    gender: str
    height: float
    date_arrest: str
    date_release: str
    date_birth: str
    occupation: str


@router.post("/criminals/")
def create_criminal(criminal: Criminal):
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        create_criminal_query = """
        INSERT INTO CRIMINAL (first_name, last_name, address, city, gender, height, date_arrest, date_release, date_birth, occupation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            create_criminal_query,
            (
                criminal.first_name,
                criminal.last_name,
                criminal.address,
                criminal.city,
                criminal.gender,
                criminal.height,
                criminal.date_arrest,
                criminal.date_release,
                criminal.date_birth,
                criminal.occupation,
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


@router.get("/getCriminalRecords/")
def get_criminal_records(first_name: str, last_name: str):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        read_criminal_records_query = """
        SELECT CRIME.*, POLICE_OFFICER.officer_id, CONCAT(POLICE_OFFICER.first_name, ' ', POLICE_OFFICER.last_name) AS officer_name
        FROM CRIMINAL
        JOIN CRIMES_INVOLVED ON CRIMINAL.criminal_id = CRIMES_INVOLVED.criminal_id
        JOIN CRIME ON CRIMES_INVOLVED.crime_id = CRIME.crime_id
        JOIN FIR ON CRIME.fir_id = FIR.fir_id
        JOIN POLICE_OFFICER ON FIR.officer_id = POLICE_OFFICER.officer_id
        WHERE CRIMINAL.first_name = %s AND CRIMINAL.last_name = %s
        """
        cursor.execute(read_criminal_records_query, (first_name, last_name))
        criminal_records = cursor.fetchall()
        if not criminal_records:
            raise HTTPException(status_code=404, detail="Criminal records not found")
        return criminal_records
    except Exception as err:
        return {"message": f"Error: {err}"}

@router.get("/criminals/")
def read_criminals():
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    read_criminals_query = "SELECT * FROM CRIMINAL"
    cursor.execute(read_criminals_query)
    criminals = cursor.fetchall()
    cursor.close()
    conn.close()
    return criminals


@router.get("/criminals/{criminal_id}")
def read_criminal(criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
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
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    update_criminal_query = """
    UPDATE CRIMINAL
    SET first_name = %s, last_name = %s, address = %s, city = %s, gender = %s, height = %s, date_arrest = %s, date_release = %s, date_birth = %s, occupation = %s
    WHERE criminal_id = %s
    """
    cursor.execute(
        update_criminal_query,
        (
            criminal.first_name,
            criminal.last_name,
            criminal.address,
            criminal.city,
            criminal.gender,
            criminal.height,
            criminal.date_arrest,
            criminal.date_release,
            criminal.date_birth,
            criminal.occupation,
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
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    delete_criminal_query = "DELETE FROM CRIMINAL WHERE criminal_id = %s"
    cursor.execute(delete_criminal_query, (criminal_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Criminal deleted successfully"}
