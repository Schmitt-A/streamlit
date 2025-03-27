import streamlit as st
import requests
from urllib.parse import urlparse
from datetime import datetime

def is_valid_url(url: str) -> bool:
    """Überprüft, ob die eingegebene URL gültig ist."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def format_ical_date(date_str: str) -> str:
    """Formatiert ein iCal-Datum in deutsches Format (TT.MM.JJJJ, XX:XX Uhr)."""
    try:
        # Typisches iCal-Format: 20230325T143000Z oder 20230325T143000
        if 'T' in date_str:
            if date_str.endswith('Z'):
                dt = datetime.strptime(date_str, "%Y%m%dT%H%M%SZ")
            else:
                dt = datetime.strptime(date_str, "%Y%m%dT%H%M%S")
            return dt.strftime("%d.%m.%Y, %H:%M Uhr")
        else:
            # Für Datumsangaben ohne Uhrzeit
            dt = datetime.strptime(date_str, "%Y%m%d")
            return dt.strftime("%d.%m.%Y")
    except ValueError:
        # Falls das Format nicht erkannt wird, Originalformat zurückgeben
        return date_str

def parse_ical(ical_data: str) -> list:
    """Parst iCal-Daten und extrahiert VEVENTS als Liste von Dictionaries."""
    events = []
    lines = ical_data.splitlines()
    current_event = {}
    in_event = False

    for line in lines:
        line = line.strip()
        if line == "BEGIN:VEVENT":
            in_event = True
            current_event = {}
            continue
        if line == "END:VEVENT":
            in_event = False
            events.append(current_event)
            continue
        if in_event:
            if ":" in line:
                key, value = line.split(":", 1)
                # Nur den reinen Schlüsselnamen verwenden, falls Parameter vorhanden sind (z.B. DTSTART;TZID=...)
                key = key.split(";")[0]
                current_event[key] = value
    return events

st.title("Kalender Übersicht")

ical_url = st.text_input("iCal URL eingeben:", 
                         placeholder="https://beispiel.com/calendar.ics")

if st.button("Kalender anzeigen"):
    url_error = ""
    events = []

    if not is_valid_url(ical_url):
        url_error = "Ungültige URL."
    else:
        try:
            response = requests.get(ical_url)
            if response.status_code != 200:
                url_error = "Fehler beim Abrufen der iCal-Daten."
            else:
                ical_data = response.text
                events = parse_ical(ical_data)
        except Exception:
            url_error = "Fehler beim Abrufen der iCal-Daten."

    if url_error:
        st.error(url_error)
    else:
        if not events:
            st.write("Keine Termine gefunden.")
        else:
            # Übersichtstabelle erstellen
            st.header("Terminübersicht")
            
            # Daten für die Tabelle vorbereiten
            table_data = []
            for event in events:
                summary = event.get("SUMMARY", "Kein Titel")
                
                # Datumsformatierung für Start und Ende
                start = format_ical_date(event.get("DTSTART", ""))
                end = format_ical_date(event.get("DTEND", ""))
                
                location = event.get("LOCATION", "")
                table_data.append({"Termin": summary, "Beginn": start, "Ende": end, "Ort": location})
            
            # Tabelle anzeigen
            st.dataframe(table_data, use_container_width=True, hide_index=True)
