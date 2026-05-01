import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"

st.set_page_config(page_title="Turnos - Nails by Iri", layout="centered", page_icon="💅🏻")

# --- DISEÑO ESTÉTICO REFORZADO (SIN CAJAS FANTASMA) ---
st.markdown(f"""
    <style>
    /* Fondo principal */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url("https://images.unsplash.com/photo-1632345031435-8727f6897d53?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* ELIMINAR CAJAS BLANCAS POR DEFECTO DE STREAMLIT */
    [data-testid="stVerticalBlock"], [data-testid="stHeader"], .main {{
        background-color: transparent !important;
    }}
    
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border: none !important;
        background-color: transparent !important;
    }}

    /* Tarjeta principal de los pasos */
    .step-card {{
        background-color: rgba(255, 255, 255, 0.98);
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(214, 51, 132, 0.1);
        margin-bottom: 20px;
    }}

    /* Contenedor sólido exclusivo para el Calendario */
    .cal-container {{
        background-color: white !important;
        border-radius: 15px;
        padding: 5px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}

    h1, h2, h3 {{ color: #d63384 !important; font-family: 'Playfair Display', serif; text-align: center; }}
    
    .stButton>button {{
        border-radius: 50px;
        background-color: #d63384;
        color: white;
        height: 3.5em;
        font-weight: bold;
        border: none;
        width: 100%;
    }}
    
    /* Estilo para el Checkbox */
    .stCheckbox label {{
        font-weight: bold;
        color: #333;
    }}
    </style>
    """, unsafe_allow_html=True)

# Inicializar sesión
if 'paso' not in st.session_state:
    st.session_state.paso = 1

# --- PASO 1: REGLAS ---
if st.session_state.paso == 1:
    st.markdown("<h1>💅🏻 Nails by Irina</h1>", unsafe_allow_html=True)
    st.progress(33)
    
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader("¡Bienvenida! ✨")
    st.write("Antes de reservar, recordá nuestras políticas:")
    st.info("""
    💰 **Seña del 50%:** Obligatoria para confirmar.  
    ⏰ **Límite de 2hs:** Para enviar el comprobante.  
    🔄 **Liberación:** Pasado ese tiempo, el turno se libera.
    """)
    if st.button("ENTENDIDO, QUIERO MI TURNO ✨"):
        st.session_state.paso = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PASO 2: CALENDARIO ---
elif st.session_state.paso == 2:
    st.markdown("<h2>📅 Reservá tu Horario</h2>", unsafe_allow_html=True)
    st.progress(66)
    
    # Calendario en caja sólida
    st.markdown('<div class="cal-container">', unsafe_allow_html=True)
    components.iframe(LINK_CITAS_GOOGLE, height=550, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.write("⚠️ **Primero elegí tu horario arriba** y completá los datos que te pide Google.")
    
    confirmado = st.checkbox("Ya completé mi reserva en el calendario oficial")
    
    if st.button("CONTINUAR AL PAGO ➡️", disabled=not confirmado):
        st.session_state.paso = 3
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        st.session_state.paso = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PASO 3: WHATSAPP ---
elif st.session_state.paso == 3:
    st.markdown("<h2>💖 Confirmación Final</h2>", unsafe_allow_html=True)
    st.progress(100)
    
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.write("Completá tus datos para finalizar la reserva:")
    
    nombre = st.text_input("¿Tu nombre completo?")
    
    servicios = {
        "Semipermanente ($16.000)": "Semipermanente - $16.000",
        "Kapping ($20.000)": "Kapping - $20.000",
        "Esculpidas ($30.000)": "Esculpidas - $30.000"
    }
    servicio_sel = st.selectbox("¿Qué servicio reservaste?", options=list(servicios.keys()))

    if st.button("ENVIAR COMPROBANTE POR WHATSAPP 📱"):
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

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Revisar Calendario"):
        st.session_state.paso = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-size: 12px; color: gray; margin-top: 20px;'>Nails by Irina • Paso del Rey</p>", unsafe_allow_html=True)