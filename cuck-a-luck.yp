import streamlit as st
import random
import pandas as pd

# Titel der Anwendung
st.title("Chuck-a-Luck Spiel")

# Initialisierung des Session States
if 'guthaben' not in st.session_state:
    st.session_state.guthaben = 0
if 'spiel_started' not in st.session_state:
    st.session_state.spiel_started = False
if 'spiel_log' not in st.session_state:
    st.session_state.spiel_log = []

# Eingabe des Startguthabens (nur vor Spielstart möglich)
if not st.session_state.spiel_started:
    start_guthaben = st.number_input(
        "Geben Sie Ihr Startguthaben ein (in Cent):",
        min_value=0,
        step=1,
        value=st.session_state.guthaben
    )
    if st.button("Spiel starten"):
        st.session_state.guthaben = start_guthaben
        st.session_state.spiel_started = True
else:
    st.write(f"**Aktuelles Guthaben:** {st.session_state.guthaben} Cent")

# Spielfeld mit Zahlenauswahl (1-6) in zwei Reihen
if st.session_state.spiel_started:
    st.write("Wählen Sie eine Zahl (1-6), auf die Sie setzen möchten:")

    # Erste Zeile: Zahlen 1-3
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("1", key="1"):
            st.session_state.auswahl = 1
    with col2:
        if st.button("2", key="2"):
            st.session_state.auswahl = 2
    with col3:
        if st.button("3", key="3"):
            st.session_state.auswahl = 3

    # Zweite Zeile: Zahlen 4-6
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("4", key="4"):
            st.session_state.auswahl = 4
    with col5:
        if st.button("5", key="5"):
            st.session_state.auswahl = 5
    with col6:
        if st.button("6", key="6"):
            st.session_state.auswahl = 6

    # Anzeige der aktuellen Auswahl
    if 'auswahl' in st.session_state:
        st.write(f"Sie haben die Zahl **{st.session_state.auswahl}** ausgewählt.")
    else:
        st.write("Bitte wählen Sie eine Zahl aus.")

    # Button zum Würfeln
    if st.button("Würfeln"):
        if 'auswahl' not in st.session_state:
            st.warning("Bitte wählen Sie zuerst eine Zahl aus.")
        elif st.session_state.guthaben >= 1:
            # Altes Guthaben speichern
            altes_guthaben = st.session_state.guthaben

            # Einsatz von 1 Cent abziehen
            st.session_state.guthaben -= 1

            # Drei Würfel werfen
            wuerfel1 = random.randint(1, 6)
            wuerfel2 = random.randint(1, 6)
            wuerfel3 = random.randint(1, 6)

            # Übereinstimmungen zählen
            wuerfel_liste = [wuerfel1, wuerfel2, wuerfel3]
            uebereinstimmungen = sum(1 for w in wuerfel_liste if w == st.session_state.auswahl)

            # Gewinn berechnen: Einsatz (1 Cent) + Anzahl der Übereinstimmungen
            gewinn = 1 + uebereinstimmungen if uebereinstimmungen > 0 else 0
            st.session_state.guthaben += gewinn

            # Neue Runde zum Log hinzufügen
            runde = len(st.session_state.spiel_log) + 1
            st.session_state.spiel_log.append({
                "Runde": runde,
                "Gesetzte Zahl": st.session_state.auswahl,
                "Würfel 1": wuerfel1,
                "Würfel 2": wuerfel2,
                "Würfel 3": wuerfel3,
                "Übereinstimmungen": uebereinstimmungen,
                "Altes Guthaben": altes_guthaben,
                "Neues Guthaben": st.session_state.guthaben
            })

            # Ergebnisse anzeigen
            st.write(f"**Würfelergebnisse:** {wuerfel1}, {wuerfel2}, {wuerfel3}")
            st.write(f"**Übereinstimmungen:** {uebereinstimmungen}")
            if uebereinstimmungen > 0:
                st.success(f"Glückwunsch! Sie haben {gewinn} Cent gewonnen.")
            else:
                st.error("Keine Übereinstimmungen. Sie haben Ihren Einsatz von 1 Cent verloren.")
            st.write(f"**Neues Guthaben:** {st.session_state.guthaben} Cent")
        else:
            st.warning("Nicht genug Guthaben, um zu spielen.")

    # Spiel-Log als Tabelle anzeigen
    if st.session_state.spiel_log:
        df = pd.DataFrame(st.session_state.spiel_log)
        st.write("**Spiel-Log:**")
        st.dataframe(df)
