import streamlit as st
import database as db

def show_extrato():
    st.header("📋 Extrato Detalhado")
    
    df = db.buscar_transacoes()
    
    if df.empty:
        st.info("Nenhuma transação encontrada.")
        return

    # Filtros simples
    col1, col2 = st.columns(2)
    with col1:
        filtro_tipo = st.multiselect("Filtrar por Tipo", ["Receita", "Despesa"], default=["Receita", "Despesa"])
    
    # Aplicar filtro
    if filtro_tipo:
        df = df[df["tipo"].isin(filtro_tipo)]
    
    # Exibir tabela interativa
    st.dataframe(
        df, 
        column_config={
            "valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
            "data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Opção de Exclusão (Simples para MVP)
    st.subheader("Gestão")
    with st.expander("🗑️ Excluir um lançamento"):
        id_to_delete = st.number_input("ID da transação para excluir", min_value=0, step=1)
        if st.button("Excluir Transação"):
            if id_to_delete > 0:
                db.excluir_transacao(id_to_delete)
                st.success(f"Transação {id_to_delete} excluída.")
                st.rerun() # Atualiza a página