import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os

# --- Configuração da Conexão ---
# Tenta pegar dos segredos do Streamlit (Local) ou Variáveis de Ambiente (Render)
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except (FileNotFoundError, KeyError):
    # Fallback para tentar ler de variáveis de ambiente do sistema operacional (caso o st.secrets falhe no Render)
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Erro: Credenciais do Supabase não encontradas. Configure as Variáveis de Ambiente ou secrets.toml.")
    st.stop()

# Inicializa o cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def init_db():
    """
    Com Supabase, a tabela já deve ter sido criada via SQL Editor.
    Esta função serve apenas para verificar a conexão.
    """
    try:
        # Faz uma consulta leve apenas para testar a conexão
        supabase.table("transacoes").select("id", count="exact").limit(1).execute()
    except Exception as e:
        st.error(f"Erro ao conectar com o banco de dados: {e}")

def adicionar_transacao(data, tipo, categoria, descricao, valor):
    """
    Adiciona uma nova transação ao Supabase.
    """
    try:
        # Prepara os dados. Converta data para string ISO se necessário.
        nova_transacao = {
            "data": str(data),
            "tipo": tipo,
            "categoria": categoria,
            "descricao": descricao,
            "valor": float(valor)
        }
        
        response = supabase.table("transacoes").insert(nova_transacao).execute()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar no banco: {e}")
        return False

def buscar_transacoes():
    """
    Busca todas as transações e retorna um DataFrame do Pandas.
    """
    try:
        response = supabase.table("transacoes").select("*").execute()
        dados = response.data
        
        if not dados:
            return pd.DataFrame(columns=["id", "data", "tipo", "categoria", "descricao", "valor", "created_at"])
            
        df = pd.DataFrame(dados)
        # Garantir que a coluna de data seja datetime para facilitar manipulação
        df['data'] = pd.to_datetime(df['data'])
        return df
    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
        return pd.DataFrame()

def deletar_transacao(id_transacao):
    """
    Deleta uma transação pelo ID.
    """
    try:
        supabase.table("transacoes").delete().eq("id", id_transacao).execute()
        return True
    except Exception as e:
        st.error(f"Erro ao deletar: {e}")
        return False