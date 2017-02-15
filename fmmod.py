import RPi.GPIO as GPIO
import smbus
from time import sleep

class data():
    byte= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ### Create A Data Holder For Registers 32 bytes in Decimal Form
    ### Use HEX() to get hex values see below in display_reg() Function
    ###
    status=[0,0,0,87.5,0]	
	    # Connected 
	      # Stero / Mono
                # RDS Available
                  # Current Frequency
	           # Extra2

reset = 4	## Pin BCM 7
adr = 0x10	## i2c Address Of The Radio Module

reg = data()

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(reset, GPIO.OUT)

bus = smbus.SMBus(1)	# Instanciate The SMBUS 

def init_i2c():
    GPIO.output(reset, GPIO.LOW)
    sleep(.1)
    GPIO.output(reset, GPIO.HIGH)
    sleep(.1)
    print"Connected"
    reg.status[1] = 1


def read_reg():
    regdata = bus.read_i2c_block_data(adr,reg.byte[16],32)
    #print "Registers Updated"		# Debug Statement
    for i in range(32):
        reg.byte[i] = (regdata[i])	

def write_reg():
    tx_list = [reg.byte[17],			# 0X20
               reg.byte[18],reg.byte[19],	# 0X30
               reg.byte[20],reg.byte[21],	# 0X40
               reg.byte[22],reg.byte[23],	# 0X50
               reg.byte[24],reg.byte[25],	# 0X60
               reg.byte[26],reg.byte[27],]	# 0X70
              # reg.byte[28],reg.byte[29],	# 0X80
              # reg.byte[30],reg.byte[31],]	# 0X90
    ## Above Creates A List From The Data Class Of Decimal Values to Be Sent Out
    ## With i2c_block_write. Offset by one due to command writing to first byte of 
    ## 0x02 register ** No idea why it does this might be smbus mod or the chip
    bus.write_i2c_block_data(adr,reg.byte[16],tx_list)
    #sleep(.5)	# ** Required Delay Otherwise Radio Doesn't Start

def setup_osc():
    reg.byte[26] = 0x81

def volume(*args):				#Use *args
    if (len(args) == 0):
        reg.byte[23] = reg.byte[23] & 0xF0
        reg.byte[23] = reg.byte[23] | 0x15
    elif(args[0] <= 15):
        reg.byte[23] = reg.byte[23] & 0xF0
        reg.byte[23] = reg.byte[23] + args[0]
    else:
        print "Radio Can't Go To Eleven"


def tune(station):
    reg.station = station
    newtune = station*10-875
    reg.byte[18] = 0x00			## Clear The Tune Bit
    reg.byte[19] = int(newtune)		## Addin New Frequency
    reg.byte[16] &= 0xFE		## Clear Set Tune Clear
    write_reg()				## Write To Register
    read_reg()
    reg.byte[18] = 0x80			## Set Tune Bit High
    write_reg()				## Write To Register
    reg.byte[18] = 0x40 		## 0x00 = 87.5 // 0xCD = 108.0
    write_reg()
    read_reg()

def enable_radio():
    reg.byte[16] = 0x40
    reg.byte[17] = 0x01

def enable_spacing():
    reg.byte[20] = 0x10
    reg.byte[21] = 0x00
    reg.byte[23] |= (1<<4)
#    print(reg.byte[20] + reg.byte[21] + reg.byte[23])

def seek_up():
    # Seek UP
    # Register 0x02   Allow Wrap/Set Direction/Start Seek
    # Register 0x06   Set Min Seek Threshold/Setmin IMP threshold
    read_reg()
    reg.byte[16] = 0x46		#Clear Seek Bit
    reg.byte[18] = 0x00		#Clear Tune/Seek STC
    write_reg()
    reg.byte[16] = 0x47		# Run Seek
    write_reg()
    read_reg()

def seek_dn():
    # Seek UP
    # Register 0x02   Allow Wrap/Set Direction/Start Seek
    # Register 0x06   Set Min Seek Threshold/Setmin IMP threshold
    read_reg()
    reg.byte[16] = 0x44         #Clear Seek Bit
    reg.byte[18] = 0x00         #Clear Tune/Seek STC
    write_reg()
    reg.byte[16] = 0x45         # Run Seek
    write_reg()
    read_reg()

def status():				#Experimental [ ]
    read_reg()
    if ((reg.byte[0] & 0x01) == 1): 
        #print "Stereo"
        reg.status[2] = "STEREO"
    elif ((reg.byte[0] & 0x01 == 0)):
        #print "Mono"
        reg.status[2] = "MONO"
	
    frequency = reg.byte[3]
    reg.status[4] = .1*frequency+87.5 	# Using Reg 0x0B (LSB)
					# Decode Currrent Frequency
#    print("Freq = " + str(reg.status[4]))



def display_reg():
    #read_reg()
    print("0x00 = " + hex(reg.byte[12]) +" "+ hex(reg.byte[13]) + " CHIP")
    print("0x01 = " + hex(reg.byte[14]) +" "+ hex(reg.byte[15]) + " FIRMWARE")
    print("0x02 = " + hex(reg.byte[16]) +" "+ hex(reg.byte[17]))
    print("0x03 = " + hex(reg.byte[18]) +" "+ hex(reg.byte[19]))
    print("0x04 = " + hex(reg.byte[20]) +" "+ hex(reg.byte[21]))
    print("0x05 = " + hex(reg.byte[22]) +" "+ hex(reg.byte[23]))
    print("0x06 = " + hex(reg.byte[24]) +" "+ hex(reg.byte[25]))
    print("0x07 = " + hex(reg.byte[26]) +" "+ hex(reg.byte[27]))
    print("0x08 = " + hex(reg.byte[28]) +" "+ hex(reg.byte[29]))
    print("0x09 = " + hex(reg.byte[30]) +" "+ hex(reg.byte[31]))
    print("0x0A = " + hex(reg.byte[0])  +" "+ hex(reg.byte[1]))
    print("0x0B = " + hex(reg.byte[2])  +" "+ hex(reg.byte[3]))
    print("0x0C = " + hex(reg.byte[4])  +" "+ hex(reg.byte[5]))
    print("0x0D = " + hex(reg.byte[6])  +" "+ hex(reg.byte[7]))
    print("0x0E = " + hex(reg.byte[8])  +" "+ hex(reg.byte[9]))
    print("0x0F = " + hex(reg.byte[10]) +" "+ hex(reg.byte[11]))

    ### 	Hex Handling	####
    #
    #   test = int(reg.byte[12],16)<<8
    #   hex(tes)   
    #   Output '0x1200'
    ###

    #

    #
    #

def start():
    	#	Sequence:	1) Enable OSC
	#			2) delay(500)
	#			3) Enable Radio (REG 0x02 = 0x4001
	#			4) Enable RDS & Set Config REG 0x04
	#			5) Set Spacing 100 KHZ	(REG 0x05) 
    init_i2c()
    read_reg()
    setup_osc()
    write_reg()
    sleep(.4)		# Let Radio Settle
    read_reg()
    enable_radio()
    write_reg()
    sleep(.4)		# Let Radio Settle
    read_reg()
    enable_spacing()
    write_reg()
    sleep(.4)		# Let Radio Settle
    read_reg()
    volume()
    write_reg()
    read_reg()
    tune(94.5)


    #read_reg()

