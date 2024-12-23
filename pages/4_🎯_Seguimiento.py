import streamlit as st
import sqlite3
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
        
    st.title("Módulo de seguimiento")
    st.write("En esta sección podrás consultar los resultados de un alumno que haya sido parte de las ejecuciones del modelo. Para consultar, escribe el ID del alumno en el siguiente cuadro:")
    code = st.text_input("Código de alumno")
    if st.button("Consultar"):
        if code == "":
            st.warning("Ingresa un código de alumno")
        else:
            conn = sqlite3.connect('studentdropout.db')
            # cur = conn.cursor()
            # cur.execute('''SELECT * FROM Predictions WHERE ID = ?''', (code,))
            
            # rows = cur.fetchall()
            # print(rows)
            sql_query = pd.read_sql_query ('''SELECT * FROM Predictions''', conn)
            df = pd.DataFrame(sql_query)
            newdf = df.loc[(df.ID == code)]
            print (newdf)
            col1, col2 = st.columns(2)
            if newdf.shape[0] != 0:
                col1.subheader("Se han realizado " + str(newdf.shape[0]) + " predicciones para el alumno con código: " + code)
                col2.dataframe(newdf)
            else:
                st.warning("Este código de alumno no ha sido encontrado")
            