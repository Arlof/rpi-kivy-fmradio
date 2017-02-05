from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from random import randint

from kivy.config import Config				#	Setting Window For RASPI
Config.set('graphics', 'width', '800')		#	Official Screen Size
Config.set('graphics', 'height', '480')		#	800 x 480

import os
import time



class FmRadio(Widget):
    import fmmod as rad
    rad.start()	
    def seekUP(self):
        self.rad.seek_up()

    def seekDN(self):
        self.rad.seek_dn()

    def exit(self, btn):
        print("Exiting")
        quit(1)

    def connect(self, fuck):
	self.rad.start()        	

    def update_freq(self):
        self.ids.label_frequency.text = str(self.rad.reg.status[4])

    def update(self, fuck):
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


