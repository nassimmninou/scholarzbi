import streamlit as st
import plotly.express as px
import pandas as pd
import shutil
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from utils import read_file_based_on_type
from docx import Document
from langchain.chat_models import ChatOpenAI
import PyPDF2
import os

# Set Streamlit page configuration
st.set_page_config(page_title="Timeline progetto", layout="wide", initial_sidebar_state="expanded")

# Define the TimeLine model
class TimeLine(BaseModel):
    tasks: list = Field(description="List down all the tasks that are in the given text but remember shorten them to 2 words")
    start_datas: list = Field(description="List down all the start dates of the tasks respectively (format: 01-01-2023)")
    end_datas: list = Field(description="List down all the end/finish dates of the tasks respectively (format: 01-03-2023)")
    resourses: list = Field(description="List all the resources being used in the tasks, but remember shorten them to 2 words")

# Initialize OpenAI model
output_model = ChatOpenAI(model="gpt-4o", temperature=0)
output_functions = [convert_pydantic_to_openai_function(TimeLine)]
output_prompt = ChatPromptTemplate.from_messages([
    ("system", """Think carefully and extract all information as per the {output_functions}. The input is about a tender document that has requirements and also some timelines. 
    Timelines are important for bidders so you have to extract tasks, timelines i.e. start dates, end dates, resources to complete the tasks.
    The text has all the information but we only need the information about the tasks, start dates, end dates, and resources.
    
     The date format should be 01-01-2024 or 01-2024, not from year to year.
     If there is start date then there will be an end date so make sure we have complete dates 
     Tasks and resources not more than 2 to 3 words. Input language is italian and remember while extract later we have built the gantt chat.
     for single task start and and dates can not be same. so please carefully analyse it.
    """),
    ("human", "{input}"),
])
output_model_with_functions = output_model.bind(functions=output_functions, function_call={"name": "TimeLine"})
output_chain = output_prompt | output_model_with_functions | JsonOutputFunctionsParser()

# Initialize query model
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.11)
info_prompt = ChatPromptTemplate.from_messages([
    ("system", """Note you only speak Italian, you answers must be in italian , You will be asked about the timeline question you should respond with good task resources start dates and end dates.
            Be specific on that query as you also get the context.
            Context: {context}
            Query: {query}
            """),
    ("human", "{context}"),
    ("human", "{query}"),
])
query_chain = info_prompt | llm

# Create vector database
def create_vector_database(directory):
    loader = PyPDFDirectoryLoader(directory)
    docs = loader.load()
    documents = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100).split_documents(docs)
    vector = FAISS.from_documents(documents, OpenAIEmbeddings())
    return vector

# Get query answer
def get_query_answer(query, vector):
    X = vector.similarity_search(query)
    X = "\n".join(x.page_content for x in X)
    message = query_chain.invoke({"context": X, "query": query})
    return message.content

# Read PDF file
def read_pdf_file(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        content = ''
        for page_num in range(len(reader.pages)):
            content += reader.pages[page_num].extract_text()
        return content

# Create Gantt chart
def create_gantt_chart(tasks, start_dates, end_dates, resources):
    df = pd.DataFrame({
        'Task': tasks,
        'Start': start_dates,
        'Finish': end_dates,
        'Resource': resources
    })
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource")
    fig.update_yaxes(categoryorder="total ascending")
    return fig

# Convert year range to month
def convert_year_range_to_month(year_range: str) -> list:
    pattern = re.compile(r'^(\d{4})-(\d{4})$')
    match = pattern.match(year_range)
    if match:
        start_year = match.group(1)
        end_year = match.group(2)
        return [f'01-{start_year}', f'01-{end_year}']
    else:
        raise ValueError("Input does not match the YYYY-YYYY format.")

# Convert to resources
def convert_to_resources(X):
    start_dates = []
    end_dates = []
    tasks = X['tasks']
    for date in X['start_datas']:
        try:
            result = convert_year_range_to_month(date)
            start_dates.append(pd.to_datetime(result[0]))
        except ValueError as e:
            start_dates.append(pd.to_datetime(date))
    for date in X['end_datas']:
        try:
            result = convert_year_range_to_month(date)
            end_dates.append(pd.to_datetime(result[1]))
        except ValueError as e:
            end_dates.append(pd.to_datetime(date))
    resources = X["resourses"]
    return resources, tasks, start_dates, end_dates

def main():
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
        .sidebar .sidebar-content .css-1lcbmhc, .sidebar .sidebar-content .css-1d391kg {
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
        .stChatMessage {
            background-color: #333;
            color: white;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .stChatMessage .stTextArea {
            background-color: #333;
            color: white;
            border-radius: 10px;
        }
        .stChatMessage .stTextArea > div > textarea {
            background-color: #333;
            color: white;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<h1>Timeline progetto</h1>', unsafe_allow_html=True)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    uploaded_file = st.file_uploader('Upload a pdf file', type=['pdf'])
    st.session_state.uploaded_file = uploaded_file
    if st.session_state.uploaded_file:
        upload_directory = "tendor_timeline"
        os.makedirs(upload_directory, exist_ok=True)
    
        file_path = os.path.join(upload_directory, uploaded_file.name)
        with open(file_path, mode='wb') as w:
            w.write(uploaded_file.getvalue())
        if "data" not in st.session_state:
            st.session_state.data = read_pdf_file(file_path)
        if "vector" not in st.session_state:
            st.session_state.vector = create_vector_database(upload_directory)
        
        shutil.rmtree(upload_directory)
        
        X = output_chain.invoke({"input": st.session_state.data, "output_functions": output_functions})
        st.session_state.X = X  # Save the result in session state
        st.session_state.uploaded_file = None

    if 'X' in st.session_state:
        resources, tasks, start_dates, end_dates = convert_to_resources(st.session_state.X)
        fig = create_gantt_chart(tasks, start_dates, end_dates, resources)
        st.plotly_chart(fig)

    st.markdown("<hr>", unsafe_allow_html=True)

    question = st.text_input("Question Here")
    if "vector" in st.session_state:
        if question:
            answer = get_query_answer(question, st.session_state.vector)
            st.session_state.chat_history.append({"question": question, "answer": answer})

    # Display chat history with the latest question and answer on top
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"<div class='chat-bubble'>"
                    f"<strong>Q:</strong> {chat['question']}<br>"
                    f"<strong>A:</strong> {chat['answer']}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
