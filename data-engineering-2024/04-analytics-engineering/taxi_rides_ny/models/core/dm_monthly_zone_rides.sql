{{ config(materialized="table") }}

with
    trips_unioned as (
        select 
            tripid, service_type, 
            pickup_borough, pickup_zone, -- pickup_locationid, 
            --dropoff_locationid, dropoff_borough, dropoff_zone,
            --pickup_datetime, dropoff_datetime,
            {{ dbt.date_trunc("month", "pickup_datetime") }} as ride_month
        from {{ ref("fact_trips") }}
        union all
        select 
            tripid, service_type, 
            pickup_borough, pickup_zone, -- pickup_locationid, 
            --dropoff_locationid, dropoff_borough, dropoff_zone,
            --pickup_datetime, dropoff_datetime,
            {{ dbt.date_trunc("month", "pickup_datetime") }} as ride_month
        from {{ ref("fact_fhv") }}
    )
select
    -- Rides grouping 
    service_type,
    pickup_borough, pickup_zone,
    ride_month,
    
    -- Rides calculation
    count(tripid) as trips

from trips_unioned
group by 1, 2, 3, 4
