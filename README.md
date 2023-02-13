# Bluetooth remote controller

## Intro

## Schematics

## Parts

- Pi Pico H board
- 2 Joysticks modules
- PCF8591 (ADC mux - I2C)
- HC-08 (bluetooth)
- TP4056 (USB-C Lipo charger with protection)
- 18650 Lipo 3.7V

## Communication Protocol
- Left button
  - Lx: M/L/R\n
  - Ly: M/U/D\n
  - Lb: 0/1\n
- Right button
  - Rx: M/L/R\n
  - Ry: M/U/D\n
  - Rb: 0/1\n
  
  
## Config & Usage

Obtain hardware address doing a AT+ADDR?
This address will be imported in the master device (robot) to bind the devices together.
When both devices start, they connect automatically and the controller begins to send data continously, using the communication protocol described above.
PCF8591 has a resolution 2<sup>8</sup> as opposed to 2<sup>16</sup> from using ADC pin directly.  However this is a concern as the controller doesn't return any numerical value, only the direction of the move on X and Y axis.  Buttons clicks are also tracked.

 
## 3D files
