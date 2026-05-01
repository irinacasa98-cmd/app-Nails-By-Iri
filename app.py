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

    [data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"] {{
        background-color: white !important;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }}

    .stMarkdown, p, span, label, li {{
        color: #2c2c2c !important; 
    }}

    h1, h2, h3 {{
        color: #d63384 !important;
        font-family: 'Playfair Display', serif;
        text-align: center;
    }}

    .stButton>button {{
        border-radius: 50px;
        background-color: #d63384;
        color: white !important;
        border: none;
        font-weight: bold;
        height: 3.5em;
        width: 100%;
    }}

    .custom-alert {{
        background-color: #fff3cd;
        color: #856404 !important;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #ffeeba;
        margin-bottom: 20px;
    }}

    .custom-error {{
        background-color: #f8d7da;
        color: #721c24 !important;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #f5c6cb;
        margin: 15px 0;
    }}

    /* CAJA UNIFICADA DE ALIAS */
    .unified-alias-box {{
        background-color: #fce4ec;
        border: 2px dashed #d63384;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
    }}
    
    .alias-title {{
        color: #d63384 !important;
        font-weight: bold;
        margin-bottom: 10px;
        font-size: 16px;
    }}

    .alias-value {{
        font-family: monospace;
        font-size: 24px;
        color: #2c2c2c !important;
        display: block;
        margin-bottom: 15px;
        background: white;
        padding: 10px;
        border-radius: 10px;
    }}

    .copy-button-custom {{
        background-color: #d63384;
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 50px;
        cursor: pointer;
        font-weight: bold;
        font-size: 14px;
        transition: 0.3s;
    }}
    
    .copy-button-custom:active {{
        transform: scale(0.95);
        background-color: #b02a6b;
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
    
    st.markdown('<div class="custom-error">⚠️ <b>IMPORTANTE:</b> Primero seleccioná el día y la hora abajo y completá tus datos.</div>', unsafe_allow_html=True)

    if st.button("YA RESERVÉ, IR AL PAGO ➡️", key="top_next"):
        st.session_state.paso = 3
        st.rerun()
    
    st.write("")
    components.iframe(LINK_CITAS_GOOGLE, height=600, scrolling=True)
    st.write("")

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
    
    st.write("Realizá la transferencia de la seña para confirmar:")
    
    # CAJA UNIFICADA TOTALMENTE PERSONALIZADA
    st.markdown(f"""
        <div class="unified-alias-box">
            <div class="alias-title">Alias para transferir:</div>
            <div class="alias-value" id="copyText">{ALIAS_PAGO}</div>
            <button class="copy-button-custom" onclick="copyAliasUnificado()">📋 COPIAR ALIAS</button>
        </div>

        <script>
        function copyAliasUnificado() {{
            const textToCopy = document.getElementById('copyText').innerText;
            const tempInput = document.createElement('input');
            tempInput.value = textToCopy;
            document.body.appendChild(tempInput);
            tempInput.select();
            tempInput.setSelectionRange(0, 99999);
            document.execCommand('copy');
            document.body.removeChild(tempInput);
            alert('¡Alias copiado!: ' + textToCopy);
        }}
        </script>
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