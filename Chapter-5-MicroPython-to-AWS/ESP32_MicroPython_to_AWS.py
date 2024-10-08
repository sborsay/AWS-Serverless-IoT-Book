#AWS MQTT client example for esp32

from umqtt.robust import MQTTClient
import time
import random
import machine
pin = machine.Pin(2)  #blinking is optional, check your LED pin

#Place these Certs at same folder level as your MicroPython program
#No need to alter your AWS Client Cert and Private Key
CERT_FILE = "/certificate.pem.crt"  
KEY_FILE = "/private.pem.key"

MQTT_CLIENT_ID = "myUniqueID"
MQTT_PORT = 8883 #MQTT secured

PUB_TOPIC = "iot/outTopic" #coming out of device
SUB_TOPIC = "iot/inTopic"  #coming into device

#Your AWS IoT Endpoint found at IoT Core-->Settings
#Change the following three settings
MQTT_HOST = "<YOUR-AWS-ATS-IOT-ENDPOINT>" #YEx: dhRtqf1kr1mft-ats.iot.us-east-1.amazonaws.com 
WIFI_SSID = "<Your-WiFi-Network-Name-Here>"
WIFI_PW = "<Your-WiFi-Password>"

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

def cloud_connect():    
    global MQTT_CLIENT

    try:  #Security certs
        with open(KEY_FILE, "r") as f: 
            key = f.read()
        print("Got Private Key")
       
        with open(CERT_FILE, "r") as f: 
            cert = f.read()
        print("Got Client/Device Cert")

        MQTT_CLIENT = MQTTClient(client_id=MQTT_CLIENT_ID, server=MQTT_HOST, port=MQTT_PORT, keepalive=5000, ssl=True, ssl_params={"cert":cert, "key":key, "server_side":False})
        MQTT_CLIENT.connect()
        print('MQTT Connected')
        MQTT_CLIENT.set_callback(sub_cb)
        MQTT_CLIENT.subscribe(SUB_TOPIC)
        print('Subscribed to %s as the incoming topic' % (SUB_TOPIC))
        return MQTT_CLIENT
    except Exception as e:
        print('Cannot connect MQTT: ' + str(e))
        raise

#Start execution
try:
    print("Connecting WiFi netowrk")
    network_connect()
    print("Connecting to AWS IoT")
    cloud_connect()
    while True: #loop forever
            pin.value(1)
            pending_message = MQTT_CLIENT.check_msg()  # check for new subscribed payload incoming
            if pending_message != 'None':  #check if message is pending
                temp =  random.randint(0, 130)
                humid = random.randint(0, 100)
                deviceTime = time.time()
                print("Publishing")
                pub_msg("{\n  \"temperature\": %d,\n  \"humidity\": %d,\n \"timestamps\": %d\n}"%(temp,humid,deviceTime))      
                print("published payload")
                time.sleep(5)  #A 5 second delay between publishing, adjust as you like
            
except Exception as e:
    print(str(e))
