import pyvisa as visa


class SR830:
    def __init__(self, gpib=11):
        self.gpib = gpib
        self.instr = visa.ResourceManager().open_resource(
            'GPIB::{}::INSTR'.format(self.gpib))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trace):
        self.instr.close()

    def get_intensity(self):
        return self.instr.query("OUTP ? 1")
