import sys
import os
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_all_keys_rendered():
    print("Testing that all JSON keys are rendered in HTML...")
    
    # Use actual fire_high_fixed structure
    fire_high_data = {
        "The Fire Element": "Fire element description...",
        "Physique": "Lean or stream-lined with powerful muscles...",
        "Temperament": "Choleric, bilious-nervous...",
        "Assessing Your Fire Balance": "To check how your Fire is doing...",
        "Urine": "Light-colored urine may indicate...",
        "Skin": "A rosy or red complexion...",
        "Eyes": "Bright, clear eyes show balanced Fire...",
        "Digestion": "With high Fire, you get super hungry...",
        "Emotions": "Balanced Fire brings cheerfulness...",
        "Immunity": "Fire gives you that fighter's edge...",
        "What Excess Fire Feels Like—and Why You Need to Rein It In": "If you've got excess Fire...",
        "Ways to Balance Excess Fire": "Cooling, hydrating, and grounding...",
        "Diet": "Go for cooling, hydrating foods...",
        "Lifestyle and Exercise": "Cool off with swimming...",
        "Herbs": "Herbs like hops, violet, aloe..."
    }
    
    data = {
        "Element_Percentages": {"Fire": 25, "Earth": 25, "Air": 25, "Water": 25},
        "Element_Descriptions": {
            "Fire": fire_high_data,
            "Earth": {},
            "Air": {},
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
        
        output_path = "tests/test_all_keys_render.html"
        with open(output_path, "w") as f:
            f.write(output_html)
            
        print(f"Success! Rendered HTML saved to {output_path}")
        
        # Check for each key
        missing_keys = []
        found_keys = []
        
        check_keys = [
            "Physique",
            "Temperament", 
            "Assessing Your Fire Balance",
            "Urine",
            "Skin",
            "Eyes",
            "Digestion",
            "Emotions",
            "Immunity",
            "Herbs"
        ]
        
        for key in check_keys:
            if key in output_html:
                found_keys.append(key)
                print(f"✓ Found: {key}")
            else:
                missing_keys.append(key)
                print(f"✗ MISSING: {key}")
        
        print(f"\nSummary: {len(found_keys)}/{len(check_keys)} keys found")
        
        if missing_keys:
            print(f"Missing keys: {', '.join(missing_keys)}")
            return False
        else:
            print("All keys successfully rendered!")
            return True
            
    except Exception as e:
        print(f"Rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_all_keys_rendered()
    sys.exit(0 if success else 1)
