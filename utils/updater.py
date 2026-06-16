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
    print(f"[DEBUG] Controllo aggiornamenti su: {url}")
    try:
        response = requests.get(url, timeout=5)
        print(f"[DEBUG] Risposta GitHub Status Code: {response.status_code}")
        
        if response.status_code == 200:
            releases = response.json()
            if releases:
                # Prendiamo i dati della release più recente
                data_release = releases[0]
                tag_name = data_release.get("tag_name", "")
                latest_version = tag_name.replace("v", "").strip()
                
                print(f"[DEBUG] Versione Locale: '{CURRENT_VERSION}' | Versione GitHub: '{latest_version}'")
                
                if latest_version > CURRENT_VERSION:
                    print("[DEBUG] Nuova versione rilevata!")
                    if "assets" in data_release and len(data_release["assets"]) > 0:
                        download_url = data_release["assets"][0]["browser_download_url"]
                        print(f"[DEBUG] URL Download trovato: {download_url}")
                        return latest_version, download_url
                    else:
                        print("[DEBUG] ERRORE: Nessun file (asset) allegato alla release di GitHub.")
                else:
                    print("[DEBUG] L'applicazione è già aggiornata rispetto a GitHub.")
            else:
                print("[DEBUG] Nessuna release trovata nel repository.")
        return None, None
    except Exception as e:
        # Questo print fondamentale ci dirà perché si bloccava!
        print(f"[DEBUG] ERRORE CRITICO nel controllo aggiornamenti: {e}")
        return None, None

def esegui_aggiornamento(url_download):
    try:
        # 1. Identificazione dei percorsi reali (Gestione Nuitka Onefile)
        if "NUITKA_ONEFILE_PARENT" in os.environ:
            percorso_attuale_exe = os.environ["NUITKA_ONEFILE_PARENT"]
        else:
            percorso_attuale_exe = os.path.abspath(sys.executable)
            if not percorso_attuale_exe.endswith(".exe"):
                percorso_attuale_exe = os.path.join(os.path.dirname(percorso_attuale_exe), "main.exe")

        cartella_attuale = os.path.dirname(percorso_attuale_exe)
        percorso_nuovo_exe = os.path.join(cartella_attuale, "update_nuova_versione.exe")

        # 2. Download binario pulito
        response = requests.get(url_download, stream=True)
        response.raise_for_status()
        with open(percorso_nuovo_exe, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # 3. CREAZIONE DELLO SCRIPT .BAT IN MODO COMPLETAMENTE ISOLATO
        # Scriviamo uno script temporaneo ma pulitissimo, senza sub-argomenti passati a CMD
        percorso_bat = os.path.join(cartella_attuale, "esegui_update.bat")
        
        contenuto_bat = (
            "@echo off\n"
            "timeout /t 2 /nobreak >nul\n"
            f"move /y \"{percorso_nuovo_exe}\" \"{percorso_attuale_exe}\"\n"
            f"start \"\" \"{percorso_attuale_exe}\"\n"
            "del \"%~f0\"\n"
        )
        
        # Salviamo in formato testo puro (ASCII) per impedire a Windows di scambiarlo per un binario
        with open(percorso_bat, "w", encoding="ascii") as f:
            f.write(contenuto_bat)

        # 4. LA SVOLTA: Diciamo a Windows di eseguire il .bat in modo nativo, senza passare da stringhe python
        os.startfile(percorso_bat)
        
        # 5. Chiudiamo subito l'app MVC per sbloccare il vecchio main.exe
        os._exit(0)
        
    except Exception as e:
        print(f"Errore critico durante la procedura: {e}")