import os
import requests
import pandas as pd
from google.cloud import storage

# services = ['fhv','green','yellow']
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'

# switch out the bucketname
BUCKET = os.environ.get("GCP_GCS_BUCKET", "all-nyc-taxi-data")


def upload_to_gcs(bucket, object_name, file_name):
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(file_name)


def web_to_gcs(year, service):
    for i in range(12):
        file_path = "../analytics_engineering_all_nyc_taxi_data/"
        month = '0' + str(i + 1)
        month = month[-2:]

        # csv file_name
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"

        # download it using requests via a pandas df
        request_url = f"{init_url}{service}/{file_name}"
        r = requests.get(request_url)
        open(f"{file_path}{file_name}", 'wb').write(r.content)
        print(f"Local: {file_path}{file_name}")

        # read it back into a parquet file
        df = pd.read_csv(f"{file_path}{file_name}", compression='gzip', low_memory=False)
        file_path_name = f"{file_path}{file_name}".replace('.csv.gz', '.parquet')
        df.to_parquet(file_path_name, engine='pyarrow')
        print(f"Parquet: {file_path_name}")

        # # upload it to gcs
        upload_to_gcs(BUCKET, f"{service}/{file_name}", file_path_name)
        print(f"GCS: {service}/{file_name}")


# web_to_gcs("2019", "fhv")
# web_to_gcs("2019", "green")
# web_to_gcs('2020', 'green')
# web_to_gcs("2019", "yellow")
# web_to_gcs('2020', 'yellow')
