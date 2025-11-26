import sys
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_dynamic_fonts():
    print("Testing dynamic font rendering...")
    
    # Mock data
    data = {
        "Element_Percentages": {},
        "Element_Descriptions": {},
        "Daily_Routine": {},
        "Modality_Descriptions": {},
        "Modalities_Percentages": {},
        "Summary": "Test",
        "Disclaimer": "Test",
        # Dynamic settings
        "body_font_size": 14,
        "title_font_size": 24
    }
    
    # Render
    try:
        tpl_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui/widgets'))
        env = Environment(loader=FileSystemLoader(tpl_dir),
                          autoescape=select_autoescape(['html', 'xml']))
        template = env.get_template('report.html')
        
        output_html = template.render(**data)
        
        output_path = "tests/test_dynamic_fonts.html"
        with open(output_path, "w") as f:
            f.write(output_html)
            
        print(f"Success! Rendered HTML saved to {output_path}")
        
        # Checks
        checks = [
            ("font-size: 14pt;", "Body Font Size 14pt"),
            ("font-size: 24pt;", "Title Font Size 24pt"),
            ("font-size: 22pt;", "H2 Font Size (24-2=22pt)"),
            ("font-size: 20pt;", "H3 Font Size (24-4=20pt)")
        ]
        
        all_passed = True
        for text, desc in checks:
            if text in output_html:
                print(f"✓ Found: {desc}")
            else:
                print(f"✗ MISSING: {desc}")
                all_passed = False
        
        if all_passed:
            print(f"\n✅ All checks passed!")
        else:
            print(f"\n❌ Some checks failed")
        
        return all_passed
            
    except Exception as e:
        print(f"Rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_dynamic_fonts()
    sys.exit(0 if success else 1)
