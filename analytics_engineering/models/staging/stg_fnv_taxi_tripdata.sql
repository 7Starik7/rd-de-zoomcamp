{{
    config(
        materialized='view'
    )
}}

with 

tripdata as (

    select * from {{ source('staging', 'fnv_taxi_tripdata') }}
)
    select
        dispatching_base_num,
        pickup_datetime,
        dropoff_datetime,
        pulocationid,
        dolocationid,
        sr_flag,
        affiliated_base_number
    from tripdata
    where 
    pulocationid is not null
    and cast(pickup_datetime as date) between '2019-01-01' and '2019-12-31'

-- dbt build --select <model.sql> --vars '{'is_test_run: false}'
{% if var('is_test_run', default=false) %}

  limit 100

{% endif %}
