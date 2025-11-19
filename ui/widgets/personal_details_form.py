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

        # Contact / Identity fields (added per request)
        identity_label = QLabel("Your Details")
        identity_label.setStyleSheet("""
            QLabel {
                color: #0099CC;
                font-size: 13px;
                font-weight: 600;
            }
        """)
        layout.addWidget(identity_label)

        # Name
        self.full_name = CustomInput("Full Name")
        layout.addWidget(self.full_name)

        # Date, Time, Place of birth row
        dtp_layout = QHBoxLayout()
        dtp_layout.setSpacing(15)

        self.date_of_birth = CustomInput("Date of Birth (YYYY-MM-DD)")
        self.time_of_birth = CustomInput("Time of Birth (HH:MM)")
        self.place_of_birth = CustomInput("Place of Birth")

        dtp_layout.addWidget(self.date_of_birth)
        dtp_layout.addWidget(self.time_of_birth)
        dtp_layout.addWidget(self.place_of_birth)
        layout.addLayout(dtp_layout)

        # Contact row (phone / email)
        contact_layout = QHBoxLayout()
        contact_layout.setSpacing(15)
        self.phone = CustomInput("Phone Number")
        self.email = CustomInput("Email Address")
        contact_layout.addWidget(self.phone)
        contact_layout.addWidget(self.email)
        layout.addLayout(contact_layout)

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

        # Validation message (hidden until needed)
        self._percent_error = QLabel("")
        self._percent_error.setStyleSheet("color: #D83333; font-size: 12px;")
        self._percent_error.setVisible(False)
        layout.addWidget(self._percent_error)

        layout.addSpacing(10)

        # Element Qualities Section
        quality_label = QLabel("Element Qualities")
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

        # Next button (store reference so we can enable/disable)
        self.next_btn = QPushButton("Generate Report")
        self.next_btn.setFixedHeight(45)
        self.next_btn.setStyleSheet("""
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
        # wire click to emit only when valid
        self.next_btn.clicked.connect(self._on_next_clicked)

        # Validate sums whenever any percentage input changes
        for w in (self.fire_element, self.earth_element, self.air_element, self.water_element,
                  self.cardinal_quality, self.fixed_quality, self.mutable_quality):
            try:
                w.textChanged.connect(self._validate_percentages)
            except Exception:
                pass

        # Initial validation
        self._validate_percentages()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_btn)
        layout.addLayout(btn_layout)

        main_layout.addWidget(scroll)

    def _on_next_clicked(self):
        # guard: ensure percentages validate
        if not self._validate_percentages():
            return
        # emit the original signal
        self.next_clicked.emit()

    def _validate_percentages(self):
        """Return True if both element percentages and quality percentages sum to 100.

        Shows a message and disables the Next button if invalid.
        """
        def to_int_safe(s):
            try:
                return int(s)
            except Exception:
                return None

        elems = [to_int_safe(self.fire_element.text()), to_int_safe(self.earth_element.text()),
                 to_int_safe(self.air_element.text()), to_int_safe(self.water_element.text())]
        quals = [to_int_safe(self.cardinal_quality.text()), to_int_safe(self.fixed_quality.text()),
                 to_int_safe(self.mutable_quality.text())]

        # If any is None (non-numeric), show error
        if any(v is None for v in elems + quals):
            self._percent_error.setText(
                "Please enter numeric percentage values for all fields.")
            self._percent_error.setVisible(True)
            try:
                self.next_btn.setEnabled(False)
            except Exception:
                pass
            return False

        elem_sum = sum(elems)
        qual_sum = sum(quals)

        if elem_sum != 100 and qual_sum != 100:
            self._percent_error.setText(
                "Element percentages must sum to 100.\nQualities must also sum to 100.")
            self._percent_error.setVisible(True)
            self.next_btn.setEnabled(False)
            return False
        if elem_sum != 100:
            self._percent_error.setText(
                f"Element percentages sum to {elem_sum} — they must total 100.")
            self._percent_error.setVisible(True)
            self.next_btn.setEnabled(False)
            return False
        if qual_sum != 100:
            self._percent_error.setText(
                f"Quality percentages sum to {qual_sum} — they must total 100.")
            self._percent_error.setVisible(True)
            self.next_btn.setEnabled(False)
            return False

        # OK
        self._percent_error.setVisible(False)
        self.next_btn.setEnabled(True)
        return True
