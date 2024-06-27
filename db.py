import mysql.connector

# Database connection details
config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'your_database'
}

def connect_to_db():
    return mysql.connector.connect(**config)

def create_officer(cursor, officer):
    query = """
    INSERT INTO POLICE_OFFICER (role_id, first_name, last_name, post, mobile_no, address, username, password, station_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, officer)

def read_officer(cursor, officer_id):
    query = "SELECT * FROM POLICE_OFFICER WHERE officer_id = %s"
    cursor.execute(query, (officer_id,))
    return cursor.fetchone()

def update_officer(cursor, officer_id, updated_data):
    query = """
    UPDATE POLICE_OFFICER
    SET role_id = %s, first_name = %s, last_name = %s, post = %s, mobile_no = %s, address = %s, username = %s, password = %s, station_id = %s
    WHERE officer_id = %s
    """
    cursor.execute(query, (*updated_data, officer_id))

def delete_officer(cursor, officer_id):
    query = "DELETE FROM POLICE_OFFICER WHERE officer_id = %s"
    cursor.execute(query, (officer_id,))

# Add similar functions for other tables...

if __name__ == '__main__':
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Example usage:
    new_officer = (1, 'John', 'Doe', 'Inspector', '1234567890', '123 Main St', 'jdoe', 'password', 1)
    create_officer(cursor, new_officer)
    conn.commit()
    
    officer = read_officer(cursor, 1)
    print(officer)
    
    updated_officer = (1, 'Jane', 'Doe', 'Inspector', '0987654321', '456 Elm St', 'jdoe', 'newpassword', 1)
    update_officer(cursor, 1, updated_officer)
    conn.commit()
    
    delete_officer(cursor, 1)
    conn.commit()
    
    cursor.close()
    conn.close()
