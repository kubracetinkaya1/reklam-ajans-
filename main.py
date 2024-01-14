import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QLineEdit
from sonlogin import Ui_Form
from system_info import SystemWindow
from connet_db import ConnectDatabase


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.login_btn = None
        self.show_password_checkbox = None
        self.password = None
        self.username = None
        self.ui_login = None
        self.init_ui()
        self.db = ConnectDatabase()

    def init_ui(self):
        self.ui_login = Ui_Form()
        self.ui_login.setupUi(self)
        self.username = self.ui_login.lineEdit_2
        self.password = self.ui_login.lineEdit
        self.login_btn = self.ui_login.pushButton
        self.show_password_checkbox = self.ui_login.checkBox
        self.login_btn.clicked.connect(self.login)
        self.password.returnPressed.connect(self.login)
        self.show_password_checkbox.stateChanged.connect(self.toggle_pwd_visibility)

    def login(self):
        user = self.username.text()
        pwd = self.password.text()

        user = self.db.login({'username': user, 'password': pwd})
        if user:
            w_login.hide()
            w_info.show()
        else:
            QMessageBox.information(self, 'Başarısız', 'Giriş Başarısız')

    def toggle_pwd_visibility(self):
        if self.show_password_checkbox.isChecked() == 1:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)


# App entry point
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w_login = LoginWindow()
    w_info = SystemWindow()
    w_login.show()
    app.exec()