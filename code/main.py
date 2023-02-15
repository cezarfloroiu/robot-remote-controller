'''
    Bluetooth controller
    Protocol:
        Right button:
            Rx:M/L/R\n
            Ry:M/U/D\n
            Rb:1/0\n
        Left button:
            Lx:M/L/R\n
            Ly:M/U/D\n
            Lb:1/0\n
        Legend:
            M = middle
            L = left
            R = right
            U = up
            D = down
'''

from machine import Pin, ADC
import utime
from pcf8591 import PCF8591

ledBoard = Pin(25, Pin.OUT)
buttonR = Pin(6,Pin.IN, Pin.PULL_UP)
buttonL = Pin(7,Pin.IN, Pin.PULL_UP)

ledBoard.off()

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
            
addr = 0x48
# Initialize PCF8591 via I2C 
i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq=400000)
#print (i2c.scan())
p = PCF8591(i2c, 72, True)
#print(p)

#init bluetooth
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(12), rx=machine.Pin(13))
print(uart)

waitResp()

utime.sleep(0.5)
sendCMD_waitResp("AT")
#sendCMD_waitRespLine("AT+RX")  #check basic parameters
#sendCMD_waitResp("AT+NAMEMIMIC-CONTROLLER")  #Name
#sendCMD_waitResp("AT+NAME?")  #Name
#sendCMD_waitResp("AT+ADDR?")  #hardware address

# turn on the led to show working status
ledBoard.on()

while True:

    # resolutions of PCF8591 is 256 , while resolution of joystick is 655536
    # consider mid is 256/2 = 128
    # consider movement if <=100 and >= 156(from mid took 28 both ways
    msgUart = ""
    
    #Right Button
    bRStatus = 0
    xRStatus = "M" #middle
    yRStatus = "M" #middle
    
    bRValue = buttonR.value()
    if bRValue == 0:
        bRStatus =1

    xRValue = p.read(0)
    #print('RB X ' + str(data))
    yRValue = p.read(1)
    #print('RB Y ' + str(data))
    
    if xRValue <= 100:
        xRStatus = "L" #left
    elif xRValue >= 156:
        xRStatus = "R" #right
    if yRValue <= 100:
        yRStatus = "U" #up
    elif yRValue >= 156:
        yRStatus = "D" #down
    
    print("Right Button ... X: " + xRStatus + ", Y: " + yRStatus + ", Click: " + str(bRStatus))
    msgUart += "Rx:" + xRStatus + "\n"
    msgUart += "Ry:" + yRStatus + "\n"
    msgUart += "Rb:" + str(bRStatus) + "\n"

    #uart.write("Rx:" + xRStatus + "\n")
    #uart.write("Ry:" + yRStatus + "\n")

    #Left button
    bLStatus = 0
    xLStatus = "M"
    yLStatus = "M"
    
    bLValue = buttonL.value()
    if bLValue == 0:
        bLStatus =1
        
    xLValue = p.read(2)
    #print('LB X ' + str(data))
    yLValue = p.read(3)
    #print('LB Y ' + str(data))
    
    
    if xLValue >=156:
        xLStatus = "L" #left
    elif xLValue <= 100:
        xLStatus = "R" #right
    if yLValue >= 156:
        yLStatus = "U" #up
    elif yLValue <= 100:
        yLStatus = "D" #down
    print("Left Button ... X: " + xLStatus + ", Y: " + yLStatus + ", Click: " + str(bLStatus))

    #uart.write("Lx:" + xLStatus + "\n")
    #uart.write("Ly:" + yLStatus + "\n")
    msgUart += "Lx:" + xLStatus + "\n"
    msgUart += "Ly:" + yLStatus + "\n"
    msgUart += "Lb:" + str(bLStatus) + "\n"

    # send positions
    uart.write(msgUart) 

    # short delay
    utime.sleep(0.1)

ledBoard.off()
