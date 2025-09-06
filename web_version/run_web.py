#!/usr/bin/env python3
"""
Web application launcher for the Attendance Management System
"""

import sys
import os

# Add the current directory to Python path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("Starting COMSOC Attendance Web Application...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error starting web application: {e}")
    sys.exit(1)
