from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from models import Student, db
from werkzeug.utils import secure_filename
import csv
import io
import os
from datetime import datetime
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw

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
    """Generate QR codes for all students, organized by course and year level"""
    students = Student.query.order_by(Student.student_id).all()
    
    # Base directory for QR codes
    base_qr_dir = 'static/qr_codes'
    os.makedirs(base_qr_dir, exist_ok=True)
    logo_path = os.path.join('web_version/static', 'logo.png')
    
    generated_count = 0
    for student in students:
        # Create course directory if it doesn't exist
        course_dir = os.path.join(base_qr_dir, student.course)
        os.makedirs(course_dir, exist_ok=True)
        
        # Create year level directory inside course directory
        year_dir = os.path.join(course_dir, f"Year_{student.year_level}")
        os.makedirs(year_dir, exist_ok=True)
        
        # Generate QR code with high error correction to allow center logo
        # Use a higher fixed version and larger quiet zone to keep large center logo scannable
        qr = qrcode.QRCode(
            version=10,  # higher module count accommodates 30% center cutout
            error_correction=ERROR_CORRECT_H,
            box_size=10,
            border=6,    # larger quiet zone improves scanner detection
        )
        qr.add_data(student.student_id)
        qr.make(fit=False)

        # Create base QR image (RGB)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Overlay logo at center if available
        try:
            if os.path.exists(logo_path):
                logo = Image.open(logo_path).convert("RGBA")

                # Compute logo size: ~30% of QR width (bigger logo)
                qr_width, qr_height = img.size
                target_logo_width = int(qr_width * 0.30)
                aspect = logo.width / logo.height if logo.height else 1
                new_logo_width = target_logo_width
                new_logo_height = int(target_logo_width / aspect)
                logo = logo.resize((new_logo_width, new_logo_height), Image.LANCZOS)

                # Small white margin cutout around the logo to improve readability (smaller than before)
                margin = max(2, qr_width // 200)
                cutout_left = (qr_width - new_logo_width) // 2 - margin
                cutout_top = (qr_height - new_logo_height) // 2 - margin
                cutout_right = cutout_left + new_logo_width + margin * 2
                cutout_bottom = cutout_top + new_logo_height + margin * 2

                draw = ImageDraw.Draw(img)
                try:
                    draw.rounded_rectangle(
                        [(cutout_left, cutout_top), (cutout_right, cutout_bottom)],
                        radius=max(2, new_logo_width // 20),
                        fill=(255, 255, 255)
                    )
                except Exception:
                    draw.rectangle(
                        [(cutout_left, cutout_top), (cutout_right, cutout_bottom)],
                        fill=(255, 255, 255)
                    )

                # Compute position to center the logo and paste
                pos = (
                    (qr_width - new_logo_width) // 2,
                    (qr_height - new_logo_height) // 2,
                )

                img.paste(logo, pos, mask=logo)
        except Exception as e:
            # If anything fails, proceed with plain QR to avoid interrupting generation
            pass

        # Save image in the appropriate course/year directory
        img_path = os.path.join(year_dir, f'{student.student_id}.png')
        img.save(img_path, format='PNG')
        generated_count += 1
    
    flash(f'{generated_count} QR codes generated successfully and organized by course/year level', 'success')
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
    
    return render_template('students/index.html', students=students, search_query=query)
