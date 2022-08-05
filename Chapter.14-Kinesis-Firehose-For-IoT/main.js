var timestamps = [];
var humidity = [];
var temperature = [];

// Start by extracting thesubfolder/ url from s3 bucket
$.ajax({
    type     : "GET",
    url      : "https://<Your-S3-Bucket-Name-Here>/",
    dataType : "xml",
    success  : function(xmlData, values){
        var url = "";
        var values = {};
        keys = xmlData.getElementsByTagName("Key");
        for(i=0; i < keys.length; i++) {
            url = keys[i].childNodes[0].nodeValue;
            parseText(url, function(getValues) {
                loadLineChart(timestamps,temperature,humidity);
                loadBarChart(timestamps,temperature,humidity);
            })
        }

    },
    error    : function(){
         alert("Could not retrieve XML file.");
    }
})

// Parse file as text
var parseText = function(url, getValues) {
    var values ={ "timestamps":"", "temperature":"", "humidity":"" };
    $.ajax({
        type     : "GET",
        url      : "https://<Your-S3-Bucket-Name-Here>/"" + url,
        dataType : "text",
        success  : function(txtFile){
            var jsonArray;
            // Convert text file to JSON Array
            jsonArray = parseToJSONArray(txtFile)
            // Get Values from JSONArray
            jsonArray.forEach(getValuesFromJSON)
            
            values.timestamps = timestamps
            values.temperature = temperature
            values.humidity = humidity
            getValues(values)
        },
        error    : function(xhr, status, error){
             alert(status + ' ' + error);
        }
    });
}


// Get timestamps, temperature and humidity from json
var getValuesFromJSON = function(json, index, JSONArray) {
    json = JSON.parse(json)
    timestamps.push(json.timestamps);
    temperature.push(json.temperature)
    humidity.push(json.humidity)
}

// This function converts the text file from server to a JSON Array
var parseToJSONArray = function(txtFile) {
    var json = [];
    var temp = "";
    var i = 0
    while(i < txtFile.length) {
        // console.log(txtFile[i])
        if(txtFile[i] != " ") {
            temp += txtFile[i]
            if(txtFile[i] == "}") {
                i = i+1
                json.push(temp)
                temp = ""
            }
        }
        i+=1
    }
    return json;
}
