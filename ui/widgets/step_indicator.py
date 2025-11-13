from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen


class StepItem(QWidget):
    def __init__(self, number, text, is_active=False, is_completed=False):
        super().__init__()
        self.number = number
        self.text = text
        self.is_active = is_active
        self.is_completed = is_completed
        self.init_ui()

    def set_state(self, active, completed):
        """Update the state of the step"""
        self.is_active = active
        self.is_completed = completed
        self.circle.is_active = active
        self.circle.is_completed = completed
        self.circle.update()

        # Update label style
        if self.is_active:
            self.label.setStyleSheet("""
                QLabel {
                    color: #000000;
                    font-size: 14px;
                    font-weight: 600;
                    background-color: transparent;
                }
            """)
        else:
            self.label.setStyleSheet("""
                QLabel {
                    color: #AAAAAA;
                    font-size: 14px;
                    background-color: transparent;
                }
            """)

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # Circle with number or checkmark
        self.circle = StepCircle(
            self.number, self.is_active, self.is_completed)
        layout.addWidget(self.circle)

        # Step text
        self.label = QLabel(self.text)
        if self.is_active:
            self.label.setStyleSheet("""
                QLabel {
                    color: #000000;
                    font-size: 14px;
                    font-weight: 600;
                    background-color: transparent;
                }
            """)
        else:
            self.label.setStyleSheet("""
                QLabel {
                    color: #AAAAAA;
                    font-size: 14px;
                    background-color: transparent;
                }
            """)

        layout.addWidget(self.label)
        layout.addStretch()


class StepCircle(QWidget):
    def __init__(self, number, is_active=False, is_completed=False):
        super().__init__()
        self.number = number
        self.is_active = is_active
        self.is_completed = is_completed
        self.setFixedSize(36, 36)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw circle
        if self.is_completed:
            painter.setBrush(QColor("#3EACA8"))
            painter.setPen(QPen(QColor("#3EACA8"), 2))
        elif self.is_active:
            painter.setBrush(QColor("#3EACA8"))
            painter.setPen(QPen(QColor("#3EACA8"), 2))
        else:
            painter.setBrush(QColor("#E0E0E0"))
            painter.setPen(QPen(QColor("#E0E0E0"), 2))

        painter.drawEllipse(2, 2, 32, 32)

        # Draw number or checkmark
        if self.is_completed:
            painter.setPen(QColor("#FFFFFF"))
            painter.setFont(painter.font())
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "✓")
        else:
            if self.is_active:
                painter.setPen(QColor("#FFFFFF"))
            else:
                painter.setPen(QColor("#999999"))

            font = painter.font()
            font.setPointSize(12)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(
                self.rect(), Qt.AlignmentFlag.AlignCenter, str(self.number))


class StepConnector(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(2, 30)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("#E0E0E0"), 2))
        painter.drawLine(18, 0, 18, 30)


class StepIndicator(QWidget):
    def __init__(self):
        super().__init__()
        self.current_step = 1
        self.step_widgets = []
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.steps_data = [
            "Personal Details",
            "Health History",
            "Tax Details",
            "Summary",
            "Receipt"
        ]

        for i, text in enumerate(self.steps_data, 1):
            is_active = (i == 1)
            is_completed = False
            step = StepItem(i, text, is_active, is_completed)
            self.step_widgets.append(step)
            self.layout.addWidget(step)

            # Add connector line between steps
            if i < len(self.steps_data):
                connector = StepConnector()
                self.layout.addWidget(connector)

    def set_active_step(self, step_number):
        """Update the active step"""
        self.current_step = step_number

        for i, step_widget in enumerate(self.step_widgets, 1):
            if i < step_number:
                step_widget.set_state(active=False, completed=True)
            elif i == step_number:
                step_widget.set_state(active=True, completed=False)
            else:
                step_widget.set_state(active=False, completed=False)
