from enum import Enum


class FormatEnum(Enum):
    JSON = "json"


class CommunityEnum(Enum):
    RE = "re"


class OperationEnum(Enum):
    AVG_ALL = 1
    CREATE_FILE = 2


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


class ServerPowerEnum(Enum):
    HOURLY_URL = "https://power.larc.nasa.gov/api/temporal/hourly/point"
    DAILY_URL = "https://power.larc.nasa.gov/api/temporal/dayly/point"
    MONTHLY_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"


def paramter_enum_to_text(param: ParameterEnum) -> str:
    if param == ParameterEnum.ALLSKY_SFC_SW_DWN:
        return "radiacion_total"
    elif param == ParameterEnum.CLRSKY_SFC_SW_DWN:
        return "radiacion_alncaza_superficie"
    elif param == ParameterEnum.ALLSKY_KT:
        return "radiacion_sin_nubes"
    elif param == ParameterEnum.ALLSKY_SFC_LW_DWN:
        return "total_radiacion_onda_larga"
    elif param == ParameterEnum.ALLSKY_SFC_PAR_TOT:
        return "total_radiacion_fotosimetica"
    elif param == ParameterEnum.CLRSKY_SFC_PAR_TOT:
        return "radiacion_fotosimetica"
    elif param == ParameterEnum.ALLSKY_SFC_UVA:
        return "uva"
    elif param == ParameterEnum.ALLSKY_SFC_UVB:
        return "uvb"
    elif param == ParameterEnum.ALLSKY_SFC_UV_INDEX:
        return "dencidad_radiacion"
    elif param == ParameterEnum.T2M:
        return "temperatura_2"
    elif param == ParameterEnum.T2MDEW:
        return "punto_congelacion_2"
    elif param == ParameterEnum.T2MWET:
        return "temperatura_bulbo_humedo_2"
    elif param == ParameterEnum.TS:
        return "temperatura_piel_tierra"
    elif param == ParameterEnum.T2M_RANGE:
        return "temperatura_range_2"
    elif param == ParameterEnum.T2M_MAX:
        return "temperatura_max_2"
    elif param == ParameterEnum.T2M_MIN:
        return "temperatura_min_2"
    elif param == ParameterEnum.QV2M:
        return "humedad_espeficica_2"
    elif param == ParameterEnum.RH2M:
        return "humedad_realtiva_2"
    elif param == ParameterEnum.PRECTOTCORR:
        return "precipitacion_pluvial"
    elif param == ParameterEnum.PS:
        return "presion_atmosferica"
    elif param == ParameterEnum.WS10M:
        return "velocidad_viento_10"
    elif param == ParameterEnum.WS10M_MAX:
        return "velocidad_viento_max_10"
    elif param == ParameterEnum.WS10M_MIN:
        return "velocidad_viento_min_10"
    elif param == ParameterEnum.WS10M_RANGE:
        return "velocidad_viento_rango_10"
    elif param == ParameterEnum.WD10M:
        return "direccion_viento_10"
    elif param == ParameterEnum.WS50M:
        return "velocidad_viento_50"
    elif param == ParameterEnum.WS50M_MAX:
        return "velocidad_viento_max_50"
    elif param == ParameterEnum.WS50M_MIN:
        return "velocidad_viento_min_50"
    elif param == ParameterEnum.WS50M_RANGE:
        return "velocidad_viento_rango_50"
    elif param == ParameterEnum.WD50M:
        return "direccion_viento_50"
    else:
        return ""


def server_power_enum_to_text(server: ServerPowerEnum):
    if server == ServerPowerEnum.HOURLY_URL:
        return "hourly"
    elif server == ServerPowerEnum.DAILY_URL:
        return "daily"
    elif server == ServerPowerEnum.MONTHLY_URL:
        return "mouthy"
    else:
        return ""


class CountryGPS():
    def __init__(self, name: str, latitude: float, longitude: float) -> None:
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
