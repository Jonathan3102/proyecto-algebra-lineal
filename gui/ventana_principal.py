import tkinter as tk
from tkinter import ttk
from .eliminacion_gaussiana import crearEliminacionGaussiana 
from .seidel_cronometro import crearSeidelCronometro


class VentanaPrincipal:
    def __init__(self, master):
        self.master = master
        self._crear_selector()
        self._frames = {}
        self._cargar_frames()

    def _crear_selector(self):
        frm = ttk.Frame(self.master, padding=5)
        frm.pack(fill="x")
        self.opcion = tk.IntVar(value=1)

        ttk.Radiobutton(
            frm,
            text="Eliminacio Gaussiana (paso a paso)",
            variable=self.opcion,
            value=1,
            command=self._mostrar,
        ).pack(side="left")

        ttk.Radiobutton(
            frm,
            text="Seidel Cronometro (tiempos)",
            variable=self.opcion,
            value=2,
            command=self._mostrar,
        ).pack(side="left", padx=10)

    def _cargar_frames(self):
        container = ttk.Frame(self.master, padding=5)
        container.pack(fill="both", expand=True)

        self._frames[1] = crearEliminacionGaussiana(container)
        self._frames[2] = crearSeidelCronometro(container)

        for frame in self._frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        self._mostrar()

    def _mostrar(self):
        sel = self.opcion.get()
        for clave, frame in self._frames.items():
            if clave == sel:
                frame.grid()
            else:
                frame.grid_remove()