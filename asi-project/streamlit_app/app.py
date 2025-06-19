import os
import tempfile
from pathlib import Path

import pandas as pd
import requests
import streamlit as st
from autogluon.multimodal import MultiModalPredictor
from PIL import Image

st.set_page_config(page_title="Pokédex AI", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>Pokédex AI</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h4 style='text-align: center;'>Klasyfikator Pokémonów</h4>",
    unsafe_allow_html=True,
)
st.divider()


@st.cache_resource
def load_model():
    """
    Dynamicznie znajduje i ładuje najnowszą wersję modelu AutoGluon
    z domyślnej lokalizacji 'AutogluonModels'.
    """
    try:
        base_model_dir = Path("AutogluonModels")

        if not base_model_dir.is_dir():
            raise FileNotFoundError(
                f"Folder bazowy modelu nie istnieje: '{base_model_dir}'"
            )

        versions = sorted(
            [d for d in base_model_dir.iterdir() if d.is_dir()],
            key=lambda d: os.path.getmtime(d),
            reverse=True,
        )

        if not versions:
            raise FileNotFoundError(
                f"Nie znaleziono żadnych wersji modelu w '{base_model_dir}'"
            )

        latest_model_path = versions[0]
        st.info(f"Ładowanie modelu z najnowszej wersji: {latest_model_path.name}")

        predictor = MultiModalPredictor.load(path=str(latest_model_path))
        return predictor

    except FileNotFoundError as e:
        st.error(f"Błąd krytyczny: {e}")
        st.error(
            "Sprawdź, czy folder 'AutogluonModels' istnieje i czy model"
            " został pobrany (np. przez 'dvc pull')."
        )
        return None
    except Exception as e:
        st.error(f"Wystąpił nieoczekiwany błąd podczas ładowania modelu: {e}")
        return None


predictor = load_model()

if predictor is None:
    st.error("Model nie został załadowany. Aplikacja nie może kontynuować.")
    st.stop()

for key in ["uploaded_file", "predicted", "processing", "done"]:
    if key not in st.session_state:
        st.session_state[key] = False

st.subheader("Wgraj zdjęcie Pokémona")
uploaded = st.file_uploader(
    "Wybierz plik", type=["png", "jpg", "jpeg"], label_visibility="collapsed"
)

if uploaded:
    st.session_state.uploaded_file = uploaded
    st.session_state.predicted = False
    st.session_state.processing = False
    st.session_state.done = False

if st.session_state.uploaded_file:
    if st.button("Rozpoznaj Pokémona", use_container_width=True):
        if st.session_state.uploaded_file is not None:
            st.session_state.processing = True
            st.session_state.done = False
            st.info("Analizuję zdjęcie...")

            try:
                image = Image.open(st.session_state.uploaded_file).convert("RGB")
                st.image(image, caption="Wgrane zdjęcie", use_container_width=True)

                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".png"
                ) as temp_image_file:
                    image.save(temp_image_file, format="PNG")
                    temp_image_path = temp_image_file.name

                try:
                    data_to_predict = pd.DataFrame([{"image": temp_image_path}])

                    predictions = predictor.predict(data_to_predict, as_pandas=False)
                    predicted_label = predictions[0]

                    probabilities = predictor.predict_proba(
                        data_to_predict, as_pandas=True
                    )
                    confidence = probabilities[predicted_label].iloc[0]

                    poke_name = (
                        predicted_label.lower()
                        .replace(" ", "-")
                        .replace(".", "")
                        .replace("'", "")
                    )
                    api_url = f"https://pokeapi.co/api/v2/pokemon/{poke_name}"
                    r = requests.get(api_url)

                    if r.status_code == 200:
                        data = r.json()
                        st.session_state.predicted = True
                        st.session_state.processing = False
                        st.session_state.done = True

                        st.success(
                            f"Rozpoznano: {predicted_label} "
                            f"({confidence:.2%} pewności)"
                        )
                        st.markdown("### Informacje o Pokémonie:")
                        st.markdown(f"**Nazwa:** {data['name'].capitalize()}")
                        st.markdown(
                            f"**Doświadczenie bazowe:** {data['base_experience']}"
                        )
                        st.markdown(f"**Wzrost:** {data['height'] / 10} m")
                        st.markdown(f"**Waga:** {data['weight'] / 10} kg")
                    else:
                        st.session_state.processing = False
                        st.session_state.done = False
                        st.warning("Nie znaleziono informacji w PokéAPI.")

                finally:
                    if os.path.exists(temp_image_path):
                        os.remove(temp_image_path)

            except Exception as e:
                st.session_state.processing = False
                st.session_state.done = False
                st.error(f"Wystąpił błąd: {e}")
        else:
            st.warning("Najpierw wgraj zdjęcie Pokémona.")

if st.session_state.predicted and st.session_state.done:
    st.divider()
    if st.button("Wyczyść wszystko", type="primary", use_container_width=True):
        for key in ["uploaded_file", "predicted", "processing", "done"]:
            st.session_state[key] = False
        st.query_params.clear()

st.divider()
st.caption("PokedexAI – wspierany przez AutoGluon i PokéAPI.")
