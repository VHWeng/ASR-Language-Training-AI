#!/usr/bin/env python3
"""
Minimal reproduction of the visibility issue
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QCheckBox, QVBoxLayout, QWidget, QPushButton

class SimpleTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Visibility Test")
        self.setGeometry(100, 100, 300, 200)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        
        # Create the problematic widget - mimicking the original setup
        self.problem_widget = QTextEdit()
        self.problem_widget.setPlaceholderText("Problem Widget")
        self.problem_widget.hide()  # This is the key - start hidden like in original code
        layout.addWidget(self.problem_widget)
        
        # Checkbox to control visibility
        self.checkbox = QCheckBox("Show Widget")
        self.checkbox.toggled.connect(self.on_checkbox_toggled)
        layout.addWidget(self.checkbox)
        
        # Manual show button
        self.show_button = QPushButton("Force Show")
        self.show_button.clicked.connect(self.force_show)
        layout.addWidget(self.show_button)
        
        central.setLayout(layout)
        
        # Test the behavior immediately
        print("=== Immediate Test ===")
        print(f"Initial visible: {self.problem_widget.isVisible()}")
        print(f"Initial hidden: {self.problem_widget.isHidden()}")
        
        # Try to show it immediately
        self.problem_widget.show()
        print(f"After immediate show: visible={self.problem_widget.isVisible()}, hidden={self.problem_widget.isHidden()}")
        
        # Try via checkbox
        self.checkbox.setChecked(True)
        print(f"After checkbox: visible={self.problem_widget.isVisible()}, hidden={self.problem_widget.isHidden()}")
    
    def on_checkbox_toggled(self, checked):
        print(f"Checkbox toggled to: {checked}")
        if checked:
            print(f"Before show: visible={self.problem_widget.isVisible()}, hidden={self.problem_widget.isHidden()}")
            self.problem_widget.show()
            print(f"After show: visible={self.problem_widget.isVisible()}, hidden={self.problem_widget.isHidden()}")
        else:
            self.problem_widget.hide()
    
    def force_show(self):
        print("Force show button clicked")
        print(f"Before force show: visible={self.problem_widget.isVisible()}, hidden={self.problem_widget.isHidden()}")
        self.problem_widget.show()
        self.problem_widget.setVisible(True)
        self.problem_widget.raise_()
        self.problem_widget.update()
        self.problem_widget.repaint()
        print(f"After force show: visible={self.problem_widget.isVisible()}, hidden={self.problem_widget.isHidden()}")

def main():
    app = QApplication(sys.argv)
    window = SimpleTestWindow()
    window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())