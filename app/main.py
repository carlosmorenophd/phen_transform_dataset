import pandas as pd
from enum import Enum


class Convert:
    def __init__(self, name: str, action) -> None:
        self.name = name
        self.action = action


class ActionToFill(Enum):
    AVG = 1
    FILL_CERO = 2
    ENUM_NONE = 3
    ENUM_NORMAL = 4



def find(name: str, actions) -> Convert:
    return list(filter(lambda item: item.name == name, actions))


def doRun(save_file: str, name_file: str, actions):
    csv_data = pd.read_csv(name_file)
    for column in csv_data.columns:
        filtered = find(name=column, actions=actions)
        if len(filtered) == 1:
            if filtered[0].action == ActionToFill.AVG:
                elements = list(
                    filter(lambda i: not pd.isnull(i), csv_data.loc[:, column]))
                csv_data[column] = csv_data[column].fillna(
                    sum(elements) / len(elements))
            elif filtered[0].action == ActionToFill.ENUM_NONE:
                csv_data[column] = csv_data[column].fillna('NONE')
            elif filtered[0].action == ActionToFill.FILL_CERO:
                csv_data[column] = csv_data[column].fillna(0)
            elif filtered[0].action == ActionToFill.ENUM_NORMAL:
                csv_data[column] = csv_data[column].fillna('NORMAL')
            # TODO: create a new function to put a date according the avg between the snow date
    save(pd=csv_data, name=save_file)


def save(pd, name: str, index: bool = False) -> None:
    from os import path, remove
    if path.exists(name):
        remove(name)
    pd.to_csv(name, index=index)


if __name__ == "__main__":
    actions = []
    actions.append(
        Convert(name='AREA_HARVESTED_BED_PLOT_M2:(m2)', action=ActionToFill.AVG))
    actions.append(
        Convert(name='AREA_SOWN_BED_PLOT_M2:(m2)', action=ActionToFill.AVG))
    actions.append(
        Convert(name='BIRD_DAMAGE:(N/T/S/M/V)', action=ActionToFill.ENUM_NONE))
    actions.append(
        Convert(name='EMERGENCE:(E/N/L)', action=ActionToFill.ENUM_NORMAL))
    

    doRun(
        save_file='test.csv',
        name_file='./origin_test.csv',
        actions=actions
    )
