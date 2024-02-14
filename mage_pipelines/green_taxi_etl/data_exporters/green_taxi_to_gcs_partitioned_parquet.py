import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(data, **kwargs) -> None:

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/rd-de-course-b17a4b91ac46-mage.json"
    bucket_name = 'mage-zoomcamp-rd-1'
    project_id = 'rd-de-course'

    table_name = "nyc_green_taxi_data"

    root_path = f'{bucket_name}/{table_name}'
    
    

    # data['lpep_pickup_date'] = data['tpep_pickup_datetime'].dt.date

    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
    )
