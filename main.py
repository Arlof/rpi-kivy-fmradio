from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from random import randint

from kivy.config import Config				#	Setting Window For RASPI
Config.set('graphics', 'width', '800')		#	Official Screen Size
Config.set('graphics', 'height', '480')		#	800 x 480

import os

butttime = "69"
TEMP = "38"
MPH = "88"
RPM = "420"
INTAKETEMP = "0"

class FmRadio(Widget):
     
	

    #print(dir(connection))

    def new_mph(r):
        global MPH          #MPH
        MPH = round((r.value.magnitude*0.621371))


    def new_rpm(r):
        global RPM          #RPM
        RPM = r.value.magnitude
  
    def new_temp(r):
        global TEMP         #Coolant Temperature
        TEMP = r.value.magnitude

    def new_intaketemp(r):
        global INTAKETEMP         #Intake Temperature
        INTAKETEMP = r.value.magnitude



    def update(self,dt):
        pass

    def exit(self, btn):
        print("Exiting")
        quit(1)

    def connect(self, fuck):
        	
	if self.connection.is_connected() == True :
	    print "connected\n"
	    self.ids.but_Connect.background_color = 0,1,0,1

	if self.connection.is_connected() == False :
	    print "not connected\n"
	    self.ids.but_Connect.background_color = 1,0,0,1
    #pass

    def update(self, DT):
	# DT Variable is time called from ClockShed Task
		global butttime
		global RPM
        #self.ids.but_G1.text = str(INTAKETEMP) + "\ndegC"
		#self.ids.but_RPM.text = str(RPM) + "\nRPM"
        #self.ids.but_MPH.text = str(MPH) + "\nMPH"
        #self.ids.but_TEMP.text = " " + str(TEMP) + "\ndegC" 


#    connection.watch(obd.commands.COOLANT_TEMP, callback=new_temp)
#    connection.watch(obd.commands.RPM, callback=new_rpm)
#    connection.watch(obd.commands.SPEED, callback=new_mph)
#    connection.watch(obd.commands.INTAKE_TEMP, callback=new_intaketemp)

#    connection.start()
	

class FmRadioApp(App):
    def build(self):
	mainscreen = FmRadio()
	# mainscreen.functions()
	#connection = obd.OBD()
        Clock.schedule_interval(mainscreen.update, 1.0/60.0)

        return mainscreen



if __name__ == '__main__':
    FmRadioApp().run()


