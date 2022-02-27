import time
import logging

from core.utils.instrument import GPIBInstrument

logger = logging.getLogger("root")


class Mark202(GPIBInstrument):
    def wait_while_busy(self):
        while True:
            logger.debug("Mark102.wait_while_busy: loop")
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
