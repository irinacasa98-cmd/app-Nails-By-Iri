import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"

st.set_page_config(page_title="Turnos - Nails by Irina", layout="wide", page_icon="💅")

st.title("💅 Nails Art - Reserva de Turnos")
st.markdown("---")

col_info, col_btn = st.columns([1, 1])

with col_info:
    st.subheader("1. Reservá tu turno")
    st.write("Hacé clic en el botón azul para elegir tu horario en el calendario oficial.")
    
    # Inyección del botón con f-string corregido
    boton_google_html = f"""
    <div id="calendar-button-container" style="min-height: 100px;">
        <link href="https://calendar.google.com/calendar/scheduling-button-script.css" rel="stylesheet">
        <script src="https://calendar.google.com/calendar/scheduling-button-script.js" async></script>
        <script>
        function loadCalendarButton() {{
            if (window.calendar && window.calendar.schedulingButton) {{
                window.calendar.schedulingButton.load({{
                    url: '{LINK_CITAS_GOOGLE}',
                    color: '#039BE5',
                    label: 'Programar una cita',
                    target: document.getElementById('calendar-button-container'),
                }});
            }} else {{
                setTimeout(loadCalendarButton, 250);
            }}
        }}
        loadCalendarButton();
        </script>
    </div>
    """
    components.html(boton_google_html, height=150)

with col_btn:
    st.subheader("2. Política de Seña")
    st.warning("""
    ⚠️ **LEER CON ATENCIÓN:**  
    * Todas las reservas se toman con el **50% de seña**.  
    * Una vez solicitado el turno, tenés **2 horas** para enviar el comprobante.  
    * Si no se recibe el pago en ese tiempo, el turno volverá a quedar disponible.
    """)

st.divider()

st.subheader("3. Confirmá tu reserva enviando el comprobante")
nombre = st.text_input("Nombre Completo:")

# Diccionario corregido (con llaves simples)
servicios = {
    "Semipermanente ($16.000)": "Semipermanente - $16.000",
    "Kapping ($20.000)": "Kapping - $20.000",
    "Esculpidas ($30.000)": "Esculpidas - $30.000"
}

servicio_sel = st.selectbox("¿Qué servicio reservaste en el calendario?", options=list(servicios.keys()))

st.markdown("<br>", unsafe_allow_html=True)

if st.button("ENVIAR COMPROBANTE POR WHATSAPP 📱", use_container_width=True, type="primary"):
    if nombre:
        detalle = servicios[servicio_sel]
        msj = (f"¡Hola Irina! Soy *{nombre}*.\n"
               f"Ya agendé mi turno para *{detalle}*.\n"
               f"Te adjunto el comprobante de la seña del 50%.")
        
        url_wa = f"https://wa.me/5491135677912?text={urllib.parse.quote(msj)}"
        
        st.markdown(f'''
            <a href="{url_wa}" target="_blank" style="text-decoration:none;">
                <div style="text-align:center; padding:15px; background-color:#25D366; color:white; border-radius:8px; font-weight:bold; font-size:18px;">
                    Hacé clic acá para abrir tu WhatsApp y adjuntar la foto
                </div>
            </a>
        ''', unsafe_allow_html=True)
        st.balloons()
    else:
        st.error("⚠️ Por favor, ingresá tu nombre para poder generar el mensaje.")

st.markdown("---")
st.caption("Nails by Irina - Gestión Automática de Citas")