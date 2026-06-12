import os
import sys

# Questo dice a Python di aggiungere la cartella corrente alla lista dei percorsi di ricerca
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Ora l'import funzionerà senza problemi
from app.controllers.main_controller import MainController

if __name__ == "__main__":
    app = MainController()
    app.avvia_applicazione()