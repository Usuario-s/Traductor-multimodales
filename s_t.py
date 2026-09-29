```python
import os
import streamlit as st
from bokeh.models.widgets import Button
#from bokeh.io import show
#from bokeh.models import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from gtts import gTTS
from googletrans import Translator


# ============================================================
# DISEÑO ROBÓTICO
# ============================================================

st.set_page_config(
    page_title="ROBOT TRANSLATOR",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>

    /* FONDO GENERAL */
    .stApp {
        background:
            radial-gradient(circle at 50% 0%,
                rgba(0, 255, 255, 0.10),
                transparent 35%),
            linear-gradient(180deg, #050b10 0%, #020508 100%);
        color: #d8ffff;
    }

    /* LÍNEAS Y TEXTO GENERAL */
    * {
        font-family: "Courier New", monospace;
    }

    /* TITULO PRINCIPAL */
    h1 {
        color: #00ffff !important;
        text-align: center;
        letter-spacing: 6px;
        text-shadow:
            0 0 5px #00ffff,
            0 0 15px #00ffff,
            0 0 30px rgba(0,255,255,0.5);
        font-weight: 700;
    }

    h2, h3 {
        color: #8fffff !important;
        letter-spacing: 2px;
    }

    /* SUBTITULO */
    .stApp p {
        color: #b9dada;
    }

    /* PANEL PRINCIPAL */
    [data-testid="stVerticalBlock"] {
        border-radius: 8px;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #07151b 0%,
                #03080c 100%
            );
        border-right: 1px solid #00ffff;
        box-shadow: 5px 0 25px rgba(0,255,255,0.08);
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #00ffff !important;
        text-shadow: 0 0 10px #00ffff;
    }

    /* INPUTS Y SELECTBOX */
    div[data-baseweb="select"] > div {
        background-color: #07151b !important;
        border: 1px solid #008f9c !important;
        color: #00ffff !important;
    }

    div[data-baseweb="select"] > div:hover {
        border: 1px solid #00ffff !important;
        box-shadow: 0 0 10px rgba(0,255,255,0.35);
    }

    /* BOTONES STREAMLIT */
    .stButton > button {
        width: 100%;
        background: #07151b;
        color: #00ffff;
        border: 1px solid #00ffff;
        border-radius: 4px;
        padding: 10px;
        font-family: "Courier New", monospace;
        font-weight: bold;
        letter-spacing: 2px;
        transition: all 0.2s ease;
        box-shadow:
            0 0 5px rgba(0,255,255,0.3),
            inset 0 0 10px rgba(0,255,255,0.05);
    }

    .stButton > button:hover {
        background: #00ffff;
        color: #021014;
        box-shadow:
            0 0 10px #00ffff,
            0 0 25px rgba(0,255,255,0.5);
        transform: scale(1.01);
    }

    /* CHECKBOX */
    .stCheckbox label {
        color: #9fffff !important;
    }

    /* IMAGEN */
    img {
        border: 1px solid #00ffff;
        box-shadow:
            0 0 10px rgba(0,255,255,0.25),
            inset 0 0 20px rgba(0,255,255,0.1);
    }

    /* TEXTO DE SALIDA */
    [data-testid="stMarkdownContainer"] {
        color: #d8ffff;
    }

    /* AUDIO */
    audio {
        width: 100%;
        filter: sepia(20%) saturate(150%) hue-rotate(130deg);
    }

    /* BLOQUES DE INFORMACIÓN */
    div[data-testid="stAlert"] {
        background: #061319;
        border: 1px solid #008f9c;
        color: #bfffff;
    }

    /* SEPARADORES */
    hr {
        border-color: #008f9c !important;
        box-shadow: 0 0 5px rgba(0,255,255,0.3);
    }

    /* EFECTO DE CURSOR */
    .robot-status {
        color: #00ffff;
        text-align: center;
        font-size: 12px;
        letter-spacing: 3px;
        margin-bottom: 20px;
        text-shadow: 0 0 8px #00ffff;
    }

    /* PANEL HUD */
    .hud-panel {
        border: 1px solid #008f9c;
        background: rgba(3, 14, 19, 0.85);
        padding: 15px;
        margin: 10px 0 20px 0;
        box-shadow:
            0 0 10px rgba(0,255,255,0.08),
            inset 0 0 20px rgba(0,255,255,0.03);
    }

    .hud-title {
        color: #00ffff;
        font-size: 13px;
        letter-spacing: 3px;
        margin-bottom: 8px;
    }

    .hud-text {
        color: #91baba;
        font-size: 12px;
        line-height: 1.6;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# INTERFAZ
# ============================================================

st.markdown("""
<div class="robot-status">
    ● SYSTEM ONLINE &nbsp; // &nbsp; TRANSLATION MODULE ACTIVE
</div>
""", unsafe_allow_html=True)

st.title("TRADUCTOR")

st.markdown("""
<div class="hud-panel">
    <div class="hud-title">[ VOICE INPUT MODULE ]</div>
    <div class="hud-text">
        Sistema preparado para recibir comandos de voz.
        Presiona el botón de escucha y comienza a hablar.
    </div>
</div>
""", unsafe_allow_html=True)

st.subheader("Escucho lo que quieres traducir.")


image = Image.open('OIG7.jpg')

st.image(image, width=300)


with st.sidebar:

    st.markdown("""
    <div class="hud-panel">
        <div class="hud-title">🤖 ROBOT TRANSLATOR</div>

        <div class="hud-text">
        SYSTEM STATUS: ONLINE<br>
        VOICE SYSTEM: READY<br>
        TRANSLATION: READY<br>
        AUDIO OUTPUT: READY
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Traductor.")

    st.write(
        "Presiona el botón, cuando escuches la señal "
        "habla lo que quieres traducir, luego selecciona "
        "la configuración de lenguaje que necesites."
    )


st.write("Toca el Botón y habla lo que quieres traducir")


# ============================================================
# BOTÓN DE RECONOCIMIENTO DE VOZ
# ============================================================

stt_button = Button(
    label=" ESCUCHAR  🎤",
    width=300,
    height=50
)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'es-ES';

    recognition.onresult = function (e) {

        var value = "";

        for (
            var i = e.resultIndex;
            i < e.results.length;
            ++i
        ) {

            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }

        }

        if (value != "") {

            document.dispatchEvent(
                new CustomEvent(
                    "GET_TEXT",
                    {detail: value}
                )
            );

        }

    }

    recognition.onend = function() {
        console.log("Reconocimiento detenido");
    }

    recognition.start();

"""))


result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)


# ============================================================
# RESULTADO
# ============================================================

if result:

    if "GET_TEXT" in result:

        st.markdown("""
        <div class="hud-panel">
            <div class="hud-title">
                [ VOICE DATA RECEIVED ]
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write(result.get("GET_TEXT"))


    try:
        os.mkdir("temp")
    except:
        pass


    st.title("Texto a Audio")

    translator = Translator()

    text = str(result.get("GET_TEXT"))


    # ========================================================
    # IDIOMA ENTRADA
    # ========================================================

    in_lang = st.selectbox(
        "Selecciona el lenguaje de Entrada",
        (
            "Inglés",
            "Español",
            "Bengali",
            "Coreano",
            "Mandarín",
            "Japonés"
        ),
    )


    if in_lang == "Inglés":
        input_language = "en"

    elif in_lang == "Español":
        input_language = "es"

    elif in_lang == "Bengali":
        input_language = "bn"

    elif in_lang == "Coreano":
        input_language = "ko"

    elif in_lang == "Mandarín":
        input_language = "zh-cn"

    elif in_lang == "Japonés":
        input_language = "ja"


    # ========================================================
    # IDIOMA SALIDA
    # ========================================================

    out_lang = st.selectbox(
        "Selecciona el lenguaje de salida",
        (
            "Inglés",
            "Español",
            "Bengali",
            "Coreano",
            "Mandarín",
            "Japonés"
        ),
    )


    if out_lang == "Inglés":
        output_language = "en"

    elif out_lang == "Español":
        output_language = "es"

    elif out_lang == "Bengali":
        output_language = "bn"

    elif out_lang == "Coreano":
        output_language = "ko"

    elif out_lang == "Mandarín":
        output_language = "zh-cn"

    elif out_lang == "Japonés":
        output_language = "ja"


    # ========================================================
    # ACENTO
    # ========================================================

    english_accent = st.selectbox(
        "Selecciona el acento",
        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canada",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )


    if english_accent == "Defecto":
        tld = "com"

    elif english_accent == "Español":
        tld = "com.mx"

    elif english_accent == "Reino Unido":
        tld = "co.uk"

    elif english_accent == "Estados Unidos":
        tld = "com"

    elif english_accent == "Canada":
        tld = "ca"

    elif english_accent == "Australia":
        tld = "com.au"

    elif english_accent == "Irlanda":
        tld = "ie"

    elif english_accent == "Sudáfrica":
        tld = "co.za"


    # ========================================================
    # TEXT TO SPEECH
    # ========================================================

    def text_to_speech(
        input_language,
        output_language,
        text,
        tld
    ):

        translation = translator.translate(
            text,
            src=input_language,
            dest=output_language
        )

        trans_text = translation.text

        tts = gTTS(
            trans_text,
            lang=output_language,
            tld=tld,
            slow=False
        )

        try:
            my_file_name = text[0:20]

        except:
            my_file_name = "audio"

        tts.save(
            f"temp/{my_file_name}.mp3"
        )

        return my_file_name, trans_text


    # ========================================================
    # MOSTRAR TEXTO
    # ========================================================

    display_output_text = st.checkbox(
        "Mostrar el texto"
    )


    # ========================================================
    # CONVERTIR
    # ========================================================

    if st.button("CONVERTIR"):

        result, output_text = text_to_speech(
            input_language,
            output_language,
            text,
            tld
        )

        audio_file = open(
            f"temp/{result}.mp3",
            "rb"
        )

        audio_bytes = audio_file.read()

        st.markdown(
            "## Tú audio:"
        )

        st.audio(
            audio_bytes,
            format="audio/mp3",
            start_time=0
        )


        if display_output_text:

            st.markdown(
                "## Texto de salida:"
            )

            st.write(
                f" {output_text}"
            )


    # ========================================================
    # ELIMINAR ARCHIVOS ANTIGUOS
    # ========================================================

    def remove_files(n):

        mp3_files = glob.glob(
            "temp/*mp3"
        )

        if len(mp3_files) != 0:

            now = time.time()

            n_days = n * 86400

            for f in mp3_files:

                if os.stat(f).st_mtime < now - n_days:

                    os.remove(f)

                    print(
                        "Deleted ",
                        f
                    )


    remove_files(7)
```

           


        
    



        
    


