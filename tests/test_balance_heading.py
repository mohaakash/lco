import sys
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_balance_heading():
    print("Testing that balance/remedies heading appears before table...")
    
    # Use actual fire_high_fixed structure with balance heading
    fire_high_data = {
        "The Fire Element": "Fire element description...",
        "Physique": "Lean or stream-lined...",
        "Temperament": "Choleric...",
        "What Excess Fire Feels Like—and Why You Need to Rein It In": "If you've got excess Fire...",
        "Ways to Balance Excess Fire": "Cooling, hydrating, and grounding strategies...",
        "Diet": "Go for cooling, hydrating foods...",
        "Lifestyle and Exercise": "Cool off with swimming...",
        "Herbs": "Herbs like hops, violet, aloe..."
    }
    
    air_low_data = {
        "The Air Element": "Air element description...",
        "Remedies to Balance Low Air": "Balancing low Air requires stimulation...",
        "Diet": "Incorporate light, airy foods...",
        "Lifestyle and Exercise": "Prioritize aerobic exercise..."
    }
    
    data = {
        "Element_Percentages": {"Fire": 40, "Earth": 20, "Air": 20, "Water": 20},
        "Element_Descriptions": {
            "Fire": fire_high_data,
            "Earth": {},
            "Air": air_low_data,
            "Water": {}
        },
        "Daily_Routine": {},
        "Modalities": {},
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
        
        output_path = "tests/test_balance_heading.html"
        with open(output_path, "w") as f:
            f.write(output_html)
            
        print(f"Success! Rendered HTML saved to {output_path}")
        
        # Check for balance headings
        checks = [
            ("Ways to Balance Excess Fire", "Ways to Balance Excess Fire heading"),
            ("Remedies to Balance Low Air", "Remedies to Balance Low Air heading"),
        ]
        
        all_passed = True
        for text, desc in checks:
            if text in output_html:
                print(f"✓ Found: {desc}")
            else:
                print(f"✗ MISSING: {desc}")
                all_passed = False
        
        # Check that "Remedies" heading is NOT present (should be removed)
        if "<h3>Remedies</h3>" in output_html:
            print("✗ FAIL: 'Remedies' heading should not be present")
            all_passed = False
        else:
            print("✓ 'Remedies' heading correctly removed")
        
        # Check that table is still present
        if "<strong>Diet</strong>" in output_html and "<strong>Lifestyle & Exercise</strong>" in output_html:
            print("✓ Remedies table still present")
        else:
            print("✗ FAIL: Remedies table missing")
            all_passed = False
        
        # Check order: balance heading should come before table
        balance_pos = output_html.find("Ways to Balance Excess Fire")
        table_pos = output_html.find("<strong>Diet</strong>")
        
        if balance_pos > 0 and table_pos > 0 and balance_pos < table_pos:
            print("✓ Balance heading appears before remedies table")
        else:
            print(f"✗ FAIL: Balance heading not in correct position (balance_pos={balance_pos}, table_pos={table_pos})")
            all_passed = False
        
        return all_passed
            
    except Exception as e:
        print(f"Rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_balance_heading()
    sys.exit(0 if success else 1)
