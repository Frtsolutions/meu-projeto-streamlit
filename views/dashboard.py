import streamlit as st
import plotly.express as px
import database as db

def show_dashboard():
    st.header("📊 Visão Geral do Negócio")
    
    # Atualizar dados
    receitas, despesas, saldo = db.obter_resumo()
    
    # Cartões de Métricas (KPIs)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Entradas", f"R$ {receitas:,.2f}", delta="Receitas")
    
    with col2:
        st.metric("Saídas", f"R$ {despesas:,.2f}", delta="-Despesas", delta_color="inverse")
    
    with col3:
        st.metric("Saldo Atual", f"R$ {saldo:,.2f}", delta_color="normal")
        
    st.divider()
    
    # Gráficos
    df = db.buscar_transacoes()
    
    if not df.empty:
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            st.subheader("Receitas vs Despesas")
            # Agrupar por tipo
            df_tipo = df.groupby("tipo")["valor"].sum().reset_index()
            fig_pie = px.pie(df_tipo, values="valor", names="tipo", 
                             color="tipo",
                             color_discrete_map={"Receita": "green", "Despesa": "red"})
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_graf2:
            st.subheader("Despesas por Categoria")
            # Filtrar apenas despesas para ver onde o dinheiro vai
            df_despesas = df[df["tipo"] == "Despesa"]
            if not df_despesas.empty:
                df_cat = df_despesas.groupby("categoria")["valor"].sum().reset_index()
                fig_bar = px.bar(df_cat, x="categoria", y="valor", 
                                 text_auto='.2s', color="valor")
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("Ainda não há despesas registadas para gerar este gráfico.")
    else:
        st.warning("Registe a sua primeira movimentação para ver os gráficos!")