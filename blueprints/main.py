from flask import Blueprint, render_template, redirect, url_for
from models import Student, Event, AttendanceRecord, Attendance
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main dashboard page"""
    # Get statistics
    total_students = Student.query.count()
    total_events = Event.query.count()
    total_records = AttendanceRecord.query.count()
    
    # Get recent events
    recent_events = Event.query.order_by(Event.created_at.desc()).limit(5).all()
    
    # Get recent attendance records
    recent_records = AttendanceRecord.query.order_by(AttendanceRecord.created_at.desc()).limit(5).all()
    
    # Get attendance statistics for today
    today = datetime.now().date()
    today_attendance = Attendance.query.filter(
        Attendance.timestamp >= today
    ).count()
    
    return render_template('main/index.html',
                         total_students=total_students,
                         total_events=total_events,
                         total_records=total_records,
                         recent_events=recent_events,
                         recent_records=recent_records,
                         today_attendance=today_attendance)

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page with detailed statistics"""
    return redirect(url_for('main.index'))
