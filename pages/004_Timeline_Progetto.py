import streamlit as st
import plotly.express as px
import pandas as pd
import shutil
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI, ChatOpenAI
import json
from docx import Document
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
import PyPDF2
import os
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from typing import List
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from typing import Optional
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from utils import read_file_based_on_type
import re

load_dotenv()

class TimeLine(BaseModel):
    """From the given text extract the tasks timelines start dates, end dates, resources"""
    tasks: list = Field(description="List down all the tasks that are in the given text but remember shorten them to 2 words")
    start_datas: list = Field(description="List down all the start dates of the tasks respectively (format: 01-01-2023)")
    end_datas: list = Field(description="List down all the end/finish dates of the tasks respectively (format: 01-03-2023)")
    resourses: list = Field(description="List all the resources being used in the tasks, but remember shorten them to 2 words")

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

def read_pdf_file(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        content = ''
        for page_num in range(len(reader.pages)):
            content += reader.pages[page_num].extract_text()
        return content

def create_gantt_chart(tasks, start_dates, end_dates, resources):
    df = pd.DataFrame({
        'Task': tasks,
        'Start': start_dates,
        'Finish': end_dates,
        'Resource': resources
    })
    print(df)
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource")
    fig.update_yaxes(categoryorder="total ascending")
    return fig

# -------------------------------------------------------------------------------------------

def convert_year_range_to_month(year_range: str) -> list:
    # Define the regex pattern for matching YYYY-YYYY format
    pattern = re.compile(r'^(\d{4})-(\d{4})$')
    
    # Check if the input matches the pattern
    match = pattern.match(year_range)
    
    if match:
        start_year = match.group(1)
        end_year = match.group(2)
        
        # Return the list of converted years
        return [f'01-{start_year}', f'01-{end_year}']
    else:
        raise ValueError("Input does not match the YYYY-YYYY format.")

# Example usage
try:
    result = convert_year_range_to_month('01-2025')
    print(result)  # Output: ['01-2024', '01-2025']
except ValueError as e:
    print(e)

# ------------------------------------------------



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

    st.title("Timeline progetto")

    uploaded_file = st.file_uploader('Upload a pdf file', type=['pdf'])
    if uploaded_file:
        upload_directory = "tendor_timeline"
        os.makedirs(upload_directory, exist_ok=True)
    
        file_path = os.path.join(upload_directory, uploaded_file.name)
        with open(file_path, mode='wb') as w:
            w.write(uploaded_file.getvalue())
        if "data" not in st.session_state:
            st.session_state.data = read_pdf_file(file_path)
        
        shutil.rmtree(upload_directory)
        
        X = output_chain.invoke({"input": st.session_state.data, "output_functions": output_functions})
        print("Raw data", pd.DataFrame(X))
        start_dates =[]
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
        
        if st.sidebar.button("Generate Gantt Chart"):
            fig = create_gantt_chart(tasks, start_dates, end_dates, resources)
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
