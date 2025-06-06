import streamlit as st
from conexion import obtener_pacientes
from gestionPacientes import gestion_pacientes
from ecgAnalisisNuev import analizar_ecg
from historial import historial_medico
from chatBot import mostrar_chatbot
import pandas as pd
from evolucion import evolucion_cardiaca

# Configuración del endpoint de LM Studio
LMSTUDIO_ENDPOINT = "http://localhost:1234/v1/chat/completions"

# Configuración de la página
st.set_page_config(
    page_title="MedECG Pro: Sistema de Análisis Cardiovascular",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados con tema médico
st.markdown("""
    <style>
    /* Tema de colores médicos */
    :root {
        --primary-color: #1a6fc4;  /* Azul profesional */
        --secondary-color: #2ecc71;  /* Verde salud */
        --background-light: #f4f6f7;
        --text-dark: #2c3e50;
    }

    /* Fondo y tipografía */
    .stApp {
        background-color: var(--background-light);
        font-family: 'Roboto', 'Arial', sans-serif;
        color: var(--text-dark);
    }

    /* Sidebar de navegación */
    .css-1d391kg {
        background-color: white;
        border-right: 2px solid var(--primary-color);
    }

    /* Títulos */
    h1, h2, h3 {
        color: var(--primary-color);
        font-weight: 600;
    }

    /* Botones de navegación */
    .stButton > button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        font-weight: bold !important;
        height: 100% !important;
        width: 100% !important;
        padding: 10px 15px !important;
        margin: 5px 2px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
        text-align: center !important;
        font-size: 0.9em !important;
    }

    .stButton > button:hover {
        background-color: #155799 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }

    /* Estilo para botón activo */
    .stButton.active > button {
        background-color: #2ecc71 !important;
        border-left: 4px solid #155799 !important;
    }

    /* Tarjetas de información */
    .stDataFrame {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        padding: 15px;
    }

    /* Mensajes de estado */
    .stSuccess {
        background-color: rgba(46, 204, 113, 0.1);
        border-left: 4px solid var(--secondary-color);
    }

    .stWarning {
        background-color: rgba(241, 196, 15, 0.1);
        border-left: 4px solid #f1c40f;
    }

    /* Animaciones sutiles */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .pulse-animation {
        animation: pulse 2s infinite;
    }
            
    /* Ajustes para el contenido principal */
    .main .block-container {
        max-width: 1200px;
        padding: 2rem 2rem;
    }

    /* Mejorar los formularios */
    .stForm {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        background: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    /* Ajustar columnas en formularios */
    .stForm .stColumns {
        gap: 1rem;
    }
      
    /* Estilos para la lista de pacientes */
    .lista-pacientes-container {
        margin-top: 30px;
    }
    
    .paciente-count {
        color: #1a6fc4;
        font-size: 1.1em;
        font-weight: 600;
        margin-bottom: 20px;
        padding: 8px 0;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .paciente-card {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        padding: 20px;
        margin-bottom: 25px;
        border-left: 4px solid #1a6fc4;
        transition: all 0.3s ease;
    }
    
    .paciente-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }
    
    .paciente-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
    }
    
    .paciente-header h3 {
        color: #1a6fc4;
        margin: 0;
        font-size: 1.3em;
    }
    
    .paciente-id {
        background-color: #f0f8ff;
        padding: 5px 10px;
        border-radius: 5px;
        color: #1a6fc4;
        font-weight: 500;
    }
    
    .flex-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 15px;
    }
    
    .flex-section {
        flex: 1;
        min-width: 250px;
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
    }
    
    .datos-personales {
        border-left: 3px solid #4e73df;
    }
    
    .datos-domicilio {
        border-left: 3px solid #1cc88a;
    }
    
    .datos-contacto {
        border-left: 3px solid #f6c23e;
    }
    
    .flex-section h4 {
        color: #2c3e50;
        margin-top: 0;
        margin-bottom: 12px;
        font-size: 1.1em;
        display: flex;
        align-items: center;
    }
    
    .flex-section h4:before {
        margin-right: 8px;
    }
    
    .observaciones-container {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
    
    .observaciones-container h4 {
        color: #2c3e50;
        margin-top: 0;
        margin-bottom: 10px;
    }
    
    .observaciones-text {
        white-space: pre-wrap;
        line-height: 1.6;
    }
    
    @media (max-width: 768px) {
        .flex-container {
            flex-direction: column;
        }
        
        .flex-section {
            min-width: 100%;
        }
    }
            
    .heartbeat-loader {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
    }

    .heartbeat-loader .heart {
        width: 30px;
        height: 30px;
        background-color: #e74c3c;
        position: relative;
        transform: rotate(-45deg);
        animation: heartbeat 1s infinite;
    }

    .heartbeat-loader .heart::before,
    .heartbeat-loader .heart::after {
        content: "";
        width: 30px;
        height: 30px;
        background-color: #e74c3c;
        border-radius: 50%;
        position: absolute;
    }

    .heartbeat-loader .heart::before {
        top: -15px;
        left: 0;
    }

    .heartbeat-loader .heart::after {
        left: 15px;
        top: 0;
    }

    @keyframes heartbeat {
        0%, 100% {
            transform: rotate(-45deg) scale(1);
        }
        50% {
            transform: rotate(-45deg) scale(1.3);
        }
    }
    
    /* Contenedor para navegación responsive */
    .nav-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        padding: 10px;
        margin: 15px 0;
    }
    
    .current-section {
        background-color: #e8f4fc;
        padding: 10px;
        border-radius: 5px; 
        border-left: 4px solid #1a6fc4;
        margin-bottom: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializar el estado de la sección si no existe
if "seccion" not in st.session_state:
    st.session_state["seccion"] = "Gestión de Pacientes"

# Encabezado con logo
with st.container():
    col1, col2 = st.columns([1, 4])
    with col1:
        # Animación de corazón latiendo
        st.markdown("""
        <div class="heartbeat-loader">
        <div class="heart"></div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("<h1 style='color:#1a6fc4;'>MedECG Pro: Sistema de Análisis Cardiovascular</h1>", unsafe_allow_html=True)

# Línea divisoria para mejorar la visualización
st.divider()

# Navegación con botones nativos de Streamlit
st.markdown("<div class='nav-container'>", unsafe_allow_html=True)

# Crear navegación adaptativa para pantallas grandes
desktop_cols = st.columns(5)

with desktop_cols[0]:
    if st.button("🏥 Gestión", key="nav_gestion", use_container_width=True):
        st.session_state["seccion"] = "Gestión de Pacientes"
        st.rerun()

with desktop_cols[1]:
    if st.button("📊 ECG", key="nav_ecg", use_container_width=True):
        st.session_state["seccion"] = "Analizador de ECG"
        st.rerun()

with desktop_cols[2]:
    if st.button("📜 Historial", key="nav_historial", use_container_width=True):
        st.session_state["seccion"] = "Historial Médico"
        st.rerun()

with desktop_cols[3]:
    if st.button("📈 Evolución", key="nav_evolucion", use_container_width=True):
        st.session_state["seccion"] = "Evolución Cardíaca"
        st.rerun()

with desktop_cols[4]:
    if st.button("🤖 Chatbot", key="nav_chatbot", use_container_width=True):
        st.session_state["seccion"] = "Chatbot"
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Mostrar la sección actual
st.markdown(f"<div class='current-section'>Sección actual: {st.session_state['seccion']}</div>", unsafe_allow_html=True)

st.divider()

# --- Sección 1: Gestión de Pacientes ---
if st.session_state["seccion"] == "Gestión de Pacientes":
    gestion_pacientes()

# --- Sección 2: Analizador de Electrocardiogramas con CNN ---
elif st.session_state["seccion"] == "Analizador de ECG":
    pacientes = obtener_pacientes()

    if st.session_state.pacientes.empty:
        st.warning("⚠️ No se encuentran pacientes registrados para realizar analisis")
    else:
        pacientes_lista = []
        for paciente in pacientes:
            paciente_data = {
                "ID Paciente": paciente.get("ID Paciente"),
                "Nombre Paciente": paciente.get("Nombre Paciente"),
                "Telefono Paciente": paciente.get("Telefono Paciente"),
                "Edad": paciente.get("Edad"),
                "Género": paciente.get("Género"),
                "CURP": paciente.get("CURP"),
                "NSS": paciente.get("NSS"),
                "Fecha Nacimiento": paciente.get("Fecha Nacimiento"),
                "Direccion": paciente.get("Direccion"),
                "Colonia": paciente.get("Colonia"),
                "Codigo Postal": paciente.get("Código Postal"),
                "Municipio": paciente.get("Municipio"),
                "Estado": paciente.get("Estado"),
                "Datos de Referencia": paciente.get("Datos de Referencia"),
                "Persona de Contacto": paciente.get("Persona de Contacto"),
                "Parentesco": paciente.get("Parentesco"),
                "Telefono Persona de Contacto": paciente.get("Telefono Persona de Contacto"),
                "Celular Persona de Contacto": paciente.get("Celular Persona de Contacto"),
                "Correo de Contacto": paciente.get("Correo de Contacto"),
                "Observaciones": paciente.get("Observaciones")
            }
            pacientes_lista.append(paciente_data)
        
        if not pacientes_lista:
            st.session_state.pacientes = pd.DataFrame().sort_values(by='ID Paciente')
        else:
            st.session_state.pacientes = pd.DataFrame(pacientes_lista).sort_values(by='ID Paciente')

        analizar_ecg(st.session_state.pacientes)

# --- Sección 3: Historial Médico ---
elif st.session_state["seccion"] == "Historial Médico":
    pacientes = obtener_pacientes()

    if st.session_state.pacientes.empty:
        st.warning("⚠️ No se encuentran pacientes registrados en el sistema")
    else:
        pacientes_lista = []
        for paciente in pacientes:
            paciente_data = {
                "ID Paciente": paciente.get("ID Paciente"),
                "Nombre Paciente": paciente.get("Nombre Paciente"),
                "Telefono Paciente": paciente.get("Telefono Paciente"),
                "Edad": paciente.get("Edad"),
                "Género": paciente.get("Género"),
                "CURP": paciente.get("CURP"),
                "NSS": paciente.get("NSS"),
                "Fecha Nacimiento": paciente.get("Fecha Nacimiento"),
                "Direccion": paciente.get("Direccion"),
                "Colonia": paciente.get("Colonia"),
                "Codigo Postal": paciente.get("Código Postal"),
                "Municipio": paciente.get("Municipio"),
                "Estado": paciente.get("Estado"),
                "Datos de Referencia": paciente.get("Datos de Referencia"),
                "Persona de Contacto": paciente.get("Persona de Contacto"),
                "Parentesco": paciente.get("Parentesco"),
                "Telefono Persona de Contacto": paciente.get("Telefono Persona de Contacto"),
                "Celular Persona de Contacto": paciente.get("Celular Persona de Contacto"),
                "Correo de Contacto": paciente.get("Correo de Contacto"),
                "Observaciones": paciente.get("Observaciones")
            }
            pacientes_lista.append(paciente_data)
        
        if not pacientes_lista:
            st.session_state.pacientes = pd.DataFrame().sort_values(by='ID Paciente')
        else:
            st.session_state.pacientes = pd.DataFrame(pacientes_lista).sort_values(by='ID Paciente')

        historial_medico(st.session_state.pacientes)
# --- Sección 4: Evolución Cardíaca ---
elif st.session_state["seccion"] == "Evolución Cardíaca":
    pacientes = obtener_pacientes()
    if st.session_state.pacientes.empty:
        st.warning("⚠️ No se encuentran pacientes registrados en el sistema")
    else:
        pacientes_lista = []
        for paciente in pacientes:
            paciente_data = {
                "ID Paciente": paciente.get("ID Paciente"),
                "Nombre Paciente": paciente.get("Nombre Paciente"),
                "Telefono Paciente": paciente.get("Telefono Paciente"),
                "Edad": paciente.get("Edad"),
                "Género": paciente.get("Género"),
                "CURP": paciente.get("CURP"),
                "NSS": paciente.get("NSS"),
                "Fecha Nacimiento": paciente.get("Fecha Nacimiento"),
                "Direccion": paciente.get("Direccion"),
                "Colonia": paciente.get("Colonia"),
                "Codigo Postal": paciente.get("Código Postal"),
                "Municipio": paciente.get("Municipio"),
                "Estado": paciente.get("Estado"),
                "Datos de Referencia": paciente.get("Datos de Referencia"),
                "Persona de Contacto": paciente.get("Persona de Contacto"),
                "Parentesco": paciente.get("Parentesco"),
                "Telefono Persona de Contacto": paciente.get("Telefono Persona de Contacto"),
                "Celular Persona de Contacto": paciente.get("Celular Persona de Contacto"),
                "Correo de Contacto": paciente.get("Correo de Contacto"),
                "Observaciones": paciente.get("Observaciones")
            }
            pacientes_lista.append(paciente_data)
        
        st.session_state.pacientes = pd.DataFrame(pacientes_lista).sort_values(by='ID Paciente')
        evolucion_cardiaca(st.session_state.pacientes)  # Nueva función
# --- Sección 5: Chatbot ---
elif st.session_state["seccion"] == "Chatbot":
    mostrar_chatbot()

# --- Pie de página ---
st.markdown("""
    <hr style='border-top: 2px solid #1a6fc4;'>
    <p style="text-align: center; color: #7f8c8d;">
        © 2025 MedECG Pro: Sistema de Análisis Cardiovascular
        <br>Desarrollado por Estudiantes de la Universidad De Colima
        <br><small>Todos los derechos reservados | Uso exclusivo profesional médico</small>
    </p>
    """, unsafe_allow_html=True)