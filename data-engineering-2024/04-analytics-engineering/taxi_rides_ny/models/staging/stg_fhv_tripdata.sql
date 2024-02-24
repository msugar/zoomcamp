{{ config(materialized="view") }}

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(["dispatching_base_num", "lpep_pickup_datetime"]) }}
    as tripid,
    dispatching_base_num,
    {{ dbt.safe_cast("pulocationid", api.Column.translate_type("integer")) }}
    as pickup_locationid,
    {{ dbt.safe_cast("dolocationid", api.Column.translate_type("integer")) }}
    as dropoff_locationid,

    -- timestamps
    cast(lpep_pickup_datetime as timestamp) as pickup_datetime,
    cast(lpep_dropoff_datetime as timestamp) as dropoff_datetime,

    -- trip info
    sr_flag,
    affiliated_base_number,
from {{ source("staging", "fhv_tripdata") }}
where {{ dbt.date_trunc("YEAR", "lpep_pickup_datetime") }} = '2019-01-01'

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var("is_test_run", default=true) %} limit 100 {% endif %}
