#!/usr/bin/env python3
"""
Debug widget hierarchy and parent relationships
"""

import sys
import os
import tempfile
import csv
from PyQt5.QtWidgets import QApplication
from asr_app import ASRApp

def debug_widget_hierarchy():
    """Debug the widget hierarchy and parent relationships"""
    print("Debugging Widget Hierarchy")
    print("=" * 30)
    
    app = QApplication(sys.argv)
    window = ASRApp()
    
    # Print widget information
    print("Pronunciation Help Text Widget Info:")
    print(f"  Object name: {window.pron_help_text.objectName()}")
    print(f"  Parent widget: {window.pron_help_text.parent()}")
    print(f"  Visible: {window.pron_help_text.isVisible()}")
    print(f"  Hidden: {window.pron_help_text.isHidden()}")
    print(f"  Geometry: {window.pron_help_text.geometry()}")
    print(f"  Size hint: {window.pron_help_text.sizeHint()}")
    
    # Compare with definition text (which works)
    print("\nDefinition Text Widget Info (for comparison):")
    print(f"  Object name: {window.definition_text.objectName()}")
    print(f"  Parent widget: {window.definition_text.parent()}")
    print(f"  Visible: {window.definition_text.isVisible()}")
    print(f"  Hidden: {window.definition_text.isHidden()}")
    
    # Test direct manipulation
    print("\nTesting Direct Manipulation:")
    print(f"Before show: visible={window.pron_help_text.isVisible()}")
    window.pron_help_text.show()
    print(f"After show: visible={window.pron_help_text.isVisible()}")
    window.pron_help_text.hide()
    print(f"After hide: visible={window.pron_help_text.isVisible()}")
    
    # Test with checkbox
    print("\nTesting with Checkbox:")
    print(f"Before checkbox toggle: visible={window.pron_help_text.isVisible()}")
    window.show_pron_help_cb.setChecked(True)
    print(f"After checkbox toggle: visible={window.pron_help_text.isVisible()}")
    
    return True

if __name__ == "__main__":
    try:
        debug_widget_hierarchy()
        print("\nDebug completed")
    except Exception as e:
        print(f"Debug error: {e}")
        import traceback
        traceback.print_exc()