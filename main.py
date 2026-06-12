import requests
import os
import sys

CURRENT_VERSION = "1.0.0"
# Sostituisci questi valori con i dati reali del tuo GitHub
REPO_OWNER = "IL_TUO_NOME_UTENTE_GITHUB"
REPO_NAME = "IL_NOME_DEL_TUO_REPOSITORY"

def check_for_updates():
    print(f"Versione corrente: {CURRENT_VERSION}")
    print("Controllo aggiornamenti in corso...")
    
    # URL delle API di GitHub per l'ultima release
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # GitHub usa spesso i tag con la 'v' (es. v1.1.0). La togliamo per il confronto.
            latest_version = data["tag_name"].replace("v", "") 
            
            if latest_version > CURRENT_VERSION:
                print(f"\n[!] Nuova versione disponibile: {latest_version}!")
                
                # Prendiamo il link di download del primo file (asset) allegato alla release
                if "assets" in data and len(data["assets"]) > 0:
                    download_url = data["assets"][0]["browser_download_url"]
                    asset_name = data["assets"][0]["name"]
                    
                    print(f"Trovato file: {asset_name}")
                    scelta = input("Vuoi scaricare l'aggiornamento adesso? (s/n): ").strip().lower()
                    
                    if scelta == 's':
                        scarica_aggiornamento(download_url)
                else:
                    print("Errore: Nessun file compilato trovato nella release di GitHub.")
            else:
                print("L'applicazione è già aggiornata all'ultima versione.")
        else:
            print(f"Impossibile verificare gli aggiornamenti (Codice errore GitHub: {response.status_code}).")
    except Exception as e:
        print(f"Errore durante il controllo aggiornamenti: {e}")

def scarica_aggiornamento(url):
    try:
        print("Download in corso... Attendi.")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Capiamo dove si trova questo eseguibile e come si chiama
        percorso_attuale = sys.executable
        cartella_attuale = os.path.dirname(percorso_attuale)
        
        # Creiamo il file temporaneo nella stessa cartella (es: main_new.exe)
        nome_nuovo_file = os.path.join(cartella_attuale, "update_nuova_versione.exe")
        
        with open(nome_nuovo_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    
        print("\n[✓] Aggiornamento scaricato con successo!")
        print(f"Salvato come: {nome_nuovo_file}")
        print("Chiudi il programma e sostituisci il vecchio file con questo per completare l'aggiornamento.")
        
    except Exception as e:
        print(f"Errore durante il download del file: {e}")

if __name__ == "__main__":
    print("--- Benvenuto nella mia App Agile ---")
    check_for_updates()
    
    # --- Il codice della tua applicazione inizia qui ---
    print("\n[Esecuzione programma principale...]")
    # ----------------------------------------------------
    
    input("\nPremi Invio per uscire...")