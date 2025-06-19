import os
import tempfile
from pathlib import Path

import pandas as pd
import requests
import streamlit as st
from PIL import Image
from autogluon.multimodal import MultiModalPredictor

# Konfiguracja strony Streamlit
st.set_page_config(page_title="Pokédex AI", layout="centered")

# Styl CSS
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    .animated-title {
        text-align: center;
        color: #FFCB05;
        font-family: 'Press Start 2P', cursive;
        animation: glow 2s infinite;
        font-size: 36px;
        margin-bottom: 20px;
    }
    @keyframes glow {
        0% { text-shadow: 0 0 5px #3B4CCA; }
        50% { text-shadow: 0 0 20px #3B4CCA; }
        100% { text-shadow: 0 0 5px #3B4CCA; }
    }
    .fade-in-slide {
        animation: fadeSlideIn 1s ease-in-out;
    }
    @keyframes fadeSlideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    button[kind="primary"] {
        background-color: #3B4CCA !important;
        color: white !important;
        animation: pulse 2s infinite;
    }
    button:hover {
        filter: brightness(1.1);
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(59, 76, 202, 0.5); }
        70% { box-shadow: 0 0 0 10px rgba(59, 76, 202, 0); }
        100% { box-shadow: 0 0 0 0 rgba(59, 76, 202, 0); }
    }
    .clear-button {
        background-color: #FF5252;
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 30px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .clear-button:hover {
        background-color: #E53935;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Wyświetlenie tytułu i nagłówka aplikacji
st.markdown("<div class='animated-title'>Pokédex AI</div>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Klasyfikator Pokémonów</h4>", unsafe_allow_html=True)
st.divider()

# Funkcja do ładowania modelu AutoGluon
@st.cache_resource
def load_model():
    try:
        base_model_dir = Path("AutogluonModels")
        if not base_model_dir.is_dir():
            raise FileNotFoundError("Brakuje folderu z modelem 'AutogluonModels'.")
        versions = sorted(
            [d for d in base_model_dir.iterdir() if d.is_dir()],
            key=lambda d: os.path.getmtime(d),
            reverse=True,
        )
        if not versions:
            raise FileNotFoundError("Nie znaleziono żadnych wersji modelu w katalogu.")
        latest_model_path = versions[0]
        st.info(f"📦 Ładowanie modelu: {latest_model_path.name}")
        return MultiModalPredictor.load(path=str(latest_model_path))
    except Exception as e:
        st.error(f"Błąd podczas ładowania modelu: {e}")
        return None

# Wczytanie modelu
predictor = load_model()
if predictor is None:
    st.error("Nie można kontynuować bez załadowanego modelu.")
    st.stop()

# Inicjalizacja stanu aplikacji
for key in ["uploaded_file", "predicted", "processing", "done"]:
    if key not in st.session_state:
        st.session_state[key] = False

# Sekcja uploadu pliku
st.subheader("Wgraj zdjęcie Pokémona")
uploaded = st.file_uploader("Wybierz plik", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
if uploaded:
    st.session_state.uploaded_file = uploaded
    st.session_state.predicted = False
    st.session_state.processing = False
    st.session_state.done = False

# Przycisk klasyfikacji
if st.session_state.uploaded_file:
    if st.button("🔍 Rozpoznaj Pokémona", use_container_width=True):
        st.session_state.processing = True
        st.session_state.done = False

        with st.spinner("🔎 Analiza zdjęcia w toku..."):
            try:
                image = Image.open(st.session_state.uploaded_file).convert("RGB")
                st.markdown('<div class="fade-in-slide">', unsafe_allow_html=True)
                st.image(image, caption="Wgrane zdjęcie", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image_file:
                    image.save(temp_image_file, format="PNG")
                    temp_image_path = temp_image_file.name

                try:
                    data_to_predict = pd.DataFrame([{"image": temp_image_path}])
                    predictions = predictor.predict(data_to_predict, as_pandas=False)
                    predicted_label = predictions[0]
                    probabilities = predictor.predict_proba(data_to_predict, as_pandas=True)
                    confidence = probabilities[predicted_label].iloc[0]

                    poke_name = predicted_label.lower().replace(" ", "-").replace(".", "").replace("'", "")
                    api_url = f"https://pokeapi.co/api/v2/pokemon/{poke_name}"
                    r = requests.get(api_url)

                    if r.status_code == 200:
                        data = r.json()
                        st.session_state.predicted = True
                        st.session_state.processing = False
                        st.session_state.done = True

                        st.markdown('<div class="fade-in-slide">', unsafe_allow_html=True)
                        st.success(f"✅ Rozpoznano: **{predicted_label}** ({confidence:.2%} pewności)")
                        st.markdown("### Informacje o Pokémonie:")
                        st.markdown(f"**🔹 Nazwa:** {data['name'].capitalize()}")
                        st.markdown(f"**📊 Doświadczenie bazowe:** {data['base_experience']}")
                        st.markdown(f"**📏 Wzrost:** {data['height'] / 10} m")
                        st.markdown(f"**⚖️ Waga:** {data['weight'] / 10} kg")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("Nie znaleziono informacji o tym Pokémonie.")
                        st.session_state.processing = False
                        st.session_state.done = False
                finally:
                    if os.path.exists(temp_image_path):
                        os.remove(temp_image_path)

            except Exception as e:
                st.session_state.processing = False
                st.session_state.done = False
                st.error(f"Wystąpił błąd: {e}")

# Przycisk resetujący aplikację
if st.session_state.predicted and st.session_state.done:
    st.divider()
    st.markdown("""
        <div style="text-align: center;">
            <form action="?">
                <button class="clear-button" type="submit">Wyczyść wszystko</button>
            </form>
    """, unsafe_allow_html=True)

# Stopka
st.divider()
st.caption("PokedexAI – wspierany przez AutoGluon i PokéAPI.")
