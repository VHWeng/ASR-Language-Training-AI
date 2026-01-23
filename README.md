# ASR Application with Pronunciation Training

An advanced speech recognition application with pronunciation training capabilities, built using Python and PyQt5. This application provides comprehensive language learning tools including vocabulary management, AI-powered pronunciation assistance, and interactive speech recognition.

## 🚀 Key Features

### 🎯 Core Functionality
- **Speech Recognition**: Multiple engine support (Google Speech Recognition, Vosk, Whisper)
- **Pronunciation Training**: Interactive pronunciation practice with AI-powered feedback
- **Vocabulary Management**: Load and navigate through vocabulary sets from CSV/ZIP files
- **Image Support**: Display images associated with vocabulary entries
- **AI Integration**: Ollama-powered definition and pronunciation generation

### 📚 Vocabulary System
- Load vocabulary from CSV, TXT, or ZIP files
- Support for custom column mappings and delimiters
- Navigation between vocabulary entries (Previous/Next buttons)
- **Automatic AI enhancement for missing definitions/pronunciations**
- **Smart fallback to local IPA conversion when AI unavailable**
- Image loading from ZIP archives with "images" subdirectory support

### 🔊 Audio Features
- Audio recording and playback
- Text-to-Speech (TTS) with normal and slow modes
- ASR conversion with accuracy scoring
- Pronunciation feedback and assessment

### ⚙️ Configuration
- Customizable column mappings for vocabulary files
- Multiple delimiter support (comma, pipe, tab, semicolon)
- Language selection for speech recognition
- Ollama model configuration
- **Visual AI status indicator with color-coded feedback**

## Features

### 🎯 Core Functionality
- **Speech Recognition**: Multiple engine support (Google Speech Recognition, Vosk, Whisper)
- **Pronunciation Training**: Interactive pronunciation practice with AI-powered feedback
- **Vocabulary Management**: Load and navigate through vocabulary sets from CSV/ZIP files
- **Image Support**: Display images associated with vocabulary entries
- **AI Integration**: Ollama-powered definition and pronunciation generation

### 📚 Vocabulary System
- Load vocabulary from CSV, TXT, or ZIP files
- Support for custom column mappings and delimiters
- Navigation between vocabulary entries (Previous/Next buttons)
- **Automatic AI enhancement for missing definitions/pronunciations**
- **Smart fallback to local IPA conversion when AI unavailable**
- Image loading from ZIP archives with "images" subdirectory support

### 🔊 Audio Features
- Audio recording and playback
- Text-to-Speech (TTS) with normal and slow modes
- ASR conversion with accuracy scoring
- Pronunciation feedback and assessment

### ⚙️ Configuration
- Customizable column mappings for vocabulary files
- Multiple delimiter support (comma, pipe, tab, semicolon)
- Language selection for speech recognition
- Ollama model configuration
- **Visual AI status indicator with color-coded feedback**

## Installation

### Prerequisites
- Python 3.10 or higher (recommended)
- Git (for version control)
- FFmpeg (for audio processing)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ASR_Language_Training
```

2. Create virtual environment:
```bash
python -m venv venv
# Or for better compatibility:
python -m venv .venv
```

3. Activate virtual environment:
```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
# Install core requirements
pip install -r requirements.txt

# Optional: Install additional audio libraries for better compatibility
pip install pyaudio
```

### System Requirements

#### Required Dependencies
See [requirements.txt](requirements.txt) for detailed Python package dependencies.

#### System Dependencies
- **FFmpeg**: Required for MP3 support and audio processing
  - Windows: Download from https://ffmpeg.org/download.html
  - Ubuntu/Debian: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`

#### Recommended Hardware
- Microphone for recording
- Speakers or headphones for audio playback
- Modern CPU for Whisper processing (optional but recommended)

## Usage

### Starting the Application
```bash
python asr_app.py
```

### Getting Started

1. **Initial Setup**
   - Launch the application: `python asr_app.py`
   - Configure your preferred settings via the gear icon (⚙)

2. **Loading Vocabulary**
   - Click "📁 Load Vocabulary" to import your learning materials
   - Supported formats: CSV, TXT, or ZIP archives
   - Sample files are provided in the `Input/` directory
   - ZIP files should contain:
     - Vocabulary file in the root directory
     - Images folder named "images/" with corresponding image files
   - See `Input/README.md` for detailed sample file descriptions

3. **Interactive Learning**
   - Navigate through vocabulary items using Previous/Next buttons
   - View definitions, pronunciations, and associated images
   - AI automatically enhances entries with missing information

4. **Pronunciation Practice**
   - Listen to correct pronunciation via TTS (normal or slow speed)
   - Record your attempt using the "Hold to Record" feature
   - Receive detailed feedback on accuracy and improvement areas

### Advanced Features

#### AI-Powered Assistance
- Automatic generation of definitions and pronunciations
- Fallback to local IPA conversion when AI is unavailable
- Real-time status indicators showing AI connection state

#### Customization Options
- Map vocabulary columns to match your file structure
- Choose from multiple delimiter types (comma, pipe, tab, semicolon)
- Select preferred speech recognition engine and language

#### Image Integration
- Display contextual images for vocabulary items
- Support for common image formats (PNG, JPG, GIF)
- Automatic loading from ZIP archive structures

## Vocabulary File Format

### CSV Structure
Default column mapping:
```
Column 1: Reference Text (Word/Phrase)
Column 2: Definition/Translation  
Column 3: English Pronunciation
Column 4: IPA Pronunciation
Column 5: Image Description
Column 6: Image Filename
```

### Example CSV Format
```csv
Word|Definition|English Pron|IPA Pron|Image Desc|Image File
hello|A greeting|heh-low|həˈloʊ|Waving hand|hello.png
world|The earth|wurld|wɜrld|Planet Earth|world.png
αὐτός|he, she, it|af-toss|ˈav.tos|Person pointing|person.png
βλέπω|I see|vleh-po|ˈvle.po|Eye seeing|eye.png
```

### ZIP Archive Structure
```
vocabulary_package.zip
├── vocabulary.csv          # Main vocabulary file
└── images/                 # Image directory
    ├── hello.png
    ├── world.png
    ├── αὐτός.png
    └── βλέπω.png
```

## Configuration Options

### Column Mapping
Customize which columns contain what data:
- Reference Text Column
- Definition Column  
- English Pronunciation Column
- Image Filename Column (Column 6)
- Image Description Column (Column 5)

### Delimiters
Supported delimiters:
- Comma (,)
- Pipe (|)
- Tab (\t)
- Semicolon (;)

## AI Integration

### Ollama Setup
1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a suitable language model:
   ```bash
   # For general language tasks
   ollama pull llama3.2
   
   # For specialized linguistic tasks
   ollama pull mistral
   ```
3. Configure the model in application settings via the gear icon (⚙)
4. The application will automatically connect to Ollama when needed

### AI Capabilities

#### Smart Content Generation
- **Definition Creation**: Automatically generates clear, contextual definitions
- **Pronunciation Assistance**: Provides both English approximations and IPA notation
- **Intelligent Enhancement**: Fills gaps in vocabulary data without user intervention

#### Robust Reliability
- **Graceful Degradation**: Falls back to local IPA algorithms when AI is unavailable
- **Asynchronous Processing**: Non-blocking AI requests prevent interface freezing
- **Connection Resilience**: Handles network interruptions and timeouts gracefully

#### Visual Feedback System
Status indicators provide immediate insight into AI availability:
- ⚪ **Disconnected** (Gray): AI service not configured or available
- 🟢 **Connected** (Green): Ready to process requests
- 🔴 **Busy/Error** (Red): Processing request or encountered an error
- 🟡 **Connecting** (Orange): Establishing connection to AI service

## Testing

The project includes comprehensive automated testing organized in the `tests/` directory:

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python tests/test_integration_workflow.py    # Complete workflow testing
python tests/test_vocabulary_feature.py      # Vocabulary functionality
python tests/test_modern_ai_interface.py     # AI features

# See tests/README.md for detailed test descriptions
```

For comprehensive test documentation, see [tests/README.md](tests/README.md).

## Local Git

To save your changes to the local git repository, use the following commands:

```bash
# Stage all changes
git add .

# Commit the changes with a message
git commit -m "Your commit message here"

# Check the status of the repository
git status
```

## Project Structure

```
ASR_Language_Training/
├── asr_app.py                      # Main application
├── requirements.txt                # Python dependencies
├── README.md                       # Primary documentation
├── HELP.md                         # User guide and help
├── .gitignore                     # Git ignore rules
├── Input/                         # Sample datasets and media
│   ├── README.md                  # Sample files documentation
│   ├── Common Words.csv           # Basic Greek vocabulary
│   ├── Gamma & Chi Words.csv      # Specialized Greek letters
│   ├── Rolling R.csv              # Pronunciation practice
│   └── *.zip                      # Complete vocabulary packages (see Input/README.md)
└── tests/                         # Automated test suite
    ├── README.md                  # Test documentation
    ├── test_integration_workflow.py    # Complete workflow testing
    ├── test_vocabulary_feature.py      # Vocabulary functionality
    ├── test_modern_ai_interface.py     # AI features
    └── [additional test files]    # See tests/README.md for full list
```

## Troubleshooting

### Common Issues and Solutions

#### AI and Connectivity
**Ollama Connection Failed**
- ✅ Ensure Ollama service is running (`ollama serve`)
- ✅ Verify the configured model is downloaded (`ollama list`)
- ✅ Check firewall/network settings
- ✅ Confirm localhost:11434 accessibility

#### Media Handling
**Image Loading Failures**
- ✅ Validate ZIP structure (images/ subdirectory)
- ✅ Confirm supported formats (.png, .jpg, .jpeg, .gif)
- ✅ Verify column 6 contains correct relative filenames
- ✅ Check file permissions and path encoding

**Audio Recording Issues**
- ✅ Grant microphone permissions to Python/application
- ✅ Test audio drivers and system sound settings
- ✅ Adjust energy threshold in application settings
- ✅ Ensure no other applications are using the microphone

#### Performance Optimization
**Slow Processing**
- ✅ Use Whisper engine for highest accuracy
- ✅ Close other resource-intensive applications
- ✅ Consider using CPU-optimized models for older hardware

#### File Compatibility
**Vocabulary Loading Errors**
- ✅ Verify CSV encoding (UTF-8 recommended)
- ✅ Check delimiter consistency throughout file
- ✅ Ensure required columns are present
- ✅ Validate ZIP file integrity

### Debug Information
The application provides detailed status messages in the status text area at the bottom of the window.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure functionality
5. Submit a pull request

## License

[Specify your license here]

## Acknowledgments

- PyQt5 for the GUI framework
- Ollama for AI capabilities
- Various speech recognition engines
- Community contributors

## Version History

### Recent Enhancements

#### 🔄 Latest Improvements (2026)
- **Modern AI Interface**: Enhanced JSON response handling and improved debugging
- **Advanced Pronunciation Analysis**: More sophisticated feedback algorithms
- **Robust Error Recovery**: Better handling of network interruptions and timeouts
- **Performance Optimizations**: Faster loading and processing times
- **Enhanced User Experience**: Improved status messaging and visual feedback

#### 🛠 Technical Upgrades
- **Asynchronous Processing**: Non-blocking AI requests for smoother operation
- **Smart Fallback Systems**: Graceful degradation when external services unavailable
- **Comprehensive Testing**: Expanded automated test coverage
- **Improved Documentation**: Updated guides and clearer instructions

#### 📈 Feature Evolution
- **Dynamic Content Enhancement**: Automatic enrichment of vocabulary data
- **Flexible File Support**: Broader compatibility with various formats
- **Intelligent Navigation**: Smoother browsing between vocabulary items
- **Rich Media Integration**: Better image and audio handling

For complete version history and detailed changes, consult the git commit log.