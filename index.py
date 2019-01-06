import pprint
import subprocess
import json
import re
import time
import RPi.GPIO as gpio
import threading
import queue

MOUNTPOINT = '/media/pi/'
BACKUP_DEST_NAME = 'backupX'
LED_GPIO = 13

ledRate = queue.Queue()

LED_SLOW = 5
LED_MEDIUM = 1
LED_FAST = 0.15

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(LED_GPIO, gpio.OUT)

def ledOn():
    gpio.output(LED_GPIO, 1)
    
def ledOff():
    gpio.output(LED_GPIO, 0)
    
        
def ledThread():
    rate = 'slow'
    while True:
        if(not ledRate.empty()):
            rate = ledRate.get()
            print("****************************************" + rate)
            ledRate.task_done()
        if(rate == 'slow'):
            ledOn()
        elif(rate == 'medium'):
            ledOn()
            time.sleep(LED_MEDIUM)
            ledOff()
            time.sleep(LED_FAST)
        elif(rate == 'fast'):
            ledOn()
            time.sleep(LED_FAST)
            ledOff()
            time.sleep(LED_FAST)
    
def runBackup(src, dest):
    srcPath = src['mountpoint']
    destPath = dest['mountpoint']
    
    ledRate.put('medium', False)
    
    runSync = subprocess.Popen(['rsync', '-abv', '--outbuf=L', '--info=progress2',  srcPath, destPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    lastPercentage = '0%'
    
    for line in iter(runSync.stdout.readline, b''):
        progress = line.split()
        if len(progress) == 6: # total transferred | % | speed | file transfer time | ??? | files remaining
            print("### " + progress[1] + " - " + progress[5])
        elif len(progress) == 4:  # size transferred | % | Current speed | Time remaining
            if lastPercentage != progress[1]:
                lastPercentage = progress[1]
                print(">>> " + progress[1] + " - " + progress[3] + " remaining")
        elif "total size is" in line:
            print(line)
            break
        else:
            print("$$$$$$$ " + line)
    
    print('done')
    
    shutdown()

def shutdown():
    subprocess.call('sudo poweroff', shell=True)
    
def waitForDriveDisconnect(src, dest):
    while False:
        print('do something here')
    
def main():
    print('in main thread')
    ledRate.put('slow')
    
    waitingForSrcAndDest = True

    while waitingForSrcAndDest:
        df = subprocess.check_output("lsblk -o label,name,mountpoint --noheadings --json", shell=True)
        devices = json.loads(df.decode('utf-8'))
        src = None
        dest = None

        for device in devices['blockdevices']:
            child = device['children'][0]
            if child:
                mountpoint = child['mountpoint']
                if (mountpoint and mountpoint.find(MOUNTPOINT) == 0):
                    if child['label'] == BACKUP_DEST_NAME:
                        dest = child
                    else:
                        src = child

        if (src and dest):
            waitingForSrcAndDest = False
            pprint.pprint(src)
            pprint.pprint(dest)
            runBackup(src, dest)
        else:
            print('wait...')
            time.sleep(1)

t = threading.Thread(target=ledThread)
t.daemon = True
t.start()

main()