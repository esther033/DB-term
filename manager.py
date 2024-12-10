from utils import get_valid_input

def view_assistants(connection):
    """조교 목록 출력"""
    cursor = connection.cursor()
    try:
        query = "SELECT ManagerID, Name, Email, PhoneNumber FROM MANAGER"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            headers = ["조교 ID", "이름", "이메일", "전화번호"]
            column_widths = [max(len(headers[i]), max(len(str(row[i])) for row in results)) + 2 for i in range(len(headers))]
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
            print("등록된 조교가 없습니다.")
    except Exception as err:
        print(f"조교 조회 중 오류 발생: {err}")
    finally:
        cursor.close()

def add_assistant(connection):
    """조교 추가"""
    cursor = connection.cursor()
    try:
        name = get_valid_input("조교 이름(Name): ", error_message="조교 이름은 필수 입력 항목입니다.")
        email = get_valid_input(
            "이메일(Email): ",
            pattern=r"[^@]+@[^@]+\.[^@]+",
            error_message="유효하지 않은 이메일 형식입니다."
        )
        phone = get_valid_input(
            "전화번호(PhoneNumber): ",
            pattern=r"^\d{2,3}-\d{3,4}-\d{4}$",
            error_message="전화번호 형식이 올바르지 않습니다. 예: 010-1234-5678"
        )

        query = "INSERT INTO MANAGER (Name, Email, PhoneNumber) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, phone))
        connection.commit()
        print(f"조교 '{name}'이(가) 성공적으로 추가되었습니다.")
    except Exception as err:
        print(f"조교 추가 중 오류 발생: {err}")
    finally:
        cursor.close()

def update_manager(connection):
    """조교 수정"""
    cursor = connection.cursor()
    try:
        # 수정할 조교 ID 입력
        manager_id = input("수정할 조교 ID를 입력하세요: ").strip()
        query_check = "SELECT * FROM MANAGER WHERE ManagerID = %s"
        cursor.execute(query_check, (manager_id,))
        result = cursor.fetchone()

        if not result:
            print(f"조교 ID {manager_id}에 해당하는 조교가 없습니다.")
            return

        # 현재 정보 출력
        print(f"현재 조교 정보: ID={result[0]}, 이름={result[1]}, 이메일={result[2]}, 전화번호={result[3]}")
        print("수정할 내용을 입력하세요. 수정하지 않을 항목은 Enter를 입력하세요.")

        new_name = input(f"새 이름(현재: {result[1]}): ").strip() or result[1]
        new_email = input(f"새 이메일(현재: {result[2]}): ").strip() or result[2]
        new_phone = input(f"새 전화번호(현재: {result[3]}): ").strip() or result[3]

        # 업데이트 쿼리 실행
        query_update = """
        UPDATE MANAGER
        SET Name = %s, Email = %s, PhoneNumber = %s
        WHERE ManagerID = %s
        """
        cursor.execute(query_update, (new_name, new_email, new_phone, manager_id))
        connection.commit()
        print(f"조교 ID {manager_id}의 정보가 성공적으로 수정되었습니다.")
    except Exception as e:
        print(f"조교 수정 중 오류 발생: {e}")
    finally:
        cursor.close()

def delete_manager(connection):
    """조교 삭제"""
    cursor = connection.cursor()
    try:
        # 삭제할 조교 ID 입력
        manager_id = input("삭제할 조교 ID를 입력하세요: ").strip()
        query_check = "SELECT * FROM MANAGER WHERE ManagerID = %s"
        cursor.execute(query_check, (manager_id,))
        result = cursor.fetchone()

        if not result:
            print(f"조교 ID {manager_id}에 해당하는 조교가 없습니다.")
            return

        # 확인 후 삭제
        confirmation = input(f"조교 ID {manager_id}을(를) 삭제하시겠습니까? (Y/N): ").strip().lower()
        if confirmation == 'y':
            query_delete = "DELETE FROM MANAGER WHERE ManagerID = %s"
            cursor.execute(query_delete, (manager_id,))
            connection.commit()
            print(f"조교 ID {manager_id}이(가) 성공적으로 삭제되었습니다.")
        else:
            print("삭제 작업이 취소되었습니다.")
    except Exception as e:
        print(f"조교 삭제 중 오류 발생: {e}")
    finally:
        cursor.close()
