from weather.all_data import CountryGPS, WeatherLoop
from weather.main import ParameterEnum, paramter_enum_to_text
from datetime import date
import matplotlib.pyplot as plt
import os


def get_mexico():
    mexico = CountryGPS(
        name="MEXICO",
        latitude=27.483333333333334,
        longitude=-109.9833333,
    )
    years = [2020]
    list = [
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

    periods = ['hourly']
    for period in periods:
        for end_year in years:
            start = date(year=2001, month=1, day=1)
            end = date(year=end_year, month=12, day=31)
            folder = "result_test_{}_{}_{}".format(
                period, start.year, end.year
            )
            if not os.path.isdir(folder):
                os.mkdir(folder)
            loop = WeatherLoop(
                url="https://power.larc.nasa.gov/api/temporal/{}/point".format(
                    period)
            )
            for param in list:
                print("Start with {}".format(param.value))
                df = loop.get_all_data(
                    gps=mexico,
                    start_date=start,
                    end_date=end,
                    parameter=param,
                )
                param_text = paramter_enum_to_text(param)
                df.to_csv(
                    "{}/{}_{}_{}_{}.csv".format(
                        folder,
                        param_text,
                        start.year,
                        end.year,
                        mexico.name,
                    ),
                    index=False,
                )
                plt.ioff()
                fig = plt.figure(figsize=(50, 50))

                plt.plot(df["time"], df[param.value])
                # plt.show()
                plt.title('Grafica de {} {} {} {}'.format(
                    param_text, mexico.name, start.year, end.year))

                plt.savefig(
                    "{}/{}_{}_{}_{}.jpg".format(
                        folder,
                        param_text,
                        start.year,
                        end.year,
                        mexico.name,
                    ),
                )
                plt.close(fig)
                print("Finsh with {}".format(param.value))
