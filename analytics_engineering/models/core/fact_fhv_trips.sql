{{
    config(
        materialized='table'
    )
}}

with fnv_taxi_tripdata as (
    select *,
    'fnv' as service_type
    from {{ref('stg_fnv_taxi_tripdata')}}
),

dim_zones as (
select *
from {{ref('dim_zones')}}
where borough != 'Unknown'
)

select 
    fnv_taxi_tripdata.dispatching_base_num,
    fnv_taxi_tripdata.pickup_datetime,
    fnv_taxi_tripdata.dropoff_datetime,
    fnv_taxi_tripdata.pulocationid,
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone, 
    fnv_taxi_tripdata.dolocationid,
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,  
    fnv_taxi_tripdata.sr_flag,
    fnv_taxi_tripdata.affiliated_base_number
from fnv_taxi_tripdata
inner join dim_zones as pickup_zone
on fnv_taxi_tripdata.pulocationid=pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fnv_taxi_tripdata.dolocationid=dropoff_zone.locationid

