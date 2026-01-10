"""
ASR Application with PyQt5 GUI
Supports Google Speech Recognition and Whisper
Default language: Greek
Enhanced with Pronunciation Training Feedback
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                             QFileDialog, QDialog, QComboBox, QCheckBox,
                             QLineEdit, QMessageBox, QToolButton, QGroupBox,
                             QProgressBar, QSpinBox, QTabWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCharFormat, QTextCursor
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import numpy as np
from pydub import AudioSegment
import whisper
import tempfile
from difflib import SequenceMatcher
import re


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
        
        # Pronunciation threshold
        pron_layout = QHBoxLayout()
        self.pron_label = QLabel("Pronunciation Accuracy Threshold (%):")
        self.pron_spin = QSpinBox()
        self.pron_spin.setRange(50, 100)
        self.pron_spin.setValue(80)
        pron_layout.addWidget(self.pron_label)
        pron_layout.addWidget(self.pron_spin)
        settings_layout.addLayout(pron_layout)
        
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

For Pronunciation Training:
• Uses phonetic comparison algorithms
• Whisper recommended for better accuracy
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
        # Updated model options for Google Speech Recognition
        if self.engine_combo.currentText() == "Google Speech Recognition":
            self.model_combo.addItems([
                "Default",           # Legacy compatibility
                "Command and Search", # Legacy compatibility  
                "Dictation",         # Legacy compatibility
                "latest_short",      # NEW: Short utterances (recommended over Command and Search)
                "latest_long",       # NEW: Long content (recommended over Default)
                "chirp_3",          # NEW: Latest multilingual model with advanced features
                "telephony"         # NEW: Phone call optimization
            ])
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
            'energy_threshold': int(self.energy_entry.text()),
            'pronunciation_threshold': self.pron_spin.value()
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
    
    def __init__(self, audio_file, config, show_punctuation, show_word_time, reference_text=None):
        super().__init__()
        self.audio_file = audio_file
        self.config = config
        self.show_punctuation = show_punctuation
        self.show_word_time = show_word_time
        self.reference_text = reference_text
    
    def run(self):
        try:
            if self.config['engine'] == "Google Speech Recognition":
                result = self.google_asr()
            else:
                result = self.whisper_asr()
            
            # Add pronunciation analysis if reference text provided
            if self.reference_text:
                result['pronunciation'] = self.analyze_pronunciation(
                    self.reference_text, result['text']
                )
            
            self.finished.emit(result['text'], result.get('metadata', {}))
        except Exception as e:
            self.error.emit(str(e))
    
    def google_asr(self):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = self.config['energy_threshold']
        
        with sr.AudioFile(self.audio_file) as source:
            audio = recognizer.record(source)
        
        text = recognizer.recognize_google(audio, language=self.config['language'])
        
        return {'text': text, 'metadata': {}}
    
    def whisper_asr(self):
        model = whisper.load_model(self.config['model'])
        
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
            word_data = []
            for segment in result['segments']:
                if 'words' in segment:
                    for word in segment['words']:
                        timestamps.append(f"{word['word']} [{word['start']:.2f}s]")
                        word_data.append({
                            'word': word['word'],
                            'start': word['start'],
                            'end': word.get('end', word['start']),
                            'probability': word.get('probability', 1.0)
                        })
            metadata['word_times'] = '\n'.join(timestamps)
            metadata['word_data'] = word_data
        
        return {'text': text, 'metadata': metadata}
    
    def analyze_pronunciation(self, reference, recognized):
        """Analyze pronunciation accuracy"""
        # Normalize texts
        ref_normalized = self.normalize_text(reference)
        rec_normalized = self.normalize_text(recognized)
        
        # Calculate similarity
        similarity = SequenceMatcher(None, ref_normalized, rec_normalized).ratio()
        accuracy = similarity * 100
        
        # Word-level analysis
        ref_words = ref_normalized.split()
        rec_words = rec_normalized.split()
        
        word_analysis = []
        max_len = max(len(ref_words), len(rec_words))
        
        for i in range(max_len):
            ref_word = ref_words[i] if i < len(ref_words) else ""
            rec_word = rec_words[i] if i < len(rec_words) else ""
            
            if ref_word and rec_word:
                word_sim = SequenceMatcher(None, ref_word, rec_word).ratio()
                status = "correct" if word_sim > 0.8 else "incorrect"
                word_analysis.append({
                    'reference': ref_word,
                    'recognized': rec_word,
                    'similarity': word_sim * 100,
                    'status': status
                })
            elif ref_word:
                word_analysis.append({
                    'reference': ref_word,
                    'recognized': "",
                    'similarity': 0,
                    'status': "missing"
                })
            elif rec_word:
                word_analysis.append({
                    'reference': "",
                    'recognized': rec_word,
                    'similarity': 0,
                    'status': "extra"
                })
        
        return {
            'accuracy': accuracy,
            'word_analysis': word_analysis,
            'reference': reference,
            'recognized': recognized
        }
    
    def normalize_text(self, text):
        """Normalize text for comparison"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        return text


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
            'energy_threshold': 300,
            'pronunciation_threshold': 80
        }
        self.pronunciation_data = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("ASR Application with Pronunciation Training")
        self.setGeometry(100, 100, 900, 700)
        
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
        
        # Pronunciation Training Mode
        pron_group = QGroupBox("Pronunciation Training Mode")
        pron_layout = QVBoxLayout()
        
        self.training_mode_cb = QCheckBox("Enable Pronunciation Training")
        self.training_mode_cb.setChecked(False)
        self.training_mode_cb.toggled.connect(self.toggle_training_mode)
        
        ref_layout = QHBoxLayout()
        ref_layout.addWidget(QLabel("Reference Text:"))
        self.reference_text = QLineEdit()
        self.reference_text.setPlaceholderText("Enter the text you want to practice...")
        self.reference_text.setEnabled(False)
        ref_layout.addWidget(self.reference_text)
        
        pron_layout.addWidget(self.training_mode_cb)
        pron_layout.addLayout(ref_layout)
        pron_group.setLayout(pron_layout)
        main_layout.addWidget(pron_group)
        
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
        
        # Tabs for output
        self.tabs = QTabWidget()
        
        # ASR Output tab
        asr_tab = QWidget()
        asr_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_text.setMinimumHeight(150)
        font = QFont("Consolas", 10)
        self.output_text.setFont(font)
        asr_layout.addWidget(self.output_text)
        asr_tab.setLayout(asr_layout)
        
        # Pronunciation Feedback tab
        feedback_tab = QWidget()
        feedback_layout = QVBoxLayout()
        
        # Accuracy score
        score_layout = QHBoxLayout()
        score_layout.addWidget(QLabel("Pronunciation Accuracy:"))
        self.accuracy_label = QLabel("N/A")
        self.accuracy_label.setFont(QFont("Arial", 14, QFont.Bold))
        score_layout.addWidget(self.accuracy_label)
        self.accuracy_bar = QProgressBar()
        self.accuracy_bar.setMaximum(100)
        score_layout.addWidget(self.accuracy_bar)
        score_layout.addStretch()
        feedback_layout.addLayout(score_layout)
        
        # Feedback text
        self.feedback_text = QTextEdit()
        self.feedback_text.setReadOnly(True)
        self.feedback_text.setFont(font)
        feedback_layout.addWidget(self.feedback_text)
        
        feedback_tab.setLayout(feedback_layout)
        
        self.tabs.addTab(asr_tab, "ASR Output")
        self.tabs.addTab(feedback_tab, "Pronunciation Feedback")
        
        main_layout.addWidget(self.tabs)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Save Text")
        self.save_btn.clicked.connect(self.save_text)
        
        self.save_report_btn = QPushButton("📊 Save Report")
        self.save_report_btn.clicked.connect(self.save_report)
        self.save_report_btn.setEnabled(False)
        
        self.exit_btn = QPushButton("❌ Exit")
        self.exit_btn.clicked.connect(self.close)
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.save_btn)
        bottom_layout.addWidget(self.save_report_btn)
        bottom_layout.addWidget(self.exit_btn)
        main_layout.addLayout(bottom_layout)
        
        central.setLayout(main_layout)
    
    def toggle_training_mode(self, enabled):
        self.reference_text.setEnabled(enabled)
        if enabled:
            self.tabs.setCurrentIndex(1)  # Switch to feedback tab
    
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
        
        # Check if reference text is needed
        reference = None
        if self.training_mode_cb.isChecked():
            reference = self.reference_text.text().strip()
            if not reference:
                QMessageBox.warning(self, "No Reference", 
                                  "Please enter reference text for pronunciation training.")
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
            self.word_time_cb.isChecked(),
            reference
        )
        self.asr_thread.finished.connect(self.on_asr_finished)
        self.asr_thread.error.connect(self.on_error)
        self.asr_thread.start()
    
    def on_asr_finished(self, text, metadata):
        result = text
        if 'word_times' in metadata:
            result += "\n\n--- Word Timestamps ---\n" + metadata['word_times']
        
        self.output_text.setText(result)
        
        # Handle pronunciation feedback
        if 'pronunciation' in metadata:
            self.pronunciation_data = metadata['pronunciation']
            self.display_pronunciation_feedback(metadata['pronunciation'])
            self.save_report_btn.setEnabled(True)
        
        self.convert_btn.setEnabled(True)
    
    def display_pronunciation_feedback(self, pron_data):
        """Display detailed pronunciation feedback"""
        accuracy = pron_data['accuracy']
        threshold = self.config['pronunciation_threshold']
        
        # Update accuracy display
        self.accuracy_label.setText(f"{accuracy:.1f}%")
        self.accuracy_bar.setValue(int(accuracy))
        
        # Color code the accuracy
        if accuracy >= threshold:
            color = "green"
            status = "Excellent!"
        elif accuracy >= threshold - 10:
            color = "orange"
            status = "Good"
        else:
            color = "red"
            status = "Needs Improvement"
        
        self.accuracy_label.setStyleSheet(f"color: {color};")
        
        # Generate detailed feedback
        feedback = f"=== PRONUNCIATION FEEDBACK ===\n\n"
        feedback += f"Overall Accuracy: {accuracy:.1f}% - {status}\n"
        feedback += f"Threshold: {threshold}%\n\n"
        
        feedback += f"Reference Text:\n{pron_data['reference']}\n\n"
        feedback += f"Your Pronunciation:\n{pron_data['recognized']}\n\n"
        
        feedback += "=== WORD-BY-WORD ANALYSIS ===\n\n"
        
        correct_count = 0
        total_count = len(pron_data['word_analysis'])
        
        for i, word_info in enumerate(pron_data['word_analysis'], 1):
            status = word_info['status']
            ref = word_info['reference']
            rec = word_info['recognized']
            sim = word_info['similarity']
            
            if status == "correct":
                feedback += f"{i}. ✓ '{ref}' → '{rec}' ({sim:.1f}%)\n"
                correct_count += 1
            elif status == "incorrect":
                feedback += f"{i}. ✗ '{ref}' → '{rec}' ({sim:.1f}%) - Mispronounced\n"
            elif status == "missing":
                feedback += f"{i}. ✗ '{ref}' → [MISSING] - Word not pronounced\n"
            elif status == "extra":
                feedback += f"{i}. ⚠ [EXTRA] → '{rec}' - Extra word added\n"
        
        feedback += f"\n=== SUMMARY ===\n"
        feedback += f"Correct Words: {correct_count}/{total_count}\n"
        feedback += f"Word Accuracy: {(correct_count/total_count*100) if total_count > 0 else 0:.1f}%\n\n"
        
        # Recommendations
        feedback += "=== RECOMMENDATIONS ===\n"
        if accuracy >= threshold:
            feedback += "• Great job! Your pronunciation is excellent.\n"
            feedback += "• Try practicing more complex sentences.\n"
        elif accuracy >= threshold - 10:
            feedback += "• Good effort! Focus on the mispronounced words.\n"
            feedback += "• Practice speaking more slowly and clearly.\n"
        else:
            feedback += "• Review the reference text carefully.\n"
            feedback += "• Practice each word individually.\n"
            feedback += "• Speak slowly and enunciate clearly.\n"
            feedback += "• Consider listening to native speakers.\n"
        
        self.feedback_text.setText(feedback)
        
        # Switch to feedback tab
        self.tabs.setCurrentIndex(1)
    
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
    
    def save_report(self):
        """Save pronunciation training report"""
        if not self.pronunciation_data:
            QMessageBox.warning(self, "No Report", "No pronunciation report to save.")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Pronunciation Report", "", 
            "Text Files (*.txt);;HTML Files (*.html);;All Files (*)"
        )
        if filename:
            try:
                report_text = self.feedback_text.toPlainText()
                report_text += f"\n\n=== SESSION INFO ===\n"
                report_text += f"Language: {self.config['language_name']}\n"
                report_text += f"Engine: {self.config['engine']}\n"
                report_text += f"Model: {self.config['model']}\n"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                QMessageBox.information(self, "Success", "Report saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", str(e))
    
    def show_help(self):
        help_text = """ASR Application with Pronunciation Training

BASIC USAGE:
1. Load or Record Audio:
   - Browse for WAV/MP3 file, or
   - Click Record to capture 10 seconds

2. Configure Settings:
   - Click ⚙ to select engine, language, and model

3. Convert:
   - Click ASR Convert to transcribe audio

PRONUNCIATION TRAINING MODE:
1. Enable "Pronunciation Training Mode"
2. Enter the reference text you want to practice
3. Record yourself reading the text
4. Click "ASR Convert" to get feedback

FEEDBACK INCLUDES:
• Overall pronunciation accuracy score
• Word-by-word analysis
• Identification of mispronounced words
• Missing or extra words
• Personalized recommendations
• Color-coded results (green/orange/red)

OPTIONS:
• Show Punctuation (context dependent)
• Word Timestamps (Whisper only)
• Adjustable accuracy threshold

SAVE OPTIONS:
• Save transcribed text
• Save detailed pronunciation report

SUPPORTED LANGUAGES:
Greek (default), English, Spanish, French, 
German, Italian, Portuguese, Russian, 
Chinese, Japanese, Korean, Arabic

TIPS FOR BEST RESULTS:
• Use Whisper engine for better accuracy
• Speak clearly and at moderate pace
• Ensure quiet recording environment
• Practice difficult words individually"""
        
        QMessageBox.information(self, "Help", help_text)
    
    def show_about(self):
        about_text = """ASR Application v2.0
Pronunciation Training Edition

Automatic Speech Recognition tool supporting:
• Google Speech Recognition
• OpenAI Whisper

NEW FEATURES:
• Pronunciation accuracy scoring
• Word-by-word analysis
• Mispronunciation detection
• Training recommendations
• Detailed feedback reports

Default Language: Greek (el-GR)

Supports multiple languages and audio formats.

Built with PyQt5 and Python.
Perfect for language learners!"""
        
        QMessageBox.about(self, "About ASR App", about_text)
    
    def show_config(self):
        dialog = ConfigDialog(self)
        # Set current values
        dialog.engine_combo.setCurrentText(self.config['engine'])
        dialog.lang_combo.setCurrentText(self.config['language_name'])
        dialog.model_combo.setCurrentText(self.config['model'])
        dialog.rate_entry.setText(str(self.config['sample_rate']))
        dialog.energy_entry.setText(str(self.config['energy_threshold']))
        dialog.pron_spin.setValue(self.config['pronunciation_threshold'])
        
        if dialog.exec_() == QDialog.Accepted:
            self.config = dialog.get_config()
            QMessageBox.information(self, "Configuration", 
                                  f"Engine: {self.config['engine']}\n"
                                  f"Language: {self.config['language_name']}\n"
                                  f"Model: {self.config['model']}\n"
                                  f"Pronunciation Threshold: {self.config['pronunciation_threshold']}%")


def main():
    app = QApplication(sys.argv)
    window = ASRApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()