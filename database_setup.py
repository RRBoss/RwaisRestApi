import os, sys
from re import T
from sqlalchemy import Column, ForeignKey, Integer, String, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Grade(Base):
    __tablename__ = 'grade'


    id = Column(Integer, primary_key=True)
    grade = Column(Integer)

    student_id = Column(Integer, ForeignKey('student.id'))

    subject_id = Column(Integer, ForeignKey('subject.id'))




    @property
    def serialize(self):
        # Return object data in easily serializealbe format
        return {
            'id': self.id,
            'grade': self.grade,
        }

class Student(Base):
    __tablename__ = 'student'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    relationship('subject', secondary=Grade, backref='student')

    @property
    def serialize(self):
        # Return object data in easily serializeable format
        return {
            'id': self.id,
            'name': self.name,  
        }


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    name  = Column(String(80), nullable=False)
    relationship('student', secondary=Grade, backref='subject')

    @property
    def serialize(self):
        # Return object data in easily serializealbe format
        return {
            'id': self.id,
            'name': self.name,
        }
    



engine = create_engine('sqlite:///school.db')
Base.metadata.create_all(engine)