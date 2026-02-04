import sys                                  # allows access to system-specific parameters and functions
from PyQt5.QtWidgets import QApplication    # imports the main Qt application class
from auth_window import AuthWindow          # imports the login (authentication) window
from main_window import MainWindow          # imports the main application window
from database import Database               # imports the database handling class

# Main application controller class
class EmergencyResponseApp:
    # Initialize the application
    def __init__(self):
        self.db = Database()      # create database connection
        self.current_user = None  # store logged-in user info
        self.auth_window = None   # login window placeholder
        self.main_window = None   # main window placeholder
    # Run the application
    def run(self):
        self.show_auth()  # start the app with login window

    # Show authentication window
    def show_auth(self):
        if self.main_window:          # close main window if open
            self.main_window.close()  # close main window
            self.main_window = None   # clear main window reference

        self.auth_window = AuthWindow() # create login window

        self.auth_window.login_success.connect(self.handle_login_success)  # connect login success signal
        
        self.auth_window.showMaximized() # show login window maximized

    # Login success handler
    def handle_login_success(self, user):
        self.current_user = user  # store logged-in user
        self.auth_window.close()  # close login window
        self.show_main_window()   # open main application window

    # Show main application window
    def show_main_window(self):
        self.main_window = MainWindow(self.current_user, self.db) # create main window with user and db info
        self.main_window.logout_signal.connect(
            self.handle_logout)  # connect logout signal
        self.main_window.show()  # show main application window
    
    # Logout handler
    def handle_logout(self):
        self.current_user = None  # clear current user info
        self.show_auth()          # return to login window

if __name__ == '__main__':
    app = QApplication(sys.argv)  # create Qt application

    # Set application style
    app.setStyle('Fusion')  # set UI theme

    emergency_app = EmergencyResponseApp()  # create app controller
    emergency_app.run()  # start the application

    sys.exit(app.exec_())   # run event loop and exit properly
    
