import tkinter as tk
from tkinter import ttk


def crearEliminacionGaussiana(parent):
    frm = ttk.Frame(parent)

    ctrl = ttk.LabelFrame(frm, text="Datos de entrada", padding=5)
    ctrl.grid(row=0, column=0, sticky="ew", pady=4)

    ttk.Label(ctrl, text="Tamaño n (2-8):").grid(row=0, column=0, sticky="e")
    n_var = tk.IntVar(value=2)
    ttk.Spinbox(ctrl, from_=2, to=8, textvariable=n_var, width=4).grid(
        row=0, column=1, sticky="w", padx=(2, 8)
    )

    ttk.Button(ctrl, text="Cargar .csv").grid(row=0, column=2, padx=4)
    ttk.Button(
        ctrl,
        text="Crear tabla",
        command=lambda: _crear_tabla(frm, n_var),
    ).grid(row=0, column=3, padx=4)

    paso = ttk.LabelFrame(frm, text="Paso a paso", padding=5)
    paso.grid(row=1, column=0, sticky="nsew", pady=4)

    txt = tk.Text(paso, width=80, height=12, wrap="none")
    txt.pack(side="left", fill="both", expand=True)

    sb = ttk.Scrollbar(paso, command=txt.yview)
    sb.pack(side="right", fill="y")
    txt.config(yscrollcommand=sb.set)

    nav = ttk.Frame(frm)
    nav.grid(row=2, column=0, pady=4)
    ttk.Button(nav, text="← Anterior").pack(side="left")
    ttk.Button(nav, text="Siguiente →").pack(side="left", padx=4)
    ttk.Button(nav, text="Ejecutar").pack(side="left", padx=10)

    frm.columnconfigure(0, weight=1)
    frm.rowconfigure(1, weight=1)
    return frm


def _crear_tabla(frm, n_var):
    for widget in frm.grid_slaves(row=3):
        widget.destroy()

    n = n_var.get()
    if n < 2 or n > 8:
        return

    tabla = ttk.LabelFrame(frm, text="Matriz aumentada [A | b]", padding=5)
    tabla.grid(row=3, column=0, sticky="ew", pady=4)

    celdas = []
    for i in range(n):
        fila = []
        for j in range(n + 1):
            entrada = ttk.Entry(tabla, width=7, justify="center")
            entrada.insert(0, "0")
            pad_x = (2, 10) if j == n - 1 else 2
            entrada.grid(row=i, column=j, padx=pad_x, pady=2)
            fila.append(entrada)
        celdas.append(fila)

    frm.celdas_matriz = celdas