#!/usr/bin/python3 

import paho.mqtt.client as mqtt 

  

def on_connect(client, userdata, flags, rc): 

    print("CONNACK received with code %d." % (rc)) 

def on_publish(client, userdata, mid): 
        pass;

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client() 

client.on_publish = on_publish 

client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("fishTank","CptS84fMuQtYBRB") 

client.tls_set(None) 

client.connect("ebcd0562010d4d17b2acce44d85128f1.s1.eu.hivemq.cloud", 8883); 

client.loop_start() 

#while True: 
#        
#        (rc, mid) = client.publish("temp/value","Python", qos=1) 
        
