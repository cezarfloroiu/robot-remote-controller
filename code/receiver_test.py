"""
    Test receiving data from MIMIC-CONTROLLER
"""
import os
import utime
import machine

#print sys info
print(os.uname())

#indicate program started visually
led_onboard = machine.Pin(25, machine.Pin.OUT)
led_onboard.value(0)     # onboard LED OFF for 0.5 sec
utime.sleep(0.5)
led_onboard.value(1)

#2 sec timeout is arbitrarily chosen
def sendCMD_waitResp(cmd, timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(timeout)
    print()
    
def waitResp(timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print(resp)

def sendCMD_waitRespLine(cmd, timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitRespLine(timeout)
    print()
    
def waitRespLine(timeout=2000):
    prvMills = utime.ticks_ms()
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            print(uart.readline())
            
#print uart info
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(12), rx=machine.Pin(13))
#uart.init(9600, bits=8, parity=None, stop=1)
#uart = machine.UART(0, baudrate=9600, tx=machine.Pin(2), rx=machine.Pin(3))
print(uart)

#clear bufer in UART
#waitResp()

#sendCMD_waitResp("AT")
#sendCMD_waitRespLine("AT+RX")  #check basic parameters
#sendCMD_waitResp("AT+VERSION") #version and date
#sendCMD_waitResp("AT+NAMEHC-08")  #Name
#sendCMD_waitResp("AT+NAME?")  #Name
#sendCMD_waitResp("AT+ADDR?")  #hardware address

#sendCMD_waitResp("AT+ROLE1")  #master mode
#sendCMD_waitResp("AT+ROLE?")  
#sendCMD_waitResp("AT+CMODE0")  #connect automatically
#sendCMD_waitResp("AT+CMODE?")  
#sendCMD_waitResp("AT+BINDB0D278301E93")  #hardware address

print("running...")
print("----------")
rxData = b''
n= 0
lastChar = b''

while True:
    while uart.any() > 0: 
        #line = uart.read()      
        #print(line)
        x=uart.read(1)
        rxData+=x
        lastChar = x
        n=n+1     
        #print(lastChar)  

    if lastChar == b'\n':
        #print ("------------------" )
        #print("Total bytes = " + str(n) )
        #print ("------------------" )
        try:
            print(rxData.decode('ascii'))
        except:
            print("some weird error")
        #print(rxData)
        rxData = b''
        n= 0
        lastChar = b''

    utime.sleep(0.1)
    #uart.write(line)

