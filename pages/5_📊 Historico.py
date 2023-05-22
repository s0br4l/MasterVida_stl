from datetime import datetime, date, time, timedelta
import plotly.express as px
import numpy as np
import streamlit as st
from PIL import Image
import pandas as pd
from numpy import datetime64

st.set_page_config(page_title="Histórico Registros", page_icon='images/resultados.ico', layout="centered",
                   initial_sidebar_state="auto", menu_items=None)

container1 = st.container()
container1.image(Image.open('images/large_master_image_historico.png'))

cadastros_historico = pd.read_excel('tables/cadastros.xlsx', index_col=0)
cadastros_dib_historico = cadastros_historico.loc[cadastros_historico['diabetes'] == 'DIB']
listanomes_geral_historico = cadastros_historico['nome'].unique().astype(str)
registros_historico = pd.read_excel('tables/reg_semanais.xlsx', index_col=0)

col1, col2 = st.columns([2.5, 1], gap='large')
nome_historico = col1.selectbox('Selecionar Nome', listanomes_geral_historico, key='nome select pre')
nomeselecionado_cad = cadastros_historico.loc[cadastros_historico['nome'] == nome_historico]
nomeselecionado_reg = registros_historico.loc[registros_historico['nome'] == nome_historico]
datas_selecionado = list(nomeselecionado_reg['data'].astype(str).values[:])
nome_id_historico = nomeselecionado_cad['nome_id'].values[0]
if nome_historico:
    foto_historico = f'foto_{nome_id_historico}'
    with Image.open(f'cad_images/{foto_historico}.png') as foto_select:
        if foto_select:
            col2.image(foto_select, width=100)


def sort_dates(dates):
    # Define a key function that converts a date string to a datetime object
    def date_key(date_string):
        return datetime.strptime(date_string, "%d/%m/%y")

    # Use the sorted function to sort the list of dates, using the date_key function as the key
    return sorted(dates, key=date_key)


datas_selecionado = sort_dates(datas_selecionado)
datamin_value = datetime.strptime(datas_selecionado[0], "%d/%m/%y").date()
datamax_value = datetime.strptime(datas_selecionado[-1], "%d/%m/%y").date()

intervalo_datas = col1.slider('Intervalo de datas', min_value=datamin_value, max_value=datamax_value,
                              value=[datamin_value, datamax_value], format='D/M/YY', step=timedelta(weeks=1))

intervalo_min = intervalo_datas[0].strftime("%d/%m/%y")
intervalo_max = intervalo_datas[-1].strftime("%d/%m/%y")

registros_selecionados = nomeselecionado_reg.loc[
    (nomeselecionado_reg['data'] <= intervalo_max)]

col1.dataframe(registros_selecionados, use_container_width=True)

colfig1, colfig2 = st.columns(2)
fig_pas = px.bar(registros_selecionados, x="data", y=["pre_pas1", "pos_pas1"], text="interv_dia", barmode="group",
                 title="PAS")
# fig_pas.update_layout(yaxis_range=[40, 160])
grafico_pas = colfig1.plotly_chart(fig_pas, theme="streamlit", use_container_width=True)

fig_pad = px.bar(registros_selecionados, x="data", y=["pre_pad1", "pos_pad1"], text="interv_dia", barmode="group",
                 title="PAD")
# fig_pad.update_layout(yaxis_range=[40, 90])
grafico_pad = colfig2.plotly_chart(fig_pad, theme="streamlit", use_container_width=True)
