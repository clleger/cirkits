from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from cirkits.EditableLabel import EditableLabel
import cirkits.Levels as Levels

Config.set('graphics', 'width', '960')
Config.set('graphics', 'height', '640')

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




class CirkitGame(Widget):
    pass

class CirkitBuilderApp(App):
    def build(self):
        presentation = Builder.load_file("cirkitbuilder.kv")
        Levels.get_level_3(presentation.get_screen('cirkit'))
        # Clock.schedule_interval(game.update, 1.0 / 60.0)
        return presentation


if __name__ == "__main__":
    CirkitBuilderApp().run()
