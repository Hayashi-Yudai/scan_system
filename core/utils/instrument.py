import pyvisa as visa


class GPIBInstrument:
    def __init__(self, gpib):
        self.rm = visa.ResourceManager()
        self.instr = self.rm.open_resource(f"GPIB::{gpib}::INSTR")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.instr.close()
