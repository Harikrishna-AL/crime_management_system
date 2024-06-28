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


class InvestigationOfficer(BaseModel):
    officer_id: int
    investigation_id: int


@router.get("/officerAffiliation/{officer_id}")
def get_investigation_officer_affiliation(officer_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()  # Using DictCursor for easier JSON serialization
    try:
        read_investigation_officer_affiliation_query = """
        SELECT FIR.*, INVESTIGATION.*
        FROM INVESTIGATION_OFFICER
        JOIN INVESTIGATION ON INVESTIGATION_OFFICER.investigation_id = INVESTIGATION.investigation_id
        JOIN FIR ON INVESTIGATION.fir_id = FIR.fir_id
        WHERE INVESTIGATION_OFFICER.officer_id = %s
        """
        cursor.execute(read_investigation_officer_affiliation_query, (officer_id,))
        investigation_officer_affiliation = cursor.fetchall()
        if not investigation_officer_affiliation:
            raise HTTPException(status_code=404, detail="Officer affiliation not found")
        return investigation_officer_affiliation
    except Exception as err:
        return {"message": f"Error: {err}"}
    
@router.post("/investigation_officers/")
def create_investigation_officer(investigation_officer: InvestigationOfficer):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_investigation_officer_query = """
        INSERT INTO Investigation_Officer (officer_id, investigation_id)
        VALUES (%s, %s)
        """
        cursor.execute(
            create_investigation_officer_query,
            (investigation_officer.officer_id, investigation_officer.investigation_id),
        )
        conn.commit()
        return {"message": "Investigation Officer created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()


@router.get("/investigation_officers/")
def read_investigation_officers():
    conn = connect_to_db()
    cursor = conn.cursor()
    read_investigation_officers_query = "SELECT * FROM Investigation_Officer"
    cursor.execute(read_investigation_officers_query)
    investigation_officers = cursor.fetchall()
    cursor.close()
    conn.close()
    return investigation_officers


@router.get("/investigation_officers/{officer_id}/{investigation_id}")
def read_investigation_officer(officer_id: int, investigation_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    read_investigation_officer_query = "SELECT * FROM Investigation_Officer WHERE officer_id = %s AND investigation_id = %s"
    cursor.execute(read_investigation_officer_query, (officer_id, investigation_id))
    investigation_officer = cursor.fetchone()
    cursor.close()
    conn.close()
    if investigation_officer:
        return investigation_officer
    else:
        raise HTTPException(status_code=404, detail="Investigation Officer not found")


@router.delete("/investigation_officers/{officer_id}/{investigation_id}")
def delete_investigation_officer(officer_id: int, investigation_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_investigation_officer_query = "DELETE FROM Investigation_Officer WHERE officer_id = %s AND investigation_id = %s"
    cursor.execute(delete_investigation_officer_query, (officer_id, investigation_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Investigation Officer deleted successfully"}
