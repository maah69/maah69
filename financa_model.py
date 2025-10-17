from database import db_manager
from datetime import datetime

class FinanceModel:
    """Contém a lógica de negócios e cálculos financeiros."""
    
    def __init__(self):
        self.db = db_manager

    # --- Funções de Transações ---
    
    def adicionar_transacao(self, descricao, valor, tipo, data, categoria_id):
        # Validação básica de entrada
        if not descricao or valor <= 0 or tipo not in ['Receita', 'Despesa']:
            raise ValueError("Dados de transação inválidos.")
            
        # Formata a data para padrão SQLite (YYYY-MM-DD)
        if isinstance(data, datetime):
            data_str = data.strftime('%Y-%m-%d')
        else:
            data_str = data # Assume que já está no formato correto se for string

        self.db.inserir_transacao(descricao, float(valor), tipo, data_str, categoria_id)

    def obter_extrato_mensal(self, ano_mes: str):
        # ano_mes deve ser 'YYYY-MM'
        return self.db.listar_transacoes_por_mes(ano_mes)

    def obter_categorias(self, tipo=None):
        return self.db.listar_categorias(tipo)
        
    # --- Funções de Cálculo (Dashboard) ---
    
    def calcular_resumo_mensal(self, ano_mes: str):
        """Calcula receitas, despesas e saldo para um dado mês."""
        transacoes = self.db.listar_transacoes_por_mes(ano_mes)
        
        total_receitas = 0.0
        total_despesas = 0.0
        
        for transacao in transacoes:
            # Estrutura do resultado: (id, descricao, valor, tipo, data, categoria_nome, categoria_id)
            valor = transacao[2]
            tipo = transacao[3]
            
            if tipo == 'Receita':
                total_receitas += valor
            elif tipo == 'Despesa':
                total_despesas += valor
                
        saldo_mensal = total_receitas - total_despesas
        
        return {
            'receitas': total_receitas,
            'despesas': total_despesas,
            'saldo_mensal': saldo_mensal
        }

    def calcular_saldo_total(self):
        """Calcula o saldo acumulado de todas as transações."""
        self.db.cursor.execute("SELECT SUM(CASE WHEN tipo='Receita' THEN valor ELSE 0 END) FROM transacoes")
        total_receitas = self.db.cursor.fetchone()[0] or 0.0
        
        self.db.cursor.execute("SELECT SUM(CASE WHEN tipo='Despesa' THEN valor ELSE 0 END) FROM transacoes")
        total_despesas = self.db.cursor.fetchone()[0] or 0.0
        
        return total_receitas - total_despesas

# Instancia o modelo para ser usado na GUI
finance_model = FinanceModel()