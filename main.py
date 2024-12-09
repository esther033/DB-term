from db_connection import connect_to_database, check_db_status
from member import search_member, add_member, update_member, delete_member
import textwrap

def main():
    connection = connect_to_database()
    if not connection:
        print("데이터베이스 연결에 실패했습니다. 프로그램을 종료합니다.")
        return

    while True:
        print(textwrap.dedent("""
        =========================
              === 메뉴 ===
        =========================
        1. 데이터베이스 상태 확인
        2. 회원 관리
        3. 종료
        =========================
        """))
        choice = input("메뉴 번호를 선택하세요: ")

        if choice == "1":
            check_db_status(connection)
        elif choice == "2":
            print(textwrap.dedent("""
                =========================
                    === 회원 관리 ===
                =========================
                1. 회원 검색
                2. 회원 추가
                3. 회원 정보 수정
                4. 회원 삭제    
                =========================
                """))
            sub_choice = input("회원 관리 메뉴 번호를 선택하세요: ")
            if sub_choice == "1":
                search_member(connection)
            elif sub_choice == "2":
                add_member(connection)
            elif sub_choice == "3":
                update_member(connection)
            elif sub_choice == "4":
                delete_member(connection)
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

    connection.close()

if __name__ == "__main__":
    main()
