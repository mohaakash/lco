import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.complete_report import generate_complete_output

def test_mapping_logic():
    # Simulate user input
    user_input = {
        "fire": 25,
        "earth": 25,
        "air": 25,
        "water": 25,
        "cardinal": 33,
        "fixed": 33,
        "mutable": 34
    }

    print("Generating report...")
    full_report = generate_complete_output(user_input)
    
    print("\n--- Full Report Keys ---")
    print(full_report.keys())

    # Simulate the mapping logic from AccountCreationWidget._on_generation_finished
    print("\n--- Testing Mapping Logic ---")
    
    elemental_src = full_report.get("Element_Descriptions", {}) or {}
    elemental_map = {}
    
    for ename, ed in elemental_src.items():
        if not isinstance(ed, dict):
            continue
        
        content_data = ed.get("Content")
        description = ""
        scientific = ""
        imbalance = ""
        remedies = {}
        
        if isinstance(content_data, dict):
            description = content_data.get("The Fire Element") or content_data.get("The Earth Element") or \
                          content_data.get("The Air Element") or content_data.get("The Water Element") or \
                          content_data.get("Description") or ""
                          
            scientific = content_data.get("Scientific Correlation") or ""
            
            imbalance_parts = []
            if content_data.get("What Low Fire Feels Like—and How It Holds You Back"):
                imbalance_parts.append(content_data.get("What Low Fire Feels Like—and How It Holds You Back"))
            if content_data.get("What Excess Fire Feels Like—and Why You Need to Rein It In"):
                imbalance_parts.append(content_data.get("What Excess Fire Feels Like—and Why You Need to Rein It In"))
            if content_data.get("Imbalance Effects"):
                imbalance_parts.append(content_data.get("Imbalance Effects"))
                
            imbalance = "\n\n".join(imbalance_parts)
            
            remedies = {
                "Diet": content_data.get("Diet", ""),
                "Lifestyle_and_Exercise": content_data.get("Lifestyle and Exercise", ""),
                "Herbal_or_Energy_Support": content_data.get("Gems, Flower Remedies, and Aromas") or \
                                            content_data.get("Herbs") or \
                                            content_data.get("Crystals, Gems, and Herbal Remedies") or ""
            }
        elif isinstance(content_data, str):
            description = content_data
        
        elemental_map[ename] = {
            "Classification": ed.get("Title", ""),
            "Description": description[:50] + "..." if description else "",
            "Scientific_Correlation": scientific[:50] + "..." if scientific else "",
            "Imbalance_Effects": imbalance[:50] + "..." if imbalance else "",
            "Remedies": {k: v[:50] + "..." if v else "" for k, v in remedies.items()},
            "Status": ed.get("Status", ""),
            "Percentage": ed.get("Percentage", 0)
        }

    print(json.dumps(elemental_map, indent=2))
    
    # Check Modalities
    modalities_src = full_report.get("Modality_Descriptions", {}) or {}
    modalities_map = {}
    
    for mname, mcontent in modalities_src.items():
        content_dict = {}
        if isinstance(mcontent, dict):
            if len(mcontent) == 1 and isinstance(list(mcontent.values())[0], dict):
                content_dict = list(mcontent.values())[0]
            else:
                content_dict = mcontent
        
        modalities_map[mname] = {
            "Content": content_dict,
            "Percentage": full_report.get("Modalities_Percentages", {}).get(mname, 0)
        }
        
    print("\n--- Modalities Map ---")
    print(json.dumps(modalities_map, indent=2))

if __name__ == "__main__":
    test_mapping_logic()
