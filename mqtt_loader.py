#!/usr/bin/python 

import paho.mqtt.client as paho 
import os
callback_functs = {}
logger=None
MY_NAME="MQTT"
def set_logger(l):
    global logger
    l.log_info(MY_NAME,"Logger linked!")
    logger=l
def register_callback(name,funct):
    global logger
    global callback_functs
    try:
        logger.log_info(MY_NAME,"Callback recorded: "+name)
        callback_functs[name]=funct
    except Exception as e:
        logger.log_err(MY_NAME,"Failed to Register Callback! :"+str(e))
def on_connect(client, userdata, flags, rc): 
    global logger
    logger.log_info(MY_NAME,"Connection Established!")

def on_publish(client, userdata, mid): 
        pass;

def on_message(client, userdata, msg):
    global callback_functs
    global logger
#    print("[MQTT] RECEIVED:"+ msg.topic+" "+str(msg.payload))
    logger.log_info(MY_NAME,"Received: "+msg.topic+" "+str(msg.payload))
    try:
        if(msg.topic in callback_functs):
            callback_functs[msg.topic](msg.payload.decode()) # Call the callback function with payload
            logger.log_info(MY_NAME,"Returned from Callback")
        else:
#            print("[MQTT] Note: Received message for unregistered callback")
             logger.log_warn(MY_NAME,"Received Message for unregistered callback")
    except Exception as ex:
        logger.log_err(MY_NAME,"Failed to process callback! : "+str(ex))
#        print("[MQTT] : Failed to process callback! : "+str(ex))

def start_mqtt():
    global logger
    #print("[MQTT] : Waiting for Connection...")
    logger.log_info(MY_NAME,"Waiting for Connection...")

    client.on_publish = on_publish 

    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set("fishTank","CptS84fMuQtYBRB") 

    client.tls_set(None) 

    client.connect("ebcd0562010d4d17b2acce44d85128f1.s1.eu.hivemq.cloud", 8883); 

    client.loop_start() 
def subscribe(topic,Qos):
    global logger
    client.subscribe(topic,qos=Qos)
def publish(topic,data):
    global logger
    client.publish(topic,data)
client = paho.Client() 

print("[MQTT] : mqtt loaded... start with mqtt_loader.start_mqtt()")

