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
    
    # Mock data with specific missing content cases
    data = {
        "Personal": {
            "name": "Test User",
            "date_of_birth": "1990-01-01",
            "time_of_birth": "12:00",
            "place_of_birth": "New York"
        },
        "Element_Percentages": {"Fire": 10.55, "Water": 60.45, "Air": 14.5, "Earth": 14.5},
        "Element_Descriptions": {
            "Fire": {
                "Title": "The Transformer", 
                "Content": {
                    "Description": "Fire content...", 
                    "What Low Fire Feels Like—and How It Holds You Back": "Low Fire description here."
                }, 
                "Status": "Low", 
                "Percentage": 10.55
            },
            "Water": {
                "water": {
                    "high": {
                        "The Water Element": "Water content...",
                        "Excess Water": "Excess Water description here."
                    }
                },
                "Status": "High", 
                "Percentage": 60
            },
            "Air": {
                "air": {
                    "low": {
                        "The Air Element": "Air content...",
                        "Low Air": "Low Air description here."
                    }
                },
                "Status": "Low", 
                "Percentage": 15
            }
        },
        "Daily_Routine": {
            "Morning": "Morning routine...",
            "Weekly_Addition": "Weekly addition content here."
        },
        "Modality_Descriptions": {
            "Cardinal": {
                "Cardinal_Energy": {
                    "Cardinal Energy": "Cardinal Energy Title Text",
                    "General Traits": "Cardinal traits..."
                }
            }
        },
        "Modalities_Percentages": {"Cardinal": 50, "Fixed": 25, "Mutable": 25},
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
        
        # Check for specific missing content
        if "Low Fire description here" in output_html:
            print("Verified: Low Fire description present.")
        else:
            print("Error: Low Fire description MISSING.")

        if "Excess Water description here" in output_html:
            print("Verified: Excess Water description present.")
        else:
            print("Error: Excess Water description MISSING.")

        if "Low Air description here" in output_html:
            print("Verified: Low Air description present.")
        else:
            print("Error: Low Air description MISSING.")

        if "Weekly addition content here" in output_html:
            print("Verified: Weekly Addition present.")
        else:
            print("Error: Weekly Addition MISSING.")

        if "Cardinal Energy Title Text" in output_html:
            print("Verified: Cardinal Energy Title present.")
        else:
            print("Error: Cardinal Energy Title MISSING.")
            
        # Check for styling changes
        if "text-align: right;" in output_html:
             print("Verified: Header is right-aligned.")
        else:
             print("Error: Header alignment check failed.")

        if "margin: 0 auto 20px auto;" in output_html:
             print("Verified: Cover image has auto margins.")
        else:
             print("Error: Cover image auto margin check failed.")

        if "color: darkblue;" in output_html:
             print("Verified: Dark blue color found.")
        else:
             print("Error: Dark blue color check failed.")

        # Check for exact float percentages
        if "10.55%" in output_html:
             print("Verified: Exact float percentage (10.55%) found.")
        else:
             print("Error: Exact float percentage (10.55%) MISSING.")

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
