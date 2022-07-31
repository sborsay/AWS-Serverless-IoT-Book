
var timestamps = new Array();
var humidity = new Array();
var temperature = new Array();

// Start by extracting folder/ url from s3 bucket
$.ajax({
    type     : "GET",
    url      : "https://<Your-S3-Bucket-Name>.s3.us-east-1.amazonaws.com/", 
    dataType : "xml",
    success  : function(xmlData){
        var url = "";
        keys = xmlData.getElementsByTagName("Key");
        for(i=0; i < keys.length; i++) {
            url = keys[i].childNodes[0].nodeValue
            url = url.trim()+"+"

            /*May not be needed as of 8/1/2022
             Find your locate folder string */
            
           // pos = url.search("iot/test/");
           //  if(pos > -1) {
           // Detect folder/partition with json file
           //   if(url.replace("iot/test/", "") != "")
           //       parseJson(url)
           //}
            
        }

        loadChart(temperature, humidity, timestamps)
    },
    error    : function(){
         alert("Could not retrieve XML file.");
    }
});


var parseJson = function(url) { 
    $.ajax({
        
        type : "GET",
        url : "https://<Your-S3-Bucket-Name>.s3.us-east-1.amazonaws.com/" + url,
        dataType : "json",
        success : function(jsonFile) {
            timestamps.push(jsonFile.timestamps);
            temperature.push(jsonFile.temperature)
            humidity.push(jsonFile.humidity)
        },
        error : function(xhr, status, error) {
            console.error("JSON error: " + status);
        }
    })
}
