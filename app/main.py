from weather.csv.csv_extracted import WeatherSourceCSV
from weather.csv.enum import GroupByDateEnum
from pandas import to_datetime
import os


if __name__ == "__main__":
    print(os.getcwd())
    weather = WeatherSourceCSV(
        file_path="data/obregon/obregon_weather.csv", column_date="Date")
    pd = weather.get_all_by_date(
        start=to_datetime('2015-12-1', format='%Y-%m-%d'),
        end=to_datetime('2015-12-2', format='%Y-%m-%d'),
        group_by=GroupByDateEnum.BIG_SINGLE_AVG,
    )