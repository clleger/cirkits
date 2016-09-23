import kivy
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout

Config.set('graphics', 'width', '960')
Config.set('graphics', 'height', '640')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from EditableLabel import EditableLabel

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

import boolean

class AndGate(Widget):
    pass


class Wire(Line):
    def __init__(self, input_source, sink, color, **kwargs):
        super(Wire, self).__init__(**kwargs)
        print self
        self.input_source = input_source
        self.sink = sink
        self.color = color
        input_source.callbacks.append(self.state_callback)



    def state_callback(self, input, old_val, new_val):
        if new_val == old_val: return
        if new_val:
            self.color.v = self.color.v*3
        else:
            self.color.v = self.color.v/3


class BooleanOutput(GridLayout, boolean.BooleanOutput):
    led_source = StringProperty('resources/LED_off.png')

    def __init__(self, desc, **kwargs):
        GridLayout.__init__(self, **kwargs)
        self.cols = 1
        self.rows = 2
        self.desc = desc
        self.led = Image(source=self.led_source, size_hint=(.75, .75))
        self.add_widget(self.led)

        label = EditableLabel(size_hint=(1,.25))
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


class TruthTable(Widget):
    def __init__(self, op_source, **kwargs):
        super(TruthTable, self).__init__(**kwargs)
        self.op_source = op_source


def get_visualization_of_gate(op):
    images = {
        boolean.AND_BGATE.operation:Image(source='resources/AND_BGATE.png'),
        boolean.NAND_BGATE.operation:Image(source='resources/NAND_BGATE.png'),
        boolean.OR_BGATE.operation:Image(source='resources/OR_BGATE.png'),
        boolean.NOR_BGATE.operation: Image(source='resources/NOR_BGATE.png'),
        boolean.XOR_BGATE.operation: Image(source='resources/XOR_BGATE.png'),
        boolean.XNOR_BGATE.operation: Image(source='resources/XNOR_BGATE.png'),
    }
    result = images.get(op.operation)
    if not result:
         result = Label(text=str(op.__class__.__name__).split('.')[-1], font_size=20)
    return result

class BGate(BoxLayout):
    led_source = StringProperty('resources/LED_off.png')

    def __init__(self, op, **kwargs):
        super(BGate, self).__init__(**kwargs)

        self.op = op

        self.spacing = 0
        self.orientation = 'vertical'
        # layout.cols = 1
        self.rows = 3

        self.ttable = TruthTable(self, size_hint=(1, .25))
        self.led = Image(source=self.led_source, size_hint=(1, .2))
        self.gate = get_visualization_of_gate(op)
        self.gate.size_hint = (1, 0.55)

        self.add_widget(self.ttable)
        self.add_widget(self.led)
        self.add_widget(self.gate)

        op.callbacks.append(self.update_value)

    def update_value(self, op, old_val, new_val):
        if new_val:
            self.led_source = 'resources/LED_on.png'
        else:
            self.led_source = 'resources/LED_off.png'
        self.led.source = self.led_source


class ToggleInput(GridLayout, boolean.MutableBooleanInput):
    led_source = StringProperty('resources/LED_off.png')

    def __init__(self, desc, **kwargs):
        super(ToggleInput, self).__init__(**kwargs)

        if kivy.uix.layout.Layout in self.__class__.mro():
            layout = self
        else:
            layout = BoxLayout(spacing=10, orientation='vertical', rows=3, size_hint=(1,1))
            self.add_widget(layout)
        layout.spacing = 0
        layout.orientation = 'vertical'
        # layout.cols = 1
        layout.rows = 3

        self.desc = desc
        self.led = Image(source=self.led_source, size_hint=(1, .2))

        self.button = ToggleButton(size_hint=(.1,.6))
        self.button.input = self
        self.button.background_normal='resources/off.png'
        self.button.background_down='resources/on.png'

        def state_callback(button, value):
            if value == 'down':
                new_val = True
            elif value == 'normal':
                new_val = False
            button.input.set_value(new_val)

        self.button.bind(state=state_callback)
        label = EditableLabel(size_hint=(1,.2))
        label.text = desc

        layout.add_widget(self.led)
        layout.add_widget(self.button)
        layout.add_widget(label)

    # def set_value(self, new_val):
    #     self.button.state = 'down' if new_val else 'normal'

    def update_value(self, input, old_val, new_val):
        super(boolean.MutableBooleanInput, self).update_value(input, old_val, new_val)
        if new_val:
            self.led_source = 'resources/LED_on.png'
        else:
            self.led_source = 'resources/LED_off.png'
        if hasattr(self, 'led'):
            self.led.source = self.led_source

    def __bool__(self):
        button = getattr(self, 'button', None)
        if button:
            return self.button.state == 'down'
        else:
            return False
    __nonzero__ = __bool__

