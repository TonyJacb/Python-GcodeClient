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

        #Keeping track of the position in absolute values
        self.value_X = 0.0
        self.value_Y = 0.0

        self.__initialise("G28")
        # self.__initialise("G28 X0 Y0 Z0\r\n")
        # self.__initialise("G28 X0 Y0\r\n")
        # self.__initialise("G28 X0\r\n")
        # self.__initialise("G28 Y0\r\n")
        # self.__initialise("G28 Z0\r\n")

        # Extruder Temp
        # self.__initialise("M104 S190 T0\r\n") #  start heating T0 to 190 degrees Celsius
        # self.__initialise("G28\r\n") # Home
        # self.__initialise("M109 S190 T0\r\n") # wait for T0 to reach 190 degrees before continuing with any other self.commands

        # Bed Temp
        # self.__initialise("M140 S55\r\n") # heat bed to 50 degrees celsius but do not wait
        # self.__initialise("G28\r\n") # Home
        # self.__initialise("M190 S55\r\n") # wait for bed to heat to 50 degrees celsius and wait

        # Fan
        # self.__initialise("M106 S255\r\n") # fan speed full
        # self.__initialise("M106 S127\r\n") # fan speed about half
        # self.__initialise("M106 S0\r\n") # turn off fan

        # Set Units(does not seem to work on ender 5)
        # self.__initialise("G20\r\n") # inches
        self.__initialise("G21") # millimeters

        # Absolute Mode
        # self.__initialise("G90\r\n")

        # Relative Mode
        self.__initialise("G91\r\n")

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
            cmd = cmd.upper()
            subcmds = cmd.split(" ")
            for subcmd in subcmds:
                if subcmd[0] == "X":
                    self.value_X += float(subcmd[1:])
                elif subcmd[0] == "Y":
                    self.value_Y += float(subcmd[1:])
            print(f'Value of X: {self.value_X}, y:{self.value_Y}')
            cmd = cmd + "\r\n"
            self.ser.write(str.encode(cmd))
            time.sleep(1)
            while True:
                feedback = self.ser.readline()
                if feedback == b'ok\r\n':
                    # print(feedback)
                    break
        except TypeError:
            print("Gcode commands must be a string")


    def __initialise(self, cmd):
        '''
        Same as that of command but for initialisation. Used in the constructor.
        '''
        cmd = cmd + "\r\n"
        self.ser.write(str.encode(cmd))
        time.sleep(1)
        while True:
            feedback = self.ser.readline()
            if feedback == b'ok\r\n':
                # print(feedback)
                break

    def flush(self):
        '''
        Use this function to close the serial port.
        '''
        time.sleep(2)
        self.ser.close()
        quit()

    def manual_mode(self):
        '''
        Use this for sending one command at a time.
        '''
        while True:
            string = input("Enter your Gcode: ")
            string = string.upper()
            print(string)
            if string == "Q":
                self.flush()
            
            else:
                self.command(string)
