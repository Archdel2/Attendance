from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import Student, AttendanceRecord, Attendance, db
from datetime import datetime
import cv2
import numpy as np
from pyzbar import pyzbar
import base64
import os

scanner_bp = Blueprint('scanner', __name__)

@scanner_bp.route('/')
def index():
    """Scanner main page"""
    records = AttendanceRecord.query.order_by(AttendanceRecord.created_at.desc()).all()
    return render_template('scanner/index.html', records=records)

@scanner_bp.route('/scan/<int:record_id>')
def scan(record_id):
    """QR code scanner page for a specific record"""
    record = AttendanceRecord.query.get_or_404(record_id)
    return render_template('scanner/scan.html', record=record)

@scanner_bp.route('/process-qr', methods=['POST'])
def process_qr():
    """Process scanned QR code"""
    data = request.get_json()
    qr_data = data.get('qr_data')
    record_id = data.get('record_id')
    
    if not qr_data or not record_id:
        return jsonify({'success': False, 'message': 'Missing QR data or record ID'})
    
    # Find student by student ID
    student = Student.query.filter_by(student_id=qr_data).first()
    
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'})
    
    # Find or create attendance record
    attendance = Attendance.query.filter_by(record_id=record_id, student_id=qr_data).first()
    
    if not attendance:
        # Create new attendance record
        attendance = Attendance(
            record_id=record_id,
            student_id=student.student_id,
            student_fname=student.fname,
            student_year_level=student.year_level,
            student_course=student.course,
            status='Present',
            timestamp=datetime.now()
        )
        db.session.add(attendance)
    else:
        # Update existing attendance
        attendance.status = 'Present'
        attendance.timestamp = datetime.now()
    
    try:
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': f'Attendance recorded for {student.fname}',
            'student': {
                'id': student.student_id,
                'name': student.fname,
                'year_level': student.year_level,
                'course': student.course
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error recording attendance: {str(e)}'})

@scanner_bp.route('/manual-entry/<int:record_id>', methods=['GET', 'POST'])
def manual_entry(record_id):
    """Manual attendance entry"""
    record = AttendanceRecord.query.get_or_404(record_id)
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        
        if not student_id:
            flash('Student ID is required', 'error')
            return redirect(url_for('scanner.manual_entry', record_id=record_id))
        
        # Find student
        student = Student.query.filter_by(student_id=student_id).first()
        
        if not student:
            flash('Student not found', 'error')
            return redirect(url_for('scanner.manual_entry', record_id=record_id))
        
        # Find or create attendance record
        attendance = Attendance.query.filter_by(record_id=record_id, student_id=student_id).first()
        
        if not attendance:
            # Create new attendance record
            attendance = Attendance(
                record_id=record_id,
                student_id=student.student_id,
                student_fname=student.fname,
                student_year_level=student.year_level,
                student_course=student.course,
                status='Present',
                timestamp=datetime.now()
            )
            db.session.add(attendance)
        else:
            # Update existing attendance
            attendance.status = 'Present'
            attendance.timestamp = datetime.now()
        
        try:
            db.session.commit()
            flash(f'Attendance recorded for {student.fname}', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error recording attendance: {str(e)}', 'error')
        
        return redirect(url_for('scanner.manual_entry', record_id=record_id))
    
    # Get students for dropdown
    students = Student.query.order_by(Student.student_id).all()
    return render_template('scanner/manual_entry.html', record=record, students=students)

@scanner_bp.route('/quick-mark/<int:record_id>')
def quick_mark(record_id):
    """Quick mark attendance page"""
    record = AttendanceRecord.query.get_or_404(record_id)
    attendances = Attendance.query.filter_by(record_id=record_id).order_by(Attendance.student_id).all()
    
    return render_template('scanner/quick_mark.html', record=record, attendances=attendances)

@scanner_bp.route('/quick-mark/<int:record_id>/toggle/<student_id>', methods=['POST'])
def toggle_attendance(record_id, student_id):
    """Toggle attendance status for quick marking"""
    attendance = Attendance.query.filter_by(record_id=record_id, student_id=student_id).first_or_404()
    
    try:
        if attendance.status == 'Present':
            attendance.status = 'Absent'
            attendance.timestamp = None
        else:
            attendance.status = 'Present'
            attendance.timestamp = datetime.now()
        
        db.session.commit()
        return jsonify({
            'success': True, 
            'status': attendance.status,
            'timestamp': attendance.timestamp.isoformat() if attendance.timestamp else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error updating attendance: {str(e)}'})

@scanner_bp.route('/bulk-mark/<int:record_id>', methods=['POST'])
def bulk_mark(record_id):
    """Bulk mark attendance"""
    record = AttendanceRecord.query.get_or_404(record_id)
    action = request.form.get('action')
    
    if action not in ['mark_all_present', 'mark_all_absent']:
        flash('Invalid action', 'error')
        return redirect(url_for('scanner.quick_mark', record_id=record_id))
    
    attendances = Attendance.query.filter_by(record_id=record_id).all()
    
    try:
        for attendance in attendances:
            if action == 'mark_all_present':
                attendance.status = 'Present'
                attendance.timestamp = datetime.now()
            else:
                attendance.status = 'Absent'
                attendance.timestamp = None
        
        db.session.commit()
        flash(f'All students marked as {action.split("_")[-1]}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error during bulk marking: {str(e)}', 'error')
    
    return redirect(url_for('scanner.quick_mark', record_id=record_id))
