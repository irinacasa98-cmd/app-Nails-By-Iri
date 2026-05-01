import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
# PEGA AQUÍ EL ENLACE QUE COPIASTE DE GOOGLE CALENDAR
LINK_CITAS_GOOGLE = "https://calendar.app.google/SKMUag2UBbHP52Lh9"

st.set_page_config(page_title="Turnos - Nails by Irina", layout="wide")

st.title("💅 Nails Art - Reserva de Turnos")

# Creamos dos columnas: una para el calendario y otra para la info/WhatsApp
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📅 Elegí tu día y horario")
    # Inyectamos el calendario oficial de Google directamente
    components.iframe(LINK_CITAS_GOOGLE, height=700, scrolling=True)

with col2:
    st.subheader("💰 Lista de Precios")
    st.write("- **Semipermanente:** $16.000")
    st.write("- **Kapping:** $20.000")
    st.write("- **Esculpidas:** $30.000")
    
    st.divider()
    
    st.subheader("📱 Confirmación")
    st.info("Una vez que reserves en el calendario de la izquierda, enviame el comprobante por acá:")
    
    nombre = st.text_input("Tu Nombre")
    
    # Botón de WhatsApp
    tel = "5491135677912"
    msj = f"¡Hola! Soy {nombre}, acabo de reservar un turno en el calendario. Adjunto el comprobante:"
    url_wa = f"https://wa.me/{tel}?text={urllib.parse.quote(msj)}"
    
    if st.button("ENVIAR COMPROBANTE POR WHATSAPP 📱", use_container_width=True):
        if nombre:
            st.markdown(f'<a href="{url_wa}" target="_blank">Abrir chat de WhatsApp</a>', unsafe_allow_html=True)
        else:
            st.error("Por favor, ingresá tu nombre.")