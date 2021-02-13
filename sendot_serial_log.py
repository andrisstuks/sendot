# This is simple RS232 communicatoin example with  Sendot FluoMini Pro
# from Raspberry Pi4
import serial
import calendar, time
from datetime import datetime

port='/dev/ttyUSB1'
fname='/home/sendot/Desktop/sendot_log_2.txt' # File name and location, with os module you can make it nicer and smoothher
# For now in file you need to add header according to how data is written, in my case: time; eff; umol; fmin; fmax

# Basically we communicate with 19k2,8,n,0.
ser=serial.Serial(port=port,
                  baudrate=19200, # corresponfs to 19k2
                  bytesize=8, #Eight bits
                  parity=serial.PARITY_NONE, # Parity - none
                  stopbits=serial.STOPBITS_ONE, # Not sure about this one, but it works
                  timeout=1) # Timeout - good to  have to read full line with .readline

serstr="" # Creating empty string for bare readings
readings="" # Creating empty string for converted readings? from what values will be extraced

cmd=(chr(0x4D)+chr(0xA)).encode() # Creating measurement command, corresponds to M\n, as here speed is not important - if works - works.

ser.write(cmd) #Writing command to sensor

while(1):
    # Wait until there is data waiting in the serial buffer
    if(ser.in_waiting > 0): # Checks byte count

        # Read data out of the buffer until a carraige return / new line is found
        serstr = ser.readline() #reads in all data, if timeout is on 0, will read few partial lines
        daida=datetime.now().isoformat() # Sets measurement epoch
        readings=serstr.decode('Ascii') # Converts readings to pure string
        # Print the contents of the serial data if needed for checking the script output
        #print(serstr)#.decode('Ascii'))
        #print(readings)

        eff=readings.split(",")[0].strip('%E ') # Efficiency, strips unnecesary spaces and symbols
        umol=readings.split(",")[1].strip('umol ')# umol, strips spaces and symbols
        fmin=readings.split(",")[2].strip() # F min is always at the same place, so we get it
        fmax=readings.split(",")[-1].strip() # Same with F max - it should be last vale from the end
        epocht=calendar.timegm(time.strptime((daida[0:10]+' '+daida[11:19]), '%Y-%m-%d %H:%M:%S')) # Creating epoch for logging, somewhat easier for crossplatform later
        val=str(epocht)+ ";"+str(eff)+ ";"+str(umol)+ ";"+str(fmin)+ ";"+str(fmax) # Creates string for log file
        with open(fname, 'a') as ieraksti: # Creates write function
            ieraksti.writelines("%s\n" %val) # writes to file, closes at the exit
        #Print function if you want to check outputs in terminal
        #print("eff {} umol {} fmin{} fmax{}".format(eff,umol,fmin,fmax))
        break # Finishes the operation
