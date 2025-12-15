import streamlit as st
import database as db

# Importar as visualizações (views)
# O erro anterior acontecia aqui porque o arquivo extrato.py não tinha a função certa
from views import dashboard, lancamentos, extrato

# Configuração da Página (Deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Caixa Zero - Gestão Simples",
    page_icon="💰",
    layout="wide"
)

# Inicializar Banco de Dados
db.init_db()

# CSS Customizado para dar uma aparência mais profissional (clean)
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
st.sidebar.caption("Versão MVP 1.0")

# Lógica de Roteamento (Router)
if menu_selection == "Dashboard":
    dashboard.show_dashboard()
elif menu_selection == "Novo Lançamento":
    lancamentos.show_lancamentos()
elif menu_selection == "Extrato":
    # O Python vai buscar a função show_extrato dentro do arquivo views/extrato.py
    extrato.show_extrato()