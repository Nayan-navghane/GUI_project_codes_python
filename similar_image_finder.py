import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import imagehash
import os
import shutil

def select_input_image():
    global input_image_path
    input_image_path = filedialog.askopenfilename(title="Select Input Image")
    input_image_entry.delete(0, tk.END)
    input_image_entry.insert(tk.END, input_image_path)

def select_search_directory():
    global search_directory
    search_directory = filedialog.askdirectory(title="Select Search Directory")
    search_directory_entry.delete(0, tk.END)
    search_directory_entry.insert(tk.END, search_directory)

def find_similar_images():
    if not input_image_path or not search_directory:
        messagebox.showerror("Error", "Please select an input image and a search directory.")
        return

    try:
        input_hash = imagehash.phash(Image.open(input_image_path))
        similar_images = []
        for root, _, files in os.walk(search_directory):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    file_path = os.path.join(root, file)
                    try:
                        other_hash = imagehash.phash(Image.open(file_path))
                        if input_hash - other_hash < 5:  # Adjust the threshold as needed
                            similar_images.append(file_path)
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

        if similar_images:
            results_text.delete(1.0, tk.END)
            results_text.insert(tk.END, "Found similar images:\n")
            for img_path in similar_images:
                results_text.insert(tk.END, f"- {img_path}\n")
            global found_images
            found_images = similar_images
        else:
            results_text.delete(1.0, tk.END)
            results_text.insert(tk.END, "No similar images found.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the search: {e}")

def move_similar_images():
    if not found_images:
        messagebox.showinfo("Info", "No similar images found yet.")
        return

    new_folder_name = new_folder_entry.get()
    if not new_folder_name:
        messagebox.showerror("Error", "Please enter a name for the new folder.")
        return

    destination_folder = os.path.join(search_directory, new_folder_name)
    os.makedirs(destination_folder, exist_ok=True)

    moved_count = 0
    for img_path in found_images:
        try:
            shutil.move(img_path, os.path.join(destination_folder, os.path.basename(img_path)))
            moved_count += 1
        except Exception as e:
            messagebox.showerror("Error", f"Error moving {os.path.basename(img_path)}: {e}")

    messagebox.showinfo("Success", f"Successfully moved {moved_count} similar images to '{destination_folder}'.")
    results_text.delete(1.0, tk.END)
    

# --- GUI Setup ---
window = tk.Tk()
window.title("Image Similarity Finder")

input_image_path = ""
search_directory = ""
found_images = []

# Input Image Selection
input_label = tk.Label(window, text="Select Input Image:")
input_label.pack(pady=5)
input_frame = tk.Frame(window)
input_frame.pack()
input_image_entry = tk.Entry(input_frame, width=50)
input_image_entry.pack(side=tk.LEFT)
input_button = tk.Button(input_frame, text="Browse", command=select_input_image)
input_button.pack(side=tk.LEFT, padx=5)

# Search Directory Selection
search_label = tk.Label(window, text="Select Search Directory:")
search_label.pack(pady=5)
search_frame = tk.Frame(window)
search_frame.pack()
search_directory_entry = tk.Entry(search_frame, width=50)
search_directory_entry.pack(side=tk.LEFT)
search_button = tk.Button(search_frame, text="Browse", command=select_search_directory)
search_button.pack(side=tk.LEFT, padx=5)

# Find Similar Images Button
find_button = tk.Button(window, text="Find Similar Images", command=find_similar_images)
find_button.pack(pady=10)

# Results Display
results_label = tk.Label(window, text="Similar Images Found:")
results_label.pack()
results_text = tk.Text(window, height=5, width=60)
results_text.pack(pady=5)

# New Folder Name and Move Button
move_frame = tk.Frame(window)
move_frame.pack(pady=5)
new_folder_label = tk.Label(move_frame, text="New Folder Name:")
new_folder_label.pack(side=tk.LEFT)
new_folder_entry = tk.Entry(move_frame, width=30)
new_folder_entry.pack(side=tk.LEFT, padx=5)
move_button = tk.Button(move_frame, text="Move Similar Images", command=move_similar_images)
move_button.pack(side=tk.LEFT, padx=5)

window.mainloop()