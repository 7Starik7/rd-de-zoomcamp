{{
    config(
        materialized='table'
    )
}}

with trips_data as (
    select * from {{ ref('fact_fhv_trips') }}
)
select
    count (*) as fnv_trips_count
    from trips_data