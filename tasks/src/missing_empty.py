"""Function to fill NAN or empty values"""

from src.helpers.file_access import get_file_to_data_frame, FolderList, save_to_csv


def missing_by_mean_for_features(file_in: str, folder_file=FolderList.UPLOAD) -> None:
    """Fill all data in every feature (column) by mean of this column

    Args:
        file_in (str): file to fill
    """
    df = get_file_to_data_frame(file_name=file_in, folder=folder_file)
    df.fillna(df.mean(), inplace=True)
    file_save = f"fill_avg_{file_in}"
    save_to_csv(data_frame=df,file_save=file_save)
