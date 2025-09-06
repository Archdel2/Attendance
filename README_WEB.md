# COMSOC Attendance System - Web Version

A modern web-based attendance management system built with Flask and SQLAlchemy, featuring QR code scanning, real-time attendance tracking, and comprehensive reporting.

## Features

### 🎯 Core Features
- **Student Management**: Add, edit, delete, and import students via CSV
- **Event Management**: Create and manage events with attendance records
- **QR Code Scanning**: Scan student QR codes for quick attendance marking
- **Real-time Attendance**: Mark attendance with Present/Absent/Excused status
- **Comprehensive Reports**: Generate and export attendance reports in CSV/Excel
- **Modern UI**: Responsive design with Bootstrap 5 and Font Awesome icons

### 🔧 Technical Features
- **Flask Blueprint Architecture**: Modular and scalable code structure
- **SQLAlchemy ORM**: Database abstraction with MySQL support
- **RESTful API**: JSON endpoints for AJAX functionality
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: Live attendance status updates

## Installation

### Prerequisites
- Python 3.8 or higher
- MySQL database server
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd Attendance
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database**
   - Create a MySQL database named `comsoc_attendance`
   - Copy `.env.example` to `.env` and update database credentials:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=comsoc_attendance
   DB_USER=your_username
   DB_PASSWORD=your_password
   SECRET_KEY=your-secret-key-here
   ```

4. **Run the application**
   ```bash
   python run_web.py
   ```

5. **Access the application**
   - Open your browser and go to: `http://localhost:5000`
   - The application will automatically create database tables on first run

## Usage Guide

### Dashboard
- View system statistics and recent activities
- Quick access to common functions
- Overview of total students, events, and attendance records

### Students Management
- **Add Students**: Individual student entry or bulk CSV import
- **Edit Students**: Update student information
- **Generate QR Codes**: Create QR codes for each student
- **Export Data**: Download student list as CSV

### Events Management
- **Create Events**: Set up new events with dates
- **Manage Records**: Create attendance records for each event
- **View Attendance**: See attendance data for specific events

### Attendance Tracking
- **QR Scanner**: Scan student QR codes for automatic attendance marking
- **Manual Entry**: Manually mark attendance for students
- **Quick Mark**: Bulk attendance marking interface
- **Real-time Updates**: Live status updates without page refresh

### Reports
- **Event Reports**: Comprehensive attendance reports for events
- **Record Reports**: Detailed attendance records
- **Export Options**: Download reports in CSV or Excel format
- **Summary Statistics**: Overall system statistics

## Project Structure

```
Attendance/
├── app.py                 # Main Flask application
├── models.py              # SQLAlchemy database models
├── run_web.py            # Web application launcher
├── requirements.txt      # Python dependencies
├── config.py             # Configuration settings
├── blueprints/           # Flask blueprints
│   ├── main.py          # Dashboard routes
│   ├── students.py      # Student management
│   ├── events.py        # Event management
│   ├── attendance.py    # Attendance tracking
│   ├── scanner.py       # QR code scanning
│   └── reports.py       # Report generation
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── main/            # Dashboard templates
│   ├── students/        # Student templates
│   ├── events/          # Event templates
│   ├── attendance/      # Attendance templates
│   ├── scanner/         # Scanner templates
│   └── reports/         # Report templates
└── static/              # Static files (CSS, JS, images)
```

## API Endpoints

### Students
- `GET /students/` - List all students
- `POST /students/add` - Add new student
- `GET /students/add` - Add student form
- `POST /students/edit/<id>` - Edit student
- `GET /students/edit/<id>` - Edit student form
- `POST /students/delete/<id>` - Delete student
- `GET /students/search` - Search students
- `POST /students/import` - Import CSV
- `GET /students/export` - Export CSV
- `GET /students/qr-codes` - Generate QR codes

### Events
- `GET /events/` - List all events
- `POST /events/add` - Add new event
- `GET /events/add` - Add event form
- `POST /events/edit/<id>` - Edit event
- `GET /events/edit/<id>` - Edit event form
- `POST /events/delete/<id>` - Delete event
- `GET /events/<id>/records` - View event records
- `POST /events/<id>/records/add` - Add attendance record
- `GET /events/<id>/attendance` - View event attendance

### Attendance
- `GET /attendance/` - List all records
- `GET /attendance/record/<id>` - View attendance record
- `POST /attendance/record/<id>/update` - Update attendance
- `POST /attendance/record/<id>/initialize` - Initialize record
- `POST /attendance/record/<id>/mark-present/<student_id>` - Mark present
- `POST /attendance/record/<id>/mark-absent/<student_id>` - Mark absent
- `POST /attendance/record/<id>/mark-excused/<student_id>` - Mark excused
- `POST /attendance/record/<id>/bulk-update` - Bulk update
- `GET /attendance/record/<id>/search` - Search attendance
- `GET /attendance/record/<id>/filter` - Filter attendance

### Scanner
- `GET /scanner/` - Scanner main page
- `GET /scanner/scan/<record_id>` - QR scanner
- `POST /scanner/process-qr` - Process QR code
- `GET /scanner/manual-entry/<record_id>` - Manual entry
- `POST /scanner/manual-entry/<record_id>` - Submit manual entry
- `GET /scanner/quick-mark/<record_id>` - Quick mark interface
- `POST /scanner/quick-mark/<record_id>/toggle/<student_id>` - Toggle attendance
- `POST /scanner/bulk-mark/<record_id>` - Bulk mark

### Reports
- `GET /reports/` - Reports main page
- `GET /reports/event/<id>` - Event report
- `GET /reports/record/<id>` - Record report
- `GET /reports/export/event/<id>/csv` - Export event CSV
- `GET /reports/export/record/<id>/csv` - Export record CSV
- `GET /reports/export/event/<id>/excel` - Export event Excel
- `GET /reports/export/record/<id>/excel` - Export record Excel
- `GET /reports/summary` - Summary report

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=comsoc_attendance
DB_USER=your_username
DB_PASSWORD=your_password

# Application Settings
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Database Schema
The application automatically creates the following tables:
- `students` - Student information
- `events` - Event details
- `attendance_records` - Attendance record sessions
- `attendance` - Individual attendance entries

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify MySQL server is running
   - Check database credentials in `.env` file
   - Ensure database `comsoc_attendance` exists

2. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **QR Code Issues**
   - Ensure camera permissions are granted
   - Check if `opencv-python` and `pyzbar` are installed

4. **Port Already in Use**
   - Change port in `run_web.py` or `app.py`
   - Kill existing process using port 5000

### Support
For issues and questions:
1. Check the troubleshooting section above
2. Review the application logs
3. Ensure all dependencies are properly installed

## Development

### Adding New Features
1. Create new blueprint in `blueprints/` directory
2. Add routes and templates
3. Register blueprint in `app.py`
4. Update navigation in `templates/base.html`

### Database Migrations
The application uses SQLAlchemy with automatic table creation. For production:
1. Use Flask-Migrate for database migrations
2. Set up proper database backup procedures
3. Configure production database settings

## License
This project is for educational and organizational use.
