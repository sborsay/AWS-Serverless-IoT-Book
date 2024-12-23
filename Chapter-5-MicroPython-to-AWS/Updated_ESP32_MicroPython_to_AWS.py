#AWS MQTT client example for esp32, this sketch is a combination of various sources:
#https://awsiot.wordpress.com/2019/01/10/connect-8266-to-aws-mqtt-using-miropython/
#https://github.com/digidotcom/xbee-micropython/blob/master/samples/cellular/aws/
#https://forum.micropython.org/viewtopic.php?t=5166
#Original code added by Stephen Borsay for Udemy Course
#Rename this as "main.py"

from umqtt.robust import MQTTClient
import ssl # new update for firmware starting 6/24
import time
import random
import machine
pin = machine.Pin(2)  #blinking is optional, check your LED pin

#Place these two certs at same folder level as your MicroPython program

CERT_FILE = "/certificate.pem.crt"  #the ".crt" may be hidden that’s ok
KEY_FILE = "/private.pem.key"

MQTT_CLIENT_ID = "myUniqueName7856"
MQTT_PORT = 8883 #MQTT secured

PUB_TOPIC = "iot/outTopic" #coming out of device
SUB_TOPIC = "iot/inTopic"  #coming into device

#Change the following three settings to match your environment
#IoT Core-->Settings or > aws iot describe-endpoint --endpoint-type iot:Data-ATS
MQTT_HOST = "<Your-ATS-IoT-AWS-Endpoint>"  #From the AWS CLI enter:  aws iot describe-endpoint --endpoint-type iot:data-ats
WIFI_SSID = "<MY-WIFI-NETWORK-NAME>"
WIFI_PW = "<MY-WIFI-PASSWORD>"

MQTT_CLIENT = None

print("starting program")

def network_connect():
    print("starting connection method")
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID , WIFI_PW)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


    
def pub_msg(msg):  #publish is synchronous so we poll and publish
    global MQTT_CLIENT
    try:    
        MQTT_CLIENT.publish(PUB_TOPIC, msg)
        print("Sent: " + msg)
    except Exception as e:
        print("Exception publish: " + str(e))
        raise

def sub_cb(topic, msg):
    print('Device received a Message: ')
    print((topic, msg))  #print incoming message, waits for loop below
    pin.value(0)         #blink if incoming message by toggle off

def device_connect():    
    global MQTT_CLIENT

    try:  #all this below runs once, equivalent to Arduino's "setup" function)
        with open(KEY_FILE, "r") as f: 
            key = f.read()
        print("Got Key")
       
        with open(CERT_FILE, "r") as f: 
            cert = f.read()
        print("Got Cert")
        
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.load_cert_chain(CERT_FILE, keyfile=KEY_FILE)

        #MQTT_CLIENT = MQTTClient(client_id=MQTT_CLIENT_ID, server=MQTT_HOST, port=MQTT_PORT, keepalive=5000, ssl=True, ssl_params={"cert":cert, "key":key, "server_side":False})
        MQTT_CLIENT = MQTTClient(client_id=MQTT_CLIENT_ID, server=MQTT_HOST, port=MQTT_PORT, keepalive=5000, ssl=ssl_context)
        MQTT_CLIENT.connect()
        print('MQTT Connected')
        MQTT_CLIENT.set_callback(sub_cb)
        MQTT_CLIENT.subscribe(SUB_TOPIC)
        print('Subscribed to %s as the incoming topic' % (SUB_TOPIC))
        return MQTT_CLIENT
    except Exception as e:
        print('Cannot connect MQTT: ' + str(e))
        raise


#start execution
try:
    print("Connecting WIFI")
    network_connect()
    print("Connecting MQTT")
    device_connect()
    while True: #loop forever
            pin.value(1)
            pending_message = MQTT_CLIENT.check_msg()  # check for new subscription payload incoming
            if pending_message != 'None':  #check if we have a message 
                temp =  random.randint(0, 130)
                humid = random.randint(0, 100)
                deviceTime = time.time()
                print("Publishing")
                pub_msg("{\n  \"temperature\": %d,\n  \"humidity\": %d,\n \"timestamps\": %d\n}"%(temp,humid,deviceTime))      
                print("published payload")
                time.sleep(5)  #A 5 second delay between publishing, adjust as you like
            
except Exception as e:
    print(str(e))
