from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Database connection details
config = {
    'user': 'root',
    'password': 'hari2430',
    'host': 'localhost',
    'database': 'crime'
}

def connect_to_db():
    return mysql.connector.connect(**config)

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

class Role(BaseModel):
    role_name: str
    permission: str

class PoliceStation(BaseModel):
    station_name: str
    location: str
    username: str
    password: str

@app.post("/stations/")
def create_station(station: PoliceStation):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_station_query = """
        INSERT INTO POLICE_STATION (station_name, location, username, password)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(create_station_query, (station.station_name, station.location, station.username, station.password))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Police station created successfully"}

    except mysql.connector.Error as err:
        conn.rollback()  # Rollback any changes if an error occurs
        return {"message": f"Error: {err}"}

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.post("/roles/")
def create_role(role: Role):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_role_query = """
        INSERT INTO ROLE (role_name, permission)
        VALUES (%s, %s)
        """
        cursor.execute(create_role_query, (role.role_name, role.permission))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Role created successfully"}

    except mysql.connector.Error as err:
        conn.rollback()  # Rollback any changes if an error occurs
        return {"message": f"Error: {err}"}

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@app.post("/officers/")
def create_officer(officer: Officer):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # # Check if role_id exists in ROLE table
        # check_role_query = "SELECT role_id FROM ROLE WHERE role_id = %s"
        # cursor.execute(check_role_query, (officer.role_id,))
        # result = cursor.fetchone()

        # if not result:
        #     raise HTTPException(status_code=404, detail=f"Role with role_id {officer.role_id} does not exist")

        create_officer_query = """
        INSERT INTO POLICE_OFFICER (role_id, first_name, last_name, post, mobile_no, address, username, password, station_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(create_officer_query, (
            officer.role_id, officer.first_name, officer.last_name, officer.post,
            officer.mobile_no, officer.address, officer.username, officer.password, officer.station_id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Officer created successfully"}

    except mysql.connector.Error as err:
        conn.rollback()  # Rollback any changes if an error occurs
        return {"message": f"Error: {err}"}

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



@app.get("/officers/{officer_id}")
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

@app.put("/officers/{officer_id}")
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

@app.delete("/officers/{officer_id}")
def delete_officer(officer_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_officer_query = "DELETE FROM POLICE_OFFICER WHERE officer_id = %s"
    cursor.execute(delete_officer_query, (officer_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Officer deleted successfully"}

# Add similar endpoints for other tables...

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
