#!/usr/bin/env python3
"""
COMSOC Attendance System Launcher
Choose between Web and GUI versions
"""

import os
import sys
import subprocess

def print_banner():
    print("=" * 60)
    print("    COMSOC ATTENDANCE MANAGEMENT SYSTEM")
    print("=" * 60)
    print()

def print_menu():
    print("Choose your preferred version:")
    print("1. 🌐 Web Version (Recommended)")
    print("   - Modern web interface")
    print("   - Accessible from any device")
    print("   - Multi-user support")
    print()
    print("2. 🖥️  GUI Version")
    print("   - Native desktop application")
    print("   - Direct camera access")
    print("   - Offline operation")
    print()
    print("3. 📊 Database Setup")
    print("   - Set up database tables")
    print("   - Test database connection")
    print()
    print("4. ❌ Exit")
    print()

def run_web_version():
    print("Starting Web Version...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        # Change to web_version directory
        os.chdir('web_version')
        
        # Check if requirements are installed
        try:
            import flask
        except ImportError:
            print("Installing web version dependencies...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        # Run the web application
        subprocess.run([sys.executable, 'run_web.py'])
        
    except KeyboardInterrupt:
        print("\nWeb server stopped.")
    except Exception as e:
        print(f"Error starting web version: {e}")
        print("Please check the web_version/README_WEB.md for troubleshooting.")

def run_gui_version():
    print("Starting GUI Version...")
    print()
    
    try:
        # Change to gui_version directory
        os.chdir('gui_version')
        
        # Check if requirements are installed
        try:
            import PyQt5
        except ImportError:
            print("Installing GUI version dependencies...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        # Run the GUI application
        subprocess.run([sys.executable, 'run.py'])
        
    except Exception as e:
        print(f"Error starting GUI version: {e}")
        print("Please check the gui_version/README_GUI.md for troubleshooting.")

def setup_database():
    print("Setting up database...")
    print()
    
    try:
        # Run database setup
        subprocess.run([sys.executable, 'setup_database.py'])
        
        print("\nDatabase setup completed!")
        print("You can now run either version of the application.")
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        print("Please check README_MYSQL.md for manual setup instructions.")

def main():
    while True:
        print_banner()
        print_menu()
        
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                run_web_version()
                break
            elif choice == '2':
                run_gui_version()
                break
            elif choice == '3':
                setup_database()
                input("\nPress Enter to continue...")
            elif choice == '4':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == '__main__':
    main()
