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

    st.subheader("Create Role")
    role_name = st.text_input("Role Name", key="admin_role_name")
    permission = st.text_input("Permission", key="admin_permission")
    if st.button("Create Role", key="admin_create_role_button"):
        result = create_role(role_name, permission)
        st.write(result)

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


# User tab
def user_tab():
    st.header("User Operations")

    st.subheader("Create Police Station")
    station_name = st.text_input("Station Name", key="user_station_name")
    location = st.text_input("Location", key="user_location")
    username = st.text_input("Station Username", key="user_station_username")
    password = st.text_input(
        "Station Password", type="password", key="user_station_password"
    )
    if st.button("Create Station", key="user_create_station_button"):
        result = create_station(station_name, location, username, password)
        st.write(result)

    # st.subheader("Create Role")
    # role_name = st.text_input("Role Name", key="user_role_name")
    # permission = st.text_input("Permission", key="user_permission")
    # if st.button("Create Role", key="user_create_role_button"):
    #     result = create_role(role_name, permission)
    #     st.write(result)

    st.subheader("Create Officer")
    role_id = st.number_input("Role ID", min_value=1, key="user_role_id")
    first_name = st.text_input("First Name", key="user_first_name")
    last_name = st.text_input("Last Name", key="user_last_name")
    post = st.text_input("Post", key="user_post")
    mobile_no = st.text_input("Mobile Number", key="user_mobile_no")
    address = st.text_input("Address", key="user_address")
    username = st.text_input("Officer Username", key="user_officer_username")
    password = st.text_input(
        "Officer Password", type="password", key="user_officer_password"
    )
    station_id = st.number_input("Station ID", min_value=1, key="user_station_id")
    if st.button("Create Officer", key="user_create_officer_button"):
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
    if st.button("Get All Police Stations", key="user_get_stations"):
        stations = get_data("stations")
        st.write(stations)

    # if st.button("Get All Roles", key="user_get_roles"):
    #     roles = get_data("roles")
    #     st.write(roles)

    if st.button("Get All Officers", key="user_get_officers"):
        officers = get_data("officers")
        st.write(officers)


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
