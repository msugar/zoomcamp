import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Load Green NYC Taxy data from last quarter of 2022
    """
    whole_df = pd.DataFrame()
    year = 2022
    for month in range(1,13):
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year:d}-{month:02d}.parquet"
        chunk_df = pd.read_parquet(url)
        chunk_rows_count = len(chunk_df)
        print(f"Loaded {url} with {chunk_rows_count} rows.")
        whole_df = pd.concat([whole_df, chunk_df], ignore_index=True)

    return whole_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert output.empty is False, 'The output is empty'