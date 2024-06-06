import streamlit as st
st.set_page_config(page_title="RendicontazioneUtile", layout="wide", initial_sidebar_state="expanded")

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
    </style>
    """,
    unsafe_allow_html=True
)
# Define the sidebar with search bars

# Define the main content area
st.markdown('<h1>RendicontazioneUtile</h1>', unsafe_allow_html=True)
