from datetime import datetime, date, timedelta
import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Registros Pressão Arterial", page_icon='images/blood_pressure_dark.ico',
                   layout="centered", initial_sidebar_state="auto", menu_items=None)

container1 = st.container()
container1.image(Image.open('images/large_master_image_pressao.png'))

cadastros_pressao = pd.read_excel('tables/cadastros.xlsx', index_col=0).dropna()
listanomes_geral_pressao = cadastros_pressao['nome'].unique().astype(str)
registros_pressao = pd.read_excel('tables/reg_semanais.xlsx', index_col=0)

tabpre, tabpos = st.tabs(['Pré-intervenção', 'Pós-intervenção'])

container_pre = tabpre.container()
dataselecionada_pre_pressao = tabpre.date_input('Filtrar por data', key='data select pre')
data_filtro_pre_pressao = dataselecionada_pre_pressao.strftime("%d/%m/%y")
registros_exib_pre_pressao = registros_pressao[
    ['data', 'interv_dia', 'nome', 'pre_pas1', 'pre_pad1', 'pre_pas2', 'pre_pad2', 'pre_pas3', 'pre_pad3']]
container_pre.dataframe(registros_exib_pre_pressao.loc[registros_exib_pre_pressao['data'] == str(data_filtro_pre_pressao)],
                        use_container_width=True)

container3 = tabpre.container()
registrospre = container3.expander('Registrar/Atualizar Pré')
addpre = registrospre.container()

colselect, colfotos = addpre.columns([2.5, 1], gap='large')
data_add_pre_pressao = colselect.date_input('Data da intervenção', min_value=date.today(), key='data add pre', disabled=True)
data_pre_pressao = data_add_pre_pressao.strftime("%d/%m/%y")
foto_label = colfotos.markdown('~')
nome_pre_pressao = colselect.selectbox('Selecionar Nome', listanomes_geral_pressao, key='nome select pre')
nomeselecionado_pre = cadastros_pressao.loc[cadastros_pressao['nome'] == nome_pre_pressao]
nome_id_value_pressao = nomeselecionado_pre['nome_id'].values[0]
if nome_pre_pressao:
    update_nome_foto = f'foto_{nome_id_value_pressao}'
    with Image.open(f'cad_images/{update_nome_foto}.png') as foto_select:
        if foto_select:
            colfotos.image(foto_select, width=100)

nomeselecionado_pre_pressao = registros_pressao.loc[registros_pressao['nome'] == nome_pre_pressao]
valoresselecionados_pre_pressao = nomeselecionado_pre_pressao[
    ['data', 'interv_dia', 'pre_pas1', 'pre_pad1', 'pre_pas2', 'pre_pad2', 'pre_pas3', 'pre_pad3']]
valorespordata_pre_pressao = valoresselecionados_pre_pressao.loc[valoresselecionados_pre_pressao['data'] == str(data_pre_pressao)].fillna(0)
if valorespordata_pre_pressao.empty:
    valorinterv_dia = 'Hidro'
    valorprepas1 = 0
    valorprepad1 = 0
    valorprepas2 = 0
    valorprepad2 = 0
    valorprepas3 = 0
    valorprepad3 = 0
else:
    valorinterv_dia = valorespordata_pre_pressao['interv_dia'].values[0]
    valorprepas1 = valorespordata_pre_pressao['pre_pas1'].values[0]
    valorprepad1 = valorespordata_pre_pressao['pre_pad1'].values[0]
    valorprepas2 = valorespordata_pre_pressao['pre_pas2'].values[0]
    valorprepad2 = valorespordata_pre_pressao['pre_pad2'].values[0]
    valorprepas3 = valorespordata_pre_pressao['pre_pas3'].values[0]
    valorprepad3 = valorespordata_pre_pressao['pre_pad3'].values[0]

if valorinterv_dia == 'Hidro':
    interv_pre = colselect.selectbox('Intervenção do dia', ['Hidro', 'Pilates', 'Relaxamento', 'Não fez aula'], index=0, key='interv select pre')
elif valorinterv_dia == 'Pilates':
    interv_pre = colselect.selectbox('Intervenção do dia', ['Hidro', 'Pilates', 'Relaxamento', 'Não fez aula'], index=1, key='interv select pre')
elif valorinterv_dia == 'Relaxamento':
    interv_pre = colselect.selectbox('Intervenção do dia', ['Hidro', 'Pilates', 'Relaxamento', 'Não fez aula'], index=2, key='interv select pre')
elif valorinterv_dia == 'Não fez aula':
    interv_pre = colselect.selectbox('Intervenção do dia', ['Hidro', 'Pilates', 'Relaxamento', 'Não fez aula'], index=3, key='interv select pre')
colpas_pre, colpad_pre = addpre.columns(2)
prepas1 = colpas_pre.number_input('PAS 1', min_value=0, max_value=999, value=int(valorprepas1), key='prepas1 input',
                                  help='Máx: 150 mmHg')
prepad1 = colpad_pre.number_input('PAD 1', min_value=0, max_value=999, value=int(valorprepad1), key='prepad1 input',
                                  help='Máx: 90 mmHg')
prepas2 = colpas_pre.number_input('PAS 2', min_value=0, max_value=999, value=int(valorprepas2), key='prepas2 input')
prepad2 = colpad_pre.number_input('PAD 2', min_value=0, max_value=999, value=int(valorprepad2), key='prepad2 input')
prepas3 = colpas_pre.number_input('PAS 3', min_value=0, max_value=999, value=int(valorprepas3), key='prepas3 input')
prepad3 = colpad_pre.number_input('PAD 3', min_value=0, max_value=999, value=int(valorprepad3), key='prepad3 input')


def salvarregistrospre():
    registros = pd.read_excel('tables/reg_semanais.xlsx', index_col=0)
    if registros.loc[(registros['nome'] == nome_pre_pressao) & (registros['data'] == str(data_pre_pressao))].empty:
        registronovo_pre = pd.Series({'nome': nome_pre_pressao, 'data': data_pre_pressao, 'interv_dia': interv_pre, 'pre_pas1': prepas1,
                                      'pre_pad1': prepad1, 'pre_pas2': prepas2, 'pre_pad2': prepad2,
                                      'pre_pas3': prepas3,
                                      'pre_pad3': prepad3, 'pos_pas1': 0, 'pos_pad1': 0, 'pos_pas2': 0, 'pos_pad2': 0,
                                      'pos_pas3': 0, 'pos_pad3': 0, 'pre_glic1': 0, 'pre_glic2': 0, 'pre_glic3': 0,
                                      'pos_glic1': 0, 'pos_glic2': 0, 'pos_glic3': 0})
        registros = pd.concat([registros, registronovo_pre.to_frame().T], ignore_index=True)
        with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
            registros.to_excel(writer, index=True)
    registros.loc[(registros['nome'] == nome_pre_pressao) & (registros['data'] == str(data_pre_pressao)), 'interv_dia'] = interv_pre
    registros.loc[(registros['nome'] == nome_pre_pressao) & (registros['data'] == str(data_pre_pressao)), 'pre_pas1'] = prepas1
    registros.loc[(registros['nome'] == nome_pre_pressao) & (registros['data'] == str(data_pre_pressao)), 'pre_pad1'] = prepad1
    registros.loc[(registros['nome'] == nome_pre_pressao) & (registros['data'] == str(data_pre_pressao)), 'pre_pas2'] = prepas2
    registros.loc[(registros['nome'] == nome_pre_pressao) & (registros['data'] == str(data_pre_pressao)), 'pre_pad2'] = prepad2
    registros.loc[(registros['nome'] == nome_pre_pressao) & (registros['data'] == str(data_pre_pressao)), 'pre_pas3'] = prepas3
    registros.loc[(registros['nome'] == nome_pre_pressao) & (registros['data'] == str(data_pre_pressao)), 'pre_pad3'] = prepad3

    with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
        registros.to_excel(writer, index=True)


if interv_pre == 'Relaxamento' or interv_pre == 'Não fez aula':
    addpre.button('Registrar pré', on_click=salvarregistrospre)
else:
    exames_value = nomeselecionado_pre['exames'].values[0]
    exames_date = datetime.strptime(exames_value, "%d/%m/%y").date()

    if (date.today()) > exames_date:
        addpre.warning('Exames vencidos', icon="⚠️")
    elif (date.today()) <= exames_date:
        addpre.button('Registrar pré', on_click=salvarregistrospre)
        if (exames_date - date.today()) <= timedelta(days=30):
            addpre.info('Parecer próximo do vencimento', icon='ℹ️')




container_pos = tabpos.container()
dataselecionada_pos_pressao = tabpos.date_input('Filtrar por data', key='data select pos')
data_filtro_pos_pressao = dataselecionada_pos_pressao.strftime("%d/%m/%y")
registros_exib_pos_pressao = registros_pressao[
    ['data', 'interv_dia', 'nome', 'pos_pas1', 'pos_pad1', 'pos_pas2', 'pos_pad2', 'pos_pas3', 'pos_pad3']]
container_pos.dataframe(registros_exib_pos_pressao.loc[registros_exib_pos_pressao['data'] == str(data_filtro_pos_pressao)],
                        use_container_width=True)

container4 = tabpos.container()
registrospos = container4.expander('Registrar/Atualizar Pós')
addpos = registrospos.container()

colselect, colfotos = addpos.columns([2.5, 1], gap='large')
data_add_pos_pressao = colselect.date_input('Data da intervenção', min_value=date.today(), key='data add pos', disabled=True)
data_pos_pressao = data_add_pos_pressao.strftime("%d/%m/%y")
foto_label = colfotos.markdown('~')
nome_pos_pressao = colselect.selectbox('Selecionar Nome', listanomes_geral_pressao, key='nome select pos')
nomeselecionado_pos = cadastros_pressao.loc[cadastros_pressao['nome'] == nome_pos_pressao]
nome_id_value = nomeselecionado_pos['nome_id'].values[0]
if nome_pos_pressao:
    update_nome_foto = f'foto_{nome_id_value}'
    with Image.open(f'cad_images/{update_nome_foto}.png') as foto_select:
        if foto_select:
            colfotos.image(foto_select, width=100)


nomeselecionado_pos_pressao = registros_pressao.loc[registros_pressao['nome'] == nome_pos_pressao]
valoresselecionados_pos_pressao = nomeselecionado_pos_pressao[
    ['data', 'pos_pas1', 'pos_pad1', 'pos_pas2', 'pos_pad2', 'pos_pas3', 'pos_pad3']]
valorespordata_pos_pressao = valoresselecionados_pos_pressao.loc[valoresselecionados_pos_pressao['data'] == str(data_pos_pressao)].fillna(0)
if valorespordata_pos_pressao.empty:
    valorpospas1 = 0
    valorpospad1 = 0
    valorpospas2 = 0
    valorpospad2 = 0
    valorpospas3 = 0
    valorpospad3 = 0
else:
    valorpospas1 = valorespordata_pos_pressao['pos_pas1'].values[0]
    valorpospad1 = valorespordata_pos_pressao['pos_pad1'].values[0]
    valorpospas2 = valorespordata_pos_pressao['pos_pas2'].values[0]
    valorpospad2 = valorespordata_pos_pressao['pos_pad2'].values[0]
    valorpospas3 = valorespordata_pos_pressao['pos_pas3'].values[0]
    valorpospad3 = valorespordata_pos_pressao['pos_pad3'].values[0]


colpas_pos, colpad_pos = addpos.columns(2)
pospas1 = colpas_pos.number_input('PAS 1', min_value=0, max_value=999, value=int(valorpospas1), key='pospas1 input',
                                  help='Máx: 150 mmHg')
pospad1 = colpad_pos.number_input('PAD 1', min_value=0, max_value=999, value=int(valorpospad1), key='pospad1 input',
                                  help='Máx: 90 mmHg')
pospas2 = colpas_pos.number_input('PAS 2', min_value=0, max_value=999, value=int(valorpospas2), key='pospas2 input')
pospad2 = colpad_pos.number_input('PAD 2', min_value=0, max_value=999, value=int(valorpospad2), key='pospad2 input')
pospas3 = colpas_pos.number_input('PAS 3', min_value=0, max_value=999, value=int(valorpospas3), key='pospas3 input')
pospad3 = colpad_pos.number_input('PAD 3', min_value=0, max_value=999, value=int(valorpospad3), key='pospad3 input')


def salvarregistrospos():
    registros = pd.read_excel('tables/reg_semanais.xlsx', index_col=0)
    if registros.loc[(registros['nome'] == nome_pos_pressao) & (registros['data'] == str(data_pos_pressao))].empty:
        registronovo_pos = pd.Series({'nome': nome_pos_pressao, 'data': data_pos_pressao, 'pre_pas1': 0,
                                      'pre_pad1': 0, 'pre_pas2': 0, 'pre_pad2': 0, 'pre_pas3': 0, 'pre_pad3': 0,
                                      'pos_pas1': pospas1, 'pos_pad1': pospad1, 'pos_pas2': pospas2,
                                      'pos_pad2': pospad2, 'pos_pas3': pospas3, 'pos_pad3': pospad3, 'pre_glic1': 0,
                                      'pre_glic2': 0, 'pre_glic3': 0, 'pos_glic1': 0, 'pos_glic2': 0, 'pos_glic3': 0})
        registros = pd.concat([registros, registronovo_pos.to_frame().T], ignore_index=True)
        with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
            registros.to_excel(writer, index=True)
    registros.loc[(registros['nome'] == nome_pos_pressao) & (registros['data'] == str(data_pos_pressao)), 'pos_pas1'] = pospas1
    registros.loc[(registros['nome'] == nome_pos_pressao) & (registros['data'] == str(data_pos_pressao)), 'pos_pad1'] = pospad1
    registros.loc[(registros['nome'] == nome_pos_pressao) & (registros['data'] == str(data_pos_pressao)), 'pos_pas2'] = pospas2
    registros.loc[(registros['nome'] == nome_pos_pressao) & (registros['data'] == str(data_pos_pressao)), 'pos_pad2'] = pospad2
    registros.loc[(registros['nome'] == nome_pos_pressao) & (registros['data'] == str(data_pos_pressao)), 'pos_pas3'] = pospas3
    registros.loc[(registros['nome'] == nome_pos_pressao) & (registros['data'] == str(data_pos_pressao)), 'pos_pad3'] = pospad3

    with pd.ExcelWriter('tables/reg_semanais.xlsx') as writer:
        registros.to_excel(writer, index=True)


if registros_pressao.loc[(registros_pressao['nome'] == nome_pos_pressao) & (registros_pressao['data'] == str(data_pos_pressao))].empty:
    addpos.warning('Registrar primeiro pré', icon="⚠️")
elif registros_pressao.loc[(registros_pressao['nome'] == nome_pos_pressao) & (registros_pressao['data'] == str(data_pos_pressao)), 'interv_dia'].values[0] == 'Relaxamento' \
        or registros_pressao.loc[(registros_pressao['nome'] == nome_pos_pressao) & (registros_pressao['data'] == str(data_pos_pressao)), 'interv_dia'].values[0] == 'Não fez aula':
    addpos.button('Registrar pós', on_click=salvarregistrospos)
elif registros_pressao.loc[(registros_pressao['nome'] == nome_pos_pressao) & (registros_pressao['data'] == str(data_pos_pressao)), 'interv_dia'].values[0] == 'Hidro' \
        or registros_pressao.loc[(registros_pressao['nome'] == nome_pos_pressao) & (registros_pressao['data'] == str(data_pos_pressao)), 'interv_dia'].values[0] == 'Pilates':
    exames_value = nomeselecionado_pos['exames'].values[0]
    exames_date = datetime.strptime(exames_value, "%d/%m/%y").date()
    if (date.today()) > exames_date:
        addpos.warning('Exames vencidos', icon="⚠️")
    elif (date.today()) <= exames_date:
        addpos.button('Registrar pós', on_click=salvarregistrospos)
        if (exames_date - date.today()) <= timedelta(days=30):
            addpos.info('Parecer próximo do vencimento', icon='ℹ️')


