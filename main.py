from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from random import randint

from kivy.config import Config		#	Setting Window For RASPI
Config.set('graphics', 'width', '800')	#	Official Screen Size
Config.set('graphics', 'height', '480')	#	800 x 480

import os
import time

class FmRadio(Widget):
    but_time = 0 

    import fmmod as rad
    rad.start()	

    def preset_press(self,delay_sec):
        self.but_time = time.time()
        #print(self.but_time)	# Debug Statement
    

    def preset_release(self, but_id):
	print"preset release"
        print(but_id)
	#print("DeltaT = " + str((time.time()-self.but_time))) # Debug Statement
	
        if ((time.time()-self.but_time) >= 3.5):

	    if (but_id == 1):
	        self.ids.but_preset_1.text = (str(self.rad.reg.status[4]))	
		self.rad.tune(float(self.rad.reg.status[4]))
	    elif (but_id == 2):
		self.ids.but_preset_2.text = (str(self.rad.reg.status[4]))
                self.rad.tune(float(self.rad.reg.status[4]))		
	    elif (but_id == 3): 
		self.ids.but_preset_3.text = (str(self.rad.reg.status[4]))
                self.rad.tune(float(self.rad.reg.status[4]))		
	    elif (but_id == 4):
		self.ids.but_preset_4.text = (str(self.rad.reg.status[4]))
                self.rad.tune(float(self.rad.reg.status[4]))		
	    elif (but_id == 5):
		self.ids.but_preset_5.text = (str(self.rad.reg.status[4]))
                self.rad.tune(float(self.rad.reg.status[4]))
	    elif (but_id == 6):
		self.ids.but_preset_6.text = (str(self.rad.reg.status[4]))
                self.rad.tune(float(self.rad.reg.status[4]))

        else:
	    if (but_id == 1):
                if (self.ids.but_preset_1.text != "P1"):
                    self.rad.tune(float(self.ids.but_preset_1.text))
		    print"Preset Set"
            if (but_id == 2):
		if (self.ids.but_preset_2.text != "P2"):
                    self.rad.tune(float(self.ids.but_preset_2.text))
            if (but_id == 3):
		if (self.ids.but_preset_3.text != "P3"):
                    self.rad.tune(float(self.ids.but_preset_3.text))
            if (but_id == 4):
		if (self.ids.but_preset_4.text != "P4"):
                    self.rad.tune(float(self.ids.but_preset_4.text))
            if (but_id == 5):
		if (self.ids.but_preset_5.text != "P5"):
                    self.rad.tune(float(self.ids.but_preset_5.text))
            if (but_id == 6):
		if (self.ids.but_preset_6.text != "P6"):
                    self.rad.tune(float(self.ids.but_preset_6.text))

    def seekUP(self):
        self.rad.seek_up()

    def seekDN(self):
        self.rad.seek_dn()

    def exit(self, btn):
        print("Exiting")
        quit(1)

    def connect(self,):
	self.rad.start()        	

    def update_freq(self):
        self.ids.label_frequency.text = str(self.rad.reg.status[4])
        self.ids.label_mode.text = self.rad.reg.status[2]

    def update(self, DT):
        self.rad.status()
        self.update_freq()

    def update_time(self, DT):
        self.ids.label_UTC.text = time.asctime()

class FmRadioApp(App):
    def build(self):
	mainscreen = FmRadio()
	# mainscreen.functions()
	#connection = obd.OBD()
        Clock.schedule_interval(mainscreen.update, 1)
        Clock.schedule_interval(mainscreen.update_time, 1)

        return mainscreen



if __name__ == '__main__':
    FmRadioApp().run()


