from weather.csv.csv_extracted import WeatherSourceCSV
from weather.csv.enum import GroupByDateEnum
from datetime import date
import os

if __name__ == "__main__":
    print(os.getcwd())
    weather = WeatherSourceCSV(
        file_path="data/obregon/obregon_weather.csv", column_date="Date")
    pd = weather.get_all_by_date(start=date(year=2015, month=12, day=1), end=date(
        year=2015, month=12, day=2), group_by=GroupByDateEnum.DAY_AVG)
    print("Start")
