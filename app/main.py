import pandas as pd
from enum import Enum


class Convert:
    def __init__(self, name: str, action) -> None:
        self.name = name
        self.action = action


class ActionToFill(Enum):
    AVG = 1
    NONE_FILL = 2


def find(name: str, actions) -> Convert:
    return list(filter(lambda item: item.name == name, actions))


def doRun(save_file: str, name_file: str, actions):
    csv_data = pd.read_csv(name_file)
    for column in csv_data.columns:
        filtered = find(name=column, actions=actions)
        if len(filtered) == 1:
            print(filtered[0].name)
            elements = list(
                filter(lambda i: not pd.isnull(i), csv_data.loc[:, column]))
            csv_data[column] = csv_data[column].fillna(
                sum(elements) / len(elements))
            # TODO:  remplace all null with avg
    save(pd=csv_data, name=save_file)


def save(pd, name: str, index:bool = False) -> None:
    from os import path, remove
    if path.exists(name):
        remove(name)
    pd.to_csv(name, index=index)

    pd.to_csv()


if __name__ == "__main__":
    actions = []
    actions.append(
        Convert(name='AREA_HARVESTED_BED_PLOT_M2:(m2)', action=ActionToFill.AVG))
    actions.append(
        Convert(name='AREA_SOWN_BED_PLOT_M2:(m2)', action=ActionToFill.AVG))
    doRun(
        save_file='test.csv',
        name_file='./origin_test.csv',
        actions=actions
    )
