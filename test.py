import mysql.connector

def connect_to_database():
    connection = mysql.connector.connect(
        host="192.168.1.101",
        user="esther",
        port=4567,
        password="Dptmej6408!",
        database="club_management"
    )
    return connection

def fetch_all_members():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM MEMBER")
    members = cursor.fetchall()
    for member in members:
        print(member)
    cursor.close()
    connection.close()

def add_member(student_number, name, role, email, phone, join_date):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "INSERT INTO MEMBER (StudentNumber, Name, Role, Email, PhoneNumber, JoinDate) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (student_number, name, role, email, phone, join_date)
    cursor.execute(query, values)
    connection.commit()
    print(f"Member {name} added successfully!")
    cursor.close()
    connection.close()

# Example usage
if __name__ == "__main__":
    fetch_all_members()
    add_member(2023041048, "Jane Doe", "Member", "jane@example.com", "010-9876-5432", "2024-05-01")
