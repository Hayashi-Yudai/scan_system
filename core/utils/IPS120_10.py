import pyvisa as visa
import logging

logger = logging.getLogger("root")


class IPS120:
    """
    Magnetic field controller IPS120-10
    """

    def __init__(self, gpib=25):
        self.instr = visa.ResourceManager().open_resource(f"GPIB0::{gpib}::INSTR")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.instr.close()

    def set_control(self, num: int):
        """
        ---
        num
        ---
        0: Local & Locked (default)
        1: Remote & Locked
        2: Local & Unlocked
        3: Remote & Unlocked
        ---

        Local: Cotrol with buttons
        Remote: Control from PC

        Unlocked: operations can be interrupted by local or remote operation
        """
        self.instr.query(f"C{num}")

    def read_parameter(self, num: int):
        """
        ---
        num
        ---
        0: output current (amp)
        1: power supply voltage (volt)
        2: measured magnet current (amp)
        5: target current (amp)
        6: current sweep rate (amp/min)
        7: output field (tesla)
        8: target field (tesla)
        9: field sweep rate (tesla/min)
        """
        self.instr.query(f"R{num}")

    def switch_heater(self, num: int):
        """
        ---
        num
        ---
        0: Off magnet at zero (switch closed)
        1: On (switch open)
        2: Off magnet at field (switch closed)
        """
        return self.instr.query(f"H{num}")

    def set_activity(self, num: int):
        """
        ---
        num
        ---
        0: Hold
        1: To set point
        2: To zero
        4: Clamp
        """
        return self.instr.query(f"A{num}")

    def set_target_field(self, field: float):
        """
        field: target field (tesla)
        """
        return self.instr.query(f"J{field}")

    def set_field_sweep_rate(self, rate: float):
        """
        rate: target sweep rate (tesla/min)
        """
        return self.instr.query(f"T{rate}")
