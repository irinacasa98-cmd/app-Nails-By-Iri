import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"

st.set_page_config(page_title="Turnos - Nails by Iri", layout="centered", page_icon="💅🏻")

# --- CSS REVISADO (BASADO EN LA VERSIÓN LIMPIA) ---
st.markdown(f"""
    <style>
    /* 1. Fondo de la App */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url("https://images.unsplash.com/photo-1632345031435-8727f6897d53?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* 2. ELIMINAR CAJAS BLANCAS (Reset de Streamlit) */
    [data-testid="stVerticalBlock"] > div {{
        background-color: transparent !important;
    }}
    
    .stMainBlockContainer {{
        background-color: transparent !important;
    }}

    /* 3. Tarjeta de contenido PRINCIPAL */
    .step-card {{
        background-color: rgba(255, 255, 255, 0.98);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(214, 51, 132, 0.1);
        margin-bottom: 10px;
    }}

    /* 4. El Calendario (Caja Blanca Sólida para evitar transparencia rara) */
    .cal-wrapper {{
        background-color: white !important;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        overflow: hidden;
    }}

    h1, h2, h3 {{ color: #d63384 !important; font-family: 'Playfair Display', serif; text-align: center; }}
    
    .stButton>button {{
        border-radius: 50px;
        background-color: #d63384;
        color: white;
        height: 3.5em;
        font-weight: bold;
        width: 100%;
        border: none;
    }}
    
    /* Quitar espacios extra arriba */
    .block-container {{
        padding-top: 2rem !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Lógica de pasos
if 'paso' not in st.session_state:
    st.session_state.paso = 1

# --- PASO 1: REGLAS ---
if st.session_state.paso == 1:
    st.markdown("<h1>💅🏻 Nails by Irina</h1>", unsafe_allow_html=True)
    st.progress(33)
    
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader("¡Bienvenida! ✨")
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
    
    # Aquí envolvemos el iframe en nuestra clase cal-wrapper
    st.markdown('<div class="cal-wrapper">', unsafe_allow_html=True)
    components.iframe(LINK_CITAS_GOOGLE, height=550)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.write("⚠️ **Primero elegí tu horario arriba** y completá tus datos en Google.")
    confirmado = st.checkbox("Ya completé mi reserva en el calendario oficial")
    if st.button("CONTINUAR AL PAGO ➡️", disabled=not confirmado):
        st.session_state.paso = 3
        st.rerun()
    if st.button("⬅️ Volver"):
        st.session_state.paso = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PASO 3: WHATSAPP ---
elif st.session_state.paso == 3:
    st.markdown("<h2>💖 Confirmación Final</h2>", unsafe_allow_html=True)
    st.progress(100)
    
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    nombre = st.text_input("¿Tu nombre completo?")
    servicio = st.selectbox("Servicio:", ["Semipermanente ($16.000)", "Kapping ($20.000)", "Esculpidas ($30.000)"])

    if st.button("ENVIAR COMPROBANTE 📱"):
        if nombre:
            msj = f"¡Hola Irina! Soy *{nombre}*. Reservé *{servicio}*. Acá mando el comprobante."
            url_wa = f"https://wa.me/5491135677912?text={urllib.parse.quote(msj)}"
            st.markdown(f'<a href="{url_wa}" target="_blank" style="text-decoration:none;"><div style="text-align:center; padding:15px; background-color:#25D366; color:white; border-radius:50px; font-weight:bold;">ABRIR WHATSAPP</div></a>', unsafe_allow_html=True)
            st.balloons()
    
    if st.button("⬅️ Revisar Calendario"):
        st.session_state.paso = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-size: 11px; color: gray;'>Nails by Irina • Paso del Rey</p>", unsafe_allow_html=True)