
# Define custom CSS for styling
import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Profilo Scuola", layout="wide", initial_sidebar_state="expanded")

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

    .stSelectbox div[role="placeholder"], .stMultiselect div[role="placeholder"] {
        color: white;
    }
    .stSelectbox div[role="label"], .stMultiselect div[role="label"] {
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
st.markdown('<h1>Profilo Scuola</h1>', unsafe_allow_html=True)

# Create columns for layout
col1, col2 = st.columns(2)

# Dropdown for Ruolo in col1
with col1:
    st.markdown("## Ruolo")
    ruolo = st.selectbox(
        "Seleziona il tuo ruolo",
        [
            "Dirigente Scolastico",
            "Dirigente Amministrativo",
            "Animatore Digitale",
            "Docente",
            "Team digitale",
            "Progettista",
            "Collaudatore"
        ],
        index=None,
        placeholder="Seleziona il tuo ruolo"
    )

# Dropdown for Tipo di Bando in col2
with col2:
    st.markdown("## Tipo di Bando")
    tipo_bando = st.selectbox(
        "Seleziona il tipo di bando",
        [
            "Fondi PNRR",
            "Fondi Pon",
            "Fondi Erasmus +",
            "Altri fondi"
        ]
        ,        
        index=None,

        placeholder="Seleziona il tipo di bando"
    )

# Create another row for the next set of dropdowns
col3, col4 = st.columns(2)

# Dropdown for Indirizzo Scolastico in col3
with col3:
    st.markdown("## Indirizzo Scolastico")
    indirizzo_scolastico = st.selectbox(
        "Seleziona l'indirizzo scolastico",
        [
            "Licei",
            "Istituto Comprensivo",
            "Liceo Classico",
            "Liceo Scientifico",
            "Opzione Scienze Applicate",
            "Liceo Linguistico",
            "Liceo delle Scienze Umane",
            "Opzione Economico-Sociale",
            "Liceo Artistico",
            "Arti Figurative",
            "Architettura e Ambiente",
            "Design",
            "Audiovisivo e Multimediale",
            "Grafica",
            "Scenografia",
            "Liceo Musicale e Coreutico",
            "Sezione Musicale",
            "Sezione Coreutica",
            "Istituti Tecnici",
            "Settore Economico",
            "Amministrazione, Finanza e Marketing",
            "Relazioni Internazionali per il Marketing",
            "Sistemi Informativi Aziendali",
            "Turismo",
            "Settore Tecnologico",
            "Meccanica, Meccatronica ed Energia",
            "Trasporti e Logistica",
            "Elettronica ed Elettrotecnica",
            "Informatica e TelSecomunicazioni",
            "Grafica e Comunicazione",
            "Chimica, Materiali e Biotecnologie",
            "Sistema Moda",
            "Agraria, Agroalimentare e Agroindustria",
            "Costruzioni, Ambiente e Territorio",
            "Istituti Professionali",
            "Servizi",
            "Servizi per l'Agricoltura e lo Sviluppo Rurale",
            "Servizi Socio-Sanitari",
            "Ottico",
            "Odontotecnico",
            "Servizi per l'Enogastronomia e l'Ospitalità Alberghiera",
            "Enogastronomia",
            "Servizi di Sala e di Vendita",
            "Accoglienza Turistica",
            "Servizi Commerciali",
            "Servizi per la Sanità e l'Assistenza Sociale",
            "Industria e Artigianato",
            "Produzioni Industriali e Artigianali",
            "Artigianato",
            "Industria",
            "Manutenzione e Assistenza Tecnica",
            "Istituti Tecnici Superiori (ITS)",
            "Settore Tecnologico",
            "Nuove Tecnologie per il Made in Italy",
            "Sistema Meccanica",
            "Sistema Moda",
            "Sistema Agroalimentare",
            "Sistema Casa",
            "Efficienza Energetica",
            "Mobilità Sostenibile",
            "Tecnologie Innovative per i Beni e le Attività Culturali - Turismo",
            "Tecnologie dell'Informazione e della Comunicazione",
            "Istituti Professionali con specifiche declinazioni",
            "Indirizzi particolari e sperimentali",
            "Servizi Culturali e dello Spettacolo",
            "Servizi per l'Enogastronomia e l'Ospitalità Alberghiera con specializzazioni regionali"
        ],
     index=None,

        placeholder="Seleziona l'indirizzo scolastico"
    )

# Multi-select for Modello Didattico in col4
with col4:
    st.markdown("## Modello Didattico")
    modello_didattico = st.multiselect(
        "Scegli il modello didattico",
        [
            "Didattica per Scoperta (Inquiry-Based Learning)",
            "Didattica Steineriana (Waldorf)",
            "Apprendimento Basato su Progetti (PBL - Project-Based Learning)",
            "Didattica Montessori",
            "Didattica Laboratoriale",
            "Flipped Classroom (Classe Capovolta)",
            "Didattica Cooperativa",
            "Didattica Digitale",
            "Didattica Inclusiva",
            "Didattica per Competenze",
            "Didattica Tradizionale",
            "Didattica Stem",
            "Didattica Steam",
            "Modello Dada",
            "Modello Ibrido"
        ],

        placeholder="Scegli il modello didattico"
    )

# Add the chat input for URL
st.text_input("Inserisci URL sito internet scuola", key="url_input")
