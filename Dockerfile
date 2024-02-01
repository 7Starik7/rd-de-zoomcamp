FROM python:3.9
LABEL authors="roman_didyk"
WORKDIR /app
RUN pip install pandas pyarrow sqlalchemy psycopg2
RUN mkdir python datasets
COPY ../python/ingest_data.py src/ingest_data.py
COPY ../datasets/green_tripdata_2019-09.csv.gz datasets/green_tripdata_2019-09.csv.gz
COPY ../datasets/yellow_tripdata_2021-01.csv.gz datasets/yellow_tripdata_2021-01.csv.gz
COPY ../datasets/taxi_plus_zone_lookup.csv datasets/taxi_plus_zone_lookup.csv
RUN gunzip ./datasets/green_tripdata_2019-09.csv.gz
RUN gunzip ./datasets/yellow_tripdata_2021-01.csv.gz
ENTRYPOINT ["python", "src/ingest_data.py"]