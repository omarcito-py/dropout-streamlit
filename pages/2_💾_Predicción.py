import streamlit as st
import sqlite3
import yaml as yaml
from datetime import datetime
import pandas as pd
import numpy as np
import time
import pickle
import streamlit_authenticator as stauth
from pathlib import Path

pd.options.mode.chained_assignment = None

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
        
    st.title("Módulo de predicción")
    st.subheader("Carga de datos")
    st.markdown("Esta sección te permitirá cargar y visualizar un set de datos que incluya las variables de deserción y "+
                "sus respectivos valores para una serie de registros (alumnos), con el fin de identificar a" + " aquellos estudiantes que podrían estar en riesgo de deserción.")
    uploaded_file = st.file_uploader("Elegir un archivo .csv o .xlsx")
    
    if uploaded_file is not None:
        fname = uploaded_file.name
        if fname.endswith('.csv'):
            print("Se cargó el archivo")
            df = pd.read_csv(uploaded_file, sep=';')
        else:
            st.error("La extensión del archivo debe ser .csv")

    if st.button("Ejecutar"):
        if fname.endswith('.csv'):
            if uploaded_file is not None:
                my_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.05)
                    my_bar.progress(percent_complete + 1)
                feats = df.iloc[:,-36:]
                clf = pickle.load(open('finalized_model.sav', 'rb'))
                predictions = clf.predict(feats.values)
                print(type(predictions))
                df['Dropout'] = predictions
                ndf = df[['ID','Nombre','Apellido','Dropout']]
                st.dataframe(ndf)
                conn = sqlite3.connect('studentdropout.db')
                cur = conn.cursor()
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                ndf['Fecha'] = dt_string
                ndf.to_sql(name='Predictions',con=conn,if_exists='append')
            
        else:
            st.error("No se ha cargado ningún archivo con el formato solicitado.")         