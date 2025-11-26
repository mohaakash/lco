import sys
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_balanced_hidden():
    print("Testing balanced elements hidden rendering...")
    
    # Mock data
    data = {
        "Element_Percentages": {"Fire": 40, "Earth": 20, "Air": 20, "Water": 20},
        "Element_Descriptions": {
            "Fire": {
                "Status": "Balanced",
                "The Fire Element": "Fire description should be hidden.",
                "Content": {"The Fire Element": "Fire description hidden."}
            },
            "Earth": {
                "Status": "High",
                "The Earth Element": "Earth description visible.",
                "Content": {"The Earth Element": "Earth description visible."}
            }
        },
        "Daily_Routine": {},
        "Modality_Descriptions": {},
        "Modalities_Percentages": {},
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
        
        output_path = "tests/test_balanced_hidden.html"
        with open(output_path, "w") as f:
            f.write(output_html)
            
        print(f"Success! Rendered HTML saved to {output_path}")
        
        # Checks
        checks = [
            # Fire (Balanced) - Should be HIDDEN
            ("<h2>The Fire Element</h2>", False, "Fire Title (Hidden)"),
            ("Fire description should be hidden", False, "Fire Description (Hidden)"),
            
            # Earth (High) - Should be VISIBLE
            ("<h2>The Earth Element</h2>", True, "Earth Title (Visible)"),
            ("Earth description visible", True, "Earth Description (Visible)"),
        ]
        
        all_passed = True
        for text, should_exist, desc in checks:
            exists = text in output_html
            if exists == should_exist:
                print(f"✓ Correct: {desc} {'found' if exists else 'not found'}")
            else:
                print(f"✗ FAILED: {desc} {'found' if exists else 'not found'} but expected {'found' if should_exist else 'not found'}")
                all_passed = False
        
        # Check for balanced div
        if '<div class="element-balanced">' in output_html:
             print("✓ Found 'element-balanced' div")
        else:
             print("✗ MISSING 'element-balanced' div")
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
    success = test_balanced_hidden()
    sys.exit(0 if success else 1)
