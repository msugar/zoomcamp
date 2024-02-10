# Module 3 Homework Answers

## Data Warehouse

#### Preparation Procedure

1. Read and follow the instructions in [homework.md](homework.md)

1. Define the path to the Google Cloud Service Account Key JSON file, and the location of the tables used or created by the pipeline, in the Mage configuration file, `io_config.yaml`

1. Using Mage, run the included `green_taxi_etl_w03` pipeline, which has these blocks:

    * `extract_api_data`: Extract the 2022 Green Taxi Trip data from the files located on the Internet

    * `snake_case_cols_names`: Rename the columns to `snake_case` style, just in case

    * `upload_as_parquet_to_gcs`: Upload the data as a single Parquet file to Google Cloud Storage. For example: `gs://mage-zoomcamp-msugar/nyc_taxi_data_2022.parquet`

1. If the destination dataset doesn't exist yet in BigQuery, use the `bq` command to create it. For example:
    ```
    bq --location=northamerica-northeast1 mk \
       --dataset \
       ny_taxi_w03
    ```

1. Use th `bq` command to (re)create an *external* BigQuery table have as its source the uploaded file.

    If the target table already exists, delete it first:
    ```
    bq rm -f -t ny_taxi_w03.green_trips_2022_ext
    ```
    
    Now, generate a definition file for your Parquet data:
    ```
    bq mkdef \
       --source_format=PARQUET \
       "gs://mage-zoomcamp-msugar/nyc_taxi_data_2022.parquet" > def_file.json
    ```

    Then, use the generated definition file to create the external table:
    ```
    bq mk \
       --external_table_definition=def_file.json \
       ny_taxi_w03.green_trips_2022_ext
    ```

1. To (re)create a *native* BigQuery table out of the same uploaded file, run the following `bq` command:
    ```
    bq load \
       --replace \
       --source_format=PARQUET \
       ny_taxi_w03.green_trips_2022 \
       gs://mage-zoomcamp-msugar/nyc_taxi_data_2022.parquet
    ```

### Question 1:
What is count of records for the 2022 Green Taxi Data??

#### Procedure
* Run the `extract_api_data` block of the pipeline; see resulting dataframe's shape.

#### Answer
* 840,402

### Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.

What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

#### Procedure
One at a time, write (but do not execute!) each query in BigQuery Studio, and see what is the value in "This query will process ... when run" on the top right side of the editor.
```
SELECT COUNT(DISTINCT pulocation_id) 
FROM `dtc-de-course-411320.ny_taxi_w03.green_trips_2022_ext`
```
```
SELECT COUNT(DISTINCT pulocation_id) 
FROM `dtc-de-course-411320.ny_taxi_w03.green_trips_2022`
```

#### Answer
* 0 MB for the External Table and 6.41MB for the Materialized Table

### Question 3:
How many records have a fare_amount of 0?

#### Procedure
```
SELECT COUNT(1) 
FROM `dtc-de-course-411320.ny_taxi_w03.green_trips_2022_ext` x
WHERE x.fare_amount = 0
```

#### Answer
- 1,622

### Question 4:
What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)

#### Procedure
```
CREATE TABLE ny_taxi_w03.optimized_green_trips_2022
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY pulocation_id
AS SELECT * FROM `ny_taxi_w03.green_trips_2022_ext`
```

#### Answer
- Partition by lpep_pickup_datetime  Cluster on PUlocationID

### Question 5:
Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime
06/01/2022 and 06/30/2022 (inclusive).

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values?

Choose the answer which most closely matches.

#### Procedure
```
SELECT DISTINCT pulocation_id
FROM `ny_taxi_w03.green_trips_2022`
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30'
ORDER BY pulocation_id
```
```
SELECT DISTINCT pulocation_id
FROM `ny_taxi_w03.optimized_green_trips_2022`
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30'
ORDER BY pulocation_id
```

#### Answer
- 12.82 MB for non-partitioned table and 1.12 MB for the partitioned table

### Question 6: 
Where is the data stored in the External Table you created?

### Answer
- GCP Bucket

### Question 7:
It is best practice in Big Query to always cluster your data?

#### Answer:
- False

While clustering can be highly beneficial for certain types of queries, it is not a blanket requirement for all BigQuery tables. Decisions about whether to cluster should be made on a case-by-case basis, considering the specific query patterns and the trade-offs between load times and query costs.

### (Bonus: Not worth points) Question 8:
No Points: Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

#### Answer:

Zero bytes.

When you run a query in BigQuery, it estimates the number of bytes read based on the smallest possible unit of data that the query can operate on. In this case, since `COUNT(*)` does not require any actual data to be read from disk (it simply counts the number of rows), BigQuery estimates that it will read zero bytes. This is because `COUNT(*)` operates on metadata and does not need to scan the actual data.
