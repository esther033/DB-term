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
