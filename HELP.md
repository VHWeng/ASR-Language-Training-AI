# ASR Application Help Guide

## 📖 Table of Contents
- [Getting Started](#getting-started)
- [Core Features](#core-features)
- [Vocabulary Management](#vocabulary-management)
- [Pronunciation Training](#pronunciation-training)
- [AI Integration](#ai-integration)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

## 🚀 Getting Started

### Initial Setup
1. **Launch the Application**
   ```bash
   python asr_app.py
   ```

2. **First-Time Configuration** (Optional)
   - Click the gear icon ⚙ to access settings
   - Configure your preferred speech recognition engine
   - Set your default language
   - Configure Ollama AI settings if available

3. **Load Your First Vocabulary**
   - Click "📁 Load Vocabulary"
   - Select a CSV, TXT, or ZIP file
   - Start exploring your vocabulary items

### System Requirements
- **Python**: 3.10 or higher recommended
- **FFmpeg**: Required for audio processing
- **Microphone**: For recording practice sessions
- **Speakers/Headphones**: For audio playback
- **Ollama** (Optional): For AI-powered features

## 🎯 Core Features

### Speech Recognition Engines
The application supports multiple speech recognition engines:
- **Google Speech Recognition**: Cloud-based, high accuracy
- **Vosk**: Offline-capable, good for privacy
- **Whisper**: Open-source, excellent accuracy, requires more processing power

### Audio Controls
- **Record Button**: Hold to record, release to stop
- **Playback Controls**: Normal and slow-speed TTS
- **ASR Conversion**: Transcribe recorded audio with accuracy scoring

### Navigation
- **Previous/Next Buttons**: Move between vocabulary items
- **Progress Indicator**: Shows current position
- **Quick Jump**: Direct navigation to specific entries

## 📚 Vocabulary Management

### Supported File Formats
1. **CSV/TXT Files**
   - Customizable column mappings
   - Multiple delimiter support (comma, pipe, tab, semicolon)
   - UTF-8 encoding recommended

2. **ZIP Archives**
   - Vocabulary file in root directory
   - Images in "images/" subdirectory
   - Automatic extraction and organization

### Column Structure
Default mapping (customizable):
```
Column 1: Reference Text (Word/Phrase)
Column 2: Definition/Translation
Column 3: English Pronunciation
Column 4: IPA Pronunciation
Column 5: Image Description
Column 6: Image Filename
```

### Example Vocabulary File
```csv
Word|Definition|English Pron|IPA Pron|Image Desc|Image File
hello|A greeting|heh-low|həˈloʊ|Waving hand|hello.png
αὐτός|he, she, it|af-toss|ˈav.tos|Person pointing|person.png
βλέπω|I see|vleh-po|ˈvle.po|Eye seeing|eye.png
```

### Loading Vocabulary
1. Click "📁 Load Vocabulary"
2. Select your file (CSV, TXT, or ZIP)
3. Configure column mappings if needed
4. The application will automatically enhance entries with AI if available

## 🔊 Pronunciation Training

### Basic Workflow
1. **Select Vocabulary Item**
   - Browse using Previous/Next buttons
   - Or enter text directly in Reference Text field

2. **Listen to Model Pronunciation**
   - Click "🔊 Play TTS" for normal speed
   - Click "🐢 Slow TTS" for slower playback
   - Pay attention to stress and intonation

3. **Record Your Attempt**
   - Hold the record button to start
   - Release to stop recording
   - Speak clearly at a moderate pace

4. **Get Feedback**
   - Click "🔄 ASR Convert" to analyze your pronunciation
   - Review accuracy score and detailed feedback
   - Identify specific areas for improvement

### Feedback Components
- **Overall Accuracy Score**: Percentage match to reference
- **Word-by-Word Analysis**: Individual word accuracy
- **Mispronounced Words**: Highlighted problematic areas
- **Missing/Extra Words**: Content completeness check
- **Personalized Recommendations**: Targeted improvement suggestions
- **Color-Coded Results**: 
  - 🟢 Green: Excellent (90%+ accuracy)
  - 🟡 Yellow: Good (70-89% accuracy)
  - 🔴 Red: Needs Improvement (<70% accuracy)

### Practice Tips
- **Environment**: Find a quiet space for recording
- **Technique**: Speak clearly and at moderate pace
- **Consistency**: Practice regularly for best results
- **Focus**: Work on one challenging sound/word at a time
- **Patience**: Improvement takes time and repetition

## 🤖 AI Integration

### Ollama Setup
1. **Install Ollama**
   - Download from [ollama.ai](https://ollama.ai)
   - Follow installation instructions for your OS

2. **Download Language Model**
   ```bash
   # For general language tasks
   ollama pull llama3.2
   
   # For specialized linguistic analysis
   ollama pull mistral
   ```

3. **Configure in Application**
   - Click gear icon ⚙
   - Enter Ollama settings
   - Select your preferred model

### AI Features
- **Automatic Enhancement**: Fills missing definitions and pronunciations
- **Smart Definitions**: Context-aware, clear explanations
- **Pronunciation Guides**: Both English approximations and IPA notation
- **Graceful Fallback**: Local IPA conversion when AI unavailable

### AI Status Indicators
- ⚪ **Disconnected** (Gray): AI service not configured or available
- 🟢 **Connected** (Green): Ready to process requests
- 🔴 **Busy/Error** (Red): Processing request or encountered error
- 🟡 **Connecting** (Orange): Establishing connection to AI service

## 🔧 Troubleshooting

### Common Issues

#### Audio Problems
**Microphone Not Working**
- Check microphone permissions in system settings
- Ensure no other applications are using the microphone
- Test microphone in system audio settings
- Adjust energy threshold in application settings

**Poor Recording Quality**
- Move closer to microphone
- Reduce background noise
- Check microphone sensitivity settings
- Ensure proper microphone placement

#### AI Connection Issues
**Ollama Connection Failed**
- Verify Ollama is running (`ollama serve`)
- Check that your model is downloaded (`ollama list`)
- Confirm localhost:11434 is accessible
- Check firewall and network settings

**AI Responses Taking Too Long**
- Ensure adequate system resources
- Check internet connectivity (if required)
- Consider using a lighter model
- Verify Ollama service health

#### File Loading Problems
**Vocabulary Not Loading**
- Verify file format and encoding (UTF-8 recommended)
- Check delimiter consistency throughout file
- Ensure required columns are present
- Validate ZIP file integrity

**Images Not Displaying**
- Confirm images are in "images/" subdirectory for ZIP files
- Check supported formats (.png, .jpg, .jpeg, .gif)
- Verify column 6 contains correct relative filenames
- Check file permissions and path encoding

### Debug Information
The application provides detailed status messages:
- Bottom status text area shows real-time information
- Error messages include specific troubleshooting guidance
- Progress indicators for long-running operations
- Detailed logs available through console output

## ❓ FAQ

### General Questions

**Q: What languages are supported?**
A: The application supports multiple languages including Greek (default), English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, and Arabic.

**Q: Do I need internet connection?**
A: Basic functionality works offline. Internet is required for Google Speech Recognition and some AI features. Whisper and Vosk work offline.

**Q: How much RAM/CPU does it need?**
A: Minimum 4GB RAM recommended. Whisper processing benefits from more powerful CPUs or GPUs.

### Vocabulary Management

**Q: Can I create my own vocabulary files?**
A: Yes! Create CSV files with your desired content following the column structure outlined above.

**Q: What image formats are supported?**
A: PNG, JPG/JPEG, and GIF formats are supported for vocabulary images.

**Q: How do I organize ZIP files?**
A: Place your CSV file in the root, and all images in an "images/" subdirectory.

### AI Features

**Q: Is Ollama required?**
A: No, but it enhances the experience. The application falls back to local processing when AI is unavailable.

**Q: Which Ollama model should I use?**
A: Llama3.2 for general use, Mistral for more specialized linguistic tasks.

**Q: How does the AI enhancement work?**
A: When loading vocabulary with missing data, the application automatically requests definitions and pronunciations from your configured AI service.

### Audio and Pronunciation

**Q: Why is my accuracy score low?**
A: Common reasons include background noise, unclear pronunciation, speaking too fast, or accent differences. Practice in a quiet environment and speak clearly.

**Q: Can I adjust sensitivity settings?**
A: Yes, you can adjust the energy threshold and other audio settings in the configuration menu.

**Q: How do I improve my pronunciation?**
A: Regular practice, listening carefully to model pronunciations, focusing on problem areas, and using the slow playback feature.

## 📞 Support

For additional help:
1. Check the detailed status messages in the application
2. Review the troubleshooting section above
3. Examine console output for error details
4. Consult the README.md for technical documentation
5. Check git commit history for recent changes and fixes

---

*Last updated: January 2026*
*Version: 2.1.0*