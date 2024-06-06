import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Scegli Bando", layout="wide", initial_sidebar_state="expanded")
# Define the main content area
st.markdown('<h1>Scegli Bando</h1>', unsafe_allow_html=True)

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

.stMultiselect > div > div {
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


# Create columns for layout
col1, col2 = st.columns(2)

# Dropdown for Ruolo in col1
with col1:
    st.markdown("## PNRR")
    ruolo = st.selectbox(
        "Seleziona il bando di tuo interesse",
        [
            "PNRR Scuole Paritarie | Competenze STEM e multilinguistiche (DM 65/2023)",
            "Competenze STEM e multilinguistiche | Scuole statali (DM 65/2023)",
            "Formazione del personale scolastico per la transizione digitale (DM 66/2023)",
            "Potenziamento infrastrutture per lo sport a scuola",
            "Messa in sicurezza e riqualificazione delle scuole",
            "Asili nido e scuole dell’infanzia",
            "Costruzione di nuove scuole",
            "Scuole 4.0: nuove aule didattiche e laboratori"
        ], 
index=None,
        placeholder="Seleziona il bando di tuo interesse"
    )

# Dropdown for Tipo di Bando in col2
with col2:
    st.markdown("## PON")
    tipo_bando = st.selectbox(
        "Seleziona il bando di tuo interesse",
        [
            "Iniziativa Agenda Sud",
            "Iniziativa CARE",
            "Iniziativa PCTO estero",
            "Avviso Socialità, apprendimenti e accoglienza",
            "Apprendimento e socialità",
            "Supporti didattici",
            "Contrasto alla povertà educativa",
            "Alternanza scuola-lavoro",
            "Formazione per adulti",
            "Competenze di base",
            "Inclusione sociale e lotta al disagio",
            "Sport di Classe",
            "Patrimonio culturale, artistico e paesaggistico",
            "Integrazione e accoglienza",
            "Cittadinanza europea",
            "Competenze di cittadinanza",
            "Orientamento",
            "Educazione all'imprenditorialità",
            "Cittadinanza e creatività digitale",
            "Formazione all'innovazione didattica e organizzativa",
            "Individuazione snodi formativi territoriali"
        ],
        index=None,
        placeholder="Seleziona il bando di tuo interesse"
    )

    # Display additional options based on the selected bando type


# Create another row for the next set of dropdowns
col3, col4 = st.columns(2)

# Dropdown for Indirizzo Scolastico in col3
with col3:
    st.markdown("## Altri Fondi ")
    indirizzo_scolastico = st.selectbox(
        "Seleziona il bando di tuo interesse ",
        [
            "Fondo PNFD",
            "Fondi PCTO",
            "Piano Nazionale Cinema e Immagini per la Scuola"
        ],
        index=None,
        placeholder="Seleziona il bando di tuo interesse"
    )

with col4:
    st.markdown("## ERASMUS +")
    indirizzo_scolastico = st.selectbox(
        "Seleziona il bando di tuo interesse",
        [
            
        ],
        index=None,
        placeholder="Seleziona il bando di tuo interesse"
    )
# Multi-select for Modello Didattico in col4


# Add the chat input for URL
