from kivy.config import Config
Config.set('graphics', 'width', '960')
Config.set('graphics', 'height', '640')

from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from cirkits.EditableLabel import EditableLabel
import cirkits.Levels as Levels

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, \
    ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Line, Color

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

import boolean, Screens


presentation = Builder.load_file("cirkitbuilder.kv")

class CirkitGame(Widget):
    pass

class CirkitBuilderApp(App):
    def load_levels(self, pres):
        menu = pres.get_screen('menu')
        cirkit = pres.get_screen('cirkit')

        levels = filter(lambda x: x.startswith('get_level_'), Levels.__dict__)

        for func in levels:
            def load_level(*args):
                pres.transition.direction = 'left'
                cirkit.clear_widgets()
                Levels.__dict__[func](cirkit)
                fl = FloatLayout()
                back_button = Button(color=(0,1,0,1), font_size=25, size_hint=(0.3,0.2), text="Main Menu",
                                     pos_hint={"right":1, "bottom":1})
                def main_screen(*args):
                    pres.transition.direction = 'right'
                    pres.current = 'menu'
                back_button.bind(on_release=main_screen)
                fl.add_widget(back_button)
                cirkit.add_widget(fl)
                pres.current = 'cirkit'
            lvl_name = func[len('get_level_'):]
            lbutton = Button(text="Level %s" % lvl_name, font_size=50)
            lbutton.bind(on_release=load_level)
            menu.levels.add_widget(lbutton)

    def build(self):
        self.load_levels(presentation)
        # Clock.schedule_interval(game.update, 1.0 / 60.0)
        return presentation


if __name__ == "__main__":
    CirkitBuilderApp().run()
