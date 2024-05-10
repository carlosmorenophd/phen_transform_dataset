from weather.csv.csv_extracted import WeatherSourceCSV
from weather.csv.enum import GroupByDateEnum, OperationToGroupEnum
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
        group_by=GroupByDateEnum.THIRTY_DAY,
        operation_group= OperationToGroupEnum.AVG,
        is_debug= True,
        is_clean_data= True,
    )


    weather.save_transform(file_path="data/thirty_day_obregon_2015.csv")

    weather.transform_date(
        start='2016-12-13',
        end='2017-02-16',
        group_by=GroupByDateEnum.THIRTY_DAY,
        operation_group= OperationToGroupEnum.AVG,
        is_debug= True,
        is_clean_data= True,
    )

    weather.save_transform(file_path="data/thirty_day_obregon_2016.csv")

    weather.transform_date(
        start='2015-12-13',
        end='2016-02-16',
        group_by=GroupByDateEnum.FIFTEEN_DAY,
        operation_group= OperationToGroupEnum.AVG,
        is_debug= True,
        is_clean_data= True,
    )


    weather.save_transform(file_path="data/fifteen_day_obregon_2015.csv")

    weather.transform_date(
        start='2016-12-13',
        end='2017-02-16',
        group_by=GroupByDateEnum.FIFTEEN_DAY,
        operation_group= OperationToGroupEnum.AVG,
        is_debug= True,
        is_clean_data= True,
    )

    weather.save_transform(file_path="data/fifteen_day_obregon_2016.csv")


    weather.transform_date(
        start='2015-12-13',
        end='2016-02-16',
        group_by=GroupByDateEnum.SEVEN_DAY,
        operation_group= OperationToGroupEnum.AVG,
        is_debug= True,
        is_clean_data= True,
    )


    weather.save_transform(file_path="data/seven_day_obregon_2015.csv")

    weather.transform_date(
        start='2016-12-13',
        end='2017-02-16',
        group_by=GroupByDateEnum.SEVEN_DAY,
        operation_group= OperationToGroupEnum.AVG,
        is_debug= True,
        is_clean_data= True,
    )

    weather.save_transform(file_path="data/seven_day_obregon_2016.csv")
