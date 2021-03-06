class BooleanInput(object):
    def __init__(self, initial_value = False, output = None):
        self.value = None
        self.output = None
        self.callbacks = []
        self.set_value(initial_value)
        self.set_output(output)

    def clear_output(self, old_output):
        if old_output is not None and self.output == old_output:
            self.output.disconnect(self)
            self.callbacks.remove(self.output.update_value)

    def set_output(self, new_output):
        # if self.output is not None:
        #     self.output.disconnect(self)
        #     self.callbacks.remove(self.output.update_value)
        self.output = new_output
        if self.output is not None:
            self.output.connect(self)
            self.callbacks.append(self.output.update_value)

    def update_value(self, input, old_val, new_val):
        # print "input of {} is being updated".format(self)
        self.value = new_val
        for callback in self.callbacks:
            callback(input, old_val, new_val)
        if self.output is not None:
            self.output.update_value(self, old_val, new_val)

    def __str__(self):
        return "%s[%s]" % (type(self), id(self))

    def __bool__(self):
        return bool(self.value)
    __nonzero__ = __bool__

class MutableBooleanInput(BooleanInput):
    def set_value(self, new_value):
        # print "%s is being set to %s" % (self, bool(new_value))
        prev_value = bool(self.value)
        self.value = new_value
        # if bool(new_value) != bool(prev_value):
        self.update_value(self, prev_value, new_value)
        return bool(self)

    def toggle_value(self):
        return self.set_value(not self.value)



class BooleanOutput(object):
    def __init__(self, default_state = False, input = None):
        self.default_state = default_state
        self.input = input

    def update_value(self, input, old_val, new_val):
        # print "%s new value is %s (old value was %s)" % (self, bool(new_val), bool(old_val))
        pass

    def connect(self, input):
        self.input = input

    def __str__(self):
        return "%s[%s]" % (type(self), id(self))

    def __bool__(self):
        if (self.input is not None):
            return bool(self.input)
        return bool(self.default_state)
    __nonzero__ = __bool__



class BooleanLogicGate(object):
    def __init__(self, input0=None, input1=None, output=None):
        self.callbacks = []
        self.input0 = input0
        self.input1 = input1
        self.outputs = set()
        self.lookup_table = tuple(bool(int(x)) for x in '{0:04b}'.format(self.operation))
        if (input0 is not None):
            self.input0.set_output(self)
        if (input1 is not None):
            self.input1.set_output(self)
        self.set_output(output)

    def _update_table(self, operation):
        old_val = bool(self)
        self.operation = operation
        self.lookup_table = tuple(bool(int(x)) for x in '{0:04b}'.format(self.operation))
        new_val = bool(self)
        self.update_value(self, old_val, new_val)

    def add_output(self, output):
        return self.outputs.add(output)
    def remove_output(self, output):
        return self.outputs.remove(output)
    def set_output(self, output):
        self.output = output
        if (output is not None):
            self.callbacks.append(self.output.update_value)

    def disconnect(self, input_param):
        pass

    def connect(self, input_param):
        pass

    def update_value(self, input, old_val, new_val):
        print "%s inputs are being updated" % (self)
        if self.output is not None:
            old1, old2 = bool(self.input0), bool(self.input1)
            if input == self.input0:
                old1 = old_val
            if input == self.input1:
                old2 = old_val
            if input is not self:
                old_val = self(old1, old2)
        for cb in self.callbacks:
            cb(self, old_val, bool(self))

    def __str__(self):
        return "%s[%s]" % (get_name_of_bgate(self.operation), id(self))

    def __call__(self, input0, input1):
        return self.lookup_table[(int(bool(input0)) << 1 | int(bool(input1)))]

    def __bool__(self):
        return self(self.input0, self.input1)

    __nonzero__ = __bool__

class FALSE_BGATE(BooleanLogicGate):
    operation = 0
class AND_BGATE(BooleanLogicGate):
    operation = 1
class CONV_NONIMPLY_BGATE(BooleanLogicGate):
    operation = 2
class INPUT0_BGATE(BooleanLogicGate):
    operation = 3
class NONIMPLY_BGATE(BooleanLogicGate):
    operation = 4
class INPUT1_BGATE(BooleanLogicGate):
    operation = 5
class XOR_BGATE(BooleanLogicGate):
    operation = 6
class OR_BGATE(BooleanLogicGate):
    operation = 7
class NOR_BGATE(BooleanLogicGate):
    operation = 8
class XNOR_BGATE(BooleanLogicGate):
    operation = 9
class NOT_INPUT1_BGATE(BooleanLogicGate):
    operation = 10
class CONV_IMPLY_BGATE(BooleanLogicGate):
    operation = 11
class NOT_INPUT0_BGATE(BooleanLogicGate):
    operation = 12
class IMPLY_BGATE(BooleanLogicGate):
    operation = 13
class NAND_BGATE(BooleanLogicGate):
    operation = 14
class TRUE_BGATE(BooleanLogicGate):
    operation = 15

binop_name_map = {
    0:"FALSE",
    1:"AND",
    2:"CONV_NONIMP",
    3:"INPUT0",
    4:"NONIMPLY",
    5:"INPUT1",
    6:"XOR",
    7:"OR",
    8:"NOR",
    9:"XNOR",
    10:"~INPUT1",
    11:"CONV_IMPLY",
    12:"~INPUT0",
    13:"->",
    14:"NAND",
    15:"TRUE",
}
def get_name_of_bgate(operation):
    return binop_name_map.get(operation, "UNKNOWN")

def UnaryLogicGate(op):
    class UnaryLogicGate(object):
        operation = op
        def __init__(self, input = None, output = None):
            self.callbacks = []
            self.input = input
            if (input is not None):
                self.input.set_output(self)
            self.lookup_table = tuple(bool(int(x)) for x in '{0:02b}'.format(op))
            self.set_output(output)

        def update_value(self, input, old_val, new_val):
            print "Updating my (%s) value to %s" % (self, new_val)
            if self.output is not None:
                old1 = bool(self.input)
                if input == self.input:
                    old1 = old_val
                for cb in self.callbacks:
                    cb(self, self(old1), bool(self))

        def set_output(self, output):
            print "Adding my (%s) output to %s" % (self, output)
            self.output = output
            if (output is not None):
                self.callbacks.append(self.output.update_value)

        def disconnect(self, input_param):
            pass

        def connect(self, input_param):
            pass

        def __str__(self):
            return "%s[%s]" % (type(self), id(self))

        def __call__(self, value):
            return self.lookup_table[(int(bool(value)))]

        def __bool__(self):
            return self(self.input)

        __nonzero__ = __bool__
    return UnaryLogicGate

FALSE_UGATE = UnaryLogicGate(0)
BUFFER_UGATE = UnaryLogicGate(1)
INVERTER_UGATE = UnaryLogicGate(2)
TRUE_UGATE = UnaryLogicGate(3)

def digit_to_char(digit):
    if digit < 10: return chr(ord('0') + digit)
    else: return chr(ord('a') + digit - 10)

def str_base(number,base):
    if number < 0:
        return '-' + str_base(-number,base)
    else:
        (d,m) = divmod(number,base)
        if d:
            return str_base(d,base) + digit_to_char(m)
        else:
            return digit_to_char(m)

def base_to_str(base):
    base_names = {
        1: "unary",
        2: "binary",
        3: "ternary",
        4: "quaternary",
        8: "octal",
        10: "decimal",
        16: "hexadecimal",
    }
    return base_names.get(base, "unknown")

def exercise():
    output = BooleanOutput()
    input0 = MutableBooleanInput()
    input1 = MutableBooleanInput()
    and1 = AND_BGATE(input0, input1, output)
    input0.toggle_value()
    input1.toggle_value()
