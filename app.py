import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
# Este es el corazón del botón, no lo borres
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"

st.set_page_config(page_title="Turnos - Nails by Irina", layout="wide", page_icon="💅")

st.title("💅 Nails Art - Reserva de Turnos")
st.markdown("---")

col_info, col_btn = st.columns([1, 1])

with col_info:
    st.subheader("1. Reservá tu turno")
    st.write("Hacé clic en el botón azul para elegir tu horario en el calendario oficial.")
    
    # Inyección del botón oficial (usa el link internamente)
    boton_google_html = f"""
    <link href="https://calendar.google.com/calendar/scheduling-button-script.css" rel="stylesheet">
    <script src="https://calendar.google.com/calendar/scheduling-button-script.js" async></script>
    <script>
    (function() {{
      var target = document.currentScript;
      window.addEventListener('load', function() {{
        calendar.schedulingButton.load({{
          url: '{LINK_CITAS_GOOGLE}',
          color: '#039BE5',
          label: 'Ver disponibilidad y agendar',
          target,
        }});
      }});
    }})();
    </script>
    """
    components.html(boton_google_html, height=100)

with col_btn:
    st.subheader("2. Política de Seña")
    st.warning("""
    ⚠️ **LEER CON ATENCIÓN:**  
    * Las reservas se toman con el **50% de seña**.  
    * Tenés **2 horas** para enviar el comprobante; de lo contrario, el turno se cancela.
    """)

st.divider()

# --- CONFIRMACIÓN POR WHATSAPP ---
st.subheader("3. Confirmá tu reserva")
nombre = st.text_input("Tu Nombre Completo:")

servicios = {
    "Semipermanente ($16.000)": "Semipermanente",
    "Kapping ($20.000)": "Kapping",
    "Esculpidas ($30.000)": "Esculpidas"
}
servicio_sel = st.selectbox("¿Qué servicio elegiste?", options=list(servicios.keys()))

if st.button("ENVIAR COMPROBANTE POR WHATSAPP 📱", use_container_width=True, type="primary"):
    if nombre:
        msj = (f"¡Hola Irina! Soy *{nombre}*.\n"
               f"Ya agendé mi turno para *{servicio_sel}*.\n"
               f"Te adjunto el comprobante de la seña.")
        url_wa = f"https://wa.me/5491135677912?text={urllib.parse.quote(msj)}"
        st.markdown(f'<a href="{url_wa}" target="_blank" style="text-decoration:none;"><div style="text-align:center; padding:15px; background-color:#25D366; color:white; border-radius:8px; font-weight:bold;">ABRIR WHATSAPP</div></a>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.error("⚠️ Por favor, ingresá tu nombre.")