import json
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analizza Preventivi", layout="wide", initial_sidebar_state="expanded")

# Define custom CSS for styling
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
    .stSelectbox > div > div {
        background-color: #333;
        color: white;
    }
    .stMultiselect > div > div {
        background-color: #333;
        color: white;
    }
    .stSelectbox div[role="listbox"], .stMultiselect div[role="listbox"] {
        background-color: #333;
        color: white;
    }
    .stSelectbox div[role="option"], .stMultiselect div[role="option"] {
        background-color: #333;
        color: white;
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
    .starter-questions button {
        background-color: #333;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        cursor: pointer;
    }
    .starter-questions button:hover {
        background-color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define the main content area
st.markdown('<h1>Analizza Preventivi</h1>', unsafe_allow_html=True)

def get_pdf_text(pdf_docs):
    texts = []
    for pdf in pdf_docs:
        text = ""
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
        texts.append(text)
    return texts

def get_vectorstore(texts):
    if not texts:
        raise ValueError("No texts to process for vector store creation.")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=texts, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(model="gpt-4")
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
    )
    return conversation_chain

def handle_userinput(user_question):
    modified_prompt = """Provide a response strictly in JSON format. Your response must be like "{}" not "```json{..". Do not include any textual explanation or additional characters. Start your answer directly with a valid JSON object in the format: 
    {
      "title": "",
      "xlabel": "",
      "ylabel": "",
      "data": [],
      "charttype": "",
      "series": [],
      "legend": false
    }. 
    The "title" field should contain the title of the chart. The "xlabel" and "ylabel" fields should contain the labels for the X and Y axes, respectively. The "data" field should be an array of objects representing the data points, and the "charttype" field should specify the appropriate chart type (e.g., "line", "bar"). The "series" field should contain an array of series names if applicable, and the "legend" field should be a boolean indicating whether a legend should be displayed. Ensure that the response provides insights that fulfill the user's request and accurately reflect the benchmark objectives, considering each document represents a vendor quote. Avoid using nested JSON structures for the data field. Answer the following question: """ + user_question

    response = st.session_state.conversation({'question': modified_prompt})
    st.session_state.chat_history.append((user_question, response['answer'], None))

    # Parse the JSON response
    try:
        json_response = json.loads(response['answer'])
    except json.JSONDecodeError:
        st.write("Error: Invalid JSON response")
        return

    # Generate the interpretation
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    messages = [
        ("system", "You are an italian, you only Speak Italian Chart Reader "),
        ("human", "Interpret the following Data (Data was Found by you from quotes vendors) and give your feedback about it" + response['answer'])
    ]
    llm_response = llm.invoke(messages).content
    st.session_state.chat_history[-1] = (user_question, response['answer'], llm_response)

    # Plot the data
    plot_data(json_response)

def plot_data(json_response):
    try:
        data = json_response['data']
        charttype = json_response['charttype']
        title = json_response['title']
        xlabel = json_response['xlabel']
        ylabel = json_response['ylabel']
        legend = json_response['legend']

        # Extract the labels and series data dynamically
        labels = [list(item.values())[0] for item in data]
        series_keys = list(data[0].keys())[1:]  # Assume first key is the label, rest are series

        # Replace None and non-numeric values with 0
        series_data = {}
        for key in series_keys:
            series_data[key] = []
            for item in data:
                value = item[key]
                if value is None or not isinstance(value, (int, float)):
                    series_data[key].append(0)
                else:
                    series_data[key].append(value)

        fig, ax = plt.subplots()
        
        if charttype == "bar":
            bar_width = 0.35
            index = range(len(labels))
            for i, key in enumerate(series_keys):
                plt.bar([x + bar_width*i for x in index], series_data[key], bar_width, label=key)
            plt.xticks([x + bar_width*(len(series_keys)-1)/2 for x in index], labels, rotation=45)
        elif charttype == "line":
            for key in series_keys:
                plt.plot(labels, series_data[key], label=key)
        else:
            st.write(f"Chart type {charttype} not supported.")

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        if legend:
            plt.legend()

        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.write("Coudn't generate the Graph")

def main():
    load_dotenv()

    # Initialize session state if not already done
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.subheader("I tuoi documenti")
    pdf_docs = st.file_uploader(
        "Carica qui i tuoi PDF e fai clic su 'Elabora'", accept_multiple_files=True)
        
    if st.button("Elabora"):
        with st.spinner("Processing"):
            texts = get_pdf_text(pdf_docs)

            if not texts:
                st.write("No text extracted from PDFs.")
                return

            try:
                vectorstore = get_vectorstore(texts)
            except ValueError as e:
                st.write(str(e))
                return

            st.session_state.conversation = get_conversation_chain(vectorstore)

    if st.session_state.conversation:

        if st.button("Confronta il prezzo di ciascun prodotto di tutti i fornitori."):
            handle_userinput("Confronta il prezzo di ciascun prodotto di tutti i fornitori.")
        if st.button("Confronta il prezzo totale dei preventivi di ciascun fornitore"):
            handle_userinput("Confronta il prezzo totale dei preventivi di ciascun fornitore.")

        user_question = st.text_input("Oppure digita la tua domanda:")
        if user_question:
            st.session_state.user_question = user_question
            handle_userinput(user_question)

        if "chat_history" in st.session_state:
            for entry in reversed(st.session_state.chat_history):
                question, answer, interpretation = entry if len(entry) == 3 else (*entry, None)
                st.write(question)
                try:
                    json_response = json.loads(answer)
                    plot_data(json_response)
                    if interpretation:
                        st.write(interpretation)
                except json.JSONDecodeError:
                    st.write("Error: Invalid JSON response")

if __name__:
    main()
