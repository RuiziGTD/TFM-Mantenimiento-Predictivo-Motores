import streamlit as st

st.set_page_config(
    page_title="Dashboard de Mantenimiento Predictivo",
    layout="wide"
)

st.title('Panel de Control de Salud de Motores ✈️')

st.header("Estado General de la Flota")
st.write("Aquí irá un resumen de los motores con RUL más bajo.")
st.empty() # Marcador de posición para un gráfico

st.header("Análisis de un Motor Específico")
unit_id = st.number_input(
    "Seleccionar ID del motor:", 
    min_value=1, 
    max_value=100, 
    value=1
)
st.write(f"Mostrando análisis para el motor {unit_id}")
st.empty() # Marcador de posición para los gráficos de ese motor