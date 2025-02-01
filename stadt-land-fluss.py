import streamlit as st

#JSON Daten
import requests
import json

#Random String
import random
import string

#Daten abrufen
url = "https://slftool.github.io/data.json"
response = requests.get(url)
data = response.json()
#print(data)

st.title("Stadt️ - Land - Fluss - ...")
st.link_button("Daten von slftool", "https://github.com/slftool/slftool.github.io")

st.divider()

#Toggle
#st.write(st.session_state)
if "zeigen" not in st.session_state:
    st.session_state.zeigen = False
    
if "buchstabe" not in st.session_state:
    st.session_state.buchstabe = "a"
    
if "punkte" not in st.session_state:
    st.session_state.punkte = 0

def toggle():
    if st.session_state.zeigen == True:
        st.session_state.zeigen = False
    else:
        st.session_state.zeigen = True


#Auswahl der Kategorien
kategorien = ["Stadt", "Land", "Fluss", "Name", "Beruf", "Tier", "Marke", "Pflanze"]
auswahl = st.segmented_control(
    "Kategorien", kategorien, selection_mode="multi", default=["Stadt","Land","Fluss"])
st.session_state['auswahl'] = auswahl
#st.markdown(f"Auswahl: {auswahl}.")


#Überprüfen ob ausreichend Kategorien ausgewählt sind
if len(auswahl) < 3:
    st.write("Du musst mehr drei Elemente auswählen")
else:
    #Button der Zufällig einen Buchstaben auswählt
    if st.button("Wähle einen zufälligen Buchstaben!", type="primary", on_click = toggle):
        st.session_state['buchstabe'] = random.choice(string.ascii_lowercase)


if st.session_state.zeigen == True:
    
    st.markdown(f"# Der Buchstabe ist ... {st.session_state.buchstabe.upper()}")

    pruefen = []
    st.session_state.pruefen = pruefen

    #Text Inputs für Auswahl erzeugen und Eingaben in Liste speichern
    for i in range(len(auswahl)):
        eingabe = st.text_input(auswahl[i], key = i)
        pruefen.append(eingabe)

    if st.button("Überprüfen?", type="primary"):
                
        #Über alle Ausgewählten Kategorien (Stadt, Land, Fluss,..)
        for j in range(len(st.session_state.auswahl)):
            
            zaehler = 0
            
            #Über jedes Element welches in der Kategorie ist
            for k in range(len(data.get(st.session_state.buchstabe).get(st.session_state.auswahl[j].lower()))):
                #Klammer bei der json entfernen
                mitKlammer = data.get(st.session_state.buchstabe).get(st.session_state.auswahl[j].lower())[k]
                ohneKlammer = mitKlammer.split('(')[0].strip()
                
                #Eingegebene Lösung mit dem der json vergleichen
                #1 - Wenn keine Eingabe
                if st.session_state.pruefen[j].lower() == "":
                    st.error(f"{st.session_state.auswahl[j]} ohne Eingabe ...", icon="🚨")
                    break
                #2 - Wenn Eingabe korrekt
                if st.session_state.pruefen[j].lower() == ohneKlammer.lower():
                    st.success(f"{st.session_state.auswahl[j]}: {ohneKlammer} ist richtig! + 1️⃣ Punkt", icon="🔥")
                    st.session_state.punkte += 1
                else:
                #3 - Wenn Eingabe falsch    
                    #Zählt die Fehler pro Kategorie
                    zaehler = zaehler + 1
                    #Wenn Falsche == Anzahl der Einträge pro Kategorie
                    if zaehler == len(data.get(st.session_state.buchstabe).get(st.session_state.auswahl[j].lower())):
                        st.warning(f"{st.session_state.auswahl[j]}: {st.session_state.pruefen[j]} ist leider falsch..", icon="❌")

        st.info(f"Du hast: {st.session_state.punkte} Punkt(e)", icon="ℹ️")



#erste Eingabe    
#st.write(st.session_state.pruefen[0])

#Entsprechende Elemente prüfen
#st.write(data.get("a").get("stadt")[0])

#Alle Daten für den entsprechenden Buchstaben
#st.write(data.get(st.session_state.buchstabe))

#Anzahl der Ausgewählten Elementes
#st.write(len(st.session_state.auswahl))

#Anzahl der ausgewählten Kategorie
#st.write(len(data.get(st.session_state.buchstabe).get(st.session_state.auswahl[0].lower())))








