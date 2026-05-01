import streamlit as st
from datetime import datetime, timedelta, time
from google.oauth2 import service_account
from googleapiclient.discovery import build
import urllib.parse

# --- CONFIGURACIÓN CRÍTICA ---
# Asegúrate de que este sea tu Gmail personal donde tienes los turnos
CALENDAR_ID = "irinacasa98@gmail.com" 
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Conecta con la API de Google usando los Secrets de Streamlit."""
    creds_dict = dict(st.secrets["google_calendar"])
    if "private_key" in creds_dict:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return build('calendar', 'v3', credentials=creds)

def obtener_disponibilidad_real(fecha_sel):
    """Lee el calendario y devuelve solo los huecos de 2.5hs libres."""
    service = get_calendar_service()
    
    # Rango del día en Argentina (GMT-3)
    tz = "-03:00"
    inicio_dia = datetime.combine(fecha_sel, time(0, 0)).isoformat() + tz
    fin_dia = datetime.combine(fecha_sel, time(23, 59)).isoformat() + tz

    # Pedimos la lista de eventos ocupados a Google
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=inicio_dia,
        timeMax=fin_dia,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    eventos_ocupados = events_result.get('items', [])
    
    slots_libres = []
    duracion_turno = timedelta(hours=2, minutes=30)
    
    # Tu horario de atención (ajustable)
    hora_inicio_lab = time(10, 0)
    hora_fin_lab = time(20, 0)
    
    actual = datetime.combine(fecha_sel, hora_inicio_lab)
    cierre = datetime.combine(fecha_sel, hora_fin_lab)

    while actual + duracion_turno <= cierre:
        bloque_inicio = actual
        bloque_fin = actual + duracion_turno
        
        es_valido = True
        for ev in eventos_ocupados:
            # Ignorar eventos de "Todo el día" que no tienen dateTime
            ev_start_raw = ev['start'].get('dateTime')
            ev_end_raw = ev['end'].get('dateTime')
            
            if ev_start_raw and ev_end_raw:
                # Normalizamos horarios para comparar
                ev_start = datetime.fromisoformat(ev_start_raw.replace('Z', tz)[:19])
                ev_end = datetime.fromisoformat(ev_end_raw.replace('Z', tz)[:19])
                
                # Si el bloque de 2.5hs se solapa con un evento ocupado, no es válido
                if not (bloque_fin <= ev_start or bloque_inicio >= ev_end):
                    es_valido = False
                    break
        
        if es_valido:
            slots_libres.append(actual.time())
        
        # Saltos de 30 minutos para ofrecer opciones de inicio
        actual += timedelta(minutes=30)
        
    return slots_libres

def agendar_en_google(nombre, servicio, precio, fecha, hora):
    """Inyecta el evento directamente en tu Google Calendar."""
    service = get_calendar_service()
    inicio = datetime.combine(fecha, hora)
    fin = inicio + timedelta(hours=2, minutes=30)
    
    evento = {
        'summary': f'Nails: {nombre} ({servicio})',
        'description': f'Servicio: {servicio}\nPrecio: {precio}\nReserva desde App Streamlit.',
        'start': {'dateTime': inicio.isoformat() + "-03:00", 'timeZone': 'America/Argentina/Buenos_Aires'},
        'end': {'dateTime': fin.isoformat() + "-03:00", 'timeZone': 'America/Argentina/Buenos_Aires'},
    }
    service.events().insert(calendarId=CALENDAR_ID, body=evento).execute()

# --- INTERFAZ DE USUARIO ---
st.set_page_config(page_title="Turnos Nails by Iri", page_icon="💅")

st.title("💅 Nails Art - Reserva de Turnos")
st.write("Seleccioná tu servicio y buscá un horario disponible.")

# 1. Selección de Servicio y Precios
nombre = st.text_input("Nombre Completo:")

servicios = {
    "Semipermanente": 16000,
    "Kapping": 20000,
    "Esculpidas": 30000
}

# Formateamos las opciones para que el cliente vea el precio
opciones_servicio = [f"{s} (${p:,})" for s, p in servicios.items()]
seleccion = st.selectbox("¿Qué servicio te vas a hacer?", opciones_servicio)

# Extraer nombre del servicio y precio para el mensaje
servicio_limpio = seleccion.split(" (")[0]
precio_limpio = seleccion.split(" (")[1].replace(")", "")

# 2. Fecha
fecha_sel = st.date_input("Elegí el día:", min_value=datetime.today())

# 3. Horarios
st.subheader("⏰ Horarios Disponibles")
st.caption("Los turnos tienen una duración de 2.5 horas.")

with st.spinner("Consultando agenda real..."):
    try:
        libres = obtener_disponibilidad_real(fecha_sel)
        
        if libres:
            cols = st.columns(4)
            for i, h in enumerate(libres):
                with cols[i % 4]:
                    if st.button(h.strftime("%H:%M"), key=f"btn_{h}", use_container_width=True):
                        if not nombre:
                            st.error("⚠️ Por favor, ingresá tu nombre.")
                        else:
                            with st.spinner("Agendando..."):
                                agendar_en_google(nombre, servicio_limpio, precio_limpio, fecha_sel, h)
                                
                                # Preparar WhatsApp
                                tel = "5491135677912"
                                msj = (f"¡Hola! Reservé mi turno:\n"
                                       f"👤 *{nombre}*\n"
                                       f"💅 *{servicio_limpio}*\n"
                                       f"💰 *{precio_limpio}*\n"
                                       f"📅 *{fecha_sel.strftime('%d/%m')}*\n"
                                       f"⏰ *{h.strftime('%H:%M')} hs*\n\n"
                                       f"Adjunto el comprobante de pago:")
                                
                                url_wa = f"https://wa.me/{tel}?text={urllib.parse.quote(msj)}"
                                
                                st.success("✅ ¡Turno agendado!")
                                st.balloons()
                                
                                st.markdown(f'''
                                    <a href="{url_wa}" target="_blank" style="text-decoration:none;">
                                        <div style="background-color:#25D366; color:white; padding:20px; border-radius:10px; font-weight:bold; text-align:center; font-size:18px;">
                                            ENVIAR COMPROBANTE POR WHATSAPP 📱
                                        </div>
                                    </a>
                                ''', unsafe_allow_html=True)
        else:
            st.warning("No hay bloques de 2.5hs disponibles para este día.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        st.info("Asegúrate de que el calendario esté compartido con la Service Account.")

st.divider()
st.caption("Nails by Iri - Sistema de Reservas Automático")