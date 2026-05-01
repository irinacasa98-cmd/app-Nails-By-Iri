import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta, time
from google.oauth2 import service_account
from googleapiclient.discovery import build
import urllib.parse

# --- CONFIGURACIÓN DE GOOGLE ---
SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = "irinacasa98@gmail.com"

def get_calendar_service():
    creds_dict = dict(st.secrets["google_calendar"])
    if "private_key" in creds_dict:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return build('calendar', 'v3', credentials=creds)

def obtener_eventos_calendario():
    service = get_calendar_service()
    # Traemos eventos desde hoy hasta 15 días adelante
    ahora = datetime.utcnow().isoformat() + 'Z'
    limite = (datetime.utcnow() + timedelta(days=15)).isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=ahora,
        timeMax=limite,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    eventos = events_result.get('items', [])
    cal_events = []
    for ev in eventos:
        cal_events.append({
            "title": "Ocupado",
            "start": ev['start'].get('dateTime'),
            "end": ev['end'].get('dateTime'),
            "color": "#FF6B6B" # Rojo para ocupado
        })
    return cal_events

def crear_evento_google(nombre, servicio, inicio_iso):
    service = get_calendar_service()
    # Calculamos el fin (1 hora después)
    inicio_dt = datetime.fromisoformat(inicio_iso.replace('Z', ''))
    fin_dt = inicio_dt + timedelta(hours=1)
    
    evento = {
        'summary': f'Nails: {nombre} ({servicio})',
        'start': {'dateTime': inicio_iso, 'timeZone': 'America/Argentina/Buenos_Aires'},
        'end': {'dateTime': fin_dt.isoformat(), 'timeZone': 'America/Argentina/Buenos_Aires'},
    }
    service.events().insert(calendarId=calendar_id, body=evento).execute()

# --- INTERFAZ ---
st.set_page_config(page_title="Agenda Nails", layout="wide")

st.title("💅 Nails Art - Agenda de Turnos")
st.write("Toca un espacio vacío en el calendario para elegir tu horario.")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Tus Datos")
    nombre = st.text_input("Nombre Completo:")
    servicio = st.selectbox("Servicio:", ["Semipermanente", "Kapping", "Esculpidas"])

with col2:
    # Configuramos el calendario visual
    opciones_calendario = {
        "initialView": "timeGridWeek",
        "slotMinTime": "10:00:00",
        "slotMaxTime": "20:00:00",
        "allDaySlot": False,
        "locale": "es",
        "selectable": True,
    }
    
    # Obtenemos eventos de Google para mostrarlos
    eventos_google = obtener_eventos_calendario()
    
    # Renderizar el calendario
    cal = calendar(events=eventos_google, options=opciones_calendario, key="calendar")

    # Si el usuario selecciona un rango de tiempo en el calendario
    if cal.get("select"):
        inicio_seleccionado = cal["select"]["start"]
        fecha_dt = datetime.fromisoformat(inicio_seleccionado.replace('Z', ''))
        
        st.info(f"Seleccionaste: {fecha_dt.strftime('%d/%m a las %H:%M hs')}")
        
        if st.button("AGENDAR ESTE TURNO"):
            if not nombre:
                st.error("Ingresá tu nombre primero.")
            else:
                with st.spinner("Guardando en agenda..."):
                    try:
                        crear_evento_google(nombre, servicio, inicio_seleccionado)
                        
                        # WhatsApp
                        tel = "5491135677912"
                        msj = f"¡Hola! Reservé mi turno:\n👤 *{nombre}*\n💅 *{servicio}*\n📅 *{fecha_dt.strftime('%d/%m')}*\n⏰ *{fecha_dt.strftime('%H:%M')} hs*"
                        url = f"https://wa.me/{tel}?text={urllib.parse.quote(msj)}"
                        
                        st.success("¡Turno confirmado!")
                        st.markdown(f'[📱 Enviar comprobante por WhatsApp]({url})')
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error: {e}")

# ... (mantener lo anterior)

with col2:
    st.markdown("### 🗓️ Paso 2: Toca un horario libre en la grilla")
    
    opciones_calendario = {
        "initialView": "timeGridWeek",
        "slotMinTime": "10:00:00",
        "slotMaxTime": "20:00:00",
        "allDaySlot": False,
        "locale": "es",
        "selectable": True,
        "contentHeight": "auto",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "timeGridWeek,timeGridDay",
        },
    }
    
    eventos_google = obtener_eventos_calendario()
    
    # Renderizar el calendario
    cal = calendar(events=eventos_google, options=opciones_calendario, key="calendar_v2")

    # --- NUEVA LÓGICA DE CAPTURA ---
    # Verificamos si hay una selección activa en el calendario
    if cal.get("callback") == "select" or cal.get("select"):
        # Dependiendo de la versión, la info viene en 'select' o en 'callback'
        seleccion = cal.get("select") or cal.get("callback")
        
        inicio_iso = seleccion.get("start")
        
        if inicio_iso:
            # Convertimos la fecha para mostrarla amigablemente
            fecha_dt = datetime.fromisoformat(inicio_iso.replace('Z', ''))
            
            st.success(f"📍 **Horario elegido:** {fecha_dt.strftime('%A %d de %B a las %H:%M hs')}")
            
            if st.button("CONFIRMAR TURNO AHORA", type="primary", use_container_width=True):
                if not nombre:
                    st.error("⚠️ Por favor, ingresá tu nombre arriba antes de confirmar.")
                else:
                    with st.spinner("Agendando..."):
                        try:
                            crear_evento_google(nombre, servicio, inicio_iso)
                            
                            tel = "5491135677912"
                            msj = f"¡Hola! Reservé mi turno:\n👤 *{nombre}*\n💅 *{servicio}*\n📅 *{fecha_dt.strftime('%d/%m')}*\n⏰ *{fecha_dt.strftime('%H:%M')} hs*"
                            url = f"https://wa.me/{tel}?text={urllib.parse.quote(msj)}"
                            
                            st.balloons()
                            st.info("✅ Turno guardado. ¡No olvides avisar por WhatsApp!")
                            st.markdown(f'''
                                <a href="{url}" target="_blank" style="text-decoration: none;">
                                    <div style="background-color: #25D366; color: white; padding: 20px; text-align: center; border-radius: 10px; font-weight: bold; font-size: 18px;">
                                        ENVIAR COMPROBANTE POR WHATSAPP 📱
                                    </div>
                                </a>
                            ''', unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Hubo un error: {e}")
    else:
        st.info("💡 Tip: Haz clic o arrastra sobre los espacios en blanco del calendario para elegir tu hora.")