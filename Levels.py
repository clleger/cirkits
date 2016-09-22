from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout

from cirkits import boolean
from cirkits.widgets import BooleanOutput, ToggleInput, Wire, BGate
from kivy.graphics import Line, Color

def get_level_3(widget):
    input1 = ToggleInput("Input 1")#, size_hint=(0.2, 0.2), pos_hint={'x':50, 'y':300})
    input1.size_hint = (50./960, 175./640)
    input1.center = (100, 480)
    widget.add_widget(input1)

    input2 = ToggleInput("Input 2", size_hint=(50./960, 175./640), center=(100, 180))#{'x':70, 'y':125})
    # input2.size = (50, 200)
    # input2.center = (100, 200)
    widget.add_widget(input2)

    output = BooleanOutput("Output 1")
    output.size_hint = (100./960, 120./640)
    output.center = (800, 340)
    widget.add_widget(output)

    op = boolean.XOR_BGATE(input1, input2, output)

    with widget.canvas:
        c1 = Color(0, 0.6, 0.8, mode='hsv')
        line_width = 5.
        line_1G = Wire(input1, op, c1, points=(160, 500), width=line_width, joint='round')
        line_1G.points += [250, 500]
        line_1G.points += [250, 385]
        line_1G.points += [275, 385]

        c2 = Color(5. / 7, 0.6, 0.8, mode='hsv')
        line_2G = Wire(input2, op, c2, points=(160, 200), width=line_width, joint='round')
        line_2G.points += [250, 200]
        line_2G.points += [250, 335]
        line_2G.points += [275, 335]

        c3 = Color(0.5, 0, 0)
        line_GO = Wire(op, output, c3, points=(375, 360), width=line_width * 2)
        line_GO.points += [725, 360]

def get_level_2(widget):
    input1 = ToggleInput("Input 1")#, size_hint=(0.2, 0.2), pos_hint={'x':50, 'y':300})
    input1.size_hint = (50./960, 175./640)
    input1.center = (100, 480)
    widget.add_widget(input1)

    input2 = ToggleInput("Input 2", size_hint=(50./960, 175./640), center=(100, 180))#{'x':70, 'y':125})
    # input2.size = (50, 200)
    # input2.center = (100, 200)
    widget.add_widget(input2)

    output = BooleanOutput("Output 1")
    output.size_hint = (100./960, 120./640)
    output.center = (800, 340)
    widget.add_widget(output)

    op = boolean.AND_BGATE(input1, input2, output)

    with widget.canvas:
        c1 = Color(0, 0.6, 0.8, mode='hsv')
        line_width = 5.
        line_1G = Wire(input1, op, c1, points=(160, 500), width=line_width, joint='round')
        line_1G.points += [250, 500]
        line_1G.points += [250, 385]
        line_1G.points += [275, 385]

        c2 = Color(5. / 7, 0.6, 0.8, mode='hsv')
        line_2G = Wire(input2, op, c2, points=(160, 200), width=line_width, joint='round')
        line_2G.points += [250, 200]
        line_2G.points += [250, 335]
        line_2G.points += [275, 335]

        c3 = Color(0.5, 0, 0)
        line_GO = Wire(op, output, c3, points=(375, 360), width=line_width * 2)
        line_GO.points += [725, 360]

    
__all__ = (get_level_2, get_level_3)