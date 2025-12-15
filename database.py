import sqlite3
import pandas as pd
from datetime import datetime

# Caminho do banco de dados
DB_NAME = "caixa_zero.db"

def init_db():
    """Inicializa o banco de dados e cria a tabela se não existir."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Criar tabela de transações
    c.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            valor REAL NOT NULL,
            descricao TEXT
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_transacao(data, tipo, categoria, valor, descricao):
    """Adiciona uma nova receita ou despesa."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO transacoes (data, tipo, categoria, valor, descricao)
        VALUES (?, ?, ?, ?, ?)
    ''', (data, tipo, categoria, valor, descricao))
    conn.commit()
    conn.close()

def buscar_transacoes():
    """Retorna todas as transações num DataFrame do Pandas."""
    conn = sqlite3.connect(DB_NAME)
    # Ler SQL diretamente para DataFrame para facilitar análises
    df = pd.read_sql_query("SELECT * FROM transacoes ORDER BY data DESC", conn)
    conn.close()
    return df

def excluir_transacao(id_transacao):
    """Exclui uma transação pelo ID."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM transacoes WHERE id = ?", (id_transacao,))
    conn.commit()
    conn.close()

def obter_resumo():
    """Calcula totais para os cartões do dashboard."""
    df = buscar_transacoes()
    if df.empty:
        return 0.0, 0.0, 0.0
    
    receitas = df[df['tipo'] == 'Receita']['valor'].sum()
    despesas = df[df['tipo'] == 'Despesa']['valor'].sum()
    saldo = receitas - despesas
    
    return receitas, despesas, saldo