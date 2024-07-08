from typing import Optional
import datetime
from pydantic import BaseModel


class Admin(BaseModel):
    name: str
    login: str
    password: str
    privilege: str


class AdminUpdate(BaseModel):
    admin_id: int
    name: Optional[str] = None
    privilege: Optional[str] = None


class NFStudent(BaseModel):
    group: str
    login: str
    password: str
    email: str


class Student(BaseModel):
    group: str
    firstname: str
    lastname: str
    middlename: Optional[str] = None
    login: str
    password: str
    record_number: str
    email: str


class StudentUpdate(BaseModel):
    student_id: int
    group: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    middlename: Optional[str] = None
    record_number: Optional[str] = None
    email: Optional[str] = None
    eos_login: Optional[str] = None
    eos_password: Optional[str] = None


class AdminAuth(BaseModel):
    login: str
    password: str


class StudentAuth(BaseModel):
    login: str
    password: str


class GetAcademicDebts(BaseModel):
    student_id: int


class CreateAcademicDebt(BaseModel):
    student_id: int
    subject: str
    commentary: Optional[str] = None
    delivery_date: Optional[datetime.date] = None


class GetMoneyDebts(BaseModel):
    student_id: int


class CreateMoneyDebt(BaseModel):
    student_id: int
    sum: float
    commentary: Optional[str] = None
    delivery_date: Optional[datetime.date] = None


class IsConfirmation(BaseModel):
    student_id: int


class Teacher(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class TeacherUpdate(BaseModel):
    teacher_id: int
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class Group(BaseModel):
    name: str
    shedule: Optional[str] = None


class ConfirmationRequest(BaseModel):
    student_id: int
    lastname: str
    firstname: str
    middlename: str
    record_number: str


class ErrorRequest(BaseModel):
    student_id: int
    theme: str
    message: str


class Shedule(BaseModel):
    name: str


class ResetEmail(BaseModel):
    email: str


class ResetCode(BaseModel):
    code: str


class ResetPassword(BaseModel):
    password: str
