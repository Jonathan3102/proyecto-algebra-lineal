import tkinter as tk
from gui.ventana_principal import VentanaPrincipal

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Eliminación Gaussiana – Gauss-Seidel")
    VentanaPrincipal(root)
    root.mainloop()