from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'Students'
    
    student_id = db.Column(db.String(20), primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    year_level = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    attendances = db.relationship('Attendance', backref='student', lazy=True, cascade='all, delete-orphan')

class Event(db.Model):
    __tablename__ = 'Events'
    
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    attendance_records = db.relationship('AttendanceRecord', backref='event', lazy=True, cascade='all, delete-orphan')

class AttendanceRecord(db.Model):
    __tablename__ = 'AttendanceRecords'
    
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_name = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('Events.event_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    attendances = db.relationship('Attendance', backref='attendance_record', lazy=True, cascade='all, delete-orphan')

class Attendance(db.Model):
    __tablename__ = 'Attendance'
    
    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id = db.Column(db.Integer, db.ForeignKey('AttendanceRecords.record_id'), nullable=False)
    student_id = db.Column(db.String(20), db.ForeignKey('Students.student_id'), nullable=False)
    student_fname = db.Column(db.String(50), nullable=False)
    student_year_level = db.Column(db.String(20), nullable=False)
    student_course = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum('Present', 'Absent', 'Excused'), default='Absent')
    timestamp = db.Column(db.DateTime, nullable=True)
    
    __table_args__ = (
        db.UniqueConstraint('record_id', 'student_id', name='unique_attendance'),
    )
