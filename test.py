import joblib

# Carica il modello SVM dalla pipeline salvata
model_path = 'C:/Users/casac/datamining/svm_pipeline.joblib'

import tkinter as tk
from tkinter import ttk
import joblib

loaded_pipeline = joblib.load(model_path)

def classify_plot():
    """
    Ottiene la trama dal campo di input e usa il modello SVM per fare una previsione.
    Visualizza la previsione nell'interfaccia.
    """
    predict_button.config(state='disabled', text='Classificando...')
    plot = text_input.get("0.8", "end-1c")  # Ottiene il testo dall'input
    genre_pred_svm = loaded_pipeline.predict([plot])
    result_label.config(text=f"Previsto: {genre_pred_svm[0]}")
    predict_button.config(state='normal', text='Classifica')

def clear_input():
    """
    Pulisce il campo di input e il label del risultato.
    """
    text_input.delete("1.0", "end")
    result_label.config(text="Previsto: ")

# Configura la finestra principale
root = tk.Tk()
root.title("Classificazione Genere Film")
root.geometry("400x300")  # Leggermente più grande per contenere i nuovi elementi
root.resizable(False, False)  # Impedisce il ridimensionamento della finestra

# Campo di input per la trama
text_input_label = ttk.Label(root, text="Inserisci la trama del film:")
text_input_label.pack(pady=(10,0))
text_input = tk.Text(root, height=5, width=50)
text_input.pack(padx=10, pady=5)

# Pulsante per inviare la trama
predict_button = ttk.Button(root, text="Classifica", command=classify_plot)
predict_button.pack(pady=5)

# Pulsante per pulire l'input
clear_button = ttk.Button(root, text="Pulisci", command=clear_input)
clear_button.pack(pady=(0,10))

# Etichetta per visualizzare il risultato
result_label = ttk.Label(root, text="Previsto: ")
result_label.pack(pady=5)

# Avvia l'interfaccia grafica
root.mainloop()
