import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="192.168.1.101",
            user="esther",
            port=4567,
            password="Dptmej6408!",
            database="club_management"
        )
        print("데이터베이스 연결 성공!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def check_db_status(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("현재 데이터베이스 테이블 목록:")
    for table in tables:
        print(table[0])
    cursor.close()
