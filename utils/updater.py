import os
import sys
import subprocess
import requests

CURRENT_VERSION = "0.1.0"
REPO_OWNER = "paolocam-bot"
REPO_NAME = "TestVersion"

def get_real_path(relative_path):
    """Trova il percorso corretto sia in sviluppo che dentro Nuitka Onefile"""
    base_path = os.environ.get("NUITKA_ONEFILE_PARENT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.normpath(os.path.join(base_path, relative_path))

def check_for_updates():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            releases = response.json()
            if releases:
                latest_version = releases[0]["tag_name"].replace("v", "")
                if latest_version > CURRENT_VERSION:
                    if "assets" in releases[0] and len(releases[0]["assets"]) > 0:
                        return latest_version, releases[0]["assets"][0]["browser_download_url"]
        return None, None
    except Exception:
        return None, None

def esegui_aggiornamento(url_download):
    try:
        # Determina l'eseguibile reale attuale
        if "NUITKA_ONEFILE_PARENT" in os.environ:
            percorso_attuale_exe = os.environ["NUITKA_ONEFILE_PARENT"]
        else:
            percorso_attuale_exe = os.path.abspath(sys.executable)
            if not percorso_attuale_exe.endswith(".exe"):
                # Fallback per l'ambiente di sviluppo .py
                percorso_attuale_exe = os.path.join(os.path.dirname(percorso_attuale_exe), "main.exe")

        cartella_attuale = os.path.dirname(percorso_attuale_exe)
        percorso_nuovo_exe = os.path.join(cartella_attuale, "update_nuova_versione.exe")

        # Download binario del file
        response = requests.get(url_download, stream=True)
        response.raise_for_status()
        with open(percorso_nuovo_exe, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # Comando CMD concatenato (invisibile o visibile) per scambiare i file
        comando_cmd = (
            f'timeout /t 2 /nobreak >nul && '
            f'move /y "{percorso_nuovo_exe}" "{percorso_attuale_exe}" && '
            f'start "" "{percorso_attuale_exe}"'
        )
        
        subprocess.Popen(f'cmd.exe /c "{comando_cmd}"', shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        os._exit(0)
    except Exception as e:
        print(f"Errore di aggiornamento: {e}")