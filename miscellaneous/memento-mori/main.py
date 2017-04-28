from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics','resizable',0)
from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import time
from time import strftime




death = "Saturday, 28th August 2060 - 2860963156"

class MementoMoriApp(App):

    def on_start(self):
        Clock.schedule_interval(self.update, 0)

    def update(self, nap):

        left = strftime('%H:%M:%S').split(":")
        
        self.root.ids.time.text =('[b]%02d[/b]:%02d:%02d' %
                                        ((23 - int(left[0])), 59 - int(left[1]), 59 - int(left[2])))
        t1 = time.time()
        t2 = 2860963156.0
        t3 = t2-t1
        days = int(t3) / 86400
        self.root.ids.stopwatch.text = "Days: [b]"+ str(days)+"[/b]"


if __name__ == '__main__':
    Window.size = (400, 200)
    LabelBase.register(name='Roboto',
                       fn_regular='Roboto-Thin.ttf',
                       fn_bold='Roboto-Medium.ttf')
    MementoMoriApp().run()
