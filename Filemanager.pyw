import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

class FileManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Manager")
        self.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        select_folder_button = tk.Button(self, text="Mappa kiválasztása", command=self.select_folder)
        select_folder_button.pack(pady=10)

        sort_files_button = tk.Button(self, text="Fájlok rendezése", command=self.sort_files)
        sort_files_button.pack(pady=5)

        delete_empty_button = tk.Button(self, text="Üres fájlok és mappák törlése", command=self.delete_empty)
        delete_empty_button.pack(pady=5)

        delete_images_button = tk.Button(self, text="Képek törlése", command=self.delete_images)
        delete_images_button.pack(pady=5)

    def select_folder(self):
        self.selected_folder = filedialog.askdirectory()
        messagebox.showinfo("Kiválasztott mappa", f"A kiválasztott mappa:\n{self.selected_folder}")

    def sort_files(self):
        if hasattr(self, 'selected_folder') and self.selected_folder:
            file_types_to_folders = {
                "Dokumentumok": [".docx", ".txt"],
                "Images": [".png", ".jpg", ".jpeg"],
                "Codes": [".html", ".css", ".js", ".json", ".bash", ".sh", ".pyw", ".py", ".java"],
                "Programs": [".exe"],
                "Videos": [".mp4", ".m4v", ".avi", ".mov", ".wmv", ".mkv"],
                 "Audios": [".mp3"],
                 "Archives":[".zip",".rar","7zip"],
                # További fájltípusok és mappák hozzáadhatók
            }

            for root, dirs, files in os.walk(self.selected_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        file_extension = os.path.splitext(file)[1].lower()
                        for target_folder, extensions in file_types_to_folders.items():
                            if file_extension in extensions:
                                target_folder_path = os.path.join(self.selected_folder, target_folder)
                                if not os.path.exists(target_folder_path):
                                    os.makedirs(target_folder_path)
                                shutil.move(file_path, os.path.join(target_folder_path, file))
                                break

            messagebox.showinfo("Fájlok rendezése", "A fájlok sikeresen rendezve lettek!")
        else:
            messagebox.showwarning("Nincs kiválasztva mappa", "Először válassz ki egy mappát!")

    def delete_empty(self):
        if hasattr(self, 'selected_folder') and self.selected_folder:
            empty_files = []
            empty_folders = []

            for root, dirs, files in os.walk(self.selected_folder, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.getsize(file_path) == 0:
                        empty_files.append(file_path)

                for folder in dirs:
                    folder_path = os.path.join(root, folder)
                    if not os.listdir(folder_path):
                        empty_folders.append(folder_path)

            for file_path in empty_files:
                os.remove(file_path)
            for folder_path in empty_folders:
                os.rmdir(folder_path)

            if empty_files or empty_folders:
                messagebox.showinfo("Üres fájlok és mappák törlése", "Az üres fájlok és mappák sikeresen törölve lettek!")
            else:
                messagebox.showinfo("Nincs változás", "Nincs üres fájl vagy mappa a megadott helyen.")
        else:
            messagebox.showwarning("Nincs kiválasztva mappa", "Először válassz ki egy mappát!")

    def delete_images(self):
        if hasattr(self, 'selected_folder') and self.selected_folder:
            image_formats = [".png", ".jpg", ".jpeg"]
            image_files = []

            for root, dirs, files in os.walk(self.selected_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.splitext(file_path)[1].lower() in image_formats:
                        image_files.append(file_path)

            for image_path in image_files:
                os.remove(image_path)

            if image_files:
                messagebox.showinfo("Képek törlése", "A képek sikeresen törölve lettek!")
            else:
                messagebox.showinfo("Nincs változás", "Nincsenek elfogadott képek a megadott helyen.")
        else:
            messagebox.showwarning("Nincs kiválasztva mappa", "Először válassz ki egy mappát!")

if __name__ == "__main__":
    app = FileManagerApp()
    app.mainloop()