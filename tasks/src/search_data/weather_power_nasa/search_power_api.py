"""Search data from power server"""
import time

import pandas as pd
import requests_cache

from src.search_data.weather_power_nasa.enum_weather import (
    ColumnsDefinition,
    CommunityPowerApiEnum,
    FeaturesPowerApiEnum,
    FormatPowerApiEnum,
    TransformWeatherActionEnum,
    UrlPowerAPI,
)
from src.helpers.file_access import StorageFile
from src.helpers.key_env import FileInformation, FolderList


class WeatherExportDataFrame():
    """Search on nasa power and get data
    """

    def __init__(
        self,
        file_information: FileInformation,
        columns_definition: ColumnsDefinition,
        features: list[FeaturesPowerApiEnum],
        action: TransformWeatherActionEnum,
    ) -> None:
        url_api = UrlPowerAPI()
        self.storage = StorageFile(file_information=file_information)
        self.url = url_api.hourly_url
        self.columns_definition = columns_definition
        self.features = features
        self.action = action
        self.df = self.storage.get_csv_to_data_frame()

    def fetching_wheat_daily(self):
        """Get data from API
        """
        start_date_column = self.columns_definition["start_date_column"]
        end_date_column = self.columns_definition["end_date_column"]
        latitude_column = self.columns_definition["latitude_column"]
        longitude_column = self.columns_definition["longitude_column"]
        self.df["date_start"] = pd.to_datetime(
            self.df[start_date_column]
        ).dt.strftime('%Y%m%d')
        self.df["date_end"] = pd.to_datetime(
            self.df[end_date_column]
        ).dt.strftime('%Y%m%d')
        sqlite_file = self.storage.get_file_on_files_repository(
            folder=FolderList.TEMP,
            file_name='wheat_cache_sqlite'
        )
        session = requests_cache.CachedSession(sqlite_file)
        for parameter_weather in self.features:
            feature = parameter_weather.value
            self.df[feature] = - 100.0
            for index, row in self.df.iterrows():
                params = {
                    "start": row["date_start"],
                    "end": row["date_end"],
                    "latitude": row[latitude_column],
                    "longitude": row[longitude_column],
                    "community": CommunityPowerApiEnum.RE.value,
                    "parameters": feature,
                    "format": FormatPowerApiEnum.JSON.value,
                    "user": "cloud",
                    "header": True,
                    "time-standard": 'lst',
                }
                response = session.get(
                    url=self.url,
                    params=params,
                    headers={'accept': 'application/json'},
                )
                if response.status_code == 200:
                    result = response.json()[
                        "properties"]["parameter"][feature]
                    columns_date = pd.date_range(start=pd.to_datetime(
                        row["date_start"]), end=pd.to_datetime(row["date_end"]))
                    df_weather = pd.DataFrame(
                        index=range(24), columns=columns_date)
                    for key in result:
                        time_index = int(key[-2:])
                        day_column = pd.to_datetime(key[:8])
                        df_weather.loc[time_index, day_column] = result[key]
                    self.get_features(
                        index=index,
                        df_weather=df_weather,
                        feature=feature,
                    )
                    print(
                        f"Success feature -> {feature} of {
                            index} - {self.df.shape[0]}"
                    )
                else:
                    print("Error on {self.url}, feature {param} -> {response}")
                if not response.from_cache:
                    print("Sleep to prevent error on Server... =(^-^)=")
                    time.sleep(5)
            self.save()

    def get_features(self, index: int, df_weather: pd.DataFrame, feature: str) -> None:
        if self.action == TransformWeatherActionEnum.ALL or self.action == TransformWeatherActionEnum.MEAN:
            for column in df_weather.columns:
                self.add_new_feature_cell_df(
                    feature=feature,
                    index=index,
                    column=column,
                    metric=TransformWeatherActionEnum.MEAN.value,
                    value=df_weather[column].mean()
                )
        if self.action == TransformWeatherActionEnum.ALL or self.action == TransformWeatherActionEnum.MINUS:
            for column in df_weather.columns:
                self.add_new_feature_cell_df(
                    feature=feature,
                    index=index,
                    column=column,
                    metric=TransformWeatherActionEnum.MINUS.value,
                    value=df_weather[column].min()
                )
        if self.action == TransformWeatherActionEnum.ALL or self.action == TransformWeatherActionEnum.MAX:
            for column in df_weather.columns:
                self.add_new_feature_cell_df(
                    feature=feature,
                    index=index,
                    column=column,
                    metric=TransformWeatherActionEnum.MAX.value,
                    value=df_weather[column].max()
                )
        if self.action == TransformWeatherActionEnum.ALL or self.action == TransformWeatherActionEnum.RANGE:
            for column in df_weather.columns:
                self.add_new_feature_cell_df(
                    feature=feature,
                    index=index,
                    column=column,
                    metric=TransformWeatherActionEnum.RANGE.value,
                    value=df_weather[column].max() - df_weather[column].min()
                )

    def add_new_feature_cell_df(self, index: int, feature: str, column: str, metric: str, value: float):
        self.df.at[
            index,
            f"{feature}_{metric}_{column}",
        ] = value

    def save(self):
        """Save file

        Args:
            save_file (_type_): _description_
        """
        self.storage.save_data_frame_to_csv(
            data_frame=self.df,
            prefix="weather",
        )
