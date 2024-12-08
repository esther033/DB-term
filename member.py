from utils import get_valid_input

def search_member(connection):
    """회원 검색"""
    cursor = connection.cursor()
    search_type = get_valid_input(
        "학번(StudentNumber)으로 검색하려면 1, 이름(Name)으로 검색하려면 2를 입력하세요: ",
        pattern=r"^[12]$",
        error_message="1 또는 2를 입력하세요."
    )
    if search_type == "1":
        student_number = get_valid_input(
            "검색할 학번을 입력하세요: ",
            pattern=r"^\d+$",
            error_message="학번은 숫자로만 입력해야 합니다."
        )
        query = "SELECT * FROM MEMBER WHERE StudentNumber = %s"
        cursor.execute(query, (student_number,))
    elif search_type == "2":
        name = get_valid_input(
            "검색할 이름을 입력하세요: ",
            error_message="이름은 비어 있을 수 없습니다."
        )
        query = "SELECT * FROM MEMBER WHERE Name = %s"
        cursor.execute(query, (name,))
    
    results = cursor.fetchall()
    if results:
        headers = ["학번", "이름", "역할", "이메일", "전화번호", "가입 날짜"]
        column_widths = [
            max(len(headers[i]), max(len(str(row[i])) for row in results)) + 2
            for i in range(len(headers))
        ]
        separator = "+".join("-" * width for width in column_widths)
        print(f"+{separator}+")
        header_row = " | ".join(f"{headers[i]:<{column_widths[i]}}" for i in range(len(headers)))
        print(f"| {header_row} |")
        print(f"+{separator}+")
        for row in results:
            row_line = " | ".join(f"{str(row[i]):<{column_widths[i]}}" for i in range(len(row)))
            print(f"| {row_line} |")
        print(f"+{separator}+")
    else:
        print("검색 결과가 없습니다.")
    cursor.close()

def add_member(connection):
    """회원 추가"""
    cursor = connection.cursor()
    try:
        student_number = get_valid_input(
            "학번(StudentNumber): ",
            pattern=r"^\d+$",
            error_message="학번은 숫자로만 입력해야 합니다."
        )
        name = get_valid_input("이름(Name): ", error_message="이름은 필수 입력 항목입니다.")
        role = input("역할(Role, 기본값: member): ").strip()
        if not role:
            role = "member"
        email = get_valid_input(
            "이메일(Email): ",
            pattern=r"[^@]+@[^@]+\.[^@]+",
            error_message="유효하지 않은 이메일 형식입니다. 다시 입력해주세요."
        )
        phone = get_valid_input(
            "전화번호(PhoneNumber): ",
            pattern=r"^\d{2,3}-\d{3,4}-\d{4}$",
            error_message="유효하지 않은 전화번호 형식입니다. 예: 010-1234-5678"
        )
        join_date = get_valid_input(
            "가입 날짜(YYYY-MM-DD): ",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            error_message="날짜 형식이 올바르지 않습니다. 예: 2023-01-01"
        )
        cursor.execute("SELECT * FROM MEMBER WHERE StudentNumber = %s", (student_number,))
        if cursor.fetchone():
            print(f"이미 존재하는 학번입니다: {student_number}")
            return
        query = """
        INSERT INTO MEMBER (StudentNumber, Name, Role, Email, PhoneNumber, JoinDate)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (student_number, name, role, email, phone, join_date))
        connection.commit()
        print("=" * 50)
        print("회원이 성공적으로 추가되었습니다!")
        print(f"학번: {student_number}, 이름: {name}, 역할: {role}, 이메일: {email}, 전화번호: {phone}, 가입 날짜: {join_date}")
        print("=" * 50)
    except Exception as err:
        print(f"회원 추가 중 오류 발생: {err}")
    finally:
        cursor.close()