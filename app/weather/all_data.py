from datetime import date
from app.main import ParameterEnum, CommunityEnum, FormatEnum
import requests_cache
import pandas as pd
import numpy as np



class CountryGPS():
    def __init__(self, name: str, latitude: float, longitude: float) -> None:
        self.name = name
        self.latitude = latitude
        self.longitude = longitude


class WeatherLoop:
    def __init__(self, url: str) -> None:
        self.url = url
        self.session = requests_cache.CachedSession('wheat_cache')

    def add_years(self, start_date: date, years: int):
        try:
            return start_date.replace(year=start_date.year + years)
        except ValueError:
            return start_date.replace(year=start_date.year + years, day=28)

    def get_all_data(
        self,
        gps: CountryGPS,
        start_date: date,
        end_date: date,
        parameter: ParameterEnum,
        community: CommunityEnum = CommunityEnum.RE,
        format: FormatEnum = FormatEnum.JSON,
        name_column: str = "",
    ):
        if name_column == "":
            name_column = parameter.value
        start_step_date = start_date
        df = pd.DataFrame({'time': [], name_column: [] })
        for year in range(start_date.year, end_date.year):
            end_step_year = self.add_years(
                start_date=start_step_date, years=1)
            if end_step_year > end_date:
                end_step_year = end_date
            params = {
                "start": start_step_date.strftime("%Y%m%d"),
                "end": end_step_year.strftime("%Y%m%d"),
                "latitude": gps.latitude,
                "longitude": gps.longitude,
                "community": community.value,
                "parameters": parameter.value,
                "format": format.value,
                "user": "cloud",
                "header": True,
                "time-standard": 'lst',
            }
            response = self.session.get(url=self.url, params=params)
            start_step_date = self.add_years(start_date=start_step_date, years=1)
            if response.status_code == 200:
                result = response.json()["properties"]["parameter"]
                for key in result[parameter.value]:
                    df.loc[len(df.index)] = [key, result[parameter.value][key]]                  
        return df
