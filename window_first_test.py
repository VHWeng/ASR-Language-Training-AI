#!/usr/bin/env python3
"""
Test showing window first, then manipulating widget visibility
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QCheckBox, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QTimer

class WindowFirstTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window First Visibility Test")
        self.setGeometry(100, 100, 300, 200)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        
        # Create the widget
        self.test_widget = QTextEdit()
        self.test_widget.setPlaceholderText("Test Widget")
        self.test_widget.hide()  # Start hidden
        layout.addWidget(self.test_widget)
        
        # Checkbox
        self.checkbox = QCheckBox("Show Widget")
        self.checkbox.toggled.connect(self.on_checkbox_toggled)
        layout.addWidget(self.checkbox)
        
        central.setLayout(layout)
        
        # Schedule the test after window is shown
        QTimer.singleShot(100, self.test_visibility)
    
    def test_visibility(self):
        print("=== Testing Visibility After Window Shown ===")
        print(f"Initial state - visible: {self.test_widget.isVisible()}, hidden: {self.test_widget.isHidden()}")
        
        # Try to show it
        self.test_widget.show()
        print(f"After show() - visible: {self.test_widget.isVisible()}, hidden: {self.test_widget.isHidden()}")
        
        # Try via checkbox
        self.checkbox.setChecked(True)
        print(f"After checkbox - visible: {self.test_widget.isVisible()}, hidden: {self.test_widget.isHidden()}")
    
    def on_checkbox_toggled(self, checked):
        print(f"Checkbox toggled to: {checked}")
        if checked:
            self.test_widget.show()
            print(f"Widget show called - visible: {self.test_widget.isVisible()}, hidden: {self.test_widget.isHidden()}")

def main():
    app = QApplication(sys.argv)
    window = WindowFirstTest()
    window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())