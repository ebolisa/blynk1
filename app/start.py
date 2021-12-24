# Module file: start.py

import BlynkLib
from BlynkTimer import BlynkTimer
from gpios import *
import network
import gc
gc.collect()

dprint('Memory free', gc.mem_free())

VERSION = "3.0"
dprint('Code version: ', VERSION)

# turn led off
yellow_led.on()

# get wifi credentials
with open("wifi.dat") as f:
    lines = f.readlines()
for line in lines:
    ssid, pwd, BLYNK_AUTH = line.strip("\n").split(";")

timer = BlynkTimer()

# Initialize Blynk
try:
#         blynk = BlynkLib.Blynk(BLYNK_AUTH, insecure=True)
    blynk = BlynkLib.Blynk(BLYNK_AUTH,
        insecure=True,          # disable SSL/TLS
        server='fra1.blynk.cloud', # fra1.blynk.cloud or blynk.cloud
        port=80,                # set server port
        heartbeat=30,           # set heartbeat to 30 secs
        log=dprint              # use print function for debug logging
        )
except OSError as e:
    dprint('ERROR', e)
    restart_and_reconnect(e)


@blynk.on("connected")
def blynk_connected(ping):
    dprint('Blynk ready. Ping:', ping, 'ms')

@blynk.on("disconnected")
def blynk_disconnected():
    dprint('Blynk disconnected')
    sleep(5)
    restart_and_reconnect('Blynk server failure...')
    

# timeouts
timeout_delay = 1 # in seconds

def R1_timeout(): R1.off()
def R2_timeout(): R2.off()
def R3_timeout(): R3.off()
def R4_timeout(): R4.off()
def R5_timeout(): R5.off()
def R6_timeout(): R6.off()
def R7_timeout(): R7.off()
def R8_timeout(): R8.off()
# end timeouts


@blynk.on("V1")
def blynk_handle(value):
    sleep(0.15)
    if int(value[0]) == 1:
        R1.on()
        timer.set_timeout(timeout_delay, R1_timeout)


@blynk.on("V2")
def blynk_handle(value):
    sleep(0.15)
    if int(value[0]) == 1:
        R2.on()
        timer.set_timeout(timeout_delay, R2_timeout)


@blynk.on("V3")
def blynk_handle(value):
    sleep(0.15)
    if int(value[0]) == 1:
        R3.on()
        timer.set_timeout(timeout_delay, R3_timeout)
        

@blynk.on("V4")
def blynk_handle(value):
    sleep(0.15)
    if int(value[0]) == 1:
        R4.on()
        timer.set_timeout(timeout_delay, R4_timeout)


@blynk.on("V5")
def blynk_handle(value):
    sleep(0.15)
    if int(value[0]) == 1:
        R5.on()
        timer.set_timeout(timeout_delay, R5_timeout)


@blynk.on("V6")
def blynk_handle(value):
    sleep(0.15)
    if int(value[0]) == 1:
        R6.on()
        timer.set_timeout(timeout_delay, R6_timeout)


@blynk.on("V7")
def blynk_handle(value):
    sleep(0.15)
    if int(value[0]) == 1:
        R7.on()
        timer.set_timeout(timeout_delay, R7_timeout)


@blynk.on("V8")
def blynk_handle(value):
    sleep(0.15)
    if int(value[0]) == 1:
        R8.on()
        timer.set_timeout(timeout_delay, R8_timeout)
        
        
# test relays
@blynk.on("V9")
def blynk_handle(value):
    sleep(0.15)
    if int(value[0]) == 1:
        for x in range(len(rls_arr)):
            rls_arr[x].on()
            sleep(0.5)
            rls_arr[x].off()
            sleep(0.5)              


def check_wifi():
    s = network.WLAN()
    e_ssid = ssid.encode('UTF8')
    try:
        rssi = [x[3] for x in s.scan() if x[0] == e_ssid][0]
        yellow_led.off()
        blynk.virtual_write(10, str(rssi))
        yellow_led.on()
    except IndexError as e:  # ssid not found.
        dprint('IndexError', e)
        rssi = -99        
        
        
def Loop():
    while True:
        gc.collect()
        blynk.run()
        timer.run()


# check on wifi every 15 seconds
timer.set_interval(15, check_wifi) 

# Run blynk in the main thread
try:
#     import _thread
    Loop()
#     _thread.stack_size(5*1024)
#     _thread.start_new_thread(Loop, ())
except Exception as e:
    print(e)
    restart_and_reconnect(e)
