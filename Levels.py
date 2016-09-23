from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout

import boolean
from widgets import BooleanOutput, ToggleInput, Wire, BGate, UGate
from kivy.graphics import Line, Color

def create_binary_level(operation, input1_default=False, input2_default=False):
    def get_binary_level(widget):
        input1 = ToggleInput("Input 0")#, size_hint=(0.2, 0.2), pos_hint={'x':50, 'y':300})
        input1.size_hint = (50./960, 175./640)
        input1.center = (100, 480)
        widget.add_widget(input1)
        input1.button.state = 'down' if input1_default else 'normal'

        input2 = ToggleInput("Input 1", size_hint=(50./960, 175./640), center=(100, 180))#{'x':70, 'y':125})
        # input2.size = (50, 200)
        # input2.center = (100, 200)
        widget.add_widget(input2)
        input2.button.state = 'down' if input2_default else 'normal'

        output = BooleanOutput("Output 0")
        output.size_hint = (100./960, 120./640)
        output.center = (800, 340)
        widget.add_widget(output)

        op = operation(input1, input2, output)
        gate = BGate(op, size_hint=(200./960, 175./640))
        gate.center = (400, 360)
        widget.add_widget(gate)

        with widget.canvas:
            c1 = Color(0, 0.9, 0.3 if not input1 else 0.9, mode='hsv')
            line_width = 5.
            line_1G = Wire(input1, op, c1, points=(160, 500), width=line_width, joint='round')
            line_1G.points += [250, 500]
            line_1G.points += [250, 385]
            line_1G.points += [350, 385]

            c2 = Color(5. / 7, 0.9, 0.3 if not input2 else 0.9, mode='hsv')
            line_2G = Wire(input2, op, c2, points=(160, 200), width=line_width, joint='round')
            line_2G.points += [250, 200]
            line_2G.points += [250, 335]
            line_2G.points += [350, 335]

            c3 = Color(0.22, 0.22, 0.22)
            line_GO = Wire(op, output, c3, points=(575, 360), width=line_width * 1.5)
            line_GO.points += [725, 360]
        # self.button.state = 'down' if new_val else 'normal'
        # input2.set_value(input2_default)
    return get_binary_level

get_level_1 = create_binary_level(boolean.INPUT0_BGATE, False, False)
get_level_2 = create_binary_level(boolean.INPUT1_BGATE, False, False)
get_level_3 = create_binary_level(boolean.AND_BGATE, False, False)
get_level_4 = create_binary_level(boolean.OR_BGATE, False, False)
get_level_5 = create_binary_level(boolean.XOR_BGATE, False, False)
get_level_6 = create_binary_level(boolean.XNOR_BGATE, True, False)
get_level_8 = create_binary_level(boolean.NAND_BGATE, True, True)
get_level_9 = create_binary_level(boolean.NOR_BGATE, True, True)


def get_level_C1(widget):
    input1_default = True
    input2_default = True

    input1 = ToggleInput("Input 0")  # , size_hint=(0.2, 0.2), pos_hint={'x':50, 'y':300})
    input1.size_hint = (50. / 960, 175. / 640)
    input1.center = (100, 480)
    widget.add_widget(input1)
    input1.button.state = 'down' if input1_default else 'normal'

    input2 = ToggleInput("Input 1", size_hint=(50. / 960, 175. / 640), center=(100, 180))  # {'x':70, 'y':125})
    # input2.size = (50, 200)
    # input2.center = (100, 200)
    widget.add_widget(input2)
    input2.button.state = 'down' if input2_default else 'normal'

    out2 = BooleanOutput("Output 1")
    out2.size_hint = (100. / 960, 120. / 640)
    out2.center = (800, 340)
    widget.add_widget(out2)

    op = boolean.AND_BGATE(input1, input2, None)
    gate = BGate(op, size_hint=(200. / 960, 175. / 640))
    gate.center = (300, 360)
    widget.add_widget(gate)

    op2 = boolean.INVERTER_UGATE(op, out2)
    gate2 = UGate(op2, size_hint=(200. /960, 175./ 640))
    gate2.center = (500, 360)
    widget.add_widget(gate2)

    with widget.canvas:
        c1 = Color(0, 0.9, 0.3 if not input1 else 0.9, mode='hsv')
        line_width = 5.
        line_1G = Wire(input1, op, c1, points=(150, 500), width=line_width, joint='round')
        line_1G.points += [200, 500]
        line_1G.points += [200, 385]
        line_1G.points += [250, 385]

        c2 = Color(5. / 7, 0.9, 0.3 if not input2 else 0.9, mode='hsv')
        line_2G = Wire(input2, op, c2, points=(150, 200), width=line_width, joint='round')
        line_2G.points += [200, 200]
        line_2G.points += [200, 335]
        line_2G.points += [250, 335]

        c3 = Color(0, 0, 0.22 if not op else 0.66, mode='hsv')
        line_GO = Wire(op, op2, c3, points=(415, 360), width=line_width * 1.5)
        line_GO.points += [500, 360]

        c4 = Color(0, 0, 0.22 if not op2 else 0.66, mode='hsv')
        line_GO2 = Wire(op2, out2, c4, points=(650, 360), width=line_width * 1.5)
        line_GO2.points += [725, 360]
        # self.button.state = 'down' if new_val else 'normal'
        # input2.set_value(input2_default)

def get_level_C2(widget):
    input1_default = False
    input2_default = False

    input1 = ToggleInput("Input 0")  # , size_hint=(0.2, 0.2), pos_hint={'x':50, 'y':300})
    input1.size_hint = (50. / 960, 175. / 640)
    input1.center = (100, 480)
    widget.add_widget(input1)
    input1.button.state = 'down' if input1_default else 'normal'

    inv1 = boolean.INVERTER_UGATE(input1, None)
    inn1 = UGate(inv1, size_hint=(200./ 960, 175./ 640))
    inn1.center = (170, 500)
    widget.add_widget(inn1)

    input2 = ToggleInput("Input 1", size_hint=(50. / 960, 175. / 640), center=(100, 180))  # {'x':70, 'y':125})
    # input2.size = (50, 200)
    # input2.center = (100, 200)
    widget.add_widget(input2)
    input2.button.state = 'down' if input2_default else 'normal'

    inv2 = boolean.INVERTER_UGATE(input2, None)
    inn2 = UGate(inv2, size_hint=(200./ 960, 175./ 640))
    inn2.center = (170, 200)
    widget.add_widget(inn2)

    out2 = BooleanOutput("Output 1")
    out2.size_hint = (100. / 960, 120. / 640)
    out2.center = (800, 340)
    widget.add_widget(out2)

    op = boolean.AND_BGATE(inn1.op, inn2.op, None)
    gate = BGate(op, size_hint=(200. / 960, 175. / 640))
    gate.center = (440, 360)
    widget.add_widget(gate)

    op2 = boolean.INVERTER_UGATE(op, out2)
    gate2 = UGate(op2, size_hint=(200. /960, 175./ 640))
    gate2.center = (600, 360)
    widget.add_widget(gate2)

    with widget.canvas:
        line_width = 5.

        c1 = Color(0, 0.9, 0.3 if not input1 else 0.9, mode='hsv')
        line_1G = Wire(input1, inv1, c1, points=(150, 500), width=line_width, joint='round')
        line_1G.points += [160, 500]

        ci1 = Color(0, 0.9, 0.3 if not inv1 else 0.9, mode='hsv')
        line_1G = Wire(inv1, op, ci1, points=(305, 500), width=line_width, joint='round')
        line_1G.points += [335, 500]
        line_1G.points += [335, 385]
        line_1G.points += [375, 385]

        c2 = Color(5. / 7, 0.9, 0.3 if not input2 else 0.9, mode='hsv')
        line_2G = Wire(input2, inv2, c2, points=(150, 200), width=line_width, joint='round')
        line_2G.points += [160, 200]

        ci2 = Color(5. / 7, 0.9, 0.3 if not inv2 else 0.9, mode='hsv')
        line_2G = Wire(inv2, op, ci2, points=(305, 200), width=line_width, joint='round')
        line_2G.points += [335, 200]
        line_2G.points += [335, 335]
        line_2G.points += [375, 335]

        c3 = Color(0, 0, 0.22 if not op else 0.66, mode='hsv')
        line_GO = Wire(op, op2, c3, points=(555, 360), width=line_width * 1.5)
        line_GO.points += [600, 360]

        c4 = Color(0, 0, 0.22 if not op2 else 0.66, mode='hsv')
        line_GO2 = Wire(op2, out2, c4, points=(730, 360), width=line_width * 1.5)
        line_GO2.points += [750, 360]
        # self.button.state = 'down' if new_val else 'normal'
        # input2.set_value(input2_default)


# __all__ = (get_level_2, get_level_3)
