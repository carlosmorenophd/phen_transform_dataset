import pandas as pd

def calculate_avg(column_data) -> float:
    elements = list(
        filter(lambda i: not pd.isnull(i), column_data)
    )
    return sum(elements) / len(elements)