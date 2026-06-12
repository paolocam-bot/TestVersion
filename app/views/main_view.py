import customtkinter as ctk

class MainView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # Configurazione Finestra Principale
        self.title("Applicazione MVC Agile")
        self.geometry("500x350")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Elementi Grafici dell'App Principale
        self.label_titolo = ctk.CTkLabel(self, text="Pannello di Controllo MVC", font=("Arial", 22, "bold"))
        self.label_titolo.pack(pady=30)

        self.btn_funzione = ctk.CTkButton(self, text="Esegui Azione Progetto", command=self.azione_cliccata)
        self.btn_funzione.pack(pady=10)

        self.label_status = ctk.CTkLabel(self, text="Stato: Pronto", font=("Arial", 12))
        self.label_status.pack(pady=20)

    def azione_cliccata(self):
        self.label_status.configure(text="Stato: Azione eseguita con successo!")

    def mostra_notifica_aggiornamento(self, nuova_versione, url):
        """Crea una finestra di dialogo grafica personalizzata per l'update"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Aggiornamento Disponibile")
        dialog.geometry("350x180")
        dialog.transient(self) # Rimane sopra la finestra principale
        dialog.resizable(False, False)

        lbl = ctk.CTkLabel(dialog, text=f"È disponibile la versione {nuova_versione}!\nVuoi scaricarla adesso?", font=("Arial", 14))
        lbl.pack(pady=20)

        def avvia_update():
            lbl.configure(text="Download in corso...\nL'app si riavvierà automaticamente.")
            btn.configure(state="disabled")
            # Chiediamo al controller di gestire l'aggiornamento in background
            self.after(100, lambda: self.controller.trigger_update(url))

        btn = ctk.CTkButton(dialog, text="Aggiorna Ora", fg_color="#2b719e", command=avvia_update)
        btn.pack(pady=10)