import streamlit as st

### PAGES ###
dashboard = st.Page(
    "dash.py", title="Админка", icon="📈"
)
Conf = st.Page("conf.py", title="Настройки", icon="🔧")

pg = st.navigation([dashboard, Conf])
pg.run()