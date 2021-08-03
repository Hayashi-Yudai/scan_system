import pyvisa as visa


class SR830:
    def __init__(self, gpib=10):
        self.instr = visa.ResourceManager().open_resource(
            'GPIB::{}::INSTR'.format(gpib))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trace):
        self.instr.close()

    def get_intensity(self):
        return self.instr.query("OUTP ? 1")
