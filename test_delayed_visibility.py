#!/usr/bin/env python3
"""
Workaround test using delayed visibility setting
"""

import sys
import os
import tempfile
import csv
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from asr_app import ASRApp

def test_delayed_visibility():
    """Test setting visibility with delay to ensure proper initialization"""
    print("Testing Delayed Visibility Workaround")
    print("=" * 40)
    
    app = QApplication(sys.argv)
    window = ASRApp()
    
    # Create test data
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
        
        # Enable pronunciation help with delay
        def delayed_enable():
            print("Setting checkbox with delay...")
            window.show_pron_help_cb.setChecked(True)
            print(f"Checkbox checked: {window.show_pron_help_cb.isChecked()}")
            print(f"Help text visible: {window.pron_help_text.isVisible()}")
            
            # Try multiple approaches to show the widget
            window.pron_help_text.show()
            window.pron_help_text.setVisible(True)
            window.pron_help_text.raise_()  # Bring to front
            
            # Force a repaint
            window.pron_help_text.repaint()
            window.pron_help_text.update()
            
            print(f"Help text visible after direct manipulation: {window.pron_help_text.isVisible()}")
            
            # Display entry
            window.current_vocab_index = 0
            window.display_current_vocabulary()
            print(f"Help text visible after display: {window.pron_help_text.isVisible()}")
        
        # Use timer to delay the operation
        QTimer.singleShot(100, delayed_enable)
        
        # Start event loop for a short time to process events
        loop = app.exec_()
        
        return True
        
    finally:
        os.unlink(csv_path)

if __name__ == "__main__":
    try:
        test_delayed_visibility()
        print("\nDelayed visibility test completed")
    except Exception as e:
        print(f"Test error: {e}")
        import traceback
        traceback.print_exc()