from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import Event, AttendanceRecord, db
from datetime import datetime

events_bp = Blueprint('events', __name__)

@events_bp.route('/')
def index():
    """Display all events"""
    events = Event.query.order_by(Event.created_at.desc()).all()
    return render_template('events/index.html', events=events)

@events_bp.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new event"""
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        event_date = request.form.get('event_date')
        
        if not event_name:
            flash('Event name is required', 'error')
            return redirect(url_for('events.add'))
        
        if not event_date:
            event_date = datetime.now().date()
        else:
            try:
                event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format', 'error')
                return redirect(url_for('events.add'))
        
        # Create new event
        new_event = Event(
            event_name=event_name,
            event_date=event_date
        )
        
        try:
            db.session.add(new_event)
            db.session.commit()
            flash('Event created successfully', 'success')
            return redirect(url_for('events.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating event: {str(e)}', 'error')
            return redirect(url_for('events.add'))
    
    return render_template('events/add.html')

@events_bp.route('/edit/<int:event_id>', methods=['GET', 'POST'])
def edit(event_id):
    """Edit an event"""
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        event_date = request.form.get('event_date')
        
        if not event_name:
            flash('Event name is required', 'error')
            return redirect(url_for('events.edit', event_id=event_id))
        
        if event_date:
            try:
                event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format', 'error')
                return redirect(url_for('events.edit', event_id=event_id))
        else:
            event_date = event.event_date
        
        try:
            event.event_name = event_name
            event.event_date = event_date
            db.session.commit()
            flash('Event updated successfully', 'success')
            return redirect(url_for('events.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating event: {str(e)}', 'error')
            return redirect(url_for('events.edit', event_id=event_id))
    
    return render_template('events/edit.html', event=event)

@events_bp.route('/delete/<int:event_id>', methods=['POST'])
def delete(event_id):
    """Delete an event"""
    event = Event.query.get_or_404(event_id)
    
    try:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting event: {str(e)}', 'error')
    
    return redirect(url_for('events.index'))

@events_bp.route('/<int:event_id>/records')
def records(event_id):
    """View attendance records for an event"""
    event = Event.query.get_or_404(event_id)
    records = AttendanceRecord.query.filter_by(event_id=event_id).order_by(AttendanceRecord.created_at.desc()).all()
    
    return render_template('events/records.html', event=event, records=records)

@events_bp.route('/<int:event_id>/records/add', methods=['POST'])
def add_record(event_id):
    """Add a new attendance record for an event"""
    event = Event.query.get_or_404(event_id)
    record_name = request.form.get('record_name')
    
    if not record_name:
        flash('Record name is required', 'error')
        return redirect(url_for('events.records', event_id=event_id))
    
    # Create new attendance record
    new_record = AttendanceRecord(
        record_name=record_name,
        event_id=event_id
    )
    
    try:
        db.session.add(new_record)
        db.session.commit()
        flash('Attendance record created successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating attendance record: {str(e)}', 'error')
    
    return redirect(url_for('events.records', event_id=event_id))

@events_bp.route('/<int:event_id>/attendance')
def attendance(event_id):
    """View attendance for an event"""
    event = Event.query.get_or_404(event_id)
    
    # Get all attendance records for this event
    records = AttendanceRecord.query.filter_by(event_id=event_id).all()
    
    # Get attendance data from all records
    attendance_data = []
    for record in records:
        attendances = record.attendances
        for attendance in attendances:
            attendance_data.append({
                'student_id': attendance.student_id,
                'student_fname': attendance.student_fname,
                'student_year_level': attendance.student_year_level,
                'student_course': attendance.student_course,
                'status': attendance.status,
                'timestamp': attendance.timestamp,
                'record_name': record.record_name
            })
    
    return render_template('events/attendance.html', event=event, attendance_data=attendance_data)
