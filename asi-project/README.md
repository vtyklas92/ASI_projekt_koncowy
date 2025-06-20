# ASI_project

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Spis treści
- [Wymagania wstępne](#wymagania-wstępne)
- [Instalacja zależności](#instalacja-zależności)
- [Konfiguracja DVC z Google Drive](#konfiguracja-dvc-z-google-drive)
- [Pipeline Data Engineering](#pipeline-data-engineering)
- [Pipeline Data Science](#pipeline-data-science)
- [Uruchamianie pipeline'u](#uruchamianie-pipelineu)
- [Przydatne polecenia](#przydatne-polecenia)

---

## Wymagania wstępne

- Python 3.11+
- pip
- git
- dvc (z obsługą GDrive)
- (opcjonalnie) Docker

---

## Instalacja zależności

1. **Sklonuj repozytorium:**
   ```bash
   git clone <adres_repo>
   cd asi-project
   ```

2. **Zainstaluj zależności:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Zainstaluj DVC z obsługą GDrive:**
   ```bash
   pip install "dvc[gdrive]"
   ```

---

## Konfiguracja DVC z Google Drive

Aby pobrać dane (np. modele) z DVC przechowywane na Google Drive, użyj przygotowanego skryptu konfiguracyjnego.

### Krok po kroku:

1. **Otrzymaj plik klucza JSON**
   - Plik z kluczem serwisowym (`dvc-gdrive-key.json`) zostanie dostarczony przez autorów projektu do sprawdzenia działania.

2. **Uruchom skrypt konfiguracyjny**
   - W katalogu głównym projektu uruchom:
     ```bash
     python .dvc/setup_dvc.py /pełna/ścieżka/do/dvc-gdrive-key.json
     ```
   - Przykład:
     ```bash
     python .dvc/setup_dvc.py /home/user/dvc-gdrive-key.json
     ```
   - Skrypt automatycznie skonfiguruje DVC do korzystania z Google Drive przez ten klucz.

3. **Pobierz dane z DVC**
   - Teraz możesz pobrać wymagane dane (np. modele) poleceniem:
     ```bash
     dvc pull AutogluonModels.dvc
     ```
   - Lub wszystkie dane DVC:
     ```bash
     dvc pull
     ```

**Uwaga:**
Bez poprawnie skonfigurowanego DVC i klucza pobieranie danych nie będzie możliwe.

---

## Pipeline Data Engineering

Kod znajduje się w:
`src/asi_project/pipelines/data_engineering/`

### Główne funkcje:
- **create_pokemon_dataframe**  
  Skanuje katalog z surowymi danymi (obrazy) i tworzy DataFrame z kolumnami `image` (ścieżka do pliku) i `label` (klasa). Oczekuje parametru `raw_data_path` w pliku konfiguracyjnym.

- **split_data**  
  Dzieli dane na zbiory treningowe i testowe z zachowaniem proporcji klas (stratyfikacja). Parametry podziału (np. `test_size`, `target_column`, `random_state`) są przekazywane przez config.

---

## Pipeline Data Science

Kod znajduje się w:
`src/asi_project/pipelines/data_science/`

### Główne funkcje:
- **train_model**  
  Trenuje model klasyfikacji obrazów przy użyciu `autogluon.multimodal.MultiModalPredictor`. Dane treningowe są zapisywane tymczasowo do pliku CSV, a następnie model jest trenowany na tym pliku. Parametry treningu (np. `time_limit`, `presets`, `eval_metric`, `target_column`) są przekazywane przez config.

- **evaluate_model**  
  Ocenia wytrenowany model na zbiorze testowym. Generuje raport klasyfikacji (`classification_report`) oraz wizualizację macierzy pomyłek (`confusion_matrix`).

---

## Uruchamianie pipeline'u

1. **Uruchomienie domyślnego pipeline'u Kedro:**
   ```bash
   kedro run
   ```
   To polecenie uruchamia domyślny pipeline, który obejmuje zarówno etap data engineering, jak i data science (jeśli są połączone w domyślnej konfiguracji).

2. **Uruchomienie wybranego pipeline'u:**
   Możesz uruchomić tylko wybraną część, np.:
   - Tylko data engineering:
     ```bash
     kedro run --pipeline=de
     ```
   - Tylko data science:
     ```bash
     kedro run --pipeline=ds
     ```

3. **Parametry pipeline'u** znajdują się w plikach `conf/base/parameters_data_engineering.yml`, `parameters_data_science.yml` oraz `parameters.yml`.

---

## Przydatne polecenia

- **Instalacja zależności:**  
  `pip install -r requirements.txt`

- **Instalacja DVC z obsługą GDrive:**  
  `pip install "dvc[gdrive]"`

- **Konfiguracja DVC z kluczem:**  
  `python .dvc/setup_dvc.py /pełna/ścieżka/do/dvc-gdrive-key.json`

- **Pobranie modeli z DVC:**  
  `dvc pull AutogluonModels.dvc`

- **Uruchomienie pipeline'u:**  
  `kedro run`

- **Testy:**  
  `pytest`

- **Podgląd struktury katalogów:**  
  `tree -L 2`

---

## Uwagi końcowe

- Nie commituj danych ani modeli do repozytorium – korzystaj z DVC.
- Parametry pipeline'ów i ścieżki do danych ustawiaj w plikach konfiguracyjnych w `conf/`.
- Przed uruchomieniem pipeline'u upewnij się, że masz pobrane wymagane dane i modele przez DVC.
- Do pobrania danych z DVC wymagany jest klucz serwisowy Google, który zostanie dostarczony recenzentowi.
- Skrypt `.dvc/setup_dvc.py` automatycznie skonfiguruje DVC do pracy z GDrive.

---

**W razie pytań lub problemów – sprawdź dokumentację Kedro, DVC lub skontaktuj się z zespołem!**
