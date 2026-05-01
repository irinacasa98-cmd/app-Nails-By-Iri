import streamlit as st
from datetime import datetime, timedelta, time
from google.oauth2 import service_account
from googleapiclient.discovery import build
import urllib.parse

# --- CONFIGURACIÓN ---
SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = "irinacasa98@gmail.com" # Cambia esto por tu mail

def get_calendar_service():
    # Creamos una copia del diccionario para poder modificarlo
    creds_dict = dict(st.secrets["google_calendar"])
    
    if "private_key" in creds_dict:
        # Aquí ya no fallará porque estamos editando la COPIA, no el secreto original
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return build('calendar', 'v3', credentials=creds)

def obtener_turnos_libres(fecha_sel):
    service = get_calendar_service()
    
    # Definir rango del día (Argentina GMT-3)
    inicio_dia = datetime.combine(fecha_sel, time(0, 0)).isoformat() + "-03:00"
    fin_dia = datetime.combine(fecha_sel, time(23, 59)).isoformat() + "-03:00"

    # Traer eventos ocupados
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=inicio_dia,
        timeMax=fin_dia,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    eventos = events_result.get('items', [])

    # Definir horarios de atención (de 10:00 a 19:00 cada 1 hora)
    horarios_posibles = [time(h, 0) for h in range(10, 19)]
    ocupados = []
    for ev in eventos:
        start = ev['start'].get('dateTime', ev['start'].get('date'))
        # Extraer solo la hora para comparar
        dt_start = datetime.fromisoformat(start.replace('Z', '-03:00'))
        ocupados.append(dt_start.time())

    # Retornar solo los que no están en la lista de ocupados
    return [h for h in horarios_posibles if h not in ocupados]

def crear_evento_google(nombre, servicio, fecha, hora):
    service = get_calendar_service()
    inicio = datetime.combine(fecha, hora)
    fin = inicio + timedelta(hours=1) # Duración de 1 hora

    evento = {
        'summary': f'Nails: {nombre} ({servicio})',
        'description': f'Reserva realizada por la App.\nServicio: {servicio}',
        'start': {'dateTime': inicio.isoformat() + "-03:00", 'timeZone': 'America/Argentina/Buenos_Aires'},
        'end': {'dateTime': fin.isoformat() + "-03:00", 'timeZone': 'America/Argentina/Buenos_Aires'},
    }
    
    service.events().insert(calendarId=calendar_id, body=evento).execute()

# --- INTERFAZ ---
st.set_page_config(page_title="Agenda Nails", page_icon="💅")
st.title("💅 Nails Art - Reserva Online")

# Paso 1: Datos básicos
nombre = st.text_input("Nombre Completo:")
servicio = st.selectbox("Servicio:", ["Semipermanente", "Kapping", "Esculpidas"])

# Paso 2: Selección de fecha
fecha_sel = st.date_input("Elegí un día:", min_value=datetime.today())

# Paso 3: Mostrar horarios disponibles dinámicamente
libres = obtener_turnos_libres(fecha_sel)

if libres:
    # Mostramos los horarios como botones o un selector limpio
    hora_sel = st.selectbox("Horarios disponibles para este día:", libres, format_func=lambda x: x.strftime("%H:%M hs"))
    
    if st.button("Confirmar Turno"):
        if not nombre:
            st.warning("Por favor, ingresá tu nombre.")
        else:
            try:
                # 1. Crear en Google Calendar
                crear_evento_google(nombre, servicio, fecha_sel, hora_sel)
                
                # 2. Preparar WhatsApp
                telefono = "5491135677912"
                msj = f"¡Hola! Reservé mi turno por la web:\n👤 *{nombre}*\n💅 *{servicio}*\n📅 *{fecha_sel.strftime('%d/%m')}*\n⏰ *{hora_sel.strftime('%H:%M')} hs*"
                url_wa = f"https://wa.me/{telefono}?text={urllib.parse.quote(msj)}"
                
                st.success("✅ ¡Turno agendado en el calendario!")
                st.markdown(f'''
                    <a href="{url_wa}" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #25D366; color: white; padding: 15px; text-align: center; border-radius: 10px; font-weight: bold; font-size: 20px;">
                            AVISAR POR WHATSAPP 📱
                        </div>
                    </a>
                ''', unsafe_allow_html=True)
                st.balloons()
            except Exception as e:
                st.error(f"Hubo un error al agendar: {e}")
else:
    st.error("❌ No hay más horarios disponibles para este día. Probá con otra fecha.")