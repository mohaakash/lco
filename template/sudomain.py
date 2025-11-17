from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import tempfile
import os
import json
from pathlib import Path
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Report Generator")

        layout = QVBoxLayout()
        btn = QPushButton("Generate Report")
        btn.clicked.connect(self.generate_report)
        layout.addWidget(btn)

        self.setLayout(layout)

    def generate_report(self):
        # Example data
        data = {
            "name": "Akash",
            "summary": "This report summarizes the system performance.",
            "items": [
                {"name": "Accuracy", "value": "95%"},
                {"name": "Processing Time", "value": "140ms"},
                {"name": "Model", "value": "YOLOv8m"}
            ]
        }

        # Render HTML from template.
        # Resolve template directory relative to this file so the script works
        # regardless of the current working directory.
        template_dir = Path(__file__).resolve().parents[1] / "ui" / "widgets"
        if not template_dir.exists():
            print(f"Template directory not found: {template_dir}")
            print(f"Current working directory: {Path.cwd()}")
            # Also try a fallback relative path
            fallback = Path("ui") / "widgets"
            print(
                f"Fallback path exists: {fallback.exists()}, fallback={fallback}")

        env = Environment(loader=FileSystemLoader(str(template_dir)))
        try:
            tpl = env.get_template("report.html")
        except Exception as e:
            # Provide diagnostic listing of files in the directory
            try:
                files = list(template_dir.iterdir())
            except Exception:
                files = []
            print(f"Failed to load template 'report.html' from {template_dir}")
            print("Files in template_dir:", files)
            raise
        html_str = tpl.render(**data)

        # Save HTML to a temporary file
        temp_html = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        temp_html.write(html_str.encode("utf-8"))
        temp_html.close()

        # Generate PDF
        output_pdf = "report.pdf"
        HTML(temp_html.name).write_pdf(output_pdf)

        # Cleanup
        os.remove(temp_html.name)

        print("PDF saved as:", output_pdf)


# Example usage
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    # PyQt6 uses exec() instead of the old exec_()
    sys.exit(app.exec())
