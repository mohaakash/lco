from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QComboBox, QScrollArea, QTextEdit,
                             QCheckBox, QRadioButton, QButtonGroup, QFileDialog,
                             QMessageBox, QSpinBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.widgets.custom_input import CustomInput
import re


class HealthHistoryForm(QWidget):
    next_clicked = pyqtSignal()
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet(
            "QScrollArea { background-color: white; border: none; }")

        content = QWidget()
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Title and Upload Section
        title_layout = QHBoxLayout()

        title = QLabel("HEALTH HISTORY")
        title.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 18px;
                font-weight: 600;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()

        # Upload PDF button
        upload_btn = QPushButton("📄 Upload PDF Form")
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #008B8B;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #006666;
            }
        """)
        upload_btn.clicked.connect(self.upload_pdf)
        title_layout.addWidget(upload_btn)

        layout.addLayout(title_layout)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #DDDDDD;")
        layout.addWidget(divider)

        # Basic Information
        self.add_section_header(layout, "BASIC INFORMATION")

        basic_row1 = QHBoxLayout()
        basic_row1.setSpacing(15)
        self.name_input = CustomInput("Name")
        self.dob_input = CustomInput("Date of Birth & Time")
        basic_row1.addWidget(self.name_input)
        basic_row1.addWidget(self.dob_input)
        layout.addLayout(basic_row1)

        basic_row2 = QHBoxLayout()
        basic_row2.setSpacing(15)
        self.contact_input = CustomInput(
            "Preferred Contact (email/mobile/other)")
        self.birthplace_input = CustomInput("Place of birth (city & country)")
        basic_row2.addWidget(self.contact_input)
        basic_row2.addWidget(self.birthplace_input)
        layout.addLayout(basic_row2)

        # Physical Information
        self.add_section_header(layout, "PHYSICAL INFORMATION")

        self.childhood_diseases = CustomInput(
            "Childhood diseases? Please describe")
        layout.addWidget(self.childhood_diseases)

        allergy_row = QHBoxLayout()
        allergy_row.setSpacing(15)
        self.allergies = CustomInput("Allergies?")
        self.allergy_age = CustomInput("At what age?")
        self.allergy_age.setFixedWidth(200)
        allergy_row.addWidget(self.allergies)
        allergy_row.addWidget(self.allergy_age)
        layout.addLayout(allergy_row)

        self.present_medication = CustomInput("Present Medication?")
        layout.addWidget(self.present_medication)

        # Smoking
        smoking_layout = QHBoxLayout()
        smoke_label = QLabel("Do you smoke?")
        smoke_label.setStyleSheet("font-size: 13px; color: #333;")
        smoking_layout.addWidget(smoke_label)

        self.smoke_yes = QRadioButton("Yes")
        self.smoke_no = QRadioButton("No")
        self.smoke_no.setChecked(True)
        smoking_layout.addWidget(self.smoke_yes)
        smoking_layout.addWidget(self.smoke_no)

        smoking_layout.addWidget(QLabel("If yes, how many packs?"))
        self.smoke_packs = QSpinBox()
        self.smoke_packs.setFixedWidth(80)
        smoking_layout.addWidget(self.smoke_packs)
        smoking_layout.addStretch()

        layout.addLayout(smoking_layout)

        # Alcohol
        alcohol_layout = QHBoxLayout()
        alcohol_label = QLabel("Do you drink alcohol?")
        alcohol_label.setStyleSheet("font-size: 13px; color: #333;")
        alcohol_layout.addWidget(alcohol_label)

        self.alcohol_yes = QRadioButton("Yes")
        self.alcohol_no = QRadioButton("No")
        self.alcohol_no.setChecked(True)
        alcohol_layout.addWidget(self.alcohol_yes)
        alcohol_layout.addWidget(self.alcohol_no)
        alcohol_layout.addStretch()

        layout.addLayout(alcohol_layout)

        alcohol_details = QHBoxLayout()
        alcohol_details.setSpacing(15)
        self.alcohol_what = CustomInput("If yes, what?")
        self.alcohol_frequency = CustomInput("How often or much?")
        self.alcohol_why = CustomInput("Why?")
        alcohol_details.addWidget(self.alcohol_what)
        alcohol_details.addWidget(self.alcohol_frequency)
        alcohol_details.addWidget(self.alcohol_why)
        layout.addLayout(alcohol_details)

        # Diet Information
        diet_row = QHBoxLayout()
        diet_row.setSpacing(15)
        self.milk_intake = CustomInput("How much milk do you drink daily?")
        self.dairy_products = CustomInput("Other dairy products?")
        diet_row.addWidget(self.milk_intake)
        diet_row.addWidget(self.dairy_products)
        layout.addLayout(diet_row)

        # Bath or Shower
        bath_layout = QHBoxLayout()
        bath_label = QLabel("Do you take a:")
        bath_layout.addWidget(bath_label)
        self.bath_radio = QRadioButton("Bath")
        self.shower_radio = QRadioButton("Shower")
        self.shower_radio.setChecked(True)
        bath_layout.addWidget(self.bath_radio)
        bath_layout.addWidget(self.shower_radio)
        bath_layout.addStretch()
        layout.addLayout(bath_layout)

        # Food preference
        food_pref_label = QLabel("Are you primarily a:")
        layout.addWidget(food_pref_label)

        food_pref_layout = QHBoxLayout()
        self.meat_eater = QRadioButton("Meat eater")
        self.fruit_eater = QRadioButton("Fruit eater")
        self.veg_eater = QRadioButton("Vegetable eater")
        self.processed_eater = QRadioButton("Processed food eater")
        food_pref_layout.addWidget(self.meat_eater)
        food_pref_layout.addWidget(self.fruit_eater)
        food_pref_layout.addWidget(self.veg_eater)
        food_pref_layout.addWidget(self.processed_eater)
        food_pref_layout.addStretch()
        layout.addLayout(food_pref_layout)

        self.diet_mix = CustomInput("Or describe your mix")
        layout.addWidget(self.diet_mix)

        # Food relationship
        self.past_food_relationship = QTextEdit()
        self.past_food_relationship.setPlaceholderText(
            "Describe your past relationship with food...")
        self.past_food_relationship.setMaximumHeight(80)
        self.past_food_relationship.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.past_food_relationship)

        self.current_food_relationship = QTextEdit()
        self.current_food_relationship.setPlaceholderText(
            "Describe current relationship with food...")
        self.current_food_relationship.setMaximumHeight(80)
        self.current_food_relationship.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.current_food_relationship)

        # Diet questions
        diet_q1 = QHBoxLayout()
        diet_q1.setSpacing(15)
        self.typical_meals = CustomInput("Typical breakfast, lunch, dinner?")
        self.diet_balanced = CustomInput("Is your diet balanced?")
        diet_q1.addWidget(self.typical_meals)
        diet_q1.addWidget(self.diet_balanced)
        layout.addLayout(diet_q1)

        diet_q2 = QHBoxLayout()
        diet_q2.setSpacing(15)
        self.nutrition_change = CustomInput(
            "Would you consider nutrition changes?")
        self.sweets_consumption = CustomInput(
            "Do you eat sweets/sugar? (Yes/No)")
        diet_q2.addWidget(self.nutrition_change)
        diet_q2.addWidget(self.sweets_consumption)
        layout.addLayout(diet_q2)

        water_caffeine = QHBoxLayout()
        water_caffeine.setSpacing(15)
        self.water_intake = CustomInput(
            "Water intake (liters/glasses per day)")
        self.caffeine = CustomInput("Caffeinated beverages?")
        water_caffeine.addWidget(self.water_intake)
        water_caffeine.addWidget(self.caffeine)
        layout.addLayout(water_caffeine)

        # Health conditions
        self.create_health_conditions_section(layout)

        # Supplements
        self.create_supplements_section(layout)

        # Goals
        self.create_goals_section(layout)

        # Environmental
        self.create_environmental_section(layout)

        # Emotional
        self.create_emotional_section(layout)

        # Navigation buttons
        btn_layout = QHBoxLayout()

        back_btn = QPushButton("Back")
        back_btn.setFixedHeight(45)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #CCCCCC;
                color: #333333;
                border: none;
                border-radius: 22px;
                font-size: 14px;
                font-weight: 600;
                padding: 12px 40px;
            }
            QPushButton:hover {
                background-color: #BBBBBB;
            }
        """)
        back_btn.clicked.connect(self.back_clicked.emit)

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
        """)
        next_btn.clicked.connect(self.next_clicked.emit)

        btn_layout.addWidget(back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(next_btn)
        layout.addLayout(btn_layout)

        main_layout.addWidget(scroll)

    def text_edit_style(self):
        return """
            QTextEdit {
                padding: 10px;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 2px solid #008B8B;
            }
        """

    def add_section_header(self, layout, text):
        label = QLabel(text)
        label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.5px;
                margin-top: 15px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(label)

    def create_health_conditions_section(self, layout):
        self.add_section_header(layout, "HEALTH CONDITIONS")

        conditions = {
            "Metabolic Health": ["Blood Sugar Imbalances", "Elevated Blood Pressure",
                                 "Elevated Cholesterol", "Elevated Triglycerides"],
            "Digestive Health": ["Bloating", "Constipation", "Diarrhea", "Nausea", "Stomach Pain"],
            "Reproductive Health": ["Infertility", "Irregular Menstrual Cycle", "Low Libido"],
            "Hormonal Health": ["Thyroid Condition", "Toxin Exposure", "Sugar in Blood"],
            "Immune Health": ["Autoimmune Conditions", "Low Vitamin D Level",
                              "Frequent Illness or Infection"],
            "Brain Health": ["Brain Fog", "Difficulty Concentrating", "Forgetfulness",
                             "Nervous Disorders", "Dizziness"]
        }

        self.condition_checkboxes = {}

        for category, items in conditions.items():
            cat_label = QLabel(category)
            cat_label.setStyleSheet(
                "font-weight: bold; color: #008B8B; font-size: 12px; margin-top: 10px;")
            layout.addWidget(cat_label)

            # Create 2-column layout for checkboxes
            cb_layout = QHBoxLayout()
            left_col = QVBoxLayout()
            right_col = QVBoxLayout()

            for i, item in enumerate(items):
                cb = QCheckBox(item)
                cb.setStyleSheet("font-size: 12px; padding: 3px;")
                self.condition_checkboxes[item] = cb

                if i % 2 == 0:
                    left_col.addWidget(cb)
                else:
                    right_col.addWidget(cb)

            cb_layout.addLayout(left_col)
            cb_layout.addLayout(right_col)
            cb_layout.addStretch()
            layout.addLayout(cb_layout)

        # Additional issues
        self.add_section_header(layout, "ADDITIONAL HEALTH ISSUES")

        additional_issues = [
            "Cardiovascular problems", "Urinary disorders", "Lung disorders",
            "Kidney/bladder ailments", "Headaches", "Osteoporosis/arthritis",
            "Weight issues", "Diabetes/insulin-related"
        ]

        self.additional_checkboxes = {}

        # 2-column layout
        for i in range(0, len(additional_issues), 2):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(20)

            for j in range(2):
                if i + j < len(additional_issues):
                    issue = additional_issues[i + j]
                    cb = QCheckBox(issue)
                    cb.setStyleSheet("font-size: 12px;")
                    self.additional_checkboxes[issue] = cb
                    row_layout.addWidget(cb)

            row_layout.addStretch()
            layout.addLayout(row_layout)

    def create_supplements_section(self, layout):
        self.add_section_header(layout, "SUPPLEMENTS AND MEDICATION")

        self.current_medication = QTextEdit()
        self.current_medication.setPlaceholderText(
            "Current medications (specify what, how much, frequency)")
        self.current_medication.setMaximumHeight(70)
        self.current_medication.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.current_medication)

        self.otc_medication = QTextEdit()
        self.otc_medication.setPlaceholderText(
            "Over-the-counter medications and frequency")
        self.otc_medication.setMaximumHeight(70)
        self.otc_medication.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.otc_medication)

        self.supplements = QTextEdit()
        self.supplements.setPlaceholderText(
            "Natural vitamin or mineral supplements (specify strength and frequency)")
        self.supplements.setMaximumHeight(70)
        self.supplements.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.supplements)

        # Surgery history
        surgery_layout = QHBoxLayout()
        surgery_layout.setSpacing(15)
        self.surgery_when = CustomInput("Surgery - When?")
        self.surgery_part = CustomInput("Part of Body?")
        self.surgery_outcome = CustomInput("Outcome?")
        surgery_layout.addWidget(self.surgery_when)
        surgery_layout.addWidget(self.surgery_part)
        surgery_layout.addWidget(self.surgery_outcome)
        layout.addLayout(surgery_layout)

    def create_goals_section(self, layout):
        self.add_section_header(
            layout, "HEALTH AND WELLNESS GOALS & FAMILY HISTORY")

        self.health_goals = QTextEdit()
        self.health_goals.setPlaceholderText(
            "What are your health and wellness goals? Why are they important?")
        self.health_goals.setMaximumHeight(70)
        self.health_goals.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.health_goals)

        self.health_story = QTextEdit()
        self.health_story.setPlaceholderText(
            "Most important thing about your health story...")
        self.health_story.setMaximumHeight(70)
        self.health_story.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.health_story)

        # Family history
        family_layout = QHBoxLayout()
        family_layout.setSpacing(15)
        self.father_history = CustomInput("Father's Health History")
        self.mother_history = CustomInput("Mother's Health History")
        family_layout.addWidget(self.father_history)
        family_layout.addWidget(self.mother_history)
        layout.addLayout(family_layout)

    def create_environmental_section(self, layout):
        self.add_section_header(
            layout, "NATURAL RHYTHMS AND ENVIRONMENTAL EXPOSURES")

        self.sleep_quality = QTextEdit()
        self.sleep_quality.setPlaceholderText(
            "Describe your sleep quality and quantity...")
        self.sleep_quality.setMaximumHeight(60)
        self.sleep_quality.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.sleep_quality)

        energy_layout = QHBoxLayout()
        energy_layout.addWidget(QLabel("Energy Level (1-5):"))
        self.energy_level = QSpinBox()
        self.energy_level.setMinimum(1)
        self.energy_level.setMaximum(5)
        self.energy_level.setValue(3)
        self.energy_level.setFixedWidth(60)
        energy_layout.addWidget(self.energy_level)
        energy_layout.addStretch()
        layout.addLayout(energy_layout)

        sun_layout = QHBoxLayout()
        sun_layout.setSpacing(15)
        self.sunlight_exposure = CustomInput(
            "Daily sunlight exposure (minutes/hours)")
        self.morning_sunlight = CustomInput(
            "Morning sunlight? (Yes/No/Sometimes)")
        sun_layout.addWidget(self.sunlight_exposure)
        sun_layout.addWidget(self.morning_sunlight)
        layout.addLayout(sun_layout)

        screen_layout = QHBoxLayout()
        screen_layout.setSpacing(15)
        self.screen_time = CustomInput("Screen time (hours per day)")
        self.blue_light_protection = CustomInput(
            "Use blue light blockers? (Yes/No)")
        screen_layout.addWidget(self.screen_time)
        screen_layout.addWidget(self.blue_light_protection)
        layout.addLayout(screen_layout)

        rhythm_layout = QHBoxLayout()
        rhythm_layout.setSpacing(15)
        self.wake_time = CustomInput("Wake up time")
        self.bed_time = CustomInput("Bed time")
        rhythm_layout.addWidget(self.wake_time)
        rhythm_layout.addWidget(self.bed_time)
        layout.addLayout(rhythm_layout)

        env_layout = QHBoxLayout()
        env_layout.setSpacing(15)
        self.mold_exposure = CustomInput("Mold exposure? (Yes/No)")
        self.water_proximity = CustomInput("Near body of water? (distance)")
        env_layout.addWidget(self.mold_exposure)
        env_layout.addWidget(self.water_proximity)
        layout.addLayout(env_layout)

        self.grounding = CustomInput(
            "Time spent barefoot on natural surfaces?")
        layout.addWidget(self.grounding)

        self.chemical_exposure = QTextEdit()
        self.chemical_exposure.setPlaceholderText(
            "Chemical or toxin exposures (pesticides, cleaning products, etc.)")
        self.chemical_exposure.setMaximumHeight(60)
        self.chemical_exposure.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.chemical_exposure)

    def create_emotional_section(self, layout):
        self.add_section_header(layout, "EMOTIONAL & MENTAL HEALTH")

        emotions_label = QLabel(
            "Rate how often you experience (1=never, 5=always):")
        emotions_label.setStyleSheet(
            "font-size: 12px; color: #666; margin-bottom: 5px;")
        layout.addWidget(emotions_label)

        emotions = ["Anger", "Sadness", "Excitement",
                    "Stress", "Fear", "Joy", "Love", "Worry"]
        self.emotion_ratings = {}

        for i in range(0, len(emotions), 4):
            h_layout = QHBoxLayout()
            h_layout.setSpacing(15)

            for j in range(4):
                if i + j < len(emotions):
                    emotion = emotions[i + j]
                    emotion_layout = QHBoxLayout()
                    emotion_layout.setSpacing(5)

                    lbl = QLabel(f"{emotion}:")
                    lbl.setFixedWidth(80)
                    lbl.setStyleSheet("font-size: 12px;")
                    emotion_layout.addWidget(lbl)

                    spinner = QSpinBox()
                    spinner.setMinimum(1)
                    spinner.setMaximum(5)
                    spinner.setValue(3)
                    spinner.setFixedWidth(50)
                    self.emotion_ratings[emotion] = spinner

                    emotion_layout.addWidget(spinner)
                    h_layout.addLayout(emotion_layout)

            h_layout.addStretch()
            layout.addLayout(h_layout)

        self.mental_health = QTextEdit()
        self.mental_health.setPlaceholderText(
            "Describe your overall mental and emotional health...")
        self.mental_health.setMaximumHeight(60)
        self.mental_health.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.mental_health)

        self.mental_support = QTextEdit()
        self.mental_support.setPlaceholderText(
            "How do you support your mental health?")
        self.mental_support.setMaximumHeight(60)
        self.mental_support.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.mental_support)

        self.stress_coping = QTextEdit()
        self.stress_coping.setPlaceholderText("How do you cope with stress?")
        self.stress_coping.setMaximumHeight(60)
        self.stress_coping.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.stress_coping)

        spirituality_relationships = QHBoxLayout()
        spirituality_relationships.setSpacing(15)
        self.spirituality = CustomInput("Relationship with spirituality?")
        self.important_relationships = CustomInput(
            "Important relationships in your life?")
        spirituality_relationships.addWidget(self.spirituality)
        spirituality_relationships.addWidget(self.important_relationships)
        layout.addLayout(spirituality_relationships)

        lifestyle_layout = QHBoxLayout()
        lifestyle_layout.setSpacing(15)
        self.work_hours = CustomInput("Work hours per week")
        self.hobbies = CustomInput("Hobbies and recreational activities")
        lifestyle_layout.addWidget(self.work_hours)
        lifestyle_layout.addWidget(self.hobbies)
        layout.addLayout(lifestyle_layout)

        self.exercise = QTextEdit()
        self.exercise.setPlaceholderText(
            "Role of movement, sports, exercise in your life...")
        self.exercise.setMaximumHeight(60)
        self.exercise.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.exercise)

        living_social = QHBoxLayout()
        living_social.setSpacing(15)
        self.living_situation = CustomInput("Who do you live with?")
        self.social_life = CustomInput("About your social life?")
        living_social.addWidget(self.living_situation)
        living_social.addWidget(self.social_life)
        layout.addLayout(living_social)

        self.additional_comments = QTextEdit()
        self.additional_comments.setPlaceholderText(
            "Any other details about your health, lifestyle, or concerns?")
        self.additional_comments.setMaximumHeight(80)
        self.additional_comments.setStyleSheet(self.text_edit_style())
        layout.addWidget(self.additional_comments)

    def upload_pdf(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Health History PDF",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )

        if file_name:
            try:
                self.parse_pdf(file_name)
                QMessageBox.information(
                    self,
                    "Success",
                    "PDF uploaded and parsed successfully!"
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Failed to parse PDF: {str(e)}"
                )

    def parse_pdf(self, file_path):
        """Parse PDF and fill form fields"""
        try:
            import PyPDF2

            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""

            # Extract information using regex patterns
            self.extract_and_fill(text)

        except ImportError:
            QMessageBox.warning(
                self,
                "Missing Dependency",
                "PyPDF2 is required to parse PDFs. Install it with: pip install PyPDF2"
            )

    def extract_and_fill(self, text):
        """Extract data from text and fill form fields"""
        # Basic Information
        name_match = re.search(
            r'Name[:\s]+([A-Za-z\s]+?)(?:Date|$)', text, re.IGNORECASE)
        if name_match:
            self.name_input.setText(name_match.group(1).strip())

        dob_match = re.search(
            r'Date of Birth.*?Time[:\s]+([^\n]+)', text, re.IGNORECASE)
        if dob_match:
            self.dob_input.setText(dob_match.group(1).strip())

        contact_match = re.search(
            r'Preferred Contact.*?\(([^)]+)\)', text, re.IGNORECASE)
        if contact_match:
            self.contact_input.setText(contact_match.group(1).strip())

        birthplace_match = re.search(
            r'Place of birth.*?\(([^)]+)\)', text, re.IGNORECASE)
        if birthplace_match:
            self.birthplace_input.setText(birthplace_match.group(1).strip())

        # Physical Information
        allergy_match = re.search(
            r'Allergies\?[:\s]*([^\n]+)', text, re.IGNORECASE)
        if allergy_match:
            self.allergies.setText(allergy_match.group(1).strip())

        medication_match = re.search(
            r'Present Medication\?[:\s]*([^\n]+)', text, re.IGNORECASE)
        if medication_match:
            self.present_medication.setText(medication_match.group(1).strip())

        # Smoking
        if re.search(r'smoke.*?Yes', text, re.IGNORECASE):
            self.smoke_yes.setChecked(True)

        # Alcohol
        if re.search(r'alcohol.*?Yes', text, re.IGNORECASE):
            self.alcohol_yes.setChecked(True)

        print("PDF data extracted and form filled!")
