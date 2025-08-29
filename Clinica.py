import tkinter as tk
from tkinter import ttk , messagebox, simpledialog
from datetime import datetime

class ClinicaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Controle - Clinica")
        self.geometry("800x600")
        self.resizable(False, False)

        # Alzheimer
        self.medicos = {}
        self.pacientes = {}
        self.consultas = []
        self._next_person_id = 1

        self._create_widgets()

    def _create_widgets(self):
        container = ttk.Frame(self, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(container)
        left.pack(side=tk.LEFT, fill=tk.Y,  padx=(0,12))

        right = ttk.Frame(container)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Cadastro Loko
        cad_frame = ttk.LabelFrame(left, text="Cadastros", padding=8)
        cad_frame.pack(fill=tk.Y)

        btn_medico = ttk.Button(cad_frame, text="Cadastrar novo Médico", command=self.novo.medico)
