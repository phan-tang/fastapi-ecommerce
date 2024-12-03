from fastapi import HTTPException

import re

from starlette import status

class EmailValidator:
    def __init__(self, email: str):
        self.email = email

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value):
        r = re.compile(r'[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-z]{2,}')
        if not r.match(value):
            raise ValueError("Email is invalid")
        self.__email = value