from dataset.operation import TransformNormalize
from dataset.valid.row import RowValid


class TransformDataset:

    def __init__(
        self,
        source_file_name: str,
        destiny_file_name: str,
        actions: list[TransformNormalize],
        remove_rows: list[RowValid]
    ) -> None:
        self.source_file_name = source_file_name
        self.destiny_file_name = destiny_file_name
        self.actions = actions
        self.remove_rows = remove_rows
