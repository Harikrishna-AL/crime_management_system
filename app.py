import streamlit as st
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time

API_URL = "http://localhost:8000"  # URL of your FastAPI app

st.title("Police Management System")


# Function to create a police station
def create_station(station_name, location, username, password):
    response = requests.post(
        f"{API_URL}/stations/",
        json={
            "station_name": station_name,
            "location": location,
            "username": username,
            "password": password,
        },
    )
    return response.json()

# Function to edit a police station
def update_station(station_id, station_name, location, username, password):
    response = requests.put(
        f"{API_URL}/stations/{station_id}",
        json={
            "station_name": station_name,
            "location": location,
            "username": username,
            "password": password,
        },
    )
    return response.json()

# Function to delete a police station
def delete_station(station_id):
    response = requests.delete(f"{API_URL}/stations/{station_id}")
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(response.content)
        return {"message": "Failed to decode JSON response", "response_text": response.text}

# Function to create a role
def create_role(role_name, permission):
    response = requests.post(
        f"{API_URL}/roles/", json={"role_name": role_name, "permission": permission}
    )
    return response.json()


# Function to create an officer
def create_officer(
    role_id,
    first_name,
    last_name,
    post,
    mobile_no,
    address,
    username,
    password,
    station_id,
):
    response = requests.post(
        f"{API_URL}/officers/",
        json={
            "role_id": role_id,
            "first_name": first_name,
            "last_name": last_name,
            "post": post,
            "mobile_no": mobile_no,
            "address": address,
            "username": username,
            "password": password,
            "station_id": station_id,
        },
    )
    return response.json()


# Function to update an officer


def update_officer(
    officer_id,
    role_id,
    first_name,
    last_name,
    post,
    mobile_no,
    address,
    username,
    password,
    station_id,
):
    response = requests.put(
        f"{API_URL}/officers/{officer_id}",
        json={
            "officer_id": officer_id,
            "role_id": role_id,
            "first_name": first_name,
            "last_name": last_name,
            "post": post,
            "mobile_no": mobile_no,
            "address": address,
            "username": username,
            "password": password,
            "station_id": station_id,
        },
    )
    return response.json()

def delete_officer(officer_id):
    response = requests.delete(f"{API_URL}/officers/{officer_id}")
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(response.content)
        return {"message": "Failed to decode JSON response", "response_text": response.text}
    
# Get officer affiliations

def get_officer_affiliations(officer_id):
    response = requests.get(f"{API_URL}/officerAffiliation/{officer_id}")
    return response.json()
    
# FIRs

# Function to create an investigation
def create_investigation(evidence, suspects, fir_id):
    response = requests.post(
        f"{API_URL}/investigations/",
        json={
            "evidence": evidence,
            "suspects": suspects,
            "fir_id": fir_id,
        },
    )
    return response.json()

# Function to read all investigations
def read_investigations():
    response = requests.get(f"{API_URL}/investigations/")
    return response.json()

# Function to read a specific investigation
def read_investigation(investigation_id):
    response = requests.get(f"{API_URL}/investigations/{investigation_id}")
    return response.json()

# Function to update an investigation
def update_investigation(investigation_id, evidence, suspects, fir_id):
    response = requests.put(
        f"{API_URL}/investigations/{investigation_id}",
        json={
            "evidence": evidence,
            "suspects": suspects,
            "fir_id": fir_id,
        },
    )
    return response.json()

# Function to delete an investigation
def delete_investigation(investigation_id):
    response = requests.delete(f"{API_URL}/investigations/{investigation_id}")
    return response.json()

# Function to create a crime
def create_crime(fir_id, type_of_crime, details, investigation_id):
    response = requests.post(
        f"{API_URL}/crimes/",
        json={
            "fir_id": fir_id,
            "type_of_crime": type_of_crime,
            "details": details,
            "investigation_id": investigation_id,
        },
    )
    return response.json()

# Function to read all crimes
def read_crimes():
    response = requests.get(f"{API_URL}/crimes/")
    return response.json()

# Function to read a specific crime
def read_crime(crime_id):
    response = requests.get(f"{API_URL}/crimes/{crime_id}")
    return response.json()

# Function to update a crime
def update_crime(crime_id, fir_id, type_of_crime, details, investigation_id):
    response = requests.put(
        f"{API_URL}/crimes/{crime_id}",
        json={
            "fir_id": fir_id,
            "type_of_crime": type_of_crime,
            "details": details,
            "investigation_id": investigation_id,
        },
    )
    return response.json()

# Function to delete a crime
def delete_crime(crime_id):
    response = requests.delete(f"{API_URL}/crimes/{crime_id}")
    return response.json()


# Function to get data from an endpoint
def get_data(endpoint):
    response = requests.get(f"{API_URL}/{endpoint}/")
    return response.json()

# Function to create an FIR
def create_fir(police_station_id, officer_id, title, act, complaint_name, date_added, details, contact_number):
    response = requests.post(
        f"{API_URL}/firs/",
        json={
            "police_station_id": police_station_id,
            "officer_id": officer_id,
            "title": title,
            "act": act,
            "complaint_name": complaint_name,
            "date_added": date_added,
            "details": details,
            "contact_number": contact_number
        },
    )
    return response.json()


# Function to update an FIR
def update_fir(fir_id, police_station_id, officer_id, title, act, complaint_name, date_added, details, contact_number):
    response = requests.put(
        f"{API_URL}/firs/{fir_id}",
        json={
            "police_station_id": police_station_id,
            "officer_id": officer_id,
            "title": title,
            "act": act,
            "complaint_name": complaint_name,
            "date_added": date_added,
            "details": details,
            "contact_number": contact_number
        },
    )
    return response.json()

# Function to delete an FIR
def delete_fir(fir_id):
    response = requests.delete(f"{API_URL}/firs/{fir_id}")
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(response.content)
        return {"message": "Failed to decode JSON response", "response_text": response.text}

# Criminal Operations

# Function to create a criminal
def create_criminal(first_name, last_name, address, city, gender, height, date_arrest, date_release, date_birth, occupation):
    response = requests.post(
        f"{API_URL}/criminals/",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "city": city,
            "gender": gender,
            "height": height,
            "date_arrest": date_arrest,
            "date_release": date_release,
            "date_birth": date_birth,
            "occupation": occupation,
        },
    )
    return response.json()

# Function to read all criminals
def read_criminals():
    response = requests.get(f"{API_URL}/criminals/")
    return response.json()

# Function to read a specific criminal
def read_criminal(criminal_id):
    response = requests.get(f"{API_URL}/criminals/{criminal_id}")
    return response.json()

# Function to update a criminal
def update_criminal(criminal_id, first_name, last_name, address, city, gender, height, date_arrest, date_release, date_birth, occupation):
    response = requests.put(
        f"{API_URL}/criminals/{criminal_id}",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "city": city,
            "gender": gender,
            "height": height,
            "date_arrest": date_arrest,
            "date_release": date_release,
            "date_birth": date_birth,
            "occupation": occupation,
        },
    )
    return response.json()

# Function to get criminal record

def get_criminal_record(first_name, last_name):
    # pass first name and last name as query parameters
    response = requests.get(f"{API_URL}/getCriminalRecords", params={"first_name": first_name, "last_name": last_name})
    return response.json()

# Function to delete a criminal
def delete_criminal(criminal_id):
    response = requests.delete(f"{API_URL}/criminals/{criminal_id}")
    return response.json()

# Function to create an investigation officer
def create_investigation_officer(officer_id, investigation_id):
    response = requests.post(
        f"{API_URL}/investigation_officers/",
        json={
            "officer_id": officer_id,
            "investigation_id": investigation_id,
        },
    )
    return response.json()

# Function to read all investigation officers
def read_investigation_officers():
    response = requests.get(f"{API_URL}/investigation_officers/")
    return response.json()

# Function to read a specific investigation officer
def read_investigation_officer(officer_id, investigation_id):
    response = requests.get(f"{API_URL}/investigation_officers/{officer_id}/{investigation_id}")
    return response.json()

# Function to delete an investigation officer
def delete_investigation_officer(officer_id, investigation_id):
    response = requests.delete(f"{API_URL}/investigation_officers/{officer_id}/{investigation_id}")
    return response.json()


# Crimes involved

# Function to create crimes involved
def create_crimes_involved(crime_id, criminal_id):
    response = requests.post(
        f"{API_URL}/crimes_involved/",
        json={
            "crime_id": crime_id,
            "criminal_id": criminal_id,
        },
    )
    return response.json()

# Function to read all crimes involved
def read_crimes_involved():
    response = requests.get(f"{API_URL}/crimes_involved/")
    return response.json()

# Function to read a specific crimes involved
def read_specific_crimes_involved(crime_id, criminal_id):
    response = requests.get(f"{API_URL}/crimes_involved/{crime_id}/{criminal_id}")
    return response.json()

# Function to delete crimes involved
def delete_crimes_involved(crime_id, criminal_id):
    response = requests.delete(f"{API_URL}/crimes_involved/{crime_id}/{criminal_id}")
    return response.json()

# PART OF

# Function to create part of
def create_part_of(investigation_id, criminal_id):
    response = requests.post(
        f"{API_URL}/part_of/",
        json={
            "investigation_id": investigation_id,
            "criminal_id": criminal_id,
        },
    )
    return response.json()

# Function to read all part of entries
def read_part_of():
    response = requests.get(f"{API_URL}/part_of/")
    return response.json()

# Function to read a specific part of entry
def read_specific_part_of(investigation_id, criminal_id):
    response = requests.get(f"{API_URL}/part_of/{investigation_id}/{criminal_id}")
    return response.json()

# Function to delete part of entry
def delete_part_of(investigation_id, criminal_id):
    response = requests.delete(f"{API_URL}/part_of/{investigation_id}/{criminal_id}")
    return response.json()

# Admin tab
def admin_tab():
    st.header("Admin Operations")

    st.subheader("Create Police Station")
    station_name = st.text_input("Station Name", key="admin_station_name")
    location = st.text_input("Location", key="admin_location")
    username = st.text_input("Station Username", key="admin_station_username")
    password = st.text_input(
        "Station Password", type="password", key="admin_station_password"
    )
    if st.button("Create Station", key="admin_create_station_button"):
        result = create_station(station_name, location, username, password)
        st.write(result)

    
    st.subheader("View Police Stations")
    if st.button("View Police Stations", key="admin_view_stations_button"):
        stations = get_data("stations")
        st.table(stations)
    

    st.subheader("Update Police Station")
    station_id = st.number_input("Station ID to Update", min_value=1, key="admin_station_id_update")
    update_station_name = st.text_input("New Station Name", key="admin_update_station_name")
    update_location = st.text_input("New Location", key="admin_update_location")
    update_username = st.text_input("New Station Username", key="admin_update_station_username")
    update_password = st.text_input(
        "New Station Password", type="password", key="admin_update_station_password"
    )
    if st.button("Update Station", key="admin_update_station_button"):
        result = update_station(station_id, update_station_name, update_location, update_username, update_password)
        st.write(result)

    
    st.subheader("Delete Police Station")
    station_id_delete = st.number_input("Station ID to Delete", min_value=1, key="admin_station_id_delete")
    if st.button("Delete Station", key="admin_delete_station_button"):
        result = delete_station(station_id_delete)
        st.write(result)
    

    # st.subheader("Create Role")
    # role_name = st.text_input("Role Name", key="admin_role_name")
    # permission = st.text_input("Permission", key="admin_permission")
    # if st.button("Create Role", key="admin_create_role_button"):
    #     result = create_role(role_name, permission)
    #     st.write(result)

    st.subheader("Create Officer")
    role_id = st.number_input("Role ID", min_value=1, key="admin_role_id")
    first_name = st.text_input("First Name", key="admin_first_name")
    last_name = st.text_input("Last Name", key="admin_last_name")
    post = st.text_input("Post", key="admin_post")
    mobile_no = st.text_input("Mobile Number", key="admin_mobile_no")
    address = st.text_input("Address", key="admin_address")
    username = st.text_input("Officer Username", key="admin_officer_username")
    password = st.text_input(
        "Officer Password", type="password", key="admin_officer_password"
    )
    station_id = st.number_input("Station ID", min_value=1, key="admin_station_id")
    if st.button("Create Officer", key="admin_create_officer_button"):
        result = create_officer(
            role_id,
            first_name,
            last_name,
            post,
            mobile_no,
            address,
            username,
            password,
            station_id,
        )
        st.write(result)

    st.subheader("Read Data")
    if st.button("Get All Police Stations", key="admin_get_stations"):
        stations = get_data("stations")
        st.write(stations)

    st.subheader("Get Officer Data")
    if st.button("Get Officer Details", key="admin_get_officer_affiliations"):
        # take officer id in input
        officer_id = st.number_input("Officer ID", min_value=1, key="admin_officer_affiliations")
        officer_affiliations = get_officer_affiliations(officer_id)
        st.write(officer_affiliations)

    if st.button("Get All Roles", key="admin_get_roles"):
        roles = get_data("roles")
        st.write(roles)

    if st.button("Get All Officers", key="admin_get_officers"):
        officers = get_data("officers")
        st.write(officers)

    st.subheader("Update Officer")
    officer_id_update = st.number_input(
        "Officer ID to Update", min_value=1, key="admin_officer_id_update"
    )
    update_role_id = st.number_input(
        "New Role ID", min_value=1, key="admin_update_role_id"
    )
    update_first_name = st.text_input("New First Name", key="admin_update_first_name")
    update_last_name = st.text_input("New Last Name", key="admin_update_last_name")
    update_post = st.text_input("New Post", key="admin_update_post")
    update_mobile_no = st.text_input("New Mobile Number", key="admin_update_mobile_no")
    update_address = st.text_input("New Address", key="admin_update_address")
    update_username = st.text_input("New Username", key="admin_update_username")
    update_password = st.text_input(
        "New Password", type="password", key="admin_update_password"
    )
    update_station_id = st.number_input(
        "New Station ID", min_value=1, key="admin_update_station_id"
    )
    if st.button("Update Officer", key="admin_update_officer_button"):
        result = update_officer(
            officer_id_update,
            update_role_id,
            update_first_name,
            update_last_name,
            update_post,
            update_mobile_no,
            update_address,
            update_username,
            update_password,
            update_station_id,
        )
        st.write(result)

    st.subheader("Delete Officer")
    officer_id_delete = st.number_input(
        "Officer ID to Delete", min_value=1, key="admin_officer_id_delete"
    )
    if st.button("Delete Officer", key="admin_delete_officer_button"):
        result = delete_officer(officer_id_delete)
        st.write(result)
    
    st.subheader("FIR Operations")

    st.subheader("Create FIR")
    police_station_id = st.number_input("Police Station ID", min_value=1, key="admin_police_station_id")
    officer_id = st.number_input("Officer ID", min_value=1, key="admin_officer_id")
    title = st.text_input("Title", key="admin_title")
    act = st.text_input("Act", key="admin_act")
    complaint_name = st.text_input("Complaint Name", key="admin_complaint_name")
    date_added = st.text_input("Date Added (YYYY-MM-DD)", key="admin_date_added")
    details = st.text_area("Details", key="admin_details")
    contact_number = st.text_input("Contact Number", key="admin_contact_number")
    if st.button("Create FIR", key="admin_create_fir_button"):
        result = create_fir(police_station_id, officer_id, title, act, complaint_name, date_added, details, contact_number)
        st.write(result)

    st.subheader("Update FIR")
    fir_id_update = st.number_input("FIR ID to Update", min_value=1, key="admin_fir_id_update")
    update_police_station_id = st.number_input("New Police Station ID", min_value=1, key="admin_update_police_station_id")
    update_officer_id = st.number_input("New Officer ID", min_value=1, key="admin_update_officer_id")
    update_title = st.text_input("New Title", key="admin_update_title")
    update_act = st.text_input("New Act", key="admin_update_act")
    update_complaint_name = st.text_input("New Complaint Name", key="admin_update_complaint_name")
    update_date_added = st.text_input("New Date Added (YYYY-MM-DD)", key="admin_update_date_added")
    update_details = st.text_area("New Details", key="admin_update_details")
    update_contact_number = st.text_input("New Contact Number", key="admin_update_contact_number")
    if st.button("Update FIR", key="admin_update_fir_button"):
        result = update_fir(fir_id_update, update_police_station_id, update_officer_id, update_title, update_act, update_complaint_name, update_date_added, update_details, update_contact_number)
        st.write(result)

    st.subheader("Delete FIR")
    fir_id_delete = st.number_input("FIR ID to Delete", min_value=1, key="admin_fir_id_delete")
    if st.button("Delete FIR", key="admin_delete_fir_button"):
        result = delete_fir(fir_id_delete)
        st.write(result)

    st.subheader("Read FIRs")
    if st.button("Get All FIRs", key="admin_get_firs"):
        firs = get_data("firs")
        st.write(firs)
    
    st.title("Investigation Operations")

    # Create Investigation
    st.subheader("Create Investigation")
    evidence = st.text_input("Evidence")
    suspects = st.text_input("Suspects")
    fir_id = st.number_input("FIR ID", min_value=1)
    if st.button("Create Investigation"):
        result = create_investigation(evidence, suspects, fir_id)
        st.write(result)

    # Read Investigations
    st.subheader("Read Investigations")
    if st.button("Get All Investigations"):
        investigations = read_investigations()
        st.write(investigations)

    # Read Specific Investigation
    st.subheader("Read Specific Investigation")
    investigation_id_read = st.number_input("Investigation ID to Read", min_value=1, key="read_investigation_id")
    if st.button("Read Investigation"):
        investigation = read_investigation(investigation_id_read)
        st.write(investigation)

    # Update Investigation
    st.subheader("Update Investigation")
    investigation_id_update = st.number_input("Investigation ID to Update", min_value=1, key="update_investigation_id")
    update_evidence = st.text_input("New Evidence", key="update_evidence")
    update_suspects = st.text_input("New Suspects", key="update_suspects")
    update_fir_id = st.number_input("New FIR ID", min_value=1, key="update_fir_id")
    if st.button("Update Investigation"):
        result = update_investigation(investigation_id_update, update_evidence, update_suspects, update_fir_id)
        st.write(result)

    # Delete Investigation
    st.subheader("Delete Investigation")
    investigation_id_delete = st.number_input("Investigation ID to Delete", min_value=1, key="delete_investigation_id")
    if st.button("Delete Investigation"):
        result = delete_investigation(investigation_id_delete)
        st.write(result)
    
    st.title("Crime Operations")

    # Create Crime
    st.subheader("Create Crime")
    fir_id = st.number_input("FIR ID", min_value=1, key="admin_crime_id")
    type_of_crime = st.text_input("Type of Crime")
    details = st.text_area("Details")
    investigation_id = st.number_input("Investigation ID", min_value=1)
    if st.button("Create Crime"):
        result = create_crime(fir_id, type_of_crime, details, investigation_id)
        st.write(result)

    # Read Crimes
    st.subheader("Read Crimes")
    if st.button("Get All Crimes"):
        crimes = read_crimes()
        st.write(crimes)

    # Read Specific Crime
    st.subheader("Read Specific Crime")
    crime_id_read = st.number_input("Crime ID to Read", min_value=1, key="read_crime_id")
    if st.button("Read Crime"):
        crime = read_crime(crime_id_read)
        st.write(crime)

    # Update Crime
    st.subheader("Update Crime")
    crime_id_update = st.number_input("Crime ID to Update", min_value=1, key="admin_update_crime_id")
    update_fir_id = st.number_input("New FIR ID", min_value=1, key="admin_update_crime_fir_id")
    update_type_of_crime = st.text_input("New Type of Crime", key="admin_update_type_of_crime")
    update_details = st.text_area("New Details", key="admin_crime_update_details")
    update_investigation_id = st.number_input("New Investigation ID", min_value=1, key="admin_crime_update_investigation_id")
    if st.button("Update Crime"):
        result = update_crime(crime_id_update, update_fir_id, update_type_of_crime, update_details, update_investigation_id)
        st.write(result)

    # Delete Crime
    st.subheader("Delete Crime")
    crime_id_delete = st.number_input("Crime ID to Delete", min_value=1, key="admin_delete_crime_id")
    if st.button("Delete Crime"):
        result = delete_crime(crime_id_delete)
        st.write(result)
    
    st.title("Criminal Operations")

    # Create Criminal
    st.subheader("Create Criminal")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    address = st.text_input("Address")
    city = st.text_input("City")
    gender = st.text_input("Gender")
    height = st.number_input("Height")
    date_arrest = st.text_input("Date of Arrest (YYYY-MM-DD)")
    date_release = st.text_input("Date of Release (YYYY-MM-DD)")
    date_birth = st.text_input("Date of Birth (YYYY-MM-DD)")
    occupation = st.text_input("Occupation")
    if st.button("Create Criminal"):
        result = create_criminal(first_name, last_name, address, city, gender, height, date_arrest, date_release, date_birth, occupation)
        st.write(result)

    # Read Criminals
    st.subheader("Read Criminals")
    if st.button("Get All Criminals"):
        criminals = read_criminals()
        st.write(criminals)

    # Read Specific Criminal
    st.subheader("Read Specific Criminal")
    criminal_id_read = st.number_input("Criminal ID to Read", min_value=1, key="read_criminal_id")
    if st.button("Read Criminal"):
        criminal = read_criminal(criminal_id_read)
        st.write(criminal)

    # Update Criminal
    st.subheader("Update Criminal")
    criminal_id_update = st.number_input("Criminal ID to Update", min_value=1, key="update_criminal_id")
    # update_name = st.text_input("New Name", key="update_name")
    update_first_name = st.text_input("New Name", key="admin_update_criminal_first_name")
    update_last_name = st.text_input("New Name", key="admin_update_criminal_last_name")
    update_address = st.text_input("New Address", key="admin_update_criminal_address")
    update_city = st.text_input("New City", key="admin_update_criminal_city")
    update_gender = st.text_input("New Gender", key="admin_update_criminal_gender")
    update_height = st.text_input("New Height", key="update_height")
    update_date_arrest = st.text_input("New Date of Arrest (YYYY-MM-DD)", key="admin_update_criminal_arrest")
    update_date_release = st.text_input("New Date of Release (YYYY-MM-DD)", key="admin_update_criminal_release")
    update_date_birth = st.text_input("New Date of Birth (YYYY-MM-DD)", key="admin_update_criminal_date_birth")
    update_occupation = st.text_input("New Occupation", key="admin_update_criminal_occupation")
    if st.button("Update Criminal"):
        result = update_criminal(criminal_id_update, update_first_name, update_last_name, update_address, update_city, update_gender, update_height, update_date_arrest, update_date_release, update_date_birth, update_occupation)
        st.write(result)
    

    st.subheader("Lookup Criminal")
    criminal_lookup_first_name = st.text_input("First Name", key="admin_criminal_lookup_first_name")
    criminal_lookup_last_name = st.text_input("Last Name", key="admin_criminal_lookup_last_name")
    if st.button("Lookup Criminal Record"):
        criminal_record = get_criminal_record(criminal_lookup_first_name, criminal_lookup_last_name)
        st.write(criminal_record)


    # Delete Criminal
    st.subheader("Delete Criminal")
    criminal_id_delete = st.number_input("Criminal ID to Delete", min_value=1, key="delete_criminal_id")
    if st.button("Delete Criminal"):
        result = delete_criminal(criminal_id_delete)
        st.write(result)
    

    st.title("Investigation Officer Operations")

    # Create Investigation Officer
    st.subheader("Create Investigation Officer")
    officer_id = st.number_input("Officer ID", min_value=1, step=1)
    investigation_id = st.number_input("Investigation ID", min_value=1, step=1)
    if st.button("Create Investigation Officer"):
        result = create_investigation_officer(officer_id, investigation_id)
        st.write(result)

    # Read Investigation Officers
    st.subheader("Read Investigation Officers")
    if st.button("Get All Investigation Officers"):
        investigation_officers = read_investigation_officers()
        st.write(investigation_officers)

    # Read Specific Investigation Officer
    st.subheader("Read Specific Investigation Officer")
    officer_id_read = st.number_input("Officer ID", min_value=1, step=1, key="read_officer_id")
    investigation_id_read = st.number_input("Investigation ID", min_value=1, step=1, key="admin_read_investigation_id")
    if st.button("Read Investigation Officer"):
        investigation_officer = read_investigation_officer(officer_id_read, investigation_id_read)
        st.write(investigation_officer)

    # Delete Investigation Officer
    st.subheader("Delete Investigation Officer")
    officer_id_delete = st.number_input("Officer ID", min_value=1, step=1, key="delete_officer_id")
    investigation_id_delete = st.number_input("Investigation ID", min_value=1, step=1, key="admin_delete_investigation_id")
    if st.button("Delete Investigation Officer"):
        result = delete_investigation_officer(officer_id_delete, investigation_id_delete)
        st.write(result)

    
    st.title("Crimes Involved Operations")

    # Create Crimes Involved
    st.subheader("Create Crimes Involved")
    crime_id = st.number_input("Crime ID", min_value=1, step=1)
    criminal_id = st.number_input("Criminal ID", min_value=1, step=1)
    if st.button("Create Crimes Involved"):
        result = create_crimes_involved(int(crime_id), int(criminal_id))
        st.write(result)

    # Read Crimes Involved
    st.subheader("Read Crimes Involved")
    if st.button("Get All Crimes Involved"):
        crimes_involved = read_crimes_involved()
        st.write(crimes_involved)

    # Read Specific Crimes Involved
    st.subheader("Read Specific Crimes Involved")
    crime_id_read = st.number_input("Crime ID", min_value=1, step=1, key="admin_read_crime_id")
    criminal_id_read = st.number_input("Criminal ID", min_value=1, step=1, key="admin_read_criminal_id")
    if st.button("Read Crimes Involved"):
        crimes_involved = read_specific_crimes_involved(int(crime_id_read), int(criminal_id_read))
        st.write(crimes_involved)

    # Delete Crimes Involved
    st.subheader("Delete Crimes Involved")
    crime_id_delete = st.number_input("Crime ID", min_value=1, step=1, key="admin_delete_crimes_id")
    criminal_id_delete = st.number_input("Criminal ID", min_value=1, step=1, key="admin_delete_crimes_involved")
    if st.button("Delete Crimes Involved"):
        result = delete_crimes_involved(int(crime_id_delete), int(criminal_id_delete))
        st.write(result)


        st.title("Part Of Operations")

    # Create Part Of
    st.subheader("Create Part Of")
    investigation_id = st.number_input("Investigation ID", min_value=1, step=1, key="admin_part_of_investigation_id")
    criminal_id = st.number_input("Criminal ID", min_value=1, step=1, key="admin_part_of_criminal_id")
    if st.button("Create Part Of"):
        result = create_part_of(int(investigation_id), int(criminal_id))
        st.write(result)

    # Read Part Of
    st.subheader("Read Part Of")
    if st.button("Get All Part Of"):
        part_of_entries = read_part_of()
        st.write(part_of_entries)

    # Read Specific Part Of
    st.subheader("Read Specific Part Of")
    investigation_id_read = st.number_input("Investigation ID", min_value=1, step=1, key="admin_part_of_read_investigation_id")
    criminal_id_read = st.number_input("Criminal ID", min_value=1, step=1, key="admin_part_of_read_criminal_id")
    if st.button("Read Part Of"):
        part_of_entry = read_specific_part_of(int(investigation_id_read), int(criminal_id_read))
        st.write(part_of_entry)

    # Delete Part Of
    st.subheader("Delete Part Of")
    investigation_id_delete = st.number_input("Investigation ID", min_value=1, step=1, key="admin_part_of_delete_investigation_id")
    criminal_id_delete = st.number_input("Criminal ID", min_value=1, step=1, key="admin_part_of_delete_criminal_id")
    if st.button("Delete Part Of"):
        result = delete_part_of(int(investigation_id_delete), int(criminal_id_delete))
        st.write(result)


# User tab
def user_tab():
    st.header("User Operations")

    # st.subheader("Create Police Station")
    # station_name = st.text_input("Station Name", key="user_station_name")
    # location = st.text_input("Location", key="user_location")
    # username = st.text_input("Station Username", key="user_station_username")
    # password = st.text_input(
    #     "Station Password", type="password", key="user_station_password"
    # )
    # if st.button("Create Station", key="user_create_station_button"):
    #     result = create_station(station_name, location, username, password)
    #     st.write(result)

    # st.subheader("Create Role")
    # role_name = st.text_input("Role Name", key="user_role_name")
    # permission = st.text_input("Permission", key="user_permission")
    # if st.button("Create Role", key="user_create_role_button"):
    #     result = create_role(role_name, permission)
    #     st.write(result)

    # st.subheader("Create Officer")
    # role_id = st.number_input("Role ID", min_value=1, key="user_role_id")
    # first_name = st.text_input("First Name", key="user_first_name")
    # last_name = st.text_input("Last Name", key="user_last_name")
    # post = st.text_input("Post", key="user_post")
    # mobile_no = st.text_input("Mobile Number", key="user_mobile_no")
    # address = st.text_input("Address", key="user_address")
    # username = st.text_input("Officer Username", key="user_officer_username")
    # password = st.text_input(
    #     "Officer Password", type="password", key="user_officer_password"
    # )
    # station_id = st.number_input("Station ID", min_value=1, key="user_station_id")
    # if st.button("Create Officer", key="user_create_officer_button"):
    #     result = create_officer(
    #         role_id,
    #         first_name,
    #         last_name,
    #         post,
    #         mobile_no,
    #         address,
    #         username,
    #         password,
    #         station_id,
    #     )
    #     st.write(result)

    # st.subheader("Read Data")
    # if st.button("Get All Police Stations", key="user_get_stations"):
    #     stations = get_data("stations")
    #     st.table(stations)

    st.subheader("Create FIR")
    police_station_id = st.number_input("Police Station ID", min_value=1, key="user_police_station_id")
    officer_id = st.number_input("Officer ID", min_value=1, key="user_officer_id")
    title = st.text_input("Title", key="user_title")
    act = st.text_input("Act", key="user_act")
    complaint_name = st.text_input("Complaint Name", key="user_complaint_name")
    date_added = st.text_input("Date Added (YYYY-MM-DD)", key="user_date_added")
    details = st.text_area("Details", key="user_details")
    contact_number = st.text_input("Contact Number", key="user_contact_number")
    if st.button("Create FIR", key="user_create_fir_button"):
        result = create_fir(police_station_id, officer_id, title, act, complaint_name, date_added, details, contact_number)
        st.write(result)

    st.subheader("Update FIR")
    fir_id_update = st.number_input("FIR ID to Update", min_value=1, key="user_fir_id_update")
    update_police_station_id = st.number_input("New Police Station ID", min_value=1, key="user_update_police_station_id")
    update_officer_id = st.number_input("New Officer ID", min_value=1, key="user_update_officer_id")
    update_title = st.text_input("New Title", key="user_update_title")
    update_act = st.text_input("New Act", key="user_update_act")
    update_complaint_name = st.text_input("New Complaint Name", key="user_update_complaint_name")
    update_date_added = st.text_input("New Date Added (YYYY-MM-DD)", key="user_update_date_added")
    update_details = st.text_area("New Details", key="user_update_details")
    update_contact_number = st.text_input("New Contact Number", key="user_update_contact_number")
    if st.button("Update FIR", key="user_update_fir_button"):
        result = update_fir(fir_id_update, update_police_station_id, update_officer_id, update_title, update_act, update_complaint_name, update_date_added, update_details, update_contact_number)
        st.write(result)

    st.subheader("Read Data")
    if st.button("Get All Police Stations", key="user_get_stations"):
        stations = get_data("stations")
        st.table(stations)

    # if st.button("Get All Roles", key="user_get_roles"):
    #     roles = get_data("roles")
    #     st.write(roles)

    if st.button("Get All Officers", key="user_get_officers"):
        officers = get_data("officers")
        st.table(officers)


# Tabs for admin and user
tab1, tab2 = st.tabs(["Admin", "User"])

with tab1:
    admin_tab()

with tab2:
    user_tab()

# if __name__ == '__main__':
#     st.run()


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            st.experimental_rerun()


if __name__ == "__main__":
    observer = Observer()
    event_handler = MyHandler()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
