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
    'password': os.getenv('DB_PASSWORD'),
    'host': 'localhost',
    'port': os.getenv('DB_PORT')
}


def connect_to_db():
    return psycopg2.connect(**config)


class FIR(BaseModel):
    police_station_id: int
    officer_id: int
    title: str
    act: str
    complaint_name: str
    date_added: str
    details: str


@router.post("/firs/")
def create_fir(fir: FIR):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_fir_query = """
        INSERT INTO FIR (police_station_id, officer_id, title, act, complaint_name, date_added, details)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            create_fir_query,
            (
                fir.police_station_id,
                fir.officer_id,
                fir.title,
                fir.act,
                fir.complaint_name,
                fir.date_added,
                fir.details,
            ),
        )
        conn.commit()
        return {"message": "FIR created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()


@router.get("/firs/")
def read_firs():
    conn = connect_to_db()
    cursor = conn.cursor()
    read_firs_query = "SELECT * FROM FIR"
    cursor.execute(read_firs_query)
    firs = cursor.fetchall()
    cursor.close()
    conn.close()
    return firs


@router.get("/firs/{fir_id}")
def read_fir(fir_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    read_fir_query = "SELECT * FROM FIR WHERE fir_id = %s"
    cursor.execute(read_fir_query, (fir_id,))
    fir = cursor.fetchone()
    cursor.close()
    conn.close()
    if fir:
        return fir
    else:
        raise HTTPException(status_code=404, detail="FIR not found")


@router.put("/firs/{fir_id}")
def update_fir(fir_id: int, fir: FIR):
    conn = connect_to_db()
    cursor = conn.cursor()
    update_fir_query = """
    UPDATE FIR
    SET police_station_id = %s, officer_id = %s, title = %s, act = %s, complaint_name = %s, date_added = %s, details = %s
    WHERE fir_id = %s
    """
    cursor.execute(
        update_fir_query,
        (
            fir.police_station_id,
            fir.officer_id,
            fir.title,
            fir.act,
            fir.complaint_name,
            fir.date_added,
            fir.details,
            fir_id,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "FIR updated successfully"}


@router.delete("/firs/{fir_id}")
def delete_fir(fir_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_fir_query = "DELETE FROM FIR WHERE fir_id = %s"
    cursor.execute(delete_fir_query, (fir_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "FIR deleted successfully"}
