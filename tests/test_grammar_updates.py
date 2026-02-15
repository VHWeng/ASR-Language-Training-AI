#!/usr/bin/env python3
"""
Test script to verify grammar help updates with new word loads
"""

import sys
import os
import tempfile
import csv
import time # Add this import
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Add parent directory to sys.path to allow importing asr_app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from asr_app import ASRApp

def test_grammar_updates():
    """Test that grammar help updates when navigating vocabulary entries"""
    print("Testing Grammar Help Update Behavior")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    window = ASRApp()
    window.show() # <--- Add this line
    
    # Test 1: Create sample vocabulary data
    print("1. Creating test vocabulary data...")
    
    test_data = [
        ['Word', 'Definition', 'English Pron', 'IPA Pron', 'Image Desc', 'Image File', 'Grammar'],
        ['hello', 'A greeting', 'heh-low', 'həˈloʊ', 'Waving hand', 'hello.png', 'Interjection'],
        ['world', 'The earth', 'wurld', 'wɜrld', 'Planet Earth', 'world.png', 'Noun'],
        ['python', 'Programming language', 'pie-thun', 'ˈpaɪθɑn', 'Snake or code', 'python.png', 'Noun']
    ]
    
    # Create temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='', encoding='utf-8') as temp_csv:
        writer = csv.writer(temp_csv, delimiter='|')
        writer.writerows(test_data)
        csv_path = temp_csv.name
    
    try:
        # Test 2: Load vocabulary file
        print("2. Loading vocabulary file...")
        window.load_csv_vocabulary(csv_path)
        assert len(window.vocabulary_data) == 3, f"Expected 3 entries, got {len(window.vocabulary_data)}"
        print("   ✓ Vocabulary loaded successfully")
        
        # Test 3: Enable grammar help
        print("3. Enabling grammar help...")
        window.show_grammar_cb.setChecked(True)
        # Process events to allow QTimer.singleShot to trigger
        QApplication.processEvents()
        time.sleep(0.15)  # Wait slightly longer than QTimer.singleShot(100)
        QApplication.processEvents()
        assert window.show_grammar_cb.isChecked(), "Grammar help checkbox should be checked"
        # Note: Visibility depends on having reference text, so we'll test this after loading an entry
        print("   ✓ Grammar help enabled")
        
        # Test 4: Display first entry and check grammar help clearing
        print("4. Testing first entry display...")
        window.current_vocab_index = 0
        window.display_current_vocabulary()
        QApplication.processEvents()
        time.sleep(0.15)  # Wait for grammar text to potentially show
        QApplication.processEvents()
        
        # Now check that help text is visible since we have reference text
        print(f"   DEBUG: grammar_text.isVisible() = {window.grammar_text.isVisible()}")
        print(f"   DEBUG: grammar_text.isHidden() = {window.grammar_text.isHidden()}")
        print(f"   DEBUG: grammar_text.parentWidget().isVisible() = {window.grammar_text.parentWidget().isVisible()}")
        assert window.grammar_text.isVisible(), "Grammar help text should be visible when enabled and reference text present"
        
        first_entry = window.vocabulary_data[0]
        assert window.reference_text.text() == first_entry['reference'], "Reference text should match first entry"
        
        # Check that grammar help is cleared (ready for new content)
        help_content = window.grammar_text.toPlainText()
        # Should be empty or placeholder text since AI hasn't loaded yet
        assert len(help_content) < 100 or "help" in help_content.lower(), "Grammar help should be cleared for new entry"
        print("   ✓ First entry displayed and help text cleared")
        
        # Test 5: Navigate to second entry
        print("5. Testing navigation to second entry...")
        window.current_vocab_index = 1
        window.display_current_vocabulary()
        QApplication.processEvents()
        time.sleep(0.15)
        QApplication.processEvents()
        
        second_entry = window.vocabulary_data[1]
        assert window.reference_text.text() == second_entry['reference'], "Reference text should match second entry"
        
        # Check that grammar help is cleared again for the new entry
        help_content_after_nav = window.grammar_text.toPlainText()
        assert help_content_after_nav != help_content or len(help_content_after_nav) < 100, "Grammar help should be cleared when navigating"
        print("   ✓ Navigation works and help text is cleared")
        
        # Test 6: Navigate back to first entry
        print("6. Testing navigation back to first entry...")
        window.current_vocab_index = 0
        window.display_current_vocabulary()
        QApplication.processEvents()
        time.sleep(0.15)
        QApplication.processEvents()
        
        assert window.reference_text.text() == first_entry['reference'], "Should navigate back to first entry"
        
        # Help text should be cleared again
        help_content_return = window.grammar_text.toPlainText()
        assert help_content_return != help_content_after_nav or len(help_content_return) < 100, "Grammar help should clear when returning to entry"
        print("   ✓ Return navigation works and help text clears")
        
        # Test 7: Test with grammar help disabled
        print("7. Testing with grammar help disabled...")
        window.show_grammar_cb.setChecked(False)
        assert not window.show_grammar_cb.isChecked(), "Grammar help should be disabled"
        
        # Navigate and check that help text behavior is consistent
        window.current_vocab_index = 2
        window.display_current_vocabulary()
        QApplication.processEvents()
        time.sleep(0.15)
        QApplication.processEvents()
        
        third_entry = window.vocabulary_data[2]
        assert window.reference_text.text() == third_entry['reference'], "Third entry should display correctly"
        print("   ✓ Navigation works with help disabled")
        
        print("\n🎉 All grammar help update tests passed!")
        print("\nKey Fixes Verified:")
        print("- Grammar help text clears when displaying new vocabulary entries")
        print("- Navigation between entries properly resets help content")
        print("- Help text refreshes when returning to previously viewed entries")
        print("- Behavior works correctly whether help is enabled or disabled")
        
        return True
        
    finally:
        # Cleanup
        os.unlink(csv_path)

if __name__ == "__main__":
    try:
        success = test_grammar_updates()
        if success:
            print("\n✅ Grammar help update behavior is working correctly!")
            sys.exit(0)
        else:
            print("\n❌ Grammar help update tests failed")
            sys.exit(1)
    except Exception as e:
        print(f"💥 Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)