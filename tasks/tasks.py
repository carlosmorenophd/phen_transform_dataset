"""Run all task"""
import gc

from celery import Celery
from src.support.utils import REDIS_BROKEN
from src.transforms.feature_selection import (
    select_column_by_text_like,
    select_column_by_patter_like,
    select_column_by_list_patter_and,
    select_column_by_patter_like_with_static,
)

print(REDIS_BROKEN)

app = Celery('phen_transform', broker=REDIS_BROKEN)


@app.task(name="feature_selection-keep_percentage_of_no_empty")
def keep_percentage_of_no_empty(file_csv: str, percentage_of_no_empty: float) -> None:
    """Read csv and only pass the column that have more or equal to percentage the cell with values

    Args:
        file_csv (str): name of file 
        percentage_of_no_empty (float): percentage valid

    Returns:
        _type_: None
    """
    print(
        f"Parameters: file - {file_csv} percentage - {percentage_of_no_empty}")
    select_column_by_text_like(
        file_in=file_csv, percentage=float(percentage_of_no_empty))
    gc.collect()
    return "success"


@app.task(name="feature_selection-keep_patter_like")
def keep_patter_like(file_csv: str, patter_like: str) -> None:
    """Read csv and only pass the column that have like column name

    Args:
        file_csv (str): name of file 
        patter_like (str): patter to like it

    Returns:
        _type_: None
    """
    print(f"Parameters: file - {file_csv} percentage - {patter_like}")
    select_column_by_patter_like(file_in=file_csv, patter_like=patter_like)
    gc.collect()
    return "success"


@app.task(name="feature_selection-keep_patter_list_like")
def keep_patter_list_like(file_csv: str, patters_like: str) -> None:
    """Read csv and only pass the column that have like column in a list split by @

    Args:
        file_csv (str): name of file 
        patter_like (str): patter to like to convert it a list with @ like common

    Returns:
        _type_: None
    """
    print(f"Parameters: file - {file_csv} percentage - {patters_like}")
    select_column_by_list_patter_and(
        file_in=file_csv, patters_like=patters_like.split("$"))
    gc.collect()
    return "success"


@app.task(name="feature_selection-patter_like_with_static")
def patter_like_with_static(file_csv: str, patter_like: str, static_columns: str) -> None:
    """Read csv and only pass the column that have like column name

    Args:
        file_csv (str): name of file 
        patter_like (str): patter to like it
        static_columns (str): name of column in str split by , 'coma' 

    Returns:
        _type_: None
    """

    print(f"Parameters: file - {file_csv} percentage - {patter_like}")
    select_column_by_patter_like_with_static(
        file_in=file_csv,
        patter_like=patter_like,
        static_columns=static_columns.split(",")
    )
    gc.collect()
    return "success"
