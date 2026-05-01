import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"

st.set_page_config(page_title="Turnos - Nails by Iri", layout="centered", page_icon="💅")

# --- DISEÑO ESTÉTICO REFORZADO ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url("https://images.unsplash.com/photo-1632345031435-8727f6897d53?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Contenedor blanco sólido para el Calendario (Soluciona el problema de los botones blancos) */
    .cal-container {{
        background-color: white !important;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}

    /* Tarjetas de los pasos */
    .step-card {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(214, 51, 132, 0.1);
    }}

    h1, h2, h3 {{ color: #d63384 !important; font-family: 'Playfair Display', serif; }}
    
    .stButton>button {{
        border-radius: 50px;
        background-color: #d63384;
        color: white;
        height: 3em;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# Inicializar sesión
if 'paso' not in st.session_state:
    st.session_state.paso = 1

# --- PASO 1: REGLAS ---
if st.session_state.paso == 1:
    st.markdown("<h1 style='text-align: center;'>💅 Nails by Irina</h1>", unsafe_allow_html=True)
    st.progress(33)
    
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader("¡Bienvenida! ✨")
    st.write("Antes de reservar, recordá:")
    st.info("""
    💰 **Seña del 50%:** Obligatoria para confirmar.  
    ⏰ **Límite de 2hs:** Para enviar el comprobante.  
    🔄 **Liberación:** Pasado ese tiempo, el turno se libera.
    """)
    
    if st.button("ENTENDIDO, QUIERO MI TURNO ✨", use_container_width=True):
        st.session_state.paso = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PASO 2: CALENDARIO (CON BLOQUEO) ---
elif st.session_state.paso == 2:
    st.markdown("<h2 style='text-align: center;'>📅 Reservá tu Horario</h2>", unsafe_allow_html=True)
    st.progress(66)
    
    # Envolvemos el iframe en un div con fondo blanco para que se vea bien
    st.markdown('<div class="cal-container">', unsafe_allow_html=True)
    components.iframe(LINK_CITAS_GOOGLE, height=550, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.write("⚠️ **Importante:** Primero elegí tu horario arriba y completá los datos que te pide Google.")
    
    # Checkbox de validación
    confirmado = st.checkbox("Ya completé mi reserva en el calendario oficial")
    
    if st.button("CONTINUAR AL PAGO ➡️", use_container_width=True, disabled=not confirmado):
        st.session_state.paso = 3
        st.rerun()
    
    if not confirmado:
        st.caption("Debes marcar la casilla de arriba para poder continuar.")
        
    if st.button("⬅️ Volver", use_container_width=True):
        st.session_state.paso = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PASO 3: WHATSAPP ---
elif st.session_state.paso == 3:
    st.markdown("<h2 style='text-align: center;'>💖 Confirmación Final</h2>", unsafe_allow_html=True)
    st.progress(100)
    
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    nombre = st.text_input("¿Tu nombre completo?")
    
    servicios = {
        "Semipermanente ($16.000)": "Semipermanente - $16.000",
        "Kapping ($20.000)": "Kapping - $20.000",
        "Esculpidas ($30.000)": "Esculpidas - $30.000"
    }
    servicio_sel = st.selectbox("¿Qué servicio reservaste?", options=list(servicios.keys()))

    if st.button("ENVIAR COMPROBANTE POR WHATSAPP 📱", use_container_width=True):
        if nombre:
            detalle = servicios[servicio_sel]
            msj = (f"¡Hola Irina! Soy *{nombre}*.\n"
                   f"Reservé mi turno para *{detalle}*.\n"
                   f"Acá te mando el comprobante de la seña.")
            url_wa = f"https://wa.me/5491135677912?text={urllib.parse.quote(msj)}"
            
            st.markdown(f'''
                <a href="{url_wa}" target="_blank" style="text-decoration:none;">
                    <div style="text-align:center; padding:15px; background-color:#25D366; color:white; border-radius:50px; font-weight:bold;">
                        ABRIR MI WHATSAPP AHORA
                    </div>
                </a>
            ''', unsafe_allow_html=True)
            st.balloons()
        else:
            st.error("Por favor, escribí tu nombre.")

    if st.button("⬅️ Revisar Calendario", use_container_width=True):
        st.session_state.paso = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-size: 12px; color: gray; margin-top: 20px;'>Nails by Irina • Paso del Rey</p>", unsafe_allow_html=True)