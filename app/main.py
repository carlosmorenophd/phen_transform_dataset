import pandas as pd
from enum import Enum


class Convert:
    def __init__(self, name: str, action) -> None:
        self.name = name
        self.action = action


class ActionToFill(Enum):
    AVG = 1
    NONE_FILL = 2

def find(name: str, actions) -> Convert :
    return list(filter(lambda item: item.name == name, actions))

def doRun(name_file: str, actions):
    csv_data = pd.read_csv(name_file)
    for column in csv_data.columns:
        filtered = find(name=column, actions=actions)
        if len(filtered) == 1:
            print(filtered[0].name)
            data = csv_data.loc[:,column]
            print(data)
            data2 = list(filter(lambda i: not pd.isnull(i), data))
            print(data2)
            print(sum(filter(lambda i: isinstance(i, float), data)))
            # TODO:  remplace all null with avg


if __name__ == "__main__":
    actions = []
    actions.append(
        Convert(name='AREA_HARVESTED_BED_PLOT_M2:(m2)', action=ActionToFill.AVG))
    actions.append(
        Convert(name='AREA_SOWN_BED_PLOT_M2:(m2)', action=ActionToFill.AVG))
    doRun(name_file='/Users/yeiden/repo/test_py/origin_test.csv', actions=actions)
