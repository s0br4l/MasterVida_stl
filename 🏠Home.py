
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Programa Master Vida", page_icon='images/logomaster_icon.ico', layout="centered", initial_sidebar_state="collapsed", menu_items=None)

container1 = st.container()
container1.image(Image.open('images/large_master_image.png'))

container2 = st.container()
container2.text_area('', "🗒️ Checklist Master Vida  \n\n"
                                              "⌚ Horário de chegada 06:50 \n"
                                              "📌Na chegada e saída, auxiliar na logística e organização dos materiais que ficam no GEquip.\n"
                                              "🗣️ A comunicação entre os monitores é importante.\n\n"
                                              "➡️Pré/Pós\n"
                                              "🆔Lembrar de solicitar a carteirinha\n"
                                              "🟡 Conferir a data de vencimento do parecer cardiológico\n"
                                              "🔴Atenção com os valores referentes as medições.\n"
                                              "⬜🟩🟥🟦 - Atenção na entrega das fichas para as usuárias\n\n"
                                              "➡️ Hidroginástica\n"
                                              "📻 Caixa de som e playlist\n"
                                              "🎟️ Recebimento das fichas\n"
                                              "❗ Organizar o quanto antes os materiais da aula.\n\n"
                                              "➡️Pilates/Relaxamento\n"
                                              "🎟️ Recebimento das fichas\n"
                                              "❗ Organizar o quanto antes os materiais da aula.\n"
                                              "🔑 Lembrar de pegar e devolver a chave da sala.", height=550)

