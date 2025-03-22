from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade

DATABASE_URL = "postgresql://postgres:1234test@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


# 1. Top 5 students with the highest average grade
def select_1():
    session = Session()
    result = (
        session.query(Student.name, func.avg(Grade.grade).label('avg_grade'))
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc('avg_grade'))
        .limit(5)
        .all()
    )
    session.close()
    return result


# 2. Student with the highest average grade in a specific subject
def select_2(subject_id):
    session = Session()
    result = (
        session.query(Student.name, func.avg(Grade.grade).label('avg_grade'))
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc('avg_grade'))
        .first()
    )
    session.close()
    return result


# 3. Average grade in each group for a specific subject
def select_3(subject_id):
    session = Session()
    result = (
        session.query(Group.name, func.avg(Grade.grade).label('avg_grade'))
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )
    session.close()
    return result


# 4. Average grade across all grades (stream average)
def select_4():
    session = Session()
    result = session.query(func.avg(Grade.grade)).scalar()
    session.close()
    return result


# 5. List of courses taught by a specific teacher
def select_5(teacher_id):
    session = Session()
    result = (
        session.query(Subject.name)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )
    session.close()
    return result


# 6. List of students in a specific group
def select_6(group_id):
    session = Session()
    result = (
        session.query(Student.name)
        .filter(Student.group_id == group_id)
        .all()
    )
    session.close()
    return result


# 7. Grades of students in a specific group and subject
def select_7(group_id, subject_id):
    session = Session()
    result = (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    session.close()
    return result


# 8. Average grade given by a specific teacher across their subjects
def select_8(teacher_id):
    session = Session()
    result = (
        session.query(func.avg(Grade.grade).label('avg_grade'))
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )
    session.close()
    return result


# 9. List of courses taken by a specific student
def select_9(student_id):
    session = Session()
    result = (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .group_by(Subject.name)
        .all()
    )
    session.close()
    return result


# 10. List of courses taught by a specific teacher to a specific student
def select_10(teacher_id, student_id):
    session = Session()
    result = (
        session.query(Subject.name)
        .join(Grade)
        .filter(Subject.teacher_id == teacher_id, Grade.student_id == student_id)
        .group_by(Subject.name)
        .all()
    )
    session.close()
    return result

# 11. Average grade that a specific teacher gives to a specific student
def select_11(teacher_id, student_id):
    session = Session()
    result = (
        session.query(func.avg(Grade.grade).label('avg_grade'))
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.teacher_id == teacher_id, Grade.student_id == student_id)
        .scalar()
    )
    session.close()
    return result


# 12. Grades of the students on specific subject in a specific group for the latest lesson
def select_12(group_id, subject_id):
    session = Session()
    latest_lesson = (
        session.query(func.max(Grade.grade_date))
        .join(Student)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .scalar()
    )

    result = (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id, Grade.grade_date == latest_lesson)
        .all()
    )

    session.close()
    return result