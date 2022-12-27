from flask import Flask
from flask_login import UserMixin
from json import load
from typing import Dict, Optional

users: Dict[str, "User"] = {}

class User(UserMixin):
    def __init__(self, id: str, username: str, email: str, password: str):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def get(user_id: str) -> Optional["User"]:
        return users.get(user_id)

    def __str__(self) -> str:
        return f"<Id: {self.id}, Username: {self.username}, Email: {self.email}>"

    def __repr__(self) -> str:
        return self.__str__()


with open("users.json") as file:
    data = load(file)
    for key in data:
        users[key] = User(
            id=key,
            username=data[key]["username"],
            email=data[key]["email"],
            password=data[key]["password"],
        )