from sqlalchemy import (
    Column,
    ForeignKey,
    INTEGER,
    BOOLEAN,
    VARCHAR,
    JSON,
    DATE,
    FLOAT,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(INTEGER, primary_key=True)
    group_name = Column(VARCHAR(50), nullable=False)
    group_shedule = Column(JSON, nullable=True, default=None)


class Student(Base):
    __tablename__ = 'students'

    student_id = Column(INTEGER, primary_key=True)
    student_1c_id = Column(INTEGER, unique=True, nullable=True, default=None)
    student_group_id = Column(ForeignKey('groups.group_id'), nullable=False, index=True)
    student_confirmed = Column(BOOLEAN, nullable=False, default=False)
    student_expelled = Column(BOOLEAN, nullable=False, default=False)
    student_firstname = Column(VARCHAR(50), nullable=True, default=None)
    student_lastname = Column(VARCHAR(50), nullable=True, default=None)
    student_middlename = Column(VARCHAR(50), nullable=True, default=None)
    student_login = Column(VARCHAR(50), unique=True, nullable=False)
    student_password = Column(VARCHAR(200), nullable=False)
    student_record_number = Column(VARCHAR(11), unique=True, nullable=True, default=None)
    student_eos_login = Column(VARCHAR(50), nullable=True, default=None)
    student_eos_password = Column(VARCHAR(50), nullable=True, default=None)
    student_email = Column(VARCHAR(50), unique=True, nullable=True, default=None)


class Admin(Base):
    __tablename__ = 'admins'

    admin_id = Column(INTEGER, primary_key=True)
    admin_name = Column(VARCHAR(150), nullable=False)
    admin_login = Column(VARCHAR(50), nullable=False, unique=True)
    admin_password = Column(VARCHAR(200), nullable=False)
    admin_privilege = Column(VARCHAR(15), nullable=False)


class Teacher(Base):
    __tablename__ = 'teachers'

    teacher_id = Column(INTEGER, primary_key=True)
    teacher_name = Column(VARCHAR(150), nullable=False)
    teacher_email = Column(VARCHAR(50), unique=True)
    teacher_phone = Column(VARCHAR(50), nullable=True, default=None)


class ConfirmationRequest(Base):
    __tablename__ = 'confirmation_requests'

    confirmation_id = Column(INTEGER, primary_key=True)
    confirmation_student_id = Column(ForeignKey('students.student_id'), nullable=False, index=True)
    confirmation_firstname = Column(VARCHAR(50), nullable=False)
    confirmation_lastname = Column(VARCHAR(50), nullable=False)
    confirmation_middlename = Column(VARCHAR(50), nullable=True, default=None)
    confirmation_record_number = Column(VARCHAR(11), nullable=False)
    confirmation_file_path = Column(VARCHAR(200), nullable=False)


class ErrorRequest(Base):
    __tablename__ = 'error_requests'

    error_id = Column(INTEGER, primary_key=True)
    error_student_id = Column(ForeignKey('students.student_id'), nullable=False, index=True)
    error_theme = Column(VARCHAR(50), nullable=False)
    error_message = Column(VARCHAR(200), nullable=False)


class AcademicDebt(Base):
    __tablename__ = 'academic_debts'

    academic_id = Column(INTEGER, primary_key=True)
    academic_student_id = Column(ForeignKey('students.student_id'), nullable=False, index=True)
    academic_subject = Column(VARCHAR(50), nullable=False)
    academic_commentary = Column(VARCHAR(200), nullable=True, default=None)
    academic_delivery_date = Column(DATE, nullable=True, default=None)


class MoneyDebts(Base):
    __tablename__ = 'money_debts'

    money_id = Column(INTEGER, primary_key=True)
    money_student_id = Column(ForeignKey('students.student_id'), nullable=False, index=True)
    money_sum = Column(FLOAT, nullable=False)
    money_commentary = Column(VARCHAR(200), nullable=True, default=None)
    money_delivery_date = Column(DATE, nullable=True, default=None)


# engine = create_engine("postgresql+psycopg2://pguser:pgpassword@localhost/buildingdb", )
# Base.metadata.create_all(engine)
