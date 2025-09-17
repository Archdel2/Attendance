from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import AttendanceRecord, Attendance, Student, db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/')
def index():
    """Display all attendance records"""
    records = AttendanceRecord.query.order_by(AttendanceRecord.created_at.desc()).all()
    return render_template('attendance/index.html', records=records)

@attendance_bp.route('/record/<int:record_id>')
def view_record(record_id):
    """View attendance for a specific record"""
    record = AttendanceRecord.query.get_or_404(record_id)
    attendances = Attendance.query.filter_by(record_id=record_id).order_by(Attendance.student_id).all()
    
    return render_template('attendance/view_record.html', record=record, attendances=attendances)

@attendance_bp.route('/record/<int:record_id>/update', methods=['POST'])
def update_attendance(record_id):
    """Update attendance status for a student"""
    record = AttendanceRecord.query.get_or_404(record_id)
    # Support both JSON payloads and form submissions
    if request.is_json:
        data = request.get_json(silent=True) or {}
        student_id = data.get('student_id')
        status = data.get('status')
    else:
        student_id = request.form.get('student_id')
        status = request.form.get('status')
    
    if not all([student_id, status]):
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    attendance = Attendance.query.filter_by(record_id=record_id, student_id=student_id).first()
    
    if not attendance:
        return jsonify({'success': False, 'message': 'Attendance record not found'})
    
    try:
        attendance.status = status
        if status == 'Present':
            attendance.timestamp = datetime.now()
        db.session.commit()
        return jsonify({'success': True, 'message': 'Attendance updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error updating attendance: {str(e)}'})

@attendance_bp.route('/record/<int:record_id>/initialize', methods=['POST'])
def initialize_record(record_id):
    """Initialize attendance record with all students"""
    record = AttendanceRecord.query.get_or_404(record_id)
    
    # Get all students
    students = Student.query.all()
    
    try:
        for student in students:
            # Check if attendance record already exists
            existing_attendance = Attendance.query.filter_by(
                record_id=record_id, 
                student_id=student.student_id
            ).first()
            
            if not existing_attendance:
                # Create attendance record for this student
                new_attendance = Attendance(
                    record_id=record_id,
                    student_id=student.student_id,
                    student_fname=student.fname,
                    student_year_level=student.year_level,
                    student_course=student.course,
                    status='Absent'
                )
                db.session.add(new_attendance)
        
        db.session.commit()
        # Return JSON if requested by fetch (web version), otherwise flash+redirect
        if 'application/json' in (request.headers.get('Accept') or ''):
            return jsonify({'success': True, 'message': 'Attendance record initialized with all students'})
        flash('Attendance record initialized with all students', 'success')
    except Exception as e:
        db.session.rollback()
        if 'application/json' in (request.headers.get('Accept') or ''):
            return jsonify({'success': False, 'message': f'Error initializing attendance record: {str(e)}'})
        flash(f'Error initializing attendance record: {str(e)}', 'error')
    
    return redirect(url_for('attendance.view_record', record_id=record_id))

@attendance_bp.route('/record/<int:record_id>/mark-present/<student_id>', methods=['POST'])
def mark_present(record_id, student_id):
    """Mark a student as present"""
    attendance = Attendance.query.filter_by(record_id=record_id, student_id=student_id).first_or_404()
    
    try:
        attendance.status = 'Present'
        attendance.timestamp = datetime.now()
        db.session.commit()
        return jsonify({'success': True, 'message': 'Student marked as present'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error marking student as present: {str(e)}'})

@attendance_bp.route('/record/<int:record_id>/mark-absent/<student_id>', methods=['POST'])
def mark_absent(record_id, student_id):
    """Mark a student as absent"""
    attendance = Attendance.query.filter_by(record_id=record_id, student_id=student_id).first_or_404()
    
    try:
        attendance.status = 'Absent'
        attendance.timestamp = None
        db.session.commit()
        return jsonify({'success': True, 'message': 'Student marked as absent'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error marking student as absent: {str(e)}'})

@attendance_bp.route('/record/<int:record_id>/mark-excused/<student_id>', methods=['POST'])
def mark_excused(record_id, student_id):
    """Mark a student as excused"""
    attendance = Attendance.query.filter_by(record_id=record_id, student_id=student_id).first_or_404()
    
    try:
        attendance.status = 'Excused'
        attendance.timestamp = datetime.now()
        db.session.commit()
        return jsonify({'success': True, 'message': 'Student marked as excused'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error marking student as excused: {str(e)}'})

@attendance_bp.route('/record/<int:record_id>/bulk-update', methods=['POST'])
def bulk_update(record_id):
    """Bulk update attendance status"""
    record = AttendanceRecord.query.get_or_404(record_id)
    data = request.get_json(silent=True) or {}
    updates = data.get('updates', [])
    # Also support a single-status bulk update used by web_version quick_mark
    single_status = data.get('status')
    
    try:
        if single_status:
            # Update all attendances for this record to the given status
            for attendance in Attendance.query.filter_by(record_id=record_id).all():
                attendance.status = single_status
                if single_status == 'Present':
                    attendance.timestamp = datetime.now()
                elif single_status == 'Absent':
                    attendance.timestamp = None
                else:
                    attendance.timestamp = datetime.now()
        else:
            for update in updates:
                student_id = update.get('student_id')
                status = update.get('status')
                
                if student_id and status:
                    attendance = Attendance.query.filter_by(record_id=record_id, student_id=student_id).first()
                    if attendance:
                        attendance.status = status
                        if status == 'Present':
                            attendance.timestamp = datetime.now()
                        elif status == 'Absent':
                            attendance.timestamp = None
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Bulk update completed successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error during bulk update: {str(e)}'})

@attendance_bp.route('/record/<int:record_id>/search')
def search_attendance(record_id):
    """Search attendance records"""
    record = AttendanceRecord.query.get_or_404(record_id)
    query = request.args.get('q', '')
    
    if query:
        attendances = Attendance.query.filter(
            Attendance.record_id == record_id,
            (Attendance.student_id.contains(query)) |
            (Attendance.student_fname.contains(query)) |
            (Attendance.student_year_level.contains(query)) |
            (Attendance.student_course.contains(query))
        ).order_by(Attendance.student_id).all()
    else:
        attendances = Attendance.query.filter_by(record_id=record_id).order_by(Attendance.student_id).all()
    
    return render_template('attendance/view_record.html', record=record, attendances=attendances, search_query=query)

@attendance_bp.route('/record/<int:record_id>/filter')
def filter_attendance(record_id):
    """Filter attendance records by status"""
    record = AttendanceRecord.query.get_or_404(record_id)
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'all':
        attendances = Attendance.query.filter_by(record_id=record_id).order_by(Attendance.student_id).all()
    else:
        attendances = Attendance.query.filter_by(record_id=record_id, status=status_filter).order_by(Attendance.student_id).all()
    
    return render_template('attendance/view_record.html', record=record, attendances=attendances, status_filter=status_filter)

@attendance_bp.route('/record/<int:record_id>/students')
def get_students_for_record(record_id):
    """Return JSON list of students for a record with current attendance status (web version helper)."""
    record = AttendanceRecord.query.get_or_404(record_id)
    attendances = Attendance.query.filter_by(record_id=record_id).order_by(Attendance.student_id).all()
    students = [{
        'student_id': a.student_id,
        'student_fname': a.student_fname,
        'student_year_level': a.student_year_level,
        'student_course': a.student_course,
        'status': a.status
    } for a in attendances]
    return jsonify({'success': True, 'record_id': record.record_id, 'students': students})

    except Exception as e:

        db.session.rollback()

        return jsonify({'success': False, 'message': f'Error marking student as present: {str(e)}'})



@attendance_bp.route('/record/<int:record_id>/mark-absent/<student_id>', methods=['POST'])

def mark_absent(record_id, student_id):

    """Mark a student as absent"""

    attendance = Attendance.query.filter_by(record_id=record_id, student_id=student_id).first_or_404()

    

    try:

        attendance.status = 'Absent'

        attendance.timestamp = None

        db.session.commit()

        return jsonify({'success': True, 'message': 'Student marked as absent'})

    except Exception as e:

        db.session.rollback()

        return jsonify({'success': False, 'message': f'Error marking student as absent: {str(e)}'})



@attendance_bp.route('/record/<int:record_id>/mark-excused/<student_id>', methods=['POST'])

def mark_excused(record_id, student_id):

    """Mark a student as excused"""

    attendance = Attendance.query.filter_by(record_id=record_id, student_id=student_id).first_or_404()

    

    try:

        attendance.status = 'Excused'

        attendance.timestamp = datetime.now()

        db.session.commit()

        return jsonify({'success': True, 'message': 'Student marked as excused'})

    except Exception as e:

        db.session.rollback()

        return jsonify({'success': False, 'message': f'Error marking student as excused: {str(e)}'})



@attendance_bp.route('/record/<int:record_id>/bulk-update', methods=['POST'])

def bulk_update(record_id):

    """Bulk update attendance status"""

    record = AttendanceRecord.query.get_or_404(record_id)

    updates = request.json.get('updates', [])

    

    try:

        for update in updates:

            student_id = update.get('student_id')

            status = update.get('status')

            

            if student_id and status:

                attendance = Attendance.query.filter_by(record_id=record_id, student_id=student_id).first()

                if attendance:

                    attendance.status = status

                    if status == 'Present':

                        attendance.timestamp = datetime.now()

                    elif status == 'Absent':

                        attendance.timestamp = None

        

        db.session.commit()

        return jsonify({'success': True, 'message': 'Bulk update completed successfully'})

    except Exception as e:

        db.session.rollback()

        return jsonify({'success': False, 'message': f'Error during bulk update: {str(e)}'})



@attendance_bp.route('/record/<int:record_id>/search')

def search_attendance(record_id):

    """Search attendance records"""

    record = AttendanceRecord.query.get_or_404(record_id)

    query = request.args.get('q', '')

    

    if query:

        attendances = Attendance.query.filter(

            Attendance.record_id == record_id,

            (Attendance.student_id.contains(query)) |

            (Attendance.student_fname.contains(query)) |

            (Attendance.student_year_level.contains(query)) |

            (Attendance.student_course.contains(query))

        ).order_by(Attendance.student_id).all()

    else:

        attendances = Attendance.query.filter_by(record_id=record_id).order_by(Attendance.student_id).all()

    

    return render_template('attendance/view_record.html', record=record, attendances=attendances, search_query=query)



@attendance_bp.route('/record/<int:record_id>/filter')

def filter_attendance(record_id):

    """Filter attendance records by status"""

    record = AttendanceRecord.query.get_or_404(record_id)

    status_filter = request.args.get('status', 'all')

    

    if status_filter == 'all':

        attendances = Attendance.query.filter_by(record_id=record_id).order_by(Attendance.student_id).all()

    else:

        attendances = Attendance.query.filter_by(record_id=record_id, status=status_filter).order_by(Attendance.student_id).all()

    

    return render_template('attendance/view_record.html', record=record, attendances=attendances, status_filter=status_filter)


