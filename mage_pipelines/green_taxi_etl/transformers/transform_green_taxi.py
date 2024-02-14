if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    data = data.query('passenger_count !=0 & trip_distance !=0')
    print(f'Count without 0 passengers and 0 trip distances is: {len(data.index)}')

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    data.columns = (data.columns
                    .str.replace('ID', '_id')
                    .str.lower())
    
    print("Converted columns after transformation: ")
    print(list(data.columns))

    return data

@test
def test_output(output, *args) -> None:
    unique_vendor_ids = output.vendor_id.unique()
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with 0 passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are trips with 0 distance'
    assert 1 in unique_vendor_ids, 'vendor_id is one of the existing values in the column'
    assert 2 in unique_vendor_ids, 'vendor_id is one of the existing values in the column'
