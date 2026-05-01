import streamlit as st
from datetime import datetime, timedelta, time
from google.oauth2 import service_account
from googleapiclient.discovery import build
import urllib.parse

# --- CONFIGURACIÓN ---
SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = "irinacasa98@gmail.com" # <--- CAMBIA ESTO POR TU GMAIL

def get_calendar_service():
    # Copia de seguridad para evitar el error de "Secrets does not support item assignment"
    creds_dict = dict(st.secrets["google_calendar"])
    if "private_key" in creds_dict:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return build('calendar', 'v3', credentials=creds)

def obtener_turnos_libres(fecha_sel):
    service = get_calendar_service()
    inicio_dia = datetime.combine(fecha_sel, time(0, 0)).isoformat() + "-03:00"
    fin_dia = datetime.combine(fecha_sel, time(23, 59)).isoformat() + "-03:00"

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=inicio_dia,
        timeMax=fin_dia,
        singleEvents=True
    ).execute()
    
    eventos = events_result.get('items', [])
    ocupados = []
    for ev in eventos:
        start = ev['start'].get('dateTime', ev['start'].get('date'))
        dt_start = datetime.fromisoformat(start.replace('Z', '-03:00'))
        ocupados.append(dt_start.time())

    # Horarios de atención: de 10hs a 19hs
    posibles = [time(h, 0) for h in range(10, 20)]
    return [h for h in posibles if h not in ocupados]

def agendar_en_google(nombre, servicio, fecha, hora):
    service = get_calendar_service()
    inicio = datetime.combine(fecha, hora)
    fin = inicio + timedelta(hours=1)
    
    evento = {
        'summary': f'Nails: {nombre} ({servicio})',
        'start': {'dateTime': inicio.isoformat() + "-03:00", 'timeZone': 'America/Argentina/Buenos_Aires'},
        'end': {'dateTime': fin.isoformat() + "-03:00", 'timeZone': 'America/Argentina/Buenos_Aires'},
    }
    service.events().insert(calendarId=calendar_id, body=evento).execute()

# --- INTERFAZ ESTILO RESERVA ---
st.set_page_config(page_title="Reserva Nails", page_icon="💅")

st.title("💅 Reserva tu Turno")
st.markdown("---")

# Paso 1: Datos
nombre = st.text_input("Tu Nombre Completo:")
servicio = st.selectbox("Elegí el servicio:", ["Semipermanente", "Kapping", "Esculpidas"])

# Paso 2: Fecha
st.subheader("📅 Seleccioná el día")
fecha_sel = st.date_input("Día:", min_value=datetime.today())

# Paso 3: Horarios (Tablero de botones)
st.subheader("⏰ Horarios Disponibles")
libres = obtener_turnos_libres(fecha_sel)

if libres:
    # Mostramos los horarios en columnas para que parezca un tablero
    cols = st.columns(4)
    for i, h in enumerate(libres):
        with cols[i % 4]:
            if st.button(h.strftime("%H:%M"), key=f"h_{i}", use_container_width=True):
                # Al hacer clic, procesamos la reserva
                if not nombre:
                    st.error("⚠️ Por favor, escribí tu nombre primero.")
                else:
                    try:
                        with st.spinner("Agendando..."):
                            agendar_en_google(nombre, servicio, fecha_sel, h)
                            
                            # WhatsApp
                            tel = "5491135677912"
                            msj = f"¡Hola! Reservé mi turno:\n👤 *{nombre}*\n💅 *{servicio}*\n📅 *{fecha_sel.strftime('%d/%m')}*\n⏰ *{h.strftime('%H:%M')} hs*\n\nAdjunto comprobante de pago:"
                            url_wa = f"https://wa.me/{tel}?text={urllib.parse.quote(msj)}"
                            
                            st.success("✅ ¡Turno agendado con éxito!")
                            st.balloons()
                            
                            st.markdown(f'''
                                <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center; border: 1px solid #ddd;">
                                    <p style="font-size:18px; color:#31333F;"><b>¡Último paso!</b></p>
                                    <p>Para confirmar el turno, enviame el comprobante de pago por WhatsApp:</p>
                                    <a href="{url_wa}" target="_blank" style="text-decoration:none;">
                                        <div style="background-color:#25D366; color:white; padding:15px; border-radius:8px; font-weight:bold; font-size:20px;">
                                            ENVIAR COMPROBANTE 📱
                                        </div>
                                    </a>
                                </div>
                            ''', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error al agendar: {e}")
else:
    st.warning("No hay horarios libres para este día. Probá con otra fecha.")

st.markdown("---")
st.caption("Agenda sincronizada con Google Calendar")