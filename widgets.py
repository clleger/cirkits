import kivy
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from kivy.graphics.vertex_instructions import Rectangle

Config.set('graphics', 'width', '960')
Config.set('graphics', 'height', '640')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from EditableLabel import EditableLabel
from BorderBehavior import BorderBehavior
import math

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

        self.label = label = EditableLabel(size_hint=(1,.25))
        label.text = desc
        self.add_widget(label)


    def update_value(self, input, old_val, new_val):
        boolean.BooleanOutput.update_value(self, input, old_val, new_val)
        # print "Updating output {}".format(self.label.text)
        if new_val:
            self.led_source = 'resources/LED_on.png'
        else:
            self.led_source = 'resources/LED_off.png'
        self.led.source = self.led_source

    def __str__(self):
        return "Mutable Output ({})".format(getattr(self,'desc','Untitled'))


class TruthTable(Widget):
    def __init__(self, op_source, **kwargs):
        super(TruthTable, self).__init__(**kwargs)
        self.op_source = op_source


def get_visualization_of_bgate(op):
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
         result = Label(text=boolean.get_name_of_bgate(op.operation), font_size=20)
    return result

def get_visualization_of_ugate(op):
    images = {
        boolean.BUFFER_UGATE.operation:Image(source='resources/BUFFER_UGATE.png'),
        boolean.INVERTER_UGATE.operation:Image(source='resources/INVERTER_UGATE.png'),
    }
    result = images.get(op.operation)
    if not result:
         result = Label(text=boolean.get_name_of_ugate(op.operation), font_size=20)
    return result

class BGate(BoxLayout):
    led_source = StringProperty('resources/LED_off.png')

    def __init__(self, op, **kwargs):
        super(BGate, self).__init__(**kwargs)

        self.op = op

        self.spacing = 0
        self.replaceable = False
        self.orientation = 'vertical'
        # layout.cols = 1
        self.rows = 3

        self.ttable = TruthTable(self, size_hint=(1, .25))
        self.led = Image(source=self.led_source, size_hint=(1, .2))
        self.gate = get_visualization_of_bgate(op)
        self.gate.size_hint = (1, 0.55)

        self.add_widget(self.ttable)
        self.add_widget(self.led)
        self.add_widget(self.gate)

        op.callbacks.append(self.update_value)
        self.update_value(op, None, bool(op))

    def on_touch_down(self, touch):
        if self.replaceable and self.collide_point(*touch.pos):
            chooser = GridLayout(rows=4, cols=4, size_hint=(1,1))
            dummy = type("dummy", (object,), dict(operation=None))
            popup = Popup(title='Replace gate', content=chooser,
                          #auto_dismiss=False,
                          size_hint=(0.4, 0.4), center=(self.center))
            for op in range(16):
                dummy.operation = op
                widget = get_visualization_of_bgate(dummy)
                button = Button(size_hint=(1,1), text=boolean.get_name_of_bgate(op))
                layout = FloatLayout()
                layout.add_widget(widget)
                widget.pos_hint = {"center_x":0.5, "center_y":0.5}
                button.add_widget(layout)
                chooser.add_widget(button)
                # def update(*largs, **kwargs):
                #     print "Updating size/pos of operation %d" % op
                #     widget.size = button.size
                #     widget.center = button.center
                # button.on_pos = button.on_size = update
                def choose_op(op=op, *largs):
                    self.op._update_table(op)
                    self.remove_widget(self.gate)
                    self.gate = get_visualization_of_bgate(self.op)
                    self.gate.size_hint = (1, 0.55)
                    self.add_widget(self.gate)
                    popup.dismiss(force=True)
                button.on_press = choose_op
            popup.attach_to = self
            popup.open()

        return super(BGate, self).on_touch_down(touch)

    def update_value(self, op, old_val, new_val):
        if new_val:
            self.led_source = 'resources/LED_on.png'
        else:
            self.led_source = 'resources/LED_off.png'
        self.led.source = self.led_source

    def set_output(self, out):
        self.op.set_output(out)

class UGate(BoxLayout):
    led_source = StringProperty('resources/LED_off.png')

    def __init__(self, op, **kwargs):
        super(UGate, self).__init__(**kwargs)

        self.op = op

        self.spacing = 0
        self.orientation = 'vertical'
        # layout.cols = 1
        self.rows = 3

        self.ttable = TruthTable(self, size_hint=(1, .25))
        self.led = Image(source=self.led_source, size_hint=(1, .2))
        self.gate = get_visualization_of_ugate(op)
        self.gate.size_hint = (1, 0.55)

        self.add_widget(self.ttable)
        self.add_widget(self.led)
        self.add_widget(self.gate)

        op.callbacks.append(self.update_value)
        self.update_value(op, None, bool(op))

    def update_value(self, op, old_val, new_val):
        if new_val:
            self.led_source = 'resources/LED_on.png'
        else:
            self.led_source = 'resources/LED_off.png'
        self.led.source = self.led_source

    def set_output(self, out):
        self.op.set_output(out)

class NumberDisplay(GridLayout, BorderBehavior):
    int_value = NumericProperty(0)

    class NumberBit(boolean.MutableBooleanInput, boolean.BooleanOutput):
        def __init__(self, owner, index):
            self.owner = owner
            self.index = index

            boolean.MutableBooleanInput.__init__(self)
            boolean.BooleanOutput.__init__(self)

            self.callbacks.append(self.owner.update_value)

        # From BooleanOutput
        def connect(self, input):
            boolean.BooleanOutput.connect(self, input)
            self.owner.connect(input, self.index)

        # From BooleanOutput
        def disconnect(self, input):
            boolean.BooleanOutput.disconnect(self, input)
            self.owner.disconnect(input, self.index)

        def __str__(self):
            return "{}.{}".format(self.owner, self.index)

    def __init__(self, bits_in, desc, **kwargs):
        self.base = 10
        self.num_bits = bits_in

        super(NumberDisplay, self).__init__(**kwargs)

        if kivy.uix.layout.Layout in self.__class__.mro():
            layout = self
        else:
            layout = BoxLayout(spacing=10, orientation='vertical', rows=3, size_hint=(1,1))
            self.add_widget(layout)
        self.borders = (1, 'solid', (1, 1, 1, 1))
        self.display = EditableLabel(size_hint=(1, 0.75), font_name='DroidSansMono', bcolor=(0,1,0,1), halign='right',
                                     font_size=68, )

        def on_text_validate(instance):
            if instance.text:
                # print "Being called now with input '{}'".format(instance.text)
                print 'Old display text was "{}"'.format(self.display.text)
                try:
                    prev_value = int(self)
                    int_value = int(instance.text, self.base)
                    print "testing int value '{}'".format(int_value)
                    if 0 <= int_value < 2**self.num_bits:
                        print "setting int_value to {}".format(int_value)
                        self.int_value = int_value
                except:
                    pass
                self.update_value(self.display, prev_value, self.int_value)
                self.display.edit = False
                self.display.text = self.get_value_string(int(self))
                print 'New display text is  "{}"'.format(self.display.text)
        def cancel(instance, focus):
            if not focus: self.display.edit = False

        self.display.on_text_validate = on_text_validate
        self.display.on_text_focus = cancel
        # self.display.bcolor = (0, 0.7, 0, 1)
        self.display.color = (1, 0.2, 0.2, 1)
        self.display.text = self.get_value_string(0)
        self.display.strip = False
        self.bits = [self.NumberBit(self, x) for x in range(self.num_bits)]
        layout.add_widget(self.display)

        self.base_in = boolean.BooleanOutput()
        self.base_in.update_value = self.update_base

        label = EditableLabel(size_hint=(1, .2))
        self.desc = desc
        self.label = label
        self.label.text = "{} ({})".format(desc, boolean.base_to_str(self.base))
        layout.add_widget(label)

    def on_size(self, instance, value):
        self.draw_display_background(instance)
    on_pos = on_size


    def render(self):
        self.canvas.clear()
        self.canvas.add(Color(0.33, 1, 0.3, mode='hsv'))

    def draw_display_background(self, display):
        if not hasattr(self, 'display'): return
        display.canvas.before.clear()
        with display.canvas.before:
            num_width = 40
            Color(0.33, 1, 0.3, mode='hsv')
            print "Calling display background for pos %s and size %s" % (display.pos, display.size)
            width = display.width if True else num_width * self.num_bits
            Rectangle(pos=(display.pos), size=(width, display.height))
            Color(0, 0, 0)
            stride = num_width #int(self.display.width*2./5)
            for x in xrange(int(display.x),int(display.x+width),stride):
                print "Drawing new line from (%d,%d) - (%d,%d)" % (x, display.y, x, display.y+display.height)
                Line(width=5, points=((x, display.y), (x, display.y + display.height)))
                Rectangle(pos=(x, display.y), size=(1, display.height))

    def connect(self, input, index):
        # TODO: Ultimately I want the text field to be able to edit any bits that aren't fixed
        # self.display.editable = not self.inputs
        self.display.text = self.get_value_string(int(self))

    def disconnect(self, input, index):
        # TODO: Ultimately I want the text field to be able to edit any bits that aren't fixed
        # self.display.editable = not self.inputs
        self.display.text = self.get_value_string(int(self))

    def get_value_string(self, value):
        value_str = boolean.str_base(value, self.base)
        min_size = self.num_bits
        padding = " "
        if (self.base == 2):
            padding = "0"
        value_str = padding * (min_size - len(value_str)) + value_str
        return value_str

    def update_value(self, input, old_val, new_val):
        disp = getattr(self, 'display', None)
        if disp and input is disp:
            old_bin = '{:0>{bits}}'.format(bin(old_val)[2:], bits=self.num_bits)
            new_bin = '{:0>{bits}}'.format(bin(new_val)[2:], bits=self.num_bits)
            for (bit,old_bit,new_bit) in zip(reversed(self.bits),old_bin,new_bin):
                bit.update_value(self, bool(int(old_bit)), bool(int(new_bit)))
        else:
            old_val = self.int_value
            new_val = int(self)

        if disp:
            disp.text = self.get_value_string(new_val)

    def update_base(self, input, old_val, new_val):
        self.base = 10 if new_val else 2
        self.update_value(None, old_val, new_val)
        self.label.text = "{} ({})".format(self.desc, boolean.base_to_str(self.base))

    def __int__(self):
        value = 0
        if not getattr(self, 'bits', None):
            return self.int_value
        for input in reversed(getattr(self, 'bits', [])):
            value = value * 2 + int(bool(input))
        return value

    def __str__(self):
        return "Numeric Display ({})".format(getattr(self,'desc','Untitled'))


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

    def __str__(self):
        return "Toggle Input ({})".format(getattr(self,'desc','Untitled'))


