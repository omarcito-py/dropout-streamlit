from queue import Empty
import streamlit as st
import pandas as pd
import sqlite3
from sklearn.inspection import permutation_importance
import time
from datetime import datetime
import numpy as np
import pickle
import yaml as yaml
import streamlit_authenticator as stauth
from pathlib import Path
from sklearn.model_selection import train_test_split as tts
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
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
        authenticator.logout('Logout', 'main')
        
    st.title("Entrenamiento del modelo")
    st.subheader("Carga de datos")
    st.markdown("Antes de poder realizar predicciones, es necesario tener un modelo entrenado. Para ello, en esta sección deberás cargar un archivo que incluya las variables de predicción y el resultado de esta serie de variables (""Deserta"" o ""No deserta"").")
    uploaded_file = st.file_uploader("Elegir un archivo .csv o .xlsx")
    
    if uploaded_file is not None:
        print("Se cargó el archivo")
        df = pd.read_csv(uploaded_file,sep=';')

    if st.button("Procesar"):
        if uploaded_file is not None:
            st.dataframe(df,height=200)
            #Obtener la última columna
            res = df.iloc[:,-1:]
            #Asignar valores a un arreglo
            labels = res['Dropout'].values[:]
            st.session_state['labels'] = labels
            #print(type(labels))

            #Todas las columnas excepto la última
            res2 = df.iloc[:,:-1]
            #Asginar valores a un arreglo
            features = res2[:].values[:]
            st.session_state['features'] = features
            
        else:
            st.error("No se ha cargado ningún archivo")
            
    st.subheader("Entrenamiento del modelo")
    st.markdown("Esta sección te entrenar el modelo de análisis predictivo teniendo como input el archivo de datos cargado. El entrenamiento se realizará con el primer set de datos de cada sesión hasta que se cargue un nuevo set de datos.")
    if st.button("Entrenar el modelo"):
        print("Entrenando")
        try:
            if st.session_state['features'] is not Empty:
                train_feats, test_feats, train_labels, test_labels = tts(st.session_state.features, st.session_state.labels, test_size=0.1)
                clf = RandomForestClassifier()
                clf.fit(train_feats, train_labels)
                predictions = clf.predict(test_feats)  
                acc = accuracy_score(test_labels, predictions)
                acc = round(acc * 100,2)
                print(acc)
                print(st.session_state.labels)
                message1 = "Se ha entrenado correctamente el modelo y logró una precisión de: " + str(acc) + "%"
                filename = 'finalized_model.sav'

                conn = sqlite3.connect('studentdropout.db')
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        
                d = {'Precision' : [acc], 'Fecha' : [dt_string]}
                trainDf = pd.DataFrame(data = d)
        
                trainDf.to_sql(name='Trainings',con=conn,if_exists='append')
                print(trainDf)
                pickle.dump(clf, open(filename, 'wb'))
                
                st.success(message1)
                
                result = permutation_importance(clf, test_feats, test_labels, n_repeats=10, random_state=42, n_jobs=2)
                st.session_state['resultados'] = result
                
            else:
                st.error("Pendiente procesamiento de archivo")
        except:
            st.error("Pendiente procesamiento de archivo")
