from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from serial import Serial
import logging
import time
import argparse
import json
import mysql.connector
import sqlalchemy as sql
import string

AllowedActions = ['both', 'publish', 'subscribe']

# Connect to mysql
# sql_engine = sql.create_engine("mysql+mysqlconnector://root:123456@172.17.0.3")
mydb = mysql.connector.connect(host="172.17.0.3", user="root", passwd="0000", database="test")
cursor = sql_engine.cursor()

# Custom MQTT message callback
def customCallback(client, userdata, message):
      # message.payload : "{"time": "2019-12-27 13:56:00", "type": "PM2.5", "value": "-55.18", "sequence": 138}"
      print("Received a new message: ")
      print(message.payload)
      print("from topic: ")
      print(message.topic)
      print("--------------\n\n")

      temp_str = message.payload.strip(string.punctuation).split(',')
      data = [i.split(":")[1] for i in temp_str]
      sql = "INSERT INTO pm25 (pm25, value, sequence) VALUES (%s,%s,%s)"
      value = data
      cursor.execute(sql,value)
      mydb.commit()
      print(cursor.rowcount, "record inserted.")

def publish(PM25, loopCount):
    if mode == 'both' or mode == 'publish':
        message = {}
        message['type'] = 'PM2.5'
        message['value'] = PM25
        message['sequence'] = loopCount
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        if mode == 'publish':
            print('Published topic %s: %s\n' % (topic, messageJson))

host = "a2jzype8xfobeg-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "/home/ubuntu/root-CA.crt"
certificatePath = "/home/ubuntu/RpiPM25.cert.pem"
privateKeyPath = "/home/ubuntu/RpiPM25.private.key"
useWebsocket = False
clientId = "ec2"
topic = "Rpi/PM25"
mode = "subscribe"


# Port defaults
if useWebsocket:  # When no port override for WebSocket, default to 443
    port = 443
if not useWebsocket:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
if mode == 'both' or mode == 'subscribe':
    while True:
      myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
      time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
ser = Serial('/dev/ttyACM0', 9600, timeout=.5) # Arduino port

#while True:
#    if ser.inWaiting():
#        str = ser.readline().decode('utf8')[:-2]
#        end = str.find(' : ')
#        if end > 0:
#            PM25 = str[:end]
#            publish(PM25,loopCount)
#            loopCount += 1