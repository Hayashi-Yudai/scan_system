from core.utils.Mark202 import Mark202
from core.utils.SR830 import SR830
from core.utils.IPS120_10 import IPS120
from core.utils.waveform import WaveForm
from core.models import TemporalData
import os
import pandas as pd
import numpy as np
import time
import logging

logger = logging.getLogger("root")


def move_stage(position: int) -> bool:
    try:
        gpib = int(os.environ["MARK202_GPIB_ADDRESS"])
        logger.debug(f"api_ops.move_stage: GPIB = {gpib}")
        logger.debug(f"api_ops.move_stage: position = {position}")
        with Mark202(gpib) as stage:
            stage.move(position)
        return True
    except Exception as e:
        logger.error(f"api_ops.move_stage: {e}")
        return False


def save_data_as_csv(save_path: str, data: list) -> None:
    df = pd.DataFrame({"x": data[0], "y": data[1]})

    if save_path.endswith(".csv"):
        df.to_csv(save_path, index=False)
    else:
        df.to_csv(save_path + ".csv", index=False)


def get_lockin_intensity() -> tuple[float, bool]:
    """
    Returns the lockin intensity and status
    """
    try:
        gpib = int(os.environ["SR830_GPIB_ADDRESS"])
        logger.debug(f"api_ops.get_lockin_intensity: GPIB = {gpib}")

        with SR830(gpib) as lockin:
            return float(lockin.get_intensity()), True
    except Exception as e:
        logger.error(f"api_ops.move_stage: {e}")
        return 0, False


def auto_phase_lockin() -> bool:
    try:
        gpib = int(os.environ["SR830_GPIB_ADDRESS"])
        logger.debug(f"api_ops.auto_phase_lockin: GPIB = {gpib}")
        with SR830(gpib) as lockin:
            lockin.auto_phase()
        return True
    except Exception as e:
        logger.error(f"api_ops.move_stage: {e}")
        return False


def set_lockin_sensitivity(value: int, unit: str) -> bool:
    try:
        gpib = int(os.environ["SR830_GPIB_ADDRESS"])
        logger.debug(f"api_ops.set_lockin_sensitivity: GPIB = {gpib}")
        with SR830(gpib) as lockin:
            lockin.set_sensitivity(value, unit)
        return True
    except Exception as e:
        logger.error(f"api_ops.set_lockin_sensitivity: {e}")
        return False


def set_lockin_time_const(value: int, unit: str) -> bool:
    try:
        gpib = int(os.environ["SR830_GPIB_ADDRESS"])
        logger.debug(f"api_ops.set_lockin_time_const: GPIB = {gpib}")
        with SR830(gpib) as lockin:
            lockin.set_time_const(value, unit)
        return True
    except Exception as e:
        logger.error(f"api_ops.set_lockin_time_const: {e}")
        return False


def calc_fft(data: list) -> list:
    delta_time = (data[0][1] - data[0][0]) * 1e-6 * 2 / 2.9979e8
    freq = [i / delta_time / 4096 for i in range(4096)]

    return freq, abs(np.fft.fft(data[1], 4096)).tolist()


def tds_scan(
    start: int, end: int, step: int, lockin_time: float, entry: TemporalData
) -> bool:
    wave = WaveForm.new(entry)
    try:
        gpib_sr = int(os.environ["SR830_GPIB_ADDRESS"])
        gpib_mk = int(os.environ["MARK202_GPIB_ADDRESS"])
        logger.debug(f"api_ops.tds_scan: GPIB(SR) = {gpib_sr}")
        logger.debug(f"api_ops.tds_scan: GPIB(MK) = {gpib_mk}")
        with SR830(gpib_sr) as amp, Mark202(gpib_mk) as stage:
            stage.move(start)
            stage.wait_while_busy()

            position_now = start
            while position_now <= end:
                time.sleep(lockin_time / 1000)
                intensity = amp.get_intensity()

                wave.push([position_now], [float(intensity)])
                entry.position_data = ",".join(map(str, wave.x))
                entry.intensity_data = ",".join(map(str, wave.y))
                entry.save()
                stage.move(position_now + step)
                position_now += step
                stage.wait_while_busy()

        return True
    except Exception as e:
        logger.error(f"api_ops.tds_scan: {e}")

        return False


def change_field(target_field: float) -> bool:
    try:
        gpib_ips = int(os.environ["IPS120_10_GPIB_ADDRESS"])

        with IPS120(gpib_ips) as instr:
            instr.set_control(1)  # Remote mode
            ##############################
            # Restore from persistent mode
            ##############################
            instr.set_activity(1)  # Set point
            time.sleep(20)
            instr.set_activity(0)  # Hold

            #############
            # Sweap field
            #############
            instr.set_target_field(target_field)
            instr.switch_heater(1)  # Switch heater on

            time.sleep(20)

            instr.set_activity(1)  # Set point
            while True:
                current_field = instr.read_parameter(7)
                if abs(current_field - target_field) < 0.0001:
                    break

                time.sleep(3)

            instr.set_activity(0)  # Hold
            instr.switch_heater(2)  # Switch heater off
            instr.set_activity(2)  # Go to zero (persistent mode)

            instr.set_control(0)  # Local mode

    except Exception:
        return False

    return True
