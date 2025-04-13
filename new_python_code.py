import os
import shutil
from PIL import Image
import imagehash
# from tkinter import Tk, filedialog  # Comment out tkinter imports
import sys  # Import sys for command-line arguments

def find_duplicate_images(folder_path):
    """
    Finds duplicate images in the given folder using perceptual hashing.

    Args:
        folder_path (str): The path to the folder containing images.

    Returns:
        dict: A dictionary where keys are image hashes and values are lists of
              file paths with that hash (duplicates).
    """
    hashes = {}
    for filename in os.listdir(folder_path):
        if any(filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']):
            img_path = os.path.join(folder_path, filename)
            try:
                img = Image.open(img_path)
                hash_value = imagehash.phash(img)
                if hash_value in hashes:
                    hashes[hash_value].append(img_path)
                else:
                    hashes[hash_value] = [img_path]
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
    return {hash_val: paths for hash_val, paths in hashes.items() if len(paths) > 1}

def move_duplicate_images(duplicate_sets, destination_folder):
    """
    Moves duplicate images to the specified destination folder.

    Args:
        duplicate_sets (dict): A dictionary of duplicate image file paths.
        destination_folder (str): The path to the folder where duplicates will be moved.
    """
    os.makedirs(destination_folder, exist_ok=True)
    moved_count = 0
    for hash_value, paths in duplicate_sets.items():
        # Keep the first occurrence, move the rest
        for i, img_path in enumerate(paths[1:]):
            try:
                filename = os.path.basename(img_path)
                destination_path = os.path.join(destination_folder, filename)
                shutil.move(img_path, destination_path)
                print(f"Moved duplicate: {filename} to {destination_folder}")
                moved_count += 1
            except Exception as e:
                print(f"Error moving {img_path}: {e}")
    print(f"\nSuccessfully moved {moved_count} duplicate images to {destination_folder}")

def main():
    """
    Main function to find duplicates and move them, taking folder path as argument.
    """
    if len(sys.argv) < 2:
        print("Usage: python duplicate_finder.py <folder_path> [destination_path]")
        return

    folder_selected = sys.argv[1]
    if not os.path.isdir(folder_selected):
        print(f"Error: Folder not found: {folder_selected}")
        return

    if len(sys.argv) > 2:
        destination_base = sys.argv[2]
    else:
        destination_base = folder_selected

    destination_folder = os.path.join(destination_base, "Duplicate_Images")

    duplicate_images = find_duplicate_images(folder_selected)

    if duplicate_images:
        move_duplicate_images(duplicate_images, destination_folder)
    else:
        print("No duplicate images found in the selected folder.")

if __name__ == "__main__":
    main()
