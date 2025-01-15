import streamlit as st
import ccxt
import pandas as pd
import time
import plotly.graph_objects as go
from datetime import datetime

# Настройки Bybit
exchange = ccxt.bybit({
    'apiKey': 'YOUR_BYBIT_API_KEY',  # Замените на свой ключ API
    'secret': 'YOUR_BYBIT_SECRET',  # Замените на свой секретный ключ
})

# Доступные таймфреймы
timeframes = {
    '1m': '1m', '5m': '5m', '15m': '15m', '30m': '30m', '1h': '1h',
    '4h': '4h', '1d': '1d', '1w': '1w', '1M': '1M'
}

# Настройки стилей
st.set_page_config(
    page_title="Админка",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
        .main {
            background-color: #f0f2f6;
            padding: 20px;
        }
        .st-emotion-cache-1v0mbdr{
          background-color: #fff !important;
        }
        .st-emotion-cache-16txtl3{
            display: flex;
            gap: 20px;
        }
        .st-emotion-cache-6q9t1s{
            display: flex;
            gap: 20px;
        }
        .st-emotion-cache-1b5596y{
            padding: 20px;
            border-radius: 10px;
            background-color: #fff;
        }
        .st-emotion-cache-10ohe9t{
              background-color: #fff !important;
              border: 1px solid #e0e0e0;
        }
         .st-emotion-cache-8y9k0d{
             margin: auto !important;
         }
    </style>
    """,
    unsafe_allow_html=True,
)

# Основная панель
with st.container():
  col1, col2 = st.columns([1, 2])
  with col1:
    st.header("Админка")

    # Выбор таймфрейма
    selected_timeframe = st.selectbox("Выберите таймфрейм:", list(timeframes.keys()))

    # Кнопка запроса данных
    if st.button("Запросить данные", key="fetch_data_button"):
        try:
            # Запрос данных с Bybit
            with st.spinner("Загрузка данных..."):
               ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe=timeframes[selected_timeframe], limit=100)

            # Преобразование в DataFrame
            df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
            df.set_index('Timestamp', inplace=True)
            
            st.success("Данные успешно загружены.")
            st.session_state['data_df'] = df
        except ccxt.ExchangeError as e:
           st.error(f"Ошибка при запросе данных: {e}")
        except Exception as e:
           st.error(f"Произошла неизвестная ошибка: {e}")
    # Кнопка очистки данных
    if st.button("Очистить данные", key="clear_data_button"):
       st.session_state.pop('data_df', None)
       st.success("Данные успешно очищены.")

    # Кнопка запуска трейлинга (placeholder)
    if st.button("Запустить трейлинг", key="start_trailing_button"):
         st.warning("Функция трейлинга еще не реализована.")

  with col2:
    # Отображение данных и графика
    if 'data_df' in st.session_state:
      df = st.session_state['data_df']

      # График
      st.subheader("График цены BTC/USDT")
      fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])
      st.plotly_chart(fig, use_container_width=True)
      # Таблица
      st.subheader("Таблица данных")
      st.dataframe(df.style.background_gradient(cmap='Blues'))
    else:
      st.info("Нет данных для отображения. Нажмите 'Запросить данные'.")
