#!/usr/bin/env python3
"""
Test script to verify text box layout and sizing changes
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from asr_app import ASRApp

def test_text_box_layout():
    """Test the text box layout changes"""
    print("🔍 Testing Text Box Layout Changes")
    print("=" * 50)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create main window
    window = ASRApp()
    
    # Test 1: Check font sizes
    print("1. Testing default font sizes...")
    
    # Check pronunciation text box
    pron_font = window.pronunciation_text.font()
    pron_size = pron_font.pointSize()
    print(f"   Pronunciation text box font size: {pron_size}pt")
    assert pron_size == 14, f"Expected 14pt, got {pron_size}pt"
    
    # Check definition text box
    def_font = window.definition_text.font()
    def_size = def_font.pointSize()
    print(f"   Definition text box font size: {def_size}pt")
    assert def_size == 14, f"Expected 14pt, got {def_size}pt"
    
    # Check pronunciation help text box
    help_font = window.pron_help_text.font()
    help_size = help_font.pointSize()
    print(f"   Pronunciation help text box font size: {help_size}pt")
    assert help_size == 14, f"Expected 14pt, got {help_size}pt"
    
    print("   ✓ All text boxes have 14pt default font size")
    
    # Test 2: Check text box heights
    print("\n2. Testing text box heights...")
    
    # Check pronunciation text box height
    pron_height = window.pronunciation_text.maximumHeight()
    print(f"   Pronunciation text box height: {pron_height}px")
    
    # Check definition text box height
    def_height = window.definition_text.maximumHeight()
    print(f"   Definition text box height: {def_height}px")
    
    # Check pronunciation help text box height
    help_height = window.pron_help_text.maximumHeight()
    print(f"   Pronunciation help text box height: {help_height}px")
    assert help_height == 120, f"Expected 120px for 6 lines, got {help_height}px"
    
    print("   ✓ Pronunciation help text box increased to 120px (6 lines)")
    
    # Test 3: Test clean_ai_response function for blank line removal
    print("\n3. Testing blank line removal...")
    
    # Test with various inputs
    test_cases = [
        ("Simple text", "Simple text"),
        ("Line 1\n\nLine 3", "Line 1\nLine 3"),
        ("  \n  spaced  \n  \n  text  \n  ", "spaced\ntext"),
        ("**bold**\n\nnormal\n```code```", "bold\nnormal\ncode"),
        ("\n\n\n", ""),
    ]
    
    for input_text, expected in test_cases:
        result = window.clean_ai_response(input_text)
        print(f"   Input: {repr(input_text)}")
        print(f"   Output: {repr(result)}")
        print(f"   Expected: {repr(expected)}")
        assert result == expected, f"Mismatch: got {repr(result)}, expected {repr(expected)}"
    
    print("   ✓ Blank line removal working correctly")
    
    # Test 4: Test multiline response handling
    print("\n4. Testing multiline response handling...")
    
    multiline_input = "Line 1\nLine 2\nLine 3"
    multiline_result = window.clean_ai_response(multiline_input)
    print(f"   Multiline input preserved: {multiline_result}")
    assert multiline_result == multiline_input, "Multiline responses should be preserved"
    
    print("   ✓ Multiline responses preserved correctly")
    
    print("\n✅ All text box layout tests passed!")
    print("\n📋 Changes verified:")
    print("   • Default font size set to 14pt for all text boxes")
    print("   • Pronunciation help text box increased to 6 lines (120px)")
    print("   • Blank lines removed from AI responses")
    print("   • Multiline responses properly preserved")
    
    return True

if __name__ == "__main__":
    try:
        success = test_text_box_layout()
        if success:
            print("\n🎉 Text box layout verification completed successfully!")
        else:
            print("\n❌ Text box layout verification failed")
            sys.exit(1)
    except Exception as e:
        print(f"💥 Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)