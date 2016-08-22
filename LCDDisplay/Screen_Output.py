#!/usr/bin/python
# loading the class
import lcddriver
from time import *
from datetime import datetime
from subprocess import *
import paho.mqtt.client as mqtt
import re #regex module for character searching

MQTT_Message = ""
MQTT_Topic = ""

while True:
   

   # mqtt subscribes, displays message
   # The callback for when the client receives a CONNACK response from the server.
   def on_connect(client, userdata, flags, rc):
      print("Connected with result code "+str(rc))

      # Subscribing in on_connect() means that if we lose the connection and
      # reconnect then subscriptions will be renewed.
      print ("Subscribing to all")
      client.subscribe("#")


   # The callback for when a PUBLISH message is received from the server.
   def on_message(client, userdata, msg):
      print ("MQTT Message incoming")
      MQTT_Topic = (msg.topic+" "+str(msg.payload))
      print (MQTT_Topic)

      #Regex expression to group the topic and message in to separate sections - keeping the last topic value after the last "/"
      #e.g "/test1/test2/temperature 666" - group 2 becomes "temperature 666" while group 1 becomes /test1/test2/
      text_remove = re.search(r'(.*\/)([^/]*)', MQTT_Topic)
      print (text_remove.group(2))

      MQTT_Message = MQTT_Topic.replace(text_remove.group(1), "")
      MQTT_Topic = MQTT_Topic.replace(text_remove.group(2), "")
      print (MQTT_Message)
      print (MQTT_Topic)


      # get IP address from Pi
      cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
     
      # lcd start
      print ("Starting LCD")
      lcd = lcddriver.lcd()

      # clears the lcd screen
      print ("Clearing LCD")
      lcd.lcd_clear()

      # function to get the ip address (and a lot of other junk)
      print ("Getting IP Address")
      def run_cmd(cmd):
         p = Popen(cmd, shell=True, stdout=PIPE)
         output = p.communicate()[0]
         return output

      # runs function to get ip address and cleans up the output
      print ("Clearing Up IP address")
      ipaddr = run_cmd(cmd)
      ip_number = ""
      for x in ipaddr:
         if x == "\n":
            break
         else:
            ip_number += x


      # gets the current time & date
      print ("Getting time and date")
      the_time = strftime('%Y-%m-%d     %H:%M')

      # shorten the MQTT message to stop screen overflow
      counted_length = 0
      short_MQTT_message = ""

      for x in MQTT_Message:
         short_MQTT_message += x
         counted_length +=1
         if counted_length >19:
            break


      #   print the information to the screen
      print("Printing info to screen")
      lcd.lcd_display_string('%s' % (the_time), 1)
      lcd.lcd_display_string('IP %s' % ( ip_number ), 2)
      lcd.lcd_display_string("%s" % (MQTT_Topic), 3)
      lcd.lcd_display_string("%s" % (short_MQTT_message), 4)

      print("Sleeping")
      sleep(20)

      return(msg.topic+" "+str(msg.payload))

   client = mqtt.Client()
   client.on_connect = on_connect
   client.on_message = on_message

   client.connect("192.168.0.10", 1883, 60)

   # get IP address from Pi
   cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
     
   # lcd start
   print ("Starting LCD")
   lcd = lcddriver.lcd()

   # clears the lcd screen
   print ("Clearing LCD")
   lcd.lcd_clear()

   # function to get the ip address (and a lot of other junk)
   print ("Getting IP Address")
   def run_cmd(cmd):
      p = Popen(cmd, shell=True, stdout=PIPE)
      output = p.communicate()[0]
      return output

   # runs function to get ip address and cleans up the output
   print ("Clearing Up IP address")
   ipaddr = run_cmd(cmd)
   ip_number = ""
   for x in ipaddr:
      if x == "\n":
         break
      else:
         ip_number += x


   # gets the current time & date
   print ("Getting time and date")
   the_time = strftime('%Y-%m-%d     %H:%M')

   #   print the information to the screen
   print("Printing info to screen")
   lcd.lcd_display_string('%s' % (the_time), 1)
   lcd.lcd_display_string('IP %s' % ( ip_number ), 2)
   lcd.lcd_display_string("Sabrina Home Auto", 3)
   lcd.lcd_display_string("Craig Rules!", 4)

   sleep(20)

   # Blocking call that processes network traffic, dispatches callbacks and
   # handles reconnecting.
   # Other loop*() functions are available that give a threaded interface and a
   # manual interface.
   client.loop_forever()







