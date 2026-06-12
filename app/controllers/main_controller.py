from app.views.main_view import MainView
from utils import updater

class MainController:
    def __init__(self):
        # Inizializziamo la vista passando questo controller
        self.view = MainView(self)

    def avvia_applicazione(self):
        # Prima di mostrare l'app, controlliamo in background se ci sono update
        nuova_versione, url_download = updater.check_for_updates()
        
        if nuova_versione:
            # Se c'è un aggiornamento, dice alla vista di mostrare il popup grafico
            self.view.mostra_notifica_aggiornamento(nuova_versione, url_download)
        
        # Avvia il loop grafico della finestra principale
        self.view.mainloop()

    def trigger_update(self, url):
        # Esegue la procedura di sovrascrittura isolata nell'updater
        updater.esegui_aggiornamento(url)