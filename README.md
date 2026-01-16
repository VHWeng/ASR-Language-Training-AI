# ASR Application with Pronunciation Training

An advanced speech recognition application with pronunciation training capabilities, built using Python and PyQt5.

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
- Python 3.8 or higher
- Git (for version control)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ASRapp
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Requirements
See [requirements.txt](requirements.txt) for detailed dependencies.

## Usage

### Starting the Application
```bash
python asr_app.py
```

### Basic Workflow

1. **Configure Settings** (Optional)
   - Click the gear icon (⚙) to configure:
     - Speech recognition engine and language
     - Ollama model settings
     - Vocabulary column mappings
     - Delimiter settings

2. **Load Vocabulary**
   - Click "📁 Load Vocabulary" to load CSV/TXT/ZIP files
   - Supported formats: `.txt`, `.csv`, `.zip`
   - For ZIP files: CSV should be in root, images in "images/" subdirectory

3. **Practice Pronunciation**
   - Enter text in "Reference Text" field
   - Click "📥 Load AI" to get AI-generated pronunciation and definition
   - Use "🔊 Play TTS" or "🐢 Slow TTS" for audio playback
   - Record your pronunciation and click "🔄 ASR Convert" for feedback

4. **Navigate Vocabulary**
   - Use "◀ Previous" and "Next ▶" buttons to browse entries
   - Toggle image display with "Enable Image" checkbox

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

### Example CSV
```csv
Word|Definition|English Pron|IPA Pron|Image Desc|Image File
hello|A greeting|heh-low|həˈloʊ|Waving hand|hello.png
world|The earth|wurld|wɜrld|Planet Earth|world.png
```

### ZIP File Structure
```
vocabulary.zip
├── vocabulary.csv
└── images/
    ├── hello.png
    ├── world.png
    └── ...
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
2. Pull a language model:
   ```bash
   ollama pull kimi-k2:1t-cloud
   ```
3. Configure the model in application settings

### AI Features
- **Definition Generation**: Creates definitions for vocabulary entries
- **Pronunciation Guide**: Generates English and IPA pronunciations
- **Fallback Support**: Local IPA conversion when AI is unavailable
- **Visual Status Indicators**: Color-coded AI connection status
  - ⚪ Disconnected (Gray)
  - 🟢 Connected (Green)
  - 🔴 Busy (Red)
  - 🔴 Error (Red)
  - 🟡 Connecting (Orange)

## Testing

The project includes comprehensive test suites:

```bash
# Run all tests
python test_integration_workflow.py

# Test specific features
python test_vocabulary_feature.py
python test_zip_image_loading.py
python test_images_directory.py
python test_column_extension.py
python test_column6_corrected.py
python test_missing_data_fix_verification.py
python test_navigation_fix.py
python test_ai_status_colors.py
```

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
ASRapp/
├── asr_app.py                 # Main application
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .gitignore                # Git ignore rules
├── Input/                    # Sample input files
│   ├── vocabulary_sample.csv
│   └── vocabulary_sample.zip
├── test_*.py                 # Test files including:
│   ├── test_missing_data_fix_verification.py
│   ├── test_navigation_fix.py
│   └── test_ai_status_colors.py
└── verify_changes.py         # Verification scripts
```

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   - Ensure Ollama is installed and running
   - Check that the configured model is available
   - Verify network connectivity

2. **Image Loading Issues**
   - Ensure images are in "images/" subdirectory for ZIP files
   - Check file extensions (.jpg, .png, .gif supported)
   - Verify column 6 contains correct image filenames

3. **Audio Recording Problems**
   - Check microphone permissions
   - Verify audio drivers are working
   - Adjust energy threshold in settings

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

### Latest Updates
- **AI Status Indicator Fix**: Corrected the AI status indicator to show "Busy" (Red) during AI lookups.
- **Asynchronous AI Data Fetching**: Implemented threading for AI data requests to prevent UI freezing and improve responsiveness.
- **Automatic Vocabulary Enhancement**: When loading files with missing data, the application now automatically fetches pronunciation and definitions from the AI.
- **Column 6 Configuration**: Image filenames now loaded from column 6
- **Enhanced Image Loading**: Improved ZIP file image handling with extension support
- **AI Integration**: Robust fallback mechanisms for pronunciation and definitions
- **UI Improvements**: Better status feedback and error handling
- **Missing Data Auto-Generation**: Automatic AI enhancement for vocabulary entries with incomplete data
- **Visual AI Status Indicator**: Color-coded status display (Gray=Disconnected, Green=Connected, Red=Busy/Error, Orange=Connecting)
- **Enhanced Error Handling**: Improved timeout management and detailed error reporting for AI operations

For detailed changelog, see commit history.