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
from gtts import gTTS
import pygame
import io
from datetime import datetime


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
        
        # Ollama AI Configuration
        ollama_group = QGroupBox("Ollama AI Interface")
        ollama_layout = QVBoxLayout()
        
        # Model selection
        model_layout = QHBoxLayout()
        self.ollama_model_label = QLabel("AI Model:")
        self.ollama_model_combo = QComboBox()
        self.ollama_models = [
            "kimi-k2:1t-cloud",
            "llama3.2",
            "mistral",
            "phi3",
            "gemma2",
            "qwen2"
        ]
        self.ollama_model_combo.addItems(self.ollama_models)
        self.ollama_model_combo.setCurrentText("kimi-k2:1t-cloud")
        
        # Update model list button
        self.update_models_btn = QPushButton("Update Models")
        self.update_models_btn.clicked.connect(self.update_ollama_models)
        
        model_layout.addWidget(self.ollama_model_label)
        model_layout.addWidget(self.ollama_model_combo)
        model_layout.addWidget(self.update_models_btn)
        ollama_layout.addLayout(model_layout)
        
        # Test AI model button
        self.test_ai_btn = QPushButton("Test AI Model")
        self.test_ai_btn.clicked.connect(self.test_ollama_model)
        ollama_layout.addWidget(self.test_ai_btn)
        
        # AI status text box
        self.ai_status_text = QTextEdit()
        self.ai_status_text.setMaximumHeight(100)
        self.ai_status_text.setPlaceholderText("AI model test results and status will appear here...")
        self.ai_status_text.setReadOnly(True)
        ollama_layout.addWidget(self.ai_status_text)
        
        ollama_group.setLayout(ollama_layout)
        layout.addWidget(ollama_group)
        
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
            self.model_combo.addItems(['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large'])
            self.model_combo.setCurrentText("base")
    
    def update_ollama_models(self):
        """Update the list of available Ollama models"""
        try:
            import subprocess
            import json
            
            # Try to get list of models from Ollama
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Parse the output to extract model names
                lines = result.stdout.strip().split('\n')
                models = []
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        model_name = line.split()[0]
                        models.append(model_name)
                
                if models:
                    self.ollama_model_combo.clear()
                    self.ollama_model_combo.addItems(models)
                    self.ai_status_text.append(f"[{self.parent().get_current_time()}] Successfully updated model list ({len(models)} models found)")
                else:
                    self.ai_status_text.append(f"[{self.parent().get_current_time()}] No models found in Ollama")
            else:
                self.ai_status_text.append(f"[{self.parent().get_current_time()}] Failed to get model list: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.ai_status_text.append(f"[{self.parent().get_current_time()}] Timeout while trying to get model list")
        except FileNotFoundError:
            self.ai_status_text.append(f"[{self.parent().get_current_time()}] Ollama not found. Please install Ollama first.")
        except Exception as e:
            self.ai_status_text.append(f"[{self.parent().get_current_time()}] Error updating models: {str(e)}")
    
    def test_ollama_model(self):
        """Test if the selected Ollama model is working"""
        try:
            import subprocess
            import json
            
            selected_model = self.ollama_model_combo.currentText()
            self.ai_status_text.append(f"[{self.parent().get_current_time()}] Testing model: {selected_model}")
            
            # Test prompt
            test_prompt = "Say hello in English"
            
            # Prepare the request
            request_data = {
                "model": selected_model,
                "prompt": test_prompt,
                "stream": False
            }
            
            # Run Ollama generate command
            result = subprocess.run([
                'ollama', 'run', selected_model, test_prompt
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                response = result.stdout.strip()
                self.ai_status_text.append(f"[{self.parent().get_current_time()}] ✅ Model test successful!")
                self.ai_status_text.append(f"Response: {response}")
            else:
                self.ai_status_text.append(f"[{self.parent().get_current_time()}] ❌ Model test failed:")
                self.ai_status_text.append(f"Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.ai_status_text.append(f"[{self.parent().get_current_time()}] ❌ Timeout while testing model")
        except FileNotFoundError:
            self.ai_status_text.append(f"[{self.parent().get_current_time()}] ❌ Ollama not found. Please install Ollama first.")
        except Exception as e:
            self.ai_status_text.append(f"[{self.parent().get_current_time()}] ❌ Error testing model: {str(e)}")
    
    def get_config(self):
        config = {
            'engine': self.engine_combo.currentText(),
            'language': self.languages[self.lang_combo.currentText()],
            'language_name': self.lang_combo.currentText(),
            'model': self.model_combo.currentText(),
            'sample_rate': int(self.rate_entry.text()),
            'energy_threshold': int(self.energy_entry.text()),
            'pronunciation_threshold': self.pron_spin.value()
        }
        
        # Add Ollama configuration
        config['ollama_model'] = self.ollama_model_combo.currentText()
        
        return config


import threading
import queue

class RecordThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, sample_rate=16000):
        super().__init__()
        self.sample_rate = sample_rate
        self.filename = None
        self.is_recording = True  # Flag to control recording
        self.audio_queue = queue.Queue()
        self.recording_thread = None
    
    def run(self):
        try:
            # Initialize recording buffer
            recording_buffer = []
            
            # Callback function to capture audio chunks
            def audio_callback(indata, frames, time, status):
                if self.is_recording:
                    recording_buffer.append(indata.copy())
            
            # Start the stream
            stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32',
                callback=audio_callback
            )
            
            stream.start()
            
            # Keep recording until flag is changed
            while self.is_recording:
                sd.sleep(100)  # Sleep for 100ms to avoid busy waiting
            
            # Stop the stream
            stream.stop()
            stream.close()
            
            # Combine all recorded chunks
            if recording_buffer:
                import numpy as np
                full_recording = np.concatenate(recording_buffer, axis=0)
                
                self.filename = tempfile.mktemp(suffix='.wav')
                sf.write(self.filename, full_recording, self.sample_rate)
                self.finished.emit(self.filename)
            else:
                self.error.emit("No audio recorded")
                
        except Exception as e:
            self.error.emit(str(e))
    
    def stop_recording(self):
        """Stop the recording"""
        self.is_recording = False


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
                pronunciation_result = self.analyze_pronunciation(
                    self.reference_text, result['text']
                )
                # Add pronunciation data to metadata
                if 'metadata' not in result:
                    result['metadata'] = {}
                result['metadata']['pronunciation'] = pronunciation_result
                
                # Debug logging
                print(f"DEBUG: Pronunciation analysis completed. Accuracy: {pronunciation_result['accuracy']:.1f}%")
                print(f"DEBUG: Word analysis items: {len(pronunciation_result['word_analysis'])}")
            
            self.finished.emit(result['text'], result.get('metadata', {}))
        except Exception as e:
            self.error.emit(str(e))
    
    def google_asr(self):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = self.config['energy_threshold']
        
        with sr.AudioFile(self.audio_file) as source:
            audio = recognizer.record(source)
        
        text = recognizer.recognize_google(audio, language=self.config['language'])
        
        print(f"DEBUG: Google ASR returned text: '{text}'")
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
            'model': 'chirp_3',
            'sample_rate': 16000,
            'energy_threshold': 300,
            'pronunciation_threshold': 80,
            'ollama_model': 'kimi-k2:1t-cloud'
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
        
        # First row: Training mode and AI checkboxes
        mode_layout = QHBoxLayout()
        self.training_mode_cb = QCheckBox("Enable Pronunciation Training")
        self.training_mode_cb.setChecked(True)  # Default enabled
        self.training_mode_cb.toggled.connect(self.toggle_training_mode)
        
        self.show_pronunciation_cb = QCheckBox("Show Pronunciation")
        self.show_pronunciation_cb.setChecked(True)
        self.show_pronunciation_cb.toggled.connect(self.toggle_pronunciation_display)
        
        self.show_definition_cb = QCheckBox("Show Definition/Translation")
        self.show_definition_cb.setChecked(True)
        self.show_definition_cb.toggled.connect(self.toggle_definition_display)
        
        mode_layout.addWidget(self.training_mode_cb)
        mode_layout.addWidget(self.show_pronunciation_cb)
        mode_layout.addWidget(self.show_definition_cb)
        
        # Add AI status indicator
        self.ai_status_indicator = QLabel("⚪ AI Disconnected")
        self.ai_status_indicator.setStyleSheet("QLabel { color: gray; font-weight: bold; }")
        mode_layout.addWidget(self.ai_status_indicator)
        mode_layout.addStretch()
        pron_layout.addLayout(mode_layout)
        
        # Reference text row
        ref_layout = QHBoxLayout()
        ref_layout.addWidget(QLabel("Reference Text:"))
        self.reference_text = QLineEdit()
        self.reference_text.setPlaceholderText("Enter the text you want to practice...")
        self.reference_text.setEnabled(True)  # Default enabled
        self.reference_text.returnPressed.connect(self.load_ai_data)  # Enter key handler
        ref_layout.addWidget(self.reference_text)
        
        # Add Load AI button
        self.load_ai_btn = QPushButton("📥 Load AI")
        self.load_ai_btn.clicked.connect(self.load_ai_data)
        self.load_ai_btn.setEnabled(True)  # Default enabled
        self.load_ai_btn.setToolTip("Load pronunciation and definition from AI")
        ref_layout.addWidget(self.load_ai_btn)
        
        # Add TTS button
        self.tts_btn = QPushButton("🔊 Play TTS")
        self.tts_btn.clicked.connect(self.play_tts)
        self.tts_btn.setEnabled(True)  # Default enabled
        ref_layout.addWidget(self.tts_btn)
        
        pron_layout.addLayout(ref_layout)
        
        # Pronunciation text box (visible by default since training mode is enabled)
        self.pronunciation_text = QTextEdit()
        self.pronunciation_text.setMaximumHeight(60)
        self.pronunciation_text.setPlaceholderText("Pronunciation information from Ollama AI will appear here...")
        self.pronunciation_text.setReadOnly(True)
        self.pronunciation_text.show()  # Show by default
        pron_layout.addWidget(self.pronunciation_text)
        
        # Definition text box (visible by default since training mode is enabled)
        self.definition_text = QTextEdit()
        self.definition_text.setMaximumHeight(80)
        self.definition_text.setPlaceholderText("Definition/translation from Ollama AI will appear here...")
        self.definition_text.setReadOnly(True)
        self.definition_text.show()  # Show by default
        pron_layout.addWidget(self.definition_text)
        
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
        
        self.record_btn = QPushButton("🎤 Hold to Record")
        self.record_btn.pressed.connect(self.start_recording)
        self.record_btn.released.connect(self.stop_recording)
        self.is_recording = False
        
        # Set button style to make it clear it's a press-and-hold button
        self.record_btn.setStyleSheet("QPushButton { font-weight: bold; padding: 10px; }")
        
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
        
        # Add auto-check checkbox
        self.auto_check_cb = QCheckBox("Auto Check After Record")
        self.auto_check_cb.setChecked(False)
        self.auto_check_cb.setToolTip("Automatically run ASR Convert after recording completes")
        
        options_layout.addWidget(self.punctuation_cb)
        options_layout.addWidget(self.word_time_cb)
        options_layout.addWidget(self.auto_check_cb)
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
        
        # Status/Debug text box
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(60)  # About 3 lines
        self.status_text.setPlaceholderText("Status and debug information will appear here...")
        self.status_text.setReadOnly(True)
        font = QFont("Consolas", 9)
        self.status_text.setFont(font)
        main_layout.addWidget(self.status_text)
        
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
        self.tts_btn.setEnabled(enabled)
        self.load_ai_btn.setEnabled(enabled)
        
        if enabled:
            # Auto-show pronunciation and definition when training mode is enabled
            self.show_pronunciation_cb.setChecked(True)
            self.show_definition_cb.setChecked(True)
            self.pronunciation_text.show()
            self.definition_text.show()
            self.tabs.setCurrentIndex(1)  # Switch to feedback tab
            
            # Auto-connect to AI if text is present
            if self.reference_text.text().strip():
                self.load_ai_data()
        else:
            # Hide text boxes when training mode is disabled
            self.pronunciation_text.hide()
            self.definition_text.hide()
    
    def toggle_pronunciation_display(self, enabled):
        """Toggle pronunciation text box visibility"""
        if enabled:
            self.pronunciation_text.show()
            # Also show definition if it's enabled
            if self.show_definition_cb.isChecked():
                self.definition_text.show()
        else:
            self.pronunciation_text.hide()
            self.definition_text.hide()
    
    def toggle_definition_display(self, enabled):
        """Toggle definition text box visibility"""
        if enabled and self.show_pronunciation_cb.isChecked():
            self.definition_text.show()
        else:
            self.definition_text.hide()
    
    def update_ai_status(self, status, color="gray"):
        """Update AI status indicator"""
        status_icons = {
            "connected": "🟢",
            "disconnected": "⚪", 
            "connecting": "🟡",
            "error": "🔴"
        }
        
        icon = status_icons.get(status.lower(), "⚪")
        status_text = f"{icon} AI {status.title()}"
        
        self.ai_status_indicator.setText(status_text)
        self.ai_status_indicator.setStyleSheet(f"QLabel {{ color: {color}; font-weight: bold; }}")
    
    def load_ai_data(self):
        """Load pronunciation and definition data from Ollama AI"""
        reference_text = self.reference_text.text().strip()
        if not reference_text:
            QMessageBox.warning(self, "No Text", "Please enter text to get AI assistance.")
            return
        
        try:
            # Update status
            self.update_ai_status("connecting", "orange")
            self.status_text.append(f"[{self.get_current_time()}] Requesting AI data for: '{reference_text}'")
            
            # Get language code
            lang_code = self.config['language'].split('-')[0].lower()
            
            # Create AI requests
            import subprocess
            import json
            
            # Pronunciation request
            pron_prompt = f"Provide the phonetic pronunciation for this {self.config['language_name']} phrase: '{reference_text}'. Respond with just the pronunciation guide."
            
            # Definition request  
            def_prompt = f"Provide the definition and translation of this {self.config['language_name']} phrase: '{reference_text}'. Include grammatical information if relevant."
            
            # Run AI requests
            selected_model = self.config.get('ollama_model', 'kimi-k2:1t-cloud')
            
            # Get pronunciation
            pron_result = subprocess.run([
                'ollama', 'run', selected_model, pron_prompt
            ], capture_output=True, text=True, timeout=30)
            
            if pron_result.returncode == 0:
                pronunciation = pron_result.stdout.strip()
                self.pronunciation_text.setPlainText(pronunciation)
                self.status_text.append(f"[{self.get_current_time()}] Pronunciation received from AI")
            else:
                self.pronunciation_text.setPlainText("Failed to get pronunciation from AI")
                self.status_text.append(f"[{self.get_current_time()}] AI pronunciation request failed")
            
            # Get definition
            def_result = subprocess.run([
                'ollama', 'run', selected_model, def_prompt
            ], capture_output=True, text=True, timeout=30)
            
            if def_result.returncode == 0:
                definition = def_result.stdout.strip()
                self.definition_text.setPlainText(definition)
                self.status_text.append(f"[{self.get_current_time()}] Definition received from AI")
            else:
                self.definition_text.setPlainText("Failed to get definition from AI")
                self.status_text.append(f"[{self.get_current_time()}] AI definition request failed")
            
            # Update status
            if pron_result.returncode == 0 and def_result.returncode == 0:
                self.update_ai_status("connected", "green")
                self.status_text.append(f"[{self.get_current_time()}] AI data loading completed successfully")
            else:
                self.update_ai_status("error", "red")
                self.status_text.append(f"[{self.get_current_time()}] AI data loading completed with errors")
                
        except subprocess.TimeoutExpired:
            self.update_ai_status("error", "red")
            self.status_text.append(f"[{self.get_current_time()}] AI request timed out")
            QMessageBox.critical(self, "Timeout", "AI request timed out. Please check if Ollama is running.")
        except FileNotFoundError:
            self.update_ai_status("error", "red")
            self.status_text.append(f"[{self.get_current_time()}] Ollama not found")
            QMessageBox.critical(self, "Ollama Not Found", "Ollama is not installed or not in PATH. Please install Ollama first.")
        except Exception as e:
            self.update_ai_status("error", "red")
            self.status_text.append(f"[{self.get_current_time()}] AI request error: {str(e)}")
            QMessageBox.critical(self, "AI Error", f"Failed to get AI data: {str(e)}")
    
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
    
    def start_recording(self):
        if self.is_recording:
            return
        
        self.is_recording = True
        self.record_btn.setText("⏹️ Stop Recording")
        self.output_text.setText("Recording... Release button to stop")
        
        self.record_thread = RecordThread(sample_rate=self.config['sample_rate'])
        self.record_thread.finished.connect(self.on_record_finished)
        self.record_thread.error.connect(self.on_error)
        self.record_thread.start()
    
    def stop_recording(self):
        if not self.is_recording:
            return
        
        self.is_recording = False
        self.record_btn.setText("🎤 Hold to Record")
        
        if hasattr(self, 'record_thread') and self.record_thread:
            self.record_thread.stop_recording()
    
    def record_audio(self):
        # This method is kept for compatibility but not used for the hold-to-record functionality
        pass
    
    def on_record_finished(self, filename):
        self.recorded_file = filename
        self.audio_file = filename
        self.file_label.setText("Recorded audio")
        self.output_text.setText("Recording complete!")
        self.status_text.append(f"[{self.get_current_time()}] Recording completed: {os.path.basename(filename)}")
        self.is_recording = False
        self.record_btn.setText("🎤 Hold to Record")
        self.playback_btn.setEnabled(True)
        self.convert_btn.setEnabled(True)
        
        # Auto-check functionality
        if self.auto_check_cb.isChecked():
            self.status_text.append(f"[{self.get_current_time()}] Auto-check enabled - starting ASR conversion...")
            self.convert_audio()
    
    def on_error(self, error_msg):
        QMessageBox.critical(self, "Error", error_msg)
        self.is_recording = False
        self.record_btn.setText("🎤 Hold to Record")
        self.record_btn.setEnabled(True)  # Re-enable the button
        self.convert_btn.setEnabled(True)
        self.output_text.setText(f"Error: {error_msg}")
    
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
            print(f"DEBUG: Training mode enabled, reference text: '{reference}'")
            if not reference:
                QMessageBox.warning(self, "No Reference", 
                                  "Please enter reference text for pronunciation training.")
                return
        else:
            print(f"DEBUG: Training mode disabled")
        
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
        # Debug logging
        print(f"DEBUG: ASR finished callback called")
        print(f"DEBUG: Metadata keys: {list(metadata.keys()) if metadata else 'None'}")
        
        result = text
        if 'word_times' in metadata:
            result += "\n\n--- Word Timestamps ---\n" + metadata['word_times']
        
        self.output_text.setText(result)
        
        # Handle pronunciation feedback
        print(f"DEBUG: Checking for pronunciation data...")
        print(f"DEBUG: metadata is None: {metadata is None}")
        if metadata is not None:
            print(f"DEBUG: metadata keys: {list(metadata.keys())}")
            print(f"DEBUG: 'pronunciation' in metadata: {'pronunciation' in metadata}")
        
        if metadata and 'pronunciation' in metadata:
            print(f"DEBUG: Found pronunciation data in metadata")
            self.pronunciation_data = metadata['pronunciation']
            self.display_pronunciation_feedback(metadata['pronunciation'])
            print(f"DEBUG: Enabling save report button")
            self.save_report_btn.setEnabled(True)
            print(f"DEBUG: Save report button enabled: {self.save_report_btn.isEnabled()}")
        else:
            print(f"DEBUG: No pronunciation data found in metadata")
            if self.training_mode_cb.isChecked():
                print(f"DEBUG: Training mode is enabled but no pronunciation data received")
                self.output_text.append("\n⚠ Warning: Pronunciation training enabled but no analysis performed.")
        
        self.convert_btn.setEnabled(True)
    
    def display_pronunciation_feedback(self, pron_data):
        """Display detailed pronunciation feedback"""
        print(f"DEBUG: display_pronunciation_feedback called")
        print(f"DEBUG: Pronunciation data keys: {list(pron_data.keys())}")
        print(f"DEBUG: Accuracy: {pron_data.get('accuracy', 'N/A')}")
        print(f"DEBUG: Word analysis count: {len(pron_data.get('word_analysis', []))}")
        
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
    
    def play_tts(self):
        """Play text-to-speech for the reference text"""
        text = self.reference_text.text().strip()
        if not text:
            QMessageBox.warning(self, "No Text", "Please enter text to convert to speech.")
            return
        
        try:
            # Get language code from config (first part before dash)
            lang_code = self.config['language'].split('-')[0].lower()
            
            # Create TTS object
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # Create temporary file in memory
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            
            # Initialize pygame mixer
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_fp)
            pygame.mixer.music.play()
            
            self.output_text.append(f"🔊 Playing TTS: '{text}' in {self.config['language_name']}")
            
        except Exception as e:
            QMessageBox.critical(self, "TTS Error", f"Failed to play text-to-speech: {str(e)}")
            self.output_text.append(f"❌ TTS Error: {str(e)}")
    
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
   - Press and hold 'Hold to Record' button to start recording, release to stop

2. Configure Settings:
   - Click ⚙ to select engine, language, and model

3. Convert:
   - Click ASR Convert to transcribe audio

PRONUNCIATION TRAINING MODE:
1. Enable "Pronunciation Training Mode"
2. Enter the reference text you want to practice
3. Click "Play TTS" to hear the correct pronunciation
4. Record yourself reading the text
5. Click "ASR Convert" to get feedback

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
• Practice difficult words individually
• Hold the record button to start recording, release to stop"""
        
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
• Push-to-start/Push-to-stop recording
• Text-to-Speech (TTS) pronunciation guide

Default Language: Greek (el-GR)

Supports multiple languages and audio formats.

Built with PyQt5 and Python.
Perfect for language learners!"""
        
        QMessageBox.about(self, "About ASR App", about_text)
    
    def get_current_time(self):
        """Get current timestamp for status messages"""
        return datetime.now().strftime("%H:%M:%S")
    
    def show_config(self):
        dialog = ConfigDialog(self)
        # Set current values
        dialog.engine_combo.setCurrentText(self.config['engine'])
        dialog.lang_combo.setCurrentText(self.config['language_name'])
        dialog.model_combo.setCurrentText(self.config['model'])
        dialog.rate_entry.setText(str(self.config['sample_rate']))
        dialog.energy_entry.setText(str(self.config['energy_threshold']))
        dialog.pron_spin.setValue(self.config['pronunciation_threshold'])
        
        # Set Ollama model if it exists in config
        if 'ollama_model' in self.config:
            index = dialog.ollama_model_combo.findText(self.config['ollama_model'])
            if index >= 0:
                dialog.ollama_model_combo.setCurrentIndex(index)
        
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