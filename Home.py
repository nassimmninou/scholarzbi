import streamlit as st
import os
from utils import create_vector_database, get_answer, extract_questions
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import shutil
st.set_page_config(page_title="Bando di Gara", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #1e1e1e;
        color: white;
    }
    .sidebar .sidebar-content {
        width: 300px;
        background-color: #1e1e1e;
    }
    .search-box input {
        background-color: #333;
        color: white;
        border-radius: 10px;
        height: 40px;
        border: none;
        padding-left: 10px;
        margin-bottom: 10px;
    }
    .search-box input::placeholder {
        color: #aaa;
    }
    .stSelectbox, .stMultiselect {
        background-color: #333;
        color: white;
        border-radius: 10px;
    }
    .stSelectbox div, .stMultiselect div {
        color: #333;
    }
    .stMarkdown h1 {
        color: white;
        text-align: center;
    }
    .stMarkdown h2 {
        color: white;
    }
    .stChatInput>div>input {
        background-color: #333;
        color: white;
        border-radius: 10px;
        height: 40px;
        border: none;
        padding-left: 10px;
    }
    .stTextInput>div>input {
        background-color: #333;
        color: white;
        border-radius: 10px;
        height: 40px;
        border: none;
        padding-left: 10px;
        margin-bottom: 10px;
    }
    .center-image {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Center the image using Streamlit's image function with CSS
st.image('aingenius_clr.png', width=778) 
