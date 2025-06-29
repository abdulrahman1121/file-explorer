import tkinter as tk
from tkinter import filedialog, messagebox
import os

class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple File Explorer")
        self.root.geometry("800x600")

        # Current directory
        self.current_dir = tk.StringVar(value=os.getcwd())

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Directory entry and browse button
        tk.Label(self.root, text="Directory:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.current_dir, width=80).pack(pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_directory).pack(pady=5)

        # File listbox
        self.file_listbox = tk.Listbox(self.root, width=80, height=20)
        self.file_listbox.pack(pady=10)
        self.file_listbox.bind("<Double-Button-1>", self.open_file)

        # Text viewer
        self.text_viewer = tk.Text(self.root, width=80, height=10, state="disabled")
        self.text_viewer.pack(pady=10)

        # Load initial directory
        self.load_directory()

    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.current_dir.get())
        if directory:
            self.current_dir.set(directory)
            self.load_directory()

    def load_directory(self):
        self.file_listbox.delete(0, tk.END)
        directory = self.current_dir.get()
        try:
            for item in os.listdir(directory):
                self.file_listbox.insert(tk.END, item)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot access directory: {e}")

    def open_file(self, event):
        selected = self.file_listbox.curselection()
        if not selected:
            return
        file_name = self.file_listbox.get(selected[0])
        file_path = os.path.join(self.current_dir.get(), file_name)
        if os.path.isfile(file_path) and file_name.endswith((".txt", ".py")):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_viewer.config(state="normal")
                self.text_viewer.delete("1.0", tk.END)
                self.text_viewer.insert("1.0", content)
                self.text_viewer.config(state="disabled")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorer(root)
    root.mainloop()