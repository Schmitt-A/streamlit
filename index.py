import streamlit as st

st.write("Willkommen, *!!!* :sunglasses:")

age = st.slider("How old are you?", 0, 130, 25)
st.write("I'm ", age, "years 0ld")


st.write(st.secrets.database.password)
st.write(st.secrets.OpenAI_key)
st.write(st.secrets.benutzer)


user = st.text_input("Benutzername", "")

if user == st.secrets.benutzer:
    st.write("Angemeldet!")
else:
    st.write("Abgemeldet")