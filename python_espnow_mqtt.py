#!/opt/espnow/bin/python3

#  python_espnow_mqtt.py   - mimic the esp32/esphome espnow->mqtt gateway 
#                            from https://github.com/u-fire
#         guidance from :
#         https://github.com/u-fire for esp-now packet structure 
#             and packet parsing
#         https://github.com/ChuckMash/ESPythoNOW for esp-now receiver in python
#             and framework for adding mqtt calls
#             and prep instructions for wifi interface on linux


import os
import sys
import paho.mqtt
import paho.mqtt.client as mqttClient
import json
import time
from ESPythoNOW import *

#----  required config by env -----------------------
MqttBroker = os.environ.get('MQTTBROKER', '192.168.1.1')
MqttPort   = int ( os.environ.get('MQTTPORT', '1883') )
hassPrefix = os.environ.get('HASSPREFIX', 'homeassistant')
MqttWlan   = os.environ.get('MQTTWLAN', 'wlp1s0' )
os.environ['PYTHONUNBUFFERED'] = '1'
# -- non env defaults
GW=getattr( os.uname() , "nodename" )
#----  required config by env -----------------------


def callback(from_mac, to_mac, msg):
  publishNow(from_mac, msg.decode() )
  print("ESP-NOW : %s :  %s" % (from_mac, msg.decode() ), file=sys.stderr)

# mimic actions of Now_MQTT_BridgeComponent::receivecallback(const uint8_t *bssid, const uint8_t *data, int len)
#  see:  https://github.com/u-fire/ESPHomeComponents/tree/master/esphome/components/now_mqtt_bridge/now_mqtt_bridge.cpp
def publishNow( from_mac, msg ):
  tokens = msg.split(':');
  doc = {}
  macaddr = from_mac.replace(':', '').lower()  #  24:EC:4A:26:91:04 to 24ec4a269104
  if ( len(tokens) != 12 ):
#   print("   %d tokens found [bad]" % (len(tokens)) )
    print() # implicit return
  else:
#   print("   %d tokens found[good]" % (len(tokens)) )
    message_type = tokens[2];
    if ( message_type == "binary_sensor"):
       if ( len(tokens[3]) > 0 ): 
         doc['name'] = tokens[3] 
       if ( len(tokens[0]) != 0):
         stat_t = tokens[0] + "/binary_sensor" + tokens[3] + "/state" 
         doc['stat_t'] =stat_t
       if ( len(tokens[0]) != 0):
         uniq_id = macaddr + "_" + tokens[3]
         doc['uniq_id'] = uniq_id;
       doc["dev"] = {}
       doc["dev"]["ids"] = macaddr
       if ( len(tokens[0]) != 0):
         doc["dev"]["name"]  = tokens[0]
       doc["dev"]["sw"]  = tokens[8]
       doc["dev"]["mdl"]  = tokens[9]
       doc["dev"]["mf"]  = "expressif"
       topic = "%s/binary_sensor/%s/state" % ( tokens[0], tokens[3]  )
       client.publish( topic, tokens[5] , 0)
       print (topic )
       config_topic = "%s/binary_sensor/%s/%s/config" % ( hassPrefix ,tokens[0], tokens[3]  )
       json_doc = json.dumps(doc) 
       client.publish( config_topic, json_doc , 0)
    else:
       if ( len(tokens[1]) > 0 ): 
         doc['dev_cla'] = tokens[1] 
       if ( len(tokens[4]) > 0 ): 
         doc['unit_of_meas'] = tokens[4] 
       if ( len(tokens[2]) > 0 ): 
         doc['stat_cla'] = tokens[2] 
       if ( len(tokens[3]) > 0 ): 
         doc['name'] = tokens[3] 
       if ( len(tokens[6]) > 0 ): 
         icon = tokens[6] + ":" + tokens[7]
         doc['icon'] = icon
       if ( len(tokens[0]) > 0 ): 
         stat_t = tokens[0] + "/sensor/" + tokens[3] + "/state"
         doc['stat_t'] = stat_t
       if ( len(tokens[0]) != 0):
         uniq_id = macaddr + "_" + tokens[3]
         doc['uniq_id'] = uniq_id;
       doc["dev"] = {}
       doc["dev"]["ids"] = macaddr
       if ( len(tokens[0]) != 0):
         doc["dev"]["name"]  = tokens[0]
       doc["dev"]["sw"]  = tokens[8]
       doc["dev"]["mdl"]  = tokens[9]
       doc["dev"]["mf"]  = "expressif"
       doc["dev"]["ids"] = macaddr
       topic = "%s/sensor/%s/state" % ( tokens[0], tokens[3]  )
       client.publish( topic, tokens[5] , 0)
       print (topic )
       config_topic = "%s/sensor/%s/%s/config" % ( hassPrefix,tokens[0], tokens[3]  )
       json_doc = json.dumps(doc) 
       client.publish( config_topic, json_doc , 0)


##  ESP-NOW saw 24:EC:4A:26:91:04 to FF:FF:FF:FF:FF:FF  now55:voltage:measurement:now55_vdd:V:4.05:::2024.10.3:esp32-s3-devkitc-1:sensor:
##   {"dev_cla": "temperature", 
##    "unit_of_meas": "\u00b0F", 
##    "stat_cla": "measurement", 
##    "name": "now55_temperature", 
##    "stat_t": "now55/sensor/now55_temperature/state", 
##    "uniq_id": "24ec4a269104_now55_temperature", 
##    "dev": {
##         "ids": "24ec4a269104", 
##         "name": "now55", 
##         "sw": "2024.10.3", 
##         "mdl": "esp32-s3-devkitc-1", 
##         "mf": "expressif"}
##   }



client = mqttClient.Client(mqttClient.CallbackAPIVersion.VERSION2, GW )
if ( client.connect(MqttBroker, MqttPort, 60) != 0 ):
    print("Couldn't connect to the mqtt broker at %s" % MqttBroker )
    sys.exit(1)
espnow = ESPythoNow(interface = MqttWlan, accept_all=True, callback=callback)
espnow.start()
while True:
  time.sleep(1)
# input() # Run until enter is pressed  ( used when running in foreground)


