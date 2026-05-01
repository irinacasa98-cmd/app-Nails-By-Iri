import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"

# Configuración de página optimizada
st.set_page_config(
    page_title="Turnos - Nails by Irina", 
    layout="centered", # Centrado para que en mobile no se pierda nada
    page_icon="💅"
)

# Título visual
st.markdown("<h1 style='text-align: center;'>💅 Nails Art</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Reserva tu turno de forma rápida</p>", unsafe_allow_html=True)

# --- SECCIÓN 1: POLÍTICA DE SEÑA (Compacta para mobile) ---
with st.expander("📌 IMPORTANTE: Leer política de seña", expanded=True):
    st.warning("""
    * **50% de seña** para confirmar.
    * Tenés **2 horas** para enviar el comprobante.
    * Caso contrario, el turno se libera automáticamente.
    """)

st.divider()

# --- SECCIÓN 2: EL CALENDARIO INYECTADO ---
st.subheader("1. Seleccioná tu turno")
# Ajustamos el alto para que el calendario de Google se vea bien en celulares
components.iframe(LINK_CITAS_GOOGLE, height=600, scrolling=True)

st.divider()

# --- SECCIÓN 3: DATOS Y WHATSAPP ---
st.subheader("2. Confirmá tu reserva")
nombre = st.text_input("Tu Nombre Completo:")

servicios = {
    "Semipermanente ($16.000)": "Semipermanente - $16.000",
    "Kapping ($20.000)": "Kapping - $20.000",
    "Esculpidas ($30.000)": "Esculpidas - $30.000"
}

servicio_sel = st.selectbox("¿Qué servicio elegiste?", options=list(servicios.keys()))

st.markdown("<br>", unsafe_allow_html=True)

# Botón de WhatsApp grande y llamativo para pulgares
if st.button("✅ ENVIAR COMPROBANTE POR WHATSAPP", use_container_width=True, type="primary"):
    if nombre:
        detalle = servicios[servicio_sel]
        msj = (f"¡Hola Irina! Soy *{nombre}*.\n"
               f"Ya agendé mi turno para *{detalle}*.\n"
               f"Te adjunto el comprobante de la seña.")
        
        url_wa = f"https://wa.me/5491135677912?text={urllib.parse.quote(msj)}"
        
        # En móviles, es mejor un enlace directo que abra la App
        st.markdown(f'''
            <a href="{url_wa}" target="_blank" style="text-decoration:none;">
                <div style="text-align:center; padding:18px; background-color:#25D366; color:white; border-radius:12px; font-weight:bold; font-size:18px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                    CLICK AQUÍ PARA ABRIR WHATSAPP 📱
                </div>
            </a>
        ''', unsafe_allow_html=True)
        st.balloons()
    else:
        st.error("⚠️ Por favor, ingresá tu nombre.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("Nails by Irina - Gestión de Turnos 2026")