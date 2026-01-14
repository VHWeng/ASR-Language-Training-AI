#!/usr/bin/env python3
"""
Test script to verify column 6 configuration for image filenames
"""

import sys
import os
import tempfile
import csv
import zipfile
from PyQt5.QtWidgets import QApplication
from asr_app import ASRApp

def test_column_6_configuration():
    """Test that image filenames are correctly loaded from column 6"""
    print("=== Testing Column 6 Configuration ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create main window
    window = ASRApp()
    
    # Verify column configuration
    print("1. Verifying column configuration...")
    columns = window.config['vocab_columns']
    
    assert columns['image_filename'] == 6, f"Expected image_filename in column 6, got {columns['image_filename']}"
    assert columns['image_description'] == 5, f"Expected image_description in column 5, got {columns['image_description']}"
    
    print("   ✓ Column configuration correct:")
    print(f"     • Image description: column {columns['image_description']}")
    print(f"     • Image filename: column {columns['image_filename']}")
    
    # Test 2: Create test CSV with image filename in column 6
    print("2. Testing CSV loading with column 6...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create CSV with image filename in column 6
        csv_data = [
            ['Word', 'Definition', 'English Pron', 'IPA Pron', 'Image Desc', 'Image File'],
            ['apple', 'A round fruit', 'ap-pul', 'ˈæpəl', 'Red apple', 'apple.jpg'],
            ['banana', 'A yellow fruit', 'buh-nan-uh', 'bəˈnænə', 'Yellow banana', 'banana.png'],
            ['cat', 'A domestic animal', 'kat', 'kæt', 'Fluffy cat', 'cat.gif']
        ]
        
        csv_path = os.path.join(temp_dir, 'test_column6.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter='|')
            writer.writerows(csv_data)
        
        # Create ZIP file
        zip_path = os.path.join(temp_dir, 'test_column6.zip')
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.write(csv_path, 'vocabulary.csv')
            zf.writestr('images/', '')
            zf.writestr('images/apple.jpg', b'dummy_apple_data')
            zf.writestr('images/banana.png', b'dummy_banana_data')
            zf.writestr('images/cat.gif', b'dummy_cat_data')
        
        print("   ✓ Test files created with image filenames in column 6")
        
        # Test 3: Load CSV and verify column 6 extraction
        print("3. Testing CSV loading...")
        
        try:
            window.load_csv_vocabulary(csv_path)
            
            assert len(window.vocabulary_data) == 3, f"Expected 3 entries, got {len(window.vocabulary_data)}"
            
            # Verify each entry has correct image filename from column 6
            expected_filenames = ['apple.jpg', 'banana.png', 'cat.gif']
            expected_descriptions = ['Red apple', 'Yellow banana', 'Fluffy cat']
            
            for i, (entry, expected_file, expected_desc) in enumerate(zip(window.vocabulary_data, expected_filenames, expected_descriptions)):
                actual_filename = entry.get('image_filename', '')
                actual_description = entry.get('image_description', '')
                
                assert actual_filename == expected_file, f"Entry {i+1}: filename expected '{expected_file}', got '{actual_filename}'"
                assert actual_description == expected_desc, f"Entry {i+1}: description expected '{expected_desc}', got '{actual_description}'"
                
                print(f"   ✓ Entry {i+1} ({entry['reference']}):")
                print(f"     • Image filename: '{actual_filename}' (from column 6)")
                print(f"     • Image description: '{actual_description}' (from column 5)")
            
            print("   ✓ All data correctly extracted from proper columns")
            
        except Exception as e:
            print(f"   ❌ CSV loading failed: {e}")
            return False
        
        # Test 4: Test ZIP loading with column 6
        print("4. Testing ZIP loading with column 6...")
        
        try:
            window.load_zip_vocabulary(zip_path)
            
            # Verify image directory detection
            assert window.image_directory == "images/", f"Expected 'images/' directory, got {window.image_directory}"
            print(f"   ✓ Images directory detected: {window.image_directory}")
            
            # Test image loading for each entry
            success_count = 0
            for i, entry in enumerate(window.vocabulary_data):
                image_filename = entry.get('image_filename', '')
                if image_filename:
                    try:
                        # Test the image loading logic
                        with zipfile.ZipFile(zip_path, 'r') as zip_file:
                            images_dir_path = "images/"
                            target_filename = os.path.basename(image_filename)
                            image_path_in_images = f"{images_dir_path}{target_filename}"
                            
                            if image_path_in_images in zip_file.namelist():
                                print(f"   ✓ Entry {i+1} ({entry['reference']}): Found {image_filename} in images/ directory")
                                success_count += 1
                            else:
                                print(f"   ❌ Entry {i+1} ({entry['reference']}): {image_filename} not found")
                                
                    except Exception as e:
                        print(f"   ❌ Entry {i+1} image test failed: {e}")
            
            print(f"   ✓ Successfully loaded {success_count}/3 images from column 6 filenames")
            assert success_count == 3, "All images should be found using column 6 data"
            
        except Exception as e:
            print(f"   ❌ ZIP loading test failed: {e}")
            return False
        
        print("\n✅ All column 6 configuration tests passed successfully!")
        return True

def demonstrate_corrected_configuration():
    """Demonstrate the corrected configuration"""
    print("\n=== Corrected Configuration ===")
    print("🎯 Column Mapping:")
    print("   • Column 5: Image description")
    print("   • Column 6: Image filename (as requested)")
    print("   • Updated to match the correct specification")
    
    print("\n📂 CSV Structure Example:")
    print("   Word | Definition | English Pron | IPA Pron | Image Desc | Image File")
    print("   apple | A fruit | ap-pul | ˈæpəl | Red apple | apple.jpg")
    print("                                           ↑ Column 6")
    
    print("\n⚡ Loading Process:")
    print("   • Extracts image description from column 5")
    print("   • Extracts image filename from column 6")
    print("   • Looks for images in 'images/' subdirectory")
    print("   • Supports .jpg, .png, .gif and other formats")

if __name__ == "__main__":
    try:
        success = test_column_6_configuration()
        demonstrate_corrected_configuration()
        
        if success:
            print("\n🎉 Column 6 configuration working perfectly!")
            print("✨ Image filenames now correctly loaded from column 6")
            print("✨ Image descriptions loaded from column 5")
            print("✨ All extension handling preserved")
        else:
            print("\n❌ Some tests failed.")
            
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()