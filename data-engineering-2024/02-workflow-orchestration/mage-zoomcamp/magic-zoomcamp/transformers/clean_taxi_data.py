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
    #data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    #data['lpep_dropoff_date'] = data['lpep_dropoff_datetime'].dt.date

    # Drop rows with zeros or nulls in passenger_count and trip_distance columns
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0.0)]

    print("Unique values of VendorID:", data['VendorID'].unique().tolist())

    # Change column names from CamelCase to snake_case
    changed = rename_columns_to_snake_case(data)
    print(f"Number of columns whose name changed from CamelCase to snake_case: {changed}")

    return data


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert (output['passenger_count'] == 0).sum() == 0, 'There are rows with zero passenger'
    assert (output['passenger_count'].isnull()).sum() == 0, 'There are rows with null passenger'
    assert (output['trip_distance'] == 0).sum() == 0, 'There are rows with zero trip distance'
    assert (output['trip_distance'].isnull()).sum() == 0, 'There are rows with null trip distance'
    