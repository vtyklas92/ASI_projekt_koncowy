import os
import pandas as pd
from sklearn.model_selection import train_test_split
from typing import List


def create_image_dataframe(pokemon_data_dir: str) -> pd.DataFrame:
    """
    Scans the raw data directory and creates a DataFrame with absolute image paths and labels.

    Args:
        pokemon_data_dir: Path to the raw data directory.

    Returns:
        A pandas DataFrame with 'image' and 'label' columns.
    """
    print(f"Scanning directory: {pokemon_data_dir}")
    if not os.path.isdir(pokemon_data_dir):
        raise FileNotFoundError(f"Directory '{pokemon_data_dir}' does not exist.")

    image_paths = []
    labels = []

    class_names = sorted([d for d in os.listdir(pokemon_data_dir)
                          if os.path.isdir(os.path.join(pokemon_data_dir, d))])

    if not class_names:
        raise ValueError(f"No class subdirectories found in {pokemon_data_dir}.")

    print(f"Found {len(class_names)} classes.")

    for class_name in class_names:
        class_dir = os.path.join(pokemon_data_dir, class_name)
        for image_name in os.listdir(class_dir):
            if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.abspath(os.path.join(class_dir, image_name)))
                labels.append(class_name)

    if not image_paths:
        raise ValueError(f"No images found in {pokemon_data_dir}.")

    df = pd.DataFrame({'image': image_paths, 'label': labels})
    print(f"Created DataFrame with {len(df)} samples.")
    return df


def split_data(master_df: pd.DataFrame, test_size: float, random_state: int) -> List[pd.DataFrame]:
    """
    Splits the master DataFrame into training and testing sets.

    Args:
        master_df: The main DataFrame with image paths and labels.
        test_size: The proportion of the dataset to allocate to the test split.
        random_state: A seed for the random number generator for reproducibility.

    Returns:
        A list containing [train_df, test_df].
    """
    train_df, test_df = train_test_split(
        master_df,
        test_size=test_size,
        stratify=master_df['label'],
        random_state=random_state
    )

    print(f"Data split complete. Train set: {len(train_df)} samples, Test set: {len(test_df)} samples.")

    # Returning a list allows Kedro to map to multiple outputs
    return [train_df, test_df]