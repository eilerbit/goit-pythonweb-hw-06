from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from models import Base, Student, Group, Teacher, Subject, Grade
import random

DATABASE_URL = "postgresql://postgres:1234test@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

groups = [Group(name=fake.unique.word().capitalize()) for _ in range(3)]
session.add_all(groups)

teachers = [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]
session.add_all(teachers)

subjects = [Subject(name=fake.unique.word().capitalize(), teacher=random.choice(teachers)) for _ in range(random.randint(5, 8))]
session.add_all(subjects)

students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(random.randint(30, 50))]
session.add_all(students)

session.commit()

for student in students:
    for subject in subjects:
        for _ in range(random.randint(5, 20)):
            grade = Grade(
                student=student,
                subject=subject,
                grade=random.uniform(60, 100),
                grade_date=fake.date_between(start_date='-1y', end_date='today')
            )
            session.add(grade)

session.commit()
session.close()

print("Database seeded successfully!")