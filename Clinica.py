import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class ClinicaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Controle - Clínica Médica")
        self.geometry("900x600")
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
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0,12))

        right = ttk.Frame(container)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Cadastrão
        cad_frame = ttk.LabelFrame(left, text="Cadastros", padding=8)
        cad_frame.pack(fill=tk.Y)

        btn_medico = ttk.Button(cad_frame, text="Novo Médico", command=self.novo_medico)
        btn_medico.pack(fill=tk.X, pady=4)

        btn_paciente = ttk.Button(cad_frame, text="Novo Paciente", command=self.novo_paciente)
        btn_paciente.pack(fill=tk.X, pady=4)

        btn_listar = ttk.Button(cad_frame, text="Listar Pessoas", command=self.listar_pessoas)
        btn_listar.pack(fill=tk.X, pady=4)

        # Agendamentão
        ag_frame = ttk.LabelFrame(left, text="Agendamento", padding=8)
        ag_frame.pack(fill=tk.Y, pady=(12,0))

        ttk.Label(ag_frame, text="Médico:").pack(anchor=tk.W)
        self.combo_med = ttk.Combobox(ag_frame, state='readonly')
        self.combo_med.pack(fill=tk.X, pady=2)

        ttk.Label(ag_frame, text="Paciente:").pack(anchor=tk.W)
        self.combo_pac = ttk.Combobox(ag_frame, state='readonly')
        self.combo_pac.pack(fill=tk.X, pady=2)

        ttk.Label(ag_frame, text="Data (DD-MM-AAAA):").pack(anchor=tk.W)
        self.entry_data = ttk.Entry(ag_frame)
        self.entry_data.pack(fill=tk.X, pady=2)

        ttk.Label(ag_frame, text="Hora (HH:MM):").pack(anchor=tk.W)
        self.entry_hora = ttk.Entry(ag_frame)
        self.entry_hora.pack(fill=tk.X, pady=2)

        ttk.Label(ag_frame, text="Descrição:").pack(anchor=tk.W)
        self.entry_desc = ttk.Entry(ag_frame)
        self.entry_desc.pack(fill=tk.X, pady=2)

        btn_agendar = ttk.Button(ag_frame, text="Agendar Consulta", command=self.agendar_consulta)
        btn_agendar.pack(fill=tk.X, pady=(6,2))

        # Filtro 1330 de café
        action_frame = ttk.LabelFrame(left, text="Ações", padding=8)
        action_frame.pack(fill=tk.Y, pady=(12,0))

        ttk.Button(action_frame, text="Remover Consulta Selecionada", command=self.remover_consulta).pack(fill=tk.X, pady=4)
        ttk.Button(action_frame, text="Limpar Cadastros (apenas memória)", command=self.limpar_cadastros).pack(fill=tk.X, pady=4)

        # Lista de consultões
        top_label = ttk.Label(right, text="Consultas Agendadas", font=(None, 14))
        top_label.pack(anchor=tk.W)

        cols = ("medico", "paciente", "datahora", "descricao")
        self.tree = ttk.Treeview(right, columns=cols, show='headings', height=20)
        self.tree.heading('medico', text='Médico')
        self.tree.heading('paciente', text='Paciente')
        self.tree.heading('datahora', text='Data e Hora')
        self.tree.heading('descricao', text='Descrição')
        self.tree.column('medico', width=180)
        self.tree.column('paciente', width=180)
        self.tree.column('datahora', width=150)
        self.tree.column('descricao', width=300)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(6,0))

        # Barra de cereal status
        self.status = ttk.Label(self, text="Pronto", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X, side=tk.BOTTOM)
        self._atualizar_comboboxes()

    # Funções do Casdastrão
    def novo_medico(self):
        dlg = PessoaDialog(self, titulo="Cadastrar Médico", fields=[('Nome',''), ('Especialidade','')])
        if dlg.result:
            nome = dlg.result.get('Nome').strip()
            esp = dlg.result.get('Especialidade').strip()
            if not nome:
                messagebox.showwarning('Aviso', 'Nome obrigatório')
                return
            pid = self._next_person_id; self._next_person_id += 1
            self.medicos[pid] = {'nome': nome, 'especialidade': esp}
            if messagebox.askyesno('Registrar como paciente?', 'Deseja também cadastrar esse médico como paciente (útil se o médico fizer consultas)?'):
                self.pacientes[pid] = {'nome': nome, 'idade': ''}
            self._atualizar_comboboxes()
            self.status['text'] = f'Médico "{nome}" cadastrado.'

    def novo_paciente(self):
        dlg = PessoaDialog(self, titulo="Cadastrar Paciente", fields=[('Nome',''), ('Idade','')])
        if dlg.result:
            nome = dlg.result.get('Nome').strip()
            idade = dlg.result.get('Idade').strip()
            if not nome:
                messagebox.showwarning('Aviso', 'Nome obrigatório')
                return
            pid = self._next_person_id; self._next_person_id += 1
            self.pacientes[pid] = {'nome': nome, 'idade': idade}
            self._atualizar_comboboxes()
            self.status['text'] = f'Paciente "{nome}" cadastrado.'

    def listar_pessoas(self):
        texto = '--- Médicos ---\n'
        for mid, m in self.medicos.items():
            texto += f'{mid}: {m["nome"]} ({m.get("especialidade","")})\n'
        texto += '\n--- Pacientes ---\n'
        for pid, p in self.pacientes.items():
            texto += f'{pid}: {p["nome"]} (idade: {p.get("idade","-")})\n'
        messagebox.showinfo('Pessoas cadastradas', texto)

    def limpar_cadastros(self):
        if messagebox.askyesno('Confirma', 'Remover todos os cadastros e consultas da memória?'):
            self.medicos.clear(); self.pacientes.clear(); self.consultas.clear(); self._next_person_id = 1
            self._atualizar_comboboxes(); self._atualizar_tree()
            self.status['text'] = 'Dados limpos.'

    # Agendamentão
    def agendar_consulta(self):
        med_sel = self.combo_med.get()
        pac_sel = self.combo_pac.get()
        data_text = self.entry_data.get().strip()
        hora_text = self.entry_hora.get().strip()
        desc = self.entry_desc.get().strip()

        if not med_sel or not pac_sel or not data_text or not hora_text:
            messagebox.showwarning('Dados insuficientes', 'Preencha médico, paciente, data e hora')
            return

        try:
            dt = datetime.strptime(data_text + ' ' + hora_text, '%d-%m-%Y %H:%M')
        except Exception:
            messagebox.showerror('Formato inválido', 'Use data no formato DD-MM-AAAA e hora HH:MM')
            return

        id_med = int(med_sel.split(' - ',1)[0])
        id_pac = int(pac_sel.split(' - ',1)[0])

        consulta = {'id_medico': id_med, 'id_paciente': id_pac, 'datahora': dt, 'descricao': desc}
        self.consultas.append(consulta)
        self._atualizar_tree()
        self.status['text'] = f'Consulta agendada: {dt.strftime("%d-%m-%Y %H:%M")}.'

    def _atualizar_comboboxes(self):
        med_items = [f"{mid} - {m['nome']} ({m.get('especialidade','')})" for mid,m in self.medicos.items()]
        pac_items = [f"{pid} - {p['nome']}" for pid,p in self.pacientes.items()]
        self.combo_med['values'] = med_items
        self.combo_pac['values'] = pac_items

    def _atualizar_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        consultas_sorted = sorted(self.consultas, key=lambda c: c['datahora'])
        for idx,c in enumerate(consultas_sorted):
            m = self.medicos.get(c['id_medico'], {'nome':'<desconhecido>'})
            p = self.pacientes.get(c['id_paciente'], {'nome':'<desconhecido>'})
            dt = c['datahora'].strftime('%d-%m-%Y %H:%M')
            desc = c.get('descricao','')
            self.tree.insert('', tk.END, iid=str(idx), values=(m['nome'], p['nome'], dt, desc))

    def remover_consulta(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo('Info', 'Selecione uma consulta na lista para remover')
            return
        idx = int(sel[0])
        consultas_sorted = sorted(self.consultas, key=lambda c: c['datahora'])
        item = consultas_sorted[idx]
        if messagebox.askyesno('Confirmar', f'Remover a consulta de {item["datahora"].strftime("%d-%m-%Y %H:%M")}?'):
            for i,c in enumerate(self.consultas):
                if c is item:
                    del self.consultas[i]
                    break
            self._atualizar_tree()
            self.status['text'] = 'Consulta removida.'


class PessoaDialog(simpledialog.Dialog):
    def __init__(self, parent, titulo='Dialog', fields=None):
        self.fields = fields or []
        self.result = None
        super().__init__(parent, titulo)

    def body(self, master):
        self.entries = {}
        for idx, (label, default) in enumerate(self.fields):
            ttk.Label(master, text=label+':').grid(row=idx, column=0, sticky=tk.W, pady=4)
            ent = ttk.Entry(master)
            ent.grid(row=idx, column=1, sticky=tk.EW, pady=4)
            ent.insert(0, default)
            self.entries[label] = ent
        return list(self.entries.values())[0]

    def apply(self):
        self.result = {label: ent.get() for label, ent in self.entries.items()}


if __name__ == '__main__':
    app = ClinicaApp()
    app.mainloop()