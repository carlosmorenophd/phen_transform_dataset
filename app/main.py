import pandas as pd
from enum import Enum


class TransformEnum(Enum):
    PASS = 0
    FILL_AVG = 1
    STR_NONE = 2
    STR_NORMAL = 3
    FORCE_ONE = 4
    DATE_FROM = 5
    FILL_CERO = 6
    STR_NO = 7
    STR_UNKNOWN = 8


class Transform():
    def __init__(self, transformEnum: TransformEnum, column_base: str = "") -> None:
        self.transformEnum = transformEnum
        self.column_base = column_base


class NormalizeEnum(Enum):
    PASS = 0
    ONE_TO_ONE = 1
    ONE_POSITIVE = 2


class Normalize():
    def __init__(self, normalizeEnum: NormalizeEnum) -> None:
        self.normalizeEnum = normalizeEnum


class TransformNormalize:
    def __init__(self, column: str, transform: Transform, normalize: Normalize) -> None:
        self.column = column
        self.transform = transform
        self.normalize = normalize


def transform_N_T_S_M_V(x):
    if x.upper() == "NONE":
        return 0
    elif x.upper() == "TRACES":
        return 1
    elif x.upper() == "SLIGHT":
        return 2
    elif x.upper() == "MODERATE":
        return 3
    elif x.upper() == "SEVERE":
        return 4


def transform_E_N_L(x):
    if x.upper() == "EARLY":
        return 0
    elif x.upper() == "NORMAL":
        return 1
    elif x.upper() == "LATE":
        return 2


def transform_Y_N(x):
    if x.upper() == "YES":
        return 1
    elif x.upper() == "NO":
        return 0

def transform_Y_N_U(x):
    if x.upper() == "YES":
        return 1
    elif x.upper() == "NO":
        return -1
    elif x.upper() == "UNKNOWN":
        return 0

def calculate_avg(column_data) -> float:
    elements = list(
        filter(lambda i: not pd.isnull(i), column_data)
    )
    return sum(elements) / len(elements)


class Preprocessing ():
    def __init__(self, save_file: str, name_file: str, actions: list[TransformNormalize]) -> None:
        self.save_file = save_file
        self.actions = actions
        self.csv = pd.read_csv(name_file)
        self.csv_process = pd.DataFrame()

    def transform(self):
        import re
        """ Apply the all transformation on actions
        """
        for action in self.actions:
            enum = action.transform.transformEnum
            column = action.column
            if enum == TransformEnum.FILL_AVG:

                self.csv_process[column] = self.csv[column].fillna(
                    calculate_avg(column_data=self.csv.loc[:, column])
                )
            elif enum == TransformEnum.STR_NONE:
                self.csv_process[column] = self.csv[column].fillna('NONE')
            elif enum == TransformEnum.STR_NORMAL:
                self.csv_process[column] = self.csv[column].fillna('NORMAL')
            elif enum == TransformEnum.PASS:
                self.csv_process[column] = self.csv[column]
            elif enum == TransformEnum.FORCE_ONE:
                self.csv_process[column] = self.csv[column].apply(
                    lambda item: 1
                )
            elif enum == TransformEnum.DATE_FROM:
                date_base = action.transform.column_base
                self.csv_process[column] = (
                    pd.to_datetime(self.csv[column])
                    -
                    pd.to_datetime(self.csv[date_base])
                ).dt.days
                self.csv_process[column] = self.csv_process[column].fillna(
                    calculate_avg(column_data=self.csv_process[column])
                )
            elif enum == TransformEnum.FILL_CERO:
                self.csv_process[column] = self.csv[column].fillna(0)
            elif enum == TransformEnum.STR_NO:
                self.csv_process[column] = self.csv[column].fillna('NO')
            elif enum == TransformEnum.STR_UNKNOWN:
                self.csv_process[column] = self.csv[column].fillna('UNKNOWN')

            if re.search("\(N/T/S/M/V\)$", column):
                self.csv_process[column] = self.csv_process[column].apply(
                    transform_N_T_S_M_V
                )
            elif re.search("\(E/N/L\)$", column):
                self.csv_process[column] = self.csv_process[column].apply(
                    transform_E_N_L
                )
            elif re.search("\(Y/N/U\)$", column):
                self.csv_process[column] = self.csv_process[column].apply(
                    transform_Y_N_U
                )
            elif re.search("\(Y/N\)$", column):
                self.csv_process[column] = self.csv_process[column].apply(
                    transform_Y_N
                )
            


    def normalize(self):
        """ Normalize the data set
        """
        for action in actions:
            enum = action.normalize.normalizeEnum
            column = action.column
            if enum == NormalizeEnum.PASS:
                self.csv_process[column] = self.csv_process[column]
            elif enum == NormalizeEnum.ONE_POSITIVE:
                max = self.csv_process[column].max()
                min = self.csv_process[column].min()
                self.csv_process[column] = self.csv_process[column].map(
                    lambda item: ((item - min) / (max - min)))
            elif enum == NormalizeEnum.ONE_TO_ONE:
                max = self.csv_process[column].max()
                min = self.csv_process[column].min()
                self.csv_process[column] = self.csv_process[column].map(
                    lambda item: (
                        (2 * ((item - min) / (max - min))) - 1
                    )
                )

    def save(self, is_save_origin: bool = False, is_index: bool = False):
        from os import path, remove
        if path.exists(self.save_file):
            remove(self.save_file)
        self.csv_process.to_csv(self.save_file, index=is_index)
        if is_save_origin:
            self.csv.to_csv("origin_{0}".format(
                self.save_file), index=is_index)


def doRun(save_file: str, name_file: str, actions: list[TransformNormalize]):
    preprocessing = Preprocessing(
        name_file=name_file, save_file=save_file, actions=actions)
    preprocessing.transform()
    preprocessing.normalize()
    preprocessing.save()


if __name__ == "__main__":
    actions = []
    actions.append(
        TransformNormalize(
            column="GRAIN_YIELD:(t/ha):avg",
            transform=Transform(transformEnum=TransformEnum.PASS),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE),
        )
    )
    actions.append(
        TransformNormalize(
            column='SOWING_DATE:(date)',
            transform=Transform(transformEnum=TransformEnum.FORCE_ONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS),
        )
    )
    actions.append(
        TransformNormalize(
            column='AREA_HARVESTED_BED_PLOT_M2:(m2)',
            transform=Transform(transformEnum=TransformEnum.FILL_AVG),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE),
        )
    )
    actions.append(
        TransformNormalize(
            column='AREA_SOWN_BED_PLOT_M2:(m2)',
            transform=Transform(TransformEnum.FILL_AVG),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='BIRD_DAMAGE:(N/T/S/M/V)',
            transform=Transform(TransformEnum.STR_NONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
        )
    )
    actions.append(
        TransformNormalize(
            column='EMERGENCE:(E/N/L)',
            transform=Transform(TransformEnum.STR_NORMAL),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='HARVEST_STARTING_DATE:(date)',
            transform=Transform(TransformEnum.DATE_FROM,
                                column_base="SOWING_DATE:(date)"),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
        )
    )
    actions.append(
        TransformNormalize(
            column='EMERGENCE_DATE:(date)',
            transform=Transform(TransformEnum.DATE_FROM,
                                column_base="SOWING_DATE:(date)"),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
        )
    )
    actions.append(
        TransformNormalize(
            column='FERTILIZER_%K2O_1:(%)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='FERTILIZER_%N_1:(%)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='FERTILIZER_%P2O5_1:(%)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='FERTILIZER_1:(date)',
            transform=Transform(TransformEnum.DATE_FROM,
                                column_base="SOWING_DATE:(date)"),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
        )
    )
    actions.append(
        TransformNormalize(
            column='FOLIAR_DISEASE_DEVELOPMENT:(N/T/S/M/V)',
            transform=Transform(TransformEnum.STR_NONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
        )
    )
    actions.append(
        TransformNormalize(
            column='FROST_DAMAGE_SPIKE:(N/T/S/M/V)',
            transform=Transform(TransformEnum.STR_NONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
        )
    )
    actions.append(
        TransformNormalize(
            column='HAIL_DAMAGE:(N/T/S/M/V)',
            transform=Transform(TransformEnum.STR_NONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
        )
    )
    actions.append(
        TransformNormalize(
            column='HERBICIDE_DAMAGE:(N/T/S/M/V)',
            transform=Transform(TransformEnum.STR_NONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
        )
    )
    actions.append(
        TransformNormalize(
            column='HERBICIDE:(Y/N)',
            transform=Transform(TransformEnum.STR_NO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='IRRIGATED:(Y/N)',
            transform=Transform(TransformEnum.STR_NO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='INSECT_DAMAGE:(N/T/S/M/V)',
            transform=Transform(TransformEnum.STR_NONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
        )
    )
    actions.append(
        TransformNormalize(
            column='LODGING:(N/T/S/M/V)',
            transform=Transform(TransformEnum.STR_NONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
        )
    )
    actions.append(
        TransformNormalize(
            column='LODGING:(N/T/S/M/V)',
            transform=Transform(TransformEnum.STR_NONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
        )
    )
    actions.append(
        TransformNormalize(
            column='NO_OF_ROWS_HARVESTED:(integer)',
            transform=Transform(TransformEnum.FILL_AVG),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='NO_OF_ROWS_SOWN:(integer)',
            transform=Transform(TransformEnum.FILL_AVG),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='NUMBER_POST_SOWING_IRRIGATIONS:(integer)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='NUMBER_PRE_SOWING_IRRIGATIONS:(integer)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PPN_MONTH_OF_HARVESTED:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PPN_1ST_MO_BEFORE_HARVESTED:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PPN_2ND_MO_BEFORE_HARVESTED:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PPN_3RD_MO_BEFORE_HARVESTED:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PPN_4TH_MO_BEFORE_HARVESTED:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PPN_5TH_MO_BEFORE_HARVESTED:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PPN_6TH_MO_BEFORE_HARVESTED:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PPN_7TH_MO_BEFORE_HARVESTED:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PPN_8TH_MO_BEFORE_HARVESTED:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PPN_9TH_MO_BEFORE_HARVESTED:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PPN_10TH_MO_BEFORE_HARVESTED:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PPN_11TH_MO_BEFORE_HARVESTED:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PRE_SOWING_IRRIGATION:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='PRECIPITATION_FROM_SOWING_TO_MATURITY:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='ROOT_DISEASE_DEVELOPMENT:(N/T/S/M/V)',
            transform=Transform(TransformEnum.STR_NONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
        )
    )
    actions.append(
        TransformNormalize(
            column='SOIL_ALUMINIUM_TOXICITY:(Y/N)',
            transform=Transform(TransformEnum.STR_NO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='SPIKE_DISEASE_DEVELOPMENT:(N/T/S/M/V)',
            transform=Transform(TransformEnum.STR_NONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
        )
    )
    actions.append(
        TransformNormalize(
            column='TOTAL_PRECIPIT_IN_12_MONTHS:(mm)',
            transform=Transform(TransformEnum.FILL_AVG),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='WEED_PROBLEM:(N/T/S/M/V)',
            transform=Transform(TransformEnum.STR_NONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
        )
    )
    actions.append(
        TransformNormalize(
            column='YIELD_FACTOR:(real)',
            transform=Transform(TransformEnum.FILL_AVG),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='IRRIGATION_AFTER_SOWING:(mm)',
            transform=Transform(TransformEnum.FILL_CERO),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )
    actions.append(
        TransformNormalize(
            column='SOIL_ROOT_BARRIER:(Y/N/U)',
            transform=Transform(TransformEnum.STR_UNKNOWN),
            normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
        )
    )


	


    	



    doRun(
        save_file='test.csv',
        name_file='./origin_test.csv',
        actions=actions
    )
