# Sample Vocabulary Files

This directory contains sample vocabulary files to demonstrate the ASR application's capabilities.

## File Types

### CSV Files (Small Reference Samples)
- `Common Words.csv` - Basic Greek vocabulary words
- `Gamma & Chi Words.csv` - Specialized Greek letter vocabulary  
- `Rolling R.csv` - Pronunciation practice for the Greek letter rho (ρ)

### ZIP Archives (Complete Vocabulary Packages)
All ZIP files follow the required structure:
```
vocabulary_package.zip
├── vocabulary.csv          # Main vocabulary file
└── images/                 # Image directory with vocabulary illustrations
    ├── word1.png
    ├── word2.png
    └── ...
```

## Sample Packages

### Essential Samples (Smaller Size)
- `Common_Words_Pen_and_Ink.zip` (~1.2MB) - Basic vocabulary with pen-and-ink style illustrations
- `Gamma_Chi_Words_Pen_and_Ink.zip` (~1.1MB) - Specialized Greek letter vocabulary
- `Rolling_R_Pen_and_Ink.zip` (~1.1MB) - Pronunciation practice focused on rho (ρ)

### Comprehensive Lessons (Larger Size)
- `Lesson01_Pen_and_Ink.zip` (~3.2MB) - Complete first lesson vocabulary
- `Lesson01_sentences_Pen_and_Ink.zip` (~2.1MB) - Sentence-based practice from lesson 1
- `Lesson02_Pen_and_Ink.zip` (~3.4MB) - Complete second lesson vocabulary  
- `Lesson02_sentences_Pen_and_Ink.zip` (~3.0MB) - Sentence-based practice from lesson 2

## Usage

Load any of these files using the "📁 Load Vocabulary" button in the application. The ZIP files provide the richest experience with both vocabulary and accompanying images.

## Creating Your Own Vocabulary

To create custom vocabulary files:
1. Create a CSV file with columns: Word|Definition|English Pron|IPA Pron|Image Desc|Image File
2. For ZIP packages, include an "images/" subdirectory with corresponding image files
3. Supported image formats: PNG, JPG, JPEG, GIF

See the main README.md for detailed file format specifications.