import streamlit as st
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import urllib.parse

# 1. Configuración de API de Google (usando los Secrets de Streamlit)
# Si estás probando local, puedes usar el archivo json directamente
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
calendar_id = "irinacasa98@gmail.com" # El calendario que compartiste

def get_calendar_service():
    # Carga las credenciales desde los Secrets de Streamlit
    creds_dict = st.secrets["google_calendar"]
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return build('calendar', 'v3', credentials=creds)

def check_disponibilidad(fecha_deseada, hora_deseada):
    service = get_calendar_service()
    
    # Definir el inicio y fin del turno para chequear (ej: 1 hora de duración)
    inicio_busqueda = datetime.combine(fecha_deseada, hora_deseada).isoformat() + 'Z'
    fin_busqueda = (datetime.combine(fecha_deseada, hora_deseada) + timedelta(hours=1)).isoformat() + 'Z'

    # Consultar eventos en ese rango
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=inicio_busqueda,
        timeMax=fin_busqueda,
        singleEvents=True
    ).execute()
    
    return len(events_result.get('items', [])) == 0

# --- INTERFAZ DE STREAMLIT ---
st.title("💅 Nails Art - Reserva de Turnos")

nombre = st.text_input("Tu Nombre completo:")
servicio = st.selectbox("Elegí tu servicio:", ["Semipermanente", "Kapping", "Esculpidas"])

col1, col2 = st.columns(2)
with col1:
    fecha = st.date_input("Día:", min_value=datetime.today())
with col2:
    # Definimos horarios de atención (ej: de 10 a 20hs)
    horas_disponibles = [f"{h:02d}:00" for h in range(10, 21)]
    hora_str = st.selectbox("Hora:", horas_disponibles)
    hora_dt = datetime.strptime(hora_str, "%H:%M").time()

if st.button("Verificar Disponibilidad y Reservar"):
    if not nombre:
        st.error("Por favor, ingresá tu nombre.")
    else:
        # Chequeamos el calendario
        is_free = check_disponibilidad(fecha, hora_dt)
        
        if is_free:
            st.success(f"¡El horario {hora_str} está disponible!")
            
            # Crear link de WhatsApp
            telefono = "5491135677912"
            mensaje = f"Hola! Soy {nombre}. Quiero reservar un turno para *{servicio}* el día {fecha.strftime('%d/%m')} a las {hora_str}."
            url_wa = f"https://wa.me/{telefono}?text={urllib.parse.quote(mensaje)}"
            
            st.markdown(f'''
                <a href="{url_wa}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #25D366; color: white; padding: 15px; text-align: center; border-radius: 10px; font-weight: bold;">
                        CONFIRMAR TURNO POR WHATSAPP 📱
                    </div>
                </a>
            ''', unsafe_allow_html=True)
        else:
            st.error("Lo siento, ese horario ya está ocupado. Por favor elegí otro.")