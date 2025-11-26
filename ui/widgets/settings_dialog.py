from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QDialogButtonBox, QFormLayout)
from PyQt6.QtCore import QSettings

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 150)
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        # Gemini API Key
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("Enter your Gemini API Key")
        form_layout.addRow("Gemini API Key:", self.api_key_input)

        layout.addLayout(form_layout)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | 
                                   QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.save_settings)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def load_settings(self):
        settings = QSettings("BirthCode", "Settings")
        self.api_key_input.setText(settings.value("gemini_api_key", ""))

    def save_settings(self):
        settings = QSettings("BirthCode", "Settings")
        settings.setValue("gemini_api_key", self.api_key_input.text())
        self.accept()
