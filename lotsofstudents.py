from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import random
import random
from database_setup import Grade, Student, Base, Subject

engine = create_engine('sqlite:///school.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

students = ["Mohamed", "Ismail", "Ali"]
subjects = ["Math", "Arabic", "Science", "Biology", "Chemistry", "Physicsc", "History"]

for i in range(0, 3):
    session.add(Student(name=students[i]))
    session.commit()
    for y in range(0, 7):
        subject = Subject(name=subjects[y])
        session.add(subject)
        session.commit()

    for z in range(0, 7):
        grade = Grade(grade=(random.randint(1, 101)), student_id=i, subject_id=z)
        session.add(grade)
        session.commit()


print("Data added!")
