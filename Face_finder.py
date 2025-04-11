import os
import shutil
import face_recognition
from tkinter import filedialog, Tk, Button, Label

def select_reference_image():
    global reference_image_path
    reference_image_path = filedialog.askopenfilename(title="Select Reference Image")
    label_ref.config(text=f"Reference Image:\n{reference_image_path}")

def select_target_folder():
    global target_folder
    target_folder = filedialog.askdirectory(title="Select Folder to Search")
    label_target.config(text=f"Target Folder:\n{target_folder}")

def find_and_move_matches():
    if not reference_image_path or not target_folder:
        result_label.config(text="Please select both reference image and target folder!")
        return

    # Load the reference image and encode face
    try:
        reference_image = face_recognition.load_image_file(reference_image_path)
        reference_encoding = face_recognition.face_encodings(reference_image)[0]
    except:
        result_label.config(text="Could not find face in reference image!")
        return

    # Create output folder
    output_folder = os.path.join(os.path.dirname(reference_image_path), "MatchedFaces")
    os.makedirs(output_folder, exist_ok=True)

    moved_count = 0

    # Scan through images in target folder
    for filename in os.listdir(target_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(target_folder, filename)
            try:
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)

                for face_encoding in encodings:
                    match = face_recognition.compare_faces([reference_encoding], face_encoding, tolerance=0.5)
                    if match[0]:
                        shutil.copy(image_path, os.path.join(output_folder, filename))
                        moved_count += 1
                        break
            except Exception as e:
                print(f"Skipping {filename}: {e}")
                continue

    result_label.config(text=f"✅ Moved {moved_count} matching images to '{output_folder}'")

# GUI setup
root = Tk()
root.title("Face Recognition Image Sorter")
root.geometry("500x300")

Button(root, text="Select Reference Image", command=select_reference_image).pack(pady=10)
label_ref = Label(root, text="No reference image selected", wraplength=400)
label_ref.pack()

Button(root, text="Select Folder to Search", command=select_target_folder).pack(pady=10)
label_target = Label(root, text="No target folder selected", wraplength=400)
label_target.pack()

Button(root, text="Find & Move Matching Faces", command=find_and_move_matches, bg="lightgreen").pack(pady=20)
result_label = Label(root, text="")
result_label.pack()

root.mainloop()
