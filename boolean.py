import sys

class BooleanInput(object):
    def __init__(self, initial_value = False, output = None):
        self.value = None
        self.output = None
        self.callbacks = []
        self.set_value(initial_value)
        self.set_output(output)

    def set_output(self, new_output):
        if self.output is not None:
            self.output.disconnect(self)
            self.callbacks.remove(self.output.update_value)
        self.output = new_output
        if self.output is not None:
            self.output.connect(self)
            self.callbacks.append(self.output.update_value)

    def update_value(self, input, old_val, new_val):
        print "input is being updated"
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
        print "%s is being set to %s" % (self, bool(new_value))
        prev_value = bool(self.value)
        self.value = new_value
        if bool(new_value) != bool(prev_value):
            self.update_value(self, prev_value, new_value)
        return bool(self)

    def toggle_value(self):
        return self.set_value(not self.value)



class BooleanOutput(object):
    def __init__(self, default_state = False, input = None):
        self.default_state = default_state
        self.input = input

    def update_value(self, input, old_val, new_val):
        print "%s new value is %s (old value was %s)" % (self, bool(new_val), bool(old_val))

    def __str__(self):
        return "%s[%s]" % (type(self), id(self))

    def __bool__(self):
        if (self.input is not None):
            return bool(self.input)
        return bool(self.default_state)
    __nonzero__ = __bool__


def BooleanLogicGate(cls_name, operation):
    class BooleanLogicGate(object):
        def __init__(self, input0 = None, input1 = None, output = None):
            self.input0 = input0
            self.input1 = input1
            self.lookup_table = tuple(bool(int(x)) for x in '{0:04b}'.format(operation))
            self.output = output
            if (input0 is not None):
                self.input0.set_output(self)
            if (input1 is not None):
                self.input1.set_output(self)
            self.callbacks = []
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
                for cb in self.callbacks:
                    cb(self, self(old1, old2), bool(self))

        def __str__(self):
            return "%s[%s]" % (type(self), id(self))

        def __call__(self, input0, input1):
            return self.lookup_table[(int(bool(input0)) << 1 | int(bool(input1)))]

        def __bool__(self):
            return self(self.input0, self.input1)
        __nonzero__ = __bool__
    BooleanLogicGate.__name__ = cls_name
    setattr(sys.modules[BooleanLogicGate.__module__], cls_name, BooleanLogicGate)
    return BooleanLogicGate



BooleanLogicGate('FALSE_BGATE', 0)
BooleanLogicGate('AND_BGATE', 1)
BooleanLogicGate('CONV_NONIMPLY_BGATE', 2)
BooleanLogicGate('INPUT0_BGATE', 3)
BooleanLogicGate('NONIMPLY_BGATE', 4)
BooleanLogicGate('INPUT1_BGATE', 5)
BooleanLogicGate('XOR_BGATE', 6)
BooleanLogicGate('OR_BGATE', 7)
BooleanLogicGate('NOR_BGATE', 8)
BooleanLogicGate('XNOR_BGATE', 9)
BooleanLogicGate('NOT_INPUT1_GATE', 10)
BooleanLogicGate('CONV_IMPLY_BGATE', 11)
BooleanLogicGate('NOT_INPUT0_BGATE', 12)
BooleanLogicGate('IMPLY_BGATE', 13)
BooleanLogicGate('NAND_BGATE', 14)
BooleanLogicGate('TRUE_BGATE', 15)

def UnaryLogicGate(operation):
    class UnaryLogicGate(object):
        def __init__(self, input = None, output = None):
            self.input = input
            if (input is not None):
                self.input.set_output(self)
            self.output = output
            self.lookup_table = tuple(bool(int(x)) for x in '{0:02b}'.format(operation))

        def update_value(self, input, old_val, new_val):
            if self.output is not None:
                old1 = bool(self.input)
                if input == self.input:
                    old1 = old_val
                self.output.update_value(self, self(old1), bool(self))

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

def exercise():
    output = BooleanOutput()
    input0 = MutableBooleanInput()
    input1 = MutableBooleanInput()
    and1 = AND_BGATE(input0, input1, output)
    input0.toggle_value()
    input1.toggle_value()
