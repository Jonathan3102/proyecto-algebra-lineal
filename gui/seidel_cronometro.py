import tkinter as tk
from tkinter import ttk


def crearSeidelCronometro(parent):
    frm = ttk.Frame(parent)

    ctrl = ttk.LabelFrame(frm, text="Comparación de tiempos", padding=5)
    ctrl.grid(row=0, column=0, sticky="ew", pady=4)

    ttk.Label(ctrl, text="Tamaño n:").grid(row=0, column=0, sticky="e")
    n_var = tk.IntVar(value=10)
    ttk.Entry(ctrl, textvariable=n_var, width=8).grid(row=0, column=1, sticky="w", padx=(2, 8))

    ttk.Button(ctrl, text="Cargar .csv").grid(row=0, column=2, padx=4)
    ttk.Button(ctrl, text="Generar aleatorio").grid(row=0, column=3, padx=4)
    ttk.Button(ctrl, text="Comparar").grid(row=0, column=4, padx=8)

    salida = ttk.LabelFrame(frm, text="Resultados", padding=5)
    salida.grid(row=1, column=0, sticky="nsew", pady=4)

    txt = tk.Text(salida, width=80, height=15, wrap="none")
    txt.pack(side="left", fill="both", expand=True)

    sb = ttk.Scrollbar(salida, command=txt.yview)
    sb.pack(side="right", fill="y")
    txt.config(yscrollcommand=sb.set)

    frm.columnconfigure(0, weight=1)
    frm.rowconfigure(1, weight=1)
    return frm