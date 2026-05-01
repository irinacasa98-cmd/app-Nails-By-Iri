import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
# Modificamos el link para intentar forzar una vista más compacta (modo agenda/semana)
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true&mode=AGENDA"

st.set_page_config(page_title="Nails by Iri", layout="centered", page_icon="💅")

# CSS para reducir márgenes superiores y estéticos
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .stAlert { padding: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)

# Contenedor principal tipo "Cuadro"
with st.container(border=True):
    st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>💅 Nails by Irina</h2>", unsafe_allow_html=True)
    st.caption("<p style='text-align: center;'>Reserva y confirmación en un solo paso</p>", unsafe_allow_html=True)

    # Política de seña muy compacta
    st.info("⚠️ **Seña del 50% requerida.** Tenés 2hs para enviar el comprobante o el turno se libera.")

    # Calendario - Reducimos la altura a 500px para que entre más info abajo
    components.iframe(LINK_CITAS_GOOGLE, height=520, scrolling=True)

    st.markdown("---")
    
    # Formulario apilado
    nombre = st.text_input("Nombre Completo:", placeholder="Ej: Juana Pérez")
    
    servicios = {
        "Semipermanente ($16.000)": "Semipermanente - $16.000",
        "Kapping ($20.000)": "Kapping - $20.000",
        "Esculpidas ($30.000)": "Esculpidas - $30.000"
    }
    
    servicio_sel = st.selectbox("Servicio reservado:", options=list(servicios.keys()))

    # Botón de WhatsApp
    if st.button("✅ CONFIRMAR Y ENVIAR COMPROBANTE", use_container_width=True, type="primary"):
        if nombre:
            detalle = servicios[servicio_sel]
            msj = (f"¡Hola Irina! Soy *{nombre}*.\n"
                   f"Reservé turno para *{detalle}*.\n"
                   f"Adjunto el comprobante de seña.")
            url_wa = f"https://wa.me/5491135677912?text={urllib.parse.quote(msj)}"
            
            st.markdown(f'''
                <a href="{url_wa}" target="_blank" style="text-decoration:none;">
                    <div style="text-align:center; padding:12px; background-color:#25D366; color:white; border-radius:10px; font-weight:bold;">
                        ABRIR WHATSAPP AQUÍ 📱
                    </div>
                </a>
            ''', unsafe_allow_html=True)
        else:
            st.error("Por favor, ingresá tu nombre.")

st.caption("<p style='text-align: center;'>Paso del Rey, Buenos Aires</p>", unsafe_allow_html=True)