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


class PoliceStation(BaseModel):
    station_name: str
    location: str
    username: str
    password: str


@router.get("/stations/")
def read_stations():
    conn = connect_to_db()
    cursor = conn.cursor()
    read_stations_query = "SELECT * FROM POLICE_STATION"
    cursor.execute(read_stations_query)
    stations = cursor.fetchall()
    cursor.close()
    conn.close()
    return stations


@router.post("/stations/")
def create_station(station: PoliceStation):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_station_query = """
        INSERT INTO POLICE_STATION (station_name, location, username, password)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            create_station_query,
            (
                station.station_name,
                station.location,
                station.username,
                station.password,
            ),
        )
        conn.commit()
        return {"message": "Police station created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()


@router.put("/stations/{station_id}")
def update_station(station_id: int, station: PoliceStation):
    conn = connect_to_db()
    cursor = conn.cursor()
    update_station_query = """
    UPDATE POLICE_STATION
    SET station_name = %s, location = %s, username = %s, password = %s
    WHERE station_id = %s
    """
    cursor.execute(
        update_station_query,
        (
            station.station_name,
            station.location,
            station.username,
            station.password,
            station_id,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Police station updated successfully"}


@router.delete("/stations/{station_id}")
def delete_station(station_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_station_query = "DELETE FROM POLICE_STATION WHERE station_id = %s"
    cursor.execute(delete_station_query, (station_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Police station deleted successfully"}
