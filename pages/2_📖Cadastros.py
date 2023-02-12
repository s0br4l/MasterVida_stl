import datetime
import string
import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Cadastros", page_icon='images/add_user_dark_.ico', layout="centered", initial_sidebar_state="collapsed", menu_items=None)

container1 = st.container()
container1.image(Image.open('images/large_master_image_cadastros.png'))

cadastros = pd.read_excel('tables/cadastros.xlsx', index_col=0)
listanomes_geral = cadastros['nome'].unique().astype(str)

container2 = st.container()
container2.dataframe(cadastros, use_container_width=True)

container3 = st.container()
adduser_exp = container3.expander('Adicionar usuário')
adduser = adduser_exp.container()
nome_add = adduser.text_input('Nome completo')
turmahidro_add = adduser.selectbox('Turma Hidro', [' ', 'TQ7h', 'TQ8h', 'QS7h', 'QS8h'])
turmapilts_add = adduser.selectbox('Turma Pilates', [' ', 'PL7h', 'PL8h'])
exames_add = adduser.date_input('Validade dos exames', min_value=datetime.datetime.today())
diabetes_add = adduser.selectbox('Tem diabetes?', [' ', 'DIB'])
hipertensao_add = adduser.selectbox('Tem hipertensao?', [' ', 'HAS'])

nome_cadastro = string.capwords(nome_add, sep=None)
if nome_cadastro == '':
    adduser.info('Preencha o nome', icon="ℹ️")
hidro_cadastro = turmahidro_add
pilts_cadastro = turmapilts_add
exames_cadastro = exames_add
diabetes_cadastro = diabetes_add
hipertensao_cadastro = hipertensao_add


if cadastros.loc[cadastros['nome'] == nome_cadastro].empty:
    cadastronovo = pd.Series({'nome': nome_cadastro, 'turma_hidro': hidro_cadastro, 'turma_pilts': pilts_cadastro,
                              'exames': exames_cadastro, 'diabetes': diabetes_cadastro, 'hipertensao': hipertensao_cadastro})
    cadastros = pd.concat([cadastros, cadastronovo.to_frame().T], ignore_index=True)

else:
    adduser.warning('Usuário já existe, atualize', icon="⚠️")


def salvarcadastro():
    with pd.ExcelWriter('tables/cadastros.xlsx') as writer:
        cadastros.to_excel(writer, index=True)


adduser.button('Registrar', on_click=salvarcadastro)

container4 = st.container()
updateuser_exp = container4.expander('Atualizar usuário')
updateuser = updateuser_exp.container()
update_nome = updateuser.selectbox('Selecionar Nome', listanomes_geral)
nomeselecionado = cadastros.loc[cadastros['nome'] == update_nome]
turma_hidro_ant_value = nomeselecionado['turma_hidro'].values[0]
turma_pilts_ant_value = nomeselecionado['turma_pilts'].values[0]
exames_ant_value = nomeselecionado['exames'].values[0]
diabetes_ant_value = nomeselecionado['diabetes'].values[0]
hipertensao_ant_value = nomeselecionado['hipertensao'].values[0]

colcheck, colant, colupdate = updateuser.columns(3)
check_label = colcheck.markdown('☑️')

colhidrocheck, colhidroant, colhidroupdate = updateuser.columns([1, 8, 8])
turma_hidro_label = colhidrocheck.markdown('~')
turma_hidro_check = colhidrocheck.checkbox(' ', key='turma_hidro')
turma_hidro_ant = colhidroant.text_input('Turma Hidro atual', value=turma_hidro_ant_value, disabled=True)
if turma_hidro_check:
    turma_hidro_updt = colhidroupdate.selectbox('Turma Hidro atualizada', [' ', 'TQ7h', 'TQ8h', 'QS7h', 'QS8h'])
    cadastros.loc[cadastros['nome'] == update_nome, 'turma_hidro'] = turma_hidro_updt
if not turma_hidro_check:
    turma_hidro_updt = colhidroupdate.selectbox('Turma Hidro atualizada', [' ', 'TQ7h', 'TQ8h', 'QS7h', 'QS8h'], disabled=True)
    cadastros.loc[cadastros['nome'] == update_nome, 'turma_hidro'] = turma_hidro_ant_value

colpiltscheck, colpiltsant, colpiltsupdate = updateuser.columns([1, 8, 8])
turma_pilts_label = colpiltscheck.markdown('~')
turma_pilts_check = colpiltscheck.checkbox(' ', key='turma_pilts')
turma_pilts_ant = colpiltsant.text_input('Turma Pilates atual', value=turma_pilts_ant_value, disabled=True)
if turma_pilts_check:
    turma_pilts_updt = colpiltsupdate.selectbox('Turma Pilates atualizada', [' ', 'PL7h', 'PL8h'])
    cadastros.loc[cadastros['nome'] == update_nome, 'turma_pilts'] = turma_pilts_updt
if not turma_pilts_check:
    turma_pilts_updt = colpiltsupdate.selectbox('Turma Pilates atualizada', [' ', 'PL7h', 'PL8h'], disabled=True)
    cadastros.loc[cadastros['nome'] == update_nome, 'turma_pilts'] = turma_pilts_ant_value


colexamescheck, colexamesant, colexamesupdate = updateuser.columns([1, 8, 8])
exames_label = colexamescheck.markdown('~')
exames_check = colexamescheck.checkbox(' ', key='exames')
exames_ant = colexamesant.text_input('Validade anterior', value=exames_ant_value, disabled=True)
if exames_check:
    exames_updt = colexamesupdate.date_input('Validade atualizada', min_value=datetime.datetime.today())
    cadastros.loc[cadastros['nome'] == update_nome, 'exames'] = exames_updt
if not exames_check:
    exames_updt = colexamesupdate.date_input('Validade atualizada', min_value=datetime.datetime.today(), disabled=True)
    cadastros.loc[cadastros['nome'] == update_nome, 'exames'] = exames_ant_value


coldiabetescheck, coldiabetesant, coldiabetesupdate = updateuser.columns([1, 8, 8])
diabetes_label = coldiabetescheck.markdown('~')
diabetes_check = coldiabetescheck.checkbox(' ', key='diabetes')
diabetes_ant = coldiabetesant.text_input('Tem diabetes atual', value=diabetes_ant_value, disabled=True)
if diabetes_check:
    diabetes_updt = coldiabetesupdate.selectbox('Tem diabetes atualizada', [' ', 'DIB'])
    cadastros.loc[cadastros['nome'] == update_nome, 'diabetes'] = diabetes_updt
if not diabetes_check:
    diabetes_updt = coldiabetesupdate.selectbox('Tem diabetes atualizada', [' ', 'DIB'], disabled=True)
    cadastros.loc[cadastros['nome'] == update_nome, 'diabetes'] = diabetes_ant_value


colhipertensaocheck, colhipertensaoant, colhipertensaoupdate = updateuser.columns([1, 8, 8])
hipertensao_label = colhipertensaocheck.markdown('~')
hipertensao_check = colhipertensaocheck.checkbox(' ', key='hipertensao')
hipertensao_ant = colhipertensaoant.text_input('Tem hipertensao atual', value=hipertensao_ant_value, disabled=True)
if hipertensao_check:
    hipertensao_updt = colhipertensaoupdate.selectbox('Tem hipertensao atualizada', [' ', 'HAS'])
    cadastros.loc[cadastros['nome'] == update_nome, 'hipertensao'] = hipertensao_updt
if not hipertensao_check:
    hipertensao_updt = colhipertensaoupdate.selectbox('Tem hipertensao atualizada', [' ', 'HAS'], disabled=True)
    cadastros.loc[cadastros['nome'] == update_nome, 'hipertensao'] = hipertensao_ant_value


print(cadastros.loc[cadastros['nome'] == update_nome])

def salvaratualizacao():
    with pd.ExcelWriter('tables/cadastros.xlsx') as writer:
        cadastros.to_excel(writer, index=True)


updateuser.button('Atualizar', on_click=salvaratualizacao)

