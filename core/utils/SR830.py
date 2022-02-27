from core.utils.instrument import GPIBInstrument


class SR830(GPIBInstrument):
    def get_intensity(self):
        return self.instr.query("OUTR ? 1")

    def auto_phase(self):
        self.instr.write("APHS")

    def set_sensitivity(self, value, unit):
        if value == 1 and unit == "micro-volt":
            self.instr.write("SENS 8")
        elif value == 2 and unit == "micro-volt":
            self.instr.write("SENS 9")
        elif value == 5 and unit == "micro-volt":
            self.instr.write("SENS 10")
        elif value == 10 and unit == "micro-volt":
            self.instr.write("SENS 11")
        elif value == 20 and unit == "micro-volt":
            self.instr.write("SENS 12")
        elif value == 50 and unit == "micro-volt":
            self.instr.write("SENS 13")
        elif value == 100 and unit == "micro-volt":
            self.instr.write("SENS 14")
        elif value == 200 and unit == "micro-volt":
            self.instr.write("SENS 15")
        elif value == 500 and unit == "micro-volt":
            self.instr.write("SENS 16")
        elif value == 1 and unit == "milli-volt":
            self.instr.write("SENS 17")
        elif value == 2 and unit == "milli-volt":
            self.instr.write("SENS 18")
        elif value == 5 and unit == "milli-volt":
            self.instr.write("SENS 19")
        elif value == 10 and unit == "milli-volt":
            self.instr.write("SENS 20")
        elif value == 20 and unit == "milli-volt":
            self.instr.write("SENS 21")
        elif value == 50 and unit == "milli-volt":
            self.instr.write("SENS 22")
        elif value == 100 and unit == "milli-volt":
            self.instr.write("SENS 23")
        elif value == 200 and unit == "milli-volt":
            self.instr.write("SENS 24")
        elif value == 500 and unit == "milli-volt":
            self.instr.write("SENS 25")
        elif value == 1 and unit == "volt":
            self.instr.write("SENS 26")

    def set_time_const(self, value, unit):
        if value == 10 and unit == "micro-sec":
            self.instr.write("OFLT 0")
        elif value == 30 and unit == "micro-sec":
            self.instr.write("OFLT 1")
        elif value == 100 and unit == "micro-sec":
            self.instr.write("OFLT 2")
        elif value == 300 and unit == "micro-sec":
            self.instr.write("OFLT 3")
        elif value == 1 and unit == "milli-sec":
            self.instr.write("OFLT 4")
        elif value == 3 and unit == "milli-sec":
            self.instr.write("OFLT 5")
        elif value == 10 and unit == "milli-sec":
            self.instr.write("OFLT 6")
        elif value == 30 and unit == "milli-sec":
            self.instr.write("OFLT 7")
        elif value == 100 and unit == "milli-sec":
            self.instr.write("OFLT 8")
        elif value == 300 and unit == "milli-sec":
            self.instr.write("OFLT 9")
        elif value == 1 and unit == "sec":
            self.instr.write("OFLT 10")
        elif value == 3 and unit == "sec":
            self.instr.write("OFLT 11")
        elif value == 10 and unit == "sec":
            self.instr.write("OFLT 12")
        elif value == 30 and unit == "sec":
            self.instr.write("OFLT 13")
        elif value == 100 and unit == "sec":
            self.instr.write("OFLT 14")
        elif value == 300 and unit == "sec":
            self.instr.write("OFLT 15")
