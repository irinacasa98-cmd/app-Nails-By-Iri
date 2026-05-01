import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# --- CONFIGURACIÓN ---
LINK_CITAS_GOOGLE = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ3-lDy6ICRk0OrhYm2IxKSub_XKS-d-BijdvSK77zL1CcXgAfTTsIVtjw46IKE42NYAjy5QOp4h?gv=true"

st.set_page_config(page_title="Turnos - Nails by Iri", layout="centered", page_icon="💅🏻")

# --- DISEÑO ESTÉTICO (CSS) ---
st.markdown(f"""
    <style>
    /* Fondo con imagen estética y degradado */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), 
                    url("https://images.unsplash.com/photo-1632345031435-8727f6897d53?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Estilo para los contenedores (Tarjetas blancas semi-transparentes) */
    [data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"] {{
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}

    /* Títulos y fuentes */
    h1, h2, h3 {{
        color: #d63384 !important; /* Rosa Nails */
        font-family: 'Playfair Display', serif;
    }}

    /* Botones personalizados */
    .stButton>button {{
        border-radius: 50px;
        background-color: #d63384;
        color: white;
        border: none;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #b02a6b;
        transform: scale(1.02);
    }}
    </style>
    """, unsafe_allow_html=True)

# Inicializar paso
if 'paso' not in st.session_state:
    st.session_state.paso = 1

# --- FLUJO POR PASOS ---

# PASO 1: BIENVENIDA Y REGLAS
if st.session_state.paso == 1:
    st.markdown("<h1 style='text-align: center;'>💅🏻 Nails by Irina</h1>", unsafe_allow_html=True)
    st.progress(33)
    
    with st.container():
        st.subheader("¡Hola! Bienvenida ✨")
        st.write("Para reservar, por favor confirmá que estás de acuerdo:")
        st.warning("""
        * **Seña del 50%** necesaria para congelar el turno.
        * Tenés **2 horas** para enviar el comprobante.
        * El sistema libera el turno si no se registra el pago.
        """)
        
        if st.button("ACEPTO Y QUIERO RESERVAR ✨", use_container_width=True):
            st.session_state.paso = 2
            st.rerun()

# PASO 2: EL CALENDARIO
elif st.session_state.paso == 2:
    st.markdown("<h2 style='text-align: center;'>📅 Elegí tu momento</h2>", unsafe_allow_html=True)
    st.progress(66)
    
    components.iframe(LINK_CITAS_GOOGLE, height=550, scrolling=True)
    
    st.markdown("---")
    
    # --- MENSAJE DE IMPORTANCIA (REEMPLAZA AL CHECKBOX) ---
    st.error("⚠️ **IMPORTANTE:** Debes seleccionar un día y horario en el calendario de arriba y completar el formulario de Google para que tu reserva sea válida.")
    st.info("Si ya finalizaste tu registro en el calendario, dale a 'Continuar'.")
    
    if st.button("CONTINUAR AL PAGO ➡️", use_container_width=True):
        st.session_state.paso = 3
        st.rerun()
    
    if st.button("⬅️ Volver", use_container_width=True):
        st.session_state.paso = 1
        st.rerun()

# PASO 3: CONFIRMACIÓN WHATSAPP
elif st.session_state.paso == 3:
    st.markdown("<h2 style='text-align: center;'>💖 Paso Final</h2>", unsafe_allow_html=True)
    st.progress(100)
    
    with st.container():
        st.write("Completá los detalles para la confirmación final.")
        
        nombre = st.text_input("¿Cómo es tu nombre?")
        
        servicios = {
            "Semipermanente ($16.000)": "Semipermanente - $16.000",
            "Kapping ($20.000)": "Kapping - $20.000",
            "Esculpidas ($30.000)": "Esculpidas - $30.000"
        }
        servicio_sel = st.selectbox("¿Qué servicio elegiste?", options=list(servicios.keys()))

        if st.button("ABRIR WHATSAPP PARA SEÑA 📱", use_container_width=True):
            if nombre:
                detalle = servicios[servicio_sel]
                msj = (f"¡Hola Irina! Soy *{nombre}*.\n"
                       f"Reservé mi turno para *{detalle}*.\n"
                       f"Acá te mando el comprobante de la seña.")
                url_wa = f"https://wa.me/5491135677912?text={urllib.parse.quote(msj)}"
                
                st.markdown(f'''
                    <a href="{url_wa}" target="_blank" style="text-decoration:none;">
                        <div style="text-align:center; padding:15px; background-color:#25D366; color:white; border-radius:50px; font-weight:bold;">
                            CLICK AQUÍ PARA ENVIAR COMPROBANTE
                        </div>
                    </a>
                ''', unsafe_allow_html=True)
            else:
                st.error("Por favor, poné tu nombre.")

    if st.button("⬅️ Ver calendario de nuevo", use_container_width=True):
        st.session_state.paso = 2
        st.rerun()

st.markdown("<br><p style='text-align: center; font-size: 12px; color: gray;'>Nails by Irina • Paso del Rey</p>", unsafe_allow_html=True)