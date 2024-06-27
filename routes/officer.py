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


class Officer(BaseModel):
    role_id: int
    first_name: str
    last_name: str
    post: str
    mobile_no: str
    address: str
    username: str
    password: str
    station_id: int


@router.post("/officers/")
def create_officer(officer: Officer):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_officer_query = """
        INSERT INTO POLICE_OFFICER (role_id, first_name, last_name, post, mobile_no, address, username, password, station_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(create_officer_query, (
            officer.role_id, officer.first_name, officer.last_name, officer.post,
            officer.mobile_no, officer.address, officer.username, officer.password, officer.station_id
        ))
        conn.commit()
        return {"message": "Officer created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()

@router.get("/officers/")
def read_officers():
    conn = connect_to_db()
    cursor = conn.cursor()
    read_officers_query = "SELECT * FROM POLICE_OFFICER"
    cursor.execute(read_officers_query)
    officers = cursor.fetchall()
    cursor.close()
    conn.close()
    return officers

@router.get("/officers/{officer_id}")
def read_officer(officer_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    read_officer_query = "SELECT * FROM POLICE_OFFICER WHERE officer_id = %s"
    cursor.execute(read_officer_query, (officer_id,))
    officer = cursor.fetchone()
    cursor.close()
    conn.close()
    if officer:
        return officer
    else:
        raise HTTPException(status_code=404, detail="Officer not found")

@router.put("/officers/{officer_id}")
def update_officer(officer_id: int, officer: Officer):
    conn = connect_to_db()
    cursor = conn.cursor()
    update_officer_query = """
    UPDATE POLICE_OFFICER
    SET role_id = %s, first_name = %s, last_name = %s, post = %s, mobile_no = %s, address = %s, username = %s, password = %s, station_id = %s
    WHERE officer_id = %s
    """
    cursor.execute(update_officer_query, (
        officer.role_id, officer.first_name, officer.last_name, officer.post,
        officer.mobile_no, officer.address, officer.username, officer.password, officer.station_id, officer_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Officer updated successfully"}

@router.delete("/officers/{officer_id}")
def delete_officer(officer_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_officer_query = "DELETE FROM POLICE_OFFICER WHERE officer_id = %s"
    cursor.execute(delete_officer_query, (officer_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Officer deleted successfully"}