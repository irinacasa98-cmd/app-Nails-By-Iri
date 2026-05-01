import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"
ALIAS_PAGO = "irina.casa" 

st.set_page_config(page_title="Turnos - Nails by Iri", layout="centered", page_icon="💅🏻")

# --- DISEÑO ESTÉTICO ADAPTATIVO (CSS) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), 
                    url("https://images.unsplash.com/photo-1632345031435-8727f6897d53?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Tarjeta principal con fondo sólido para evitar conflictos de modo oscuro */
    [data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"] {{
        background-color: white !important;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }}

    /* Forzado de color de texto para que NO cambie con el modo del celular */
    .stMarkdown, p, span, label, li {{
        color: #2c2c2c !important; 
    }}

    h1, h2, h3 {{
        color: #d63384 !important;
        font-family: 'Playfair Display', serif;
        text-align: center;
    }}

    /* Botones Rosa */
    .stButton>button {{
        border-radius: 50px;
        background-color: #d63384;
        color: white !important;
        border: none;
        font-weight: bold;
        height: 3.5em;
        width: 100%;
    }}

    /* Cuadros de mensaje personalizados (Reemplazan st.warning y st.info) */
    .custom-alert {{
        background-color: #fff3cd;
        color: #856404 !important;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #ffeeba;
        margin-bottom: 20px;
    }}
    .custom-info {{
        background-color: #d1ecf1;
        color: #0c5460 !important;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #bee5eb;
        margin-bottom: 15px;
    }}
    .custom-error {{
        background-color: #f8d7da;
        color: #721c24 !important;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #f5c6cb;
        margin: 15px 0;
    }}
    
    .alias-box {{
        background-color: #fce4ec;
        padding: 20px;
        border-radius: 15px;
        border: 2px dashed #d63384;
        text-align: center;
        margin: 15px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

if 'paso' not in st.session_state:
    st.session_state.paso = 1

# --- PASO 1: BIENVENIDA ---
if st.session_state.paso == 1:
    st.markdown("<h1>💅🏻 Nails by Irina</h1>", unsafe_allow_html=True)
    st.progress(33)
    
    st.markdown("<h3>¡Hola! Bienvenida ✨</h3>", unsafe_allow_html=True)
    st.write("Confirmá que estás de acuerdo con nuestras políticas:")
    
    # Cuadro de políticas personalizado
    st.markdown("""
        <div class="custom-alert">
            • <b>Seña del 50%</b> para congelar el turno.<br>
            • Tenés <b>2 horas</b> para enviar el comprobante.<br>
            • El sistema libera el turno si no se registra el pago.
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("ACEPTO Y QUIERO RESERVAR ✨"):
        st.session_state.paso = 2
        st.rerun()

# --- PASO 2: CALENDARIO ---
elif st.session_state.paso == 2:
    st.markdown("<h2>📅 Reservá tu lugar</h2>", unsafe_allow_html=True)
    st.progress(66)
    
    if st.button("YA RESERVÉ, IR AL PAGO ➡️", key="top_next"):
        st.session_state.paso = 3
        st.rerun()

    st.markdown('<div class="custom-info">👇 Elegí día y hora aquí abajo y completá tus datos:</div>', unsafe_allow_html=True)
    
    components.iframe(LINK_CITAS_GOOGLE, height=600, scrolling=True)
    
    st.markdown('<div class="custom-error">⚠️ <b>IMPORTANTE:</b> Debes finalizar la reserva en el calendario de arriba antes de continuar.</div>', unsafe_allow_html=True)
    
    if st.button("CONTINUAR AL PAGO ➡️", key="bottom_next"):
        st.session_state.paso = 3
        st.rerun()
    
    if st.button("⬅️ Volver"):
        st.session_state.paso = 1
        st.rerun()

# --- PASO 3: PAGO ---
elif st.session_state.paso == 3:
    st.markdown("<h2>💰 Pago de la Seña</h2>", unsafe_allow_html=True)
    st.progress(100)
    
    st.write("Para confirmar tu turno, por favor realizá la transferencia de la seña:")
    
    st.markdown(f"""
        <div class="alias-box">
            <p style="margin:0; font-size:14px; color:#d63384 !important;">Alias para transferir:</p>
            <b style="font-size:22px; color:#d63384 !important;">{ALIAS_PAGO}</b>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    nombre = st.text_input("¿Tu nombre completo?")
    
    servicios = {
        "Semipermanente ($16.000) - Seña $8.000": "Semipermanente",
        "Kapping ($20.000) - Seña $10.000": "Kapping",
        "Esculpidas ($30.000) - Seña $15.000": "Esculpidas"
    }
    servicio_sel = st.selectbox("¿Qué servicio reservaste?", options=list(servicios.keys()))

    if st.button("ENVIAR COMPROBANTE POR WHATSAPP 📱"):
        if nombre:
            detalle = servicios[servicio_sel]
            msj = (f"¡Hola Irina! Soy *{nombre}*.\n"
                   f"Ya realicé la transferencia para mi turno de *{detalle}*.\n"
                   f"Adjunto el comprobante aquí abajo.")
            url_wa = f"https://wa.me/5491135677912?text={urllib.parse.quote(msj)}"
            
            st.markdown(f'''
                <a href="{url_wa}" target="_blank" style="text-decoration:none;">
                    <div style="text-align:center; padding:15px; background-color:#25D366; color:white; border-radius:50px; font-weight:bold;">
                        ABRIR MI WHATSAPP AHORA
                    </div>
                </a>
            ''', unsafe_allow_html=True)
        else:
            st.error("Por favor, ingresá tu nombre para continuar.")

    if st.button("⬅️ Ver calendario de nuevo"):
        st.session_state.paso = 2
        st.rerun()

st.markdown("<br><p style='text-align: center; font-size: 12px; color: gray;'>Nails by Irina • Paso del Rey</p>", unsafe_allow_html=True)