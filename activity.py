from utils import get_valid_input

def view_activities_by_club(connection):
    """동아리별 활동 목록 출력"""
    cursor = connection.cursor()
    try:
        # 동아리 이름 입력
        club_name = get_valid_input(
            "조회할 동아리 이름(Club Name): ",
            error_message="동아리 이름은 비어 있을 수 없습니다."
        )

        # 동아리 이름으로 ClubID 조회
        query_club_id = "SELECT ClubID FROM CLUB WHERE Name = %s"
        cursor.execute(query_club_id, (club_name,))
        club_result = cursor.fetchone()

        if not club_result:
            print(f"'{club_name}' 동아리가 존재하지 않습니다.")
            return

        club_id = club_result[0]

        # 활동 목록 조회
        query = """
        SELECT ActivityNumber, Name, Start_date, End_date, Location
        FROM ACTIVITY
        WHERE Controlling_Club = %s
        """
        cursor.execute(query, (club_id,))
        results = cursor.fetchall()

        if results:
            # 헤더와 데이터를 위한 열 너비 계산
            headers = ["활동 번호", "활동 이름", "시작 날짜", "종료 날짜", "장소"]
            column_widths = [
                max(len(headers[i]), max(len(str(row[i])) for row in results)) + 2
                for i in range(len(headers))
            ]

            # 구분선 생성
            separator = "+".join("-" * width for width in column_widths)

            # 출력
            print(f"+{separator}+")
            header_row = " | ".join(f"{headers[i]:<{column_widths[i]}}" for i in range(len(headers)))
            print(f"| {header_row} |")
            print(f"+{separator}+")
            for row in results:
                row_line = " | ".join(f"{str(row[i]):<{column_widths[i]}}" for i in range(len(row)))
                print(f"| {row_line} |")
            print(f"+{separator}+")
        else:
            print(f"'{club_name}' 동아리에 등록된 활동이 없습니다.")
    except Exception as err:
        print(f"활동 조회 중 오류 발생: {err}")
    finally:
        cursor.close()


def add_activity(connection):
    """활동 추가"""
    cursor = connection.cursor()
    try:
        # 활동 정보 입력
        activity_name = get_valid_input("활동 이름(Name): ", error_message="활동 이름은 필수 입력 항목입니다.")
        start_date = get_valid_input(
            "활동 시작 날짜(YYYY-MM-DD): ",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            error_message="날짜 형식이 올바르지 않습니다. 예: 2024-01-01"
        )
        end_date = get_valid_input(
            "활동 종료 날짜(YYYY-MM-DD): ",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            error_message="날짜 형식이 올바르지 않습니다. 예: 2024-01-10"
        )
        location = get_valid_input("활동 장소(Location): ", error_message="활동 장소는 필수 입력 항목입니다.")
        club_name = get_valid_input("활동을 주관하는 동아리 이름(Club Name): ", error_message="동아리 이름은 필수 입력 항목입니다.")

        # 동아리 이름으로 ClubID 조회
        query_club_id = "SELECT ClubID FROM CLUB WHERE Name = %s"
        cursor.execute(query_club_id, (club_name,))
        club_result = cursor.fetchone()

        if not club_result:
            print(f"'{club_name}' 동아리가 존재하지 않습니다. 활동 추가를 취소합니다.")
            return

        club_id = club_result[0]

        # 데이터 삽입
        query = """
        INSERT INTO ACTIVITY (Name, Start_date, End_date, Location, Controlling_Club)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (activity_name, start_date, end_date, location, club_id))
        connection.commit()
        print(f"활동 '{activity_name}'이(가) 성공적으로 추가되었습니다.")
    except Exception as err:
        print(f"활동 추가 중 오류 발생: {err}")
    finally:
        cursor.close()

def delete_activity(connection):
    """활동 삭제"""
    cursor = connection.cursor()
    try:
        # 삭제할 활동 번호 입력
        activity_number = get_valid_input(
            "삭제할 활동 번호(Activity Number)를 입력하세요: ",
            pattern=r"^\d+$",
            error_message="활동 번호는 숫자로만 입력해야 합니다."
        )

        # 삭제할 활동 확인
        query_check = "SELECT * FROM ACTIVITY WHERE ActivityNumber = %s"
        cursor.execute(query_check, (activity_number,))
        result = cursor.fetchone()

        if not result:
            print(f"활동 번호 {activity_number}에 해당하는 활동이 없습니다.")
            return

        # 활동 삭제
        confirmation = input(f"활동 번호 {activity_number}을(를) 삭제하시겠습니까? (Y/N): ").strip().lower()
        if confirmation == 'y':
            query_delete = "DELETE FROM ACTIVITY WHERE ActivityNumber = %s"
            cursor.execute(query_delete, (activity_number,))
            connection.commit()
            print(f"활동 번호 {activity_number}이(가) 성공적으로 삭제되었습니다.")
        else:
            print("삭제 작업이 취소되었습니다.")
    except Exception as err:
        print(f"활동 삭제 중 오류 발생: {err}")
    finally:
        cursor.close()

def update_activity(connection):
    """활동 수정"""
    cursor = connection.cursor()
    try:
        # 수정할 활동 번호 입력
        activity_number = get_valid_input(
            "수정할 활동 번호(Activity Number)를 입력하세요: ",
            pattern=r"^\d+$",
            error_message="활동 번호는 숫자로만 입력해야 합니다."
        )

        # 수정할 활동 확인
        query_check = "SELECT * FROM ACTIVITY WHERE ActivityNumber = %s"
        cursor.execute(query_check, (activity_number,))
        result = cursor.fetchone()

        if not result:
            print(f"활동 번호 {activity_number}에 해당하는 활동이 없습니다.")
            return

        # 현재 활동 정보 출력
        print(f"현재 활동 정보: 번호={result[0]}, 이름={result[1]}, 시작 날짜={result[2]}, 종료 날짜={result[3]}, 장소={result[4]}")

        # 수정할 값 입력
        print("수정할 내용을 입력하세요. 수정하지 않을 항목은 Enter를 입력하세요.")
        new_name = input(f"새 이름(Name, 현재: {result[1]}): ").strip() or result[1]
        new_start_date = get_valid_input(
            f"새 시작 날짜(YYYY-MM-DD, 현재: {result[2]}): ",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            error_message="날짜 형식이 올바르지 않습니다. 예: 2024-01-01"
        ) or result[2]
        new_end_date = get_valid_input(
            f"새 종료 날짜(YYYY-MM-DD, 현재: {result[3]}): ",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            error_message="날짜 형식이 올바르지 않습니다. 예: 2024-01-10"
        ) or result[3]
        new_location = input(f"새 장소(Location, 현재: {result[4]}): ").strip() or result[4]

        # 데이터 업데이트
        query_update = """
        UPDATE ACTIVITY
        SET Name = %s, Start_date = %s, End_date = %s, Location = %s
        WHERE ActivityNumber = %s
        """
        cursor.execute(query_update, (new_name, new_start_date, new_end_date, new_location, activity_number))
        connection.commit()
        print(f"활동 번호 {activity_number} 정보가 성공적으로 수정되었습니다.")
    except Exception as err:
        print(f"활동 수정 중 오류 발생: {err}")
    finally:
        cursor.close()
