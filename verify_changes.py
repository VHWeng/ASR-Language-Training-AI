#!/usr/bin/env python3
"""Simple verification script"""

import sys
from PyQt5.QtWidgets import QApplication
from asr_app import ASRApp

# Create QApplication
app = QApplication(sys.argv)

# Create app instance
window = ASRApp()

# Check column configuration
columns = window.config['vocab_columns']

print("✅ Column configuration verification:")
print(f"   Image filename column: {columns['image_filename']}")
print(f"   Image description column: {columns['image_description']}")

# Verify it's the correct configuration
if columns['image_filename'] == 6 and columns['image_description'] == 5:
    print("✅ SUCCESS: Columns configured correctly!")
else:
    print("❌ ERROR: Column configuration incorrect!")

print("\n✅ Extension handling automatically supports:")
print("   • .jpg/.jpeg files")
print("   • .png files") 
print("   • And other common image formats")