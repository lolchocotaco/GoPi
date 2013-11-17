#!/usr/bin/python

# GoProController.py
# Josh Villbrandt <josh@javconcepts.com>
# 8/24/2013

# import django settings
import os, sys
sys.path.append('/var/sites/GoProSite/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'GoProSite.settings'
import GoProSite

# import django models
from GoProApp.models import *

# import controller
from GoProController import GoProController
controller = GoProController()

# other includes
from django.utils import timezone
import json
import time

# settings
maxRetry = 3

# send command
def sendCommand(command):
    i = 0
    result = False
    while i < maxRetry and result == False:
        result = controller.sendCommand(command.camera.ssid, command.camera.password, command.command)
        # TODO: check result, if failed, put in a new command for later so that we can go through the rest of the list now
        i += 1

    command.time_completed = timezone.now()
    command.save()

# get status
def getStatus(camera):
    camera.last_attempt = timezone.now()
    status = controller.getStatus(camera.ssid, camera.password)
    camera.status = json.loads(camera.status)
    for key in status:
        if isinstance(status[key], dict) and isinstance(camera.status[key], dict):
            for keykey in status[key]:
                camera.status[key][keykey] = status[key][keykey]
        else:
            camera.status[key] = status[key]
    if 'power' in status:
        camera.last_update = camera.last_attempt

    # grab snapshot
    if 'power' in status and status['power'] == 'on':
        image = controller.getImage(camera.ssid, camera.password)
        if image != False:
            camera.image = image

    # save camera
    camera.status = json.dumps(camera.status)
    camera.save()

# main loop here
print "Starting GoProProxy..."

# keep running until we land on Mars (and come back?)
# keep the contents of this loop short (limit to one cmd/status or one status) so that we can quickly catch KeyboardInterrupt, SystemExit
while "people" != "on Mars":
    # PRIORITY 1: send a command for the network we are currently on if possible
    command_set = CameraCommand.objects.filter(time_completed__isnull=True, camera__ssid__exact=controller.currentSSID)
    if len(command_set) > 0:
        sendCommand(command_set[0])
        if(command_set[0].command != "power_off"):
            getStatus(command_set[0].camera) # get the status now because it is cheap
    else:
        # PRIORITY 2: send the oldest command still in the queue
        command_set = CameraCommand.objects.filter(time_completed__isnull=True).order_by('-date_added')
        if len(command_set) > 0:
            sendCommand(command_set[0])
            if(command_set[0].command != "power_off"):
                getStatus(command_set[0].camera) # get the status now because it is cheap
        else:
            # PRIORITY 3: check status of the most stale camera
            camera_set = Camera.objects.all().order_by('last_attempt')
            if len(camera_set) > 0:
                getStatus(camera_set[0])

    # protect the cpu in the event that there was nothing to do
    time.sleep(0.1)

