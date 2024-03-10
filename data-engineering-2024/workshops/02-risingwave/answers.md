# Workshop 2 - RisingWave - Homework Answers

## Setup
1. Start with [rising-wave.md](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/workshops/rising-wave.md) for the Workshop Videos and general guidance.
1. Follow the instructions found in [readme-ov-file#getting-started](https://github.com/risingwavelabs/risingwave-data-talks-workshop-2024-03-04?tab=readme-ov-file#getting-started) to set up your environment. 
1. If you are following the Workshop, find further instructions in [homework.md#setting-up](https://github.com/risingwavelabs/risingwave-data-talks-workshop-2024-03-04/blob/main/homework.md#setting-up).
1. Go back to [rising-wave.md#homework](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/workshops/rising-wave.md#homework) for the Homework Questions. 

## Question 1
- psql (risingwave):
    ```
    create materialized view taxi_trips_q01 as 
    select
        tz1.zone as pickup_zone,
        tz2.zone as dropoff_zone,
        avg(td.tpep_dropoff_datetime - td.tpep_pickup_datetime) as avg_trip_time,
        min(td.tpep_dropoff_datetime - td.tpep_pickup_datetime) as min_trip_time,
        max(td.tpep_dropoff_datetime - td.tpep_pickup_datetime) as max_trip_time 
    from
        trip_data td 
        join
            taxi_zone tz1 
            on td.pulocationid = tz1.location_id 
        join
            taxi_zone tz2 
            on td.dolocationid = tz2.location_id 
    group by
        tz1.zone,
        tz2.zone;
    ```
    ```   
    select
        pickup_zone,
        dropoff_zone,
        avg_trip_time 
    from
        taxi_trips_q01
    order by
        avg_trip_time desc limit 1;
    ```
- Results:
    ```
      pickup_zone   | dropoff_zone | avg_trip_time
    ----------------+--------------+---------------
     Yorkville East | Steinway     | 23:59:33
    (1 row)
    ```
- Answer is *Yorkville East, Steinway*.

## Question 2
- psql (risingwave):
    ```
    create materialized view taxi_trips_q02 as 
    select
        tz1.zone as pickup_zone,
        tz2.zone as dropoff_zone,
        count(*) as number_trips,
        avg(td.tpep_dropoff_datetime - td.tpep_pickup_datetime) as avg_trip_time,
        min(td.tpep_dropoff_datetime - td.tpep_pickup_datetime) as min_trip_time,
        max(td.tpep_dropoff_datetime - td.tpep_pickup_datetime) as max_trip_time 
    from
        trip_data td 
        join
            taxi_zone tz1 
            on td.pulocationid = tz1.location_id 
        join
            taxi_zone tz2 
            on td.dolocationid = tz2.location_id 
    group by
        tz1.zone,
        tz2.zone;
    ```
    ```
    select
        number_trips,
        pickup_zone,
        dropoff_zone 
    from
        taxi_trips_q02 
    order by
        avg_trip_time desc limit 1;        
    ```
- Results:
    ```
     number_trips |  pickup_zone   | dropoff_zone
    --------------+----------------+--------------
                1 | Yorkville East | Steinway
    (1 row)
    ```
- Answer is *1*.

## Question 3
- psql (risingwave):
    ```
    select
        tz.zone as pickup_zone,
        count(*) as number_trips 
    from
        trip_data td 
        join
            taxi_zone tz 
            on td.pulocationid = tz.location_id 
    where
        td.tpep_pickup_datetime between
        (
            select
                max(tpep_pickup_datetime) - interval '17 hours' 
            from
                trip_data
        )
        and
        (
            select
                max(tpep_pickup_datetime) 
            from
                trip_data
        )
    group by
        pickup_zone 
    order by
        number_trips desc limit 3;
    ```
- Results:
    ```
         pickup_zone     | number_trips
    ---------------------+--------------
     LaGuardia Airport   |           19
     Lincoln Square East |           17
     JFK Airport         |           17
    (3 rows)    
    ```
- Answer is *LaGuardia Airport, Lincoln Square East, JFK Airport*.
