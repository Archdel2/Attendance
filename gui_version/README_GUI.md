# COMSOC Attendance System - GUI Version

A desktop attendance management system built with PyQt5, featuring QR code scanning, real-time attendance tracking, and comprehensive reporting.

## Features

### 🎯 Core Features
- **Student Management**: Add, edit, delete, and import students via CSV
- **Event Management**: Create and manage events with attendance records
- **QR Code Scanning**: Scan student QR codes for quick attendance marking
- **Real-time Attendance**: Mark attendance with Present/Absent/Excused status
- **Comprehensive Reports**: Generate and export attendance reports
- **Modern UI**: Clean, intuitive interface with PyQt5

### 🔧 Technical Features
- **Native Desktop App**: Fast and responsive performance
- **Offline Operation**: Works without internet connection
- **Camera Integration**: Direct camera access for QR scanning
- **System Integration**: Native file dialogs and system notifications
- **High Performance**: Optimized for desktop use

## Installation

### Prerequisites
- Python 3.8 or higher
- MySQL database server
- Camera (for QR code scanning)
- pip (Python package manager)

### Setup Instructions

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure database**
   - Create a MySQL database named `comsoc_attendance`
   - Copy `config.py` and update database credentials:
   ```python
   DB_HOST = 'localhost'
   DB_PORT = 3306
   DB_NAME = 'comsoc_attendance'
   DB_USER = 'your_username'
   DB_PASSWORD = 'your_password'
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

## Usage Guide

### Main Menu
- **View Events**: Access event management
- **View Masterlist**: View student database
- **QR Scanner**: Access camera-based QR code scanning

### Student Management
- **Add Students**: Individual student entry or bulk CSV import
- **Edit Students**: Update student information
- **Generate QR Codes**: Create QR codes for each student
- **Export Data**: Download student list as CSV

### Event Management
- **Create Events**: Set up new events with dates
- **Manage Records**: Create attendance records for each event
- **View Attendance**: See attendance data for specific events

### Attendance Tracking
- **QR Scanner**: Scan student QR codes for automatic attendance marking
- **Manual Entry**: Manually mark attendance for students
- **Real-time Updates**: Live status updates in the interface

### QR Code Scanner
- **Camera Access**: Direct camera integration for QR scanning
- **Automatic Marking**: Scans automatically mark students as present
- **Real-time Feedback**: Immediate status updates and notifications

## Project Structure

```
gui_version/
├── main_app.py          # Main GUI application
├── run.py              # Application launcher
├── database.py         # Database operations
├── ui_pages.py         # UI components
├── camera_scanner.py   # QR code scanning
├── requirements.txt    # Python dependencies
├── config.py          # Configuration settings
└── README_GUI.md      # This file
```

## Configuration

### Database Settings
Edit `config.py` to configure:
- MySQL database connection settings
- Application dimensions and camera settings
- UI styling preferences

### Camera Settings
- **Camera Index**: Set the default camera (usually 0)
- **Resolution**: Configure camera resolution for optimal scanning
- **Update Interval**: Set camera frame update frequency

## Dependencies

- **PyQt5**: GUI framework
- **OpenCV**: Camera operations and image processing
- **pyzbar**: QR code decoding
- **NumPy**: Numerical operations
- **PyMySQL**: MySQL database connectivity
- **python-dotenv**: Environment variable management
- **openpyxl**: Excel file operations

## Troubleshooting

### Database Issues
- Run `test_db_connection.py` to verify MySQL connection
- Check MySQL server is running
- Verify database permissions and credentials
- Ensure database `comsoc_attendance` exists

### Camera Issues
- Ensure camera is not in use by other applications
- Check camera permissions
- Verify OpenCV installation
- Try different camera index in config.py

### Import Errors
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python path and module locations
- Ensure PyQt5 is properly installed

### Performance Issues
- Close other applications using the camera
- Reduce camera resolution if needed
- Check system resources

## Development

### Adding New Features
1. Add UI components in `ui_pages.py`
2. Update main application logic in `main_app.py`
3. Add database operations in `database.py` if needed
4. Test thoroughly with different scenarios

### UI Customization
- Modify styles in `config.py`
- Update UI layouts in `ui_pages.py`
- Add new pages by extending existing UI components

### Database Operations
- Add new queries in `database.py`
- Follow existing patterns for consistency
- Test with sample data

## Migration from Web Version

The GUI version shares the same database schema as the web version:
1. Both versions use the same MySQL database
2. Data created in one version is immediately available in the other
3. No data migration required

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the application logs
3. Ensure all dependencies are properly installed
4. Test database connection separately

## License

This project is for educational and organizational use.
