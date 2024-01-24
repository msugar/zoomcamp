#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine, types
from sqlalchemy.types import *

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    action_if_table_already_exists = params.if_table_exists
    datetime_fields = params.datetime_fields
    
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    total_row_count = 0
    chunk_num = 0
    for df_chunk in pd.read_csv(csv_name, iterator=True, chunksize=100000):
        chunk_num += 1
        for field in datetime_fields:
            df_chunk[field] = pd.to_datetime(df_chunk[field])
        if chunk_num == 1:
            df_chunk.info()
            df_chunk.head(n=0).to_sql(name=table_name, con=engine, if_exists=action_if_table_already_exists, index=False)
        chunk_row_count = len(df_chunk) 
        total_row_count += chunk_row_count
        t_start = time()
        df_chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        t_end = time()
        print(f'Inserted chunk # {chunk_num} with {chunk_row_count} rows, took {t_end - t_start:.3f} seconds')
    else:
        if chunk_num > 0:
            print(f"Finished ingesting data into the postgres database, {total_row_count} rows inserted.")
        else:
            print("Found no data to ingest")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')
    parser.add_argument('--if_table_exists', required=False, default='replace', choices=['append', 'replace'])
    parser.add_argument('--datetime_fields', required=False, default=[], nargs='*', help='fields that should be converted to datetime')

    args = parser.parse_args()

    main(args)
