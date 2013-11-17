import time
import RPi.GPIO as GPIO
import datetime as dt
from numpy import linalg
from GoProController import GoProController as GPC
from bs4 import BeautifulSoup
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
    pass


if __name__ == "__main__":
    gpc = GPC("wlan0")
    ssid = "theprogo"
    pw = "calculator"
    #getImages()

