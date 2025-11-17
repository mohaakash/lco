from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QFrame, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.widgets.step_indicator import StepIndicator
from ui.widgets.custom_input import CustomInput, PhoneInput, HelpIcon
from ui.widgets.personal_details_form import PersonalDetailsForm
from ui.widgets.health_history_form import HealthHistoryForm
from ui.widgets.elemental_assessment_result_form import ElementalAssessmentResultForm
from ai.ai import generate_elemental_report


class AccountCreationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(1100, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left sidebar
        left_panel = self.create_left_panel()

        # Right panel with stacked widget for different forms
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: white;")

        # Add forms
        self.personal_details_form = PersonalDetailsForm()
        self.health_history_form = HealthHistoryForm()
        self.elemental_assessment_form = ElementalAssessmentResultForm()

        self.stacked_widget.addWidget(self.personal_details_form)
        self.stacked_widget.addWidget(self.health_history_form)
        self.stacked_widget.addWidget(self.elemental_assessment_form)

        # Connect next button from personal details
        self.personal_details_form.next_clicked.connect(
            self.show_health_history)
        self.health_history_form.back_clicked.connect(
            self.show_personal_details)
        self.health_history_form.next_clicked.connect(
            self.on_health_history_next)
        self.elemental_assessment_form.back_clicked.connect(
            self.show_health_history)
        self.elemental_assessment_form.next_clicked.connect(
            self.on_assessment_next)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(self.stacked_widget)

    def create_left_panel(self):
        panel = QFrame()
        panel.setFixedWidth(280)
        panel.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
            }
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(30, 40, 30, 40)
        layout.setSpacing(0)

        # DNB Logo
        logo = QLabel("ASTRO HEALTH - AI")
        logo.setStyleSheet("""
            QLabel {
                color: #008B8B;
                font-size: 32px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        layout.addWidget(logo)

        layout.addSpacing(20)

        # Create account title
        title = QLabel("Your Elemental Balance Assessment")
        title.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 22px;
                font-weight: 600;
                background-color: transparent;
            }
        """)
        layout.addWidget(title)

        layout.addSpacing(40)

        # Step indicator
        self.step_indicator = StepIndicator()
        layout.addWidget(self.step_indicator)

        layout.addStretch()

        return panel

    def show_personal_details(self):
        self.stacked_widget.setCurrentIndex(0)
        self.step_indicator.set_active_step(1)

    def show_health_history(self):
        self.stacked_widget.setCurrentIndex(1)
        self.step_indicator.set_active_step(2)

    def show_assessment_result(self):
        self.stacked_widget.setCurrentIndex(2)
        self.step_indicator.set_active_step(3)

    def on_health_history_next(self):
        """Generate AI assessment and show results"""
        try:
            # Extract elemental inputs from personal details form
            fire = int(self.personal_details_form.fire_element.text() or 0)
            earth = int(self.personal_details_form.earth_element.text() or 0)
            air = int(self.personal_details_form.air_element.text() or 0)
            water = int(self.personal_details_form.water_element.text() or 0)

            # Prepare element data for AI
            elements = {
                "Fire": fire,
                "Earth": earth,
                "Air": air,
                "Water": water
            }

            # Call AI function
            assessment_data = generate_elemental_report(elements)

            # Convert string response to dict if needed
            if isinstance(assessment_data, str):
                import json
                assessment_data = json.loads(assessment_data)

            # Load data into form
            self.elemental_assessment_form.load_assessment_data(
                assessment_data)

            # Show assessment result form
            self.show_assessment_result()

        except Exception as e:
            print(f"Error generating assessment: {e}")

    def on_assessment_next(self):
        """Handle next button on assessment form"""
        print("Assessment completed, moving to next step")
        # Here you would proceed to final step or completion

    def create_right_panel(self):
        panel = QWidget()
        panel.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Personal Details Section
        personal_label = QLabel("YOUR PERSONAL DETAILS")
        personal_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
        """)
        layout.addWidget(personal_label)

        # National Identity Number
        id_label = QLabel("National Identity Number/D-number")
        id_label.setStyleSheet("color: #008B8B; font-size: 12px;")
        layout.addWidget(id_label)

        self.id_input = CustomInput("01010102302")
        layout.addWidget(self.id_input)

        hint_label = QLabel("This should be 11 digits long.")
        hint_label.setStyleSheet("color: #999999; font-size: 11px;")
        layout.addWidget(hint_label)

        layout.addSpacing(10)

        # Name fields
        name_layout = QHBoxLayout()
        name_layout.setSpacing(15)

        self.first_name = CustomInput("First Name")
        self.last_name = CustomInput("Last Name")

        name_layout.addWidget(self.first_name)
        name_layout.addWidget(self.last_name)
        layout.addLayout(name_layout)

        layout.addSpacing(10)

        # Residential Address Section
        address_label = QLabel("YOUR RESIDENTIAL ADDRESS")
        address_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
        """)
        layout.addWidget(address_label)

        # Address fields
        address_layout = QHBoxLayout()
        address_layout.setSpacing(15)

        self.street_address = CustomInput("Street Address")
        self.street_optional = CustomInput("Street Address (optional)")

        address_layout.addWidget(self.street_address)
        address_layout.addWidget(self.street_optional)
        layout.addLayout(address_layout)

        # Post code, city, country
        location_layout = QHBoxLayout()
        location_layout.setSpacing(15)

        self.post_code = CustomInput("Post Code")
        self.post_code.setFixedWidth(150)

        self.city = CustomInput("City")

        self.country = QComboBox()
        self.country.addItem("Country")
        self.country.setStyleSheet("""
            QComboBox {
                padding: 12px;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                background-color: white;
                font-size: 13px;
                color: #999999;
            }
            QComboBox:focus {
                border: 2px solid #008B8B;
            }
        """)

        location_layout.addWidget(self.post_code)
        location_layout.addWidget(self.city)
        location_layout.addWidget(self.country)
        layout.addLayout(location_layout)

        layout.addSpacing(10)

        # Contact Details Section
        contact_label = QLabel("CONTACT DETAILS")
        contact_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
        """)
        layout.addWidget(contact_label)

        # Phone number
        self.phone_input = PhoneInput()
        layout.addWidget(self.phone_input)

        # Email
        email_layout = QHBoxLayout()
        email_layout.setSpacing(10)

        self.email = CustomInput("Your Email Address")
        help_icon = HelpIcon()

        email_layout.addWidget(self.email)
        email_layout.addWidget(help_icon, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addLayout(email_layout)

        layout.addStretch()

        # Next button
        next_btn = QPushButton("Next")
        next_btn.setFixedHeight(45)
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #3EACA8;
                color: white;
                border: none;
                border-radius: 22px;
                font-size: 14px;
                font-weight: 600;
                padding: 12px 40px;
            }
            QPushButton:hover {
                background-color: #359B97;
            }
            QPushButton:pressed {
                background-color: #2E8985;
            }
        """)
        next_btn.clicked.connect(self.on_next_clicked)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(next_btn)
        layout.addLayout(btn_layout)

        return panel

    def on_next_clicked(self):
        print("Next button clicked")
        # Here you would validate and proceed to next step
