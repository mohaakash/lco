import sys
import os
import base64
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import tempfile

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_pdf_generation():
    print("Testing PDF generation with WeasyPrint...")
    
    try:
        from weasyprint import HTML
        print("WeasyPrint imported successfully.")
    except ImportError:
        print("Error: WeasyPrint not found!")
        return

    # Mock data
    data = {
        "Personal": {
            "name": "Test User",
            "date_of_birth": "1990-01-01",
            "time_of_birth": "12:00",
            "place_of_birth": "New York"
        },
        "Element_Percentages": {"Fire": 40, "Water": 60},
        "Element_Descriptions": {
            "Fire": {"Title": "The Transformer", "Content": "Fire content...", "Status": "High", "Percentage": 40},
            "Water": {"Title": "The Feeler", "Content": {"Description": "Water content..."}, "Status": "Balanced", "Percentage": 60}
        },
        "Summary": "Test Summary",
        "Disclaimer": "Test Disclaimer"
    }
    
    # Load images
    def load_image_b64(filename):
        try:
            img_path = Path(os.getcwd()) / 'images' / filename
            if img_path.exists():
                with open(img_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error loading image {filename}: {e}")
        return None

    ctx = data.copy()
    ctx['report_date'] = datetime.date.today().strftime("%B %d, %Y")
    ctx['logo_png'] = load_image_b64('logo.png')
    ctx['cover_image_png'] = load_image_b64('coverimage.png')
    
    # Render HTML
    try:
        tpl_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui/widgets'))
        env = Environment(loader=FileSystemLoader(tpl_dir),
                          autoescape=select_autoescape(['html', 'xml']))
        template = env.get_template('report.html')
        
        output_html = template.render(**ctx)
        print("HTML rendered successfully.")
        
        # Generate PDF
        output_pdf_path = "tests/test_report_weasyprint.pdf"
        HTML(string=output_html).write_pdf(output_pdf_path)
        
        if os.path.exists(output_pdf_path):
            print(f"Success! PDF generated at {output_pdf_path}")
            print(f"PDF size: {os.path.getsize(output_pdf_path)} bytes")
        else:
            print("Error: PDF file was not created.")
            
    except Exception as e:
        print(f"PDF generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_generation()
