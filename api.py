from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from shedule.shedule import update_shedule as upd_shedule
from email_sender.email_sender import reset_password

from database import tables
from database.database import get_session
import models

app = FastAPI()


@app.get('/api/get_students')
async def get_students(session: Session = Depends(get_session)):
    result = []
    for student in session.query(tables.Student).all():
        group = session.query(tables.Group).filter(tables.Group.group_id == student.student_group_id).first()
        student_dict = student.__dict__
        student_dict.pop("student_group_id")
        student_dict.update({"student_group": group.group_name})
        result.append(student_dict)
    return result


@app.get('/api/get_teachers')
async def get_teachers(session: Session = Depends(get_session)):
    result = [x.__dict__ for x in session.query(tables.Teacher).all()]
    return result


@app.get('/api/get_groups')
async def get_groups(session: Session = Depends(get_session)):
    result = [x.group_name for x in session.query(tables.Group).all()]
    return result


@app.get('/api/get_confirmation_requests')
async def get_confirmation_requests(session: Session = Depends(get_session)):
    result = [x for x in session.query(tables.ConfirmationRequest).all()]
    return result


@app.get('/api/get_error_requests')
async def get_error_requests(session: Session = Depends(get_session)):
    result = [x for x in session.query(tables.ErrorRequest).all()]
    return result


@app.get('/api/get_groups/shedule/{group_name}')
async def get_group_shedule(group_name: str, session: Session = Depends(get_session)):
    result = session.query(tables.Group).filter(tables.Group.group_name == group_name).first()
    if result:
        result = result.group_shedule
    else:
        result = -1
    return result


@app.get('/api/get_admins')
async def get_admin(session: Session = Depends(get_session)):
    result = [x.__dict__ for x in session.query(tables.Admin).all()]
    return result


@app.get('/api/get_admins/{id}')
async def get_admin_by_id(id: int, session: Session = Depends(get_session)):
    result = session.query(tables.Admin).filter(tables.Admin.admin_id == id).first()
    if result:
        result = result.__dict__
    else:
        result = -1
    return result


@app.get('/api/get_all_academic_debts')
async def get_all_academic_debts(session: Session = Depends(get_session)):
    result = [x for x in session.query(tables.AcademicDebt).all()]
    return result


@app.get('/api/get_academic_debts')
async def get_academic_debts(request: models.GetAcademicDebts, session: Session = Depends(get_session)):
    academic_debt = [x.__dict__ for x in session.query(tables.AcademicDebt).filter(
        tables.AcademicDebt.academic_student_id == request.student_id).all()]
    if academic_debt:
        return academic_debt
    return -1


@app.get('/api/get_money_debts')
async def get_all_money_debts(session: Session = Depends(get_session)):
    result = [x for x in session.query(tables.MoneyDebts).all()]
    return result


@app.post('/api/admin_auth')
async def admin_auth(admin_auth: models.AdminAuth, session: Session = Depends(get_session)):
    admin = session.query(tables.Admin).filter(
        tables.Admin.admin_login == admin_auth.login,
        tables.Admin.admin_password == admin_auth.password,
    ).first()
    if admin:
        return admin.__dict__
    return -1


@app.post('/api/student_auth')
async def student_auth(student_auth: models.StudentAuth, session: Session = Depends(get_session)):
    student = session.query(tables.Student).filter(
        tables.Student.student_login == student_auth.login,
        tables.Student.student_password == student_auth.password
    ).first()
    if student:
        group = session.query(tables.Group).filter(tables.Group.group_id == student.student_group_id).first()
        student_dict = student.__dict__
        student_dict.pop("student_group_id")
        student_dict.update({"student_group": group.group_name})
        return student_dict
    return -1


@app.post('/api/create_admin')
async def create_admin(admin: models.Admin, session: Session = Depends(get_session)):
    try:
        admin = tables.Admin(
            admin_name=admin.name,
            admin_login=admin.login,
            admin_password=admin.password,
            admin_privilege=admin.privilege
        )
        session.add(admin)
        session.commit()
        return 0
    except:
        return -1


@app.post('/api/update_admin')
async def update_admin(admin: models.AdminUpdate, session: Session = Depends(get_session)):
    update_admin = session.query(tables.Admin).filter(tables.Admin.admin_id == admin.admin_id).first()
    if update_admin:
        if admin.name:
            update_admin.admin_name = admin.name
        if admin.privilege:
            update_admin.admin_privilege = admin.privilege
        session.commit()
        return 0
    return -1


@app.delete('/api/delete_admin/{id}')
async def delete_admin(id: int, session: Session = Depends(get_session)):
    delete_admin = session.query(tables.Admin).filter(tables.Admin.admin_id == id).first()
    if delete_admin:
        session.delete(delete_admin)
        session.commit()
        return 0
    return -1


@app.post('/api/create_teacher')
async def create_teacher(teacher: models.Teacher, session: Session = Depends(get_session)):
    try:
        new_teacher = tables.Teacher(
            teacher_name=teacher.name,
            teacher_email=teacher.email,
            teacher_phone=teacher.phone
        )
        session.add(new_teacher)
        session.commit()
        return 0
    except:
        return -1


@app.post('/api/update_teacher')
async def update_teacher(teacher: models.TeacherUpdate, session: Session = Depends(get_session)):
    update_teacher = session.query(tables.Teacher).filter(tables.Teacher.teacher_id == teacher.teacher_id).first()
    if update_teacher:
        if teacher.name:
            update_teacher.teacher_name = teacher.name
        if teacher.email:
            update_teacher.teacher_email = teacher.email
        if teacher.phone:
            update_teacher.teacher_phone = teacher.phone
        session.commit()
        return 0
    return -1


@app.delete('/api/delete_teacher/{id}')
async def delete_teacher(id: int, session: Session = Depends(get_session)):
    delete_teacher = session.query(tables.Teacher).filter(tables.Teacher.teacher_id == id).first()
    if delete_teacher:
        session.delete(delete_teacher)
        session.commit()
        return 0
    return -1


@app.post('/api/create_nf_student')
async def create_nf_student(student: models.NFStudent, session: Session = Depends(get_session)):
    if session.query(tables.Student).filter(tables.Student.student_login == student.login).first():
        return 1
    if session.query(tables.Student).filter(tables.Student.student_email == student.email).first():
        return 2

    group = session.query(tables.Group).filter(tables.Group.group_name == student.group).first()
    if group:
        new_student = tables.Student(
            student_group_id=group.group_id,
            student_login=student.login,
            student_password=student.password,
            student_email=student.email,
        )
        session.add(new_student)
        session.commit()
        result = await student_auth(models.StudentAuth(login=student.login, password=student.password), session)
        return result
    return -1


@app.post('/api/create_student')
async def create_student(student: models.Student, session: Session = Depends(get_session)):
    if session.query(tables.Student).filter(tables.Student.student_login == student.login).first():
        return 1
    if session.query(tables.Student).filter(tables.Student.student_email == student.email).first():
        return 2
    if session.query(tables.Student).filter(tables.Student.student_record_number == student.record_number).first():
        return 3

    group = session.query(tables.Group).filter(tables.Group.group_name == student.group).first()
    if group:
        new_student = tables.Student(
            student_group_id=group.group_id,
            student_login=student.login,
            student_password=student.password,
            student_email=student.email,
            student_firstname=student.firstname,
            student_lastname=student.lastname,
            student_middlename=student.middlename,
            student_record_number=student.record_number
        )
        session.add(new_student)
        session.commit()
        result = await student_auth(models.StudentAuth(login=student.login, password=student.password), session)
        new_confirmation_request = tables.ConfirmationRequest(
            confirmation_student_id=result['student_id'],
            confirmation_firstname=student.firstname,
            confirmation_lastname=student.lastname,
            confirmation_middlename=student.middlename,
            confirmation_record_number=student.record_number,
        )
        session.add(new_confirmation_request)
        session.commit()
        return result
    return -1


@app.post("/api/update_student")
async def update_student(student: models.StudentUpdate, session: Session = Depends(get_session)):
    update_student = session.query(tables.Student).filter(tables.Student.student_id == student.student_id).first()
    if update_student:
        if student.group:
            group = session.query(tables.Group).filter(tables.Group.group_name == student.group).first()
            if group:
                update_student.student_group_id = group.group_id
            else:
                return -1
        if student.firstname:
            update_student.student_firstname = student.firstname
        if student.lastname:
            update_student.student_lastname = student.lastname
        if student.middlename:
            update_student.student_middlename = student.middlename
        if student.record_number:
            update_student.student_record_number = student.record_number
        if student.email:
            update_student.student_email = student.email
        if student.eos_login:
            update_student.student_eos_login = student.eos_login
        if student.eos_password:
            update_student.student_eos_password = student.eos_password
        session.commit()
        return 0
    return -1


@app.delete('/api/delete_student/{id}')
async def delete_student(id: int, session: Session = Depends(get_session)):
    student = session.query(tables.Student).filter(tables.Student.student_id == id).first()
    if student:
        session.delete(student)
        session.commit()
        return 0
    return -1


@app.post("/api/create_confirmation_request")
async def create_confirmation_request(request: models.ConfirmationRequest, session: Session = Depends(get_session)):
    if session.query(tables.ConfirmationRequest).filter(tables.ConfirmationRequest.confirmation_student_id == request.student_id).first():
        return 4
    if session.query(tables.Student).filter(tables.Student.student_record_number == request.record_number).first():
        return 3
    student = session.query(tables.Student).filter(tables.Student.student_id == request.student_id).first()
    if student:
        new_confirmation_request = tables.ConfirmationRequest(
            confirmation_student_id=student.student_id,
            confirmation_firstname=request.firstname,
            confirmation_lastname=request.lastname,
            confirmation_middlename=request.middlename,
            confirmation_record_number=request.record_number,
        )
        session.add(new_confirmation_request)
        session.commit()
        return 0
    return -1


@app.post("/api/confirm_confirmation_request/{id}")
async def confirm_confirmation_request(id: int, session: Session = Depends(get_session)):
    confirmation_request = session.query(tables.ConfirmationRequest).filter(
        tables.ConfirmationRequest.confirmation_id == id).first()
    if confirmation_request:
        student = session.query(tables.Student).filter(
            tables.Student.student_id == confirmation_request.confirmation_student_id).first()
        student.student_confirmed = True
        student.student_firstname = confirmation_request.confirmation_firstname
        student.student_lastname = confirmation_request.confirmation_lastname
        student.student_middlename = confirmation_request.confirmation_middlename
        student.student_record_number = confirmation_request.confirmation_record_number
        session.delete(confirmation_request)
        session.commit()
        return 0
    return -1


@app.delete("/api/delete_confirmation_request/{id}")
async def delete_confirmation_request(id: int, session: Session = Depends(get_session)):
    confirmation_request = session.query(tables.ConfirmationRequest).filter(
        tables.ConfirmationRequest.confirmation_id == id).first()
    if confirmation_request:
        session.delete(confirmation_request)
        session.commit()
        return 0
    return -1


@app.post('/api/create_error_request')
async def create_error_request(request: models.ErrorRequest, session: Session = Depends(get_session)):
    try:
        error_request = tables.ErrorRequest(
            error_student_id=request.student_id,
            error_theme=request.theme,
            error_message=request.message
        )
        session.add(error_request)
        session.commit()
        return 0
    except:
        return -1


@app.delete('/api/delete_error_request/{id}')
async def delete_error_request(id: int, session: Session = Depends(get_session)):
    delete_error_request = session.query(tables.ErrorRequest).filter(tables.ErrorRequest.error_id == id).first()
    if delete_error_request:
        session.delete(delete_error_request)
        session.commit()
        return 0
    return -1


@app.post('/api/create_academic_debts')
async def create_academic_debts(academic_debt: models.CreateAcademicDebt, session: Session = Depends(get_session)):
    try:
        new_academic_debt = tables.AcademicDebt(
            academic_student_id=academic_debt.student_id,
            academic_subject=academic_debt.subject,
            academic_commentary=academic_debt.commentary,
            academic_delivery_date=academic_debt.delivery_date
        )
        session.add(new_academic_debt)
        session.commit()
        return 0
    except:
        return -1


@app.delete('/api/delete_academic_debts/{id}')
async def delete_academic_debts(id: int, session: Session = Depends(get_session)):
    delete_academic_debt = session.query(tables.AcademicDebt).filter(tables.AcademicDebt.academic_id == id).first()
    if delete_academic_debt:
        session.delete(delete_academic_debt)
        session.commit()
        return 0
    return -1


@app.post('/api/create_money_debts')
async def create_money_debts(money_debt: models.CreateMoneyDebt, session: Session = Depends(get_session)):
    try:
        new_money_debt = tables.MoneyDebts(
            money_student_id=money_debt.student_id,
            money_sum=money_debt.sum,
            money_commentary=money_debt.commentary,
            money_delivery_date=money_debt.delivery_date
        )
        session.add(new_money_debt)
        session.commit()
        return 0
    except:
        return -1


@app.delete('/api/delete_money_debts/{id}')
async def delete_money_debts(id: int, session: Session = Depends(get_session)):
    delete_money_debt = session.query(tables.MoneyDebts).filter(tables.MoneyDebts.money_id == id).first()
    if delete_money_debt:
        session.delete(delete_money_debt)
        session.commit()
        return 0
    return -1


@app.post('/api/update_shedule')
async def update_shedule(session: Session = Depends(get_session)):
    upd_shedule(session)
    return 0


@app.post('/api/reset_student_password')
async def reset_student_password(student: models.ResetEmail, session: Session = Depends(get_session)):
    if session.query(tables.Student).filter(tables.Student.student_email == student.email).first():
        global verify_code
        verify_code = reset_password(student.email)

        @app.post("/api/reset_student_password/code")
        async def check_code(code: models.ResetCode):
            global verify_code
            if code.code == verify_code:
                @app.post("/api/reset_student_password/new_password")
                async def new_password(password: models.ResetPassword, session: Session = Depends(get_session)):
                    try:
                        db_student = session.query(tables.Student).filter(
                            tables.Student.student_email == student.email).first()
                        db_student.student_password = password.password
                        session.commit()
                        return 0
                    except:
                        return -1

                return 0
            else:
                return -1  # код не верный

        return 0
    else:
        return -1  # Студента с таким E-mail не существует