from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from models import Student, db
from werkzeug.utils import secure_filename
import csv
import io
import qrcode
import os
from datetime import datetime

students_bp = Blueprint('students', __name__)

@students_bp.route('/')
def index():
    """Display all students"""
    students = Student.query.order_by(Student.student_id).all()
    return render_template('students/index.html', students=students)

@students_bp.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new student"""
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        fname = request.form.get('fname')
        year_level = request.form.get('year_level')
        course = request.form.get('course')
        
        if not all([student_id, fname, year_level, course]):
            flash('All fields are required', 'error')
            return redirect(url_for('students.add'))
        
        # Check if student already exists
        existing_student = Student.query.filter_by(student_id=student_id).first()
        if existing_student:
            flash('Student ID already exists', 'error')
            return redirect(url_for('students.add'))
        
        # Create new student
        new_student = Student(
            student_id=student_id,
            fname=fname,
            year_level=year_level,
            course=course
        )
        
        try:
            db.session.add(new_student)
            db.session.commit()
            flash('Student added successfully', 'success')
            return redirect(url_for('students.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {str(e)}', 'error')
            return redirect(url_for('students.add'))
    
    return render_template('students/add.html')

@students_bp.route('/edit/<student_id>', methods=['GET', 'POST'])
def edit(student_id):
    """Edit a student"""
    student = Student.query.filter_by(student_id=student_id).first_or_404()
    
    if request.method == 'POST':
        fname = request.form.get('fname')
        year_level = request.form.get('year_level')
        course = request.form.get('course')
        
        if not all([fname, year_level, course]):
            flash('All fields are required', 'error')
            return redirect(url_for('students.edit', student_id=student_id))
        
        try:
            student.fname = fname
            student.year_level = year_level
            student.course = course
            db.session.commit()
            flash('Student updated successfully', 'success')
            return redirect(url_for('students.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'error')
            return redirect(url_for('students.edit', student_id=student_id))
    
    return render_template('students/edit.html', student=student)

@students_bp.route('/delete/<student_id>', methods=['POST'])
def delete(student_id):
    """Delete a student"""
    student = Student.query.filter_by(student_id=student_id).first_or_404()
    
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'error')
    
    return redirect(url_for('students.index'))

@students_bp.route('/import', methods=['GET', 'POST'])
def import_csv():
    """Import students from CSV file"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('students.import_csv'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('students.import_csv'))
        
        if file and file.filename.endswith('.csv'):
            try:
                # Read CSV file
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_reader = csv.reader(stream)
                next(csv_reader)  # Skip header row
                
                imported_count = 0
                for row in csv_reader:
                    if len(row) >= 4:
                        student_id, fname, year_level, course = row[0], row[1], row[2], row[3]
                        
                        # Check if student already exists
                        existing_student = Student.query.filter_by(student_id=student_id).first()
                        if not existing_student:
                            new_student = Student(
                                student_id=student_id,
                                fname=fname,
                                year_level=year_level,
                                course=course
                            )
                            db.session.add(new_student)
                            imported_count += 1
                
                db.session.commit()
                flash(f'{imported_count} students imported successfully', 'success')
                return redirect(url_for('students.index'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Error importing CSV: {str(e)}', 'error')
                return redirect(url_for('students.import_csv'))
        else:
            flash('Please upload a valid CSV file', 'error')
            return redirect(url_for('students.import_csv'))
    
    return render_template('students/import.html')

@students_bp.route('/export')
def export_csv():
    """Export students to CSV file"""
    students = Student.query.order_by(Student.student_id).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Student ID', 'First Name', 'Year Level', 'Course'])
    
    for student in students:
        writer.writerow([student.student_id, student.fname, student.year_level, student.course])
    
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'students_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@students_bp.route('/qr-codes')
def generate_qr_codes():
    """Generate QR codes for all students"""
    students = Student.query.order_by(Student.student_id).all()
    
    # Create QR codes directory
    qr_dir = 'static/qr_codes'
    os.makedirs(qr_dir, exist_ok=True)
    
    generated_count = 0
    for student in students:
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(student.student_id)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save image
        img_path = os.path.join(qr_dir, f'{student.student_id}.png')
        img.save(img_path)
        generated_count += 1
    
    flash(f'{generated_count} QR codes generated successfully', 'success')
    return redirect(url_for('students.index'))

@students_bp.route('/search')
def search():
    """Search students"""
    query = request.args.get('q', '')
    if query:
        students = Student.query.filter(
            (Student.student_id.contains(query)) |
            (Student.fname.contains(query)) |
            (Student.year_level.contains(query)) |
            (Student.course.contains(query))
        ).order_by(Student.student_id).all()
    else:
        students = Student.query.order_by(Student.student_id).all()
    # If client expects JSON (web version fetch), return JSON list
    if 'application/json' in (request.headers.get('Accept') or ''):
        return jsonify({
            'success': True,
            'students': [
                {
                    'student_id': s.student_id,
                    'fname': s.fname,
                    'year_level': s.year_level,
                    'course': s.course
                } for s in students
            ]
        })
    return render_template('students/index.html', students=students, search_query=query)
