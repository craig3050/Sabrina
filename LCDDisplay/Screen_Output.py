# loading the class
import lcddriver
from time import *
from datetime import datetime
from subprocess import *
import paho.mqtt.client as mqtt

MQTT_Message = ""

while True:
   

   # mqtt subscribes, displays message
   # The callback for when the client receives a CONNACK response from the server.
   def on_connect(client, userdata, flags, rc):
      print("Connected with result code "+str(rc))

      # Subscribing in on_connect() means that if we lose the connection and
      # reconnect then subscriptions will be renewed.
      print ("Subscribing to all")
      client.subscribe("$SYS/#")


   # The callback for when a PUBLISH message is received from the server.
   def on_message(client, userdata, msg):
      print ("MQTT Message incoming")
      MQTT_Message = (msg.topic+" "+str(msg.payload))
      print (MQTT_Message)

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
      lcd.lcd_display_string("%s" % (MQTT_Message), 3)
      lcd.lcd_display_string("              ", 4)

      print("Sleeping")
      sleep(20)

      return(msg.topic+" "+str(msg.payload))

   client = mqtt.Client()
   client.on_connect = on_connect
   client.on_message = on_message

   client.connect("192.168.0.10", 1883, 60)
   

   # Blocking call that processes network traffic, dispatches callbacks and
   # handles reconnecting.
   # Other loop*() functions are available that give a threaded interface and a
   # manual interface.
   client.loop_forever()







