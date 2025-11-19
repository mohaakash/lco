from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QScrollArea, QTextEdit, QFrame,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
import json
from pathlib import Path


class ElementalAssessmentResultForm(QWidget):
    next_clicked = pyqtSignal()
    back_clicked = pyqtSignal()
    # Emitted when the user requests export; payload is HTML string and current assessment data
    export_requested = pyqtSignal(str, dict)

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
        # top toolbar with Edit toggle and Export
        toolbar = QHBoxLayout()
        toolbar.addStretch()
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setFixedHeight(32)
        self.edit_btn.setStyleSheet(
            "background-color:#EEE; border-radius:6px; padding:6px 14px;")
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        toolbar.addWidget(self.edit_btn)

        self.export_btn = QPushButton("Export PDF")
        self.export_btn.setFixedHeight(32)
        self.export_btn.setStyleSheet(
            "background-color:#3EACA8; color:white; border-radius:6px; padding:6px 14px;")
        # When clicked, build the HTML and emit a signal for the parent to handle PDF generation/preview
        self.export_btn.clicked.connect(self.export_pdf)
        toolbar.addWidget(self.export_btn)

        layout.addLayout(toolbar)
        layout.addWidget(title)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #DDDDDD;")
        layout.addWidget(divider)

        # Keep a reference to the content layout so we can rebuild it
        self.content_layout = layout
        # Widgets used for full-report rendering that should be toggled read-only/edit
        self.report_text_widgets = []

        # By default we'll show elemental analysis sections (legacy). If a
        # combined report payload is provided (contains 'Personal'), we'll
        # re-render the layout to show the full report style.
        # Create placeholders for potential legacy fields.
        self.element_fields = {}
        self.summary_text = QTextEdit()
        self.disclaimer_text = QTextEdit()

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

        next_btn = QPushButton("Export Report")
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

        # If this is the combined report payload (includes personal info),
        # render the full report view instead of the legacy editable element sections.
        if isinstance(assessment_data, dict) and "Personal" in assessment_data:
            try:
                self.render_full_report(assessment_data)
                return
            except Exception as e:
                print(f"Error rendering full report: {e}")

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

    def clear_layout(self, layout):
        """Recursively remove widgets from a layout."""
        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                child_layout = item.layout()
                if child_layout is not None:
                    self.clear_layout(child_layout)

    def render_full_report(self, data: dict):
        """Render a nice report UI showing personal details and all AI outputs."""
        layout = self.content_layout

        # Clear existing content and rebuild
        self.clear_layout(layout)

        # Title
        title = QLabel("Elemental Assessment Report")
        title.setStyleSheet("""
            QLabel { color: #000; font-size: 20px; font-weight: 700; }
        """)
        layout.addWidget(title)

        # Personal header
        personal = data.get("Personal", {})
        name = personal.get("name", "")
        dob = personal.get("date_of_birth", "")
        tob = personal.get("time_of_birth", "")
        pob = personal.get("place_of_birth", "")

        header = QLabel(
            f"Name: {name}    |    DOB: {dob} {tob}    |    Place: {pob}")
        header.setStyleSheet(
            "color: #555; font-size: 12px; margin-top:8px; margin-bottom:12px;")
        layout.addWidget(header)

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("background-color: #DDDDDD; margin-bottom:12px;")
        layout.addWidget(div)

        # Elemental Analysis
        elem = data.get("Elemental_Analysis") or data.get(
            "Elemental Analysis") or {}
        if elem:
            section_label = QLabel("Elemental Analysis")
            section_label.setStyleSheet(
                "color:#008B8B; font-weight:600; margin-top:8px;")
            layout.addWidget(section_label)

            for el_name, el_data in elem.items():
                el_header = QLabel(
                    f"{el_name} — {el_data.get('Classification', '')}")
                el_header.setStyleSheet(
                    "color:#333; font-weight:600; margin-top:10px;")
                layout.addWidget(el_header)

                parts = []
                for key in ("Description", "Scientific_Correlation", "Imbalance_Effects"):
                    if el_data.get(key):
                        parts.append(
                            f"<b>{key.replace('_', ' ')}</b>: {el_data.get(key)}")

                remedies = el_data.get("Remedies") or {}
                if remedies:
                    rem_parts = []
                    for rk in ("Diet", "Lifestyle_and_Exercise", "Herbal_or_Energy_Support"):
                        if remedies.get(rk):
                            rem_parts.append(
                                f"<b>{rk.replace('_', ' ')}</b>: {remedies.get(rk)}")
                    if rem_parts:
                        parts.append("<b>Remedies</b>:<br>" +
                                     "<br>".join(rem_parts))

                el_text = QTextEdit()
                el_text.setReadOnly(True)
                el_text.setHtml("<br><br>".join(parts))
                el_text.setStyleSheet(
                    "padding:10px; border:1px solid #DDDDDD; border-radius:6px;")
                el_text.setMinimumHeight(120)
                layout.addWidget(el_text)
                self.report_text_widgets.append(el_text)

        # Modalities
        modalities = data.get("Modalities") or {}
        if modalities and isinstance(modalities, dict):
            mod_label = QLabel("Modalities & Qualities")
            mod_label.setStyleSheet(
                "color:#008B8B; font-weight:600; margin-top:12px;")
            layout.addWidget(mod_label)

            for mod_name, mod_content in modalities.items():
                pct = ''
                if isinstance(mod_content, dict):
                    pct = mod_content.get('Percentage', '')

                m_header = QLabel(f"{mod_name} {('— ' + pct) if pct else ''}")
                m_header.setStyleSheet(
                    "color:#333; font-weight:600; margin-top:8px;")
                layout.addWidget(m_header)

                html_parts = []
                if isinstance(mod_content, dict):
                    for k, v in mod_content.items():
                        if k == 'Percentage' or not v:
                            continue
                        html_parts.append(f"<b>{k.replace('_', ' ')}</b>: {v}")
                else:
                    html_parts.append(str(mod_content))

                m_text = QTextEdit()
                m_text.setReadOnly(True)
                m_text.setHtml("<br><br>".join(html_parts))
                m_text.setStyleSheet(
                    "padding:10px; border:1px solid #DDDDDD; border-radius:6px;")
                m_text.setMinimumHeight(110)
                layout.addWidget(m_text)
                self.report_text_widgets.append(m_text)

        # Daily Guideline
        daily = data.get("Daily_Guideline") or {}
        if daily and isinstance(daily, dict):
            daily_label = QLabel("Daily Guideline")
            daily_label.setStyleSheet(
                "color:#008B8B; font-weight:600; margin-top:12px;")
            layout.addWidget(daily_label)

            for period, content in daily.items():
                p_header = QLabel(period)
                p_header.setStyleSheet(
                    "color:#333; font-weight:600; margin-top:8px;")
                layout.addWidget(p_header)

                if isinstance(content, dict):
                    html_parts = []
                    for ck, cv in content.items():
                        if not cv:
                            continue
                        html_parts.append(
                            f"<b>{ck.replace('_', ' ')}</b>: {cv}")
                    p_text = QTextEdit()
                    p_text.setReadOnly(True)
                    p_text.setHtml("<br><br>".join(html_parts))
                    p_text.setStyleSheet(
                        "padding:10px; border:1px solid #DDDDDD; border-radius:6px;")
                    p_text.setMinimumHeight(120)
                    layout.addWidget(p_text)
                    self.report_text_widgets.append(p_text)
                else:
                    p_text = QTextEdit()
                    p_text.setReadOnly(True)
                    p_text.setPlainText(str(content))
                    p_text.setStyleSheet(
                        "padding:10px; border:1px solid #DDDDDD; border-radius:6px;")
                    p_text.setMinimumHeight(80)
                    layout.addWidget(p_text)
                    self.report_text_widgets.append(p_text)

        # Summary
        summary = data.get("Summary") or ""
        if summary:
            sum_label = QLabel("Summary")
            sum_label.setStyleSheet(
                "color:#008B8B; font-weight:600; margin-top:12px;")
            layout.addWidget(sum_label)

            sum_text = QTextEdit()
            sum_text.setPlainText(summary)
            sum_text.setReadOnly(True)
            sum_text.setStyleSheet(
                "padding:10px; border:1px solid #DDDDDD; border-radius:6px;")
            sum_text.setMinimumHeight(100)
            layout.addWidget(sum_text)
            self.report_text_widgets.append(sum_text)

        # Disclaimer
        disclaimer = data.get("Disclaimer") or ""
        if disclaimer:
            disc_label = QLabel("Disclaimer")
            disc_label.setStyleSheet(
                "color:#666; font-weight:600; margin-top:12px;")
            layout.addWidget(disc_label)

            disc_text = QTextEdit()
            disc_text.setPlainText(disclaimer)
            disc_text.setReadOnly(True)
            disc_text.setStyleSheet(
                "padding:10px; border:1px solid #DDDDDD; border-radius:6px;")
            disc_text.setMinimumHeight(80)
            layout.addWidget(disc_text)
            self.report_text_widgets.append(disc_text)

        # Bottom navigation
        nav = QHBoxLayout()
        back = QPushButton("Back")
        back.setFixedHeight(44)
        back.setStyleSheet(
            "background-color:#CCCCCC; border-radius:8px; padding:10px;")
        back.clicked.connect(self.back_clicked.emit)
        nextb = QPushButton("Export Report")
        nextb.setFixedHeight(44)
        nextb.setStyleSheet(
            "background-color:#3EACA8; color:white; border-radius:8px; padding:10px;")
        nextb.clicked.connect(self.next_clicked.emit)
        nav.addWidget(back)
        nav.addStretch()
        nav.addWidget(nextb)
        layout.addLayout(nav)

    def toggle_edit_mode(self):
        """Toggle edit/view mode for the rendered report widgets."""
        currently_editing = getattr(self, '_editing_mode', False)
        new_mode = not currently_editing
        # When new_mode is True we enter editing mode -> widgets should be writable
        for w in getattr(self, 'report_text_widgets', []):
            try:
                w.setReadOnly(not new_mode)
            except Exception:
                pass
        self._editing_mode = new_mode
        # Update button label
        try:
            self.edit_btn.setText('View' if new_mode else 'Edit')
        except Exception:
            pass
        # If we're leaving edit mode, capture edits into assessment_data
        if not new_mode:
            try:
                # Merge edited content where possible
                edited = self.get_edited_assessment_data()
                # Best-effort update
                if isinstance(self.assessment_data, dict):
                    self.assessment_data.update(edited)
            except Exception:
                pass

    def export_pdf(self):
        """Export the currently rendered report to PDF (or HTML fallback)."""
        # Build a simple HTML representation from the report widgets
        html_parts = ["<html><head><meta charset='utf-8'></head><body>"]
        # Title
        html_parts.append("<h1>Elemental Assessment Report</h1>")
        # Include the content of each report widget
        for w in getattr(self, 'report_text_widgets', []):
            try:
                # Prefer rich HTML when available
                html_parts.append(w.toHtml())
            except Exception:
                try:
                    html_parts.append(f"<p>{w.toPlainText()}</p>")
                except Exception:
                    continue

        html_parts.append("</body></html>")
        full_html = "\n".join(html_parts)
        # Emit HTML to parent for PDF generation/preview
        try:
            self.export_requested.emit(full_html, self.assessment_data or {})
            return
        except Exception:
            # Fallback to saving HTML directly if emit failed
            fname, _ = QFileDialog.getSaveFileName(
                self, "Export Report HTML", "", "HTML Files (*.html)")
            if not fname:
                return
            try:
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write(full_html)
                QMessageBox.information(
                    self, 'Exported', f'HTML saved to {fname}')
            except Exception as e:
                QMessageBox.critical(self, 'Export Failed',
                                     f'Could not save HTML: {e}')

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
