import streamlit as st

st.write("Willkommen, *!!!* :sunglasses:")

age = st.slider("How old are you?", 0, 130, 25)
st.write("I'm ", age, "years old")

st.secrets.database.password
st.write(st.secrets.database.password)
