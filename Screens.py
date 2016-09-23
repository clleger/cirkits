from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, FadeTransition, Screen
from kivy.uix.textinput import TextInput

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

class ScreenManagement(ScreenManager):
    pass

class MenuScreen(Screen):
    pass


class CirkitScreen(Screen):
    pass
