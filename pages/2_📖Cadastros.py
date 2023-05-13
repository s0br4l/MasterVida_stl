import datetime
import os
import string
import streamlit as st
from PIL import Image
import pandas as pd
import ulid

st.set_page_config(page_title="Cadastros", page_icon='images/add_user_dark_.ico', layout="centered", initial_sidebar_state="auto", menu_items=None)

container1 = st.container()
container1.image(Image.open('images/large_master_image_cadastros.png'))

cadastros = pd.read_excel('tables/cadastros.xlsx', index_col=0).dropna()
cadastros_exib = cadastros[['nome', 'data_nascimento', 'turma_hidro', 'turma_pilts', 'exames', 'diabetes', 'hipertensao']]
listanomes_geral = cadastros['nome'].unique().astype(str)


container2 = st.container()
container2.dataframe(cadastros_exib, use_container_width=True)


container3 = st.container()
adduser_exp = container3.expander('Adicionar usuário')
adduser = adduser_exp.container()
nome_add = adduser.text_input('Nome completo')
nome_id_add = ulid.new()
data_nascimento = adduser.date_input('Data de nascimento')
turmahidro_add = adduser.selectbox('Turma Hidro', [' ', 'TQ7h', 'TQ8h', 'QS7h', 'QS8h'])
turmapilts_add = adduser.selectbox('Turma Pilates', [' ', 'PL7h', 'PL8h'])
exames_add = adduser.date_input('Validade dos exames', min_value=datetime.date.today())
diabetes_add = adduser.selectbox('Tem diabetes?', [' ', 'DIB'])
hipertensao_add = adduser.selectbox('Tem hipertensao?', [' ', 'HAS'])
foto_add = adduser.file_uploader('Selecionar foto', type=['jpg', 'png', 'jpeg'])

nome_cadastro = string.capwords(nome_add, sep=None)
nome_id_cadastro = str(nome_id_add)
nascimento_cadastro = data_nascimento.strftime("%d/%m/%y")
hidro_cadastro = turmahidro_add
pilts_cadastro = turmapilts_add
exames_cadastro = exames_add.strftime("%d/%m/%y")
diabetes_cadastro = diabetes_add
hipertensao_cadastro = hipertensao_add
if foto_add:
    with Image.open(foto_add) as im:
        im2 = im.resize((500, 500))
        adduser.image(im2, width=100)


if not nome_cadastro:
    adduser.info('Preencha o nome', icon="ℹ️")

if not foto_add:
    adduser.info('Adicione uma foto', icon="ℹ️")

if cadastros.loc[cadastros['nome'] == nome_cadastro].empty:
    cadastronovo = pd.Series({'nome': nome_cadastro, 'nome_id': nome_id_cadastro, 'data_nascimento': nascimento_cadastro,
                              'turma_hidro': hidro_cadastro, 'turma_pilts': pilts_cadastro, 'exames': exames_cadastro,
                              'diabetes': diabetes_cadastro, 'hipertensao': hipertensao_cadastro})
    cadastros = pd.concat([cadastros, cadastronovo.to_frame().T], ignore_index=True)

else:
    adduser.warning('Usuário já existe, atualize', icon="⚠️")


def salvarcadastro():
    nome_foto = f'foto_{nome_id_cadastro}'
    im2.save(f'cad_images/{nome_foto}.png')
    with pd.ExcelWriter('tables/cadastros.xlsx') as writer:
        cadastros.to_excel(writer, index=True)

if nome_cadastro and foto_add:
    adduser.button('Registrar', on_click=salvarcadastro)


container4 = st.container()
updateuser_exp = container4.expander('Atualizar usuário')
updateuser = updateuser_exp.container()

colnomeselect, colfotoatual = updateuser.columns([2.5, 1], gap='large')
update_nome = colnomeselect.selectbox('Selecionar Nome', listanomes_geral)
nomeselecionado = cadastros.loc[cadastros['nome'] == update_nome]
nome_id_value = nomeselecionado['nome_id'].values[0]
nascimento_ant_value = nomeselecionado['data_nascimento'].values[0]
turma_hidro_ant_value = nomeselecionado['turma_hidro'].values[0]
turma_pilts_ant_value = nomeselecionado['turma_pilts'].values[0]
exames_ant_value = nomeselecionado['exames'].values[0]
diabetes_ant_value = nomeselecionado['diabetes'].values[0]
hipertensao_ant_value = nomeselecionado['hipertensao'].values[0]
if update_nome:
    update_nome_foto = f'foto_{nome_id_value}'
    with Image.open(f'cad_images/{update_nome_foto}.png') as update_foto:
        if update_foto:
            colfotoatual.image(update_foto, width=100, caption='Foto atual')

colcheck, colant, colupdate = updateuser.columns(3)
check_label = colcheck.markdown('☑️')

colfotocheck, colfotoupdate, colupdtprvw = updateuser.columns([0.1, 2.5, 1], gap='medium')
foto_label = colfotocheck.markdown('~')
foto_check = colfotocheck.checkbox(' ', key='foto att')
if foto_check:
    foto_updt = colfotoupdate.file_uploader('Selecionar foto para atualizar', type=['jpg', 'png', 'jpeg'], key='foto updt')
    if foto_updt:
        with Image.open(foto_updt) as im:
            im3 = im.resize((500, 500))
            colupdtprvw.image(im3, width=100, caption='Foto atualizada')
if not foto_check:
    foto_updt = colfotoupdate.file_uploader('Selecionar foto', type=['jpg', 'png', 'jpeg'], key='foto updt', disabled=True)
    update_nome_foto = f'foto_{nome_id_value}'
    with Image.open(f'cad_images/{update_nome_foto}.png') as im:
        im3 = im.resize((500, 500))

colnomecheck, colnomeant, colnomeupdate = updateuser.columns([1, 8, 8])
nome_label = colnomecheck.markdown('~')
nome_check = colnomecheck.checkbox(' ', key='nome att')
nome_ant = colnomeant.text_input('Nome atual', value=update_nome, disabled=True)
if nome_check:
    nome_updt = colnomeupdate.text_input('Nome atualizado')
    nome_cadastro_att = string.capwords(nome_updt, sep=None)
    cadastros.loc[cadastros['nome'] == update_nome, 'nome'] = nome_cadastro_att
if not nome_check:
    nome_updt = colnomeupdate.text_input('Nome atualizado', disabled=True)
    nome_cadastro_att = string.capwords(update_nome, sep=None)
    cadastros.loc[cadastros['nome'] == update_nome, 'nome'] = nome_cadastro_att

colnascimentocheck, colnascimentoant, colnascimentoupdate = updateuser.columns([1, 8, 8])
nascimento_label = colnascimentocheck.markdown('~')
nascimento_check = colnascimentocheck.checkbox(' ', key='data_nascimento')
nascimento_ant = colnascimentoant.text_input('Data nascimento atual', value=nascimento_ant_value, disabled=True)
if nascimento_check:
    nascimento_updt = colnascimentoupdate.date_input('Data nascimento atualizada', max_value=datetime.date.today())
    cadastros.loc[cadastros['nome'] == update_nome, 'data_nascimento'] = nascimento_updt.strftime("%d/%m/%y")
if not nascimento_check:
    nascimento_updt = colnascimentoupdate.date_input('Data nascimento atualizada', max_value=datetime.date.today(), disabled=True)
    cadastros.loc[cadastros['nome'] == update_nome, 'data_nascimento'] = nascimento_ant_value

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
exames_ant = colexamesant.text_input('Validade atual', value=exames_ant_value, disabled=True)
if exames_check:
    exames_updt = colexamesupdate.date_input('Validade atualizada')
    cadastros.loc[cadastros['nome'] == update_nome, 'exames'] = exames_updt.strftime("%d/%m/%y")
if not exames_check:
    exames_updt = colexamesupdate.date_input('Validade atualizada', min_value=datetime.date.today(), disabled=True)
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


def salvaratualizacao():
    nome_foto_updt = f'foto_{nome_id_value}'
    im3.save(f'cad_images/{nome_foto_updt}.png')
    with pd.ExcelWriter('tables/cadastros.xlsx') as writer:
        cadastros.to_excel(writer, index=True)


if foto_check or nome_check or nascimento_check or turma_hidro_check or turma_pilts_check or exames_check \
        or diabetes_check or hipertensao_check:
    updateuser.button('Atualizar', on_click=salvaratualizacao)


container5 = st.container()
deleteuser_exp = container5.expander('Deletar usuário')
deleteuser = deleteuser_exp.container()

colnomedel, colbotaodel = deleteuser.columns([5, 1])
delete_nome = colnomedel.selectbox('Selecionar usuário para excluir', listanomes_geral)
selecionado_del = cadastros.loc[cadastros['nome'] == delete_nome]
nome_del = selecionado_del['nome'].values[0]
index_del = selecionado_del.index.values[0]
nome_id_del = selecionado_del['nome_id'].values[0]


def del_user():
    cadastros = pd.read_excel('tables/cadastros.xlsx', index_col=0).dropna()
    cadastros = cadastros.drop(index=cadastros.index[index_del])
    os.remove(f'cad_images/foto_{nome_id_del}.png')
    with pd.ExcelWriter('tables/cadastros.xlsx') as writer:
        cadastros.to_excel(writer, index=True)


def confirmardel():
    confirmacao_label = deleteuser.text('Tem certeza que quer deletar o cadastro de:')
    deleteuser_cont = deleteuser.container()
    colnome_del, colfoto_del = deleteuser_cont.columns([0.55, 1], gap='large')
    nome_label_del = colnome_del.markdown(f'\n     {nome_del}\n')
    if nome_del:
        delete_foto = f'foto_{nome_id_del}'
        with Image.open(f'cad_images/{delete_foto}.png') as del_foto:
            if del_foto:
                colfoto_del.image(del_foto, width=100)

    colsim, colnao = deleteuser.columns([0.1, 1], gap='small')
    colsim.button('Sim', on_click=del_user)
    colnao.button('Não', on_click=None)


delete_label = colbotaodel.text('~')
colbotaodel.button('Excluir', on_click=confirmardel)

