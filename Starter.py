import os
import subprocess
import tempfile
from urllib.request import urlopen, urlretrieve
from zipfile import ZipFile
import sys
from tkinter import messagebox

BASE_DIR = os.path.join(os.path.expanduser("~"), "Documents", "ZombieMania")

EXE_PATH = os.path.join(BASE_DIR, "ZombieMania.exe") 
LOCAL_VERSION = os.path.join(BASE_DIR, "Version.txt")

URL_VERSION = "https://github.com/Darkzuzus/ZombieMania/releases/download/Latest/Version.txt"
URL_ZIP = "https://github.com/Darkzuzus/ZombieMania/releases/download/Latest/Install.zip"

def get_remote_version():
    try:
        return urlopen(URL_VERSION).read().decode().strip()
    except:
        return None


def get_local_version():
    try:
        with open(LOCAL_VERSION, "r") as f:
            return f.read().strip()
    except:
        return None


def reinstall():
    zip_path = os.path.join(tempfile.gettempdir(), "ZombieMania.zip")
    os.makedirs(BASE_DIR, exist_ok=True)

    print("Téléchargement de la mise à jour...")
    urlretrieve(URL_ZIP, zip_path)

    print("Installation...")
    with ZipFile(zip_path, "r") as z:
        for member in z.infolist():
            try:
                z.extract(member, BASE_DIR)
            except PermissionError:
                if "Starter" in member.filename or "launcher" in member.filename.lower():
                    continue
                else:
                    raise 

    if os.path.exists(zip_path):
        os.remove(zip_path)

def launch_game():
    if os.path.exists(EXE_PATH):
        subprocess.Popen([EXE_PATH], creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit() 
    else:
        reinstall()
        messagebox.showinfo(
            "Installation Complète", 
            "Le jeu a été installé avec succès !\nVeuillez relancer le launcher."
        )
        sys.exit()

def main():
    remote = get_remote_version()
    local = get_local_version()

    print("Local:", local)
    print("Remote:", remote)

    if remote is None:
        if os.path.exists(EXE_PATH):
            launch_game()
        else:
            messagebox.showerror(
                "Erreur de connexion", 
                "Impossible de se connecter au serveur pour l'installation initiale."
            )
        return
    if remote != local:
        print("Mise à jour requise...")
        try:
            reinstall()
            messagebox.showinfo(
                "Mise à jour réussie", 
                "Le client a été mis à jour avec succès !\nVeuillez relancer le launcher pour jouer."
            )
        except PermissionError as e:
            messagebox.showerror(
                "Erreur de Permission", 
                f"Impossible de mettre à jour le jeu.\n\nDétails : {e}\n\nAssurez-vous qu'aucune autre instance n'est ouverte."
            )
        return
    print("Le jeu est à jour.")
    launch_game()


if __name__ == "__main__":
    main()