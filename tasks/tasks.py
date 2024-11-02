"""Run all task"""
import gc

from celery import Celery
from src.support.utils import REDIS_BROKEN
from src.transforms.feature_selection import select_column_by_percentage_values

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
    print(f"Parameters: file - {file_csv} percentage - {percentage_of_no_empty}")
    select_column_by_percentage_values(file_in=file_csv, percentage=float(percentage_of_no_empty))
    gc.collect()
    return "success"
