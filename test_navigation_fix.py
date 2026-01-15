#!/usr/bin/env python3
"""
Test navigation with missing data to ensure the fix works during browsing
"""

import sys
import os
import tempfile
import csv
from PyQt5.QtWidgets import QApplication
from asr_app import ASRApp

def test_navigation_with_missing_data():
    """Test that navigation works properly with auto-generated missing data"""
    print("=== Testing Navigation with Missing Data ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = ASRApp()
    
    # Create test CSV with multiple entries having missing data
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_data = [
            ['Word', 'Definition', 'English Pron', 'IPA Pron', 'Image Desc', 'Image File'],
            ['first', '', '', '', 'First image', 'first.png'],      # Missing everything
            ['second', 'Known def', '', 'sɛkənd', 'Second image', 'second.png'],  # Missing English pron
            ['third', '', 'thurd', '', 'Third image', 'third.png'],   # Missing definition and IPA
            ['fourth', 'Complete def', 'fɔrθ', 'fɔrθ', 'Fourth image', 'fourth.png']  # Complete
        ]
        
        csv_path = os.path.join(temp_dir, 'nav_test.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter='|')
            writer.writerows(csv_data)
        
        print("✓ Created navigation test CSV")
        
        # Load CSV
        window.load_csv_vocabulary(csv_path)
        print(f"✓ Loaded {len(window.vocabulary_data)} entries")
        
        # Test each entry by navigating to it
        results = []
        
        for i in range(len(window.vocabulary_data)):
            print(f"\n--- Testing entry {i+1}: '{window.vocabulary_data[i]['reference']}' ---")
            
            # Navigate to this entry
            window.current_vocab_index = i
            window.display_current_vocabulary()
            
            # Check content
            reference = window.reference_text.text()
            definition = window.definition_text.toPlainText()
            pronunciation = window.pronunciation_text.toPlainText()
            
            print(f"Reference: '{reference}'")
            print(f"Definition: {len(definition)} chars - {'✓' if definition else '✗'}")
            print(f"Pronunciation: {'✓' if 'English:' in pronunciation and 'IPA:' in pronunciation else '✗'}")
            
            # Verify content exists
            has_content = (
                reference and 
                definition and 
                'English:' in pronunciation and 
                'IPA:' in pronunciation
            )
            
            results.append({
                'index': i,
                'reference': reference,
                'has_content': has_content,
                'definition_length': len(definition),
                'pronunciation_valid': 'English:' in pronunciation and 'IPA:' in pronunciation
            })
            
            if not has_content:
                print(f"❌ Entry {i+1} missing required content!")
                return False
        
        # Test forward navigation
        print("\n--- Testing Forward Navigation ---")
        window.current_vocab_index = 0
        
        for i in range(len(window.vocabulary_data) - 1):
            window.next_vocabulary()
            expected_index = i + 1
            actual_index = window.current_vocab_index
            
            if actual_index != expected_index:
                print(f"❌ Forward navigation failed: expected {expected_index}, got {actual_index}")
                return False
            
            # Verify content is still there after navigation
            reference = window.reference_text.text()
            if not reference:
                print(f"❌ No reference text after navigating to entry {actual_index + 1}")
                return False
                
        print("✓ Forward navigation works")
        
        # Test backward navigation
        print("\n--- Testing Backward Navigation ---")
        for i in range(len(window.vocabulary_data) - 1, 0, -1):
            window.previous_vocabulary()
            expected_index = i - 1
            actual_index = window.current_vocab_index
            
            if actual_index != expected_index:
                print(f"❌ Backward navigation failed: expected {expected_index}, got {actual_index}")
                return False
                
            # Verify content is still there after navigation
            reference = window.reference_text.text()
            if not reference:
                print(f"❌ No reference text after navigating to entry {actual_index + 1}")
                return False
        
        print("✓ Backward navigation works")
        
        # Summary
        print(f"\n=== Results Summary ===")
        print(f"Total entries tested: {len(results)}")
        complete_entries = sum(1 for r in results if r['has_content'])
        print(f"Entries with complete content: {complete_entries}/{len(results)}")
        
        if complete_entries == len(results):
            print("✅ ALL TESTS PASSED - Navigation with missing data works perfectly!")
            return True
        else:
            print("❌ Some entries missing content")
            return False

if __name__ == "__main__":
    try:
        success = test_navigation_with_missing_data()
        if success:
            print("\n🎉 Navigation fix is working correctly!")
            sys.exit(0)
        else:
            print("\n❌ Navigation fix needs more work")
            sys.exit(1)
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)