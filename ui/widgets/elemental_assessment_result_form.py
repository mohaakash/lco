from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QScrollArea, QTextEdit, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
import json


class ElementalAssessmentResultForm(QWidget):
    next_clicked = pyqtSignal()
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.assessment_data = None
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

        # Title
        title = QLabel("Elemental Balance Assessment Results")
        title.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 18px;
                font-weight: 600;
            }
        """)
        layout.addWidget(title)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #DDDDDD;")
        layout.addWidget(divider)

        # Elemental Analysis Section
        analysis_label = QLabel("ELEMENTAL ANALYSIS")
        analysis_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.5px;
                margin-top: 15px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(analysis_label)

        # Store editable fields for each element
        self.element_fields = {}

        # Create sections for each element (Fire, Earth, Air, Water)
        elements = ["Fire", "Earth", "Air", "Water"]
        for element in elements:
            self.create_element_section(layout, element)

        layout.addSpacing(20)

        # Summary Section
        summary_label = QLabel("SUMMARY")
        summary_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.5px;
                margin-top: 15px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(summary_label)

        self.summary_text = QTextEdit()
        self.summary_text.setPlaceholderText("Summary will appear here...")
        self.summary_text.setMaximumHeight(100)
        self.summary_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 2px solid #008B8B;
            }
        """)
        layout.addWidget(self.summary_text)

        layout.addSpacing(10)

        # Disclaimer Section
        disclaimer_label = QLabel("DISCLAIMER")
        disclaimer_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.5px;
                margin-top: 15px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(disclaimer_label)

        self.disclaimer_text = QTextEdit()
        self.disclaimer_text.setPlaceholderText(
            "Disclaimer will appear here...")
        self.disclaimer_text.setMaximumHeight(60)
        self.disclaimer_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 2px solid #008B8B;
            }
        """)
        layout.addWidget(self.disclaimer_text)

        layout.addStretch()

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

    def create_element_section(self, layout, element_name):
        """Create an editable section for each element"""
        # Element header with classification
        header_layout = QHBoxLayout()
        element_label = QLabel(element_name.upper())
        element_label.setStyleSheet("""
            QLabel {
                color: #008B8B;
                font-size: 13px;
                font-weight: 600;
            }
        """)
        header_layout.addWidget(element_label)

        classification_label = QLabel("")
        classification_label.setStyleSheet("""
            QLabel {
                color: #0099CC;
                font-size: 12px;
                font-weight: 500;
            }
        """)
        header_layout.addWidget(classification_label)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Store reference to classification label
        if not hasattr(self, 'classification_labels'):
            self.classification_labels = {}
        self.classification_labels[element_name] = classification_label

        # Description
        description_label = QLabel("Description:")
        description_label.setStyleSheet(
            "color: #666; font-size: 11px; font-weight: 600;")
        layout.addWidget(description_label)

        description_text = QTextEdit()
        description_text.setPlaceholderText("Element description...")
        description_text.setMaximumHeight(80)
        description_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 2px solid #008B8B;
            }
        """)
        layout.addWidget(description_text)

        # Scientific Correlation
        scientific_label = QLabel("Scientific Correlation:")
        scientific_label.setStyleSheet(
            "color: #666; font-size: 11px; font-weight: 600;")
        layout.addWidget(scientific_label)

        scientific_text = QTextEdit()
        scientific_text.setPlaceholderText("Scientific correlation...")
        scientific_text.setMaximumHeight(70)
        scientific_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 2px solid #008B8B;
            }
        """)
        layout.addWidget(scientific_text)

        # Imbalance Effects
        imbalance_label = QLabel("Imbalance Effects:")
        imbalance_label.setStyleSheet(
            "color: #666; font-size: 11px; font-weight: 600;")
        layout.addWidget(imbalance_label)

        imbalance_text = QTextEdit()
        imbalance_text.setPlaceholderText("Imbalance effects...")
        imbalance_text.setMaximumHeight(70)
        imbalance_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 2px solid #008B8B;
            }
        """)
        layout.addWidget(imbalance_text)

        # Remedies
        remedies_label = QLabel("Remedies:")
        remedies_label.setStyleSheet(
            "color: #666; font-size: 11px; font-weight: 600;")
        layout.addWidget(remedies_label)

        # Diet
        diet_label = QLabel("• Diet:")
        diet_label.setStyleSheet("color: #999; font-size: 11px;")
        layout.addWidget(diet_label)

        diet_text = QTextEdit()
        diet_text.setPlaceholderText("Diet recommendations...")
        diet_text.setMaximumHeight(60)
        diet_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                font-size: 13px;
                margin-left: 10px;
            }
            QTextEdit:focus {
                border: 2px solid #008B8B;
            }
        """)
        layout.addWidget(diet_text)

        # Lifestyle
        lifestyle_label = QLabel("• Lifestyle and Exercise:")
        lifestyle_label.setStyleSheet("color: #999; font-size: 11px;")
        layout.addWidget(lifestyle_label)

        lifestyle_text = QTextEdit()
        lifestyle_text.setPlaceholderText(
            "Lifestyle and exercise recommendations...")
        lifestyle_text.setMaximumHeight(60)
        lifestyle_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                font-size: 13px;
                margin-left: 10px;
            }
            QTextEdit:focus {
                border: 2px solid #008B8B;
            }
        """)
        layout.addWidget(lifestyle_text)

        # Herbal Support
        herbal_label = QLabel("• Herbal or Energy Support:")
        herbal_label.setStyleSheet("color: #999; font-size: 11px;")
        layout.addWidget(herbal_label)

        herbal_text = QTextEdit()
        herbal_text.setPlaceholderText(
            "Herbal or energy support recommendations...")
        herbal_text.setMaximumHeight(60)
        herbal_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                font-size: 13px;
                margin-left: 10px;
            }
            QTextEdit:focus {
                border: 2px solid #008B8B;
            }
        """)
        layout.addWidget(herbal_text)

        # Store field references
        self.element_fields[element_name] = {
            "description": description_text,
            "scientific": scientific_text,
            "imbalance": imbalance_text,
            "diet": diet_text,
            "lifestyle": lifestyle_text,
            "herbal": herbal_text,
            "classification": classification_label
        }

        layout.addSpacing(15)

    def load_assessment_data(self, assessment_data):
        """Load and display AI assessment data with editable fields"""
        self.assessment_data = assessment_data

        # Load Elemental Analysis
        if "Elemental_Analysis" in assessment_data:
            analysis = assessment_data["Elemental_Analysis"]
            for element_name, element_data in analysis.items():
                if element_name in self.element_fields:
                    fields = self.element_fields[element_name]

                    # Set classification
                    classification = element_data.get("Classification", "")
                    fields["classification"].setText(classification)

                    # Set editable fields
                    fields["description"].setPlainText(
                        element_data.get("Description", ""))
                    fields["scientific"].setPlainText(
                        element_data.get("Scientific_Correlation", ""))
                    fields["imbalance"].setPlainText(
                        element_data.get("Imbalance_Effects", ""))

                    # Set remedies
                    remedies = element_data.get("Remedies", {})
                    fields["diet"].setPlainText(
                        remedies.get("Diet", ""))
                    fields["lifestyle"].setPlainText(
                        remedies.get("Lifestyle_and_Exercise", ""))
                    fields["herbal"].setPlainText(
                        remedies.get("Herbal_or_Energy_Support", ""))

        # Load Summary
        if "Summary" in assessment_data:
            self.summary_text.setPlainText(assessment_data["Summary"])

        # Load Disclaimer
        if "Disclaimer" in assessment_data:
            self.disclaimer_text.setPlainText(assessment_data["Disclaimer"])

    def get_edited_assessment_data(self):
        """Retrieve all edited data"""
        edited_data = {
            "Elemental_Analysis": {},
            "Summary": self.summary_text.toPlainText(),
            "Disclaimer": self.disclaimer_text.toPlainText()
        }

        for element_name, fields in self.element_fields.items():
            edited_data["Elemental_Analysis"][element_name] = {
                "Classification": fields["classification"].text(),
                "Description": fields["description"].toPlainText(),
                "Scientific_Correlation": fields["scientific"].toPlainText(),
                "Imbalance_Effects": fields["imbalance"].toPlainText(),
                "Remedies": {
                    "Diet": fields["diet"].toPlainText(),
                    "Lifestyle_and_Exercise": fields["lifestyle"].toPlainText(),
                    "Herbal_or_Energy_Support": fields["herbal"].toPlainText()
                }
            }

        return edited_data
