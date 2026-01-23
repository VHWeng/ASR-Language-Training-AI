#!/usr/bin/env python3
"""
Simple test to verify the core fix for missing data auto-generation
"""

import sys
import os
import tempfile
import csv
from PyQt5.QtWidgets import QApplication
from asr_app import ASRApp

def test_core_functionality():
    """Test the core functionality with a simple example"""
    print("=== Testing Core Missing Data Fix ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = ASRApp()
    
    # Create a very simple test case
    with tempfile.TemporaryDirectory() as temp_dir:
        # Simple CSV with one entry missing all data
        csv_data = [
            ['Word', 'Definition', 'English Pron', 'IPA Pron', 'Image Desc', 'Image File'],
            ['testword', '', '', '', 'Test image', 'test.png']
        ]
        
        csv_path = os.path.join(temp_dir, 'simple_test.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter='|')
            writer.writerows(csv_data)
        
        print("✓ Created simple test CSV")
        
        # Load the CSV
        window.load_csv_vocabulary(csv_path)
        
        print(f"✓ Loaded {len(window.vocabulary_data)} vocabulary entries")
        
        # Display the first (and only) entry
        window.current_vocab_index = 0
        window.display_current_vocabulary()
        
        # Check that text boxes are populated
        reference = window.reference_text.text()
        definition = window.definition_text.toPlainText()
        pronunciation = window.pronunciation_text.toPlainText()
        
        print(f"Reference: '{reference}'")
        print(f"Definition length: {len(definition)} characters")
        print(f"Pronunciation contains 'English:': {'English:' in pronunciation}")
        print(f"Pronunciation contains 'IPA:': {'IPA:' in pronunciation}")
        
        # The key test: ensure no crashes and content is generated
        success = (
            reference == 'testword' and
            len(definition) > 0 and
            'English:' in pronunciation and
            'IPA:' in pronunciation
        )
        
        if success:
            print("✅ SUCCESS: Missing data was automatically generated!")
            return True
        else:
            print("❌ FAILURE: Missing data was not properly handled")
            return False

if __name__ == "__main__":
    try:
        success = test_core_functionality()
        if success:
            print("\n🎉 Core fix is working correctly!")
            sys.exit(0)
        else:
            print("\n❌ Core fix needs more work")
            sys.exit(1)
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)