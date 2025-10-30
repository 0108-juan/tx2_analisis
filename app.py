import streamlit as st
from textblob import TextBlob
from googletrans import Translator
from streamlit_lottie import st_lottie
import json
import requests

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Sentimientos",
    page_icon="😊",
    layout="centered"
)

# Cargar animaciones Lottie
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# URLs de animaciones Lottie
lottie_positive = "https://assets1.lottiefiles.com/packages/lf20_vybwn7df.json"
lottie_negative = "https://assets1.lottiefiles.com/packages/lf20_6q0bbj5z.json"
lottie_neutral = "https://assets1.lottiefiles.com/packages/lf20_6gzbqhhv.json"
lottie_welcome = "https://assets1.lottiefiles.com/packages/lf20_6cyslbfn.json"

# Cargar animaciones
positive_anim = load_lottie_url(lottie_positive)
negative_anim = load_lottie_url(lottie_negative)
neutral_anim = load_lottie_url(lottie_neutral)
welcome_anim = load_lottie_url(lottie_welcome)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .sentiment-positive {
        background-color: #D1FAE5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #10B981;
        margin: 1rem 0;
    }
    .sentiment-negative {
        background-color: #FEE2E2;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #EF4444;
        margin: 1rem 0;
    }
    .sentiment-neutral {
        background-color: #FEF3C7;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #F59E0B;
        margin: 1rem 0;
    }
    .metric-box {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #E2E8F0;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

translator = Translator()

# Header principal con animación
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<h1 class="main-title">😊 Analizador de Sentimientos</h1>', unsafe_allow_html=True)
    st.write("Descubre el sentimiento detrás de tus palabras")
with col2:
    if welcome_anim:
        st_lottie(welcome_anim, height=150, key="welcome")

# Sidebar informativo
with st.sidebar:
    st.markdown("### 📊 Métricas de Sentimiento")
    st.markdown("""
    <div style='background-color: #EFF6FF; padding: 1rem; border-radius: 8px;'>
    <strong>Polaridad:</strong> 
    <br>• -1 a -0.5: Negativo 😔
    <br>• -0.5 a 0.5: Neutral 😐  
    <br>• 0.5 a 1: Positivo 😊
    
    <br><br><strong>Subjetividad:</strong>
    <br>• 0 a 0.3: Muy Objetivo
    <br>• 0.3 a 0.7: Neutral
    <br>• 0.7 a 1: Muy Subjetivo
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 Consejos")
    st.write("""
    • Escribe frases completas
    • Usa palabras emocionales
    • Evita texto muy técnico
    • Sé específico en tus opiniones
    """)

# Pestañas para diferentes funcionalidades
tab1, tab2 = st.tabs(["📝 Análisis de Sentimiento", "🔧 Corrección de Texto"])

with tab1:
    st.subheader("Analiza el sentimiento de tu texto")
    
    text_input = st.text_area(
        "Escribe tu texto aquí:",
        placeholder="Por ejemplo: 'Estoy muy feliz con los resultados obtenidos hoy' o 'Me siento decepcionado con el servicio'",
        height=100
    )
    
    if st.button("🔍 Analizar Sentimiento", use_container_width=True):
        if text_input:
            with st.spinner('Analizando el sentimiento...'):
                # Traducir y analizar
                try:
                    translation = translator.translate(text_input, src="es", dest="en")
                    trans_text = translation.text
                    blob = TextBlob(trans_text)
                    
                    polarity = round(blob.sentiment.polarity, 2)
                    subjectivity = round(blob.sentiment.subjectivity, 2)
                    
                    # Mostrar métricas
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                        <div class="metric-box">
                        <h3>📈 Polaridad</h3>
                        <h2>{polarity}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-box">
                        <h3>🎯 Subjetividad</h3>
                        <h2>{subjectivity}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Mostrar resultado del sentimiento con animación
                    st.markdown("### 🎭 Resultado del Análisis")
                    
                    if polarity >= 0.3:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"""
                            <div class="sentiment-positive">
                            <h3>😊 Sentimiento Positivo</h3>
                            <p>Tu texto expresa emociones positivas. ¡Qué bueno!</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            if positive_anim:
                                st_lottie(positive_anim, height=100, key="positive")
                        
                        # Interacción basada en sentimiento positivo
                        st.success("🌟 **Sugerencia:** ¡Comparte tu energía positiva con los demás!")
                        
                    elif polarity <= -0.3:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"""
                            <div class="sentiment-negative">
                            <h3>😔 Sentimiento Negativo</h3>
                            <p>Tu texto expresa emociones negativas. ¡Ánimo!</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            if negative_anim:
                                st_lottie(negative_anim, height=100, key="negative")
                        
                        # Interacción basada en sentimiento negativo
                        st.info("💝 **Sugerencia:** Recuerda que cada día es una nueva oportunidad")
                        
                    else:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"""
                            <div class="sentiment-neutral">
                            <h3>😐 Sentimiento Neutral</h3>
                            <p>Tu texto es principalmente neutral u objetivo.</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            if neutral_anim:
                                st_lottie(neutral_anim, height=100, key="neutral")
                        
                        # Interacción basada en sentimiento neutral
                        st.warning("📝 **Sugerencia:** Intenta expresar más emociones en tu texto")
                    
                    # Información adicional
                    with st.expander("📖 Ver detalles del análisis"):
                        st.write(f"**Texto original:** {text_input}")
                        st.write(f"**Texto traducido:** {trans_text}")
                        st.write(f"**Longitud del texto:** {len(text_input)} caracteres")
                        
                except Exception as e:
                    st.error(f"Error en el análisis: {str(e)}")
        else:
            st.warning("⚠️ Por favor, escribe algún texto para analizar")

with tab2:
    st.subheader("Corrección de texto en inglés")
    st.write("Escribe texto en inglés para corregir la ortografía:")
    
    correction_text = st.text_area(
        "Texto en inglés:",
        placeholder="Enter your English text here for spelling correction...",
        height=100,
        key="correction"
    )
    
    if st.button("✏️ Corregir Texto", use_container_width=True):
        if correction_text:
            try:
                blob_correct = TextBlob(correction_text)
                corrected = blob_correct.correct()
                
                st.markdown("### 📝 Texto Corregido")
                st.success(corrected)
                
                # Mostrar diferencias
                if str(corrected) != correction_text:
                    st.info("🔍 Se realizaron correcciones en tu texto")
                else:
                    st.info("✅ Tu texto ya estaba correcto")
                    
            except Exception as e:
                st.error(f"Error en la corrección: {str(e)}")
        else:
            st.warning("⚠️ Por favor, escribe algún texto en inglés para corregir")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6B7280;'>"
    "Analizador de Sentimientos • Desarrollado con TextBlob y Streamlit"
    "</div>",
    unsafe_allow_html=True
)
