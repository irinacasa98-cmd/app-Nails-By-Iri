import streamlit as st
from datetime import datetime, timedelta, time
from google.oauth2 import service_account
from googleapiclient.discovery import build
import urllib.parse

# --- CONFIGURACIÓN ---
CALENDAR_ID = "irinacasa98@gmail.com" 
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds_dict = dict(st.secrets["google_calendar"])
    if "private_key" in creds_dict:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return build('calendar', 'v3', credentials=creds)

def obtener_disponibilidad_estricta(fecha_sel):
    service = get_calendar_service()
    tz = "-03:00"
    
    # Consultamos el día completo
    inicio_dia = datetime.combine(fecha_sel, time(0, 0)).isoformat() + tz
    fin_dia = datetime.combine(fecha_sel, time(23, 59)).isoformat() + tz

    # LEER EVENTOS REALES
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=inicio_dia,
        timeMax=fin_dia,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    ocupados = events_result.get('items', [])
    
    # Definimos los inicios de tus turnos según tu imagen (8:00, 10:30, 13:00, 15:30)
    # Esto asegura que coincida con tu esquema de 150 min
    horarios_fijos = [time(8, 0), time(10, 30), time(13, 0), time(15, 30)]
    libres = []
    
    duracion = timedelta(minutes=150)

    for h_inicio in horarios_fijos:
        bloque_inicio = datetime.combine(fecha_sel, h_inicio)
        bloque_fin = bloque_inicio + duracion
        
        choque = False
        for ev in ocupados:
            ev_start_raw = ev['start'].get('dateTime')
            ev_end_raw = ev['end'].get('dateTime')
            
            if ev_start_raw and ev_end_raw:
                ev_start = datetime.fromisoformat(ev_start_raw.replace('Z', tz)[:19])
                ev_end = datetime.fromisoformat(ev_end_raw.replace('Z', tz)[:19])
                
                # Si hay solapamiento
                if not (bloque_fin <= ev_start or bloque_inicio >= ev_end):
                    choque = True
                    break
        
        if not choque:
            libres.append(h_inicio)
            
    return libres

# --- INTERFAZ ---
st.title("💅 Turnos - Nails by Irina")

nombre = st.text_input("Nombre Completo:")
servicios = {"Semipermanente": 16000, "Kapping": 20000, "Esculpidas": 30000}
seleccion = st.selectbox("¿Qué servicio te vas a hacer?", [f"{s} (${p:,})" for s, p in servicios.items()])

fecha_sel = st.date_input("Elegí el día:", min_value=datetime.today())

st.subheader("⏰ Horarios Disponibles")

try:
    turnos = obtener_disponibilidad_estricta(fecha_sel)
    
    if turnos:
        cols = st.columns(2)
        for i, t in enumerate(turnos):
            with cols[i % 2]:
                if st.button(t.strftime("%H:%M hs"), use_container_width=True):
                    if not nombre:
                        st.error("Escribí tu nombre")
                    else:
                        # Aquí iría la función de agendar_en_google y el botón de WhatsApp
                        st.success(f"Turno seleccionado: {t.strftime('%H:%M')}")
                        # (Agrega aquí la lógica de agendar y WhatsApp del mensaje anterior)
    else:
        st.warning("No hay turnos disponibles para este día.")
except Exception as e:
    st.error(f"Error de acceso: Asegurate de dar permiso de 'Realizar cambios' en Google Calendar a la Service Account.")