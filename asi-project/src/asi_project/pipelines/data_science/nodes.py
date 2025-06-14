import os
import tempfile
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from autogluon.multimodal import MultiModalPredictor
from sklearn.metrics import classification_report, confusion_matrix


def train_model(
    train_data: pd.DataFrame, parameters: dict[str, Any]
) -> "MultiModalPredictor":
    """Trenuje model klasyfikacji obrazów przy użyciu AutoGluon.

    Funkcja ta inicjalizuje i trenuje `MultiModalPredictor` z biblioteki
    AutoGluon. Aby zapewnić niezawodność i ominąć potencjalne problemy z
    przekazywaniem DataFrame w pamięci, dane treningowe są najpierw zapisywane
    do tymczasowego pliku CSV, a następnie ścieżka do tego pliku jest
    przekazywana do metody `.fit()`.

    Args:
        train_data: Ramka danych pandas zawierająca dane treningowe.
                    Oczekiwane kolumny to 'image' ze ścieżkami do obrazów
                    i 'label' z etykietami klas.
        parameters: Słownik zawierający parametry. Oczekiwane są klucze:
            - 'autogluon' (Dict): Parametry dla AutoGluon, np. 'time_limit',
              'presets', 'eval_metric'.
            - 'split' (Dict): Parametry podziału, w tym 'target_column'.

    Returns:
        MultiModalPredictor: Wytrenowany i gotowy do użycia obiekt predyktora
                             AutoGluon.
    """
    autogluon_params = parameters["autogluon"]
    target_column = parameters["split"]["target_column"]

    predictor = MultiModalPredictor(
        label=target_column, eval_metric=autogluon_params["eval_metric"]
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_train_csv_path = os.path.join(temp_dir, "train.csv")
        train_data.to_csv(temp_train_csv_path, index=False)

        print(f"Dane treningowe zapisane tymczasowo w: {temp_train_csv_path}")
        print("Rozpoczynam trening AutoGluon...")

        predictor.fit(
            train_data=temp_train_csv_path,
            time_limit=autogluon_params["time_limit"],
            presets=autogluon_params["presets"],
        )

    print("Trening zakończony.")
    return predictor


def evaluate_model(
    predictor: "MultiModalPredictor", test_data: pd.DataFrame
) -> tuple[dict, plt.Figure]:
    """Ocenia wytrenowany model i generuje artefakty ewaluacyjne.

    Funkcja generuje predykcje na zbiorze testowym, a następnie tworzy
    dwa kluczowe artefakty: szczegółowy raport klasyfikacji w formie
    słownika oraz wizualizację macierzy pomyłek jako obiekt figury
    matplotlib.

    Args:
        predictor: Wytrenowany obiekt `MultiModalPredictor` zwrócony przez
                   węzeł `train_model`.
        test_data: Ramka danych pandas zawierająca dane testowe. Oczekiwane
                   kolumny to 'image' i 'label'.

    Returns:
        Krotka zawierająca dwa elementy:
            - Pierwszy element (Dict): Słownik reprezentujący raport
              klasyfikacji z metrykami (precision, recall, f1-score)
              dla każdej z klas.
            - Drugi element (plt.Figure): Obiekt figury Matplotlib
              zawierający wykres macierzy pomyłek.
    """
    y_true = test_data["label"]
    y_pred = predictor.predict(data=test_data)

    report_dict = classification_report(
        y_true, y_pred, output_dict=True, zero_division=0
    )

    actual_target_names = sorted(y_true.unique())
    cm = confusion_matrix(y_true, y_pred, labels=actual_target_names)

    fig, ax = plt.subplots(figsize=(20, 18))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=actual_target_names,
        yticklabels=actual_target_names,
        ax=ax,
    )
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    ax.set_xlabel("Predicted Class", fontsize=12)
    ax.set_ylabel("True Class", fontsize=12)
    ax.set_title("Confusion Matrix", fontsize=14)
    fig.tight_layout()

    return report_dict, fig
