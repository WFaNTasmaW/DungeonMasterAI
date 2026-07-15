import streamlit as st
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from services.rag_service import RAGService
st.set_page_config(
    page_title="Rule Search",
    page_icon="📖",
)

st.title("📖 AI Rule Search")

st.write(
    "Задайте любой вопрос по правилам D&D, монстрам, заклинаниям или классам."
)

if "rag_service" not in st.session_state:
    st.session_state.rag_service = RAGService()

question = st.text_area(
    "Ваш вопрос",
    placeholder="Например: Что делает заклинание Ускорение?"
)

if st.button("Получить ответ", use_container_width=True):

    if question.strip():

        with st.spinner("Думаю..."):

            answer = st.session_state.rag_service.ask(question)

        st.markdown("### Ответ")

        st.write(answer)