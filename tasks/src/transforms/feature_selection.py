"""Select variables by criteria"""
import re
from src.support.utils import get_file_to_data_frame, FolderCache, save_to_csv


def select_column_by_text_like(file_in: str, percentage: float) -> None:
    """Keep only columns that are more or equal to percentage
    Args:
        file_in: File to get the data and is in upload file folder
        percentage: Range to select columns (0 y 1)
    """
    if percentage > 1 or percentage < 0:
        raise ValueError("Percentage only be 0 to 1")
    df = get_file_to_data_frame(file_name=file_in, folder=FolderCache.UPLOAD)
    percentage_no_null = df.notnull().mean()
    select_columns = percentage_no_null[percentage_no_null >
                                        percentage].index.values
    print(select_columns)
    df_filter = df[select_columns]
    file_out = f"select_percentage_{file_in}"
    save_to_csv(data_frame=df_filter, file_save=file_out)


def select_column_by_patter_like(file_in: str, patter_like: str) -> None:
    """Keep only columns that have same str of patters
    Args:
        file_in: File to get the data and is in upload file folder
        patter_like: str of patterns
    """
    df = get_file_to_data_frame(file_name=file_in, folder=FolderCache.UPLOAD)
    patter = re.compile(patter_like, re.IGNORECASE)
    df_filter = df.filter(regex=patter)
    print(df_filter.columns.values)
    file_out = f"select_patter_{patter_like}_{file_in}"
    save_to_csv(data_frame=df_filter, file_save=file_out)


def select_column_by_list_patter_and(file_in: str, patters_like: list) -> None:
    """Keep only columns that have same list of patters
    Args:
        file_in: File to get the data and is in upload file folder
        patter_like: List of patterns
    """
    df = get_file_to_data_frame(file_name=file_in, folder=FolderCache.UPLOAD)
    patter = re.compile(r"*".join(patters_like), re.IGNORECASE)
    df_filter = df.filter(regex=patter)
    print(df_filter.columns.values)
    file_out = f"select_patter_{patters_like}_{file_in}"
    save_to_csv(data_frame=df_filter, file_save=file_out)
