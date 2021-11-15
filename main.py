from flask import Flask, json, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student, Subject, Grade

app = Flask(__name__)

engine = create_engine('sqlite:///school.db?check_same_thread=False')


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Grades


@app.route('/student/<int:studentID>/grade/api')
def grades(studentID):
    students = session.query(Student).filter_by(id=f'{studentID}').one()
    grade = session.query(Grade).filter_by(student_id=f'{studentID}')
    subjects = ["Math", "Arabic", "Science", "Biology", "Chemistry", "Physicsc", "History"]
    grades = []
    subIn = 0
    for r in grade:
        grades.append(f'{subjects[subIn], r.grade}')
        subIn = subIn+1
    # print()
    # return jsonify(students=students, grade=[ra.serialize for ra in grade])
    return json.dumps({'Name': students.name,
                       'grade': grades})


@app.route('/student/<int:student_id>/subject/api')
def studentSubjectJSON(student_id):
    student = session.query(Student).filter_by(id=student_id).one()
    items = session.query(Subject).filter_by(
        student=student_id).all()
    return jsonify(Subject=[i.serialize for i in items])


@app.route('/student/<int:student_id>/subject/<int:subject_id>/api')
def subjectJSON(student_id, subject_id):
    subject = session.query(Subject).filter_by(id=subject_id).one()
    return jsonify(subject=subject.serialize)


@app.route('/student/api')
def studentsJSON():
    students = session.query(Student).all()
    return jsonify(students=[r.serialize for r in students])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
