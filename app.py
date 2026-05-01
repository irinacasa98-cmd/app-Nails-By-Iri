import streamlit as st
from datetime import datetime, timedelta, time
from google.oauth2 import service_account
from googleapiclient.discovery import build
import urllib.parse

# --- CONFIGURACIÓN ---
SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = "irinacasa98@gmail.com" # <--- CAMBIA ESTO

def get_calendar_service():
    creds_dict = dict(st.secrets["google_calendar"])
    if "private_key" in creds_dict:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return build('calendar', 'v3', credentials=creds)

def obtener_disponibilidad_real(fecha_sel):
    service = get_calendar_service()
    
    # Definimos el inicio y fin del día para consultar
    tz_offset = "-03:00" # Argentina
    inicio_dia = datetime.combine(fecha_sel, time(9, 0)).isoformat() + tz_offset
    fin_dia = datetime.combine(fecha_sel, time(21, 0)).isoformat() + tz_offset

    # Consultamos los bloques ocupados (FreeBusy)
    body = {
        "timeMin": inicio_dia,
        "timeMax": fin_dia,
        "items": [{"id": calendar_id}]
    }
    
    freebusy_result = service.freebusy().query(body=body).execute()
    ocupados = freebusy_result['calendars'][calendar_id]['busy']

    # Generamos slots cada 30 min para buscar dónde entran tus 2.5 hs
    slots_libres = []
    duracion_turno = timedelta(hours=2, minutes=30)
    
    actual = datetime.combine(fecha_sel, time(10, 0)) # Hora de apertura
    cierre = datetime.combine(fecha_sel, time(20, 0)) # Hora de cierre

    while actual + duracion_turno <= cierre:
        # Verificamos si este bloque de 2.5hs choca con algún evento ocupado
        bloque_inicio = actual.replace(tzinfo=None)
        bloque_fin = (actual + duracion_turno).replace(tzinfo=None)
        
        es_valido = True
        for ocupado in ocupados:
            bus_start = datetime.fromisoformat(ocupado['start'].replace('Z', '')[:19])
            bus_end = datetime.fromisoformat(ocupado['end'].replace('Z', '')[:19])
            
            # Si el turno se solapa con un evento ocupado
            if not (bloque_fin <= bus_start or bloque_inicio >= bus_end):
                es_valido = False
                break
        
        if es_valido:
            slots_libres.append(actual.time())
        
        # Saltamos de a 30 min para ofrecer opciones (ej: 10:00, 10:30, 11:00)
        actual += timedelta(minutes=30)
        
    return slots_libres

def agendar_en_google(nombre, servicio, fecha, hora):
    service = get_calendar_service()
    inicio = datetime.combine(fecha, hora)
    fin = inicio + timedelta(hours=2, minutes=30) # Bloque de 2.5hs
    
    evento = {
        'summary': f'Nails: {nombre} ({servicio})',
        'description': f'Servicio: {servicio}\nDuración bloqueada: 2.5hs',
        'start': {'dateTime': inicio.isoformat() + "-03:00", 'timeZone': 'America/Argentina/Buenos_Aires'},
        'end': {'dateTime': fin.isoformat() + "-03:00", 'timeZone': 'America/Argentina/Buenos_Aires'},
    }
    service.events().insert(calendarId=calendar_id, body=evento).execute()

# --- INTERFAZ ---
st.set_page_config(page_title="Reserva Nails", page_icon="💅")

st.title("💅 Reserva tu Turno")

# 1. Datos y Precios
nombre = st.text_input("Tu Nombre Completo:")

# Diccionario de precios para el mensaje de WhatsApp
servicios_precios = {
    "Semipermanente ($16.000)": "Semipermanente - $16.000",
    "Kapping ($20.000)": "Kapping - $20.000",
    "Esculpidas ($30.000)": "Esculpidas - $30.000"
}

servicio_elegido = st.selectbox("Elegí el servicio:", list(servicios_precios.keys()))

# 2. Fecha
st.subheader("📅 Seleccioná el día")
fecha_sel = st.date_input("Día:", min_value=datetime.today())

# 3. Horarios con lógica de 2.5hs
st.subheader("⏰ Horarios Disponibles (Bloques de 2.5hs)")
with st.spinner("Consultando agenda real..."):
    libres = obtener_disponibilidad_real(fecha_sel)

if libres:
    cols = st.columns(4)
    for i, h in enumerate(libres):
        with cols[i % 4]:
            if st.button(h.strftime("%H:%M"), key=f"h_{i}", use_container_width=True):
                if not nombre:
                    st.error("⚠️ Escribí tu nombre primero.")
                else:
                    try:
                        agendar_en_google(nombre, servicio_elegido, fecha_sel, h)
                        
                        tel = "5491135677912"
                        resumen = servicios_precios[servicio_elegido]
                        msj = f"¡Hola! Reservé mi turno:\n👤 *{nombre}*\n💅 *{resumen}*\n📅 *{fecha_sel.strftime('%d/%m')}*\n⏰ *{h.strftime('%H:%M')} hs*\n\nAdjunto comprobante:"
                        url_wa = f"https://wa.me/{tel}?text={urllib.parse.quote(msj)}"
                        
                        st.success("✅ Turno inyectado en el calendario.")
                        st.markdown(f'''
                            <a href="{url_wa}" target="_blank" style="text-decoration:none;">
                                <div style="background-color:#25D366; color:white; padding:15px; border-radius:8px; font-weight:bold; text-align:center; font-size:18px;">
                                    ENVIAR COMPROBANTE POR WHATSAPP 📱
                                </div>
                            </a>
                        ''', unsafe_allow_html=True)
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error: {e}")
else:
    st.warning("No hay espacio suficiente para un turno de 2.5hs este día.")