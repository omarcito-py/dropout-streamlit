import base64
import streamlit as st
import pandas as pd
import numpy as np
import yaml as yaml
import pickle
import streamlit_authenticator as stauth
from pathlib import Path
st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
#------- Login
with open('security.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Iniciar sesión', 'main')
if authentication_status == None:
        st.warning("Por favor, ingresa tu usuario y contraseña")
        st.markdown('<a href="/Recuperar_contraseña" target="_self">¿Olvidaste tu contraseña?</a>', unsafe_allow_html=True)

if authentication_status == False:
        st.error("El usuario o la contraseña son incorrectos")
        st.markdown('<a href="/Recuperar_contraseña" target="_self">¿Olvidaste tu contraseña?</a>', unsafe_allow_html=True)
    
if authentication_status:

    #Sidebar + navigation
    with st.sidebar:
        st.sidebar.header("Navegación")
        st.sidebar.write("Usa los distintos enlaces para navegar por las páginas de la aplicación.")
        st.sidebar.header("Autores:")
        st.sidebar.write("Ashley Jesús Llontop")
        st.sidebar.write("Omar Jiménez Ramírez")
        authenticator.logout("Logout", "sidebar")
    
    # Opening file from file path
    st.title("Documentación")
    with open('MAPMDEMLESUP - Desarrollo del Objetivo 3 v.0.1.pdf', "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf">'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)