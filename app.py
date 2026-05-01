import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"

st.set_page_config(page_title="Turnos - Nails by Iri", layout="centered", page_icon="💅")

# Inicializar el paso actual si no existe
if 'paso' not in st.session_state:
    st.session_state.paso = 1

# CSS para mejorar la estética de los pasos
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-color: #039BE5; }
    .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- PASO 1: CONDICIONES ---
if st.session_state.paso == 1:
    st.markdown("<h2 style='text-align: center;'>💅 Nails by Irina</h2>", unsafe_allow_html=True)
    st.progress(33)
    
    with st.container(border=True):
        st.subheader("Antes de empezar...")
        st.write("Por favor, leé y aceptá nuestras condiciones de reserva:")
        st.warning("""
        * **Seña del 50%:** Todos los turnos requieren una seña para ser confirmados.
        * **Límite de 2 horas:** Una vez solicitado el turno, tenés 2hs para enviar el comprobante.
        * **Cancelación:** Si no se recibe el pago en ese tiempo, el turno se libera automáticamente.
        """)
        
        if st.button("ACEPTO LAS CONDICIONES ✅", use_container_width=True, type="primary"):
            st.session_state.paso = 2
            st.rerun()

# --- PASO 2: CALENDARIO ---
elif st.session_state.paso == 2:
    st.markdown("<h2 style='text-align: center;'>📅 Elegí tu horario</h2>", unsafe_allow_html=True)
    st.progress(66)
    
    components.iframe(LINK_CITAS_GOOGLE, height=550, scrolling=True)
    
    st.markdown("---")
    if st.button("YA ELEGÍ MI HORARIO ➡️", use_container_width=True, type="primary"):
        st.session_state.paso = 3
        st.rerun()
    
    if st.button("⬅️ Volver", use_container_width=True):
        st.session_state.paso = 1
        st.rerun()

# --- PASO 3: WHATSAPP ---
elif st.session_state.paso == 3:
    st.markdown("<h2 style='text-align: center;'>📱 Confirmación Final</h2>", unsafe_allow_html=True)
    st.progress(100)
    
    with st.container(border=True):
        st.write("Completá tus datos para enviarme el comprobante de pago.")
        
        nombre = st.text_input("Tu Nombre Completo:")
        
        servicios = {
            "Semipermanente ($16.000)": "Semipermanente - $16.000",
            "Kapping ($20.000)": "Kapping - $20.000",
            "Esculpidas ($30.000)": "Esculpidas - $30.000"
        }
        servicio_sel = st.selectbox("Servicio que reservaste:", options=list(servicios.keys()))

        if st.button("ENVIAR WHATSAPP ✅", use_container_width=True, type="primary"):
            if nombre:
                detalle = servicios[servicio_sel]
                msj = (f"¡Hola Irina! Soy *{nombre}*.\n"
                       f"Acabo de reservar el turno para *{detalle}*.\n"
                       f"Adjunto el comprobante de la seña.")
                url_wa = f"https://wa.me/5491135677912?text={urllib.parse.quote(msj)}"
                
                st.markdown(f'''
                    <a href="{url_wa}" target="_blank" style="text-decoration:none;">
                        <div style="text-align:center; padding:15px; background-color:#25D366; color:white; border-radius:10px; font-weight:bold;">
                            ABRIR MI WHATSAPP AQUÍ
                        </div>
                    </a>
                ''', unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("Por favor, ingresá tu nombre.")

    if st.button("⬅️ Volver al calendario", use_container_width=True):
        st.session_state.paso = 2
        st.rerun()