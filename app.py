import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"
ALIAS_PAGO = "irina.casa"  # <-- CAMBIA ESTO POR TU ALIAS REAL

st.set_page_config(page_title="Turnos - Nails by Iri", layout="centered", page_icon="💅🏻")

# --- DISEÑO ESTÉTICO ADAPTATIVO (CSS) ---
st.markdown(f"""
    <style>
    /* Fondo con imagen y degradado */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), 
                    url("https://images.unsplash.com/photo-1632345031435-8727f6897d53?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Tarjetas con opacidad alta para asegurar legibilidad de texto negro/rosa */
    [data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"] {{
        background-color: rgba(255, 255, 255, 0.98);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}

    /* Forzar color de texto para modo claro/oscuro */
    .stMarkdown, p, span, label {{
        color: #1a1a1a !important; /* Gris muy oscuro, casi negro, legible en todo */
    }}

    h1, h2, h3 {{
        color: #d63384 !important;
        font-family: 'Playfair Display', serif;
    }}

    /* Botones personalizados */
    .stButton>button {{
        border-radius: 50px;
        background-color: #d63384;
        color: white !important;
        border: none;
        font-weight: bold;
        transition: all 0.3s;
    }}
    
    /* Estilo especial para el Alias */
    .alias-box {{
        background-color: #fce4ec;
        padding: 15px;
        border-radius: 15px;
        border: 2px dashed #d63384;
        text-align: center;
        margin: 10px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

# Inicializar paso
if 'paso' not in st.session_state:
    st.session_state.paso = 1

# --- FLUJO POR PASOS ---

# PASO 1: BIENVENIDA
if st.session_state.paso == 1:
    st.markdown("<h1 style='text-align: center;'>💅🏻 Nails by Irina</h1>", unsafe_allow_html=True)
    st.progress(33)
    
    with st.container():
        st.subheader("¡Hola! Bienvenida ✨")
        st.write("Confirmá que estás de acuerdo con nuestras políticas:")
        st.warning("""
        * **Seña del 50%** para congelar el turno.
        * Tenés **2 horas** para enviar el comprobante.
        * El sistema libera el turno si no se registra el pago.
        """)
        
        if st.button("ACEPTO Y QUIERO RESERVAR ✨", use_container_width=True):
            st.session_state.paso = 2
            st.rerun()

# PASO 2: EL CALENDARIO
elif st.session_state.paso == 2:
    st.markdown("<h2 style='text-align: center;'>📅 Reservá tu lugar</h2>", unsafe_allow_html=True)
    st.progress(66)
    
    # Botón superior para las que ya saben usarlo
    if st.button("YA RESERVÉ, IR AL PAGO ➡️", key="top_next", use_container_width=True):
        st.session_state.paso = 3
        st.rerun()

    st.info("👇 Elegí día y hora aquí abajo y completá tus datos:")
    components.iframe(LINK_CITAS_GOOGLE, height=600, scrolling=True)
    
    st.error("⚠️ **IMPORTANTE:** Debes finalizar la reserva en el calendario de arriba antes de continuar.")
    
    if st.button("CONTINUAR AL PAGO ➡️", key="bottom_next", use_container_width=True):
        st.session_state.paso = 3
        st.rerun()
    
    if st.button("⬅️ Volver", use_container_width=True):
        st.session_state.paso = 1
        st.rerun()

# PASO 3: DATOS DE PAGO Y WHATSAPP
elif st.session_state.paso == 3:
    st.markdown("<h2 style='text-align: center;'>💰 Pago de la Seña</h2>", unsafe_allow_html=True)
    st.progress(100)
    
    with st.container():
        st.write("Para confirmar tu turno, por favor realizá la transferencia de la seña:")
        
        # Bloque de Alias
        st.markdown(f"""
            <div class="alias-box">
                <p style="margin:0; font-size:14px;">Alias para transferir:</p>
                <b style="font-size:20px; color:#d63384;">{ALIAS_PAGO}</b>
            </div>
        """, unsafe_allow_html=True)
        
        st.caption("Copiá el alias y realizá la transferencia desde tu Home Banking.")
        
        st.markdown("---")
        nombre = st.text_input("¿Tu nombre completo?")
        
        servicios = {
            "Semipermanente ($16.000) - Seña $8.000": "Semipermanente",
            "Kapping ($20.000) - Seña $10.000": "Kapping",
            "Esculpidas ($30.000) - Seña $15.000": "Esculpidas"
        }
        servicio_sel = st.selectbox("¿Qué servicio reservaste?", options=list(servicios.keys()))

        if st.button("ENVIAR COMPROBANTE POR WHATSAPP 📱", use_container_width=True):
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

    if st.button("⬅️ Ver calendario de nuevo", use_container_width=True):
        st.session_state.paso = 2
        st.rerun()

st.markdown("<br><p style='text-align: center; font-size: 12px; color: gray;'>Nails by Irina • Paso del Rey</p>", unsafe_allow_html=True)