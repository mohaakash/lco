import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.utils.docx_generator import DocxReportGenerator

def test_docx_generation():
    output_path = "tests/test_report.docx"
    
    # Sample data matching the structure from ai/complete_report.py and UI mapping
    data = {
        "Personal": {
            "name": "Test User",
            "date_of_birth": "1990-01-01",
            "time_of_birth": "12:00",
            "place_of_birth": "New York, USA",
            "phone": "555-0123",
            "email": "test@example.com"
        },
        "Element_Percentages": {
            "Fire": 25,
            "Earth": 25,
            "Air": 25,
            "Water": 25
        },
        "Modalities_Percentages": {
            "Cardinal": 33,
            "Fixed": 33,
            "Mutable": 34
        },
        "Element_Descriptions": {
            "Fire": {
                "Title": "The Transformer",
                "Content": {
                    "Description": "Fire is the element of transformation...",
                    "Scientific Correlation": "Associated with metabolism...",
                    "Imbalance Effects": "Burnout, inflammation...",
                    "Diet": "Cooling foods...",
                    "Lifestyle and Exercise": "Swimming...",
                    "Gems, Flower Remedies, and Aromas": "Sandalwood..."
                },
                "Status": "Balanced",
                "Percentage": 25
            },
            "Water": {
                "Title": "The Feeler",
                "Content": "Water represents emotion and intuition...",
                "Status": "High",
                "Percentage": 36
            }
        },
        "Daily_Routine": {
            "Morning": {
                "Activity": "Wake up early",
                "Breakfast": "Light meal"
            },
            "Evening": "Wind down with reading"
        },
        "Modality_Descriptions": {
            "Cardinal": {
                "Title": "The Initiator",
                "Content": {
                    "Description": "Cardinal signs start things...",
                    "Traits": "Active, ambitious"
                },
                "Percentage": 33
            },
            "Fixed": {
                "Content": "Fixed signs stabilize...",
                "Percentage": 33
            }
        },
        "Summary": "This is a test summary of the report.",
        "Disclaimer": "This is a test disclaimer."
    }

    print(f"Generating Docx report to {output_path}...")
    try:
        generator = DocxReportGenerator(output_path)
        generator.generate(data)
        
        if os.path.exists(output_path):
            print(f"Success! File created at {output_path}")
            print(f"File size: {os.path.getsize(output_path)} bytes")
        else:
            print("Error: File was not created.")
            
    except Exception as e:
        print(f"Error during generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_docx_generation()
