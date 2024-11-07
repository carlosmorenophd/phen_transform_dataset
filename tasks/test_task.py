"""To run test from files"""


import sys

from celery.app import Celery
from src.helpers.key_env import REDIS_BROKEN


def keep_percentage_of_no_empty(file_csv, percentage) -> None:
    """Send task to remove empty values on cells"""
    app = Celery('phen_transform', broker_url=REDIS_BROKEN)
    app.send_task(name="feature_selection-keep_percentage_of_no_empty",
                  args=(file_csv, percentage))


def keep_patter_like(file_csv: str, patter_like: str) -> None:
    """Send task to remove keep only column like patter"""
    app = Celery('phen_transform', broker_url=REDIS_BROKEN)
    app.send_task(name="feature_selection-keep_patter_like",
                  args=(file_csv, patter_like))


def keep_patter_list_like(file_csv: str, patters_like: str) -> None:
    """Send task to remove keep only column like patters list with and"""
    app = Celery('phen_transform', broker_url=REDIS_BROKEN)
    app.send_task(name="feature_selection-keep_patter_list_like",
                  args=(file_csv, patters_like))


def patter_like_with_static(file_csv: str, patters_like: str, static_columns: str) -> None:
    """Send task to remove keep only column like patters list with and"""
    app = Celery('phen_transform', broker_url=REDIS_BROKEN)
    app.send_task(name="feature_selection-patter_like_with_static",
                  args=(file_csv, patters_like, static_columns))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f"Run with props action - {sys.argv[1]}")
        app = Celery('phen_transform', broker_url=REDIS_BROKEN)
        action = sys.argv[1]
        param1 = sys.argv[2]
        param2 = sys.argv[3]
        param3 = sys.argv[4]
        if action == "keep_percentage_of_no_empty":
            print("Run - keep_percentage_of_no_empty")
            print(f"file - {sys.argv[2]}, percentage - {sys.argv[3]}")
            keep_percentage_of_no_empty(file_csv=param1, percentage=param2)
        elif action == "keep_patter_like":
            print("Run - keep_patter_like")
            print(f"file - {sys.argv[2]}, percentage - {sys.argv[3]}")
            keep_patter_like(file_csv=param1, patter_like=param2)
        elif action == "keep_patter_list_like":
            print("Run - keep_patter_list_like")
            print(f"file - {sys.argv[2]}, percentage - {sys.argv[3]}")
            keep_patter_list_like(file_csv=param1, patters_like=param2)
        elif action == "patter_like_with_static":
            print("Run - patter_like_with_static")
            print(
                f"file - {sys.argv[2]}, patter - {sys.argv[3]}, columns {param3}")
            patter_like_with_static(
                file_csv=param1,
                patters_like=param2,
                static_columns=param3,
            )
        elif action == "feature_selection-correlation":
            print("Run - feature_selection-correlation")
            print(
                f"file - {sys.argv[2]}, threshold - {sys.argv[3]}, create_heatmap - {param3}")
            app.send_task(name="feature_selection-correlation",
                          args=(param1, param2, param3))
        else:
            print("Not action valid")

    else:
        print("Only test")
    print("end")
