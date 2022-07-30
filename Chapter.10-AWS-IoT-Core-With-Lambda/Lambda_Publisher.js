var AWS = require('aws-sdk');
var iotdata = new AWS.IotData({endpoint: '<YOUR-AWS-IOT-ENDPOINT-HERE>' });

exports.handler = (event) => {
    //event['temperature'] = round(((event['temperature'] - 32) / 1.8))
    console.log("The event object is: " + JSON.stringify(event));
    var params = {
        topic: "fromLambda", 
        payload: JSON.stringify(event), //event.Temperature
        qos: 0
    };

    return iotdata.publish(params, function(err, data) {
        if (err) {
            console.log("If error: " + JSON.stringify(err));
        }
        else {
            console.log("Success");
        }
    })
};

