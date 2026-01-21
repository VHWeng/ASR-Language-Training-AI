#!/usr/bin/env python3
"""
Simple debug script to check pronunciation help visibility behavior
"""

import sys
import os
import tempfile
import csv
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QEventLoop
from asr_app import ASRApp

def debug_pron_help_visibility():
    """Debug the pronunciation help visibility behavior"""
    print("Debugging Pronunciation Help Visibility")
    print("=" * 40)
    
    app = QApplication(sys.argv)
    window = ASRApp()
    
    # Create minimal test data
    test_data = [
        ['Word', 'Definition', 'English Pron', 'IPA Pron', 'Image Desc', 'Image File'],
        ['test', 'A test word', 'test', 'tɛst', 'Test image', 'test.png']
    ]
    
    # Create temporary CSV
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='', encoding='utf-8') as temp_csv:
        writer = csv.writer(temp_csv, delimiter='|')
        writer.writerows(test_data)
        csv_path = temp_csv.name
    
    try:
        # Load vocabulary
        window.load_csv_vocabulary(csv_path)
        print(f"Loaded {len(window.vocabulary_data)} entries")
        
        # Enable pronunciation help
        print("Enabling pronunciation help...")
        window.show_pron_help_cb.setChecked(True)
        print(f"Checkbox checked: {window.show_pron_help_cb.isChecked()}")
        print(f"Help text visible: {window.pron_help_text.isVisible()}")
        
        # Display first entry
        print("Displaying first entry...")
        window.current_vocab_index = 0
        window.display_current_vocabulary()
        
        print(f"Reference text: '{window.reference_text.text()}'")
        print(f"Help text visible after display: {window.pron_help_text.isVisible()}")
        print(f"Help text content length: {len(window.pron_help_text.toPlainText())}")
        
        # Wait a bit to see if async loading affects visibility
        print("Waiting for potential async operations...")
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)
        loop.exec_()
        
        print(f"Help text visible after wait: {window.pron_help_text.isVisible()}")
        print(f"Help text content after wait: '{window.pron_help_text.toPlainText()[:50]}...'")
        
        return True
        
    finally:
        os.unlink(csv_path)

if __name__ == "__main__":
    try:
        debug_pron_help_visibility()
        print("\nDebug completed")
    except Exception as e:
        print(f"Debug error: {e}")
        import traceback
        traceback.print_exc()