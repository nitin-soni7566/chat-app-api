from pydantic import EmailStr, SecretStr
from fastapi import Query, Body, Form
from datetime import date
from enum import Enum


class Gender(str, Enum):
    a = "MALE"
    b = "FEMALE"
    c = "OTHER"


class Login:

    def __init__(
        self,
        username: EmailStr = Form(..., description="Register user eamil"),
        password: SecretStr = Form(..., description="User password"),
    ):
        self.username = username
        self.password = password


class CreateUser:

    def __init__(
        self,
        first_name: str = Form(..., description="User first name"),
        last_name: str = Form(..., description="User last name"),
        email: EmailStr = Form(..., description="User eamil"),
        gender: Gender = Form(..., description="User Gender MALE,FEMALE or OTHER"),
        dob: date = Form(..., description="User Date of Brith"),
        password: SecretStr = Form(..., description="User password"),
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.dob = dob
        self.password = password


class UpdateUser:

    def __init__(
        self,
        id: str = Form(..., description="User id"),
        first_name: str = Form(description="User first name"),
        last_name: str = Form(description="User last name"),
        email: EmailStr = Form(description="User eamil"),
        dob: date = Form(description="User Date of Brith"),
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.dob = dob


class UpdateUserPassword:

    def __init__(
        self,
        current_password: SecretStr = Form(..., description="User current password"),
        new_password: str = Form(..., description="User first name"),
    ):
        self.current_password = current_password
        self.new_password = new_password
