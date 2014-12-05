# -*- coding: utf-8 -*-

#important: before running this demo, make certain that you import the library
#'paho.mqtt.client' into python (https://pypi.python.org/pypi/paho-mqtt)

import allthingstalk_arduino_standard_lib as IOT       #provide cloud support
from time import sleep                             #pause the app
from subprocess import call
import os

#set up the ATT internet of things platform
# IOT.on_message = on_message
IOT.ClientId = <client_id>
IOT.ClientKey = <client_key>
IOT.DeviceId = <device_id>

In1Name = "foo"                                #name of the button
In1Id = 1                                      #the id of the button, don't uses spaces. required for the att platform
Out1Name = "bar"
Out1Id = 2


#callback: handles values sent from the cloudapp to the device
def on_message(id, value):
    if id.endswith(str(Out1Id)) == True:
        value = value.lower()                        #make certain that the value is in lower case, for 'True' vs 'true'
        if value == "true":
            print("true on " + Out1Name)
            IOT.send("true", Out1Id)                #provide feedback to the cloud that the operation was succesful
        elif value == "false":
            print("false on " + Out1Name)
            IOT.send("false", Out1Id)                #provide feedback to the cloud that the operation was succesful
        else:
            print("unknown value: " + value)
    else:
        print("unknown actuator: " + id)


#make certain that the device & it's features are defined in the cloudapp
IOT.connect()
IOT.addAsset(In1Id, In1Name, "In1Id", False, "String")
IOT.addAsset(Out1Id, Out1Name, "Out1Id", True, "bool")
IOT.subscribe()                                        		#starts the bi-directional communication

nextVal = True;
#main loop: run as long as the device is turned on
while True:
    temp = os.popen("/Users/peter_v/Documents/data/projects/temp/osx-cpu-temp/osx-cpu-temp").read()
    temp = temp[:2] + temp[3:4]
    print("temp is " + temp)
    IOT.send(temp, In1Id)
    sleep(2)
