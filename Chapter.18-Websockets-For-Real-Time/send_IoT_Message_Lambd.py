#Don't forget to add both 'ExecuteAPI' and 'System' (AWS Systems Manger) permissions as inline policys for this Lambda function

import json
import boto3
Websocket_HTTPS_URL = "https://<Insert-Your-Websocket-Endpoint_Here>"
client = boto3.client("apigatewaymanagementapi", endpoint_url = Websocket_HTTPS_URL)
ssm_Client = boto3.client('ssm')


def lambda_handler(event, context):
    print(event) 
    response_ssm = ssm_Client.get_parameter(Name='<Insert-Your-SSM-Parameter-Name-Here>')
    print("my stored connection id: ", response_ssm['Parameter']['Value'] )
    connectionId =  response_ssm['Parameter']['Value']  #dig into the response blob to get our string cvalue
    Test_Message = json.dumps({ "message": "Hello from lambda, hardcoded test message"})
    IoT_Message = json.dumps(event)
    #AWS API Gateway API's require 'key=value' arguments
    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewaymanagementapi.html#ApiGatewayManagementApi.Client.post_to_connection
    response = client.post_to_connection(ConnectionId = connectionId, Data = IoT_Message)
