import pandas as pd
from datetime import date
from weather.csv.enum import GroupByDateEnum


class WeatherSourceCSV():
    def __init__(self, file_path: str, column_date: str) -> None:
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        self.column_key = column_date
        self.df[column_date] = pd.to_datetime(self.df[column_date])

    def get_all_by_date(self, start: date, end: date, group_by: GroupByDateEnum) -> pd.DataFrame:
        df_date = self.df[self.df[self.column_key].dt >=
                          start & self.df[self.column_key].dt <= end]
        print(df_date)
