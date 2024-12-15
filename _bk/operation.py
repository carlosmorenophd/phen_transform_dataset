"""Operation on"""
import re
from os import path, remove

import pandas as pd

from normalize.process import Normalize, NormalizeActionEnum
from src.transforms.valid.row import RowValid, RowValidEnum
from src.transforms.transform import (
    Transform,
    TransformEnum,
    transform_N_T_S_M_V,
    transform_E_N_L,
    transform_Y_N,
    transform_Y_N_U,
    transform_N_S_W_E,
)


class TransformNormalize:
    """Techniques of normalize"""

    def __init__(
            self,
            column: str,
            transform: Transform,
            normalize: Normalize
    ) -> None:
        self.column = column
        self.transform = transform
        self.normalize = normalize


class Preprocessing ():
    """Preprocessing functions"""

    def __init__(
        self,
        save_file: str,
        name_file: str,
        actions: list[TransformNormalize],
        remove_rows: list[RowValid]
    ) -> None:
        self.save_file = save_file
        self.actions = actions
        self.csv = pd.read_csv(name_file)
        self.csv_process = pd.DataFrame()
        self.remove_rows = remove_rows

    def validate_rows(self) -> None:
        """Validate Rows"""
        for remove_row in self.remove_rows:
            enum = remove_row.valid
            column = remove_row.column
            if enum == RowValidEnum.VALUE_OR_REMOVE:
                self.csv = self.csv.dropna(subset=[column])

    def transform(self) -> None:
        """ Apply the all transformation on actions
        """
        for action in self.actions:
            enum = action.transform.transform_enum
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
            elif enum == TransformEnum.COORDINATE_DECIMAL:
                degree = action.transform.column_coordinate_degree
                minute = action.transform.column_coordinate_minute
                n_s_e_w = action.transform.column_coordinate_nswe
                self.csv_process[column] = (
                    (self.csv[degree] + 1/60 * (self.csv[minute])) * self.csv[n_s_e_w].apply(transform_N_S_W_E))
            elif enum == TransformEnum.COORDINATE_DECIMAL_LIMIT_180:
                degree = action.transform.column_coordinate_degree
                minute = action.transform.column_coordinate_minute
                n_s_e_w = action.transform.column_coordinate_nswe
                self.csv_process[column] = (
                    self.csv[degree] + 1/60 * (self.csv[minute]) * self.csv[n_s_e_w].apply(transform_N_S_W_E))
                self.csv_process[column] = self.csv_process[column].apply(
                    lambda x: 180 if x > 180 else x)
                self.csv_process[column] = self.csv_process[column].apply(
                    lambda x: -180 if x < -180 else x)

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

    def normalize(self) -> None:
        """ Normalize the data set
        """
        for action in self.actions:
            enum = action.normalize.normalize_enum
            column = action.column
            if enum == NormalizeActionEnum.PASS:
                self.csv_process[column] = self.csv_process[column]
            elif enum == NormalizeActionEnum.ONE_POSITIVE:
                max = self.csv_process[column].max()
                min = self.csv_process[column].min()
                self.csv_process[column] = self.csv_process[column].map(
                    lambda item: ((item - min) / (max - min)))
            elif enum == NormalizeActionEnum.ONE_TO_ONE:
                max = self.csv_process[column].max()
                min = self.csv_process[column].min()
                self.csv_process[column] = self.csv_process[column].map(
                    lambda item: (
                        (2 * ((item - min) / (max - min))) - 1
                    )
                )

    def save(self, is_save_origin: bool = False, is_index: bool = False):
        """Save results"""
        if path.exists(self.save_file):
            remove(self.save_file)
        self.csv_process.to_csv(self.save_file, index=is_index)
        if is_save_origin:
            new_name = f"origin_{self.save_file}"
            if path.exists(new_name):
                remove(new_name)
            self.csv.to_csv(new_name, index=is_index)


def calculate_avg(column_data) -> float:
    """Calculate avg"""
    elements = list(
        filter(lambda i: not pd.isnull(i), column_data)
    )
    return sum(elements) / len(elements)
