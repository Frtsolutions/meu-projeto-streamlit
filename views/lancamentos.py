import streamlit as st
import database as db
from datetime import date

def show_lancamentos():
    st.header("📝 Novo Lançamento")
    
    with st.form("form_transacao", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            data_mov = st.date_input("Data", date.today())
            tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
        
        with col2:
            valor = st.number_input("Valor (R$)", min_value=0.01, format="%.2f")
            
            # Categorias dinâmicas baseadas no tipo
            if tipo == "Receita":
                categorias = ["Vendas", "Serviços", "Investimentos", "Outros"]
            else:
                categorias = ["Fornecedores", "Aluguel/Fixo", "Marketing", "Pessoal", "Impostos", "Outros"]
                
            categoria = st.selectbox("Categoria", categorias)
            
        descricao = st.text_input("Descrição (Opcional)", placeholder="Ex: Venda para o Sr. João")
        
        submitted = st.form_submit_button("💾 Salvar Lançamento")
        
        if submitted:
            # Correção: A ordem dos argumentos deve bater com a função no database.py
            # Ordem correta: data, tipo, categoria, descricao, valor
            sucesso = db.adicionar_transacao(data_mov, tipo, categoria, descricao, valor)
            
            if sucesso:
                st.success("Lançamento registrado com sucesso!")
            else:
                st.error("Houve um erro ao tentar salvar no banco de dados.")