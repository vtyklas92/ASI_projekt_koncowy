# ASI_project

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Overview

This is your new Kedro project with PySpark setup, which was generated using `kedro 0.19.12`.

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```
pip install -r requirements.txt
```

## How to run your Kedro pipeline:

You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the files `src/tests/test_run.py` and `src/tests/pipelines/data_science/test_pipeline.py` for instructions on how to write your tests. Run the tests as follows:

```
pytest
```

To configure the coverage threshold, look at the `.coveragerc` file.

## Project dependencies

To see and update the dependency requirements for your project use `requirements.txt`. Install the project requirements with `pip install -r requirements.txt`.

[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab
To use JupyterLab, you need to install it:

```
pip install jupyterlab
```

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can use tools like [`nbstripout`](https://github.com/kynan/nbstripout). For example, you can add a hook in `.git/config` with `nbstripout --install`. This will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://docs.kedro.org/en/stable/tutorial/package_a_project.html)

## Pipeline Data Engineering

Kod znajduje się w:
`src/asi_project/pipelines/data_engineering/`

Moduł odpowiedzialny za przygotowanie danych do dalszych etapów analizy i modelowania.

### Główne funkcje:
- **create_pokemon_dataframe**  
  Skanuje katalog z surowymi danymi (np. obrazami Pokémonów), gdzie każdy podfolder reprezentuje jedną klasę (np. nazwę Pokémona). Funkcja:
  - Przechodzi przez wszystkie podfoldery w katalogu surowych danych.
  - Zbiera ścieżki do plików graficznych (.png, .jpg, .jpeg) oraz odpowiadające im etykiety (nazwy podfolderów).
  - Tworzy ramkę danych (DataFrame) z dwiema kolumnami: `image` (pełna ścieżka do pliku) oraz `label` (klasa).
  - Oczekuje parametru `raw_data_path` w pliku konfiguracyjnym.
  - Zwraca DataFrame gotowy do dalszego przetwarzania.

- **split_data**  
  Dzieli dane na zbiory treningowe i testowe z zachowaniem proporcji klas (stratyfikacja). Funkcja:
  - Przyjmuje DataFrame z obrazami i etykietami.
  - Wykorzystuje parametry z plików konfiguracyjnych (`test_size`, `target_column`, `random_state`).
  - Zapewnia, że rozkład klas w obu zbiorach jest taki sam jak w oryginalnych danych.
  - Zwraca dwa DataFrame: zbiór treningowy i testowy.

---

## Pipeline Data Science

Kod znajduje się w:
`src/asi_project/pipelines/data_science/`

Moduł odpowiedzialny za trening i ocenę modelu klasyfikacyjnego na przygotowanych danych.

### Główne funkcje:
- **train_model**  
  Trenuje model klasyfikacji obrazów przy użyciu `autogluon.multimodal.MultiModalPredictor`. Funkcja:
  - Przyjmuje zbiór treningowy (DataFrame) oraz parametry treningu (np. `time_limit`, `presets`, `eval_metric`, `target_column`).
  - Dane treningowe są zapisywane tymczasowo do pliku CSV, aby zapewnić kompatybilność z AutoGluon.
  - Inicjalizuje i trenuje model klasyfikacyjny na podstawie przekazanych parametrów.
  - Zwraca wytrenowany obiekt predyktora, gotowy do predykcji i ewaluacji.

- **evaluate_model**  
  Ocenia jakość wytrenowanego modelu na zbiorze testowym. Funkcja:
  - Przyjmuje wytrenowany model oraz zbiór testowy (DataFrame).
  - Generuje predykcje dla zbioru testowego.
  - Tworzy szczegółowy raport klasyfikacji (precision, recall, f1-score dla każdej klasy).
  - Generuje i wizualizuje macierz pomyłek (confusion matrix) jako wykres.
  - Zwraca raport klasyfikacji oraz obiekt wykresu macierzy pomyłek.
  - Raporty mogą być zapisywane do plików i wykorzystywane do dalszej analizy.

---
