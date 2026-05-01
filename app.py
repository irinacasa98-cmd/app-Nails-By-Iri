import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"

st.set_page_config(page_title="Turnos - Nails by Iri", layout="centered", page_icon="💅🏻")

# --- DISEÑO ESTÉTICO ULTRA-LIMPIO (ELIMINA CAJAS VACÍAS) ---
st.markdown(f"""
    <style>
    /* 1. Fondo principal */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url("https://images.unsplash.com/photo-1632345031435-8727f6897d53?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* 2. Ocultar contenedores vacíos de Streamlit y cajas blancas fantasma */
    [data-testid="stVerticalBlock"] > div:empty {{
        display: none !important;
    }}
    
    [data-testid="stVerticalBlockBorderWrapper"], 
    [data-testid="stVerticalBlock"] > div {{
        background-color: transparent !important;
        border: none !important;
    }}

    /* 3. Tarjeta de contenido (La única que debe ser blanca) */
    .step-card {{
        background-color: rgba(255, 255, 255, 0.98);
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin-top: 10px;
    }}

    /* 4. Calendario sólido */
    .cal-container {{
        background-color: white !important;
        border-radius: 15px;
        padding: 5px;
        margin-bottom: 15px;
    }}

    h1, h2, h3 {{ color: #d63384 !important; font-family: 'Playfair Display', serif; text-align: center; }}
    
    .stButton>button {{
        border-radius: 50px;
        background-color: #d63384;
        color: white;
        height: 3.5em;
        font-weight: bold;
        border: none;
    }}
    
    /* Eliminar espacio superior extra */
    .block-container {{
        padding-top: 1rem !important;
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
    
    # Usamos un div manual en lugar de st.container para evitar cajas automáticas
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>¡Bienvenida! ✨</h3>", unsafe_allow_html=True)
    st.write("Antes de reservar, recordá nuestras políticas:")
    st.info("""
    💰 **Seña del 50%:** Obligatoria para confirmar.  
    ⏰ **Límite de 2hs:** Para enviar el comprobante.  
    🔄 **Liberación:** Pasado ese tiempo, el turno se libera.
    """)
    if st.button("ENTENDIDO, QUIERO MI TURNO ✨", key="btn_p1"):
        st.session_state.paso = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PASO 2: CALENDARIO ---
elif st.session_state.paso == 2:
    st.markdown("<h2>📅 Reservá tu Horario</h2>", unsafe_allow_html=True)
    st.progress(66)
    
    st.markdown('<div class="cal-container">', unsafe_allow_html=True)
    components.iframe(LINK_CITAS_GOOGLE, height=550, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.write("⚠️ **Primero elegí tu horario arriba** y completá los datos de Google.")
    
    confirmado = st.checkbox("Ya completé mi reserva en el calendario", key="check_p2")
    
    if st.button("CONTINUAR AL PAGO ➡️", disabled=not confirmado, key="btn_p2"):
        st.session_state.paso = 3
        st.rerun()
    
    if st.button("⬅️ Volver", key="back_p2"):
        st.session_state.paso = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PASO 3: WHATSAPP ---
elif st.session_state.paso == 3:
    st.markdown("<h2>💖 Confirmación Final</h2>", unsafe_allow_html=True)
    st.progress(100)
    
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    nombre = st.text_input("¿Tu nombre completo?", placeholder="Ej: Maria Lopez")
    
    servicios = {
        "Semipermanente ($16.000)": "Semipermanente - $16.000",
        "Kapping ($20.000)": "Kapping - $20.000",
        "Esculpidas ($30.000)": "Esculpidas - $30.000"
    }
    servicio_sel = st.selectbox("Servicio reservado:", options=list(servicios.keys()))

    if st.button("ENVIAR COMPROBANTE 📱", key="btn_p3"):
        if nombre:
            detalle = servicios[servicio_sel]
            msj = (f"¡Hola Irina! Soy *{nombre}*.\n"
                   f"Reservé mi turno para *{detalle}*.\n"
                   f"Acá te mando el comprobante de la seña.")
            url_wa = f"https://wa.me/5491135677912?text={urllib.parse.quote(msj)}"
            
            st.markdown(f'''
                <a href="{url_wa}" target="_blank" style="text-decoration:none;">
                    <div style="text-align:center; padding:15px; background-color:#25D366; color:white; border-radius:50px; font-weight:bold;">
                        ABRIR MI WHATSAPP
                    </div>
                </a>
            ''', unsafe_allow_html=True)
            st.balloons()
        else:
            st.error("Por favor, escribí tu nombre.")

    if st.button("⬅️ Revisar Calendario", key="back_p3"):
        st.session_state.paso = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-size: 11px; color: gray; margin-top: 20px;'>Nails by Irina • Paso del Rey</p>", unsafe_allow_html=True)