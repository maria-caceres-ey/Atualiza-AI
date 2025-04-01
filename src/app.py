# app.py
import os
import streamlit as st
from dotenv import load_dotenv
from api import get_projects, get_overdue_tasks, get_team, get_project_status
from utils import get_keywords

load_dotenv()

api_base = os.getenv("EYQ_INCUBATOR_ENDPOINT")
api_key = os.getenv("EYQ_INCUBATOR_KEY")

if not api_base or not api_key:
    st.error("As variáveis de ambiente devem ser definidas.")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = []
if "selected_project" not in st.session_state:
    st.session_state.selected_project = None
if "selected_project_id" not in st.session_state:
    st.session_state.selected_project_id = None

st.markdown("<h1 style='text-align: center;'>Atualiza AI</h1>", unsafe_allow_html=True)
st.write("<h3>Bem-vindo ao Atualiza AI! Escolha um projeto que deseja obter mais informações e acompanhar o andamento.</h3>", unsafe_allow_html=True)
st.write("")

projects = get_projects()
if projects:
    if st.session_state.selected_project is None:
        for project in projects:
            if st.button(f"{project['name']}"):
                st.session_state.selected_project = project
                st.session_state.selected_project_id = project['id']
                st.success(f"Você escolheu o projeto: {project['name']}.")
    else:
        st.markdown(f"<div style='color: green; font-size: 16px;'>Projeto selecionado: {st.session_state.selected_project['name']}</div>", unsafe_allow_html=True)

    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.selected_project:
        user_input = st.text_input(
            "",
            placeholder="Me fale o que deseja saber sobre o projeto . . .",
            key="user_input"
        )

        st.markdown("""
        <style>
        .stTextInput>div>input {
            font-size: 20px; /* Aumenta o tamanho da fonte */
        }
        </style>
        """, unsafe_allow_html=True)

        if user_input:
            keyword = get_keywords(user_input)  # Chama a função de keywords
            if keyword == "atividades atrasadas":
                response_message = get_overdue_tasks(st.session_state.selected_project_id)
            elif keyword == "equipe do projeto":
                response_message = get_team(st.session_state.selected_project_id)
            elif keyword == "status do projeto":
                response_message = get_project_status(st.session_state.selected_project_id)
            else:
                response_message = "Solicitação não reconhecida."

            st.success(response_message)
            st.session_state.history.append({"role": "user", "content": user_input})
            st.session_state.history.append({"role": "assistant", "content": response_message})
