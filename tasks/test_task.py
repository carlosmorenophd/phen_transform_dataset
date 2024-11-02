"""To run test from files"""


import sys

from celery.app import Celery
from src.support.utils import REDIS_BROKEN


def keep_percentage_of_no_empty(file_csv, percentage) -> None:
    """Send task to remove empty values on cells"""
    app = Celery('phen_transform', broker_url=REDIS_BROKEN)
    app.send_task(name="feature_selection-keep_percentage_of_no_empty",
                  args=(file_csv, percentage))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f"Run with props action - {sys.argv[1]}")
        action = sys.argv[1]
        param1 = sys.argv[2]
        param2 = sys.argv[3]
        if action == "keep_percentage_of_no_empty":
            print("Run - keep_percentage_of_no_empty")
            print(f"file - {sys.argv[2]}, percentage - {sys.argv[3]}")
            keep_percentage_of_no_empty(file_csv=param1, percentage=param2)

        else:
            print("Not action valid")

    else:
        print("Run no case")

    print("end")
