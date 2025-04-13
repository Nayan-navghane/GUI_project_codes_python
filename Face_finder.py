import os
import shutil
import face_recognition
from PIL import Image
from tkinter import Tk, filedialog

def find_similar_faces(reference_image_path, folder_path, tolerance=0.6):
    """
    Finds images in the given folder containing faces similar to the
    face in the reference image.

    Args:
        reference_image_path (str): Path to the reference image.
        folder_path (str): Path to the folder to search for similar faces.
        tolerance (float): Tolerance for face comparison (lower is stricter).

    Returns:
        list: A list of file paths of images containing similar faces.
    """
    try:
        reference_image = face_recognition.load_image_file(reference_image_path)
        reference_face_encodings = face_recognition.face_encodings(reference_image)

        if not reference_face_encodings:
            print("No face found in the reference image.")
            return []

        reference_face_encoding = reference_face_encodings[0]  # Use the first face found

        similar_images = []
        for filename in os.listdir(folder_path):
            if any(filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
                target_image_path = os.path.join(folder_path, filename)
                try:
                    target_image = face_recognition.load_image_file(target_image_path)
                    target_face_locations = face_recognition.face_locations(target_image)
                    target_face_encodings = face_recognition.face_encodings(target_image, target_face_locations)

                    for face_encoding in target_face_encodings:
                        face_distances = face_recognition.face_distance([reference_face_encoding], face_encoding)
                        if face_distances[0] <= tolerance:
                            similar_images.append(target_image_path)
                            break  # Found a similar face, move to the next image

                except Exception as e:
                    print(f"Error processing {target_image_path}: {e}")

        return similar_images

    except Exception as e:
        print(f"Error loading reference image: {e}")
        return []

def move_similar_face_images(similar_image_paths, destination_folder):
    """
    Moves images containing similar faces to the specified destination folder.

    Args:
        similar_image_paths (list): A list of file paths of images with similar faces.
        destination_folder (str): The path to the folder where similar face images will be moved.
    """
    if not similar_image_paths:
        print("No similar face images found to move.")
        return

    os.makedirs(destination_folder, exist_ok=True)
    moved_count = 0
    for img_path in similar_image_paths:
        try:
            filename = os.path.basename(img_path)
            destination_path = os.path.join(destination_folder, filename)
            shutil.move(img_path, destination_path)
            print(f"Moved similar face image: {filename} to {destination_folder}")
            moved_count += 1
        except Exception as e:
            print(f"Error moving {img_path}: {e}")
    print(f"\nSuccessfully moved {moved_count} images with similar faces to {destination_folder}")

def main():
    """
    Main function to select a reference image, a folder to search,
    find similar faces, and move the corresponding images.
    """
    root = Tk()
    root.withdraw()  # Hide the main window

    reference_image_path = filedialog.askopenfilename(title="Select the reference image")
    if not reference_image_path:
        print("No reference image selected. Exiting.")
        return

    folder_selected = filedialog.askdirectory(title="Select the folder to search for similar faces")
    if not folder_selected:
        print("No folder selected for searching. Exiting.")
        return

    similar_images = find_similar_faces(reference_image_path, folder_selected)

    if similar_images:
        destination_folder = os.path.join(folder_selected, "Similar_Face_Images")
        move_similar_face_images(similar_images, destination_folder)
    else:
        print("No images with similar faces found in the selected folder.")

if __name__ == "__main__":
    main()