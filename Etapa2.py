from tkinter import N
from unicodedata import name
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

#---IMPORT DATA---#
df=pd.read_csv("airbnb_limpio.csv", nrows=2000)

DATA_URL = ('airbnb_limpio.csv')

#--- PAGE CONFIG ---#
st.set_page_config(page_title="AIRBNB ANÁLISIS",
                   page_icon=":busts_in_silhouette:")

st.title("AIRBNB ANÁLISIS")
st.markdown("En este tablero se puede observar información crucial acerca de factores importantes para AIRBNB.")

#--- LOGO ---#
st.sidebar.image("AIRBNB.png")
st.sidebar.markdown("##")

#--- SIDEBAR FILTERS ---#
select_delegacion = st.sidebar.selectbox("Selecciona la delegación", df['neighbourhood'].unique())
st.write(f"Selected Option: {select_delegacion!r}")
st.write(df.query(f"""neighbourhood==@select_delegacion"""))
st.markdown("_")

select_roomtype = st.sidebar.selectbox("Selecciona el tipo de habitación", df['room_type'].unique())
st.write(f"Selected Option: {select_roomtype!r}")
st.write(df.query(f"""room_type==@select_roomtype"""))
st.markdown("_")

optionals = st.sidebar.expander("Optional Configurations", True)
price_min = optionals.slider(
    "Minimum Price",
    min_value=float(df['price'].min()),
    max_value=float(df['price'].max())
)
price_max = optionals.slider(
    "Maximum Price",
    min_value=float(df['price'].min()),
    max_value=float(df['price'].max())
)

subset_price = df[ (df['price'] >= price_min) & (df['price'] <= price_max)]
st.write(f"Number of Records With Price Between {price_min} and {price_max}: {subset_price.shape[0]}")

# Display of the dataset whith the max fare selected
st.write(subset_price)
st.markdown("_")

#--- CHARTS ---#
@st.cache
def load_data(nrows):
    df = pd.read_csv("airbnb_limpio.csv", nrows=nrows)
    lowercase = lambda x: str(x).lower()
    return df

agree= st.checkbox("Histograma de Distribución de los Precios ")
if agree:
    fig, ax = plt.subplots()
    ax.hist(df.price)
    st.header("Histograma Precios")
    st.pyplot(fig)
    st.markdown("_")

average_price_habitacion=(
    df.groupby(by=['room_type'])[['price']].sum().sort_values(by="room_type"))

fig_price_habitacion=px.bar(average_price_habitacion,
                        x=average_price_habitacion.index,
                        y="price", 
                        orientation="v",
                        title="Precio promedio por habitación",
                        labels=dict(room_type="Tipo de habitación", price="Precio"),
                        color_discrete_sequence=["#7ECBB4"],
                        template="plotly_white")
fig_price_habitacion.update_layout(plot_bgcolor="rgba(0,0,0,0)")

st.plotly_chart(fig_price_habitacion)

average_price_delegacion=(
    df.groupby(by=['neighbourhood'])[['price']].sum().sort_values(by="neighbourhood"))

fig_price_delegacion=px.bar(average_price_delegacion,
                        x=average_price_delegacion.index,
                        y="price", 
                        orientation="v",
                        title="Delegación por precio promedio",
                        labels=dict(neighbourhood="Delegación", price="Precio"),
                        color_discrete_sequence=["#7ECBB4"],
                        template="plotly_white")
fig_price_delegacion.update_layout(plot_bgcolor="rgba(0,0,0,0)")

st.plotly_chart(fig_price_delegacion)

agree9= st.sidebar.selectbox ("Selecciona delegación", df['neighbourhood'].unique())
if st.sidebar.button ("Filtro por delegación") :
    subset_delegación=df[(df["neighbourhood"]==agree9)]
    st.write(f"Opción seleccionada: {agree9!r}")
    st.write(df.query(f"""neighbourhood==@agree9"""))
    st.map(subset_delegación)
    st.markdown("_")

#--- CONCLUSION ---#
st.markdown("**Analysis**")
st.markdown("Esta pagina web se creo para trabajar con la base de datos de Airbnb en la Ciudad de México, su principal objetivo es conocer todas las locaciones disponibles dentro de la ciudad y filtrar estas locaciones mediante precio y otras variables importantes, todo esto para conocer si para Carina es una buena opción el poner en renta su habitación disponible.")
