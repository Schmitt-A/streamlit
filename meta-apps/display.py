import streamlit as st
import pandas as pd
import openpyxl
import random

# CSV-Daten laden
data = pd.read_excel("vr-data.xlsx")
#st.dataframe(data)

# Initialisiere Session State Keys
if "selected_game" not in st.session_state:
    game_titles = list(data["Name"].dropna())
    st.session_state.selected_game = random.choice(game_titles)
if "selected_fach" not in st.session_state:
    st.session_state.selected_fach = ""

# Callback-Funktionen, die den jeweils anderen Wert zurücksetzen
def game_changed():
    st.session_state.selected_fach = ""

def fach_changed():
    st.session_state.selected_game = ""

spalten = [
    "ID",
    "Quelle",
    "Erfassungsdatum",
    "Video",
    "Bild",
    "Name",
    "USK",
    "Preis",
    "In-App-Kaeufe",
    "Sprache",
    "Internet",
    "Beschreibung",
    "Schlagworte",
    "Fach",
    "Klasse",
    "Didaktischer_Hinweis_1",
    "Didaktischer_Hinweis_2",
    "Didaktischer_Hinweis_3",
    "Kompetenzen",
    "Bildungsportal",
    "Kategorie",
    "Nutzungshinweise",
    "Komfort",
    "Triggerwarnung",
    "Tiggerhinweise",
    "KMZ1",
    "KMZ2",
    "KMZ3",
    "Meta_Store",
    "Entwickler",
    "Speicherbedarf",
    "Spielermodus",
    "Plattform"
]


# Funktion für den gemeinsamen Layout-Code
def display_app_layout(data):
    st.title(data.get("Name", "Kein Titel"))
    
    o1, o2 = st.columns(2)
    o1.image(data.get("Bild", ""), caption=f"Quelle: [Meta Store]({data.get('Meta_Store','')}) / [Entwickler]({data.get('Entwickler','')})")
    o2.markdown(f"**Beschreibung** {data.get('Beschreibung','')}")
    o2.link_button("📼 Trailer", str(data.get("Video", "")), use_container_width=True, type="secondary")        
    f1, f2 = st.columns(2)
    f1.markdown(f"<div style='font-size:20px'><b>Unterricht</b><br>{data.get('Fach','')}</div>", unsafe_allow_html=True)
    f2.markdown(f"<div style='font-size:20px'><b>Stichpunkte</b><br>{data.get('Schlagworte','')}</div>", unsafe_allow_html=True)
    
    st.write("")
    with st.expander("Weitere Informationen"):
        a, b, c, d = st.columns(4)
        a.metric("USK", f"{data.get('USK','')}", border=True)
        b.metric("Klassenstufe", f"{data.get('Klasse','')}", border=True)
        c.metric("Kosten", f"{data.get('Preis','')}", border=True)
        d.metric("Internet", f"{data.get('Internet','')}", border=True)
    
        st.caption("Sprachen")
        st.write(data.get("Sprache", ""))
    
        st.header("Didaktische Hinweise")    
        st.write(data.get('Didaktischer_Hinweis_1',''))
        st.write(data.get('Didaktischer_Hinweis_2',''))
        st.write(data.get('Didaktischer_Hinweis_3',''))

        # Ersetze im display_app_layout den betreffenden Abschnitt:
        st.header("Kompetenzen")
        st.write(data.get('Kompetenzen',''))
        url = data.get('Bildungsportal', '')
        if pd.isnull(url) or url == "":
            st.error("Keine weiteren Materialien im Bildungsportal RLP")
        else:
            st.link_button("Weitere Materialien im Bildungsportal RLP", str(url), use_container_width=True, type="primary")
        
        st.divider()
        st.header("Beratung und Verleih")
        
        
        kmz1, kmz2, kmz3 = st.columns(3)
        if not pd.isna(data.get('KMZ1', '')):
            kmz1.link_button(str(data.get('KMZ1', '')), "https://streamlit.io/gallery", use_container_width=True)
        if not pd.isna(data.get('KMZ2', '')):
            kmz2.link_button(str(data.get('KMZ2', '')), "https://streamlit.io/gallery", use_container_width=True)
        if not pd.isna(data.get('KMZ3', '')):
            kmz3.link_button(str(data.get('KMZ3', '')), "https://streamlit.io/gallery", use_container_width=True)
        
        st.divider()
        st.header("Nutzungshinweise")
        st.metric("Platzbedarf", data.get("Nutzungshinweise", ""), border=True)
    
        n1, n2, n3 = st.columns(3)
        n1.metric("In-App-Käufe", f"{data.get('In-App-Kaeufe','')}", border=True)
        n2.metric("Speicherplatz", f"{data.get('Speicherbedarf','')}", border=True)
        n3.metric("Quelle", f"{data.get('Quelle','')}", border=True)
    
        a1, b1 = st.columns(2)
        a1.metric("Komfort", f"{data.get('Komfort','')}", border=True)
        b1.metric("Triggerwarnung", f"{data.get('Triggerwarnung','')}", border=True)
        
        trigger_text = data.get("Tiggerhinweise", "")
        if pd.notna(trigger_text) and trigger_text != "":
            st.write(trigger_text)
        else:
            st.success("Keine sonstigen Anmerkungen.") 
        
        st.markdown(f"<div style='font-size:20px'><b>Plattform</b><br>{data.get('Plattform','')}</div>", unsafe_allow_html=True)

        st.divider()
        
        update_date = data.get('Erfassungsdatum', '')
        if pd.notnull(update_date) and hasattr(update_date, 'strftime'):
            update_date = update_date.strftime('%Y-%m-%d')
        st.write(f"Aktualisiert: {update_date}")
        
        st.write(f"ID: {data.get('ID','')}")




f1, f2 = st.columns(2)

# Spiele auswählen (Optionen-Liste um ein leeres Element erweitern)
spiel_titel = [""] + list(data["Name"].dropna())
selected_game = f1.selectbox(
    "Spiele", 
    spiel_titel, 
    key="selected_game", 
    on_change=game_changed
)

# Fächer auswählen (Optionen-Liste um ein leeres Element erweitern)
unterricht_strings = data["Fach"].dropna()  # NaN-Werte ignorieren
unterricht_list = [fach.strip() for unterricht in unterricht_strings for fach in unterricht.split(",")]
unterricht_list = sorted(set(unterricht_list))
unterricht_list = [""] + unterricht_list
selected_fach = f2.selectbox(
    "Fächer", 
    unterricht_list, 
    key="selected_fach", 
    on_change=fach_changed
)

if st.session_state.selected_game != "":
    selected_row = data[data["Name"] == st.session_state.selected_game].squeeze()
    if not selected_row.empty:
        display_app_layout(selected_row.to_dict())
elif st.session_state.selected_fach != "":
    selected_rows = data[data["Fach"].str.contains(st.session_state.selected_fach, na=False)]
    # Ausgabe aller Spiele, die zu dem ausgewählten Fach passen:
    for index, row in selected_rows.iterrows():
        display_app_layout(row.to_dict())
        
# An einer passenden Stelle im Code (z. B. am Ende der Seite) hinzufügen:
st.link_button(
    "E-Mail senden",
    "mailto:beispiel@domain.de?subject=Dein%20Betreff",
    use_container_width=True,
    type="primary"
)
