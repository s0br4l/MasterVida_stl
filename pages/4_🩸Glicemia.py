from datetime import datetime, date, timedelta
import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Registros Glicemia", page_icon='images/glucose_meter_dark.ico', layout="centered", initial_sidebar_state="auto", menu_items=None)

container1 = st.container()
container1.image(Image.open('images/large_master_image_glic.png'))

cadastros_glicemia = pd.read_excel('tables/cadastros.xlsx', index_col=0)
cadastros_dib = cadastros_glicemia.loc[cadastros_glicemia['diabetes'] == 'DIB']
listanomes_geral_glicemia = cadastros_dib['nome'].unique().astype(str)
registros_glicemia = pd.read_excel('tables/reg_semanais.xlsx', index_col=0)


tabpre, tabpos = st.tabs(['Pré-intervenção', 'Pós-intervenção'])

container_pre = tabpre.container()
dataselecionada_pre_glicemia = tabpre.date_input('Filtrar por data', key='data select pre')
data_filtro_pre_glicemia = dataselecionada_pre_glicemia.strftime("%d/%m/%y")
registros_exib_pre_glicemia = registros_glicemia[['data', 'interv_dia', 'nome', 'pre_glic1', 'pre_glic2', 'pre_glic3']]
container_pre.dataframe(registros_exib_pre_glicemia.loc[registros_exib_pre_glicemia['data'] == str(data_filtro_pre_glicemia)], use_container_width=True)


container3 = tabpre.container()
registrospre = container3.expander('Registrar/Atualizar Pré')
addpre = registrospre.container()

colselect, colfotos = addpre.columns([2.5, 1], gap='large')
data_add_pre_glicemia = colselect.date_input('Data da intervenção', min_value=date.today(), key='data add pre', disabled=True)
data_pre_glicemia = data_add_pre_glicemia.strftime("%d/%m/%y")
foto_label = colfotos.markdown('~')
nome_pre_glicemia = colselect.selectbox('Selecionar Nome', listanomes_geral_glicemia, key='nome select pre')
nomeselecionado_prg = cadastros_glicemia.loc[cadastros_glicemia['nome'] == nome_pre_glicemia]
nome_id_value = nomeselecionado_prg['nome_id'].values[0]
if nome_pre_glicemia:
    update_nome_foto = f'foto_{nome_id_value}'
    with Image.open(f'cad_images/{update_nome_foto}.png') as foto_select:
        if foto_select:
            colfotos.image(foto_select, width=100)

nomeselecionado_pre_glicemia = registros_glicemia.loc[registros_glicemia['nome'] == nome_pre_glicemia]
valoresselecionados_pre_glicemia = nomeselecionado_pre_glicemia[['data', 'pre_glic1', 'pre_glic2', 'pre_glic3']]
valorespordata_pre_glicemia = valoresselecionados_pre_glicemia.loc[valoresselecionados_pre_glicemia['data'] == str(data_pre_glicemia)].fillna(0)
if valorespordata_pre_glicemia.empty:
    valorpreglic1 = 0
    valorpreglic2 = 0
    valorpreglic3 = 0

else:
    valorpreglic1 = valorespordata_pre_glicemia['pre_glic1'].values[0]
    valorpreglic2 = valorespordata_pre_glicemia['pre_glic2'].values[0]
    valorpreglic3 = valorespordata_pre_glicemia['pre_glic3'].values[0]


colglic1_pre, colglic2_pre = addpre.columns(2)
preglic1 = colglic1_pre.number_input('GLICEMIA 1', min_value=0, max_value=999, value=int(valorpreglic1), key='preglic1 input', help='Intervalo: 120-250 mg/dl')
preglic2 = colglic2_pre.number_input('GLICEMIA 2', min_value=0, max_value=999, value=int(valorpreglic2), key='preglic2 input')
preglic3 = colglic1_pre.number_input('GLICEMIA 3', min_value=0, max_value=999, value=int(valorpreglic3), key='preglic3 input')


def salvarregistrospre():
    registros = pd.read_excel('tables/reg_semanais.xlsx', index_col=0)
    if registros.loc[(registros['nome'] == nome_pre_glicemia) & (registros['data'] == str(data_pre_glicemia))].empty:
        registronovo_pre = pd.Series({'nome': nome_pre_glicemia, 'data': data_pre_glicemia, 'pre_pas1': 0, 'pre_pad1': 0,
                                      'pre_pas2': 0, 'pre_pad2': 0, 'pre_pas3': 0, 'pre_pad3': 0,
                                      'pos_pas1': 0, 'pos_pad1': 0, 'pos_pas2': 0, 'pos_pad2': 0, 'pos_pas3': 0,
                                      'pos_pad3': 0, 'pre_glic1': preglic1, 'pre_glic2': preglic2,
                                      'pre_glic3': preglic3,
                                      'pos_glic1': 0, 'pos_glic2': 0, 'pos_glic3': 0})
        registros = pd.concat([registros, registronovo_pre.to_frame().T], ignore_index=True)
        with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
            registros.to_excel(writer, index=True)
    registros.loc[(registros['nome'] == nome_pre_glicemia) & (registros['data'] == str(data_pre_glicemia)), 'pre_glic1'] = preglic1
    registros.loc[(registros['nome'] == nome_pre_glicemia) & (registros['data'] == str(data_pre_glicemia)), 'pre_glic2'] = preglic2
    registros.loc[(registros['nome'] == nome_pre_glicemia) & (registros['data'] == str(data_pre_glicemia)), 'pre_glic3'] = preglic3

    with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
        registros.to_excel(writer, index=True)


if registros_glicemia.loc[(registros_glicemia['nome'] == nome_pre_glicemia) & (registros_glicemia['data'] == str(data_pre_glicemia))].empty:
    addpre.warning('Registrar primeiro pressão', icon="⚠️")
elif registros_glicemia.loc[(registros_glicemia['nome'] == nome_pre_glicemia) & (registros_glicemia['data'] == str(data_pre_glicemia)), 'interv_dia'].values[0] == 'Relaxamento' \
        or registros_glicemia.loc[(registros_glicemia['nome'] == nome_pre_glicemia) & (registros_glicemia['data'] == str(data_pre_glicemia)), 'interv_dia'].values[0] == 'Não fez aula':
    addpre.button('Registrar pós', on_click=salvarregistrospre)
elif registros_glicemia.loc[(registros_glicemia['nome'] == nome_pre_glicemia) & (registros_glicemia['data'] == str(data_pre_glicemia)), 'interv_dia'].values[0] == 'Hidro' \
        or registros_glicemia.loc[(registros_glicemia['nome'] == nome_pre_glicemia) & (registros_glicemia['data'] == str(data_pre_glicemia)), 'interv_dia'].values[0] == 'Pilates':
    exames_value = nomeselecionado_prg['exames'].values[0]
    exames_date = datetime.strptime(exames_value, "%d/%m/%y").date()
    if (date.today()) > exames_date:
        addpre.warning('Exames vencidos', icon="⚠️")
    elif (date.today()) <= exames_date:
        addpre.button('Registrar pré', on_click=salvarregistrospre)
        if (exames_date - date.today()) <= timedelta(days=30):
            addpre.info('Parecer próximo do vencimento', icon='ℹ️')


container_pos = tabpos.container()
dataselecionada_pos_glicemia = tabpos.date_input('Filtrar por data', key='data select pos')
data_filtro_pos_glicemia = dataselecionada_pos_glicemia.strftime("%d/%m/%y")
registros_exib_pos_glicemia = registros_glicemia[['data', 'nome', 'pos_glic1', 'pos_glic2', 'pos_glic3']]
container_pos.dataframe(registros_exib_pos_glicemia.loc[registros_exib_pos_glicemia['data'] == str(data_filtro_pos_glicemia)], use_container_width=True)


container4 = tabpos.container()
registrospos = container4.expander('Registrar/Atualizar Pós')
addpos = registrospos.container()

colselect, colfotos = addpos.columns([2.5, 1], gap='large')
data_add_pos_glicemia = colselect.date_input('Data da intervenção', min_value=date.today(), key='data add pos', disabled=True)
data_pos_glicemia = data_add_pos_glicemia.strftime("%d/%m/%y")
foto_label = colfotos.markdown('~')
nome_pos_glicemia = colselect.selectbox('Selecionar Nome', listanomes_geral_glicemia, key='nome select pos')
nomeselecionado_psg = cadastros_glicemia.loc[cadastros_glicemia['nome'] == nome_pos_glicemia]
nome_id_value = nomeselecionado_psg['nome_id'].values[0]
if nome_pos_glicemia:
    update_nome_foto = f'foto_{nome_id_value}'
    with Image.open(f'cad_images/{update_nome_foto}.png') as foto_select:
        if foto_select:
            colfotos.image(foto_select, width=100)


nomeselecionado_pos_glicemia = registros_glicemia.loc[registros_glicemia['nome'] == nome_pos_glicemia]
valoresselecionados_pos_glicemia = nomeselecionado_pos_glicemia[['data', 'pos_glic1', 'pos_glic2', 'pos_glic3']]
valorespordata_pos_glicemia = valoresselecionados_pos_glicemia.loc[valoresselecionados_pos_glicemia['data'] == str(data_pos_glicemia)].fillna(0)
if valorespordata_pos_glicemia.empty:
    valorposglic1 = 0
    valorposglic2 = 0
    valorposglic3 = 0

else:
    valorposglic1 = valorespordata_pos_glicemia['pos_glic1'].values[0]
    valorposglic2 = valorespordata_pos_glicemia['pos_glic2'].values[0]
    valorposglic3 = valorespordata_pos_glicemia['pos_glic3'].values[0]


colglic1_pos, colglic2_pos = addpos.columns(2)
posglic1 = colglic1_pos.number_input('GLICEMIA 1', min_value=0, max_value=999, value=int(valorposglic1), key='posglic1 input', help='Intervalo: 120-250 mg/dl')
posglic2 = colglic2_pos.number_input('GLICEMIA 2', min_value=0, max_value=999, value=int(valorposglic2), key='posglic2 input')
posglic3 = colglic1_pos.number_input('GLICEMIA 3', min_value=0, max_value=999, value=int(valorposglic3), key='posglic3 input')


def salvarregistrospos():
    registros = pd.read_excel('tables/reg_semanais.xlsx', index_col=0)
    if registros.loc[(registros['nome'] == nome_pos_glicemia) & (registros['data'] == str(data_pos_glicemia))].empty:
        registronovo_pos = pd.Series({'nome': nome_pos_glicemia, 'data': data_pos_glicemia, 'pre_pas1': 0, 'pre_pad1': 0,
                                      'pre_pas2': 0, 'pre_pad2': 0, 'pre_pas3': 0, 'pre_pad3': 0,
                                      'pos_pas1': 0, 'pos_pad1': 0, 'pos_pas2': 0, 'pos_pad2': 0, 'pos_pas3': 0,
                                      'pos_pad3': 0, 'pre_glic1': 0, 'pre_glic2': 0, 'pre_glic3': 0,
                                      'pos_glic1': posglic1,
                                      'pos_glic2': posglic2, 'pos_glic3': posglic3})
        registros = pd.concat([registros, registronovo_pos.to_frame().T], ignore_index=True)
        with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
            registros.to_excel(writer, index=True)
    registros.loc[(registros['nome'] == nome_pos_glicemia) & (registros['data'] == str(data_pos_glicemia)), 'pos_glic1'] = posglic1
    registros.loc[(registros['nome'] == nome_pos_glicemia) & (registros['data'] == str(data_pos_glicemia)), 'pos_glic2'] = posglic2
    registros.loc[(registros['nome'] == nome_pos_glicemia) & (registros['data'] == str(data_pos_glicemia)), 'pos_glic3'] = posglic3

    with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
        registros.to_excel(writer, index=True)


if registros_glicemia.loc[(registros_glicemia['nome'] == nome_pos_glicemia) & (registros_glicemia['data'] == str(data_pos_glicemia))].empty:
    addpos.warning('Registrar primeiro pré', icon="⚠️")
elif registros_glicemia.loc[(registros_glicemia['nome'] == nome_pos_glicemia) & (registros_glicemia['data'] == str(data_pos_glicemia)), 'interv_dia'].values[0] == 'Relaxamento' \
        or registros_glicemia.loc[(registros_glicemia['nome'] == nome_pos_glicemia) & (registros_glicemia['data'] == str(data_pos_glicemia)), 'interv_dia'].values[0] == 'Não fez aula':
    addpos.button('Registrar pós', on_click=salvarregistrospos, key='botao reg pos relx')
elif registros_glicemia.loc[(registros_glicemia['nome'] == nome_pos_glicemia) & (registros_glicemia['data'] == str(data_pos_glicemia)), 'interv_dia'].values[0] == 'Hidro' \
        or registros_glicemia.loc[(registros_glicemia['nome'] == nome_pos_glicemia) & (registros_glicemia['data'] == str(data_pos_glicemia)), 'interv_dia'].values[0] == 'Pilates':
    exames_value = nomeselecionado_psg['exames'].values[0]
    exames_date = datetime.strptime(exames_value, "%d/%m/%y").date()
    if (date.today()) > exames_date:
        addpos.warning('Exames vencidos', icon="⚠️")
    elif (date.today()) <= exames_date:
        addpos.button('Registrar pós', on_click=salvarregistrospos, key='botao reg pos')
        if (exames_date - date.today()) <= timedelta(days=30):
            addpos.info('Parecer próximo do vencimento', icon='ℹ️')

