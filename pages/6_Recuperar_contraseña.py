from pydoc import visiblename
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

st.warning("Por favor, ingresa tu usuario")
try:
    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
    if username_forgot_pw:
        st.success('Tu nueva contraseña es: ' + random_password)
        config['credentials']['usernames'][username_forgot_pw]['password'] = stauth.Hasher([random_password]).generate()[0]
        with open("security.yaml", "w") as f:
            yaml.dump(config, f)
    elif username_forgot_pw == False:
        st.error('Username not found')
except Exception as e:
    st.error(e)
