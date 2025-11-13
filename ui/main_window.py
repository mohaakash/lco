from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import Qt
from ui.widgets.account_creation_widget import AccountCreationWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DNB - Create Account")
        self.setMinimumSize(1000, 750)

        # Set background color
        self.setStyleSheet("""
            QMainWindow {
                background-color: #B8D8D8;
            }
        """)

        # Center widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create account creation widget
        self.account_widget = AccountCreationWidget()

        # Center the account widget
        from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(50, 50, 50, 50)

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.account_widget)
        h_layout.addStretch()

        main_layout.addStretch()
        main_layout.addLayout(h_layout)
        main_layout.addStretch()
