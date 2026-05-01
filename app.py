import streamlit as st
import urllib.parse

# --- CONFIGURACIÓN ---
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"

st.set_page_config(page_title="Turnos - Nails by Irina", layout="wide", page_icon="💅")

st.title("💅 Nails Art - Reserva de Turnos")
st.markdown("---")

col_info, col_btn = st.columns([1, 1])

with col_info:
    st.subheader("1. Reservá tu turno")
    st.write("Hacé clic en el botón de abajo para elegir tu día y horario en el calendario oficial.")
    
    # Creamos un botón de Streamlit que funciona como enlace directo
    # Esto evita los scripts de Google que se están bloqueando
    st.markdown(f'''
        <a href="{LINK_CITAS_GOOGLE}" target="_blank" style="text-decoration:none;">
            <div style="text-align:center; padding:20px; background-color:#039BE5; color:white; border-radius:10px; font-weight:bold; font-size:20px; border: 2px solid #0277bd;">
                📅 VER DISPONIBILIDAD Y AGENDAR
            </div>
        </a>
    ''', unsafe_allow_html=True)
    st.caption("Se abrirá una nueva pestaña con el calendario de Google.")

with col_btn:
    st.subheader("2. Política de Seña")
    st.warning("""
    ⚠️ **LEER CON ATENCIÓN:**  
    * Todas las reservas se toman con el **50% de seña**.  
    * Tenés **2 horas** para enviar el comprobante.  
    * Pasado ese tiempo, el turno se libera automáticamente.
    """)

st.divider()

# --- SECCIÓN DE WHATSAPP ---
st.subheader("3. Confirmá tu reserva enviando el comprobante")
nombre = st.text_input("Nombre Completo:")

servicios = {
    "Semipermanente ($16.000)": "Semipermanente - $16.000",
    "Kapping ($20.000)": "Kapping - $20.000",
    "Esculpidas ($30.000)": "Esculpidas - $30.000"
}

servicio_sel = st.selectbox("¿Qué servicio reservaste?", options=list(servicios.keys()))

if st.button("GENERAR MENSAJE DE WHATSAPP 📱", use_container_width=True, type="primary"):
    if nombre:
        detalle = servicios[servicio_sel]
        msj = (f"¡Hola Irina! Soy *{nombre}*.\n"
               f"Ya agendé mi turno para *{detalle}*.\n"
               f"Te adjunto el comprobante de la seña.")
        
        url_wa = f"https://wa.me/5491135677912?text={urllib.parse.quote(msj)}"
        
        st.markdown(f'''
            <a href="{url_wa}" target="_blank" style="text-decoration:none;">
                <div style="text-align:center; padding:15px; background-color:#25D366; color:white; border-radius:8px; font-weight:bold; font-size:18px;">
                    Hacé clic acá para abrir WhatsApp
                </div>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.error("⚠️ Por favor, ingresá tu nombre.")

st.markdown("---")
st.caption("Nails by Irina - Gestión de Citas")