import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"

st.set_page_config(page_title="Turnos - Nails by Iri", layout="centered", page_icon="💅🏻")

# --- CSS RADICAL CONTRA CAJAS BLANCAS ---
st.markdown(f"""
    <style>
    /* 1. Fondo e invisibilidad total de bloques de Streamlit */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url("https://images.unsplash.com/photo-1632345031435-8727f6897d53?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Matamos cualquier fondo blanco de los contenedores internos */
    [data-testid="stVerticalBlock"], 
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stHeader"],
    .main,
    div[role="presentation"],
    .element-container {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    /* 2. La ÚNICA tarjeta permitida */
    .main-card {{
        background-color: rgba(255, 255, 255, 0.98);
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(214, 51, 132, 0.1);
        margin-top: 0px;
    }}

    /* 3. Contenedor de Calendario (Blanco sólido para que no falle Google) */
    .cal-box {{
        background-color: white !important;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 20px;
    }}

    /* Estilos de texto */
    h1 {{ color: #d63384 !important; font-family: 'Playfair Display', serif; text-align: center; margin-bottom: 0px; }}
    h3 {{ color: #d63384 !important; text-align: center; }}
    
    /* Botón personalizado */
    .stButton>button {{
        border-radius: 50px;
        background-color: #d63384;
        color: white;
        height: 3.5em;
        font-weight: bold;
        width: 100%;
        border: none;
        box-shadow: 0 4px 15px rgba(214, 51, 132, 0.3);
    }}

    /* Limpieza de espacios superiores */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Inicializar sesión
if 'paso' not in st.session_state:
    st.session_state.paso = 1

# --- ESTRUCTURA DE LA APP ---

# Título siempre visible arriba
st.markdown("<h1>💅🏻 Nails by Irina</h1>", unsafe_allow_html=True)

if st.session_state.paso == 1:
    st.progress(33)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("<h3>¡Bienvenida! ✨</h3>", unsafe_allow_html=True)
    st.info("""
    💰 **Seña del 50%:** Obligatoria para confirmar.  
    ⏰ **Límite de 2hs:** Para enviar el comprobante.  
    🔄 **Liberación:** Pasado ese tiempo, el turno se libera.
    """)
    if st.button("ENTENDIDO, QUIERO MI TURNO ✨"):
        st.session_state.paso = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.paso == 2:
    st.progress(66)
    # El calendario va en su propia caja blanca para evitar errores visuales de Google
    st.markdown('<div class="cal-box">', unsafe_allow_html=True)
    components.iframe(LINK_CITAS_GOOGLE, height=550)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("⚠️ **Elegí tu horario arriba** y completá los datos.")
    confirmado = st.checkbox("Ya completé mi reserva en el calendario")
    if st.button("CONTINUAR AL PAGO ➡️", disabled=not confirmado):
        st.session_state.paso = 3
        st.rerun()
    if st.button("⬅️ Volver"):
        st.session_state.paso = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.paso == 3:
    st.progress(100)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("<h3>💖 Confirmación Final</h3>", unsafe_allow_html=True)
    nombre = st.text_input("¿Tu nombre completo?")
    servicios = ["Semipermanente ($16.000)", "Kapping ($20.000)", "Esculpidas ($30.000)"]
    servicio_sel = st.selectbox("Servicio reservado:", servicios)

    if st.button("ENVIAR COMPROBANTE POR WHATSAPP 📱"):
        if nombre:
            msj = (f"¡Hola Irina! Soy *{nombre}*.\n"
                   f"Reservé mi turno para *{servicio_sel}*.\n"
                   f"Acá te mando el comprobante de la seña.")
            url_wa = f"https://wa.me/5491135677912?text={urllib.parse.quote(msj)}"
            st.markdown(f'<a href="{url_wa}" target="_blank" style="text-decoration:none;"><div style="text-align:center; padding:15px; background-color:#25D366; color:white; border-radius:50px; font-weight:bold;">ABRIR WHATSAPP</div></a>', unsafe_allow_html=True)
            st.balloons()
    
    st.write("")
    if st.button("⬅️ Revisar Calendario"):
        st.session_state.paso = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-size: 10px; color: gray; margin-top: 30px;'>Paso del Rey, Buenos Aires</p>", unsafe_allow_html=True)