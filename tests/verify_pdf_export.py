import sys
import os
import base64
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_pdf_template_rendering():
    print("Testing PDF template rendering...")
    
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
    ctx['human_png'] = load_image_b64('human.png')
    
    # Render
    try:
        tpl_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui/widgets'))
        env = Environment(loader=FileSystemLoader(tpl_dir),
                          autoescape=select_autoescape(['html', 'xml']))
        template = env.get_template('report.html')
        
        output_html = template.render(**ctx)
        
        output_path = "tests/test_report_render.html"
        with open(output_path, "w") as f:
            f.write(output_html)
            
        print(f"Success! Rendered HTML saved to {output_path}")
        print(f"HTML size: {len(output_html)} bytes")
        
        # Check for image inclusion
        if ctx['logo_png'] and ctx['logo_png'] in output_html:
            print("Logo image found in output.")
        else:
            print("Warning: Logo image not found in output (or image missing).")
            
        if ctx['human_png'] and ctx['human_png'] in output_html:
            print("Human image found in output.")
        else:
            print("Warning: Human image not found in output (or image missing).")
            
    except Exception as e:
        print(f"Rendering failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_template_rendering()
