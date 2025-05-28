# src/pokemon_kedro_project/pipelines/data_science/nodes.py

import pandas as pd
from autogluon.multimodal import MultiModalPredictor
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple
import tempfile  # <--- DODAJEMY IMPORT
import os  # <--- DODAJEMY IMPORT


def train_model(train_data: pd.DataFrame, parameters: Dict[str, Any]) -> MultiModalPredictor:
    """Trenuje model klasyfikacji obrazów przy użyciu AutoGluon."""
    autogluon_params = parameters["autogluon"]
    target_column = parameters["target_column"]

    predictor = MultiModalPredictor(
        label=target_column,
        eval_metric=autogluon_params["eval_metric"]
    )

    # === POCZĄTEK ZMIANY ===
    # Tworzymy tymczasowy folder, aby zapisać dane w formacie,
    # który AutoGluon na pewno poprawnie odczyta (jako plik CSV na dysku).
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_train_csv_path = os.path.join(temp_dir, 'train.csv')

        # Zapisujemy DataFrame otrzymany od Kedro do tymczasowego pliku CSV
        train_data.to_csv(temp_train_csv_path, index=False)

        print(f"Temporarily saving training data to: {temp_train_csv_path}")
        print("Starting AutoGluon training from file path...")

        # Przekazujemy do .fit() ŚCIEŻKĘ do pliku, a nie obiekt DataFrame
        predictor.fit(
            train_data=temp_train_csv_path,  # <--- KLUCZOWA ZMIANA
            time_limit=autogluon_params["time_limit"],
            presets=autogluon_params["presets"],
        )

    # Folder tymczasowy i jego zawartość są automatycznie usuwane po wyjściu z bloku 'with'
    # === KONIEC ZMIANY ===

    print("Training finished.")

    return predictor


def evaluate_model(
        predictor: MultiModalPredictor, test_data: pd.DataFrame
) -> Tuple[Dict, plt.Figure]:
    """Ocenia wytrenowany model i generuje raport oraz macierz pomyłek."""
    print("Evaluating model...")

    # Przekazujemy DataFrame do ewaluacji - tutaj to działa poprawnie
    y_true = test_data['label']
    y_pred = predictor.predict(data=test_data)

    # Generowanie raportu klasyfikacji jako słownik
    report_dict = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    print("Classification Report generated.")

    # Generowanie macierzy pomyłek jako wykres matplotlib
    actual_target_names = sorted(y_true.unique())
    cm = confusion_matrix(y_true, y_pred, labels=actual_target_names)

    fig, ax = plt.subplots(figsize=(18, 15))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=actual_target_names, yticklabels=actual_target_names, ax=ax)
    ax.set_xlabel('Predicted Class')
    ax.set_ylabel('True Class')
    ax.set_title('Confusion Matrix')
    print("Confusion Matrix plot generated.")

    return report_dict, fig