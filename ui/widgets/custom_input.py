from PyQt6.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen


class CustomInput(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                font-size: 13px;
                background-color: white;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #008B8B;
            }
            QLineEdit::placeholder {
                color: #999999;
            }
        """)
        self.setMinimumHeight(45)


class PhoneInput(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Country code selector
        self.country_code = QComboBox()
        self.country_code.addItem("🇳🇴 +47")
        self.country_code.setFixedWidth(100)
        self.country_code.setStyleSheet("""
            QComboBox {
                padding: 12px;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                background-color: white;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 2px solid #008B8B;
            }
        """)

        # Phone number input
        self.phone_number = CustomInput("Your Phone Number")

        # Help icon
        help_icon = HelpIcon()

        layout.addWidget(self.country_code)
        layout.addWidget(self.phone_number, 1)
        layout.addWidget(help_icon, alignment=Qt.AlignmentFlag.AlignTop)


class HelpIcon(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(24, 24)
        self.setToolTip("Help information")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw circle
        painter.setPen(QPen(QColor("#3EACA8"), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(2, 2, 20, 20)

        # Draw question mark
        painter.setPen(QColor("#3EACA8"))
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "?")

    def mousePressEvent(self, event):
        print("Help icon clicked")
