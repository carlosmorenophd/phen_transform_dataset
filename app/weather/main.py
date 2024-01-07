from enum import Enum
import pandas as pd
import requests_cache




class FormatEnum(Enum):
    JSON = "json"


class CommunityEnum(Enum):
    RE = "re"


class OperationEnum(Enum):
    AVG_ALL = 1


def do_run(
    name_file: str,
    latitude_column: str,
    longitude_column: str,
    start_date_column: str,
    end_date_column: str,
    parameters: list,
    save_file: str,
    format: FormatEnum = FormatEnum.JSON,
    community: CommunityEnum = CommunityEnum.RE,
    operation: OperationEnum = OperationEnum.AVG_ALL,
):
    url = 'https://power.larc.nasa.gov/api/temporal/hourly/point'
    csv = pd.read_csv(name_file)
    csv["date_start"] = pd.to_datetime(csv[start_date_column])
    csv["date_start"] = csv["date_start"].dt.strftime('%Y%m%d')
    csv["date_end"] = pd.to_datetime(csv[end_date_column])
    csv["date_end"] = csv["date_end"].dt.strftime('%Y%m%d')
    session = requests_cache.CachedSession('wheat_cache')
    for param in parameters:
        csv[param] = 0.0
    for index, row in csv.iterrows():
        params = {
            "start": row["date_start"],
            "end": row["date_end"],
            "latitude": row[latitude_column],
            "longitude": row[longitude_column],
            "community": community.value,
            "parameters": ','.join(parameters),
            "format": format.value,
            "user": "cloud",
            "header": True,
            "time-standard": 'lst',
        }
        response = session.get(url=url, params=params)
        result = response.json()["properties"]["parameter"]
        for param in parameters:
            if operation == OperationEnum.AVG_ALL:
                avg = sum(result[param].values()) / float(len(result[param]))
                csv.at[index, param] = avg
    csv.to_csv(save_file, index=True)


if __name__ == "__main__":
    name_file = "dataset_wheat.csv"
    latitude_column = "GPS Latitude (Decimal)"
    longitude_column = "GPS Longitude (Decimal)"
    start_date_column = "SOWING_DATE:(date)"
    end_date_column = "HARVEST_STARTING_DATE:(date)"
    parameters = ["ALLSKY_SFC_SW_DWN"]
    save_file = "test_wheat.csv"
    do_run(
        name_file=name_file,
        latitude_column=latitude_column,
        longitude_column=longitude_column,
        start_date_column=start_date_column,
        end_date_column=end_date_column,
        parameters=parameters,
        save_file=save_file,
    )
