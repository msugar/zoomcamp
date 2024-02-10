import pandas as pd


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import re

def rename_columns_to_snake_case(data):
    """
    Rename the columns of a DataFrame from CamelCase to snake_case.

    Parameters:
    - data (pandas DataFrame): The input DataFrame whose column names need to be converted.

    Returns:
    - col_names_changed (int): The count of columns that had their names changed from CamelCase to snake_case.
    """

    # Helper function to convert CamelCase to snake_case
    def camel_to_snake(name):
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    col_names_before = data.columns.tolist()
    data.columns = map(camel_to_snake, col_names_before)
    col_names_after = data.columns.tolist()
    col_names_changed = sum(x != y for x, y in zip(col_names_before, col_names_after))
    return col_names_changed


@transformer
def transform(data, *args, **kwargs):
    # Change column names from CamelCase to snake_case
    changed = rename_columns_to_snake_case(data)

    #data.info()

    print(data['lpep_pickup_datetime'].agg(['min', 'max']))
    print(data['lpep_dropoff_datetime'].agg(['min', 'max']))

    return data


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'