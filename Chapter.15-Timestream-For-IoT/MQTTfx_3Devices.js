//MQTT.fx switch fountain test, modified by Stephen Borsay

var Thread = Java.type("java.lang.Thread");

var topic = "iot/mqttfx";
var waitTime = 2000;
var iterations = 10;

deviceArray = [ 'ESP32_Alpha1', 'ESP32_Bravo2', 'ESP32_Charlie3' ]; //try ennumerated array with Arduino

function execute(action) {
    out("Test Script: " + action.getName());
    for (var i = 0; i < iterations; i++) {
        sendPayload();
        Thread.sleep(waitTime);
    }
    action.setExitCode(0);
    action.setResultText("done.");
    out("Test Script: Done");
    return action;
}

function sendPayload() {
  
  var temp = Math.round(Math.random()*130);
  var humid = Math.round(Math.random()*100);
  var ts = Date.now();
  
  var IoT_Payload = {
      "device_ID"    : deviceArray[Math.floor(Math.random() * 3)], 
      "temperature" :  temp, 
      "humidity"    :  humid
    }

var payload = JSON.stringify(IoT_Payload)

  mqttManager.publish(topic, payload);
  out("Topic is:  \n" + topic);
  out("payload sent \n" + payload);
}

function out(message){
     output.print(message);
}
