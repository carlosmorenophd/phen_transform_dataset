import pandas as pd
import requests_cache
from weather.power_nasa.enum import (
    ParameterEnum, FormatEnum, CommunityEnum,
    OperationEnum, CountryGPS, ServerPowerEnum, paramter_enum_to_text, server_power_enum_to_text
)
from datetime import date
import matplotlib.pyplot as plt
import os


class WheatherCSV():
    def __init__(
        self,
        name_file: str,
        latitude_column: str,
        longitude_column: str,
        start_date_column: str,
        end_date_column: str,
        parameters: list[ParameterEnum],
        format: FormatEnum = FormatEnum.JSON,
        community: CommunityEnum = CommunityEnum.RE,
        operation: OperationEnum = OperationEnum.AVG_ALL,
    ) -> None:
        self.name_file = name_file
        self.latitude_column = latitude_column
        self.longitude_column = longitude_column
        self.start_date_column = start_date_column
        self.end_date_column = end_date_column
        self.parameters = parameters
        self.format = format
        self.community = community
        self.operation = operation
        self.url = 'https://power.larc.nasa.gov/api/temporal/hourly/point'
        self.csv = pd.read_csv(name_file)

    def fetching_wheat(self):
        self.csv["date_start"] = pd.to_datetime(
            self.csv[self.start_date_column])
        self.csv["date_start"] = self.csv["date_start"].dt.strftime('%Y%m%d')
        self.csv["date_end"] = pd.to_datetime(self.csv[self.end_date_column])
        self.csv["date_end"] = self.csv["date_end"].dt.strftime('%Y%m%d')
        session = requests_cache.CachedSession('wheat_cache')
        for paramEnum in self.parameters:
            param = paramEnum.value
            self.csv[param] = 0.0
            for index, row in self.csv.iterrows():
                params = {
                    "start": row["date_start"],
                    "end": row["date_end"],
                    "latitude": row[self.latitude_column],
                    "longitude": row[self.longitude_column],
                    "community": self.community.value,
                    "parameters": param,
                    "format": format.value,
                    "user": "cloud",
                    "header": True,
                    "time-standard": 'lst',
                }
                response = session.get(url=self.url, params=params)
                result = response.json()["properties"]["parameter"]
                if self.operation == OperationEnum.AVG_ALL:
                    avg = sum(result[param].values()) / \
                        float(len(result[param]))
                    self.csv.at[index, param] = avg

    def save(self, save_file):
        self.csv.to_csv(save_file, index=True)


class WeatherPlot():
    def __init__(self) -> None:
        self.session = requests_cache.CachedSession('wheat_cache')

    def add_years(self, start_date: date, years: int):
        try:
            return start_date.replace(year=start_date.year + years)
        except ValueError:
            return start_date.replace(year=start_date.year + years, day=28)

    def get_data(
        self,
        url: ServerPowerEnum,
        gps: CountryGPS,
        start_date: date,
        end_date: date,
        parameter: ParameterEnum,
        community: CommunityEnum = CommunityEnum.RE,
        format: FormatEnum = FormatEnum.JSON,
        name_column: str = "",
    ) -> pd.DataFrame:
        if name_column == "":
            name_column = parameter.value
        df = pd.DataFrame({'time': [], name_column: []})
        year_parameter = YearParameter(start=start_date, end=end_date, url=url)
        for _ in range(start_date.year, end_date.year):
            year_parameter.add(increase=1)
            start_step_date, end_step_year = year_parameter.get_dates()
            params = {
                "start": start_step_date,
                "end": end_step_year,
                "latitude": gps.latitude,
                "longitude": gps.longitude,
                "community": community.value,
                "parameters": parameter.value,
                "format": format.value,
                "user": "cloud",
                "header": True,
                "time-standard": 'lst',
            }
            response = self.session.get(url=url.value, params=params)
            if response.status_code == 200:
                result = response.json()["properties"]["parameter"]
                for key in result[parameter.value]:
                    df.loc[len(df.index)] = [key, result[parameter.value][key]]
        return df

    def plot_from_point_2001(
        self,
        country: CountryGPS,
        years: list[int],
        parameters: list[ParameterEnum],
        endpoints: list[ServerPowerEnum]
    ):
        for enpoint in endpoints:
            for end_year in years:
                start = date(year=2001, month=1, day=1)
                end = date(year=end_year, month=12, day=31)
                folder = "result_test_{}_{}_{}".format(
                    server_power_enum_to_text(enpoint), start.year, end.year
                )
                if not os.path.isdir(folder):
                    os.mkdir(folder)
                for param in parameters:
                    print("Start with {}".format(param.value))
                    df = self.get_data(
                        gps=country,
                        start_date=start,
                        end_date=end,
                        parameter=param,
                        url=enpoint,
                    )
                    param_text = paramter_enum_to_text(param)
                    df.to_csv(
                        "{}/{}_{}_{}_{}.csv".format(
                            folder,
                            param_text,
                            start.year,
                            end.year,
                            country.name,
                        ),
                        index=False,
                    )
                    plt.ioff()
                    fig = plt.figure(figsize=(50, 50))

                    plt.plot(df["time"], df[param.value])
                    # plt.show()
                    plt.title('Grafica de {} {} {} {}'.format(
                        param_text, country.name, start.year, end.year))

                    plt.savefig(
                        "{}/{}_{}_{}_{}.jpg".format(
                            folder,
                            param_text,
                            start.year,
                            end.year,
                            country.name,
                        ),
                    )
                    plt.close(fig)
                    print("Finsh with {}".format(param.value))


class YearParameter():
    def __init__(self, start: date, end: date, url: ServerPowerEnum) -> None:
        self.start = start
        self.end = end
        self.url = url
        self.date_start = start
        self.date_end = None
        self.is_increase = False

    def add_years(self, date_init: date, years: int):
        try:
            return date_init.replace(year=date_init.year + years)
        except ValueError:
            return date_init.replace(year=date_init.year + years, day=28)

    def add(self, increase: int) -> None:
        if self.date_end == None:
            self.date_end = self.add_years(
                date_init=self.date_start, years=increase)
        else:
            self.date_end = self.add_years(
                date_init=self.date_end, years=increase)
            self.date_start = self.add_years(
                date_init=self.date_start, years=increase)
        if self.date_end > self.end:
            self.date_end = self.end

    def get_dates(self) -> tuple[str, str]:
        if self.url == ServerPowerEnum.MONTHLY_URL:
            return "{}".format(self.date_start), "{}".format(self.date_end)
        else:
            return self.date_start.strftime("%Y%m%d"), self.date_end.strftime("%Y%m%d")
