const AWS = require('aws-sdk');

const docClient = new AWS.DynamoDB.DocumentClient({
    apiVersion: '2012-08-10',
    sslEnabled: false,
    paramValidation: false,
    convertResponseTypes: false
});

const tableName = '<YOUR-DDB-TABLE-HERE>’;

exports.handler = async (event, context, callback) => {
    let params = { TableName: tableName };

    let scanResults = [];
    let items;

    do {
        items = await docClient.scan(params).promise();
        items.Items.forEach((item) => scanResults.push(item));
        params.ExclusiveStartKey = items.LastEvaluatedKey;
    } while (typeof items.LastEvaluatedKey != "undefined");

    callback(null, scanResults);
};
