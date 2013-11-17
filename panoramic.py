import time
import RPi.GPIO as GPIO
import datetime as dt
from numpy import linalg
from GoProController import GoProController as GPC
#from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import urllib2
import numpy as np

def getImages(dir="http://10.5.5.9:8080/videos/DCIM/100GOPRO/"):
    soup = BeautifulSoup(urllib2.urlopen(dir))

    links = soup.find_all('a', attrs={'class': 'link'})
    linkList = filter(lambda x: ".JPG" in x, [y["href"] for y in links])


    print(linkList[-6:])
    for n,imageLink in enumerate(linkList[-3:]):
        imgRqst = urllib2.Request("img/"+dir+imageLink)
        imgData = urllib2.urlopen(imgRqst).read()
        outFile = open("img"+str(n+1)+".jpg","wb")
        outFile.write(imgData)
        outFile.close()


def takePanoramic():
    for n in xrange(6):
        GPIO.output(02, True)
        time.sleep(1)
        GPIO.output(02, False)
        gpc.sendCommand(ssid,pw,"record_on")
        time.sleep(1)


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)
    GPIO.setup(02, GPIO.OUT)
    GPIO.output(02, False)
    GPIO.setup(03, GPIO.OUT)
    GPIO.output(03, False)
    GPIO.setup(04, GPIO.OUT)
    GPIO.output(04, False)
    GPIO.setup(14, GPIO.OUT)
    GPIO.output(14, False)

    gpc = GPC("wlan0")
    ssid = "theprogo"
    pw = "calculator"
    print gpc.sendCommand(ssid,pw,"mode_still")
    print gpc.sendCommand(ssid,pw,"record_on")
    #getImages()

