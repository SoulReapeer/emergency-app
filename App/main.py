import sys
from PyQt5.QtWidgets import QApplication
from auth_window import AuthWindow
from main_window import MainWindow
from database import Database


class EmergencyResponseApp:
    def __init__(self):
        self.db = Database()
        self.current_user = None
        self.auth_window = None
        self.main_window = None
        
    def run(self):
        self.show_auth()
        
    def show_auth(self):
        if self.main_window:
            self.main_window.close()
            self.main_window = None
            
        self.auth_window = AuthWindow()
        self.auth_window.login_success.connect(self.handle_login_success)
        self.auth_window.showMaximized()
        
    def handle_login_success(self, user):
        self.current_user = user
        self.auth_window.close()
        self.show_main_window()
        
    def show_main_window(self):
        self.main_window = MainWindow(self.current_user, self.db)
        self.main_window.logout_signal.connect(self.handle_logout)
        self.main_window.show()
        
    def handle_logout(self):
        self.current_user = None
        self.show_auth()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    emergency_app = EmergencyResponseApp()
    emergency_app.run()
    
    sys.exit(app.exec_())
