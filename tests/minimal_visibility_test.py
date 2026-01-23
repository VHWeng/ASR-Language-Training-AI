#!/usr/bin/env python3
"""
Minimal test to isolate pronunciation help visibility issue
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QCheckBox, QVBoxLayout, QWidget

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visibility Test")
        self.setGeometry(100, 100, 400, 300)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        
        # Create pronunciation help text box
        self.pron_help_text = QTextEdit()
        self.pron_help_text.setPlaceholderText("Pronunciation help text")
        self.pron_help_text.hide()  # Start hidden
        layout.addWidget(self.pron_help_text)
        
        # Create checkbox
        self.checkbox = QCheckBox("Show Pronunciation Help")
        self.checkbox.toggled.connect(self.toggle_visibility)
        layout.addWidget(self.checkbox)
        
        # Add manual show button for testing
        from PyQt5.QtWidgets import QPushButton
        self.show_btn = QPushButton("Manual Show")
        self.show_btn.clicked.connect(self.manual_show)
        layout.addWidget(self.show_btn)
        
        central.setLayout(layout)
    
    def toggle_visibility(self, checked):
        print(f"Checkbox toggled: {checked}")
        print(f"Text box visible before: {self.pron_help_text.isVisible()}")
        if checked:
            self.pron_help_text.show()
            print("Called show()")
        else:
            self.pron_help_text.hide()
            print("Called hide()")
        print(f"Text box visible after: {self.pron_help_text.isVisible()}")
    
    def manual_show(self):
        print("Manual show clicked")
        print(f"Text box visible before manual show: {self.pron_help_text.isVisible()}")
        self.pron_help_text.show()
        print(f"Text box visible after manual show: {self.pron_help_text.isVisible()}")

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    
    # Test the visibility behavior programmatically
    print("=== Programmatic Test ===")
    print(f"Initial visibility: {window.pron_help_text.isVisible()}")
    
    # Enable checkbox
    print("\nEnabling checkbox...")
    window.checkbox.setChecked(True)
    print(f"After checkbox enable: {window.pron_help_text.isVisible()}")
    
    # Manual show
    print("\nManual show...")
    window.manual_show()
    print(f"After manual show: {window.pron_help_text.isVisible()}")
    
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())