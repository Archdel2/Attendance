# COMSOC Attendance Management System

A comprehensive attendance management system with both **Desktop GUI** and **Web** versions, built with Python.

## 🎯 Project Overview

This project provides two different implementations of the same attendance management system:

- **GUI Version**: Desktop application built with PyQt5
- **Web Version**: Web application built with Flask

Both versions share the same database schema and core functionality, but offer different user interfaces and deployment options.

## 📁 Project Structure

```
Attendance/
├── web_version/           # Flask web application
│   ├── app.py            # Main Flask application
│   ├── models.py         # SQLAlchemy database models
│   ├── run_web.py        # Web application launcher
│   ├── requirements.txt  # Web dependencies
│   ├── config.py         # Web configuration
│   ├── blueprints/       # Flask blueprints
│   ├── templates/        # HTML templates
│   └── README_WEB.md     # Web version documentation
├── gui_version/          # PyQt5 desktop application
│   ├── main_app.py       # Main GUI application
│   ├── run.py           # GUI application launcher
│   ├── database.py      # Database operations
│   ├── ui_pages.py      # UI components
│   ├── camera_scanner.py # QR code scanning
│   ├── requirements.txt  # GUI dependencies
│   ├── config.py        # GUI configuration
│   └── README_GUI.md    # GUI version documentation
├── setup_database.py     # Database setup script
├── test_db_connection.py # Database connection test
├── config.py            # Shared configuration
├── requirements.txt     # Combined dependencies
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL database server
- pip (Python package manager)

### Database Setup
1. Create a MySQL database named `comsoc_attendance`
2. Run the database setup script:
   ```bash
   python setup_database.py
   ```

### Choose Your Version

#### 🚀 Easy Launcher (Recommended)
```bash
python launcher.py
```
This will show you a menu to choose between versions and handle setup automatically.

#### 🌐 Web Version (Manual)
```bash
cd web_version
pip install -r requirements.txt
python run_web.py
```
Access at: `http://localhost:5000`

#### 🖥️ GUI Version (Manual)
```bash
cd gui_version
pip install -r requirements.txt
python run.py
```

## 🔧 Features

### Core Features (Both Versions)
- **Student Management**: Add, edit, delete, import/export students
- **Event Management**: Create and manage events
- **QR Code Scanning**: Scan student QR codes for attendance
- **Attendance Tracking**: Mark Present/Absent/Excused status
- **Reporting**: Generate attendance reports
- **Data Export**: Export to CSV and Excel formats

### Web Version Features
- **Modern Web UI**: Responsive design with Bootstrap 5
- **Multi-user Access**: Multiple users can access simultaneously
- **Mobile Friendly**: Works on phones and tablets
- **Real-time Updates**: Live attendance tracking
- **RESTful API**: JSON endpoints for AJAX functionality
- **Easy Deployment**: Can be hosted on any web server

### GUI Version Features
- **Native Desktop App**: Fast and responsive
- **Offline Operation**: Works without internet connection
- **Camera Integration**: Direct camera access for QR scanning
- **System Integration**: Native file dialogs and system notifications
- **High Performance**: Optimized for desktop use

## 📊 Database Schema

Both versions use the same MySQL database with these tables:
- `students` - Student information
- `events` - Event details
- `attendance_records` - Attendance record sessions
- `attendance` - Individual attendance entries

## 🔄 Migration Between Versions

You can switch between versions seamlessly:
1. Both versions use the same database
2. Data created in one version is immediately available in the other
3. No data migration required

## 🛠️ Development

### Adding Features
- **Web Version**: Add routes in blueprints and create HTML templates
- **GUI Version**: Add UI components in ui_pages.py and update main_app.py

### Configuration
- Edit `config.py` in each version folder for version-specific settings
- Database settings are shared via the root `config.py`

## 📝 Documentation

- **Web Version**: See `web_version/README_WEB.md`
- **GUI Version**: See `gui_version/README_GUI.md`
- **Database**: See `README_MYSQL.md`

## 🤝 Contributing

1. Choose the version you want to work on
2. Follow the specific documentation for that version
3. Test both versions to ensure compatibility
4. Update both README files if adding new features

## 📄 License

This project is for educational and organizational use.

## 🆘 Support

- **Web Issues**: Check `web_version/README_WEB.md`
- **GUI Issues**: Check `gui_version/README_GUI.md`
- **Database Issues**: Check `README_MYSQL.md`
- **General Issues**: Check this README first
