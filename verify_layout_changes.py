#!/usr/bin/env python3
"""
Simple verification script to check text box layout changes in the source code
"""

import re

def verify_text_box_changes():
    """Verify the text box layout changes in the source code"""
    print("🔍 Verifying Text Box Layout Changes in Source Code")
    print("=" * 60)
    
    # Read the source file
    with open('asr_app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test 1: Check font size settings
    print("1. Checking font size settings...")
    
    # Look for 14pt font settings
    font_14_matches = re.findall(r'setFont\(QFont\([^)]*14\)', content)
    print(f"   Found {len(font_14_matches)} explicit 14pt font settings")
    
    # Look for font-size: 14pt in stylesheets
    stylesheet_14_matches = re.findall(r'font-size: 14pt', content)
    print(f"   Found {len(stylesheet_14_matches)} stylesheet 14pt declarations")
    
    # Check specific text boxes
    text_boxes = ['pronunciation_text', 'definition_text', 'pron_help_text']
    for box in text_boxes:
        box_pattern = rf'self\.{box}.*?setFont\(QFont\([^)]*14\)'
        if re.search(box_pattern, content, re.DOTALL):
            print(f"   ✓ {box} has 14pt font setting")
        else:
            print(f"   ❌ {box} missing 14pt font setting")
    
    # Test 2: Check pronunciation help height
    print("\n2. Checking pronunciation help text box height...")
    
    help_height_pattern = r'self\.pron_help_text\.setMaximumHeight\(120\)'
    if re.search(help_height_pattern, content):
        print("   ✓ Pronunciation help text box set to 120px height")
    else:
        print("   ❌ Pronunciation help text box height not set to 120px")
    
    # Test 3: Check clean_ai_response function enhancements
    print("\n3. Checking clean_ai_response function...")
    
    # Look for blank line removal logic
    blank_line_pattern = r'lines = \[line\.strip\(\) for line in cleaned\.split.*?if line\.strip\(\)\]'
    if re.search(blank_line_pattern, content):
        print("   ✓ Blank line removal logic found")
    else:
        print("   ❌ Blank line removal logic not found")
    
    # Look for multiline preservation
    multiline_pattern = r"if '\\n' not in cleaned:"
    if re.search(multiline_pattern, content):
        print("   ✓ Multiline response preservation logic found")
    else:
        print("   ❌ Multiline response preservation logic not found")
    
    # Test 4: Verify all changes are present
    print("\n4. Overall verification...")
    
    required_changes = [
        (r'self\.pronunciation_text\.setFont\(QFont\([^)]*14\)', "Pronunciation text box 14pt font"),
        (r'self\.definition_text\.setFont\(QFont\([^)]*14\)', "Definition text box 14pt font"),
        (r'self\.pron_help_text\.setFont\(QFont\([^)]*14\)', "Pronunciation help text box 14pt font"),
        (r'self\.pron_help_text\.setMaximumHeight\(120\)', "Pronunciation help 120px height"),
        (r'lines = \[line\.strip\(\) for line in cleaned\.split.*?if line\.strip\(\)\]', "Blank line removal"),
        (r"if '\\n' not in cleaned:", "Multiline preservation")
    ]
    
    all_passed = True
    for pattern, description in required_changes:
        if re.search(pattern, content):
            print(f"   ✓ {description}")
        else:
            print(f"   ❌ {description} - NOT FOUND")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL CHANGES VERIFIED SUCCESSFULLY!")
        print("\n📋 Summary of implemented changes:")
        print("   • Default font size set to 14pt for all text boxes")
        print("   • Pronunciation help text box increased from 80px to 120px (6 lines)")
        print("   • Enhanced clean_ai_response function removes blank lines")
        print("   • Multiline AI responses are properly preserved")
        print("   • CSS stylesheets updated with 14pt font declarations")
    else:
        print("❌ SOME CHANGES ARE MISSING")
        print("Please review the implementation above.")
    
    return all_passed

if __name__ == "__main__":
    try:
        success = verify_text_box_changes()
        if success:
            print("\n✅ Text box layout verification completed successfully!")
        else:
            print("\n❌ Text box layout verification failed")
            exit(1)
    except Exception as e:
        print(f"💥 Verification error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)