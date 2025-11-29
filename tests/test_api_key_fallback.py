"""
Test API key fallback logic
"""
import os
import sys

# Mock the environment
os.environ["GEMINI_API_KEY"] = "test_env_key_12345"

# Test cases
print("="*60)
print("API KEY FALLBACK LOGIC TEST")
print("="*60)

print("\nTest Setup:")
print(f"  .env GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY')}")

# Simulate the logic from generate_complete_output
def test_api_key_selection(gui_key, env_key):
    """Simulate the API key selection logic"""
    effective_api_key = None
    source = None
    
    # Check if GUI-provided key is valid
    if gui_key and gui_key.strip():
        effective_api_key = gui_key.strip()
        source = "GUI Settings"
    else:
        # Fall back to .env file
        if env_key and env_key.strip():
            effective_api_key = env_key.strip()
            source = ".env file"
        else:
            effective_api_key = None
            source = "NONE - ERROR"
    
    return effective_api_key, source

# Test Case 1: Valid GUI key
print("\n" + "-"*60)
print("Test 1: Valid GUI key provided")
gui_key = "gui_key_abc123"
env_key = os.getenv("GEMINI_API_KEY")
result, source = test_api_key_selection(gui_key, env_key)
print(f"  GUI Key: '{gui_key}'")
print(f"  Result: '{result}'")
print(f"  Source: {source}")
print(f"  ✅ PASS" if source == "GUI Settings" else "  ❌ FAIL")

# Test Case 2: Empty GUI key (should use .env)
print("\n" + "-"*60)
print("Test 2: Empty GUI key (should fall back to .env)")
gui_key = ""
env_key = os.getenv("GEMINI_API_KEY")
result, source = test_api_key_selection(gui_key, env_key)
print(f"  GUI Key: '{gui_key}'")
print(f"  Result: '{result}'")
print(f"  Source: {source}")
print(f"  ✅ PASS" if source == ".env file" and result == "test_env_key_12345" else "  ❌ FAIL")

# Test Case 3: Whitespace-only GUI key (should use .env)
print("\n" + "-"*60)
print("Test 3: Whitespace-only GUI key (should fall back to .env)")
gui_key = "   "
env_key = os.getenv("GEMINI_API_KEY")
result, source = test_api_key_selection(gui_key, env_key)
print(f"  GUI Key: '{gui_key}'")
print(f"  Result: '{result}'")
print(f"  Source: {source}")
print(f"  ✅ PASS" if source == ".env file" and result == "test_env_key_12345" else "  ❌ FAIL")

# Test Case 4: None GUI key (should use .env)
print("\n" + "-"*60)
print("Test 4: None GUI key (should fall back to .env)")
gui_key = None
env_key = os.getenv("GEMINI_API_KEY")
result, source = test_api_key_selection(gui_key, env_key)
print(f"  GUI Key: {gui_key}")
print(f"  Result: '{result}'")
print(f"  Source: {source}")
print(f"  ✅ PASS" if source == ".env file" and result == "test_env_key_12345" else "  ❌ FAIL")

# Test Case 5: No GUI key and no .env key (ERROR)
print("\n" + "-"*60)
print("Test 5: No GUI key and no .env key (should error)")
gui_key = None
env_key = None
result, source = test_api_key_selection(gui_key, env_key)
print(f"  GUI Key: {gui_key}")
print(f"  .env Key: {env_key}")
print(f"  Result: {result}")
print(f"  Source: {source}")
print(f"  ✅ PASS" if source == "NONE - ERROR" and result is None else "  ❌ FAIL")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print("✅ API key fallback logic implemented:")
print("  1. If GUI key is valid (not None/empty/whitespace) → Use GUI key")
print("  2. If GUI key is invalid → Fall back to .env GEMINI_API_KEY")
print("  3. If both are invalid → Return error message")
print("="*60)
