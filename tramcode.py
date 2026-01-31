import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time

# ----------------- Utilitaires -----------------
ASSET_IMAGE = "tram.png"

def load_tram_image(max_width=600, max_height=160):
    if os.path.exists(ASSET_IMAGE):
        img = Image.open(ASSET_IMAGE).convert("RGBA")
        img.thumbnail((max_width, max_height), Image.LANCZOS)
        return img
    return None

def rendre_monnaie(prix, monnaie):
    rendu = monnaie - prix
    dh10 = rendu // 10
    rendu %= 10
    dh5 = rendu // 5
    rendu %= 5
    dh2 = rendu // 2
    rendu %= 2
    dh1 = rendu
    return dh10, dh5, dh2, dh1

# ----------------- Application -----------------
class TramApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NAZIH Tramway")
        self.geometry("760x500")
        self.configure(bg="#111111")

        self.primary = "#cc1f1f"
        self.panel = "#1f1f1f"
        self.fg = "#f3f3f3"

        self.transaction_history = []
        self.create_widgets()

    def create_widgets(self):
        # Top
        top = tk.Frame(self, bg="#111111")
        top.pack(fill="x", padx=12, pady=10)

        img = load_tram_image()
        if img:
            self.tram_img = ImageTk.PhotoImage(img)
            tk.Label(top, image=self.tram_img, bg="#111111").pack(side="left")

        tk.Label(
            top,
            text="NAZIH Tramway",
            font=("Segoe UI", 20, "bold"),
            bg="#111111",
            fg=self.primary
        ).pack(anchor="w", padx=10)

        # Middle
        mid = tk.Frame(self, bg=self.panel)
        mid.pack(fill="x", padx=12, pady=10)

        left = tk.Frame(mid, bg=self.panel)
        left.pack(side="left", padx=12)

        tk.Label(left, text="Choisissez votre trajet :", bg=self.panel, fg=self.fg).pack(anchor="w")

        self.var_trajet = tk.IntVar(value=1)
        ttk.Radiobutton(left, text="Aller simple (8 Dh)", variable=self.var_trajet, value=1).pack(anchor="w")
        ttk.Radiobutton(left, text="Aller-retour (14 Dh)", variable=self.var_trajet, value=2).pack(anchor="w")

        tk.Label(left, text="Montant (Dh) :", bg=self.panel, fg=self.fg).pack(anchor="w", pady=(10, 0))
        self.entry_money = tk.Entry(left, width=12, justify="center")
        self.entry_money.pack(pady=5)

        tk.Button(
            left,
            text="Valider paiement",
            bg=self.primary,
            fg="white",
            command=self.process_payment
        ).pack(fill="x", pady=8)

        # Ticket zone
        self.ticket_canvas = tk.Canvas(mid, width=320, height=140, bg=self.panel, highlightthickness=0)
        self.ticket_canvas.pack(side="left", padx=20)

        # Historique
        right = tk.Frame(self, bg="#111111")
        right.pack(fill="both", expand=True, padx=12)

        tk.Label(right, text="Historique :", bg="#111111", fg=self.fg).pack(anchor="w")

        self.hist_text = tk.Text(right, height=10, bg="#0e0e0e", fg=self.fg)
        self.hist_text.pack(fill="both", expand=True)
        self.hist_text.config(state="disabled")

    def process_payment(self):
        s = self.entry_money.get().strip()
        if not s.isdigit():
            messagebox.showerror("Erreur", "Montant invalide")
            return

        monnaie = int(s)
        prix = 8 if self.var_trajet.get() == 1 else 14
        trajet = "Aller simple" if prix == 8 else "Aller-retour"

        if monnaie < prix:
            messagebox.showwarning("Insuffisant", f"Manque {prix - monnaie} Dh")
            return

        rendu = None
        if monnaie > prix:
            rendu = rendre_monnaie(prix, monnaie)

        self.add_history(trajet, prix, monnaie)
        self.show_ticket(trajet, prix, rendu)
        self.entry_money.delete(0, "end")

    def add_history(self, trajet, prix, paid):
        self.hist_text.config(state="normal")
        self.hist_text.insert(
            "end",
            f"{time.strftime('%H:%M:%S')} | {trajet} | Prix {prix} Dh | Payé {paid} Dh\n"
        )
        self.hist_text.config(state="disabled")

    def show_ticket(self, trajet, prix, rendu=None):
        c = self.ticket_canvas
        c.delete("all")

        c.create_rectangle(20, 20, 300, 120, fill="#fff7e6", outline="#d4a02a", width=2)

        txt = f"NAZIH Tramway\n{trajet}\nPrix : {prix} Dh\nBon voyage !"
        if rendu:
            txt += f"\nRendu : {rendu}"

        c.create_text(30, 30, anchor="nw", text=txt, font=("Segoe UI", 10, "bold"))

        # ⏱️ Ticket visible 5 minutes
        self.after(100000, lambda: c.delete("all"))

# ----------------- Run -----------------
if __name__ == "__main__":
    app = TramApp()
    app.mainloop()
