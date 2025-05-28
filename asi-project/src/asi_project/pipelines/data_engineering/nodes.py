import os
import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Dict, Any, Tuple


def create_pokemon_dataframe(parameters: Dict[str, Any]) -> pd.DataFrame:
    """Tworzy DataFrame z ścieżkami do obrazów i ich etykietami."""
    raw_data_path = parameters["raw_data_path"]
    if not os.path.isdir(raw_data_path):
        raise FileNotFoundError(f"Directory not found: {raw_data_path}")

    image_paths = []
    labels = []
    class_names = sorted([d for d in os.listdir(raw_data_path) if os.path.isdir(os.path.join(raw_data_path, d))])

    print(f"Found {len(class_names)} classes.")
    for class_name in class_names:
        class_dir = os.path.join(raw_data_path, class_name)
        for image_name in os.listdir(class_dir):
            if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Używamy ścieżek bezwzględnych, aby uniknąć problemów
                image_paths.append(os.path.abspath(os.path.join(class_dir, image_name)))
                labels.append(class_name)

    df = pd.DataFrame({'image': image_paths, 'label': labels})
    print(f"Created DataFrame with {len(df)} samples.")
    return df


def split_data(
        df: pd.DataFrame, parameters: Dict[str, Any]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Dzieli dane na zbiory treningowe i testowe."""
    target_column = parameters["target_column"]
    test_size = parameters["test_size"]
    random_state = parameters["random_state"]

    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        stratify=df[target_column],
        random_state=random_state
    )
    print(f"Data split complete. Train size: {len(train_df)}, Test size: {len(test_df)}")
    return train_df, test_df