import io
import pandas as pd
import requests


# @data_loader
def load_data_from_api(*args, **kwargs):
    months = (10, 11, 12)

    green_taxi_dtypes = {
        'VendorID': pd.Int64Dtype(),
        'store_and_fwd_flag': str,
        'RatecodeID': pd.Int64Dtype(),
        'PULocationID': pd.Int64Dtype(),
        'DOLocationID': pd.Int64Dtype(),
        'passenger_count': pd.Int64Dtype(),
        'trip_distance': float,
        'fare_amount': float,
        'extra': float,
        'mta_tax': float,
        'tip_amount': float,
        'tolls_amount': float,
        'ehail_fee': float,
        'improvement_surcharge': float,
        'total_amount': float,
        'payment_type': pd.Int64Dtype(),
        'trip_type': pd.Int64Dtype(),
        'congestion_surcharge': float,
    }

    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    data_frames = []

    for month in months:
        url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-{month}.csv.gz'
        df = pd.read_csv(url, sep=',', compression='gzip', dtype=green_taxi_dtypes,
                         parse_dates=parse_dates)
        print(f'Length is: {len(df.index)} - {url}')
        data_frames.append(df)

    df = pd.concat(data_frames, ignore_index=True)
    print(f'Count is: {len(df.index)}')

    return df


def transform(data):
    print("Rows with 0 passengers before transformation:", data['passenger_count'].isin([0]).sum())
    print("Rows with 0 trip distances before transformation:", data['trip_distance'].isin([0]).sum())
    data = data.query('passenger_count !=0 & trip_distance !=0')
    print(f'Count without 0 passengers and 0 trip distances is: {len(data.index)}')
    print("Column lpep_pickup_datetime before transformation: ")
    print(list(data.columns))
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    print("Converted column lpep_pickup_date after transformation: ")
    print(list(data.columns))
    print("Converted columns after transformation: ")
    data.columns = (data.columns
                    .str.replace('ID', '_id')
                    .str.lower())
    print(list(data.columns))
    print(data.head())

    return data


def test_output(output, *args) -> None:
    unique_vendor_ids = output.vendor_id.unique()
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with 0 passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are trips with 0 distance'
    assert 1 in unique_vendor_ids, 'vendor_id is one of the existing values in the column'
    assert 2 in unique_vendor_ids, 'vendor_id is one of the existing values in the column'


if __name__ == '__main__':
    dt = load_data_from_api()
    t = transform(dt)
    test_output(t)
