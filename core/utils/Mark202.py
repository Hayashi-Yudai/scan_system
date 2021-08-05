import pyvisa as visa
import time


class Mark202:
    def __init__(self, gpib=12):
        self.instr = visa.ResourceManager().open_resource(f"GPIB0::{gpib}::INSTR")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.instr.close()

    def wait_while_busy(self):
        while True:
            status = self.instr.query("!:")
            if "R" in status:
                break
            time.sleep(0.5)

    def initialize(self):
        self.wait_while_busy()
        self.instr.write("H:W")

    def move(self, position):
        query = f"A:1+P{position // 2}"
        self.instr.write(query)
        self.instr.write("G:")

    def get_position(self):
        status = self.instr.query("Q:")
        position = status.split(",")[0].replace(" ", "")

        return int(position)
