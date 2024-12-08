import re

def get_valid_input(prompt, pattern=None, error_message=None):
    """유효한 입력값을 받을 때까지 반복"""
    while True:
        user_input = input(prompt).strip()
        if not pattern or re.match(pattern, user_input):
            return user_input
        print(error_message or "잘못된 입력입니다. 다시 시도하세요.")
