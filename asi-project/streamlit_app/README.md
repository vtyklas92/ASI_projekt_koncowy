# Pokédex AI

Pokédex AI to aplikacja webowa napisana w Pythonie, oparta na **Streamlit** i **AutoGluon**, służąca do rozpoznawania Pokémonów na przesłanych zdjęciach oraz pobierania szczegółowych informacji z PokéAPI.

## Funkcje

- Klasyfikacja Pokémonów ze zdjęcia
- Wbudowany model AutoGluon Multimodal
- Integracja z [PokéAPI](https://pokeapi.co)
- Stylizowany interfejs użytkownika (CSS i animacje)
- Przycisk resetujący stan aplikacji

## Instalacja i uruchomienie

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/vtyklas92/ASI_projekt_koncowy.git
cd ASI_projekt_koncowy
```

### 2. Instalacja zależności

```bash
pip install -r requirements.txt
```

> Wymagane biblioteki: `streamlit`, `pandas`, `requests`, `Pillow`, `autogluon.multimodal`

### 3. Pobranie modelu AutoGluon (opcjonalnie przez DVC)

Upewnij się, że katalog `AutogluonModels/` zawiera wytrenowany model.  
Jeśli korzystasz z `DVC`, użyj polecenia:

```bash
dvc pull
```

### 4. Uruchomienie aplikacji

```bash
streamlit run app.py
```

## Model AI

Aplikacja korzysta z modelu klasyfikującego obraz typu `AutoGluon MultiModal ImagePredictor`:

- Biblioteka: `autogluon.multimodal`
- Model: AutoGluon Image Predictor
- Urządzenie: CPU (lub GPU, jeśli dostępne)
- Model ładowany dynamicznie z najnowszej wersji zapisanej w katalogu `AutogluonModels/`

## Jak korzystać

1. Uruchom aplikację poleceniem:
   ```bash
   streamlit run app.py
   ```
2. Wgraj zdjęcie Pokémona (obsługiwane formaty: PNG, JPG, JPEG)
3. Kliknij „Rozpoznaj Pokémona”
4. Otrzymasz:
   - nazwę rozpoznanego Pokémona  
   - procentową pewność predykcji  
   - dane z PokéAPI:
     - nazwa, doświadczenie bazowe, wzrost (m), waga (kg)
5. Kliknij „Wyczyść wszystko”, aby rozpocząć nową klasyfikację

## Licencja

Projekt udostępniono na licencji MIT.  
Dane i ilustracje Pokémonów pochodzą z [PokéAPI](https://pokeapi.co/).

## Kontakt

Masz pytania lub sugestie?  
Zgłoś issue lub skontaktuj się przez GitHub.