import os
from dotenv import load_dotenv

from dotenv import main
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI, ChatOpenAI
# Importing PyPDFDirectoryLoader from langchain_community.document_loaders to load PDF documents from a directory
from langchain_community.document_loaders import PyPDFDirectoryLoader
# Importing FAISS from langchain_community.vectorstores for efficient similarity search and clustering of dense vectors
from langchain_community.vectorstores import FAISS
# Importing OpenAIEmbeddings from langchain_openai to create embeddings using OpenAI's API
from langchain_openai import OpenAIEmbeddings
# Importing RecursiveCharacterTextSplitter from langchain_text_splitters to split text into chunks recursively
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Importing ChatPromptTemplate from langchain_core.prompts to define a template for chat prompts
from langchain_core.prompts import ChatPromptTemplate
# Importing RunnablePassthrough and RunnableLambda from langchain_core.runnables to create runnable objects
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from langchain_core.runnables.history import RunnableWithMessageHistory
# --------------------------------------------------------------------------------------------
load_dotenv()

# --------------------------------------------------------------------------------------------
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser

from typing import List
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
class Questions(BaseModel):
    """Passage that contains the question"""
    question: str= Field(description="Extract all the question from the provided text")
        
class MultiQuest(BaseModel):
    """extract all questions from the the passage"""
    questions: List[Questions]

tagging_prompt = ChatPromptTemplate.from_template(
    """
    There are multiple question in the provided passage please extract all the questions. Questions are in italian language.
    
    Passage: {input}
"""
)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106")
question_extract_func = [convert_pydantic_to_openai_function(MultiQuest)]
extraction_model = llm.bind(functions=question_extract_func, function_call={"name":"MultiQuest"})

extraction_chain = tagging_prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="questions")
# ------------------------------------------------------------------------------------------


llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.11)

# Define a chat prompt template with a system message to maintain language and word count restrictions, a placeholder for chat history, and a human message for the query
info_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful assistant. The task is to answer the questions for tendor that a user want to fill. 
            You have to answer the query from the context. The limitation in the question are defined.
            Please maintain the restriction of language (Italian) and number of charcters mentioned in the query.
            Be formal and maintain the professional tone. And also generate as possible as max limit charcter answer.
            Answer should be elaborative and must be greater than max charchter mention in  query.
            Context: {context}
            Query: {query}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
    ]
)

# ----------------------

X=""

# Define a function to concatenate the page content from each document in a list X into a single string
def get_context(_):
    return "\n".join(x.page_content for x in X)


# Create a processing chain where the context is generated using a lambda function, the query is passed through unchanged, and both are fed into the chat prompt template and then to the language model
chain = {"context": RunnableLambda(get_context), "query": RunnablePassthrough()} | info_prompt | llm
# Initialize an empty store for session histories
store = {}

# Define a function to retrieve chat message history for a given session ID
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    # If the session ID is not in the store, create a new ChatMessageHistory for it
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    # Return the chat message history for the given session ID
    return store[session_id]

chain_with_chat_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="query",
    history_messages_key="chat_history",
)

# --------crea-----------------------------------------------------

def create_vector_database(directory):
    # Load all PDF documents from the "stemup-attachments/" directory using PyPDFDirectoryLoader
    loader = PyPDFDirectoryLoader(directory)
    docs = loader.load()
    documents = RecursiveCharacterTextSplitter(
    chunk_size=512, chunk_overlap=100
    ).split_documents(docs)
    vector = FAISS.from_documents(documents, OpenAIEmbeddings())
    return vector

def get_answer(query, vector):
    global X
    X = vector.similarity_search(query)
    message = chain_with_chat_history.invoke(
    {"query": query},
    config={"configurable": {"session_id": "abc114"}},
    )
    print(X)
    return message.content

def extract_questions(file_path):
    content = read_file_based_on_type(file_path)
    X = extraction_chain.invoke({"input": content})
    return X
# -----------------------------------------------
import mimetypes
from docx import Document
import PyPDF2

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def read_pdf_file(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        content = ''
        for page_num in range(len(reader.pages)):
            content += reader.pages[page_num].extract_text()
        return content

def read_docx_file(file_path):
    doc = Document(file_path)
    content = ''
    for para in doc.paragraphs:
        content += para.text + '\n'
    return content

def read_file_based_on_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type == 'text/plain':
        return read_txt_file(file_path)
    elif mime_type == 'application/pdf':
        return read_pdf_file(file_path)
    elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return read_docx_file(file_path)
    else:
        return 'Unsupported file type'


