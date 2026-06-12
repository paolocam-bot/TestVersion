import requests
import os
import sys

CURRENT_VERSION = "1.0.0"
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
            latest_version = data["tag_name"].replace("v", "") # Es: "v1.1.0" diventa "1.1.0"
            
            if latest_version > CURRENT_VERSION:
                print(f"Nuova versione disponibile: {latest_version}!")
                # Qui inseriremo la logica di download nello Sprint 3
            else:
                print("L'applicazione è aggiornata.")
        else:
            print("Impossibile verificare gli aggiornamenti al momento.")
    except Exception as e:
        print(f"Errore durante il controllo aggiornamenti: {e}")

if __name__ == "__main__":
    print("--- Benvenuto nella mia App Agile ---")
    check_for_updates()
    # Il resto del tuo programma va qui
    input("\nPremi Invio per uscire...")