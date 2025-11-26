import sys
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_paragraph_spacing():
    print("Testing paragraph spacing with double newlines...")
    
    # Test data with double newlines
    data = {
        "Element_Percentages": {"Fire": 40, "Earth": 20, "Air": 20, "Water": 20},
        "Element_Descriptions": {
            "Fire": {
                "The Fire Element": "First paragraph.\n\nSecond paragraph.\n\nThird paragraph.",
                "Physique": "Single line physique.",
                "Ways to Balance Excess Fire": "First line.\n\nSecond paragraph with spacing.",
                "Diet": "Diet line 1.\n\nDiet line 2 with spacing."
            },
            "Earth": {},
            "Air": {},
            "Water": {}
        },
        "Daily_Routine": {
            "Morning": {
                "Diet": "Morning diet line 1.\n\nMorning diet line 2."
            }
        },
        "Modality_Descriptions": {
            "Cardinal": {
                "Cardinal_Energy": {
                    "Cardinal Energy": "Cardinal paragraph 1.\n\nCardinal paragraph 2."
                }
            }
        },
        "Modalities_Percentages": {"Cardinal": 50, "Fixed": 25, "Mutable": 25},
        "Summary": "Test Summary",
        "Disclaimer": "Test Disclaimer"
    }
    
    # Render
    try:
        tpl_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui/widgets'))
        env = Environment(loader=FileSystemLoader(tpl_dir),
                          autoescape=select_autoescape(['html', 'xml']))
        template = env.get_template('report.html')
        
        output_html = template.render(**data)
        
        output_path = "tests/test_paragraph_spacing.html"
        with open(output_path, "w") as f:
            f.write(output_html)
            
        print(f"Success! Rendered HTML saved to {output_path}")
        
        # Check for double <br> tags (paragraph spacing)
        checks = [
            ("First paragraph.<br><br>Second paragraph.", "Element description paragraph spacing"),
            ("First line.<br><br>Second paragraph with spacing.", "Balance heading paragraph spacing"),
            ("Diet line 1.<br><br>Diet line 2 with spacing.", "Remedies table paragraph spacing"),
            ("Morning diet line 1.<br><br>Morning diet line 2.", "Daily routine paragraph spacing"),
            ("Cardinal paragraph 1.<br><br>Cardinal paragraph 2.", "Modality paragraph spacing"),
        ]
        
        all_passed = True
        for text, desc in checks:
            if text in output_html:
                print(f"✓ Found: {desc}")
            else:
                print(f"✗ MISSING: {desc}")
                all_passed = False
        
        if all_passed:
            print(f"\n✅ All {len(checks)} paragraph spacing checks passed!")
        else:
            print(f"\n❌ Some checks failed")
        
        return all_passed
            
    except Exception as e:
        print(f"Rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_paragraph_spacing()
    sys.exit(0 if success else 1)
