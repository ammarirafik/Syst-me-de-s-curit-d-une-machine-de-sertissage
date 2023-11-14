import tkinter as tk
import smtplib
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import sqlite3

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

        self.bind('<Return>', lambda e: self.access_button.invoke())
        self.operator_entry = ttk.Entry(self, style='Custom.TEntry')
        self.password_entry = ttk.Entry(self, style='Custom.TEntry', show="*")

        self.operator_entry.bind('<Up>', lambda e: self.password_entry.focus())
        self.operator_entry.bind('<Down>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Up>', lambda e: self.operator_entry.focus())
        self.password_entry.bind('<Down>', lambda e: self.operator_entry.focus())

        self.attributes('-fullscreen', True)
        self.bind('<Escape>', lambda e: self.close_application())  # Nouvelle ligne
        self.configure(bg='white')

        style = ttk.Style()
        style.configure('Custom.TLabel', font=('Arial', 12, 'bold'), foreground='navy')

        logo_image = Image.open("DR.ico")
        logo_image = logo_image.resize((100, 100), Image.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(logo_image)

        self.header_label = ttk.Label(self, text="Accès sécurisé aux paramètres de HANKE 971", style='Custom.TLabel', anchor=tk.W)
        self.operator_label = ttk.Label(self, text="Matricule employé :", style='Custom.TLabel')
        self.password_label = ttk.Label(self, text=" Mot de passe:", style='Custom.TLabel')
        self.access_button = ttk.Button(self, text="Accéder", command=self.access_machine_settings, style='Custom.TButton')
        self.result_label = ttk.Label(self, text="", style='Custom.TLabel')
        self.logo_label = ttk.Label(self, image=self.logo_image)

        self.header_label.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        self.operator_label.pack(side=tk.TOP, padx=10, pady=10)
        self.operator_entry.pack(side=tk.TOP, padx=10, pady=5)
        self.password_label.pack(side=tk.TOP, padx=10, pady=10)
        self.password_entry.pack(side=tk.TOP, padx=10, pady=5)
        self.access_button.pack(side=tk.TOP, padx=10, pady=10)
        self.result_label.pack(side=tk.TOP, padx=10, pady=10)
        self.logo_label.pack(side=tk.TOP, padx=10, pady=20)

        self.operator_entry.focus()

        self.conn = None
        self.cursor = None
        self.connect_to_database()

    def connect_to_database(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        self.conn = conn
        self.cursor = cursor

    def check_operator_credentials(self, operator_id, operator_password):
        query = "SELECT * FROM users WHERE operator_id = ? AND operator_password = ?"
        self.cursor.execute(query, (operator_id, operator_password))
        result = self.cursor.fetchone()
        return result is not None

    def access_machine_settings(self):
        operator_id = self.operator_entry.get()
        operator_password = self.password_entry.get()

        if self.check_operator_credentials(operator_id, operator_password):
            self.result_label.config(text="Accès autorisé", foreground='green')
            self.notify_specialist(operator_id, "accès aux paramètres de HANKE 971")
        else:
            self.result_label.config(text="Accès refusé", foreground='red')
    def notify_specialist(self, operator_id, object_name):
        specialist_email = "rafikammari430@gmail.com"
        message = f"L'opérateur {operator_id} a accédé aux paramètres de la machine."
        subject = f"Notification : {object_name}"

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login("rafikammari430@gmail.com", "")
                email_message = f"Subject: {subject}\n\n{message}"
                server.sendmail("rafikammari430@gmail.com", specialist_email, email_message.encode('utf-8'))
            self.result_label.config(text="Notification envoyée avec succès", foreground='green')
        except Exception as e:
            print(f"Erreur lors de l'envoi de la notification : {str(e)}")
            self.result_label.config(text="Échec de l'envoi de la notification", foreground='red')

    def close_application(self):
        self.attributes('-fullscreen', False)  # Désactive le plein écran
        self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
