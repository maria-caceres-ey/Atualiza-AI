# app.py
import logging
import os
import subprocess
import streamlit as st
from dotenv import load_dotenv
import requests
import sys
import os
from app.streamlit.streamlit_models import *

def start_streamlit():
    """Starts the Streamlit application."""
    try:
        logging.info("Starting Streamlit app...")

        # (one of the possible solutions)
        # Setting PYTHONPATH to the current working directory
        os.environ["PYTHONPATH"] = os.getcwd()

        subprocess.run(["streamlit", "run", "ui/streamlit_ui.py"], check=True)
    except subprocess.CalledProcessError as e:
        # Logging the specific error if the Streamlit command fails
        logging.error(f"Streamlit command failed with error: {e}")
    except Exception as e:
        # Logging any other errors that might occur
        logging.error(f"Error starting Streamlit app: {e}")



if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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

    #streamlit run app\streamlit\app.py
    project_id = "e4005fd0-7b95-4391-8486-c4b21c935b2e"
    url = f"http://localhost:8000/devops/projects/{project_id}/daily_tasks"

    try:
        response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
        response.raise_for_status()
        daily_tasks = response.json()

        result = SlWorkItemQueryResult.from_json_list(daily_tasks)
        result.display_in_streamlit()

        if daily_tasks:
            st.write("### Tarefas Diárias")
            st.json(daily_tasks)  # Exibe a lista de JSON como está
        else:
            st.write("Nenhuma tarefa diária encontrada.")

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao obter dados: {e}")