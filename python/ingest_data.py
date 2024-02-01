import argparse
import pandas as pd
from time import time
from sqlalchemy import create_engine


def choose_table_type(source_dataset, iterator):
    # Convert some columns to valid datatypes
    if "yellow_tripdata" in source_dataset:
        iterator.tpep_pickup_datetime = pd.to_datetime(iterator.tpep_pickup_datetime)
        iterator.tpep_dropoff_datetime = pd.to_datetime(iterator.tpep_dropoff_datetime)
    elif "green_tripdata" in source_dataset:
        iterator.lpep_pickup_datetime = pd.to_datetime(iterator.lpep_pickup_datetime)
        iterator.lpep_dropoff_datetime = pd.to_datetime(iterator.lpep_dropoff_datetime)
    elif "zone_lookup" in source_dataset:
        return
    else:
        print(f"Incorrect source dataset - {source_dataset}")


def upload_to_db(source_dataset, destination_table, chunk_size, db_engine):
    print(f"The data ingestion from {source_dataset} has been initiated!")
    ingestedAmount = 0
    # Read from csv
    df_iter = pd.read_csv(source_dataset, iterator=True, chunksize=chunk_size, low_memory=False)
    # Create iterator
    df = next(df_iter)
    # Create schema / ingest first chunk
    df.head(n=0).to_sql(name=destination_table, con=db_engine, if_exists='replace')
    choose_table_type(source_dataset, df)
    df.to_sql(name=destination_table, con=db_engine, if_exists='append')
    while True:
        try:
            t_start = time()
            df = next(df_iter)
            choose_table_type(source_dataset, df)
            df.to_sql(name=destination_table, con=db_engine, if_exists='append')
            t_end = time()
            print("inserted another chunk..., took %.3f seconds" % (t_end - t_start))
            ingestedAmount = ingestedAmount + chunk_size
            print(f"ingested amount of rows:  {ingestedAmount}")
        except StopIteration:
            amount = pd.read_sql("SELECT COUNT(*) FROM " + destination_table, db_engine)
            print(f"The data ingestion from {source_dataset} into the postgres {destination_table} "
                  f"table has been completed successfully!")
            print(f"Count of ingested rows: {amount['count'].loc[amount.index[0]]}")
            break


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # Connect to Postgresql DB
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    upload_to_db(f'{url}', f'{table_name}', 100000, engine)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')
    args = parser.parse_args()
    main(args)
