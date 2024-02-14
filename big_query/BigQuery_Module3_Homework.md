##### Question 1: 
What is count of records for the 2022 Green Taxi Data??

Answer: 840,402
```
SELECT COUNT(*) FROM rd-de-course.module3.green_tripdata_2022_non_partitoned;
```

##### Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

Answer: 0 MB for the External Table and 6.41MB for the Materialized Table
```
SELECT DISTINCT(PULocationID)
FROM rd-de-course.module3.external_green_taxi_trip_data_2022;

SELECT DISTINCT(PULocationID)
FROM rd-de-course.module3.green_tripdata_2022_partitoned;
```

##### Question 3:
How many records have a fare_amount of 0?

Answer: 1622
```
SELECT COUNT(*) FROM rd-de-course.module3.green_tripdata_2022_partitoned
WHERE fare_amount = 0;
```

##### Question 4:
What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID 
and filter based on lpep_pickup_datetime? (Create a new table with this strategy)

Answer: Partition by lpep_pickup_datetime Cluster on PUlocationID

(OR Partition by lpep_pickup_datetime and Partition by PUlocationID)
```
CREATE OR REPLACE TABLE rd-de-course.module3.green_tripdata_2022_answer4
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID 
AS
SELECT * FROM rd-de-course.module3.external_green_taxi_trip_data_2022;
```

##### Question 5:
Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)
Use the materialized table you created earlier in your from clause and note the estimated bytes. 
Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values?

Answer: 12.82 MB for non-partitioned table and 1.12 MB for the partitioned table
```
SELECT DISTINCT(PULocationID)
FROM rd-de-course.module3.green_tripdata_2022_non_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

SELECT DISTINCT(PULocationID)
FROM rd-de-course.module3.green_tripdata_2022_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';
```

##### Question 6:
Where is the data stored in the External Table you created?

Answer: GCP Bucket


##### Question 7:
It is best practice in Big Query to always cluster your data:

Answer: True

##### (Bonus: Not worth points) Question 8:
No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

Answer: 0
```
SELECT COUNT(*)
FROM rd-de-course.module3.green_tripdata_2022_non_partitoned;
```