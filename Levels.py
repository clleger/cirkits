from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout

import boolean
from widgets import BooleanOutput, ToggleInput, Wire, BGate, UGate, NumberDisplay
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

def get_level_C3(widget):
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

    Y = boolean.AND_BGATE(inn1.op, inn2.op, None)
    gateY = BGate(Y, size_hint=(200. / 960, 175. / 640))
    gateY.center = (440, 500)
    widget.add_widget(gateY)

    Z = boolean.AND_BGATE(inn1.op, inn2.op, None)
    gateZ = BGate(Z, size_hint=(200. / 960, 175. / 640))
    gateZ.center = (440, 300)
    widget.add_widget(gateZ)

    op2 = boolean.OR_BGATE(Y, Z)
    gate2 = BGate(op2, size_hint=(200. /960, 350./ 640))
    gate2.center = (600, 360)
    widget.add_widget(gate2)

    with widget.canvas:
        line_width = 5.

        c1 = Color(0, 0.9, 0.3 if not input1 else 0.9, mode='hsv')
        line_1G = Wire(input1, inv1, c1, points=(150, 500), width=line_width, joint='round')
        line_1G.points += [160, 500]

        ci1 = Color(0, 0.9, 0.3 if not inv1 else 0.9, mode='hsv')
        line_1G = Wire(inv1, Y, ci1, points=(305, 500), width=line_width, joint='round')
        line_1G.points += [335, 500]
        line_1G.points += [335, 385]
        line_1G.points += [375, 385]

        c2 = Color(5. / 7, 0.9, 0.3 if not input2 else 0.9, mode='hsv')
        line_2G = Wire(input2, inv2, c2, points=(150, 200), width=line_width, joint='round')
        line_2G.points += [160, 200]

        ci2 = Color(5. / 7, 0.9, 0.3 if not inv2 else 0.9, mode='hsv')
        line_2G = Wire(inv2, Y, ci2, points=(305, 200), width=line_width, joint='round')
        line_2G.points += [335, 200]
        line_2G.points += [335, 335]
        line_2G.points += [375, 335]

        c3 = Color(0, 0, 0.22 if not Y else 0.66, mode='hsv')
        line_GO = Wire(Y, op2, c3, points=(555, 360), width=line_width * 1.5)
        line_GO.points += [600, 360]

        c4 = Color(0, 0, 0.22 if not op2 else 0.66, mode='hsv')
        line_GO2 = Wire(op2, out2, c4, points=(730, 360), width=line_width * 1.5)
        line_GO2.points += [750, 360]
        # self.button.state = 'down' if new_val else 'normal'
        # input2.set_value(input2_default)

def get_level_N1(widget):
    input1_default = False
    input2_default = False
    input3_default = False
    input4_default = False
    input5_default = False
    base_default = True

    input1 = ToggleInput("16", size_hint=(25. / 960, 80. / 640), center=(200, 520))
    widget.add_widget(input1)
    input1.button.state = 'down' if input1_default else 'normal'

    input2 = ToggleInput("8", size_hint=(25. / 960, 80. / 640), center=(300, 520))
    widget.add_widget(input2)
    input2.button.state = 'down' if input2_default else 'normal'

    input3 = ToggleInput("4", size_hint=(25. / 960, 80. / 640), center=(400, 520))
    widget.add_widget(input3)
    input3.button.state = 'down' if input3_default else 'normal'

    input4 = ToggleInput("2", size_hint=(25. / 960, 80. / 640), center=(500, 520))
    widget.add_widget(input4)
    input4.button.state = 'down' if input4_default else 'normal'

    input5 = ToggleInput("1", size_hint=(25. / 960, 80. / 640), center=(600, 520), rows=3)
    widget.add_widget(input5)
    input5.button.state = 'down' if input5_default else 'normal'

    display = NumberDisplay("Display", size_hint=(200. / 960, 100. / 640), center=(300, 320), rows=3)
    widget.add_widget(display)

    base = ToggleInput("bin/dec", size_hint=(25. / 960, 80. / 640), center=(250, 220), rows=3)
    widget.add_widget(base)
    base.button.state = 'down' if base_default else 'normal'

    input1.set_output(display)
    input2.set_output(display)
    input3.set_output(display)
    input4.set_output(display)
    input5.set_output(display)

    base.set_output(display.base_in)

    with widget.canvas:
        line_width = 2.

        c1 = Color(0, 0.9, 0.3 if not input1 else 0.9, mode='hsv')
        line_1G = Wire(input1, display, c1, points=(163, 460), width=line_width, joint='round')
        line_1G.points += [163, 400]
        line_1G.points += [265, 400]
        line_1G.points += [265, 380]

        c1 = Color(0, 0.9, 0.3 if not input2 else 0.9, mode='hsv')
        line_1G = Wire(input2, display, c1, points=(263, 460), width=line_width, joint='round')
        line_1G.points += [263, 415]
        line_1G.points += [305, 415]
        line_1G.points += [305, 380]

        c1 = Color(0, 0.9, 0.3 if not input3 else 0.9, mode='hsv')
        line_1G = Wire(input3, display, c1, points=(363, 460), width=line_width, joint='round')
        line_1G.points += [363, 430]
        line_1G.points += [345, 430]
        line_1G.points += [345, 380]

        c1 = Color(0, 0.9, 0.3 if not input4 else 0.9, mode='hsv')
        line_1G = Wire(input4, display, c1, points=(463, 460), width=line_width, joint='round')
        line_1G.points += [463, 415]
        line_1G.points += [385, 415]
        line_1G.points += [385, 380]

        c1 = Color(0, 0.9, 0.3 if not input5 else 0.9, mode='hsv')
        line_1G = Wire(input5, display, c1, points=(563, 460), width=line_width, joint='round')
        line_1G.points += [563, 400]
        line_1G.points += [425, 400]
        line_1G.points += [425, 380]

        c2 = Color(4. / 7, 0.9, 0.3 if not base else 0.9, mode='hsv')
        line_2G = Wire(base, display.base_in, c2, points=(213, 260), width=line_width, joint='round')
        line_2G.points += [213, 300]
        line_2G.points += [243, 300]

        #
        # ci2 = Color(5. / 7, 0.9, 0.3 if not inv2 else 0.9, mode='hsv')
        # line_2G = Wire(inv2, Y, ci2, points=(305, 200), width=line_width, joint='round')
        # line_2G.points += [335, 200]
        # line_2G.points += [335, 335]
        # line_2G.points += [375, 335]
        #
        # c3 = Color(0, 0, 0.22 if not Y else 0.66, mode='hsv')
        # line_GO = Wire(Y, op2, c3, points=(555, 360), width=line_width * 1.5)
        # line_GO.points += [600, 360]
        #
        # c4 = Color(0, 0, 0.22 if not op2 else 0.66, mode='hsv')
        # line_GO2 = Wire(op2, out2, c4, points=(730, 360), width=line_width * 1.5)
        # line_GO2.points += [750, 360]
        # # self.button.state = 'down' if new_val else 'normal'
        # # input2.set_value(input2_default)

def get_level_N2(widget):
    base_default = True

    output1 = BooleanOutput("16", size_hint=(25. / 960, 80. / 640), center = (200, 140))
    widget.add_widget(output1)

    output2 = BooleanOutput("8", size_hint=(25. / 960, 80. / 640), center = (300, 140))
    widget.add_widget(output2)

    output3 = BooleanOutput("4", size_hint=(25. / 960, 80. / 640), center = (400, 140))
    widget.add_widget(output3)

    output4 = BooleanOutput("2", size_hint=(25. / 960, 80. / 640), center = (500, 140))
    widget.add_widget(output4)

    output5 = BooleanOutput("1", size_hint=(25. / 960, 80. / 640), center = (600, 140))
    widget.add_widget(output5)

    display = NumberDisplay("Display", size_hint=(200. / 960, 100. / 640), center=(300, 320), rows=3)
    widget.add_widget(display)

    base = ToggleInput("bin/dec", size_hint=(25. / 960, 80. / 640), center=(200, 320), rows=3)
    widget.add_widget(base)
    base.button.state = 'down' if base_default else 'normal'

    display.add_output(output5)
    display.add_output(output4)
    display.add_output(output3)
    display.add_output(output2)
    display.add_output(output1)

    base.set_output(display.base_in)

    with widget.canvas:
        line_width = 2.

        c1 = Color(0, 0.9, 0.3 if not output1 else 0.9, mode='hsv')
        line_1G = Wire(display, output1, c1, points=(265, 280), width=line_width, joint='round')
        line_1G.points += [265, 250]
        line_1G.points += [163, 250]
        line_1G.points += [163, 150]

        c1 = Color(0, 0.9, 0.3 if not output1 else 0.9, mode='hsv')
        line_1G = Wire(display, output2, c1, points=(305, 280), width=line_width, joint='round')
        line_1G.points += [305, 235]
        line_1G.points += [263, 235]
        line_1G.points += [263, 150]

        c1 = Color(0, 0.9, 0.3 if not output1 else 0.9, mode='hsv')
        line_1G = Wire(display, output3, c1, points=(345, 280), width=line_width, joint='round')
        line_1G.points += [345, 220]
        line_1G.points += [363, 220]
        line_1G.points += [363, 150]

        c1 = Color(0, 0.9, 0.3 if not output1 else 0.9, mode='hsv')
        line_1G = Wire(display, output4, c1, points=(385, 280), width=line_width, joint='round')
        line_1G.points += [385, 235]
        line_1G.points += [463, 235]
        line_1G.points += [463, 150]

        c1 = Color(0, 0.9, 0.3 if not output1 else 0.9, mode='hsv')
        line_1G = Wire(display, output5, c1, points=(425, 280), width=line_width, joint='round')
        line_1G.points += [425, 250]
        line_1G.points += [563, 250]
        line_1G.points += [563, 150]

        c2 = Color(4. / 7, 0.9, 0.3 if not base else 0.9, mode='hsv')
        line_2G = Wire(base, display.base_in, c2, points=(243, 300), width=line_width, joint='round')
        line_2G.points += [183, 300]


# __all__ = (get_level_2, get_level_3)
