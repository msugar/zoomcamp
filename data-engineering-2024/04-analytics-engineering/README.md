 I've followed the recommended manual procedure to load the data into BigQuery for Week 04.
 
 - [Hack for loading data to BigQuery for Week 4](https://www.youtube.com/watch?v=Mork172sK_c&list=PLaNLNpjZpzwgneiI-Gl8df8GCsPYp_6Bs): step-by-step instructions. Watch the whole video, there are some additional steps at the end. 

 - [hack-load-data.sql](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/taxi_rides_ny/analyses/hack-load-data.sql): SQL to create, append, and alter the tables. Below is my version of it.

1. On Google Cloud, open BigQuery Studio. Make sure you have selected the right project, so you don't need to inform the project id in the SQL commands below.

2. In BigQuery, create a `trips_data_all` dataset in the US Multiregion.

3. Create the green_tripdata and yellow_tripdata tables with data from 2019:
    ```
    create table `trips_data_all.green_tripdata` as
    select * from `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2019`;

    create table `trips_data_all.yellow_tripdata` as
    select * from `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2019`;
    ```

4. Append the 2020 data:
    ```
    insert into `trips_data_all.green_tripdata`
    select * from `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2020`;

    insert into `trips_data_all.yellow_tripdata`
    select * from `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2020`;
    ```

5. Alter the tables to conform to the expected structure
    ```
    -- When you run the query, only run at most 5 of the ALTER TABLE statements at one time (by highlighting only 5 or less). 
    -- Otherwise BigQuery will say too many alterations to the table are being made.

    -- Fixes yellow table schema
    ALTER TABLE `trips_data_all.yellow_tripdata`
    RENAME COLUMN vendor_id TO VendorID;
    ALTER TABLE `trips_data_all.yellow_tripdata`
    RENAME COLUMN pickup_datetime TO tpep_pickup_datetime;
    ALTER TABLE `trips_data_all.yellow_tripdata`
    RENAME COLUMN dropoff_datetime TO tpep_dropoff_datetime;
    ALTER TABLE `trips_data_all.yellow_tripdata`
    RENAME COLUMN rate_code TO RatecodeID;
    ALTER TABLE `trips_data_all.yellow_tripdata`
    RENAME COLUMN imp_surcharge TO improvement_surcharge;
    ALTER TABLE `trips_data_all.yellow_tripdata`
    RENAME COLUMN pickup_location_id TO PULocationID;
    ALTER TABLE `trips_data_all.yellow_tripdata`
    RENAME COLUMN dropoff_location_id TO DOLocationID;

    -- Fixes green table schema
    ALTER TABLE `trips_data_all.green_tripdata`
    RENAME COLUMN vendor_id TO VendorID;
    ALTER TABLE `trips_data_all.green_tripdata`
    RENAME COLUMN pickup_datetime TO lpep_pickup_datetime;
    ALTER TABLE `trips_data_all.green_tripdata`
    RENAME COLUMN dropoff_datetime TO lpep_dropoff_datetime;
    ALTER TABLE `trips_data_all.green_tripdata`
    RENAME COLUMN rate_code TO RatecodeID;
    ALTER TABLE `trips_data_all.green_tripdata`
    RENAME COLUMN imp_surcharge TO improvement_surcharge;
    ALTER TABLE `trips_data_all.green_tripdata`
    RENAME COLUMN pickup_location_id TO PULocationID;
    ALTER TABLE `trips_data_all.green_tripdata`
    RENAME COLUMN dropoff_location_id TO DOLocationID;
    ```

6. Copy the [For-hire vehicles (FHV)](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv)files (CSV format, gnuzipped) to an ingestion GCS bucket

7. Using bq, create the `fhv_tripdata_all` table:  [fhv_tripdata.bq.sh](fhv_tripdata.bq.sh) 

8. Note the CSV files have this header:
```dispatching_base_num,pickup_datetime,dropOff_datetime,PUlocationID,DOlocationID,SR_Flag,Affiliated_base_number```

    But since we're using a table definition file, we can name the columns whatever we like to conform to the same naming used for the green and yellow tripdata tables.