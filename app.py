from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import qrcode
import io
import base64
from werkzeug.utils import secure_filename
import csv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'comsoc_attendance')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import models first
from models import db, Student, Event, AttendanceRecord, Attendance

# Initialize database
db.init_app(app)

# Import blueprints
from blueprints.main import main_bp
from blueprints.students import students_bp
from blueprints.events import events_bp
from blueprints.attendance import attendance_bp
from blueprints.scanner import scanner_bp
from blueprints.reports import reports_bp

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(students_bp, url_prefix='/students')
app.register_blueprint(events_bp, url_prefix='/events')
app.register_blueprint(attendance_bp, url_prefix='/attendance')
app.register_blueprint(scanner_bp, url_prefix='/scanner')
app.register_blueprint(reports_bp, url_prefix='/reports')

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
