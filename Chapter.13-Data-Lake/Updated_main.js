var timestamps = new Array();
var humidity = new Array();
var temperature = new Array();

// Start by extracting folder/ url from s3 bucket
$.ajax({
    type     : "GET",
    url      : "https://<Your-S3-Bucket_Name>.s3.amazonaws.com/", 
    dataType : "xml",
    success  : function(xmlData){
        var url = "";
        keys = xmlData.getElementsByTagName("Key");
        for(i=0; i < keys.length; i++) {
            url = keys[i].childNodes[0].nodeValue
            url = url.trim()

            pos = url.search("republish/");
            if(pos > -1) {
           // Detect folder/partition with json file
              if(url.replace("republish/", "") != "")//Your key folder name
                  parseJson(url)
           }
            
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
        url : "https://<Your-S3-Bucket_Name>.s3.amazonaws.com/" + url,
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
