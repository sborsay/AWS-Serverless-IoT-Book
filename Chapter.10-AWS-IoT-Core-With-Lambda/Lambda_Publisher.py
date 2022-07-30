import json
import boto3

client = boto3.client('iot-data', region_name='<Your-AWS-Region-Here>')

def lambda_handler(event, context):
    #event['temperature'] = round(((event['temperature'] - 32) / 1.8))
    print(event)
    response = client.publish(
        topic='fromLambda',
        qos=0,
        payload=json.dumps(event) 
    )
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Published to topic')
    }

