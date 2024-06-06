import streamlit as st
import os
from utils import create_vector_database, get_answer, extract_questions
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import shutil

# Set the page configuration
st.set_page_config(page_title="Bando di Gara", layout="wide", initial_sidebar_state="expanded")

# Define custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e1e;
        color: white;
    }
    .sidebar .sidebar-content {
        width: 300px;
        background-color: #333;
        color: white;
    }
    .sidebar .sidebar-content .css-1lcbmhc {
        color: white;
    }
    .sidebar .sidebar-content .css-1d391kg {
        color: white;
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
    div.stButton > button:first-child {
        background-color: #3393FF;
        color: white;
        font-size: 20px;
        height: 3em;
        width: 5em;
        border-radius: 10px;
    }
    .chat-bubble {
        background-color: #333;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        position: relative;
        color: white;
    }
    .chat-buttons {
        position: absolute;
        top: 10px;
        right: 10px;
        display: flex;
        gap: 10px;
    }
    .chat-buttons img {
        width: 20px;
        height: 20px;
        cursor: pointer;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: white;
    }
    .stTextInput > div > input, .stTextArea > div > textarea {
        background-color: #333;
        
        color: white;
        border-radius: 10px;
        height: 40px;
        border: none;
        padding-left: 10px;
    }
    .stChatInput input {
        background-color: #333 !important;
        color: white !important;
        border-radius: 10px !important;
        height: 40px !important;
        border: none !important;
        padding-left: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Display logo
# st.sidebar.image('Dotslot Logo CL.png', width=200)  # Adjust the width as needed
# st.image('chip.png', width=200)  # Adjust the width as needed

# Initialize an instance of the OpenAIEmbeddings class
embeddings = OpenAIEmbeddings()

# Use the `from_texts` class method of the FAISS class to initialize an instance and add the texts and their corresponding embeddings
if 'vector' not in st.session_state:
    texts = ["FAISS is an important library", "LangChain supports FAISS"]
    st.session_state.vector = FAISS.from_texts(texts, embeddings)

# Initialize session state for questions if not already done
if 'questions' not in st.session_state:
    st.session_state.questions = {}

def get_answer_from_vector(question, vector):
    return get_answer(question, vector)

# Example external function to handle the uploaded files and question
def handle_files_and_question(uploaded_files):
    upload_directory = "tendor_docs"
    os.makedirs(upload_directory, exist_ok=True)
    
    for uploaded_file in uploaded_files:
        file_path = os.path.join(upload_directory, uploaded_file.name)
        with open(file_path, mode='wb') as w:
            w.write(uploaded_file.getvalue())
    st.session_state.vector = create_vector_database(upload_directory)

def handle_files_and_others(uploaded_file):
    upload_directory = "tendor_docs"
    os.makedirs(upload_directory, exist_ok=True)
    
    file_path = os.path.join(upload_directory, uploaded_file.name)
    with open(file_path, mode='wb') as w:
        w.write(uploaded_file.getvalue())
    
    st.session_state.vector = create_vector_database(upload_directory)
    shutil.rmtree(upload_directory)

def handle_question(question_file):
    upload_directory_question = "question"
    os.makedirs(upload_directory_question, exist_ok=True)

    question_file_path = os.path.join(upload_directory_question, question_file.name)
    with open(question_file_path, mode='wb') as w:
        w.write(question_file.getvalue())

    st.session_state.questions = extract_questions(question_file_path)
    print(st.session_state.questions)
    shutil.rmtree(upload_directory_question)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar with file uploaders and submit buttons
st.sidebar.header("Bando di Gara")
st.sidebar.markdown('<img src="https://upload.wikimedia.org/wikipedia/commons/8/87/PDF_file_icon.svg" width="30" style="margin-bottom: 5px;">', unsafe_allow_html=True)
uploaded_files = st.sidebar.file_uploader("Choose files", accept_multiple_files=True)
if st.sidebar.button("Submit"):
    if uploaded_files:
        handle_files_and_question(uploaded_files)
        st.sidebar.write("Files submitted and vectorized!")
    else:
        st.sidebar.write("No files selected")

st.sidebar.header("Schema progetto")
uploaded_question_file = st.sidebar.file_uploader("Choose Question file")
if st.sidebar.button("Submit Question"):
    if uploaded_question_file:
        handle_question(uploaded_question_file)
        st.sidebar.write("Question file submitted")
    else:
        st.sidebar.write("No question file selected")

st.sidebar.header("Altri documenti")
st.sidebar.markdown('<img src="https://upload.wikimedia.org/wikipedia/commons/8/87/PDF_file_icon.svg" width="30" style="margin-bottom: 5px;">', unsafe_allow_html=True)
uploaded_other_file = st.sidebar.file_uploader("Choose Other file")
if st.sidebar.button("Submit Other"):
    if uploaded_other_file:
        handle_files_and_others(uploaded_other_file)
        st.sidebar.write("Other files submitted")
    else:
        st.sidebar.write("No other file selected")

# Main panel for displaying questions and answers
question = st.text_input("Question Here",)

def regenerate_answer(question):
    answer = get_answer_from_vector(question, st.session_state.vector)
    for chat in st.session_state.chat_history:
        if chat["question"] == question:
            chat["answer"] = answer
            break

if uploaded_files:
    if question:
        for data in st.session_state.questions:
            val = data["question"]
            answer = get_answer_from_vector(val, st.session_state.vector)
            st.session_state.chat_history.append({"question": val, "answer": answer})

    for i, chat in enumerate(st.session_state.chat_history):
        st.markdown(f"<div class='chat-bubble'>"
                    f"<strong>Q:</strong> {chat['question']}<br>"
                    f"<strong>A:</strong> {chat['answer']}</div>", unsafe_allow_html=True)
        if st.button(f"Regen-{i}", key=f"regen_{i}"):
            regenerate_answer(chat["question"])
            st.experimental_rerun()
else:
    st.error("Carica tutti i file necessari prima di inviare una domanda.")
