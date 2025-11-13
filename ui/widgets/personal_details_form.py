from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.widgets.custom_input import CustomInput


class PersonalDetailsForm(QWidget):
    next_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main layout with scroll
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet(
            "QScrollArea { background-color: white; border: none; }")

        # Content widget
        content = QWidget()
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Title
        title_label = QLabel("Elemental Balance Assessment")
        title_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 18px;
                font-weight: 600;
            }
        """)
        layout.addWidget(title_label)

        # Element Percentages Section
        element_pct_label = QLabel("Element Percentages")
        element_pct_label.setStyleSheet("""
            QLabel {
                color: #0099CC;
                font-size: 13px;
                font-weight: 600;
            }
        """)
        layout.addWidget(element_pct_label)

        # Fire and Earth row
        fire_earth_layout = QHBoxLayout()
        fire_earth_layout.setSpacing(15)

        self.fire_element = CustomInput("Fire Element (%)")
        self.earth_element = CustomInput("Earth Element (%)")

        fire_earth_layout.addWidget(self.fire_element)
        fire_earth_layout.addWidget(self.earth_element)
        layout.addLayout(fire_earth_layout)

        # Air and Water row
        air_water_layout = QHBoxLayout()
        air_water_layout.setSpacing(15)

        self.air_element = CustomInput("Air Element (%)")
        self.water_element = CustomInput("Water Element (%)")

        air_water_layout.addWidget(self.air_element)
        air_water_layout.addWidget(self.water_element)
        layout.addLayout(air_water_layout)

        # Note
        note_label = QLabel(
            "Note: Any element with 0% will not be included in the analysis.")
        note_label.setStyleSheet("color: #999999; font-size: 11px;")
        layout.addWidget(note_label)

        layout.addSpacing(10)

        # Element Qualities Section
        quality_label = QLabel("Element Qualities (from Kepler's PDF Report)")
        quality_label.setStyleSheet("""
            QLabel {
                color: #0099CC;
                font-size: 13px;
                font-weight: 600;
            }
        """)
        layout.addWidget(quality_label)

        # Cardinal, Fixed, Mutable row
        qualities_layout = QHBoxLayout()
        qualities_layout.setSpacing(15)

        self.cardinal_quality = CustomInput("Cardinal Quality (%)")
        self.fixed_quality = CustomInput("Fixed Quality (%)")
        self.mutable_quality = CustomInput("Mutable Quality (%)")

        qualities_layout.addWidget(self.cardinal_quality)
        qualities_layout.addWidget(self.fixed_quality)
        qualities_layout.addWidget(self.mutable_quality)
        layout.addLayout(qualities_layout)

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
        next_btn.clicked.connect(self.next_clicked.emit)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(next_btn)
        layout.addLayout(btn_layout)

        main_layout.addWidget(scroll)
