import datetime
import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Registros Glicemia", page_icon='images/glucose_meter_dark.ico', layout="centered", initial_sidebar_state="collapsed", menu_items=None)

container1 = st.container()
container1.image(Image.open('images/large_master_image_glic.png'))

cadastros = pd.read_excel('tables/cadastros.xlsx', index_col=0)
listanomes_geral = cadastros['nome'].unique().astype(str)
registros = pd.read_excel('tables/reg_semanais.xlsx', index_col=0)


tabpre, tabpos = st.tabs(['Pré-intervenção', 'Pós-intervenção'])

container_pre = tabpre.container()
dataselecionada_pre = tabpre.date_input('Filtrar por data', key='data select pre')
container_pre.dataframe(registros.loc[registros['data'] == str(dataselecionada_pre)][['data', 'nome',
                                                                'pre_glic1', 'pre_glic2', 'pre_glic3']], use_container_width=True)


container3 = tabpre.container()
registrospre = container3.expander('Registrar/Atualizar Pré')
addpre = registrospre.container()
data_add_pre = addpre.date_input('Data da intervenção', min_value=datetime.date.today(), key='data add pre')
nome_pre = addpre.selectbox('Selecionar Nome', listanomes_geral, key='nome select pre')
nomeselecionado_pre = registros.loc[registros['nome'] == nome_pre]
valoresselecionados_pre = nomeselecionado_pre[['data', 'pre_glic1', 'pre_glic2', 'pre_glic3']]
valorespordata_pre = valoresselecionados_pre.loc[valoresselecionados_pre['data'] == str(data_add_pre)].fillna(0)
if valorespordata_pre.empty:
    valorpreglic1 = 0
    valorpreglic2 = 0
    valorpreglic3 = 0

else:
    valorpreglic1 = valorespordata_pre['pre_glic1'].values[0]
    valorpreglic2 = valorespordata_pre['pre_glic2'].values[0]
    valorpreglic3 = valorespordata_pre['pre_glic3'].values[0]


colglic1_pre, colglic2_pre = addpre.columns(2)
preglic1 = colglic1_pre.number_input('GLICEMIA 1', min_value=0, value=int(valorpreglic1), key='preglic1 input')
preglic2 = colglic2_pre.number_input('GLICEMIA 2', min_value=0, value=int(valorpreglic2), key='preglic2 input')
preglic3 = colglic1_pre.number_input('GLICEMIA 3', min_value=0, value=int(valorpreglic3), key='preglic3 input')


if registros.loc[(registros['nome'] == nome_pre) & (registros['data'] == str(data_add_pre))].empty:
    registronovo_pre = pd.Series({'nome': nome_pre, 'data': data_add_pre, 'pre_pas1': 0, 'pre_pad1': 0,
                              'pre_pas2': 0, 'pre_pad2': 0, 'pre_pas3': 0, 'pre_pad3': 0,
                              'pos_pas1': 0, 'pos_pad1': 0, 'pos_pas2': 0, 'pos_pad2': 0, 'pos_pas3': 0,
                              'pos_pad3': 0, 'pre_glic1': preglic1, 'pre_glic2': preglic2, 'pre_glic3': preglic3,
                              'pos_glic1': 0, 'pos_glic2': 0, 'pos_glic3': 0})
    registros = pd.concat([registros, registronovo_pre.to_frame().T], ignore_index=True)
    with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
        registros.to_excel(writer, index=True)


registros.loc[(registros['nome'] == nome_pre) & (registros['data'] == str(data_add_pre)), 'pre_glic1'] = preglic1
registros.loc[(registros['nome'] == nome_pre) & (registros['data'] == str(data_add_pre)), 'pre_glic2'] = preglic2
registros.loc[(registros['nome'] == nome_pre) & (registros['data'] == str(data_add_pre)), 'pre_glic3'] = preglic3


def salvarregistrospre():
    with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
        registros.to_excel(writer, index=True)


addpre.button('Registrar pré', on_click=salvarregistrospre)

container_pos = tabpos.container()
dataselecionada_pos = tabpos.date_input('Filtrar por data', key='data select pos')
container_pos.dataframe(registros.loc[registros['data'] == str(dataselecionada_pos)][['data', 'nome',
                                                                'pos_glic1', 'pos_glic2', 'pos_glic3']], use_container_width=True)


container4 = tabpos.container()
registrospos = container4.expander('Registrar/Atualizar Pós')
addpos = registrospos.container()
data_add_pos = addpos.date_input('Data da intervenção', min_value=datetime.date.today(), key='data add pos')
nome_pos = addpos.selectbox('Selecionar Nome', listanomes_geral, key='nome select pos')
nomeselecionado_pos = registros.loc[registros['nome'] == nome_pos]
valoresselecionados_pos = nomeselecionado_pos[['data', 'pos_glic1', 'pos_glic2', 'pos_glic3']]
valorespordata_pos = valoresselecionados_pos.loc[valoresselecionados_pos['data'] == str(data_add_pos)].fillna(0)
if valorespordata_pos.empty:
    valorposglic1 = 0
    valorposglic2 = 0
    valorposglic3 = 0

else:
    valorposglic1 = valorespordata_pos['pos_glic1'].values[0]
    valorposglic2 = valorespordata_pos['pos_glic2'].values[0]
    valorposglic3 = valorespordata_pos['pos_glic3'].values[0]


colglic1_pos, colglic2_pos = addpos.columns(2)
posglic1 = colglic1_pos.number_input('GLICEMIA 1', min_value=0, value=int(valorposglic1), key='posglic1 input')
posglic2 = colglic2_pos.number_input('GLICEMIA 2', min_value=0, value=int(valorposglic2), key='posglic2 input')
posglic3 = colglic1_pos.number_input('GLICEMIA 3', min_value=0, value=int(valorposglic3), key='posglic3 input')


if registros.loc[(registros['nome'] == nome_pos) & (registros['data'] == str(data_add_pos))].empty:
    registronovo_pos = pd.Series({'nome': nome_pos, 'data': data_add_pos, 'pre_pas1': 0, 'pre_pad1': 0,
                              'pre_pas2': 0, 'pre_pad2': 0, 'pre_pas3': 0, 'pre_pad3': 0,
                              'pos_pas1': 0, 'pos_pad1': 0, 'pos_pas2': 0, 'pos_pad2': 0, 'pos_pas3': 0,
                              'pos_pad3': 0, 'pre_glic1': 0, 'pre_glic2': 0, 'pre_glic3': 0, 'pos_glic1': posglic1,
                              'pos_glic2': posglic2, 'pos_glic3': posglic3})
    registros = pd.concat([registros, registronovo_pos.to_frame().T], ignore_index=True)
    with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
        registros.to_excel(writer, index=True)


registros.loc[(registros['nome'] == nome_pos) & (registros['data'] == str(data_add_pos)), 'pos_glic1'] = posglic1
registros.loc[(registros['nome'] == nome_pos) & (registros['data'] == str(data_add_pos)), 'pos_glic2'] = posglic2
registros.loc[(registros['nome'] == nome_pos) & (registros['data'] == str(data_add_pos)), 'pos_glic3'] = posglic3


def salvarregistrospos():
    with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
        registros.to_excel(writer, index=True)


addpos.button('Registrar pós', on_click=salvarregistrospos)

