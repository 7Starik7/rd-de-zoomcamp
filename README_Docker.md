##### Build docker container with ingest_data.py
```
docker build -t taxi_ingest:v001 .
```
##### Run ingest_data.py in docker - taxi_plus_zone_lookup.csv
```
docker run -it \
--network=pg-network \
taxi_ingest:v001 \
--user=root \
--password=root \
--host=pg-database \
--port=5432 \
--db=ny_taxi \
--table_name=taxi_zone_lookup \
--url=./datasets/taxi_plus_zone_lookup.csv
```
##### Run ingest_data.py in docker - green_tripdata_2019-09.csv
```
docker run -it \
--network=pg-network \
taxi_ingest:v001 \
--user=root \
--password=root \
--host=pg-database \
--port=5432 \
--db=ny_taxi \
--table_name=green_taxi_data \
--url=./datasets/green_tripdata_2019-09.csv
```
##### Run ingest_data.py in docker - yellow_tripdata_2021-01.csv
```
docker run -it \
--network=pg-network \
taxi_ingest:v001 \
--user=root \
--password=root \
--host=pg-database \
--port=5432 \
--db=ny_taxi \
--table_name=yellow_taxi_data \
--url=./datasets/yellow_tripdata_2021-01.csv
```