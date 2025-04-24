import streamlit as st
from steuerung import Ampel, Ampelsteuerung

st.set_page_config(page_title="Ampelsteuerung", page_icon="🚦")


schaltung = Ampelsteuerung()



st.title("Ampelsteuerung")

# Anzahl der Ampeln bestimmen
anzahlAmpeln = st.number_input("Wie viele Ampeln möchten Sie steuern?", min_value=1, max_value=5, value=1)

# Ampeln im Session State speichern oder laden
if "ampelListe" not in st.session_state:
    st.session_state.ampelListe = []

while len(st.session_state.ampelListe) < anzahlAmpeln:
    st.session_state.ampelListe.append(Ampel())

ampelListe = st.session_state.ampelListe

# Eine oder mehrere Ampeln auswählen
ampel_optionen = [f"Ampel {i + 1}" for i in range(anzahlAmpeln)]
ausgewaehlteAmpeln = st.multiselect(
    "Welche Ampel möchten Sie steuern?",
    options=ampel_optionen
)

auswahl = st.selectbox(
    'Was möchten Sie tun?',
    ('Ampel ausschalten', 'Ampel auf grün', 'Ampel auf rot', 'Status abfragen')
)

# Steuerung für alle ausgewählten Ampeln
for ampelnr in ausgewaehlteAmpeln:
    idx = int(ampelnr.split()[-1]) - 1
    ampel = ampelListe[idx]
    if auswahl == 'Ampel ausschalten':
        schaltung.ausschalten(ampel)
        st.write(f"{ampelnr} wurde ausgeschaltet.")
    elif auswahl == 'Ampel auf grün':
        schaltung.aufGruen(ampel)
        st.write(f"{ampelnr} wurde auf grün geschaltet.")
    elif auswahl == 'Ampel auf rot':
        schaltung.aufRot(ampel)
        st.write(f"{ampelnr} wurde auf rot geschaltet.")
    elif auswahl == 'Status abfragen':
        st.write(f"Status von {ampelnr}: {schaltung.status(ampel)}")

# Anzeige der Ampel-Widgets in den Spalten
a, b, c, d, e = st.columns(5)
spalten = [a, b, c, d, e]
for i in range(anzahlAmpeln):
    spalte = spalten[i]
    spalte.write("Ampel " + str(i+1))
    if ampelListe[i].rot:
        spalte.write("🔴")
    else:
        spalte.write("⚪️")
    if ampelListe[i].gelb:
        spalte.write("🟡")
    else:
        spalte.write("⚪️")
    if ampelListe[i].gruen:
        spalte.write("🟢")
    else:
        spalte.write("⚪️")
