import streamlit as st

st.write("Willkommen, *!!!* :sunglasses:")

age = st.slider("How old are you?", 0, 130, 25)
st.write("I'm ", age, "years old")

