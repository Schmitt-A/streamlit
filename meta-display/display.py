import streamlit as st
import pandas as pd
import requests
#import openpyxl
#import random

# Meta-Media-URL
meta_media_url = "https://vr3.gfg-woerrstadt.de/meta-media/"

# CSV-Daten laden
#data = pd.read_excel("https://github.com/Schmitt-A/streamlit/raw/refs/heads/main/meta-display/vr-data.xlsx")
data = pd.read_csv("https://github.com/Schmitt-A/streamlit/raw/refs/heads/main/meta-display/vr-data.csv", sep=";")
#st.dataframe(data)

# Initialisiere Session State Keys
if "selected_game" not in st.session_state:
    game_titles = list(data["Name"].dropna())
    #st.session_state.selected_game = random.choice(game_titles)
    st.session_state.selected_game = "Gravity Sketch"

if "selected_fach" not in st.session_state:
    st.session_state.selected_fach = ""

if "expander_key" not in st.session_state:
    st.session_state.expander_key = 0

# Callback-Funktionen, die den jeweils anderen Wert zurücksetzen
def game_changed():
    st.session_state.selected_fach = ""
    st.session_state.expander_key += 1  # Erzwingt das Zurücksetzen des Expanders

def fach_changed():
    st.session_state.selected_game = ""
    st.session_state.expander_key += 1  # Erzwingt das Zurücksetzen des Expanders

# Funktion zum Überprüfen der Bild-URL und Rückgabe eines Platzhalters, falls ungültig
def get_valid_image_url(url, placeholder=f"{meta_media_url}platzhalter.jpg"):
    try:
        response = requests.head(url)
        if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
            return url
    except Exception:
        pass
    return placeholder

def schlagwort_changed():
    # Wenn mindestens ein Stichwort ausgewählt wurde, werden andere Filter zurückgesetzt
    if st.session_state.get("selected_schlagwort", []):
        st.session_state.selected_game = ""
        st.session_state.selected_fach = ""



st.image("https://medienbildung-mainz.bildung-rp.de/wp-content/uploads/2020/12/mbmz-header-700x200-1.png", width=200)
st.header("Meta Quest im Unterricht")


# Funktion für den gemeinsamen Layout-Code
def display_app_layout(data):
    st.subheader(data.get("Name", "Kein Titel"))
    
    o1, o2 = st.columns(2)
    
    img_url = meta_media_url + str(data.get("ID", "")) + ".jpg"
    valid_img_url = get_valid_image_url(img_url)
    o1.image(valid_img_url, caption=f"Quelle: [Meta Store]({data.get('Meta_Store','')}) / [Entwickler]({data.get('Entwickler','')})")
    
    o2.markdown(f"**Beschreibung** {data.get('Beschreibung','')}")
    #o2.link_button("📼 Trailer", str(data.get("Video", "")), use_container_width=True, type="secondary")        
    f1, f2 = st.columns(2)
    f1.markdown(f"<div style='font-size:20px'><b>Unterricht</b><br>{data.get('Fach','')}</div>", unsafe_allow_html=True)
    f2.markdown(f"<div style='font-size:20px'><b>Stichpunkte</b><br>{data.get('Schlagworte','')}</div>", unsafe_allow_html=True)
    
    st.write("")
    with st.expander("Weitere Informationen" + "\u200b" * st.session_state.expander_key, expanded=False):

        a, b, c, d = st.columns(4)
        a.metric("USK", f"{data.get('USK','')}", border=True)
        b.metric("Klassenstufe", f"{data.get('Klasse','')}", border=True)
        c.metric("Kosten", f"{data.get('Preis','')}", border=True)
        d.metric("Internet", f"{data.get('Internet','')}", border=True)
    
        st.caption("Sprachen")
        st.write(data.get("Sprache", ""))
    
        st.header("Didaktische Hinweise")
        if not pd.isna(data.get('Didaktischer_Hinweis_1', '')):    
            st.write(data.get('Didaktischer_Hinweis_1',''))
        if not pd.isna(data.get('Didaktischer_Hinweis_2', '')):
            st.write(data.get('Didaktischer_Hinweis_2',''))
        if not pd.isna(data.get('Didaktischer_Hinweis_3', '')):
            st.write(data.get('Didaktischer_Hinweis_3',''))

        st.header("Kompetenzen")
        st.write(data.get('Medienkompetenz_1',''))
        st.write(data.get('Medienkompetenz_2',''))
        st.write(data.get('Medienkompetenz_3',''))
        
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
        
        #st.markdown(f"<div style='font-size:20px'><b>Plattform</b><br>{data.get('Plattform','')}</div>", unsafe_allow_html=True)
        plattforms = [data.get('Plattform')]
        plattforms = [p.strip() for p in data.get('Plattform', '').split(',')]
        st.pills("Plattformen", plattforms, selection_mode="single", key=data.get('ID',''))
        
        st.divider()
        
        update_date = data.get('Erfassungsdatum', '')
        if pd.notnull(update_date) and hasattr(update_date, 'strftime'):
            update_date = update_date.strftime('%Y-%m-%d')
        st.write(f"Aktualisiert: {update_date}")
        
        st.write(f"ID: {data.get('ID','')}")
    st.divider()




f1, f2 = st.columns(2)

# Spiele auswählen (Optionen-Liste um ein leeres Element erweitern)
spiel_titel = [""] + list(data["Name"].dropna())
selected_game = f1.selectbox(
    "Anwendung", 
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
    "Fach",
    unterricht_list, 
    key="selected_fach", 
    on_change=fach_changed,
)




# Schlagwörter extrahieren, dabei Komma-getrennte Werte aufsplitten, sortieren und ein leeres Element hinzufügen
schlagworte_list = data["Schlagworte"].dropna() \
    .apply(lambda x: [s.strip() for s in x.split(",")]).explode().unique()
schlagworte_list = sorted(schlagworte_list)
schlagworte_list = [""] + list(schlagworte_list)

selected_schlagwort = st.multiselect(
    "Stichwortfilter",
    placeholder="Experiment, Design, ...",
    options=schlagworte_list,
    default=[],
    key="selected_schlagwort",
    on_change=schlagwort_changed
)

if st.session_state.selected_game != "":
    selected_row = data[data["Name"] == st.session_state.selected_game].squeeze()
    if not selected_row.empty:
        display_app_layout(selected_row.to_dict())
elif st.session_state.selected_fach != "":
    selected_rows = data[data["Fach"].str.contains(st.session_state.selected_fach, na=False)]
    for index, row in selected_rows.iterrows():
        display_app_layout(row.to_dict())
elif st.session_state.selected_schlagwort:
    def contains_any(value):
        return any(sel in value for sel in st.session_state.selected_schlagwort)
    selected_rows = data[data["Schlagworte"].dropna().apply(contains_any)]
    for index, row in selected_rows.iterrows():
        display_app_layout(row.to_dict())


   
# Kontaktinformationen
inf1, inf2, inf3 = st.columns(3)

inf1.write("Pädagogische Beratung:")
inf1.link_button(
    "Harald Jacob",
    "mailto:harald.jacob@pl.rlp.de?subject=VR%20Einsatz%20im%20Unterricht",
    use_container_width=True,
    type="secondary",
    icon="📧"
)
inf2.markdown("<span style='color:transparent'>.</span>", unsafe_allow_html=True)
inf2.link_button(
    "Andreas Schmitt",
    "mailto:andreas.schmitt@pl.rlp.de?subject=VR%20Einsatz%20im%20Unterricht",
    use_container_width=True,
    type="secondary",
    icon="📧"
)

inf3.write("Technische Beratung:")

inf3.link_button(
    "Timo Keller",
    "mailto:timo.keller@pl.rlp.de?subject=VR%20Einsatz%20im%20Unterricht",
    use_container_width=True,
    type="secondary",
    icon="📧"
)
