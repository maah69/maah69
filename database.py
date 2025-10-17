import sqlite3

DATABASE_NAME = "financas_pessoais.db"

class DatabaseManager:
    """Gerencia a conexão e operações no banco de dados SQLite."""
    
    def __init__(self):
        # Conecta ao DB. Se o arquivo não existir, ele é criado.
        self.conn = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.conn.cursor()
        self._criar_tabelas()

    def _criar_tabelas(self):
        # 1. Tabela de Categorias
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                tipo TEXT CHECK(tipo IN ('Receita', 'Despesa')) NOT NULL
            );
        """)
        
        # 2. Tabela de Transações
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                tipo TEXT CHECK(tipo IN ('Receita', 'Despesa')) NOT NULL,
                data TEXT NOT NULL,
                categoria_id INTEGER,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            );
        """)
        self.conn.commit()
        self._popular_categorias_iniciais()

    def _popular_categorias_iniciais(self):
        """Insere algumas categorias padrão se o banco estiver vazio."""
        categorias_iniciais = [
            ('Salário', 'Receita'), ('Investimento', 'Receita'),
            ('Alimentação', 'Despesa'), ('Transporte', 'Despesa'),
            ('Moradia', 'Despesa'), ('Lazer', 'Despesa')
        ]
        
        for nome, tipo in categorias_iniciais:
            # Garante que a categoria só seja inserida se não existir (IntegrityError)
            try:
                self.cursor.execute(
                    "INSERT INTO categorias (nome, tipo) VALUES (?, ?)", 
                    (nome, tipo)
                )
            except sqlite3.IntegrityError:
                pass
        self.conn.commit()


    # --- CRUD de Transações ---
    
    def inserir_transacao(self, descricao, valor, tipo, data, categoria_id):
        self.cursor.execute(
            "INSERT INTO transacoes (descricao, valor, tipo, data, categoria_id) VALUES (?, ?, ?, ?, ?)",
            (descricao, valor, tipo, data, categoria_id)
        )
        self.conn.commit()

    def listar_transacoes_por_mes(self, ano_mes: str):
        """Lista transações em um formato 'YYYY-MM'."""
        self.cursor.execute("""
            SELECT t.id, t.descricao, t.valor, t.tipo, t.data, c.nome, c.id
            FROM transacoes t
            LEFT JOIN categorias c ON t.categoria_id = c.id
            WHERE strftime('%Y-%m', t.data) = ?
            ORDER BY t.data DESC
        """, (ano_mes,))
        return self.cursor.fetchall()
        
    def deletar_transacao(self, id):
        # Adiciona a função de deletar para cumprir o C(R)U(D)
        self.cursor.execute("DELETE FROM transacoes WHERE id=?", (id,))
        self.conn.commit()
        
    # --- CRUD de Categorias (Read e Create) ---

    def listar_categorias(self, tipo=None):
        if tipo:
            self.cursor.execute("SELECT id, nome, tipo FROM categorias WHERE tipo=?", (tipo,))
        else:
            self.cursor.execute("SELECT id, nome, tipo FROM categorias ORDER BY nome")
        return self.cursor.fetchall()
        
    def close(self):
        self.conn.close()

# Inicializa o DB ao ser importado
db_manager = DatabaseManager()