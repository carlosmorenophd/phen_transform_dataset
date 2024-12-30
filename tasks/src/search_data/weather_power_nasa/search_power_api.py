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

    def fetching_wheat(self):
        """Get data from API
        """
        start_date_column = self.columns_definition["start_date_column"]
        end_date_column = self.columns_definition["end_date_column"]
        latitude_column = self.columns_definition["latitude_column"]
        longitude_column = self.columns_definition["longitude_column"]
        self.df["date_start"] = pd.to_datetime(
            self.df[start_date_column]
        )
        self.df["date_start"] = self.df["date_start"].dt.strftime('%Y%m%d')
        self.df["date_end"] = pd.to_datetime(self.df[end_date_column])
        self.df["date_end"] = self.df["date_end"].dt.strftime('%Y%m%d')
        sqlite_file = self.storage.get_file_on_files_repository(
            folder=FolderList.TEMP,
            file_name='wheat_cache_sqlite'
        )
        session = requests_cache.CachedSession(sqlite_file)
        for feature in self.features:
            param = feature.value
            self.df[param] = - 100.0
            for index, row in self.df.iterrows():
                params = {
                    "start": row["date_start"],
                    "end": row["date_end"],
                    "latitude": row[latitude_column],
                    "longitude": row[longitude_column],
                    "community": CommunityPowerApiEnum.RE.value,
                    "parameters": param,
                    "format": FormatPowerApiEnum.JSON.value,
                    "user": "cloud",
                    "header": True,
                    "time-standard": 'lst',
                }
                print(self.url)
                response = session.get(
                    url=self.url,
                    params=params,
                    headers={'accept': 'application/json'},
                )
                if response.status_code == 200:
                    result = response.json()["properties"]["parameter"]
                    avg = sum(result[param].values()) / \
                        float(len(result[param]))
                    self.df.at[index, param] = avg
                else:
                    print(response.json())
                time.sleep(5)

    def save(self):
        """Save file

        Args:
            save_file (_type_): _description_
        """
        self.storage.save_data_frame_to_csv(
            data_frame=self.df,
            prefix="weather",
        )
