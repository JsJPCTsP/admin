import streamlit as st

left, middle, right = st.columns(3)

with left:
        with st.container():
            button1 = st.button("Запросить сделки")
        with st.container():
            button2 = st.button("Очистить")
        

with middle:
    timeframe = ["1м", "5м", "15м", "1ч"]
    selection = st.segmented_control(
        "Time Frame", timeframe, selection_mode="single"
    )
    if selection == None:
         st.write("Выберите Time Frame")
    else:
        st.markdown(f"Выбран Time Frame: {selection}.")

with right: 
    on = st.toggle("Запустить ТРЕЛЛИНГ")

    if on:
         st.write("ТРЕЛЛИНГ ЗАПУЩЕН!")
