# Test Suite Documentation

This directory contains automated tests for the ASR Application with Pronunciation Training.

## Running Tests

To run all tests:
```bash
python -m pytest tests/
```

Or run specific test files:
```bash
python tests/test_integration_workflow.py
python tests/test_vocabulary_feature.py
```

## Test Categories

### Core Functionality Tests
- `test_vocabulary_feature.py` - Vocabulary loading and navigation
- `test_integration_workflow.py` - Complete user workflow testing
- `test_navigation_fix.py` - Navigation between vocabulary items
- `test_modern_ai_interface.py` - AI interface functionality

### Image Handling Tests
- `test_images_directory.py` - Directory-based image loading
- `test_zip_image_loading.py` - ZIP archive image handling
- `test_image_sizing_fix.py` - Image display sizing issues

### Column and Data Tests
- `test_column_extension.py` - Column mapping flexibility
- `test_column6_corrected.py` - Column 6 implementation
- `test_missing_data_fix.py` - Missing data handling
- `test_missing_data_fix_verification.py` - Missing data auto-generation

### AI and Pronunciation Tests
- `test_ai_status_colors.py` - AI status indicator visualization
- `test_pron_help_updates.py` - Pronunciation help enhancements
- `test_pronunciation_help.py` - Pronunciation assistance features
- `test_text_box_layout.py` - Text display layout

### Debug and Utility Tests
These are diagnostic tools and should typically not be run in production:
- `debug_pron_help.py` - Pronunciation help debugging
- `debug_widget_hierarchy.py` - Widget hierarchy analysis
- `minimal_visibility_test.py` - Minimal reproduction tests
- `simple_reproduction.py` - Simple issue reproduction
- `test_delayed_visibility.py` - Visibility timing issues
- `test_simple_fix.py` - Simple bug fixes
- `window_first_test.py` - Window initialization tests
- `verify_*` files - Various verification utilities

## Development Notes

- Tests are organized by functionality for easier maintenance
- Most tests can be run independently
- Integration tests (`test_integration_workflow.py`) test complete workflows
- Debug utilities are kept for development troubleshooting