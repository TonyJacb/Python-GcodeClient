import serial
import time

#Inspired from 
#https://kevinponce.com/blog/python/send-gcode-through-serial-to-a-3d-printer-using-python/

class Client:
    def __init__(self, port, baud) -> None:
        '''
        Initialises the serial port and wakes up GRBL with desired settings.
        :param port: specify the port to which your printer is connected.
                    If it is an Arduino CNC shield, check the port from Arduino IDE
        :param baud: specify the baudrate at which GRBL is communicating. 
        '''
        self.ser = serial.Serial(port, baud)
        time.sleep(2)

        self.command("G28")
        # self.command("G28 X0 Y0 Z0\r\n")
        # self.command("G28 X0 Y0\r\n")
        # self.command("G28 X0\r\n")
        # self.command("G28 Y0\r\n")
        # self.command("G28 Z0\r\n")

        # Extruder Temp
        # self.command("M104 S190 T0\r\n") #  start heating T0 to 190 degrees Celsius
        # self.command("G28\r\n") # Home
        # self.command("M109 S190 T0\r\n") # wait for T0 to reach 190 degrees before continuing with any other self.commands

        # Bed Temp
        # self.command("M140 S55\r\n") # heat bed to 50 degrees celsius but do not wait
        # self.command("G28\r\n") # Home
        # self.command("M190 S55\r\n") # wait for bed to heat to 50 degrees celsius and wait

        # Fan
        # self.command("M106 S255\r\n") # fan speed full
        # self.command("M106 S127\r\n") # fan speed about half
        # self.command("M106 S0\r\n") # turn off fan

        # Set Units(does not seem to work on ender 5)
        # self.command("G20\r\n") # inches
        self.command("G21") # millimeters

        # Absolute Mode
        # self.command("G90\r\n")

        # Relative Mode
        self.command("G91\r\n")

        # Move
        # self.command("G0 X7 Y18\r\n") # rapid motion but does not extrude material
        # self.command("G0 X350 Y350\r\n") # rapid motion but does not extrude material ender 5 plus is 350 x 350
        # self.command("G1 Z0.345 F500\r\n") # change layer
        # self.command("G0 X50 Y50\r\n") # rapid motion but does not extrude material ender 5 plus is 350 x 350

    def command(self, cmd):
        '''
        Interfaces the Gcode commands to GRBL
        :param cmd:  A Gcode String.
        '''
        try:   
            cmd = cmd + "\r\n"
            self.ser.write(str.encode(cmd))
            time.sleep(1)
            while True:
                feedback = self.ser.readline()
                if feedback == b'ok\r\n':
                    break
        except TypeError:
            print("Gcode commands must be a string")

    def flush(self):
        '''
        Use this function at the end of script. It closes the serial port.
        '''
        time.sleep(2)
        self.ser.close()