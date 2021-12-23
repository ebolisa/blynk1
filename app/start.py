import BlynkLib
from BlynkTimer import BlynkTimer
import network
import machine
import utime
gc.collect()


VERSION = "1.0"
print('Code version: ', VERSION)

# works ****
#ping google
# import usocket
# try:
#     # print(usocket.getaddrinfo('www.google', 443))
#     r = usocket.getaddrinfo("googles.com",1)[0][-1][0]
#     print(r)
# except OSError as err:
#     print(err.errno)
#     if (err.errno == -202):
#         print('wifi down')
# ****

# turn led off
yellow_led.on()

DEBUG = True
def dprint(*args):
        if DEBUG:
            print(*args)
          

def restart_and_reconnect(reason):
    dprint('Some went wrong. Reconnecting...')
    dprint('Due to ', reason)
    utime.sleep(5)
    machine.reset()
            

if wlan.isconnected():
    for x in range(10):
        yellow_led.off()
        utime.sleep(0.25)
        yellow_led.on()
        utime.sleep(0.25)
else:
    yellow_led.on()
    utime.sleep(2)
    restart_and_reconnect('No wifi')
            

dprint('IP:', wlan.ifconfig()[0])

timer = BlynkTimer()


# Initialize Blynk
try:
#         blynk = BlynkLib.Blynk(BLYNK_AUTH, insecure=True)
    blynk = BlynkLib.Blynk(wifimgr.get_profiles()[2],
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
    utime.sleep(5)
#     restart_and_reconnect('Blynk server failure...')
    

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
    utime.sleep_ms(150)
    if int(value[0]) == 1:
        R1.on()
        timer.set_timeout(timeout_delay, R1_timeout)


@blynk.on("V2")
def blynk_handle(value):
    utime.sleep_ms(150)
    if int(value[0]) == 1:
        R2.on()
        timer.set_timeout(timeout_delay, R2_timeout)


@blynk.on("V3")
def blynk_handle(value):
    utime.sleep_ms(150)
    if int(value[0]) == 1:
        R3.on()
        timer.set_timeout(timeout_delay, R3_timeout)
        

@blynk.on("V4")
def blynk_handle(value):
    utime.sleep_ms(150)
    if int(value[0]) == 1:
        R4.on()
        timer.set_timeout(timeout_delay, R4_timeout)


@blynk.on("V5")
def blynk_handle(value):
    utime.sleep_ms(150)
    if int(value[0]) == 1:
        R5.on()
        timer.set_timeout(timeout_delay, R5_timeout)


@blynk.on("V6")
def blynk_handle(value):
    utime.sleep_ms(150)
    if int(value[0]) == 1:
        R6.on()
        timer.set_timeout(timeout_delay, R6_timeout)


@blynk.on("V7")
def blynk_handle(value):
    utime.sleep_ms(150)
    if int(value[0]) == 1:
        R7.on()
        timer.set_timeout(timeout_delay, R7_timeout)


@blynk.on("V8")
def blynk_handle(value):
    utime.sleep_ms(150)
    if int(value[0]) == 1:
        R8.on()
        timer.set_timeout(timeout_delay, R8_timeout)
        
        
# test relays
@blynk.on("V9")
def blynk_handle(value):
    utime.sleep_ms(150)
    if int(value[0]) == 1:
        for x in range(len(rls_arr)):
            rls_arr[x].on()
            utime.sleep(0.5)
            rls_arr[x].off()
            utime.sleep(0.5)              


def check_wifi():
    if wlan.isconnected():
        yellow_led.on()
        rssi = wlan.status('rssi')
        blynk.virtual_write(10, str(rssi))
    else:
        yellow_led.off()
        
        
def Loop():
    gc.collect()
    while True:       
        blynk.run()
        timer.run()
        machine.idle()


timer.set_interval(15, check_wifi) # check on wifi every 15 seconds

# Run blynk in the main thread
try:
    import _thread
#     Loop()
    _thread.stack_size(5*1024)
    _thread.start_new_thread(Loop, ())
except:
    restart_and_reconnect('In Loop')

# You can also run blynk in a separate thread (ESP32 only)
#import _thread
#_thread.stack_size(5*1024)
#_thread.start_new_thread(Loop, ())
