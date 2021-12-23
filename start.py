# mqtt_as.py Asynchronous version of umqtt.robust
# (C) Copyright Peter Hinch 2017-2021.
# Released under the MIT licence.
# https://github.com/peterhinch/micropython-mqtt/tree/master/mqtt_as

# OTA code from https://github.com/rdehuyss/micropython-ota-updater


# from sys import platform
# print('platform:',platform)

from mqtt_as import MQTTClient, config
from app.config import wifi_led, blue_led
import uasyncio as asyncio
import machine
import network
import sys
import gc
gc.collect()

VERSION = "beta +1"
print('Code version: ', VERSION)

# used to flip pins output level
inverse = True

pub_topic = 'casa/esp/32/oled/wlan'  # For demo publication and last will use same topic
sub_topic = 'casa/esp/32/oled'

outages = 0
rssi = -199

# set relay array pins
R1 = machine.Pin(19, machine.Pin.OUT)
R2 = machine.Pin(18, machine.Pin.OUT)
R3 = machine.Pin(5, machine.Pin.OUT)
R4 = machine.Pin(17, machine.Pin.OUT)
R5 = machine.Pin(16, machine.Pin.OUT)
R6 = machine.Pin(21, machine.Pin.OUT)
R7 = machine.Pin(4, machine.Pin.OUT)
R8 = machine.Pin(15, machine.Pin.OUT)
yel_led = machine.Pin(32, machine.Pin.OUT)

# reset relays
rls_arr = [R1, R2, R3, R4, R5, R6, R7, R8]
for x in range(len(rls_arr)):
    if inverse:
        rls_arr[x].value(1)
    else:
        rls_arr[x].value(1)

def restart_and_reconnect():
    from utime import sleep
    print('Some went wrong. Reconnecting...')
    utime.sleep(10)
    machine.reset()

def test_relays():
    from utime import sleep
    for x in range(len(rls_arr)):
        if inverse:
            rls_arr[x].off()
            sleep(1)
#             await asyncio.sleep(timer)
            rls_arr[x].on()
            sleep(1)
        else:
            rls_arr[x].on()
            sleep(1)
            rls_arr[x].off()
            sleep(1)

async def pulse():  # This demo pulses blue LED each time a subscribed msg arrives.
    yel_led(True)
    await asyncio.sleep(1)
    yel_led(False)

def sub_cb(topic, msg, retained):
    print((topic, msg))
    asyncio.create_task(pulse()) # This pulses blue LED each time a subscribed msg arrives.
    data = msg.decode()

    if topic.decode() == sub_topic:
        try:
            if data == "test":
                test_relays()
            elif data == "dummy":
                led.off()
                utime.sleep(0.5)
                led.on()
            elif data == "R11":
                if inverse:
                    R1.off()
                else:
                    R1.on()
            elif data == "R10":
                if inverse:
                    R1.on()
                else:
                    R1.off()
            elif data == 'R21':
                if inverse:
                    R2.off()
                else:
                    R2.on()
            elif data == 'R20':
                if inverse:
                    R2.on()
                else:
                    R2.off()
            elif data == "R31":
                if inverse:
                    R3.off()
                else:
                    R3.on()
            elif data == "R30":
                if inverse:
                    R3.on()
                else:
                    R3.off()
            elif data == 'R41':
                if inverse:
                    R4.off()
                else:
                    R4.on()
            elif data == 'R40':
                if inverse:
                    R4.on()
                else:
                    R4.off()
            elif data == "R51":
                if inverse:
                    R5.off()
                else:
                    R5.on()
            elif data == "R50":
                if inverse:
                    R5.on()
                else:
                    R5.off()
            elif data == 'R61':
                if inverse:
                    R6.off()
                else:
                    R6.on()
            elif data == 'R60':
                if inverse:
                    R6.on()
                else:
                    R6.off()
            elif data == "R71":
                if inverse:
                    R7.off()
                else:
                    R7.on()
            elif data == "R70":
                if inverse:
                    R7.on()
                else:
                    R7.off()
            elif data == 'R81':
                if inverse:
                    R8.off()
                else:
                    R8.on()
            elif data == 'R80':
                if inverse:
                    R8.on()
                else:
                    R8.off()
            else:
                pass
        except Exception as e:
            if DEBUG: print(e)
            restart_and_reconnect()

async def wifi_han(state):
    global outages
    wifi_led(not state)  # Light LED when WiFi down
    if state:
        print('We are connected to broker.')
    else:
        outages += 1
        print('WiFi or broker is down.')
    await asyncio.sleep(1)
    # RESTART BOARD!!


async def get_rssi():
    global rssi
    s = network.WLAN()
    ssid = config['ssid'].encode('UTF8')
    while True:
        try:
            rssi = [x[3] for x in s.scan() if x[0] == ssid][0]
        except IndexError:  # ssid not found.
            rssi = -199
        await asyncio.sleep(30)


async def conn_han(client):
    print('Subscribing...')
    await client.subscribe(sub_topic, 1)

async def main(client):
    try:
        await client.connect()
        await asyncio.sleep(2)  # Give broker time
#         print('rssi ', MQTTClient.wifi_connect.rssi)
    except OSError:
        print('Connection failed.')
        return
    n = 0
    # s = '{} repubs: {} outages: {} rssi: {}dB free: {}bytes'
    s = 'rssi: {}dB free: {} bytes'
    while True:
        await asyncio.sleep(5)
        gc.collect()
        m = gc.mem_free()
        get_rssi()
        # If WiFi is down the following will pause for the duration.
        await client.publish(pub_topic, s.format(rssi, m), qos = 1)
#         await client.publish(pub_topic, '{} repubs: {} outages: {}'.format(n, client.REPUB_COUNT, outages), qos = 1)
        n += 1

# Define configuration
config['subs_cb'] = sub_cb
config['wifi_coro'] = wifi_han
config['will'] = (pub_topic, 'Goodbye cruel world!', False, 0)
config['connect_coro'] = conn_han
config['keepalive'] = 120

# Set up client. Enable optional debug statements.
MQTTClient.DEBUG = False
client = MQTTClient(config)

asyncio.create_task(get_rssi())
try:
#     loop = asyncio.get_event_loop()
    asyncio.run(main(client))
finally:  # Prevent LmacRxBlk:1 errors.
    client.close()
    blue_led(True)
    asyncio.new_event_loop()