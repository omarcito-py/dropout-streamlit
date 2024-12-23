from pydoc import visiblename
from queue import Empty
from random import random
import streamlit as st
import pickle
import yaml as yaml
from pathlib import Path

import streamlit_authenticator as stauth

st.set_page_config(initial_sidebar_state="collapsed")

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
        authenticator.logout('Logout', 'main')
    #Body
    st.title("DropMonitor App") 

    st.markdown("DropMonitor es una aplicación que te permitirá predecir los casos de deserción en tu centro de estudios. Gracias a esta predicción, podrás actuar proactivamente y disminuir este índice:)")