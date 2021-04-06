import configparser
import logging
import paho.mqtt.client as mqtt
import time
import json
import os

#globals
config = configparser.ConfigParser()
client = mqtt.Client("PiMonitor")
lastHeartbeatTS = int(time.time()) 
motionTS = int(time.time())



def initialisation():
    global config
    global client
    config.read('piCam.ini')
    #config['DEFAULT']['screenAliveTime']
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
    logging.debug(initialisation.__name__ )

    #MQTT Setup
    #client.connect(config['mqtt']['mqttBroker']) 
    client.username_pw_set(username='xxx',password='xxxx')
    #client.connect("mqtt.stanners.co.nz") 
 
    client.subscribe(config['mqtt']['mqttTopic'])
    client.on_message=on_message 
    client.loop_start()

# countdown after a motion message has been received
def screenOffCountdown(timeToOff):
    logging.debug(screenOffCountdown.__name__ )


# Force the screen on (touch screen or no server hearbeat)
def screenPower(powerSetting):
    logging.debug(screenPower.__name__ )
    if powerSetting == 'ON':
        logging.debug(screenPower.__name__ + " Screen On")
        os.system("vcgencmd display_power 1")
    else:
        logging.debug(screenPower.__name__ + " Screen Off")
        os.system("vcgencmd display_power 0")


#Turn PI screen on of screen on of off

# Endless loop checking for server heartbeat
def serverHeartbeatMonitor():
    logging.debug(serverHeartbeatMonitor.__name__ )
    


# MQTT Stuff
def on_message(client, userdata, message):
    global lastHeartbeatTS
    global motionTS
    logging.debug("received message: " + str(message.payload.decode("utf-8")))
    m_decode = str( message.payload.decode("utf-8","ignore") )
    mqttMessage = json.loads(m_decode)

    if mqttMessage['message'] == 'ping' : 
        lastHeartbeatTS = int(time.time()) 
   
    if mqttMessage['message'] == 'motion' :
        motionTS = int(time.time())        

if __name__ == '__main__':
    initialisation()
    logging.info(__name__ )

    while True:
        time.sleep(1)

        logging.debug("motion  " +  str(motionTS) + " : " + str( int (time.time()) - int(config['DEFAULT']['screenMotionAliveTime'])  ) )

        logging.debug("heartbt " +  str(lastHeartbeatTS) + " : " + str( int (time.time()) - int(config['DEFAULT']['serverHeatbeatMissingSecs']) ) )

        if motionTS >  int (time.time()) - int(config['DEFAULT']['screenMotionAliveTime']) :
            screenPower('ON')
        else:
            if lastHeartbeatTS <  int (time.time()) - int(config['DEFAULT']['serverHeatbeatMissingSecs']) :
                screenPower('ON')
            else:
                screenPower('OFF')


