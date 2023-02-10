import datetime
import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Registros Pressão Arterial", page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)

container1 = st.container()
container1.image(Image.open('images/large_master_image_pressao.png'))

cadastros = pd.read_excel('tables/cadastros.xlsx', index_col=0)
listanomes_geral = cadastros['nome'].unique().astype(str)
registros = pd.read_excel('tables/reg_semanais.xlsx', index_col=0)
datahoje = str(datetime.date.today())


tabpre, tabpos = st.tabs(['Pré-intervenção', 'Pós-intervenção'])
container2 = tabpre.container()
dataselecionada = tabpre.date_input('Filtrar por data')
container2.dataframe(registros.loc[registros['data'] == str(dataselecionada)][['data', 'nome',
                                                                'pre_pas1', 'pre_pad1', 'pre_pas2',
                                                                'pre_pad2', 'pre_pas3', 'pre_pad3']])


container3 = tabpre.container()
registrospre = container3.expander('Registrar Pré')
addpre = registrospre.container()
data_add = addpre.date_input('Data da intervenção', min_value=datetime.date.today())
nome_pre = addpre.selectbox('Selecionar Nome', listanomes_geral)
nomeselecionado = registros.loc[registros['nome'] == nome_pre]
valoresselecionados = nomeselecionado[['data', 'pre_pas1', 'pre_pad1', 'pre_pas2', 'pre_pad2', 'pre_pas3', 'pre_pad3']]
valorespordata = valoresselecionados.loc[valoresselecionados['data'] == str(data_add)].fillna(0)
if valorespordata.empty:
    valorprepas1 = 0
    valorprepad1 = 0
    valorprepas2 = 0
    valorprepad2 = 0
    valorprepas3 = 0
    valorprepad3 = 0
else:
    valorprepas1 = valorespordata['pre_pas1'].values[0]
    valorprepad1 = valorespordata['pre_pad1'].values[0]
    valorprepas2 = valorespordata['pre_pas2'].values[0]
    valorprepad2 = valorespordata['pre_pad2'].values[0]
    valorprepas3 = valorespordata['pre_pas3'].values[0]
    valorprepad3 = valorespordata['pre_pad3'].values[0]


colpas, colpad = addpre.columns(2)
prepas1 = colpas.number_input('PAS 1', min_value=0, value=int(valorprepas1))
prepad1 = colpad.number_input('PAD 1', min_value=0, value=int(valorprepad1))
prepas2 = colpas.number_input('PAS 2', min_value=0, value=int(valorprepas2))
prepad2 = colpad.number_input('PAD 2', min_value=0, value=int(valorprepad2))
prepas3 = colpas.number_input('PAS 3', min_value=0, value=int(valorprepas3))
prepad3 = colpad.number_input('PAD 3', min_value=0, value=int(valorprepad3))

if registros.loc[(registros['nome'] == nome_pre) & (registros['data'] == str(data_add))].empty:
    registronovo = pd.Series({'nome': nome_pre, 'data': data_add, 'pre_pas1': prepas1, 'pre_pad1': prepad1,
                              'pre_pas2': prepas2, 'pre_pad2': prepad2, 'pre_pas3': prepas3, 'pre_pad3': prepad3,
                              'pos_pas1': 0, 'pos_pad1': 0, 'pos_pas2': 0, 'pos_pad2': 0, 'pos_pas3': 0,
                              'pos_pad3': 0, 'pre_glic1': 0, 'pre_glic2': 0, 'pre_glic3': 0, 'pos_glic1': 0,
                              'pos_glic2': 0, 'pos_glic3': 0})
    registros = pd.concat([registros, registronovo.to_frame().T], ignore_index=True)
    with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
        registros.to_excel(writer, index=True)


registros.loc[(registros['nome'] == nome_pre) & (registros['data'] == str(data_add)), 'pre_pas1'] = prepas1
registros.loc[(registros['nome'] == nome_pre) & (registros['data'] == str(data_add)), 'pre_pad1'] = prepad1
registros.loc[(registros['nome'] == nome_pre) & (registros['data'] == str(data_add)), 'pre_pas2'] = prepas2
registros.loc[(registros['nome'] == nome_pre) & (registros['data'] == str(data_add)), 'pre_pad2'] = prepad2
registros.loc[(registros['nome'] == nome_pre) & (registros['data'] == str(data_add)), 'pre_pas3'] = prepas3
registros.loc[(registros['nome'] == nome_pre) & (registros['data'] == str(data_add)), 'pre_pad3'] = prepad3

def salvarregistros():
    with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
        registros.to_excel(writer, index=True)


addpre.button('Registrar pré', on_click=salvarregistros)

