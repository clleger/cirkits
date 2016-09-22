from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from cirkits.EditableLabel import EditableLabel

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

from cirkits import boolean

class AndGate(Widget):
    pass


class Wire(Line):
    def __init__(self, source, sink, color, **kwargs):
        super(Wire, self).__init__(**kwargs)
        print self
        self.source = source
        self.sink = sink
        self.color = color
        source.callbacks.append(self.state_callback)



    def state_callback(self, input, old_val, new_val):
        if new_val:
            self.color.s = self.color.s - .3
        else:
            self.color.s = self.color.s + .3

class BooleanOutput(GridLayout, boolean.BooleanOutput):
    led_source = StringProperty('resources/LED_off.png')

    def __init__(self, desc, **kwargs):
        GridLayout.__init__(self, **kwargs)
        self.cols = 1
        self.rows = 2
        self.desc = desc
        self.led = Image(source=self.led_source, size_hint=(.75, .75))
        self.add_widget(self.led)

        label = EditableLabel(size_hint=(.25,.25))
        label.text = desc
        self.add_widget(label)


    def update_value(self, input, old_val, new_val):
        boolean.BooleanOutput.update_value(self, input, old_val, new_val)
        print "And I'm here"
        if new_val:
            self.led_source = 'resources/LED_on.png'
        else:
            self.led_source = 'resources/LED_off.png'
        self.led.source = self.led_source


class ToggleInput(GridLayout, boolean.MutableBooleanInput):
    led_source = StringProperty('resources/LED_off.png')

    def __init__(self, desc, **kwargs):
        GridLayout.__init__(self, **kwargs)
        boolean.MutableBooleanInput.__init__(self)
        self.cols = 1
        self.rows = 3
        self.desc = desc
        self.led = Image(source=self.led_source, size_hint=(.15, .15))
        self.add_widget(self.led)
        self.button = ToggleButton(size_hint=(.65,.65))
        self.button.input = self
        self.button.background_normal='resources/off.png'
        self.button.background_down='resources/on.png'

        def state_callback(button, value):
            if value == 'down':
                new_val = True
            elif value == 'normal':
                new_val = False
            button.input.update_value(None, not new_val, new_val)

        self.button.bind(state=state_callback)
        self.add_widget(self.button)
        label = EditableLabel(size_hint=(.2,.2))
        label.text = desc
        self.add_widget(label)

    def update_value(self, input, old_val, new_val):
        super(boolean.MutableBooleanInput, self).update_value(input, old_val, new_val)
        if new_val:
            self.led_source = 'resources/LED_on.png'
        else:
            self.led_source = 'resources/LED_off.png'
        self.led.source = self.led_source

    def __bool__(self):
        button = getattr(self, 'button', None)
        if button:
            return self.button.state == 'down'
        else:
            return False
    __nonzero__ = __bool__


class BGate(Widget):
    def __init__(self, in1, in2, out, op, **kwargs):
        super(BGate, self).__init__(**kwargs)

