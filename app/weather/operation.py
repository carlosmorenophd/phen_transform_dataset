from enum import Enum
import pandas as pd
import requests_cache

class ParameterEnum(Enum):
    ALLSKY_SFC_SW_DWN = "ALLSKY_SFC_SW_DWN"
    CLRSKY_SFC_SW_DWN = "CLRSKY_SFC_SW_DWN"
    ALLSKY_KT = "ALLSKY_KT"
    ALLSKY_SFC_LW_DWN = "ALLSKY_SFC_LW_DWN"
    ALLSKY_SFC_PAR_TOT = "ALLSKY_SFC_PAR_TOT"
    CLRSKY_SFC_PAR_TOT = "CLRSKY_SFC_PAR_TOT"
    ALLSKY_SFC_UVA = "ALLSKY_SFC_UVA"
    ALLSKY_SFC_UVB = "ALLSKY_SFC_UVB"
    ALLSKY_SFC_UV_INDEX = "ALLSKY_SFC_UV_INDEX"
    T2M = "T2M"
    T2MDEW = "T2MDEW"
    T2MWET = "T2MWET"
    TS = "TS"
    T2M_RANGE = "T2M_RANGE"
    T2M_MAX = "T2M_MAX"
    T2M_MIN = "T2M_MIN"
    QV2M = "QV2M"
    RH2M = "RH2M"
    PRECTOTCORR = "PRECTOTCORR"
    PS = "PS"
    WS10M = "WS10M"
    WS10M_MAX = "WS10M_MAX"
    WS10M_MIN = "WS10M_MIN"
    WS10M_RANGE = "WS10M_RANGE"
    WD10M = "WD10M"
    WS50M = "WS50M"
    WS50M_MAX = "WS50M_MAX"
    WS50M_MIN = "WS50M_MIN"
    WS50M_RANGE = "WS50M_RANGE"
    WD50M = "WD50M"


class GetWheat():
    def __init__(
        self,
        name_file: str,
        latitude_column: str,
        longitude_column: str,
        start_date_column: str,
        end_date_column: str,
        parameters: list(ParameterEnum),
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
        self.csv["date_start"] = pd.to_datetime(self.csv[self.start_date_column])
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
                    avg = sum(result[param].values()) / float(len(result[param]))
                    self.csv.at[index, param] = avg
    def save(self, save_file):
        self.csv.to_csv(save_file, index=True)
