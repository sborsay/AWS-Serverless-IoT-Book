import json
import boto3
from botocore.config import Config

config = Config(region_name = '<Your-Region>')
config.endpoint_discovery_enabled = True
timestream_query_client = boto3.client('timestream-query', config=config)

def lambda_handler(event, context):
    result = timestream_query_client.query(
        QueryString= 'SELECT * FROM "<YOUR-TIMESTREAM-DATABASE>"."<YOUR-TABLE-NAME>"'
    )

    print(result['ColumnInfo'])
    print(result['Rows'])
    print(result)
    return(result)
