import sys
import os
import pytest
import tempfile
import csv
from unittest.mock import MagicMock, patch

from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtCore import Qt, QTimer

# Add parent directory to sys.path to allow importing asr_app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from asr_app import ASRApp, AIGrammarThread, ConfigDialog

@pytest.fixture
def app(qtbot):
    """Fixture to create and clean up ASRApp for each test"""
    test_app = QApplication(sys.argv)
    window = ASRApp()
    window.show()
    qtbot.addWidget(window)
    yield window
    window.close()
    test_app.quit()
    QApplication.processEvents()

@pytest.fixture
def mock_grammar_thread(qtbot):
    """Fixture to mock AIGrammarThread for AI generation tests"""
    with patch('asr_app.AIGrammarThread', autospec=True) as mock_thread_cls:
        mock_thread_instance = mock_thread_cls.return_value
        yield mock_thread_instance

def test_grammar_ui_elements_exist(app, qtbot):
    """Verify that the 'Show Grammar' checkbox and text box exist."""
    assert hasattr(app, 'show_grammar_cb')
    assert hasattr(app, 'grammar_text')
    assert app.show_grammar_cb is not None
    assert app.grammar_text is not None

def test_grammar_initial_state(app, qtbot):
    """Verify initial state: checkbox unchecked, text box hidden."""
    assert not app.show_grammar_cb.isChecked()
    assert not app.grammar_text.isVisible()

def test_toggle_grammar_display(app, qtbot):
    """Verify toggling 'Show Grammar' checkbox makes text box visible."""
    app.show_grammar_cb.setChecked(True)
    qtbot.wait(100) # Give event loop time to process
    assert app.show_grammar_cb.isChecked()
    assert app.grammar_text.isVisible()

    app.show_grammar_cb.setChecked(False)
    qtbot.wait(100) # Give event loop time to process
    assert not app.show_grammar_cb.isChecked()
    assert not app.grammar_text.isVisible()

def test_load_grammar_from_csv(app, qtbot):
    """Test loading grammar from a CSV file."""
    # Create a mock CSV file with grammar data
    test_data = [
        ['Word', 'Definition', 'English Pron', 'IPA Pron', 'Image Desc', 'Image File', 'Grammar'],
        ['hello', 'A greeting', 'heh-low', 'həˈloʊ', 'Waving hand', 'hello.png', 'Interjection'],
    ]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='', encoding='utf-8') as temp_csv:
        writer = csv.writer(temp_csv, delimiter='|')
        writer.writerows(test_data)
        csv_path = temp_csv.name
    
    try:
        # Load vocabulary (which will trigger display_current_vocabulary)
        app.load_csv_vocabulary(csv_path)
        app.current_vocab_index = 0
        app.show_grammar_cb.setChecked(True)
        app.display_current_vocabulary()
        qtbot.wait(100) # Wait for UI updates

        assert app.grammar_text.isVisible()
        assert app.grammar_text.toPlainText() == "Interjection"

    finally:
        os.unlink(csv_path)

def test_ai_grammar_generation_triggered(app, qtbot, mock_grammar_thread):
    """Test that AI grammar generation is triggered when grammar is missing."""
    # Create a mock CSV file *without* grammar data
    test_data = [
        ['Word', 'Definition', 'English Pron', 'IPA Pron', 'Image Desc', 'Image File'],
        ['testword', 'A definition', 'test-word', 'tɛst-wɜːd', 'test image', 'test.png'],
    ]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='', encoding='utf-8') as temp_csv:
        writer = csv.writer(temp_csv, delimiter='|')
        writer.writerows(test_data)
        csv_path = temp_csv.name

    try:
        # Load vocabulary
        app.load_csv_vocabulary(csv_path)
        app.current_vocab_index = 0
        app.show_grammar_cb.setChecked(True) # Enable grammar display
        app.display_current_vocabulary()
        qtbot.wait(100) # Wait for UI updates and potential AI call

        # Verify that AIGrammarThread was instantiated and started
        mock_grammar_thread.assert_called_once_with("testword", app.config)
        mock_grammar_thread.start.assert_called_once()
        
        # Simulate AI response
        mock_grammar_thread.finished.emit("Mocked AI Grammar Output")
        qtbot.wait(100) # Wait for signal to be processed

        assert app.grammar_text.isVisible()
        assert app.grammar_text.toPlainText() == "Mocked AI Grammar Output"

    finally:
        os.unlink(csv_path)

def test_config_dialog_grammar_column(app, qtbot):
    """Test that the ConfigDialog correctly sets and retrieves the grammar column."""
    dialog = ConfigDialog(app)
    dialog.grammar_col_spin.setValue(10) # Set a new value
    dialog.accept() # Close dialog

    new_config = app.config # Config should be updated after dialog closes

    assert new_config['vocab_columns']['grammar'] == 10

    # Re-open dialog to verify it reflects the saved value
    dialog = ConfigDialog(app)
    qtbot.wait(100) # Allow dialog to initialize
    assert dialog.grammar_col_spin.value() == 10
    dialog.reject() # Close dialog
