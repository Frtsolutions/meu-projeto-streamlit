import streamlit as st
import database as db
import os
import time

# Importar as visualizações (views)
from views import dashboard, lancamentos, extrato

# Configuração da Página (Deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Caixa Zero - Gestão Simples",
    page_icon="💰",
    layout="wide"
)

# --- Função de Segurança ---
def check_password():
    """Retorna True se o utilizador inserir a senha correta."""
    
    # Inicializa o estado da senha se não existir
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    # Se a senha já foi verificada, retorna True e segue o baile
    if st.session_state.password_correct:
        return True

    # Se não, mostra o formulário de login
    st.title("🔒 Acesso Restrito")
    senha_input = st.text_input("Digite a senha de acesso", type="password")
    
    # Busca a senha nas variáveis de ambiente (Render) ou segredos locais
    try:
        senha_correta = st.secrets["APP_PASSWORD"]
    except (FileNotFoundError, KeyError):
        senha_correta = os.getenv("APP_PASSWORD")

    if st.button("Entrar"):
        if senha_input == senha_correta:
            st.session_state.password_correct = True
            st.success("Login efetuado! Carregando sistema...")
            time.sleep(1) # Espera 1 segundinho para ler a mensagem
            st.rerun()    # Recarrega a página para mostrar o conteúdo
        else:
            st.error("Senha incorreta.")
    
    return False

# --- Bloqueio da Aplicação ---
# Se a senha não estiver correta, o script para aqui (st.stop) e não mostra o resto
if not check_password():
    st.stop()

# =========================================================
# DAKI PARA BAIXO, TUDO IGUAL (SÓ CARREGA SE LOGADO)
# =========================================================

# Inicializar Banco de Dados
db.init_db()

# CSS Customizado
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    div.stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Navegação Lateral
st.sidebar.title("💰 Caixa Zero")
st.sidebar.markdown("---")
menu_selection = st.sidebar.radio(
    "Navegação",
    ["Dashboard", "Novo Lançamento", "Extrato"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Versão MVP 1.1 - Seguro")

# Lógica de Roteamento (Router)
if menu_selection == "Dashboard":
    dashboard.show_dashboard()
elif menu_selection == "Novo Lançamento":
    lancamentos.show_lancamentos()
elif menu_selection == "Extrato":
    extrato.show_extrato()