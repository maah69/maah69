import customtkinter as ctk
from tkinter import messagebox
from financa_model import finance_model
from datetime import datetime
from tkinter import Toplevel, ttk


ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("green") 

class FinancialApp(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        self.title("Gerenciador Financeiro Pessoal")
        self.geometry("850x650") 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

       
        self.current_year_month = ctk.StringVar(value=datetime.now().strftime("%Y-%m"))
        self.current_year_month.trace_add("write", self.update_all_views)

        
        self.tabview = ctk.CTkTabview(self, width=800)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        
        self.tabview.add("Dashboard")
        self.tabview.add("Extrato")
        self.tabview.add("+ Nova Transação")
        
        
        self._setup_dashboard(self.tabview.tab("Dashboard"))
        self._setup_extrato(self.tabview.tab("Extrato"))
        self._setup_nova_transacao(self.tabview.tab("+ Nova Transação"))
        
        
        self.update_all_views()
        
    def update_all_views(self, *args):
        """Chamada sempre que o mês muda ou uma transação é salva."""
        self._update_dashboard()
        self._update_extrato()

   
    
    def _setup_dashboard(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        
        
        mes_frame = ctk.CTkFrame(tab)
        mes_frame.grid(row=0, column=0, pady=10)
        
        ctk.CTkLabel(mes_frame, text="Mês/Ano (YYYY-MM):").pack(side="left", padx=10)
        self.mes_entry = ctk.CTkEntry(mes_frame, textvariable=self.current_year_month, width=100)
        self.mes_entry.pack(side="left", padx=10)
        
        
        self.saldo_total_var = ctk.StringVar(value="R$ 0.00")
        self.receitas_mes_var = ctk.StringVar(value="R$ 0.00")
        self.despesas_mes_var = ctk.StringVar(value="R$ 0.00")
        
        
        ctk.CTkLabel(tab, text="SALDO ATUAL TOTAL", font=ctk.CTkFont(size=14, weight="bold")).grid(row=1, column=0, pady=(15, 0))
        
       
        self.label_saldo_total = ctk.CTkLabel(tab, 
                                            textvariable=self.saldo_total_var, 
                                            font=ctk.CTkFont(size=30, weight="bold"), 
                                            text_color="blue") 
        self.label_saldo_total.grid(row=2, column=0, pady=5)
        
        
        resumo_frame = ctk.CTkFrame(tab)
        resumo_frame.grid(row=3, column=0, pady=30, padx=20, sticky="ew")
        resumo_frame.grid_columnconfigure((0, 1), weight=1)
        
       
        ctk.CTkLabel(resumo_frame, text="RECEITAS DO MÊS", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(resumo_frame, textvariable=self.receitas_mes_var, font=ctk.CTkFont(size=18, weight="bold"), text_color="green").grid(row=1, column=0, padx=10, pady=5)
        
       
        ctk.CTkLabel(resumo_frame, text="DESPESAS DO MÊS", font=ctk.CTkFont(size=12)).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(resumo_frame, textvariable=self.despesas_mes_var, font=ctk.CTkFont(size=18, weight="bold"), text_color="red").grid(row=1, column=1, padx=10, pady=5)

    def _update_dashboard(self):
        try:
           
            saldo_total = finance_model.calcular_saldo_total()
            saldo_formatado = f"R$ {saldo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.saldo_total_var.set(saldo_formatado)
            
            
            cor_saldo = 'green' if saldo_total >= 0 else 'red'
            self.label_saldo_total.configure(text_color=cor_saldo) 
            
           
            ano_mes = self.current_year_month.get()
            resumo = finance_model.calcular_resumo_mensal(ano_mes)
            
            receitas = resumo['receitas']
            despesas = resumo['despesas']
            
            self.receitas_mes_var.set(f"R$ {receitas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            self.despesas_mes_var.set(f"R$ {despesas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            
        except Exception as e:
            messagebox.showerror("Erro de Cálculo", f"Ocorreu um erro ao atualizar o dashboard: {e}")

    
    
    def _setup_nova_transacao(self, tab):
        
        tab.grid_columnconfigure(0, weight=1)
        form_frame = ctk.CTkFrame(tab, fg_color="transparent")
        form_frame.grid(row=0, column=0, padx=50, pady=20, sticky="ew")
        form_frame.grid_columnconfigure(1, weight=1)
        
        
        self.var_descricao = ctk.StringVar()
        self.var_valor = ctk.StringVar()
        self.var_tipo = ctk.StringVar(value='Despesa') 
        self.var_data = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.var_categoria_id = ctk.IntVar()
        
       
        
        
        ctk.CTkLabel(form_frame, text="Descrição:").grid(row=0, column=0, sticky='w', pady=10, padx=5)
        ctk.CTkEntry(form_frame, textvariable=self.var_descricao).grid(row=0, column=1, sticky='ew', padx=10)

        
        ctk.CTkLabel(form_frame, text="Valor (R$):").grid(row=1, column=0, sticky='w', pady=10, padx=5)
        ctk.CTkEntry(form_frame, textvariable=self.var_valor).grid(row=1, column=1, sticky='ew', padx=10)
        
        
        ctk.CTkLabel(form_frame, text="Tipo:").grid(row=2, column=0, sticky='w', pady=10, padx=5)
        
        radio_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        radio_frame.grid(row=2, column=1, sticky='w', padx=10)
        
        ctk.CTkRadioButton(radio_frame, text="Receita", variable=self.var_tipo, value='Receita', command=self._load_categorias_combobox).pack(side="left", padx=10)
        ctk.CTkRadioButton(radio_frame, text="Despesa", variable=self.var_tipo, value='Despesa', command=self._load_categorias_combobox).pack(side="left", padx=10)
        
        
        ctk.CTkLabel(form_frame, text="Data (YYYY-MM-DD):").grid(row=3, column=0, sticky='w', pady=10, padx=5)
        ctk.CTkEntry(form_frame, textvariable=self.var_data).grid(row=3, column=1, sticky='ew', padx=10)
        
        
        ctk.CTkLabel(form_frame, text="Categoria:").grid(row=4, column=0, sticky='w', pady=10, padx=5)
        self.categoria_combobox = ctk.CTkComboBox(form_frame, width=200, command=self._set_categoria_id)
        self.categoria_combobox.grid(row=4, column=1, sticky='w', padx=10)
        
        self._load_categorias_combobox() 
        
        ctk.CTkButton(form_frame, text="Salvar Transação", command=self._salvar_transacao,
                      fg_color="#A7AED3", hover_color="#DFE9F5", font=ctk.CTkFont(weight="bold")).grid(row=5, column=0, columnspan=2, pady=30)
        
    def _load_categorias_combobox(self, *args):
        """Carrega as categorias no combobox baseado no tipo (Receita/Despesa)."""
        tipo = self.var_tipo.get()
        categorias = finance_model.obter_categorias(tipo)
        
        self.categorias_map = {nome: id for id, nome, _ in categorias}
        nomes_categorias = list(self.categorias_map.keys())
        
        self.categoria_combobox.configure(values=nomes_categorias)
        
        if nomes_categorias:
            self.categoria_combobox.set(nomes_categorias[0])
            self.var_categoria_id.set(self.categorias_map[nomes_categorias[0]])
        else:
            self.categoria_combobox.set("Nenhuma Categoria")
            self.var_categoria_id.set(0)

    def _set_categoria_id(self, nome_selecionado):
        """Define o ID da categoria selecionada."""
        if nome_selecionado in self.categorias_map:
            self.var_categoria_id.set(self.categorias_map[nome_selecionado])
        else:
            self.var_categoria_id.set(0)

    def _salvar_transacao(self):
        try:
            descricao = self.var_descricao.get()
            valor = float(self.var_valor.get().replace(',', '.'))
            tipo = self.var_tipo.get()
            data = self.var_data.get()
            categoria_id = self.var_categoria_id.get()
            
            if not descricao or valor <= 0 or not data or categoria_id == 0:
                messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios e verifique o valor.")
                return

            finance_model.adicionar_transacao(descricao, valor, tipo, data, categoria_id)
            
            messagebox.showinfo("Sucesso", "Transação salva com sucesso!")
            
            
            self.var_descricao.set("")
            self.var_valor.set("")
            self.var_data.set(datetime.now().strftime("%Y-%m-%d"))
            self._load_categorias_combobox()
            
            self.update_all_views()
            self.tabview.set("Dashboard") 
            
        except ValueError as e:
            messagebox.showerror("Erro de Valor", f"Verifique a entrada de Valor (deve ser um número). Detalhe: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar a transação: {e}")
            
    
    
    def _setup_extrato(self, tab):
        
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        mes_frame = ctk.CTkFrame(tab)
        mes_frame.grid(row=0, column=0, pady=10)
        
        ctk.CTkLabel(mes_frame, text="Filtrar Mês/Ano (YYYY-MM):").pack(side="left", padx=10)
        ctk.CTkEntry(mes_frame, textvariable=self.current_year_month, width=100).pack(side="left", padx=10)
        
       
        self.extrato_tree = ttk.Treeview(tab, columns=('Descricao', 'Valor', 'Tipo', 'Data', 'Categoria'), show='headings')
        self.extrato_tree.heading('Descricao', text='Descrição')
        self.extrato_tree.heading('Valor', text='Valor')
        self.extrato_tree.heading('Tipo', text='Tipo')
        self.extrato_tree.heading('Data', text='Data')
        self.extrato_tree.heading('Categoria', text='Categoria')
        
        
        self.extrato_tree.tag_configure('receita', foreground='green')
        self.extrato_tree.tag_configure('despesa', foreground='red')

        self.extrato_tree.column('Descricao', width=200, anchor='w')
        self.extrato_tree.column('Valor', width=80, anchor='e')
        self.extrato_tree.column('Tipo', width=70, anchor='center')
        self.extrato_tree.column('Data', width=80, anchor='center')
        self.extrato_tree.column('Categoria', width=100, anchor='w')
        
        self.extrato_tree.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

    def _update_extrato(self):
        
        for item in self.extrato_tree.get_children():
            self.extrato_tree.delete(item)
            
        ano_mes = self.current_year_month.get()
        transacoes = finance_model.obter_extrato_mensal(ano_mes)
        
        for transacao in transacoes:
            valor = transacao[2]
            valor_formatado = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            
            tipo = transacao[3]
            tag_cor = 'receita' if tipo == 'Receita' else 'despesa'
            
            self.extrato_tree.insert('', 'end', 
                                     text=transacao[0],
                                     values=(transacao[1], valor_formatado, tipo, transacao[4], transacao[5]),
                                     tags=(tag_cor,))

if __name__ == "__main__":
    
    app = FinancialApp()
    app.mainloop()