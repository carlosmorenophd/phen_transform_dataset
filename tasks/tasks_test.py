"""To run test from files"""
import sys

from celery.app import Celery
from src.helpers.key_env import REDIS_BROKEN

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f"Run with props action - {sys.argv[1]}")
        app = Celery('phen_transform', broker_url=REDIS_BROKEN)
        action = sys.argv[1]
        if action == "keep_percentage_of_no_empty":
            print("Run - keep_percentage_of_no_empty")
            print(f"file -> {sys.argv[2]}, percentage -> {sys.argv[3]}")
            app.send_task(
                name="feature_selection-keep_percentage_of_no_empty",
                args=(
                    sys.argv[2],
                    sys.argv[3],
                )
            )
        elif action == "keep_patter_like":
            print("Run - keep_patter_like")
            print(f"file - {sys.argv[2]}, percentage - {sys.argv[3]}")
            app.send_task(
                name="feature_selection-keep_patter_like",
                args=(
                    sys.argv[2],
                    sys.argv[3],
                )
            )
        elif action == "keep_patter_list_like":
            print("Run - keep_patter_list_like")
            print(f"file -> {sys.argv[2]}, percentage -> {sys.argv[3]}")
            app.send_task(
                name="feature_selection-keep_patter_list_like",
                args=(
                    sys.argv[2],
                    sys.argv[3],
                )
            )
        elif action == "patter_like_with_static":
            print("Run - patter_like_with_static")
            print(
                f"file -> {sys.argv[2]}, patter -> {sys.argv[3]}, columns -> {sys.argv[4]}")
            app.send_task(
                name="feature_selection-patter_like_with_static",
                args=(
                    sys.argv[2],
                    sys.argv[3],
                    sys.argv[4],
                )
            )
        elif action == "feature_selection-correlation":
            print("Run - feature_selection-correlation")
            print(
                f"file -> {
                    sys.argv[2]
                }, threshold -> {
                    sys.argv[3]
                }, create_heatmap -> {
                    sys.argv[4]
                }"
            )
            app.send_task(
                name="feature_selection-correlation",
                args=(
                    sys.argv[2],
                    sys.argv[3],
                    sys.argv[4],
                )
            )
        elif action == "missing_fill-average":
            print("Run - missing_fill-average")
            print(
                f"file -> {
                    sys.argv[2]
                }"
            )
            app.send_task(
                name="missing_fill-average",
                args=(
                    sys.argv[2],
                )
            )
        elif action == "normalize_dataset":
            print("Run - normalize_dataset")
            print(
                f"file -> {
                    sys.argv[2]
                } action -> {
                    sys.argv[3]
                } avoid columns - {
                    sys.argv[4]
                }"
            )
            app.send_task(
                routing_key="high_priority",
                name="normalize_dataset",
                args=(
                    sys.argv[2],
                    sys.argv[3],
                    sys.argv[4],
                ),
            )
        elif action == "search_data_power_hourly":
            print("Run - search_data_power_hourly")
            print(
                f"file -> {
                    sys.argv[2]
                } action -> {
                    sys.argv[3]
                } columns - {
                    sys.argv[4]
                } features -> {
                    sys.argv[5]
                }"
            )
            app.send_task(
                name="search_data_power_hourly",
                args=(
                    sys.argv[2],
                    sys.argv[3],
                    sys.argv[4],
                    sys.argv[5],
                ),
            )
        else:
            print("Not action valid")

    else:
        print("Only test")
    print("end")
