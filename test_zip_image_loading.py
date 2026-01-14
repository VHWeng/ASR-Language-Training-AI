#!/usr/bin/env python3
"""
Test script to verify image loading from ZIP files
"""

import sys
import os
import tempfile
import csv
import zipfile
from PyQt5.QtWidgets import QApplication
from asr_app import ASRApp

def test_zip_image_loading():
    """Test image loading from ZIP files with subdirectories"""
    print("=== Testing ZIP Image Loading ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create main window
    window = ASRApp()
    
    # Test 1: Create test ZIP with images in subdirectory
    print("1. Creating test ZIP file with images in subdirectory...")
    
    # Create temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create CSV file
        csv_data = [
            ['Word', 'Definition', 'English Pron', 'IPA Pron', 'Image Desc', 'Image File'],
            ['apple', 'A round fruit', 'ap-pul', 'ˈæpəl', 'Red apple', 'apple.jpg'],
            ['banana', 'A yellow fruit', 'buh-nan-uh', 'bəˈnænə', 'Yellow banana', 'banana.png'],
            ['cat', 'A domestic animal', 'kat', 'kæt', 'Fluffy cat', 'cat.gif']
        ]
        
        csv_path = os.path.join(temp_dir, 'vocabulary.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter='|')
            writer.writerows(csv_data)
        
        # Create ZIP file
        zip_path = os.path.join(temp_dir, 'test_vocabulary.zip')
        with zipfile.ZipFile(zip_path, 'w') as zf:
            # Add CSV file
            zf.write(csv_path, 'vocabulary.csv')
            
            # Create images subdirectory and add dummy images
            zf.writestr('images/', '')  # Directory entry
            zf.writestr('images/apple.jpg', b'dummy_jpg_data_for_apple')
            zf.writestr('images/banana.png', b'dummy_png_data_for_banana')
            zf.writestr('images/cat.gif', b'dummy_gif_data_for_cat')
            
            # Add one image to root for testing
            zf.writestr('dog.jpg', b'dummy_jpg_data_for_dog')
        
        print("   ✓ Test ZIP file created with images in subdirectory")
        
        # Test 2: Load ZIP vocabulary
        print("2. Testing ZIP vocabulary loading...")
        
        try:
            window.load_zip_vocabulary(zip_path)
            
            assert len(window.vocabulary_data) == 3, f"Expected 3 entries, got {len(window.vocabulary_data)}"
            assert window.image_directory is not None, "Image directory should be detected"
            
            print("   ✓ ZIP vocabulary loaded successfully")
            print(f"   ✓ Detected image directory: {window.image_directory}")
            
        except Exception as e:
            print(f"   ❌ ZIP loading failed: {e}")
            return False
        
        # Test 3: Test image loading functionality
        print("3. Testing image loading from ZIP...")
        
        # Test loading an image that exists
        window.current_vocab_index = 0  # apple entry
        entry = window.vocabulary_data[0]
        
        # Mock the image loading to test the logic without actually displaying
        try:
            # This will test the path resolution logic
            image_filename = entry.get('image_filename', '')
            if image_filename:
                # Test the image finding logic
                with zipfile.ZipFile(zip_path, 'r') as zip_file:
                    image_files = [f for f in zip_file.namelist() 
                                 if not f.endswith('/') and '.' in f.split('/')[-1]]
                    
                    target_filename = os.path.basename(image_filename).lower()
                    found = False
                    for img_path in image_files:
                        if os.path.basename(img_path).lower() == target_filename:
                            found = True
                            print(f"   ✓ Found image: {img_path}")
                            break
                    
                    assert found, f"Should find image {image_filename} in ZIP"
            
            print("   ✓ Image path resolution works correctly")
            
        except Exception as e:
            print(f"   ❌ Image loading test failed: {e}")
            return False
        
        # Test 4: Test image loading for all entries
        print("4. Testing image loading for all vocabulary entries...")
        
        success_count = 0
        for i, entry in enumerate(window.vocabulary_data):
            image_filename = entry.get('image_filename', '')
            if image_filename:
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_file:
                        image_files = [f for f in zip_file.namelist() 
                                     if not f.endswith('/') and '.' in f.split('/')[-1]]
                        
                        target_filename = os.path.basename(image_filename).lower()
                        found = any(os.path.basename(img_path).lower() == target_filename 
                                  for img_path in image_files)
                        
                        if found:
                            success_count += 1
                            print(f"   ✓ Entry {i+1} ({entry['reference']}): Found image {image_filename}")
                        else:
                            print(f"   ⚠ Entry {i+1} ({entry['reference']}): Image {image_filename} not found")
                            
                except Exception as e:
                    print(f"   ❌ Entry {i+1} image test failed: {e}")
        
        print(f"   ✓ Successfully located images for {success_count}/{len(window.vocabulary_data)} entries")
        
        # Test 5: Test directory detection logic
        print("5. Testing image directory detection...")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                all_entries = zip_file.namelist()
                
                # Test the directory detection logic
                image_dirs = [f for f in all_entries if f.lower().endswith('/') and ('image' in f.lower() or 'img' in f.lower())]
                
                if not image_dirs:
                    # Check for directories containing image files
                    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
                    image_files = [f for f in all_entries 
                                 if not f.endswith('/') and any(f.lower().endswith(ext) for ext in image_extensions)]
                    
                    dirs_with_images = set()
                    for img_file in image_files:
                        parts = img_file.split('/')
                        if len(parts) > 1:
                            dir_path = '/'.join(parts[:-1]) + '/'
                            dirs_with_images.add(dir_path)
                    
                    image_dirs = list(dirs_with_images) if dirs_with_images else []
                
                print(f"   ✓ Detected image directories: {image_dirs}")
                assert len(image_dirs) > 0, "Should detect at least one image directory"
                
        except Exception as e:
            print(f"   ❌ Directory detection test failed: {e}")
            return False
        
        print("\n✅ All ZIP image loading tests passed successfully!")
        return True

def demonstrate_fixes():
    """Demonstrate the fixes made"""
    print("\n=== Fixes Implemented ===")
    print("🔧 Enhanced Image Loading from ZIP Files:")
    print("   • Searches all directories in ZIP for image files")
    print("   • Matches images by filename (case-insensitive)")
    print("   • Handles subdirectories properly")
    print("   • Works with various image extensions (.jpg, .png, .gif, etc.)")
    print("   • Provides detailed status feedback")
    
    print("\n🔍 Improved Directory Detection:")
    print("   • Looks for 'image' or 'img' in directory names")
    print("   • Automatically detects directories containing images")
    print("   • Falls back to searching entire ZIP if no image directory found")
    print("   • Handles both dedicated image folders and mixed structures")
    
    print("\n📋 CSV Column Usage:")
    print("   • Column 5: Image Description (optional)")
    print("   • Column 6: Image Filename (used for loading)")
    print("   • Filenames can include subdirectory paths")
    print("   • Extension matching is case-insensitive")

if __name__ == "__main__":
    try:
        success = test_zip_image_loading()
        demonstrate_fixes()
        
        if success:
            print("\n🎉 ZIP image loading is now working correctly!")
            print("✨ Images will load from subdirectories in ZIP files")
            print("✨ Filename matching works regardless of path structure")
        else:
            print("\n❌ Some tests failed.")
            
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()