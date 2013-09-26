#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import datetime as dt
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(02, GPIO.OUT)
GPIO.output(02, False)
GPIO.setup(03, GPIO.OUT)
GPIO.output(03, False)
GPIO.setup(04, GPIO.OUT)
GPIO.output(04, False)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, False)


t1=dt.datetime.now()
t3=0
GPIO.output(02, True)
while t3<1:
	t2=dt.datetime.now()
   	t3=(t2-t1).seconds
GPIO.output(02, False)
t1=dt.datetime.now()
t3=0
GPIO.output(14, True)
while t3<1:
	t2=dt.datetime.now()
   	t3=(t2-t1).seconds
GPIO.output(14, False)
t1=dt.datetime.now()
t3=0
GPIO.output(03, True)
while t3<1:
   	t2=dt.datetime.now()
  	t3=(t2-t1).seconds
GPIO.output(03, False)
t1=dt.datetime.now()
t3=0
GPIO.output(04, True)
while t3<1:
   	t2=dt.datetime.now()
   	t3=(t2-t1).seconds
GPIO.output(04, False)

