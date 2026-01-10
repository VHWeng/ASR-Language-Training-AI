"""
ASR Application with PyQt5 GUI
Supports Google Speech Recognition and Whisper
Default language: Greek
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                             QFileDialog, QDialog, QComboBox, QCheckBox,
                             QLineEdit, QMessageBox, QToolButton, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import numpy as np
from pydub import AudioSegment
import whisper
import tempfile

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Engine selection
        engine_group = QGroupBox("ASR Engine")
        engine_layout = QVBoxLayout()
        
        self.engine_label = QLabel("Select Engine:")
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["Google Speech Recognition", "Whisper"])
        self.engine_combo.currentIndexChanged.connect(self.on_engine_changed)
        
        engine_layout.addWidget(self.engine_label)
        engine_layout.addWidget(self.engine_combo)
        engine_group.setLayout(engine_layout)
        layout.addWidget(engine_group)
        
        # Language selection
        lang_group = QGroupBox("Language")
        lang_layout = QVBoxLayout()
        
        self.lang_label = QLabel("Select Language:")
        self.lang_combo = QComboBox()
        self.languages = {
            "Greek": "el-GR",
            "English (US)": "en-US",
            "English (UK)": "en-GB",
            "Spanish": "es-ES",
            "French": "fr-FR",
            "German": "de-DE",
            "Italian": "it-IT",
            "Portuguese": "pt-PT",
            "Russian": "ru-RU",
            "Chinese": "zh-CN",
            "Japanese": "ja-JP",
            "Korean": "ko-KR",
            "Arabic": "ar-SA"
        }
        self.lang_combo.addItems(self.languages.keys())
        self.lang_combo.setCurrentText("Greek")
        
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_combo)
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)
        
        # Model selection
        model_group = QGroupBox("Model")
        model_layout = QVBoxLayout()
        
        self.model_label = QLabel("Select Model:")
        self.model_combo = QComboBox()
        self.update_model_options()
        
        model_layout.addWidget(self.model_label)
        model_layout.addWidget(self.model_combo)
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # Additional settings
        settings_group = QGroupBox("Additional Settings")
        settings_layout = QVBoxLayout()
        
        # Sample rate
        rate_layout = QHBoxLayout()
        self.rate_label = QLabel("Sample Rate (Hz):")
        self.rate_entry = QLineEdit("16000")
        rate_layout.addWidget(self.rate_label)
        rate_layout.addWidget(self.rate_entry)
        settings_layout.addLayout(rate_layout)
        
        # Energy threshold for Google
        energy_layout = QHBoxLayout()
        self.energy_label = QLabel("Energy Threshold:")
        self.energy_entry = QLineEdit("300")
        energy_layout.addWidget(self.energy_label)
        energy_layout.addWidget(self.energy_entry)
        settings_layout.addLayout(energy_layout)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Requirements info
        req_group = QGroupBox("Setup Requirements")
        req_layout = QVBoxLayout()
        req_text = QTextEdit()
        req_text.setReadOnly(True)
        req_text.setMaximumHeight(150)
        
        requirements = """Required packages:
• pip install PyQt5
• pip install SpeechRecognition
• pip install sounddevice soundfile
• pip install pydub
• pip install openai-whisper
• pip install numpy

For audio playback:
• Install FFmpeg for MP3 support

For Whisper:
• Requires PyTorch (CPU or GPU version)
• First run will download model files
"""
        req_text.setText(requirements)
        req_layout.addWidget(req_text)
        req_group.setLayout(req_layout)
        layout.addWidget(req_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Cancel")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def on_engine_changed(self):
        self.update_model_options()
    
    def update_model_options(self):
        self.model_combo.clear()
        if self.engine_combo.currentText() == "Google Speech Recognition":
            self.model_combo.addItems(["Default", "Command and Search", "Dictation"])
        else:  # Whisper
            self.model_combo.addItems(["tiny", "base", "small", "medium", "large"])
            self.model_combo.setCurrentText("base")
    
    def get_config(self):
        return {
            'engine': self.engine_combo.currentText(),
            'language': self.languages[self.lang_combo.currentText()],
            'language_name': self.lang_combo.currentText(),
            'model': self.model_combo.currentText(),
            'sample_rate': int(self.rate_entry.text()),
            'energy_threshold': int(self.energy_entry.text())
        }


class RecordThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, duration=10, sample_rate=16000):
        super().__init__()
        self.duration = duration
        self.sample_rate = sample_rate
        self.filename = None
    
    def run(self):
        try:
            recording = sd.rec(int(self.duration * self.sample_rate), 
                             samplerate=self.sample_rate, 
                             channels=1, 
                             dtype='float32')
            sd.wait()
            
            self.filename = tempfile.mktemp(suffix='.wav')
            sf.write(self.filename, recording, self.sample_rate)
            self.finished.emit(self.filename)
        except Exception as e:
            self.error.emit(str(e))


class ASRThread(QThread):
    finished = pyqtSignal(str, dict)
    error = pyqtSignal(str)
    
    def __init__(self, audio_file, config, show_punctuation, show_word_time):
        super().__init__()
        self.audio_file = audio_file
        self.config = config
        self.show_punctuation = show_punctuation
        self.show_word_time = show_word_time
    
    def run(self):
        try:
            if self.config['engine'] == "Google Speech Recognition":
                result = self.google_asr()
            else:
                result = self.whisper_asr()
            
            self.finished.emit(result['text'], result.get('metadata', {}))
        except Exception as e:
            self.error.emit(str(e))
    
    def google_asr(self):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = self.config['energy_threshold']
        
        with sr.AudioFile(self.audio_file) as source:
            audio = recognizer.record(source)
        
        # Google doesn't support punctuation toggle or word timestamps
        text = recognizer.recognize_google(audio, language=self.config['language'])
        
        return {'text': text, 'metadata': {}}
    
    def whisper_asr(self):
        model = whisper.load_model(self.config['model'])
        
        # Extract language code (first 2 chars)
        lang_code = self.config['language'][:2]
        
        result = model.transcribe(
            self.audio_file, 
            language=lang_code,
            word_timestamps=self.show_word_time
        )
        
        text = result['text']
        
        metadata = {}
        if self.show_word_time and 'segments' in result:
            timestamps = []
            for segment in result['segments']:
                if 'words' in segment:
                    for word in segment['words']:
                        timestamps.append(f"{word['word']} [{word['start']:.2f}s]")
            metadata['word_times'] = '\n'.join(timestamps)
        
        return {'text': text, 'metadata': metadata}


class ASRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_file = None
        self.recorded_file = None
        self.config = {
            'engine': 'Google Speech Recognition',
            'language': 'el-GR',
            'language_name': 'Greek',
            'model': 'Default',
            'sample_rate': 16000,
            'energy_threshold': 300
        }
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("ASR Application")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        
        # Top toolbar with icons
        toolbar = QHBoxLayout()
        toolbar.addStretch()
        
        self.config_btn = QToolButton()
        self.config_btn.setText("⚙")
        self.config_btn.setToolTip("Configuration")
        self.config_btn.clicked.connect(self.show_config)
        
        self.help_btn = QToolButton()
        self.help_btn.setText("?")
        self.help_btn.setToolTip("Help")
        self.help_btn.clicked.connect(self.show_help)
        
        self.about_btn = QToolButton()
        self.about_btn.setText("ℹ")
        self.about_btn.setToolTip("About")
        self.about_btn.clicked.connect(self.show_about)
        
        toolbar.addWidget(self.config_btn)
        toolbar.addWidget(self.help_btn)
        toolbar.addWidget(self.about_btn)
        main_layout.addLayout(toolbar)
        
        # File browser section
        file_group = QGroupBox("Audio File (Optional)")
        file_layout = QHBoxLayout()
        
        self.file_label = QLabel("No file selected")
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_file)
        
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.browse_btn)
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.record_btn = QPushButton("🎤 Record")
        self.record_btn.clicked.connect(self.record_audio)
        
        self.playback_btn = QPushButton("▶ Playback")
        self.playback_btn.clicked.connect(self.playback_audio)
        self.playback_btn.setEnabled(False)
        
        self.convert_btn = QPushButton("🔄 ASR Convert")
        self.convert_btn.clicked.connect(self.convert_audio)
        self.convert_btn.setEnabled(False)
        
        control_layout.addWidget(self.record_btn)
        control_layout.addWidget(self.playback_btn)
        control_layout.addWidget(self.convert_btn)
        main_layout.addLayout(control_layout)
        
        # Options
        options_layout = QHBoxLayout()
        
        self.punctuation_cb = QCheckBox("Show Punctuation")
        self.punctuation_cb.setChecked(True)
        
        self.word_time_cb = QCheckBox("Word Timestamps")
        self.word_time_cb.setChecked(False)
        
        options_layout.addWidget(self.punctuation_cb)
        options_layout.addWidget(self.word_time_cb)
        options_layout.addStretch()
        main_layout.addLayout(options_layout)
        
        # Output text box
        output_group = QGroupBox("ASR Output")
        output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setMinimumHeight(150)
        font = QFont("Consolas", 10)
        self.output_text.setFont(font)
        
        output_layout.addWidget(self.output_text)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Save Text")
        self.save_btn.clicked.connect(self.save_text)
        
        self.exit_btn = QPushButton("❌ Exit")
        self.exit_btn.clicked.connect(self.close)
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.save_btn)
        bottom_layout.addWidget(self.exit_btn)
        main_layout.addLayout(bottom_layout)
        
        central.setLayout(main_layout)
    
    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Audio File", "", 
            "Audio Files (*.wav *.mp3);;All Files (*)"
        )
        if filename:
            self.audio_file = filename
            self.file_label.setText(os.path.basename(filename))
            self.playback_btn.setEnabled(True)
            self.convert_btn.setEnabled(True)
    
    def record_audio(self):
        self.record_btn.setEnabled(False)
        self.output_text.setText("Recording for 10 seconds...")
        
        self.record_thread = RecordThread(duration=10, 
                                         sample_rate=self.config['sample_rate'])
        self.record_thread.finished.connect(self.on_record_finished)
        self.record_thread.error.connect(self.on_error)
        self.record_thread.start()
    
    def on_record_finished(self, filename):
        self.recorded_file = filename
        self.audio_file = filename
        self.file_label.setText("Recorded audio")
        self.output_text.setText("Recording complete!")
        self.record_btn.setEnabled(True)
        self.playback_btn.setEnabled(True)
        self.convert_btn.setEnabled(True)
    
    def playback_audio(self):
        if not self.audio_file:
            QMessageBox.warning(self, "No Audio", "Please load or record audio first.")
            return
        
        try:
            data, samplerate = sf.read(self.audio_file)
            sd.play(data, samplerate)
            self.output_text.setText("Playing audio...")
        except Exception as e:
            QMessageBox.critical(self, "Playback Error", str(e))
    
    def convert_audio(self):
        if not self.audio_file:
            QMessageBox.warning(self, "No Audio", "Please load or record audio first.")
            return
        
        # Convert MP3 to WAV if needed
        audio_file = self.audio_file
        if self.audio_file.lower().endswith('.mp3'):
            try:
                audio = AudioSegment.from_mp3(self.audio_file)
                audio_file = tempfile.mktemp(suffix='.wav')
                audio.export(audio_file, format='wav')
            except Exception as e:
                QMessageBox.critical(self, "Conversion Error", 
                                   f"Failed to convert MP3: {str(e)}")
                return
        
        self.convert_btn.setEnabled(False)
        self.output_text.setText(f"Processing with {self.config['engine']}...")
        
        self.asr_thread = ASRThread(
            audio_file, 
            self.config,
            self.punctuation_cb.isChecked(),
            self.word_time_cb.isChecked()
        )
        self.asr_thread.finished.connect(self.on_asr_finished)
        self.asr_thread.error.connect(self.on_error)
        self.asr_thread.start()
    
    def on_asr_finished(self, text, metadata):
        result = text
        if 'word_times' in metadata:
            result += "\n\n--- Word Timestamps ---\n" + metadata['word_times']
        
        self.output_text.setText(result)
        self.convert_btn.setEnabled(True)
    
    def on_error(self, error_msg):
        QMessageBox.critical(self, "Error", error_msg)
        self.record_btn.setEnabled(True)
        self.convert_btn.setEnabled(True)
        self.output_text.setText(f"Error: {error_msg}")
    
    def save_text(self):
        text = self.output_text.toPlainText()
        if not text:
            QMessageBox.warning(self, "No Text", "No text to save.")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Text", "", "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                QMessageBox.information(self, "Success", "Text saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", str(e))
    
    def show_config(self):
        dialog = ConfigDialog(self)
        
        # Set current values
        dialog.engine_combo.setCurrentText(self.config['engine'])
        dialog.lang_combo.setCurrentText(self.config['language_name'])
        dialog.model_combo.setCurrentText(self.config['model'])
        dialog.rate_entry.setText(str(self.config['sample_rate']))
        dialog.energy_entry.setText(str(self.config['energy_threshold']))
        
        if dialog.exec_() == QDialog.Accepted:
            self.config = dialog.get_config()
            QMessageBox.information(self, "Configuration", 
                                  f"Engine: {self.config['engine']}\n"
                                  f"Language: {self.config['language_name']}\n"
                                  f"Model: {self.config['model']}")
    
    def show_help(self):
        help_text = """ASR Application Help

1. Load or Record Audio:
   - Browse for WAV/MP3 file, or
   - Click Record to capture 10 seconds

2. Configure Settings:
   - Click ⚙ to select engine, language, and model

3. Convert:
   - Click ASR Convert to transcribe audio

4. Options:
   - Show Punctuation (context dependent)
   - Word Timestamps (Whisper only)

5. Save:
   - Save transcribed text to file

Supported Languages:
Greek (default), English, Spanish, French, 
German, Italian, Portuguese, Russian, 
Chinese, Japanese, Korean, Arabic"""
        
        QMessageBox.information(self, "Help", help_text)
    
    def show_about(self):
        about_text = """ASR Application v1.0

Automatic Speech Recognition tool supporting:
• Google Speech Recognition
• OpenAI Whisper

Default Language: Greek (el-GR)

Supports multiple languages and audio formats.

Built with PyQt5 and Python."""
        
        QMessageBox.about(self, "About ASR App", about_text)


def main():
    app = QApplication(sys.argv)
    window = ASRApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
