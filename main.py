from GoProController import GoProController as GPC

if __name__ == "__main__":
    gpc = GPC("wlan0")
    ssid = "theprogo"
    pw = "calculator"
    image = gpc.getImage(ssid,pw)
    print(image)
