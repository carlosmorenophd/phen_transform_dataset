import pandas as pd
from enum import Enum


class TransformEnum(Enum):
    PASS = 0
    FILL_AVG = 1
    STR_NONE = 2
    STR_NORMAL = 3
    FORCE_ONE = 4


class Transform():
    def __init__(self, transformEnum: TransformEnum, column_base: str = "") -> None:
        self.transformEnum = transformEnum
        self.column_base = column_base


class NormalizeEnum(Enum):
    PASS = 0
    ONE_TO_ONE = 1
    ONE_POSITIVE = 2
    THREE_TO_THREE = 3
    THREE_POSITIVE = 4


class Normalize():
    def __init__(self, normalizeEnum: NormalizeEnum) -> None:
        self.normalizeEnum = normalizeEnum


class TransformNormalize:
    def __init__(self, column: str, transform: Transform, normalize: Normalize) -> None:
        self.column = column
        self.transform = transform
        self.normalize = normalize


class Preprocessing ():
    def __init__(self, save_file: str, name_file: str, actions: list[TransformNormalize]) -> None:
        self.save_file = save_file
        self.actions: actions
        self.csv = pd.read_csv(name_file)
        self.csv_process = pd.DataFrame()

    def transform(self):
        # Transform data
        for action in self.actions:
            enum = action.transform.transformEnum
            column = action.column
            if enum == TransformEnum.FILL_AVG:
                elements = list(
                    filter(lambda i: not pd.isnull(i), self.csv.loc[:, column]))
                self.csv_process[column] = self.csv[column].fillna(
                    sum(elements) / len(elements))
            elif enum == TransformEnum.STR_NONE:
                self.csv_process[column] = self.csv[column].fillna('NONE')
            elif enum == TransformEnum.STR_NORMAL:
                self.csv_process[column] = self.csv[column].fillna('NORMAL')
            elif enum == TransformEnum.PASS:
                self.csv_process[column] = self.csv[column]
            # TODO: create a new function to put a date according the avg between the snow date

    def normalize(self):
        # Normalize data
        for action in actions:
            enum = action.normalize.normalizeEnum
            column = action.column
            if enum == NormalizeEnum.PASS:
                self.csv_process[column] = self.csv_process[column]
            elif enum == NormalizeEnum.ONE_POSITIVE:
                max = self.csv_process[column].max()
                min = self.csv_process[column].min()
                self.csv_process[column] = self.csv_process[column].map(lambda item: ((item - min) / (max - min)))

    def save(self, is_save_origin: bool = True, is_index: bool = False):
        from os import path, remove
        if path.exists(self.save_file):
            remove(self.save_file)
        self.csv_process(self.save_file, index=is_index)
        if is_save_origin:
            self.csv("origin_{0}"self.save_file, index=is_index)



def doRun(save_file: str, name_file: str, actions: list[TransformNormalize]):
    preprocessing=Preprocessing(name_file=name_file, save_file=save_file, actions=actions)
    preprocessing.transform()
    preprocessing.normalize()
    preprocessing.save()
    
    


def save(pd, name: str, index: bool = False) -> None:
    


if __name__ == "__main__":
    actions = []
    actions.append(
        TransformNormalize(
            column="GRAIN_YIELD:(t/ha):avg",
            transform=Transform(transformEnum=TransformEnum.PASS),
            normalize=Normalize(normalizeEnum=NormalizeEnum.THREE_POSITIVE),
        )
    )
    actions.append(
        TransformNormalize(
            column='SOWING_DATE:(date)',
            transform=Transform(transformEnum=TransformEnum.PASS),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS),
        )
    )
    actions.append(
        TransformNormalize(
            column='AREA_HARVESTED_BED_PLOT_M2:(m2)',
            transform=Transform(transformEnum=TransformEnum.FILL_AVG),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS),
        )
    )
    actions.append(
        TransformNormalize(
            column='AREA_SOWN_BED_PLOT_M2:(m2)',
            transform=Transform(TransformEnum.FILL_AVG),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
        )
    )
    actions.append(
        TransformNormalize(
            column='BIRD_DAMAGE:(N/T/S/M/V)',
            transform=Transform(TransformEnum.STR_NONE),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
        )
    )
    actions.append(
        TransformNormalize(
            column='EMERGENCE:(E/N/L)',
            transform=Transform(TransformEnum.STR_NORMAL),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
        )
    )

    doRun(
        save_file='test.csv',
        name_file='./origin_test.csv',
        actions=actions
    )
