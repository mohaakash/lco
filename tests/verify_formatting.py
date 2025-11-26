
import sys
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Mock data matching the template structure
data = {
    "Elemental_Percentages": {"Fire": 25, "Earth": 25, "Air": 25, "Water": 25},
    "Element_Descriptions": {
        "Fire": {
            "Description": "Line 1.\nLine 2.",
            "Imbalance Effects": "Effect 1.<br>Effect 2."
        },
        "Earth": {},
        "Air": {},
        "Water": {}
    },
    "Daily_Routine": {},
    "Modalities": {},
    "Summary": "Summary text.",
    "Disclaimer": "Disclaimer text."
}

def verify():
    tpl_dir = "/home/akash/projects/lco/ui/widgets"
    env = Environment(loader=FileSystemLoader(tpl_dir),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('report.html')
    
    html = template.render(**data)
    
    print("Checking Description rendering (newline to <br>)...")
    if "Line 1.<br>Line 2." in html:
        print("SUCCESS: Newlines converted to <br>.")
    elif "Line 1.\nLine 2." in html:
        print("FAIL: Newlines preserved as-is (browsers ignore this).")
    else:
        print(f"FAIL: Unexpected output for description.")
        
    print("\nChecking Imbalance rendering (preservation of <br>)...")
    if "Effect 1.<br>Effect 2." in html:
        print("SUCCESS: <br> tags preserved (safe).")
    elif "Effect 1.&lt;br&gt;Effect 2." in html:
        print("FAIL: <br> tags were escaped.")
    else:
        print("FAIL: Unexpected output for imbalance.")

if __name__ == "__main__":
    verify()
