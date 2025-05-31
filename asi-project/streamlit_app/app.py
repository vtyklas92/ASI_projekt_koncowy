import streamlit as st
from PIL import Image
from transformers import ViTForImageClassification, ViTFeatureExtractor
import torch
import requests
import time

# Ustawienia strony
st.set_page_config(page_title="Pokédex AI", page_icon="🧠", layout="centered")

# Nagłówek
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🧠 Pokédex AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>  Klasyfikator Pokémonów</h4>", unsafe_allow_html=True)
st.divider()

# Wczytaj model i ekstraktor
@st.cache_resource
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ViTForImageClassification.from_pretrained("imjeffhi/pokemon_classifier").to(device)
    extractor = ViTFeatureExtractor.from_pretrained("imjeffhi/pokemon_classifier")
    return model, extractor, device

model, feature_extractor, device = load_model()

# Inicjalizacja stanu
for key in ["uploaded_file", "predicted", "processing", "done"]:
    if key not in st.session_state:
        st.session_state[key] = False

# Wgrywanie zdjęcia
st.subheader("📸 Wgraj zdjęcie Pokémona")
uploaded = st.file_uploader("Wybierz plik", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

if uploaded:
    st.session_state.uploaded_file = uploaded
    st.session_state.predicted = False
    st.session_state.processing = False
    st.session_state.done = False

# Przycisk Rozpoznaj
if st.session_state.uploaded_file:
    if st.button("🔍 Rozpoznaj Pokémona", use_container_width=True):
        if st.session_state.uploaded_file is not None:
            st.session_state.processing = True
            st.session_state.done = False
            st.info("🔎 Analizuję zdjęcie...")

            try:
                # Wczytaj i pokaż obrazek
                image = Image.open(st.session_state.uploaded_file).convert("RGB")
                st.image(image, caption="Wgrane zdjęcie", use_container_width=True)

                # Przetworzenie obrazu
                inputs = feature_extractor(images=image, return_tensors="pt").to(device)

                # Predykcja
                outputs = model(**inputs)
                predicted_id = outputs.logits.argmax(-1).item()
                predicted_label = model.config.id2label[predicted_id]
                confidence = torch.nn.functional.softmax(outputs.logits, dim=1)[0][predicted_id].item()

                # Pobranie informacji z PokéAPI
                poke_name = predicted_label.lower().replace(" ", "-").replace(".", "").replace("'", "")
                api_url = f"https://pokeapi.co/api/v2/pokemon/{poke_name}"
                r = requests.get(api_url)

                if r.status_code == 200:
                    data = r.json()
                    st.session_state.predicted = True
                    st.session_state.processing = False
                    st.session_state.done = True

                    # Wyświetlanie informacji
                    st.success(f"✅ Rozpoznano: **{predicted_label}** ({confidence:.2%} pewności)")
                    st.markdown("### 📘 Informacje o Pokémonie:")
                    st.markdown(f"**Nazwa:** {data['name'].capitalize()}")
                    st.markdown(f"**Doświadczenie bazowe:** {data['base_experience']}")
                    st.markdown(f"**Wzrost:** {data['height'] / 10} m")
                    st.markdown(f"**Waga:** {data['weight'] / 10} kg")
                else:
                    st.session_state.processing = False
                    st.session_state.done = False
                    st.warning("Nie znaleziono informacji w PokéAPI.")

            except Exception as e:
                st.session_state.processing = False
                st.session_state.done = False
                st.error(f"Wystąpił błąd: {e}")
        else:
            st.warning("⚠️ Najpierw wgraj zdjęcie Pokémona.")

# Przycisk WYCZYŚĆ – tylko po udanej predykcji
if st.session_state.predicted and st.session_state.done:
    st.divider()
    if st.button("🗑️ Wyczyść wszystko", type="primary", use_container_width=True):
        for key in ["uploaded_file", "predicted", "processing", "done"]:
            st.session_state[key] = False
        st.query_params.clear()

# Stopka
st.divider()
st.caption("Projekt demonstracyjny – wspierany przez Vision Transformer (ViT) i PokéAPI.")
