from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QFrame, QStackedWidget)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QFontDatabase
from ui.widgets.step_indicator import StepIndicator
from ui.widgets.custom_input import CustomInput, PhoneInput, HelpIcon
from ui.widgets.personal_details_form import PersonalDetailsForm
from ui.widgets.elemental_assessment_result_form import ElementalAssessmentResultForm
from ui.widgets.pdf_preview_widget import PdfPreviewWidget
from ai.complete_report import generate_complete_output
import tempfile
import os


class ReportWorker(QThread):
    """Background worker that runs the slow generate_complete_output call."""
    result_ready = pyqtSignal(dict)

    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input

    def run(self):
        try:
            result = generate_complete_output(self.user_input)
            print(result)
        except Exception as e:
            result = {"__error": True, "error_message": str(e)}
        # emit result (in main thread)
        try:
            self.result_ready.emit(result)
        except Exception:
            pass


class AccountCreationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Register local fonts (Aptos) so Qt widgets and stylesheets can use them
        try:
            from pathlib import Path
            fonts_dir = Path(__file__).resolve().parents[2] / 'fonts'
            if fonts_dir.exists():
                for f in fonts_dir.glob('*.ttf'):
                    try:
                        QFontDatabase.addApplicationFont(str(f))
                    except Exception:
                        pass
        except Exception:
            pass

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
        logo = QLabel("BirthCode")
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
        title = QLabel("Unveil Your Energetic Blueprint")
        title.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 14px;
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

    # --- Loading overlay helpers ---
    def _create_loading_overlay(self):
        """Create a semi-transparent overlay with a loading message."""
        overlay = QWidget(self)
        overlay.setObjectName("loading_overlay")
        overlay.setStyleSheet("background: rgba(0,0,0,0.45);")
        overlay.setGeometry(self.rect())
        layout = QVBoxLayout(overlay)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel("Please wait report is generating")
        label.setStyleSheet("color: white; font-size: 18px; font-weight: 600;")
        layout.addWidget(label)
        overlay.setVisible(False)
        return overlay

    def _show_loading(self):
        if not hasattr(self, '_loading_overlay'):
            self._loading_overlay = self._create_loading_overlay()
        self._loading_overlay.setGeometry(self.rect())
        self._loading_overlay.setVisible(True)

    def _hide_loading(self):
        if hasattr(self, '_loading_overlay'):
            self._loading_overlay.setVisible(False)

    def _on_generation_finished(self, full_report: dict, personal, fire, earth, air, water, cardinal, fixed, mutable):
        """Handle the report generation result emitted from the background worker."""
        try:
            # hide loading
            self._hide_loading()
            try:
                self.personal_details_form.next_btn.setEnabled(True)
            except Exception:
                pass

            # if error returned, show minimal feedback and abort
            if not isinstance(full_report, dict) or full_report.get("__error"):
                print("Report generation failed:", full_report.get(
                    "error_message") if isinstance(full_report, dict) else full_report)
                # still show assessment page with fallback message
                combined = {
                    "Elemental_Analysis": {},
                    "Daily_Guideline": {},
                    "Modalities": {},
                    "Element_Percentages": {"Fire": fire, "Earth": earth, "Air": air, "Water": water},
                    "Modalities_Percentages": {"Cardinal": cardinal, "Fixed": fixed, "Mutable": mutable},
                    "Personal": personal,
                    "Summary": "Report generation failed. Please try again later."
                }
                combined["Element_Descriptions"] = full_report.get(
                    "Element_Descriptions", {}) if isinstance(full_report, dict) else {}
                combined["Daily_Routine"] = full_report.get(
                    "Daily_Routine", {}) if isinstance(full_report, dict) else {}
                combined["Modality_Descriptions"] = full_report.get(
                    "Modality_Descriptions", {}) if isinstance(full_report, dict) else {}
                self.elemental_assessment_form.load_assessment_data(combined)
                self.show_assessment_result()
                return

            # Map AI output keys into the structure expected by the UI/template
            # New JSON structure from ai/complete_report.py:
            # "Element_Descriptions": {
            #   "Fire": { "Title": "...", "Content": {...}, "Status": "...", "Percentage": ... },
            #   ...
            # }
            elemental_src = full_report.get("Element_Descriptions", {}) or {}
            elemental_map = {}

            for ename, ed in elemental_src.items():
                # ed is expected to be a dict with Title, Content, Status, Percentage
                if not isinstance(ed, dict):
                    continue

                content_data = ed.get("Content")
                # Content might be a JSON string, a dict, or a plain string
                description = ""
                scientific = ""
                imbalance = ""
                remedies = {}

                if isinstance(content_data, dict):
                    # It's already a parsed dict (e.g. from fire_high_fixed JSON)
                    # We need to map keys from the JSON prompts to UI fields
                    # Example keys in JSON: "The Fire Element", "Physique", "Temperament", "Diet", "Lifestyle and Exercise"

                    # Heuristic mapping
                    description = content_data.get("The Fire Element") or content_data.get("The Earth Element") or \
                        content_data.get("The Air Element") or content_data.get("The Water Element") or \
                        content_data.get("Description") or ""

                    # Not present in all, but good to have
                    scientific = content_data.get(
                        "Scientific Correlation") or ""

                    # Combine some fields for "Imbalance Effects" if not explicitly present
                    imbalance_parts = []
                    if content_data.get("What Low Fire Feels Like—and How It Holds You Back"):
                        imbalance_parts.append(content_data.get(
                            "What Low Fire Feels Like—and How It Holds You Back"))
                    if content_data.get("What Excess Fire Feels Like—and Why You Need to Rein It In"):
                        imbalance_parts.append(content_data.get(
                            "What Excess Fire Feels Like—and Why You Need to Rein It In"))
                    # ... add other element specific keys if needed, or generic "Imbalance"
                    if content_data.get("Imbalance Effects"):
                        imbalance_parts.append(
                            content_data.get("Imbalance Effects"))

                    imbalance = "\n\n".join(imbalance_parts)

                    # Remedies
                    remedies = {
                        "Diet": content_data.get("Diet", ""),
                        "Lifestyle_and_Exercise": content_data.get("Lifestyle and Exercise", ""),
                        "Herbal_or_Energy_Support": content_data.get("Gems, Flower Remedies, and Aromas") or
                        content_data.get("Herbs") or
                        content_data.get(
                            "Crystals, Gems, and Herbal Remedies") or ""
                    }
                elif isinstance(content_data, str):
                    description = content_data

                elemental_map[ename] = {
                    "Classification": ed.get("Title", ""),
                    "Description": description,
                    "Scientific_Correlation": scientific,
                    "Imbalance_Effects": imbalance,
                    "Remedies": remedies,
                    "Status": ed.get("Status", ""),
                    "Percentage": ed.get("Percentage", 0)
                }

            daily_src = full_report.get("Daily_Routine", {}) or {}

            # Modalities
            modalities_src = full_report.get("Modality_Descriptions", {}) or {}
            modalities_map = {}

            for mname, mcontent in modalities_src.items():
                # mcontent is expected to be a dict (parsed JSON) or string
                # Structure: "Cardinal": { "Cardinal_Energy": { "Cardinal Energy": "...", ... } } OR just the inner dict

                content_dict = {}
                if isinstance(mcontent, dict):
                    # Check if it's nested like {"Cardinal_Energy": {...}}
                    if len(mcontent) == 1 and isinstance(list(mcontent.values())[0], dict):
                        content_dict = list(mcontent.values())[0]
                    else:
                        content_dict = mcontent

                modalities_map[mname] = {
                    "Content": content_dict,  # Pass the whole dict for rendering
                    "Percentage": full_report.get("Modalities_Percentages", {}).get(mname, 0)
                }

            combined = {
                "Elemental_Analysis": elemental_map,
                "Daily_Guideline": daily_src,
                "Modalities": modalities_map,
                "Element_Percentages": full_report.get("Element_Percentages", {}),
                "Modalities_Percentages": full_report.get("Modalities_Percentages", {}),
                "Personal": personal,
                "Summary": full_report.get("Summary", "AI generated assessment"),
                "Disclaimer": full_report.get("Disclaimer", "")
            }

            # Keep raw data too just in case
            combined["Element_Descriptions"] = full_report.get(
                "Element_Descriptions", {})
            combined["Daily_Routine"] = full_report.get("Daily_Routine", {})
            combined["Modality_Descriptions"] = full_report.get(
                "Modality_Descriptions", {})

            self.elemental_assessment_form.load_assessment_data(combined)
            self.show_assessment_result()

        except Exception as e:
            print(f"Error processing generated assessment: {e}")
            import traceback
            traceback.print_exc()

    def on_personal_details_next(self):
        """Collect personal details and elemental inputs, call AI functions,
        and show the assessment result page."""
        # Collect user input and run generation in a background thread to keep UI responsive
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
        fire = float(pd.fire_element.text() or 0)
        earth = float(pd.earth_element.text() or 0)
        air = float(pd.air_element.text() or 0)
        water = float(pd.water_element.text() or 0)

        # Qualities
        cardinal = float(pd.cardinal_quality.text() or 0)
        fixed = float(pd.fixed_quality.text() or 0)
        mutable = float(pd.mutable_quality.text() or 0)

        # Build user input for the single canonical report generator
        user_input = {
            "fire": fire,
            "earth": earth,
            "air": air,
            "water": water,
            "cardinal": cardinal,
            "fixed": fixed,
            "mutable": mutable,
        }

        # show loading overlay
        self._show_loading()
        # disable next button to avoid duplicate clicks
        try:
            self.personal_details_form.next_btn.setEnabled(False)
        except Exception:
            pass

        # start background worker
        self._worker = ReportWorker(user_input)
        self._worker.result_ready.connect(lambda result: self._on_generation_finished(
            result, personal, fire, earth, air, water, cardinal, fixed, mutable))
        self._worker.finished.connect(lambda: None)
        self._worker.start()

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
