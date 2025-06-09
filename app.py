import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

usuarios = {
    "superSD009": "1234",
    "admin": "admin123"
}

st.set_page_config(page_title="Dashboard Interativo", layout='wide')

def login():
    st.title("🔐 Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Palavra-Passe", type="password")

    if st.button("Entrar"):
        if usuario in usuarios and usuarios[usuario] == senha:
            st.success(f"Bem-vindo, {usuario}!")
            st.session_state['logado'] = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")


# ======================================================================

def view_dashboard():
    #Configuração da página
    #st.set_page_config(page_title="Dashboard Interativo", layout='wide')

    st.sidebar.title("⚙️ Filtros")
    arquivo = st.file_uploader("📁 Envie um arquivo csv", type=["csv"])
    st.title("📊 Análise de Dados com layout interativo")

    if arquivo is not None:
        df = pd.read_csv(arquivo)

        if 'Categoria' in df.columns:
            categorias = df['Categoria'].unique()
            categoria_escolhida = st.sidebar.selectbox("📂 Selecione uma categoria", categorias)
            df_filtrado = df[df['Categoria'] == categoria_escolhida]
        else:
            st.warning("📂 'Categoria' não encontrada")
            df_filtrado = df

        with st.expander("🗂 Visualizar dados brutos"):
            st.dataframe(df_filtrado)

        if 'Valor' in df_filtrado.columns:
            total = df_filtrado['Valor'].sum()
            media = df_filtrado['Valor'].mean()

            col1, col2 = st.columns(2)
            col1.metric("💰 Total Vendido", f"{total:,.2f} KZ")
            col2.metric("📊 Média por Venda", f"{media:,.2f} KZ")

            fig, ax = plt.subplots()
            df_filtrado.groupby('Produto')['Valor'].sum().plot(kind="bar", ax=ax)
            ax.set_ylabel("Valor (KZ)")
            ax.set_title("💹 Vendas por produto")
            st.pyplot(fig)
        else:
            st.warning("Coluna 'Valor' não encontrada.")

        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar dados filtrados", data=csv, file_name="dados_filtrados.csv", mime='text/csv')

    else:
        st.info("Por favor, envie um arquivo csv para iniciar")


#======================================================================

if not st.session_state.get("logado"):
    login()
else:
    view_dashboard()
