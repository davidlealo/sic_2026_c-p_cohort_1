import streamlit as st

st.set_page_config(
    page_title="Simulador Biobío – Grupo 5",
    page_icon="🚨",
    layout="wide"
)

pg = st.navigation([
    st.Page("app.py", title="simulador", icon="🚨"),
    st.Page("contexto.py",  title="contexto",  icon="📖"),
])

pg.run()
