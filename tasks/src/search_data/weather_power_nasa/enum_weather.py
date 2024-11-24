"""Get all data class and enum for weather"""
from dataclasses import dataclass
from enum import Enum
import json


class FormatPowerApiEnum(Enum):
    """Type of format for power API

    Args:
        Enum (_type_): _description_
    """
    JSON = "json"


class CommunityPowerApiEnum(Enum):
    """Type of community for power API

    Args:
        Enum (_type_): _description_
    """
    RE = "re"


class FeaturesPowerApiEnum(Enum):
    """Enum to get from server

    Args:
        Enum (_type_): _description_
    """
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


@dataclass
class ColumnDefinition():
    """All column to get information from power API
    """
    latitude_column: str
    longitude_column: str
    start_date_column: str
    end_date_column: str


class UrlPowerAPIEnum(Enum):
    """List of endpoint to get data from nasa power API

    Args:
        Enum (_type_): _description_
    """
    HOURLY_URL = "https://power.larc.nasa.gov/api/temporal/hourly/point"
    DAILY_URL = "https://power.larc.nasa.gov/api/temporal/dayly/point"
    MONTHLY_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"


def feature_power_to_text_spanish(param: FeaturesPowerApiEnum) -> str:
    """Cat enum to spanish definition

    Args:
        param (ParameterEnum): parameter to cast

    Returns:
        str: definition on spanish
    """
    if param == FeaturesPowerApiEnum.ALLSKY_SFC_SW_DWN:
        return "radiacion_total"
    if param == FeaturesPowerApiEnum.CLRSKY_SFC_SW_DWN:
        return "radiacion_alncaza_superficie"
    if param == FeaturesPowerApiEnum.ALLSKY_KT:
        return "radiacion_sin_nubes"
    if param == FeaturesPowerApiEnum.ALLSKY_SFC_LW_DWN:
        return "total_radiacion_onda_larga"
    if param == FeaturesPowerApiEnum.ALLSKY_SFC_PAR_TOT:
        return "total_radiacion_fotosimetica"
    if param == FeaturesPowerApiEnum.CLRSKY_SFC_PAR_TOT:
        return "radiacion_fotosimetica"
    if param == FeaturesPowerApiEnum.ALLSKY_SFC_UVA:
        return "uva"
    if param == FeaturesPowerApiEnum.ALLSKY_SFC_UVB:
        return "uvb"
    if param == FeaturesPowerApiEnum.ALLSKY_SFC_UV_INDEX:
        return "dencidad_radiacion"
    if param == FeaturesPowerApiEnum.T2M:
        return "temperatura_2"
    if param == FeaturesPowerApiEnum.T2MDEW:
        return "punto_congelacion_2"
    if param == FeaturesPowerApiEnum.T2MWET:
        return "temperatura_bulbo_humedo_2"
    if param == FeaturesPowerApiEnum.TS:
        return "temperatura_piel_tierra"
    if param == FeaturesPowerApiEnum.T2M_RANGE:
        return "temperatura_range_2"
    if param == FeaturesPowerApiEnum.T2M_MAX:
        return "temperatura_max_2"
    if param == FeaturesPowerApiEnum.T2M_MIN:
        return "temperatura_min_2"
    if param == FeaturesPowerApiEnum.QV2M:
        return "humedad_espeficica_2"
    if param == FeaturesPowerApiEnum.RH2M:
        return "humedad_realtiva_2"
    if param == FeaturesPowerApiEnum.PRECTOTCORR:
        return "precipitacion_pluvial"
    if param == FeaturesPowerApiEnum.PS:
        return "presion_atmosferica"
    if param == FeaturesPowerApiEnum.WS10M:
        return "velocidad_viento_10"
    if param == FeaturesPowerApiEnum.WS10M_MAX:
        return "velocidad_viento_max_10"
    if param == FeaturesPowerApiEnum.WS10M_MIN:
        return "velocidad_viento_min_10"
    if param == FeaturesPowerApiEnum.WS10M_RANGE:
        return "velocidad_viento_rango_10"
    if param == FeaturesPowerApiEnum.WD10M:
        return "direccion_viento_10"
    if param == FeaturesPowerApiEnum.WS50M:
        return "velocidad_viento_50"
    if param == FeaturesPowerApiEnum.WS50M_MAX:
        return "velocidad_viento_max_50"
    if param == FeaturesPowerApiEnum.WS50M_MIN:
        return "velocidad_viento_min_50"
    if param == FeaturesPowerApiEnum.WS50M_RANGE:
        return "velocidad_viento_rango_50"
    if param == FeaturesPowerApiEnum.WD50M:
        return "direccion_viento_50"
    raise NotImplementedError("In valid enum ")


def url_power_enum_to_text(server: UrlPowerAPIEnum):
    """get text of 

    Args:
        server (ServerPowerEnum): _description_

    Raises:
        NotImplementedError: _description_

    Returns:
        _type_: _description_
    """
    if server == UrlPowerAPIEnum.HOURLY_URL:
        return "hourly"
    if server == UrlPowerAPIEnum.DAILY_URL:
        return "daily"
    if server == UrlPowerAPIEnum.MONTHLY_URL:
        return "mouthy"
    raise NotImplementedError("Not valid server power enum")


class TransformWeatherActionEnum(Enum):
    """Action to transform weather"""
    ALL = "all"
    NO_TRANSFORM = "no_transform"
    MEAN = "mean"
    MAX = "max"
    MINUS = "minus"


def convert_string_to_transform_weather_action(action_str) -> TransformWeatherActionEnum:
    """Cast str into action

    Returns:
        TransformWeatherActionEnum: action to work with it on API
    """
    if action_str == TransformWeatherActionEnum.ALL.value:
        return TransformWeatherActionEnum.ALL
    if action_str == TransformWeatherActionEnum.NO_TRANSFORM.value:
        return TransformWeatherActionEnum.NO_TRANSFORM
    if action_str == TransformWeatherActionEnum.MAX.value:
        return TransformWeatherActionEnum.MAX
    if action_str == TransformWeatherActionEnum.MINUS.value:
        return TransformWeatherActionEnum.MINUS
    raise ModuleNotFoundError("Convert not valid - for normalize action")


def convert_string_to_column_definition(column_definition_str) -> ColumnDefinition:
    """Convert string into columns definition

    Args:
        action_str (_type_): string to cast

    Returns:
        ColumnDefinition: object column definition
    """
    column_definition = json.loads(column_definition_str)
    if "latitude_column" not in column_definition:
        raise NameError("latitude_column don't exist")
    if "longitude_column" not in column_definition:
        raise NameError("longitude_column don't exist")
    if "start_date_column" not in column_definition:
        raise NameError("start_date_column don't exist")
    if "end_date_column" not in column_definition:
        raise NameError("end_date_column don't exist")
    return column_definition


def convert_string_to_feature_power_list_(column_definition_str) -> list[FeaturesPowerApiEnum]:
    """Cast string to list of features power api

    Args:
        column_definition_str (_type_): string to cast

    Returns:
        list[FeaturesPowerApiEnum]: list off features
    """

    if column_definition_str == "ALL_ALL":
        return [features.value for features in FeaturesPowerApiEnum]
    if "," in column_definition_str:
        features = []
        for input_str in column_definition_str.split(","):
            features.append(convert_string_to_feature_power(input_str=input_str))
        return features
    raise NameError("don't exist this values on features power api")


def convert_string_to_feature_power(input_str) -> FeaturesPowerApiEnum:
    """Cast one text to single feature power api

    Args:
        input_str (_type_): text to cast

    Raises:
        NameError: Feature

    Returns:
        FeaturesPowerApiEnum: Error feature not valid
    """
    for feature in FeaturesPowerApiEnum:
        if feature.value == input_str:
            return feature.value
    raise NameError(f"Feature not valid {input_str}")
# class CountryGPS():
#     """Class with country and geo reference
#     """
#     def __init__(self, name: str, latitude: float, longitude: float) -> None:
#         self.name = name
#         self.latitude = latitude
#         self.longitude = longitude
