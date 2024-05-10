from weather.csv.csv_extracted import WeatherSourceCSV
from weather.csv.enum import GroupByDateEnum, OperationToGroupEnum
from pandas import to_datetime
import os


if __name__ == "__main__":
    print(os.getcwd())
    weather = WeatherSourceCSV(
        file_path="data/obregon/weather_151617_obregon.csv", 
       column_date="Date"
    )
    weather.transform_date(
        start='2015-12-13',
        end='2016-02-16',
        group_by=GroupByDateEnum.SEVEN_DAY,
        operation_group= OperationToGroupEnum.AVG,
        is_debug= True,
    )
    weather.save_transform(file_path="data/sevent_day_obregon_2015.csv")