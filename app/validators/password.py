from fastapi import HTTPException

from starlette import status

class PasswordValidator:
    def __init__(self, password: str):
        self.special_chars = ['$','@','#','%','!','^','&','*','(',')','-','_','+','=','{','}','[',']']
        self.password = password

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value):
        if not (self.check_special_characters(value) and self.check_contains_lowercase_uppercase(value) and self.check_numeric_characters(value)):
            raise ValueError("Password is invalid")
        self.__password = value

    def check_contains_lowercase_uppercase(self, value):
        return value not in [value.lower(), value.upper()]

    def check_special_characters(self, value):
        for special_char in self.special_chars:
            if special_char in value:
                return True
        return False

    def check_numeric_characters(self, value):
        for char in value:
            if char.isnumeric():
                return True
        return False