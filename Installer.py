import os
import tempfile
import threading
from win32com.client import Dispatch
from zipfile import ZipFile
from urllib.request import urlretrieve

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

URL = "https://github.com/Darkzuzus/ZombieMania/releases/download/Latest/Install.zip"



def create_shortcut(target, name):
    desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
    shortcut_path = os.path.join(desktop, f"{name}.lnk")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.IconLocation = target
    shortcut.save()

class Installer:

    def __init__(self, root):

        self.root = root
        self.root.title("ZombieMania Setup")
        self.root.geometry("700x350")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.center_window()

        tk.Label(
            root,
            text="ZOMBIEMANIA",
            font=("Arial", 26, "bold"),
            fg="#00ff00",
            bg="#1e1e1e"
        ).pack(pady=10)

        self.status = tk.Label(
            root,
            text="Prêt à installer",
            fg="white",
            bg="#1e1e1e"
        )
        self.status.pack(pady=10)

        self.progress = ttk.Progressbar(
            root,
            length=600,
            mode="determinate"
        )
        self.progress.pack(pady=15)

        self.percent = tk.Label(
            root,
            text="0%",
            fg="white",
            bg="#1e1e1e"
        )
        self.percent.pack()

        self.install_btn = tk.Button(
            root,
            text="INSTALLER",
            bg="#333",
            fg="white",
            command=self.start_install
        )
        self.install_btn.pack(pady=15)

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 350
        y = (self.root.winfo_screenheight() // 2) - 175
        self.root.geometry(f"700x350+{x}+{y}")

    def start_install(self):
        self.install_btn.config(state="disabled")
        threading.Thread(target=self.install, daemon=True).start()

    def update_progress(self, count, block_size, total_size):

        if total_size > 0:
            percent = int(count * block_size * 100 / total_size)
            percent = min(percent, 100)

            self.progress["value"] = percent
            self.percent.config(text=f"{percent}%")
            self.root.update_idletasks()

    def install(self):

        try:
            install_path = os.path.join(os.path.expanduser("~"), "Documents", "ZombieMania")
            

            os.makedirs(install_path, exist_ok=True)

            zip_path = os.path.join(tempfile.gettempdir(), "ZombieMania.zip")

            self.status.config(text="Téléchargement...")

            urlretrieve(URL, zip_path, self.update_progress)

            self.status.config(text="Installation...")

            with ZipFile(zip_path, "r") as z:
                z.extractall(install_path)

            os.remove(zip_path)

            launcher_exe = os.path.join(install_path, "Starter.exe")

            create_shortcut(launcher_exe, "ZombieMania")

            self.finish()

        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            self.root.destroy()

    def finish(self):

        self.progress.pack_forget()
        self.percent.pack_forget()

        self.status.config(text="Installation terminée !")

        self.root.after(2500, self.root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = Installer(root)
    root.mainloop()