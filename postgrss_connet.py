from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from routes import role_router, station_router, officer_router, fir_router, crime_router

app = FastAPI()
app.include_router(role_router)
app.include_router(station_router)
app.include_router(officer_router)
app.include_router(fir_router)
app.include_router(crime_router)
# Database connection details
config = {
    'dbname': 'lorem',
    'user': 'postgres',
    'password': 'hari2430',
    'host': 'localhost',
    'port': 5432
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

class Role(BaseModel):
    role_name: str
    permission: str

class PoliceStation(BaseModel):
    station_name: str
    location: str
    username: str
    password: str

class FIR(BaseModel):
    police_station_id: int
    officer_id: int
    title: str
    act: str
    complaint_name: str
    date_added: str
    details: str

class Crime(BaseModel):
    fir_id: int
    type_of_crime: str
    details: str
    investigation_id: int

class Investigation(BaseModel):
    evidence: str
    suspects: str
    fir_id: int

class Criminal(BaseModel):
    name: str
    address: str
    gender: str
    height: str
    date_arrest: str
    date_birth: str

class InvestigationOfficer(BaseModel):
    officer_id: int
    investigation_id: int

class CrimesInvolved(BaseModel):
    crime_id: int
    criminal_id: int

class PartOf(BaseModel):
    investigation_id: int
    criminal_id: int

# @app.get("/stations/")
# def read_stations():
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     read_stations_query = "SELECT * FROM POLICE_STATION"
#     cursor.execute(read_stations_query)
#     stations = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return stations

# @app.post("/stations/")
# def create_station(station: PoliceStation):
#     conn = connect_to_db()
#     cursor = conn.cursor()

#     try:
#         create_station_query = """
#         INSERT INTO POLICE_STATION (station_name, location, username, password)
#         VALUES (%s, %s, %s, %s)
#         """
#         cursor.execute(create_station_query, (station.station_name, station.location, station.username, station.password))
#         conn.commit()
#         return {"message": "Police station created successfully"}

#     except Exception as err:
#         conn.rollback()
#         return {"message": f"Error: {err}"}

#     finally:
#         cursor.close()
#         conn.close()

# @app.put("/stations/{station_id}")
# def update_station(station_id: int, station: PoliceStation):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     update_station_query = """
#     UPDATE POLICE_STATION
#     SET station_name = %s, location = %s, username = %s, password = %s
#     WHERE station_id = %s
#     """
#     cursor.execute(update_station_query, (
#         station.station_name, station.location, station.username, station.password, station_id
#     ))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"message": "Police station updated successfully"}

# @app.delete("/stations/{station_id}")
# def delete_station(station_id: int):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     delete_station_query = "DELETE FROM POLICE_STATION WHERE station_id = %s"
#     cursor.execute(delete_station_query, (station_id,))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"message": "Police station deleted successfully"}

# @app.get("/roles/")
# def read_roles():
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     read_roles_query = "SELECT * FROM ROLE"
#     cursor.execute(read_roles_query)
#     roles = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return roles

# @app.post("/roles/")
# def create_role(role: Role):
#     conn = connect_to_db()
#     cursor = conn.cursor()

#     try:
#         create_role_query = """
#         INSERT INTO ROLE (role_name, permission)
#         VALUES (%s, %s)
#         """
#         cursor.execute(create_role_query, (role.role_name, role.permission))
#         conn.commit()
#         return {"message": "Role created successfully"}

#     except Exception as err:
#         conn.rollback()
#         return {"message": f"Error: {err}"}

#     finally:
#         cursor.close()
#         conn.close()

# @app.put("/roles/{role_id}")
# def update_role(role_id: int, role: Role):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     update_role_query = """
#     UPDATE ROLE
#     SET role_name = %s, permission = %s
#     WHERE role_id = %s
#     """
#     cursor.execute(update_role_query, (
#         role.role_name, role.permission, role_id
#     ))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"message": "Role updated successfully"}

# @app.delete("/roles/{role_id}")
# def delete_role(role_id: int):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     delete_role_query = "DELETE FROM ROLE WHERE role_id = %s"
#     cursor.execute(delete_role_query, (role_id,))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"message": "Role deleted successfully"}

# @app.post("/officers/")
# def create_officer(officer: Officer):
#     conn = connect_to_db()
#     cursor = conn.cursor()

#     try:
#         create_officer_query = """
#         INSERT INTO POLICE_OFFICER (role_id, first_name, last_name, post, mobile_no, address, username, password, station_id)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         cursor.execute(create_officer_query, (
#             officer.role_id, officer.first_name, officer.last_name, officer.post,
#             officer.mobile_no, officer.address, officer.username, officer.password, officer.station_id
#         ))
#         conn.commit()
#         return {"message": "Officer created successfully"}

#     except Exception as err:
#         conn.rollback()
#         return {"message": f"Error: {err}"}

#     finally:
#         cursor.close()
#         conn.close()

# @app.get("/officers/")
# def read_officers():
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     read_officers_query = "SELECT * FROM POLICE_OFFICER"
#     cursor.execute(read_officers_query)
#     officers = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return officers

# @app.get("/officers/{officer_id}")
# def read_officer(officer_id: int):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     read_officer_query = "SELECT * FROM POLICE_OFFICER WHERE officer_id = %s"
#     cursor.execute(read_officer_query, (officer_id,))
#     officer = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     if officer:
#         return officer
#     else:
#         raise HTTPException(status_code=404, detail="Officer not found")

# @app.put("/officers/{officer_id}")
# def update_officer(officer_id: int, officer: Officer):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     update_officer_query = """
#     UPDATE POLICE_OFFICER
#     SET role_id = %s, first_name = %s, last_name = %s, post = %s, mobile_no = %s, address = %s, username = %s, password = %s, station_id = %s
#     WHERE officer_id = %s
#     """
#     cursor.execute(update_officer_query, (
#         officer.role_id, officer.first_name, officer.last_name, officer.post,
#         officer.mobile_no, officer.address, officer.username, officer.password, officer.station_id, officer_id
#     ))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"message": "Officer updated successfully"}

# @app.delete("/officers/{officer_id}")
# def delete_officer(officer_id: int):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     delete_officer_query = "DELETE FROM POLICE_OFFICER WHERE officer_id = %s"
#     cursor.execute(delete_officer_query, (officer_id,))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"message": "Officer deleted successfully"}

# @app.post("/firs/")
# def create_fir(fir: FIR):
#     conn = connect_to_db()
#     cursor = conn.cursor()

#     try:
#         create_fir_query = """
#         INSERT INTO FIR (police_station_id, officer_id, title, act, complaint_name, date_added, details)
#         VALUES (%s, %s, %s, %s, %s, %s, %s)
#         """
#         cursor.execute(create_fir_query, (
#             fir.police_station_id, fir.officer_id, fir.title, fir.act, fir.complaint_name,
#             fir.date_added, fir.details
#         ))
#         conn.commit()
#         return {"message": "FIR created successfully"}

#     except Exception as err:
#         conn.rollback()
#         return {"message": f"Error: {err}"}

#     finally:
#         cursor.close()
#         conn.close()

# @app.get("/firs/")
# def read_firs():
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     read_firs_query = "SELECT * FROM FIR"
#     cursor.execute(read_firs_query)
#     firs = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return firs

# @app.get("/firs/{fir_id}")
# def read_fir(fir_id: int):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     read_fir_query = "SELECT * FROM FIR WHERE fir_id = %s"
#     cursor.execute(read_fir_query, (fir_id,))
#     fir = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     if fir:
#         return fir
#     else:
#         raise HTTPException(status_code=404, detail="FIR not found")

# @app.put("/firs/{fir_id}")
# def update_fir(fir_id: int, fir: FIR):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     update_fir_query = """
#     UPDATE FIR
#     SET police_station_id = %s, officer_id = %s, title = %s, act = %s, complaint_name = %s, date_added = %s, details = %s
#     WHERE fir_id = %s
#     """
#     cursor.execute(update_fir_query, (
#         fir.police_station_id, fir.officer_id, fir.title, fir.act, fir.complaint_name,
#         fir.date_added, fir.details, fir_id
#     ))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"message": "FIR updated successfully"}

# @app.delete("/firs/{fir_id}")
# def delete_fir(fir_id: int):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     delete_fir_query = "DELETE FROM FIR WHERE fir_id = %s"
#     cursor.execute(delete_fir_query, (fir_id,))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"message": "FIR deleted successfully"}

# @app.post("/crimes/")
# def create_crime(crime: Crime):
#     conn = connect_to_db()
#     cursor = conn.cursor()

#     try:
#         create_crime_query = """
#         INSERT INTO CRIME (fir_id, type_of_crime, details, investigation_id)
#         VALUES (%s, %s, %s, %s)
#         """
#         cursor.execute(create_crime_query, (
#             crime.fir_id, crime.type_of_crime, crime.details, crime.investigation_id
#         ))
#         conn.commit()
#         return {"message": "Crime created successfully"}

#     except Exception as err:
#         conn.rollback()
#         return {"message": f"Error: {err}"}

#     finally:
#         cursor.close()
#         conn.close()

# @app.get("/crimes/")
# def read_crimes():
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     read_crimes_query = "SELECT * FROM CRIME"
#     cursor.execute(read_crimes_query)
#     crimes = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return crimes

# @app.get("/crimes/{crime_id}")
# def read_crime(crime_id: int):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     read_crime_query = "SELECT * FROM CRIME WHERE crime_id = %s"
#     cursor.execute(read_crime_query, (crime_id,))
#     crime = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     if crime:
#         return crime
#     else:
#         raise HTTPException(status_code=404, detail="Crime not found")

# @app.put("/crimes/{crime_id}")
# def update_crime(crime_id: int, crime: Crime):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     update_crime_query = """
#     UPDATE CRIME
#     SET fir_id = %s, type_of_crime = %s, details = %s, investigation_id = %s
#     WHERE crime_id = %s
#     """
#     cursor.execute(update_crime_query, (
#         crime.fir_id, crime.type_of_crime, crime.details, crime.investigation_id, crime_id
#     ))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"message": "Crime updated successfully"}

# @app.delete("/crimes/{crime_id}")
# def delete_crime(crime_id: int):
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     delete_crime_query = "DELETE FROM CRIME WHERE crime_id = %s"
#     cursor.execute(delete_crime_query, (crime_id,))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"message": "Crime deleted successfully"}

@app.post("/investigations/")
def create_investigation(investigation: Investigation):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_investigation_query = """
        INSERT INTO INVESTIGATION (evidence, suspects, fir_id)
        VALUES (%s, %s, %s)
        """
        cursor.execute(create_investigation_query, (
            investigation.evidence, investigation.suspects, investigation.fir_id
        ))
        conn.commit()
        return {"message": "Investigation created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()

@app.get("/investigations/")
def read_investigations():
    conn = connect_to_db()
    cursor = conn.cursor()
    read_investigations_query = "SELECT * FROM INVESTIGATION"
    cursor.execute(read_investigations_query)
    investigations = cursor.fetchall()
    cursor.close()
    conn.close()
    return investigations

@app.get("/investigations/{investigation_id}")
def read_investigation(investigation_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    read_investigation_query = "SELECT * FROM INVESTIGATION WHERE investigation_id = %s"
    cursor.execute(read_investigation_query, (investigation_id,))
    investigation = cursor.fetchone()
    cursor.close()
    conn.close()
    if investigation:
        return investigation
    else:
        raise HTTPException(status_code=404, detail="Investigation not found")

@app.put("/investigations/{investigation_id}")
def update_investigation(investigation_id: int, investigation: Investigation):
    conn = connect_to_db()
    cursor = conn.cursor()
    update_investigation_query = """
    UPDATE INVESTIGATION
    SET evidence = %s, suspects = %s, fir_id = %s
    WHERE investigation_id = %s
    """
    cursor.execute(update_investigation_query, (
        investigation.evidence, investigation.suspects, investigation.fir_id, investigation_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Investigation updated successfully"}

@app.delete("/investigations/{investigation_id}")
def delete_investigation(investigation_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_investigation_query = "DELETE FROM INVESTIGATION WHERE investigation_id = %s"
    cursor.execute(delete_investigation_query, (investigation_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Investigation deleted successfully"}

@app.post("/criminals/")
def create_criminal(criminal: Criminal):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_criminal_query = """
        INSERT INTO CRIMINAL (name, address, gender, height, date_arrest, date_birth)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(create_criminal_query, (
            criminal.name, criminal.address, criminal.gender, criminal.height,
            criminal.date_arrest, criminal.date_birth
        ))
        conn.commit()
        return {"message": "Criminal created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()

@app.get("/criminals/")
def read_criminals():
    conn = connect_to_db()
    cursor = conn.cursor()
    read_criminals_query = "SELECT * FROM CRIMINAL"
    cursor.execute(read_criminals_query)
    criminals = cursor.fetchall()
    cursor.close()
    conn.close()
    return criminals

@app.get("/criminals/{criminal_id}")
def read_criminal(criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    read_criminal_query = "SELECT * FROM CRIMINAL WHERE criminal_id = %s"
    cursor.execute(read_criminal_query, (criminal_id,))
    criminal = cursor.fetchone()
    cursor.close()
    conn.close()
    if criminal:
        return criminal
    else:
        raise HTTPException(status_code=404, detail="Criminal not found")

@app.put("/criminals/{criminal_id}")
def update_criminal(criminal_id: int, criminal: Criminal):
    conn = connect_to_db()
    cursor = conn.cursor()
    update_criminal_query = """
    UPDATE CRIMINAL
    SET name = %s, address = %s, gender = %s, height = %s, date_arrest = %s, date_birth = %s
    WHERE criminal_id = %s
    """
    cursor.execute(update_criminal_query, (
        criminal.name, criminal.address, criminal.gender, criminal.height,
        criminal.date_arrest, criminal.date_birth, criminal_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Criminal updated successfully"}

@app.delete("/criminals/{criminal_id}")
def delete_criminal(criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_criminal_query = "DELETE FROM CRIMINAL WHERE criminal_id = %s"
    cursor.execute(delete_criminal_query, (criminal_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Criminal deleted successfully"}

@app.post("/investigation_officers/")
def create_investigation_officer(investigation_officer: InvestigationOfficer):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_investigation_officer_query = """
        INSERT INTO Investigation_Officer (officer_id, investigation_id)
        VALUES (%s, %s)
        """
        cursor.execute(create_investigation_officer_query, (
            investigation_officer.officer_id, investigation_officer.investigation_id
        ))
        conn.commit()
        return {"message": "Investigation Officer created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()

@app.get("/investigation_officers/")
def read_investigation_officers():
    conn = connect_to_db()
    cursor = conn.cursor()
    read_investigation_officers_query = "SELECT * FROM Investigation_Officer"
    cursor.execute(read_investigation_officers_query)
    investigation_officers = cursor.fetchall()
    cursor.close()
    conn.close()
    return investigation_officers

@app.get("/investigation_officers/{officer_id}/{investigation_id}")
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

@app.delete("/investigation_officers/{officer_id}/{investigation_id}")
def delete_investigation_officer(officer_id: int, investigation_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_investigation_officer_query = "DELETE FROM Investigation_Officer WHERE officer_id = %s AND investigation_id = %s"
    cursor.execute(delete_investigation_officer_query, (officer_id, investigation_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Investigation Officer deleted successfully"}

@app.post("/crimes_involved/")
def create_crimes_involved(crimes_involved: CrimesInvolved):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_crimes_involved_query = """
        INSERT INTO Crimes_Involved (crime_id, criminal_id)
        VALUES (%s, %s)
        """
        cursor.execute(create_crimes_involved_query, (
            crimes_involved.crime_id, crimes_involved.criminal_id
        ))
        conn.commit()
        return {"message": "Crimes Involved created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()

@app.get("/crimes_involved/")
def read_crimes_involved():
    conn = connect_to_db()
    cursor = conn.cursor()
    read_crimes_involved_query = "SELECT * FROM Crimes_Involved"
    cursor.execute(read_crimes_involved_query)
    crimes_involved = cursor.fetchall()
    cursor.close()
    conn.close()
    return crimes_involved

@app.get("/crimes_involved/{crime_id}/{criminal_id}")
def read_crimes_involved(crime_id: int, criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    read_crimes_involved_query = "SELECT * FROM Crimes_Involved WHERE crime_id = %s AND criminal_id = %s"
    cursor.execute(read_crimes_involved_query, (crime_id, criminal_id))
    crimes_involved = cursor.fetchone()
    cursor.close()
    conn.close()
    if crimes_involved:
        return crimes_involved
    else:
        raise HTTPException(status_code=404, detail="Crimes Involved not found")

@app.delete("/crimes_involved/{crime_id}/{criminal_id}")
def delete_crimes_involved(crime_id: int, criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_crimes_involved_query = "DELETE FROM Crimes_Involved WHERE crime_id = %s AND criminal_id = %s"
    cursor.execute(delete_crimes_involved_query, (crime_id, criminal_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Crimes Involved deleted successfully"}

@app.post("/part_of/")
def create_part_of(part_of: PartOf):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        create_part_of_query = """
        INSERT INTO Part_Of (investigation_id, criminal_id)
        VALUES (%s, %s)
        """
        cursor.execute(create_part_of_query, (
            part_of.investigation_id, part_of.criminal_id
        ))
        conn.commit()
        return {"message": "Part Of created successfully"}

    except Exception as err:
        conn.rollback()
        return {"message": f"Error: {err}"}

    finally:
        cursor.close()
        conn.close()

@app.get("/part_of/")
def read_part_of():
    conn = connect_to_db()
    cursor = conn.cursor()
    read_part_of_query = "SELECT * FROM Part_Of"
    cursor.execute(read_part_of_query)
    part_of = cursor.fetchall()
    cursor.close()
    conn.close()
    return part_of

@app.get("/part_of/{investigation_id}/{criminal_id}")
def read_part_of(investigation_id: int, criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    read_part_of_query = "SELECT * FROM Part_Of WHERE investigation_id = %s AND criminal_id = %s"
    cursor.execute(read_part_of_query, (investigation_id, criminal_id))
    part_of = cursor.fetchone()
    cursor.close()
    conn.close()
    if part_of:
        return part_of
    else:
        raise HTTPException(status_code=404, detail="Part Of not found")

@app.delete("/part_of/{investigation_id}/{criminal_id}")
def delete_part_of(investigation_id: int, criminal_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_part_of_query = "DELETE FROM Part_Of WHERE investigation_id = %s AND criminal_id = %s"
    cursor.execute(delete_part_of_query, (investigation_id, criminal_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Part Of deleted successfully"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
