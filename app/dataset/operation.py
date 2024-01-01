from dataset.transform import (
    Transform,
    TransformEnum,
    transform_N_T_S_M_V,
    transform_E_N_L,
    transform_Y_N,
    transform_Y_N_U,
    transform_N_S_W_E,
)
from dataset.normalize import Normalize, NormalizeEnum
from dataset.util import calculate_avg
from dataset.valid.row import RowValid, RowValidEnum
import pandas as pd


class TransformNormalize:
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
        for remove_row in self.remove_rows:
            enum = remove_row.valid
            column = remove_row.column
            if enum == RowValidEnum.VALUE_OR_REMOVE:
                self.csv = self.csv.dropna(subset=[column])

    def transform(self) -> None:
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
            elif enum == TransformEnum.COORDINATE_DECIMAL:
                degree = action.transform.column_coordinate_degree
                minute = action.transform.column_coordinate_minute
                n_s_e_w = action.transform.column_coordinate_NSEW
                self.csv_process[column] = (self.csv[degree] + 1/60 * (self.csv[minute]) * self.csv[n_s_e_w].apply(transform_N_S_W_E) )

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
            new_name = "origin_{0}".format(self.save_file)
            if path.exists(new_name):
                remove(new_name)
            self.csv.to_csv(new_name, index=is_index)
