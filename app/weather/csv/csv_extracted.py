import pandas as pd
import numpy as np
from weather.csv.enum import GroupByDateEnum


class WeatherSourceCSV():
    def __init__(self, file_path: str, column_date: str) -> None:
        self.file_path = file_path
        self.df = pd.read_csv(file_path, parse_dates=[column_date])
        self.column_key = column_date
        # self.df[column_date] = pd.to_datetime(self.df[column_date])

    def get_all_by_date(
            self,
            start,
            end,
            group_by: GroupByDateEnum,
    ) -> pd.DataFrame:
        df_date = self.df[
            (self.df[self.column_key] >= start) &
            (self.df[self.column_key] <= end)
        ]
        if group_by == GroupByDateEnum.BIG_SINGLE_AVG:
            df_date = df_date.drop(self.column_key, axis=True)
            means = np.nanmean(df_date, axis=0)

        print(means)
