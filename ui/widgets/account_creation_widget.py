from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QFrame, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.widgets.step_indicator import StepIndicator
from ui.widgets.custom_input import CustomInput, PhoneInput, HelpIcon
from ui.widgets.personal_details_form import PersonalDetailsForm
from ui.widgets.health_history_form import HealthHistoryForm
from ui.widgets.elemental_assessment_result_form import ElementalAssessmentResultForm
from ui.widgets.pdf_preview_widget import PdfPreviewWidget
from ai.elemental_assesment import generate_elemental_report, generate_daily_guideline
from ai.elemental_quality import generate_modality_report
import tempfile
import os


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

        # Add forms: Personal Details and Elemental Assessment Result.
        # Note: Health history form exists in the codebase but is not added to
        # the UI flow for this client demo per request.
        self.personal_details_form = PersonalDetailsForm()
        self.elemental_assessment_form = ElementalAssessmentResultForm()
        self.pdf_preview = PdfPreviewWidget()

        self.stacked_widget.addWidget(self.personal_details_form)
        self.stacked_widget.addWidget(self.elemental_assessment_form)
        # PDF preview page sits after the assessment result
        self.stacked_widget.addWidget(self.pdf_preview)

        # Connect next button from personal details to generate AI reports
        self.personal_details_form.next_clicked.connect(
            self.on_personal_details_next)
        # Allow returning to personal details from assessment
        self.elemental_assessment_form.back_clicked.connect(
            self.show_personal_details)
        self.elemental_assessment_form.next_clicked.connect(
            self.on_assessment_next)
        # When report requests export, generate PDF and show preview
        self.elemental_assessment_form.export_requested.connect(
            self.on_export_requested)

        # Close on preview returns to personal details
        self.pdf_preview.closed.connect(self.show_personal_details)

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
        logo = QLabel("ASTRO HEALTH")
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
        title = QLabel("Elemental Balance Assessment")
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

    def show_assessment_result(self):
        # assessment is index 1 now
        self.stacked_widget.setCurrentIndex(1)
        self.step_indicator.set_active_step(2)

    def on_personal_details_next(self):
        """Collect personal details and elemental inputs, call AI functions,
        and show the assessment result page."""
        try:
            pd = self.personal_details_form

            # Personal identity/contact
            personal = {
                "name": pd.full_name.text(),
                "date_of_birth": pd.date_of_birth.text(),
                "time_of_birth": pd.time_of_birth.text(),
                "place_of_birth": pd.place_of_birth.text(),
                "phone": pd.phone.text(),
                "email": pd.email.text(),
            }

            # Element percentages
            fire = int(pd.fire_element.text() or 0)
            earth = int(pd.earth_element.text() or 0)
            air = int(pd.air_element.text() or 0)
            water = int(pd.water_element.text() or 0)

            # Qualities
            cardinal = int(pd.cardinal_quality.text() or 0)
            fixed = int(pd.fixed_quality.text() or 0)
            mutable = int(pd.mutable_quality.text() or 0)

            # Call AI functions
            elemental_report = generate_elemental_report(
                fire, earth, air, water)
            modality_report = generate_modality_report(
                cardinal, fixed, mutable)

            # daily guideline uses user input and elemental report
            try:
                daily_guideline = generate_daily_guideline(
                    {"fire": fire, "earth": earth, "air": air, "water": water}, elemental_report)
            except Exception:
                daily_guideline = {}

            # Combine into a single payload for the result form
            combined = {
                "Elemental_Analysis": elemental_report if isinstance(elemental_report, dict) else {},
                "Modalities": modality_report,
                "Daily_Guideline": daily_guideline,
                "Personal": personal,
                "Summary": "AI generated assessment"
            }

            # Load into assessment form and show
            self.elemental_assessment_form.load_assessment_data(combined)
            self.show_assessment_result()

        except Exception as e:
            print(f"Error generating AI assessment: {e}")

    def on_assessment_next(self):
        """Handle next button on assessment form"""
        # When user clicks Next on the assessment page, treat it like an export request
        # — generate the HTML from the report widget and show the preview page.
        try:
            # call the report widget's export routine which emits export_requested
            self.elemental_assessment_form.export_pdf()
        except Exception as e:
            print(f"Error while exporting from assessment next: {e}")

    def on_export_requested(self, html: str, assessment_data: dict):
        """Handle export request from the assessment form: generate PDF and show preview."""
        pdf_path = None
        # Try to generate a PDF using WeasyPrint
        try:
            from weasyprint import HTML
            tf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            tf.close()
            HTML(string=html).write_pdf(tf.name)
            pdf_path = tf.name
        except Exception as e:
            # Fallback: write HTML to a temp file (no PDF)
            try:
                tf = tempfile.NamedTemporaryFile(
                    delete=False, suffix='.html', mode='w', encoding='utf-8')
                tf.write(html)
                tf.close()
                pdf_path = None
            except Exception as e2:
                print(f"Failed to generate PDF or HTML preview: {e} / {e2}")
                pdf_path = None

        # Show preview page (pass pdf path and html)
        self.pdf_preview.load_preview(pdf_path, html)
        # switch to preview page (index 2)
        self.stacked_widget.setCurrentWidget(self.pdf_preview)
        self.step_indicator.set_active_step(3)

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
