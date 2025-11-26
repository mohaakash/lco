import sys
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_comprehensive_rendering():
    print("Testing comprehensive JSON rendering...")
    
    # Create comprehensive test data with various keys
    data = {
        "Element_Percentages": {"Fire": 40, "Earth": 20, "Air": 20, "Water": 20},
        "Element_Descriptions": {
            "Fire": {
                "The Fire Element": "Fire description...",
                "Physique": "Lean or stream-lined...",
                "Temperament": "Choleric...",
                "Assessing Your Fire Balance": "To check how your Fire is doing...",
                "Urine": "Light-colored urine...",
                "Skin": "A rosy or red complexion...",
                "Eyes": "Bright, clear eyes...",
                "Digestion": "With high Fire...",
                "Emotions": "Balanced Fire brings...",
                "Immunity": "Fire gives you...",
                "What Excess Fire Feels Like—and Why You Need to Rein It In": "If you've got excess Fire...",
                "Ways to Balance Excess Fire": "Cooling, hydrating...",
                "Diet": "Go for cooling foods...",
                "Lifestyle and Exercise": "Cool off with swimming...",
                "Herbs": "Herbs like hops..."
            },
            "Earth": {},
            "Air": {},
            "Water": {}
        },
        "Daily_Routine": {
            "Morning": {
                "Diet": "Morning diet recommendations...",
                "Lifestyle": "Morning lifestyle...",
                "Exercise": "Morning exercise..."
            },
            "Midday": {
                "Diet": "Midday diet...",
                "Lifestyle": "Midday lifestyle..."
            },
            "Evening": {
                "Diet": "Evening diet...",
                "Lifestyle": "Evening lifestyle..."
            },
            "Weekly_Addition": "Weekly addition content...",
            "Extra_Custom_Key": "This is an extra key that should also render..."
        },
        "Modality_Descriptions": {
            "Cardinal": {
                "Cardinal_Energy": {
                    "Cardinal Energy": "Cardinal energy description...",
                    "General Traits": "Cardinal traits...",
                    "Physical Effects": "Physical effects..."
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
        
        output_path = "tests/test_comprehensive_render.html"
        with open(output_path, "w") as f:
            f.write(output_html)
            
        print(f"Success! Rendered HTML saved to {output_path}")
        
        # Check for all keys
        checks = [
            # Element keys
            ("Physique", "Element: Physique"),
            ("Temperament", "Element: Temperament"),
            ("Assessing Your Fire Balance", "Element: Assessing Your Fire Balance"),
            ("Urine", "Element: Urine"),
            ("Skin", "Element: Skin"),
            ("Eyes", "Element: Eyes"),
            ("Digestion", "Element: Digestion"),
            ("Emotions", "Element: Emotions"),
            ("Immunity", "Element: Immunity"),
            ("Herbs", "Element: Herbs"),
            # Balance heading
            ("Ways to Balance Excess Fire", "Balance heading"),
            # Daily routine keys
            ("Morning", "Daily Routine: Morning"),
            ("Midday", "Daily Routine: Midday"),
            ("Evening", "Daily Routine: Evening"),
            ("Weekly Addition", "Daily Routine: Weekly Addition"),
            ("Extra Custom Key", "Daily Routine: Extra Custom Key (dynamic)"),
            # Modality keys
            ("Cardinal Energy", "Modality: Cardinal Energy"),
            ("General Traits", "Modality: General Traits"),
            ("Physical Effects", "Modality: Physical Effects"),
        ]
        
        all_passed = True
        for text, desc in checks:
            if text in output_html:
                print(f"✓ Found: {desc}")
            else:
                print(f"✗ MISSING: {desc}")
                all_passed = False
        
        # Summary
        if all_passed:
            print(f"\n✅ All {len(checks)} checks passed!")
        else:
            print(f"\n❌ Some checks failed")
        
        return all_passed
            
    except Exception as e:
        print(f"Rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_comprehensive_rendering()
    sys.exit(0 if success else 1)
