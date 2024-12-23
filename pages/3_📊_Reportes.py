from queue import Empty
from sys import stderr
import streamlit as st
import pandas as pd
import time
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import sqlite3
import yaml as yaml
from datetime import datetime
import numpy as np
import pickle
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
        authenticator.logout("Logout", "sidebar")
    conn = sqlite3.connect('studentdropout.db')
    st.title("Módulo de reportería")
    st.subheader("Última ejecución del modelo")
    st.write("Se presentan los resultados de la ejecución más reciente del modelo")
    cl1, cl2 = st.columns(2)
    qry = pd.read_sql_query('''SELECT * FROM Trainings order by substr (fecha,7,4) || substr(Fecha,4,2) || substr(Fecha,1,2) || substr(Fecha,12,2) || substr(Fecha,15,2) DESC LIMIT 1''', conn)
    df2 = pd.DataFrame(qry)
    pre = df2['Precision'].max()
    pre = round(pre, 2)
    txt = str(pre)
    fech = df2['Fecha'].max()
    cl1.metric("Precision lograda", txt+"%")
    cl2.metric("Fecha del último entrenamiento", fech)
    print(df2)
    st.subheader("Data visualization")
    st.markdown("Esta sección te permitirá consultar las últimas ejecuciones del modelo de predicción, así como los resultados de precisión y eficiencia")
    col1, col2, col3 = st.columns(3)
    
    sql_query = pd.read_sql_query ('''SELECT * FROM Trainings''', conn)
    df = pd.DataFrame(sql_query)

    max1 = df['Precision'].max()
    avg = df['Precision'].mean()
    avg = round(avg , 2)
    
    dif = max1 - avg
    dif = round(dif , 2)
    str1 = str(dif)+"% más que el promedio"
    
    n = df.shape[0]
    str2 = "A partir de " + str(n) + " entrenamientos"
    
    col1.metric("Precision máxima", str(max1)+"%", str1)
    col2.metric("Precisión promedio", str(avg)+"%", str2, delta_color="off")
    
    sql_query2 = pd.read_sql_query ('''SELECT * FROM Predictions''', conn)
    df2 = pd.DataFrame(sql_query2)
    
    nb = df2.shape[0]
    nb2 = df2['ID'].nunique()
    str3 = "Para un total de " + str(nb2) + " alumnos"
    
    col3.metric("Predicciones realizadas", nb, str3, delta_color="off")
    st.markdown("")
    
    try:
        result = st.session_state['resultados']
        forest_importances = pd.Series(result.importances_mean , index=['Marital status','Application mode','Application order','Course','Daytime/evening attendance','Previous qualification','Previous qualification (grade)','Nacionality','''Mother's qualification''','''Father's qualification''','''Mother's occupation''','''Father's occupation''','Admission grade','Displaced','Educational special needs','Debtor','Tuition fees up to date','Gender','Scholarship holder','Age at enrollment','International','Curricular units 1st sem (credited)','Curricular units 1st sem (enrolled)','Curricular units 1st sem (evaluations)','Curricular units 1st sem (approved)','Curricular units 1st sem (grade)','Curricular units 1st sem (without evaluations)','Curricular units 2nd sem (credited)','Curricular units 2nd sem (enrolled)','Curricular units 2nd sem (evaluations)','Curricular units 2nd sem (approved)','Curricular units 2nd sem (grade)','Curricular units 2nd sem (without evaluations)','Unemployment rate','Inflation rate','GDP'])
        fig, ax = plt.subplots()
        forest_importances.plot.bar(y=result.importances_std, ax=ax)
        st.pyplot(fig)
        
    except Exception as e:
        st.warning("Para mostrar gráficas de análisis estadístico de variables, debes ejecutar un Entrenamiento en la sesión vigente.")