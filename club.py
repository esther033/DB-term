from utils import get_valid_input

def view_clubs(connection):
    """동아리 목록 출력"""
    cursor = connection.cursor()
    try:
        query = "SELECT ClubID, Name, Location, Capacity FROM CLUB"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            headers = ["동아리 ID", "동아리 이름", "위치", "정원"]
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
            print("등록된 동아리가 없습니다.")
    except Exception as err:
        print(f"동아리 조회 중 오류 발생: {err}")
    finally:
        cursor.close()

def add_club(connection):
    """동아리 추가"""
    cursor = connection.cursor()
    try:
        club_name = get_valid_input("동아리 이름(Name): ", error_message="동아리 이름은 필수 입력 항목입니다.")
        location = get_valid_input("위치(Location): ", error_message="위치는 필수 입력 항목입니다.")
        capacity = get_valid_input(
            "정원(Capacity): ",
            pattern=r"^\d+$",
            error_message="정원은 숫자로 입력해야 합니다."
        )

        query = "INSERT INTO CLUB (Name, Location, Capacity) VALUES (%s, %s, %s)"
        cursor.execute(query, (club_name, location, capacity))
        connection.commit()
        print(f"동아리 '{club_name}'이(가) 성공적으로 추가되었습니다.")
    except Exception as err:
        print(f"동아리 추가 중 오류 발생: {err}")
    finally:
        cursor.close()

def update_club(connection):
    """동아리 수정"""
    cursor = connection.cursor()
    try:
        # 수정할 동아리 ID 입력
        club_id = input("수정할 동아리 ID를 입력하세요: ").strip()
        query_check = "SELECT * FROM CLUB WHERE ClubID = %s"
        cursor.execute(query_check, (club_id,))
        result = cursor.fetchone()

        if not result:
            print(f"동아리 ID {club_id}에 해당하는 동아리가 없습니다.")
            return

        # 현재 정보 출력
        print(f"현재 동아리 정보: ID={result[0]}, 이름={result[1]}, 위치={result[2]}, 수용 인원={result[3]}")
        print("수정할 내용을 입력하세요. 수정하지 않을 항목은 Enter를 입력하세요.")

        new_name = input(f"새 이름(현재: {result[1]}): ").strip() or result[1]
        new_location = input(f"새 위치(현재: {result[2]}): ").strip() or result[2]
        new_capacity = input(f"새 수용 인원(현재: {result[3]}): ").strip() or result[3]

        # 업데이트 쿼리 실행
        query_update = """
        UPDATE CLUB
        SET Name = %s, Location = %s, Capacity = %s
        WHERE ClubID = %s
        """
        cursor.execute(query_update, (new_name, new_location, new_capacity, club_id))
        connection.commit()
        print(f"동아리 ID {club_id}의 정보가 성공적으로 수정되었습니다.")
    except Exception as e:
        print(f"동아리 수정 중 오류 발생: {e}")
    finally:
        cursor.close()

def delete_club(connection):
    """동아리 삭제"""
    cursor = connection.cursor()
    try:
        # 삭제할 동아리 ID 입력
        club_id = input("삭제할 동아리 ID를 입력하세요: ").strip()
        query_check = "SELECT * FROM CLUB WHERE ClubID = %s"
        cursor.execute(query_check, (club_id,))
        result = cursor.fetchone()

        if not result:
            print(f"동아리 ID {club_id}에 해당하는 동아리가 없습니다.")
            return

        # 확인 후 삭제
        confirmation = input(f"동아리 ID {club_id}을(를) 삭제하시겠습니까? (Y/N): ").strip().lower()
        if confirmation == 'y':
            query_delete = "DELETE FROM CLUB WHERE ClubID = %s"
            cursor.execute(query_delete, (club_id,))
            connection.commit()
            print(f"동아리 ID {club_id}이(가) 성공적으로 삭제되었습니다.")
        else:
            print("삭제 작업이 취소되었습니다.")
    except Exception as e:
        print(f"동아리 삭제 중 오류 발생: {e}")
    finally:
        cursor.close()
