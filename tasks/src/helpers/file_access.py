"""Function to use in other class"""
import os

import pandas as pd

from src.helpers.key_env import IS_DEBUG, FolderCache, FOLDER_DATA


# class TransformDataset:
#     """Validate transform"""

#     def __init__(
#         self,
#         source_file_name: str,
#         destiny_file_name: str,
#         actions: list[TransformNormalize],
#         remove_rows: list[RowValid]
#     ) -> None:
#         self.source_file_name = source_file_name
#         self.destiny_file_name = destiny_file_name
#         self.actions = actions
#         self.remove_rows = remove_rows


def get_file(file_name: str, folder: FolderCache) -> str:
    """Get file from cache"""
    file = os.path.join(FOLDER_DATA, folder.value, file_name)
    return file


def get_file_to_data_frame(file_name: str, folder: FolderCache) -> pd.DataFrame:
    """Util - load csv file with pandas """
    file = os.path.join(FOLDER_DATA, folder.value, file_name)
    if IS_DEBUG:
        print(os.getcwd())
        print(FOLDER_DATA)
        print(file)
    if os.path.isfile(file):
        return pd.read_csv(file)
    raise FileNotFoundError(f"file not found - {file}")


def get_absolute_file_to_data_frame(path_to_file: str) -> pd.DataFrame:
    """file access - load csv file with pandas from absolute file name """
    if IS_DEBUG:
        print(os.getcwd())
        print(FOLDER_DATA)
        print(path_to_file)
    if os.path.isfile(path_to_file):
        return pd.read_csv(path_to_file)
    raise FileNotFoundError(f"file not found - {path_to_file}")


def save_to_csv(data_frame: pd.DataFrame, file_save: str, is_index: bool = False) -> None:
    """Util -  save any data frame on file """
    path_to_save = get_file(file_name=file_save, folder=FolderCache.UPLOAD)
    data_frame.to_csv(path_to_save, index=is_index)
