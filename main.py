import requests
import os
import sys
import subprocess

CURRENT_VERSION = "0.1.0"  # Cambiala a "0.2.0" quando compilerai la nuova versione
REPO_OWNER = "paolocam-bot"
REPO_NAME = "TestVersion"

def check_for_updates():
    print(f"--- Benvenuto nella mia App Agile ---")
    print(f"Versione corrente: {CURRENT_VERSION}")
    print("Controllo aggiornamenti in corso...")
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            releases = response.json()
            
            if len(releases) > 0:
                data = releases[0] 
                latest_version = data["tag_name"].replace("v", "") 
                
                if latest_version > CURRENT_VERSION:
                    print(f"\n[!] Nuova versione disponibile su GitHub: {latest_version}!")
                    
                    if "assets" in data and len(data["assets"]) > 0:
                        download_url = data["assets"][0]["browser_download_url"]
                        
                        scelta = input("Vuoi installare l'aggiornamento adesso? (s/n): ").strip().lower()
                        if scelta == 's':
                            scarica_e_installa_aggiornamento(download_url)
                    else:
                        print("Errore: Nessun file .exe trovato nella release di GitHub.")
                else:
                    print("L'applicazione è già aggiornata.")
        else:
            print(f"Impossibile verificare gli aggiornamenti (Errore GitHub: {response.status_code}).")
    except Exception as e:
        print(f"Errore durante il controllo aggiornamenti: {e}")

def scarica_e_installa_aggiornamento(url):
    try:
        # 1. Identificazione dei percorsi reali (Gestione Nuitka Onefile)
        if "NUITKA_ONEFILE_PARENT" in os.environ:
            percorso_attuale_exe = os.environ["NUITKA_ONEFILE_PARENT"]
        else:
            percorso_attuale_exe = os.path.abspath(sys.executable)
            
        cartella_attuale = os.path.dirname(percorso_attuale_exe)
        nome_exe_attuale = os.path.basename(percorso_attuale_exe)
        
        # Sicurezza per l'ambiente di sviluppo .py
        if not percorso_attuale_exe.endswith(".exe") or "python" in nome_exe_attuale.lower():
            nome_exe_attuale = "main.exe"
            percorso_attuale_exe = os.path.join(cartella_attuale, nome_exe_attuale)

        percorso_nuovo_exe = os.path.join(cartella_attuale, "update_nuova_versione.exe")
        
        # Pulizia preventiva di vecchi residui di test
        if os.path.exists(percorso_nuovo_exe):
            os.remove(percorso_nuovo_exe)
        
        # 2. Download del nuovo .exe da GitHub
        print("Download dell'aggiornamento in corso...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(percorso_nuovo_exe, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print("[OK] Nuovo eseguibile scaricato.")
        print("\n[!] Preparazione scambio file in corso...")

        # 3. IL TRUCCO: Un comando CMD concatenato in un'unica riga
        # Spiegazione dei comandi separati da && (esegui uno dopo l'altro):
        # - timeout /t 3: aspetta 3 secondi che Python si chiuda
        # - move /y ...: sovrascrive il file vecchio con il nuovo
        # - start ...: riavvia l'applicazione aggiornata
        comando_cmd = (
            f'timeout /t 3 /nobreak >nul && '
            f'move /y "{percorso_nuovo_exe}" "{percorso_attuale_exe}" && '
            f'start "" "{percorso_attuale_exe}"'
        )
        
        # 4. Lanciamo CMD passandogli la stringa di comandi. 
        # /c dice a CMD di eseguire la stringa e poi chiudersi.
        # Usiamo os.system o subprocess in modo che apra una finestra visibile per fare il debug!
        print("[!] Chiusura applicazione. Guarda la finestra di Windows che si apre...")
        
        # Questo comando apre una vera istanza di CMD indipendente
        subprocess.Popen(f'cmd.exe /c "{comando_cmd}"', shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        # 5. Chiusura istantanea e totale dell'applicazione Python per liberare il file
        os._exit(0)
        
    except Exception as e:
        print(f"Errore critico durante la procedura: {e}")


if __name__ == "__main__":
    check_for_updates()
    
    # --- Qui inizia la tua vera applicazione ---
    print("\n[Esecuzione della tua App Super Agile...]")
    print("Lavoriamo sodo sulle nuove feature dello Sprint!")
    # ------------------------------------------
    
    input("\nPremi Invio per chiudere l'app...")