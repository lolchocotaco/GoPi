from GoProController import GoProController as GPC
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import urllib2


def getImageNames(dir="http://10.5.5.9:8080/videos/DCIM/100GOPRO/"):
    soup = BeautifulSoup(open(dir))
    #print soup.prettify()

    links = soup.find_all('a', attrs={'class': 'link'})
    linkList = filter(lambda x: ".JPG" in x, [y["href"] for y in links])
    #linkList = []
    #for link in links:
    #    if ".JPG" in link["href"]:
    #        linkList += [link["href"]]
    #        #print(link["href"])

    print(linkList[-3:])
    for imageLink in linkList[-3:]:
        imgRqst = urllib2.Request(imageLink)
        imgData = urllib2.urlopen(imgRqst).read()
        print(imgData)


    #r = requests.get(dir)
    #tree = ET.fromstring(r.text)
    #root = tree.getroot()
    #
    #for link in root.iter("a"):
    #    if link.attrib["class"] == "link" and ".jpg" in link.text.lower():
    #        print link.text

if __name__ == "__main__":
    gpc = GPC("wlan0")
    ssid = "theprogo"
    pw = "calculator"


    getImageNames("./photosrc.html")

