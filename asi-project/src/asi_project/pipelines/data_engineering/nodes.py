import os
from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split


def create_pokemon_dataframe(parameters: dict[str, Any]) -> pd.DataFrame:
    """Skanuje katalog z surowymi danymi i tworzy DataFrame.

    Funkcja przeszukuje podfoldery w podanej ścieżce, traktując każdą nazwę
    podfolderu jako etykietę klasy. Gromadzi bezwzględne ścieżki do wszystkich
    plików graficznych (.png, .jpg, .jpeg) i tworzy z nich ramkę danych
    zawierającą dwie kolumny: 'image' i 'label'.

    Args:
        parameters: Słownik zawierający parametry. Oczekiwany jest klucz:
            'raw_data_path' (str): Ścieżka do głównego folderu z danymi,
                                   który zawiera podfoldery z klasami.

    Returns:
        pd.DataFrame: Ramka danych z dwiema kolumnami:
            - 'image': Bezwzględna ścieżka do pliku obrazu.
            - 'label': Nazwa klasy (nazwa podfolderu).

    Raises:
        FileNotFoundError: Jeśli katalog podany w `parameters['raw_data_path']`
                           nie istnieje.
    """
    raw_data_path = parameters["raw_data_path"]
    if not os.path.isdir(raw_data_path):
        raise FileNotFoundError(
            f"Katalog z danymi nie został znaleziony: {raw_data_path}"
        )

    image_paths = []
    labels = []
    class_names = sorted(
        [
            d
            for d in os.listdir(raw_data_path)
            if os.path.isdir(os.path.join(raw_data_path, d))
        ]
    )

    for class_name in class_names:
        class_dir = os.path.join(raw_data_path, class_name)
        for image_name in os.listdir(class_dir):
            if image_name.lower().endswith((".png", ".jpg", ".jpeg")):
                # Kluczowe: Używamy ścieżek bezwzględnych, aby uniknąć problemów
                image_paths.append(os.path.abspath(os.path.join(class_dir, image_name)))
                labels.append(class_name)

    df = pd.DataFrame({"image": image_paths, "label": labels})
    print(f"Stworzono DataFrame z {len(df)} obrazami.")
    return df


def split_data(
    df: pd.DataFrame, parameters: dict[str, Any]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Dzieli dane na zbiory treningowe i testowe.

    Funkcja wykorzystuje stratyfikowany podział, aby zapewnić, że proporcje
    klas w zbiorze treningowym i testowym będą takie same jak w zbiorze
    początkowym.

    Args:
        df: Ramka danych pandas do podziału. Powinna zawierać kolumny
            z danymi i etykietami.
        parameters: Słownik zawierający parametry podziału. Oczekiwane klucze
                    znajdują się w zagnieżdżonym słowniku pod kluczem 'split':
            'test_size' (float): Procent danych, który ma trafić do zbioru testowego.
            'target_column' (str): Nazwa kolumny, która ma być użyta do stratyfikacji.
            'random_state' (int):
            Ziarno losowości dla zapewnienia powtarzalności podziału.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Krotka zawierająca dwie ramki danych:
            - Pierwszy element: zbiór treningowy.
            - Drugi element: zbiór testowy.
    """
    train_df, test_df = train_test_split(
        df,
        test_size=parameters["split"]["test_size"],
        stratify=df[parameters["split"]["target_column"]],
        random_state=parameters["split"]["random_state"],
    )
    print(
        f"Podział danych zakończony. Zbiór treningowy: {len(train_df)},"
        f"Zbiór testowy: {len(test_df)}"
    )
    return train_df, test_df
