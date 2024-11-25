"""Search data from power server"""

import pandas as pd
import requests_cache

from src.search_data.weather_power_nasa.enum_weather import (
    ColumnsDefinition,
    CommunityPowerApiEnum,
    FeaturesPowerApiEnum,
    FormatPowerApiEnum,
    TransformWeatherActionEnum,
    UrlPowerAPIEnum,
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
        self.storage = StorageFile(file_information=file_information)
        self.url = UrlPowerAPIEnum.DAILY_URL.value
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
                response = session.get(url=self.url, params=params)
                if response.status_code == 200:
                    result = response.json()["properties"]["parameter"]
                    avg = sum(result[param].values()) / \
                        float(len(result[param]))
                    self.df.at[index, param] = avg
                else:
                    print(response.json())

    def save(self):
        """Save file

        Args:
            save_file (_type_): _description_
        """
        self.storage.save_data_frame_to_csv(
            data_frame=self.df,
            prefix="weather",
        )


# class WeatherPlot():
#     def __init__(self) -> None:
#         self.session = requests_cache.CachedSession('wheat_cache')

#     def add_years(self, start_date: date, years: int):
#         try:
#             return start_date.replace(year=start_date.year + years)
#         except ValueError:
#             return start_date.replace(year=start_date.year + years, day=28)

#     def get_data(
#         self,
#         url: ServerPowerEnum,
#         gps: CountryGPS,
#         start_date: date,
#         end_date: date,
#         parameter: ParameterEnum,
#         community: CommunityPowerEnum = CommunityPowerEnum.RE,
#         format: FormatPowerEnum = FormatPowerEnum.JSON,
#         name_column: str = "",
#     ) -> pd.DataFrame:
#         if name_column == "":
#             name_column = parameter.value
#         df = pd.DataFrame({'time': [], name_column: []})
#         year_parameter = YearParameter(start=start_date, end=end_date, url=url)
#         for _ in range(start_date.year, end_date.year):
#             year_parameter.add(increase=1)
#             start_step_date, end_step_year = year_parameter.get_dates()
#             params = {
#                 "start": start_step_date,
#                 "end": end_step_year,
#                 "latitude": gps.latitude,
#                 "longitude": gps.longitude,
#                 "community": community.value,
#                 "parameters": parameter.value,
#                 "format": format.value,
#                 "user": "cloud",
#                 "header": True,
#                 "time-standard": 'lst',
#             }
#             response = self.session.get(url=url.value, params=params)
#             if response.status_code == 200:
#                 result = response.json()["properties"]["parameter"]
#                 for key in result[parameter.value]:
#                     df.loc[len(df.index)] = [key, result[parameter.value][key]]
#         return df

#     def plot_from_point_2001(
#         self,
#         country: CountryGPS,
#         years: list[int],
#         parameters: list[ParameterEnum],
#         endpoints: list[ServerPowerEnum]
#     ):
#         for enpoint in endpoints:
#             for end_year in years:
#                 start = date(year=2001, month=1, day=1)
#                 end = date(year=end_year, month=12, day=31)
#                 folder = "result_test_{}_{}_{}".format(
#                     server_power_enum_to_text(enpoint), start.year, end.year
#                 )
#                 if not os.path.isdir(folder):
#                     os.mkdir(folder)
#                 for param in parameters:
#                     print("Start with {}".format(param.value))
#                     df = self.get_data(
#                         gps=country,
#                         start_date=start,
#                         end_date=end,
#                         parameter=param,
#                         url=enpoint,
#                     )
#                     param_text = paramter_enum_to_text(param)
#                     df.to_csv(
#                         "{}/{}_{}_{}_{}.csv".format(
#                             folder,
#                             param_text,
#                             start.year,
#                             end.year,
#                             country.name,
#                         ),
#                         index=False,
#                     )
#                     plt.ioff()
#                     fig = plt.figure(figsize=(50, 50))

#                     plt.plot(df["time"], df[param.value])
#                     # plt.show()
#                     plt.title('Grafica de {} {} {} {}'.format(
#                         param_text, country.name, start.year, end.year))

#                     plt.savefig(
#                         "{}/{}_{}_{}_{}.jpg".format(
#                             folder,
#                             param_text,
#                             start.year,
#                             end.year,
#                             country.name,
#                         ),
#                     )
#                     plt.close(fig)
#                     print("Finsh with {}".format(param.value))


# class YearParameter():
#     """Get from year
#     """

#     def __init__(self, start: date, end: date, url: ServerPowerEnum) -> None:
#         self.start = start
#         self.end = end
#         self.url = url
#         self.date_start = start
#         self.date_end = None
#         self.is_increase = False

#     def add_years(self, date_init: date, years: int):
#         try:
#             return date_init.replace(year=date_init.year + years)
#         except ValueError:
#             return date_init.replace(year=date_init.year + years, day=28)

#     def add(self, increase: int) -> None:
#         if self.date_end == None:
#             self.date_end = self.add_years(
#                 date_init=self.date_start, years=increase)
#         else:
#             self.date_end = self.add_years(
#                 date_init=self.date_end, years=increase)
#             self.date_start = self.add_years(
#                 date_init=self.date_start, years=increase)
#         if self.date_end > self.end:
#             self.date_end = self.end

#     def get_dates(self) -> tuple[str, str]:
#         if self.url == ServerPowerEnum.MONTHLY_URL:
#             return "{}".format(self.date_start), "{}".format(self.date_end)
#         else:
#             return self.date_start.strftime("%Y%m%d"), self.date_end.strftime("%Y%m%d")
