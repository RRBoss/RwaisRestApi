from flask import Flask, json, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine, insert, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import null, table
from database_setup import Base, Student, Subject, Grade

app = Flask(__name__)

engine = create_engine('sqlite:///school.db?check_same_thread=False')


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Grades

# GET 1
# DELETE 1
# POST 1
# EDIT 0


################### GET ################
@app.route('/student/<int:studentID>/grade/api/get')
def grades(studentID):
    students = session.query(Student).filter_by(id=f'{studentID}').one()
    grade = session.query(Grade).filter_by(student_id=f'{studentID}')
    subjects = ["Math", "Arabic", "Science",
                "Biology", "Chemistry", "Physicsc", "History"]
    grades = []
    subIn = 0
    for r in grade:
        grades.append(f'{subjects[subIn], r.grade}')
        subIn = subIn+1
    # print()
    # return jsonify(students=students, grade=[ra.serialize for ra in grade])
    return json.dumps({'Name': students.name,
                       'grade': grades})


@app.route('/student/<int:student_id>/subject/api/get')
def studentSubjectJSON(student_id):
    student = session.query(Student).filter_by(id=student_id).one()
    items = session.query(Subject).filter_by(
        student=student_id).all()
    return jsonify(Subject=[i.serialize for i in items])


@app.route('/student/<int:student_id>/subject/<int:subject_id>/api/get')
def subjectJSON(student_id, subject_id):
    subject = session.query(Subject).filter_by(id=subject_id).one()
    return jsonify(subject=subject.serialize)


@app.route('/student_only/api/get')
def studentsOnlyJSON():
    students = session.query(Student).all()
    return jsonify(students=[r.serialize for r in students])

@app.route('/student/api/get')
def studentsJSON():
    all = {}
    students = session.query(Student)
    for x in students:
        grade = session.query(Grade).filter_by(student_id=f'{x.id}')
        subjects = ["Math", "Arabic", "Science",
                    "Biology", "Chemistry", "Physicsc", "History"]
        grades = []
        subIn = 0
        for r in grade:
            grades.append(f'{subjects[subIn], r.grade}')
            subIn = subIn+1
        
        all.update({x.name: grades})
    # print()
    # return jsonify(students=students, grade=[ra.serialize for ra in grade])
    return json.dumps(all)


################### DELETE ################
@app.route('/drop/database/api')
def deleteStudentsJSON():
    import os
    os.remove("./school.db")
    return json.dumps({'Database': "dropped"})


@app.route('/student/<int:student_id>/drop')
def dropStudent(student_id):
    student_name = session.query(Student).filter_by(id=f'{student_id}').one()
    student = session.query(Student).filter_by(id=student_id).delete()

    grade = session.query(Grade).filter_by(student_id=f'{student_id}')
    for r in grade:
        r.delete()
    return json.dumps({student_name.name: "dropped"})


@app.route('/subject/<int:subject_id>/drop')
def dropSubject(subject_id):
    subject = session.query(Subject).filter_by(id=subject_id).delete()
    if subject == 1:
        return json.dumps({"Dropped": "successfully"})
    else:
        return json.dumps({"Dropping": "faliled"})


################ POST #######################
@app.route('/student/<string:student_name>/api/post')
def postStudenet(student_name):
    stmt = (
        insert(Student).
        values(name=student_name))
    print(f"{student_name}")
    engine.execute(stmt)
    return json.dumps({f"{student_name}": "successfully"})



@app.route('/student/<string:student_name>/<string:subject_name>/<int:subject_id>/api/post')
def postGrade(student_name, subject_name ,subject_id):
    stmt = (
        update(Grade).
        where(subject_id == Grade.subject_id).
        values(name='user #5')
    )
    print(f"{student_name}")
    engine.execute(stmt)
    return json.dumps({f"{student_name}": "successfully"})


@app.route('/student/<string:subject_name>/api/post')
def postSubject(subject_name):
    stmt = (
        insert(Subject).
        values(name=subject_name))
    print(f"{subject_name}")
    engine.execute(stmt)
    return json.dumps({f"{subject_name}": "successfully"})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=9507)
