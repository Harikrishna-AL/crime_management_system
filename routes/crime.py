from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

router = APIRouter()
load_dotenv()

config = {
<<<<<<< HEAD
    "dbname": os.getenv("DB_NAME"),
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "host": "localhost",
    "port": os.getenv("DB_PORT"),
=======
    'dbname': os.getenv('DB_NAME'),
    'user': 'postgres',
    'password': os.getenv('DB_PASSWORD'),
    'host': 'localhost',
    'port': os.getenv('DB_PORT')
>>>>>>> e62069b (fixed streamlit errors)
}


def connect_to_db():
    return psycopg2.connect(**config)


class Crime(BaseModel):
    fir_id: int
    type_of_crime: str
    details: str
    investigation_id: int


@router.post("/crimes/")
def create_crime(crime: Crime):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_crime_query = """
        INSERT INTO CRIME (fir_id, type_of_crime, details, investigation_id)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            create_crime_query,
            (crime.fir_id, crime.type_of_crime, crime.details, crime.investigation_id),
        )
        conn.commit()
        return {"message": "Crime created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()


@router.get("/crimes/")
def read_crimes():
    conn = connect_to_db()
    cursor = conn.cursor()
    read_crimes_query = "SELECT * FROM CRIME"
    cursor.execute(read_crimes_query)
    crimes = cursor.fetchall()
    cursor.close()
    conn.close()
    return crimes


@router.get("/crimes/{crime_id}")
def read_crime(crime_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    read_crime_query = "SELECT * FROM CRIME WHERE crime_id = %s"
    cursor.execute(read_crime_query, (crime_id,))
    crime = cursor.fetchone()
    cursor.close()
    conn.close()
    if crime:
        return crime
    else:
        raise HTTPException(status_code=404, detail="Crime not found")


@router.put("/crimes/{crime_id}")
def update_crime(crime_id: int, crime: Crime):
    conn = connect_to_db()
    cursor = conn.cursor()
    update_crime_query = """
    UPDATE CRIME
    SET fir_id = %s, type_of_crime = %s, details = %s, investigation_id = %s
    WHERE crime_id = %s
    """
    cursor.execute(
        update_crime_query,
        (
            crime.fir_id,
            crime.type_of_crime,
            crime.details,
            crime.investigation_id,
            crime_id,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Crime updated successfully"}


@router.delete("/crimes/{crime_id}")
def delete_crime(crime_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_crime_query = "DELETE FROM CRIME WHERE crime_id = %s"
    cursor.execute(delete_crime_query, (crime_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Crime deleted successfully"}
