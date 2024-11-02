from weather.power_nasa.enum import CountryGPS, ParameterEnum, ServerPowerEnum
from weather.power_nasa.power import WeatherPlot


if __name__ == "__main__":
    mexico = CountryGPS(
        name="MEXICO",
        latitude=27.483333333333334,
        longitude=-109.9833333,
    )
    years = [2002]
    parameters = [
        ParameterEnum.ALLSKY_SFC_SW_DWN,
        ParameterEnum.CLRSKY_SFC_SW_DWN,
        ParameterEnum.ALLSKY_KT,
        ParameterEnum.ALLSKY_SFC_LW_DWN,
        ParameterEnum.ALLSKY_SFC_PAR_TOT,
        ParameterEnum.CLRSKY_SFC_PAR_TOT,
        ParameterEnum.ALLSKY_SFC_UVA,
        ParameterEnum.ALLSKY_SFC_UVB,
        ParameterEnum.ALLSKY_SFC_UV_INDEX,
        ParameterEnum.T2M,
        ParameterEnum.T2MDEW,
        ParameterEnum.T2MWET,
        ParameterEnum.TS,
        ParameterEnum.T2M_RANGE,
        ParameterEnum.T2M_MAX,
        ParameterEnum.T2M_MIN,
        ParameterEnum.QV2M,
        ParameterEnum.RH2M,
        ParameterEnum.PRECTOTCORR,
        ParameterEnum.PS,
        ParameterEnum.WS10M,
        ParameterEnum.WS10M_MAX,
        ParameterEnum.WS10M_MIN,
        ParameterEnum.WS10M_RANGE,
        ParameterEnum.WD10M,
        ParameterEnum.WS50M,
        ParameterEnum.WS50M_MAX,
        ParameterEnum.WS50M_MIN,
        ParameterEnum.WS50M_RANGE,
        ParameterEnum.WD50M,
    ]

    endpoints = [ServerPowerEnum.DAILY_URL]

    plot = WeatherPlot()
    plot.plot_from_point_2001(
        country=mexico, parameters=parameters, endpoints=endpoints,years=years
    )
