from core.utils.Mark202 import Mark202
from core.utils.SR830 import SR830
from core.utils.waveform import WaveForm
import os
import pandas as pd
import numpy as np
import time


def move_stage(position: int) -> bool:
    try:
        with Mark202(int(os.environ["MARK202_GPIB_ADDRESS"])) as stage:
            stage.move(position)
        return True
    except Exception:
        print("Error in moving stage")
        return False


def save_data_as_csv(save_path: str, data: list) -> None:
    df = pd.DataFrame({"x": data[0], "y": data[1]})

    if save_path.endswith(".csv"):
        df.to_csv(save_path, index=False)
    else:
        df.to_csv(save_path + ".csv", index=False)


def get_lockin_intensity() -> tuple:
    """
    Returns the lockin intensity and status
    """
    try:
        with SR830(int(os.environ["SR830_GPIB_ADDRESS"])) as lockin:
            return float(lockin.get_intensity()), True
    except Exception:
        return 0, False


def auto_phase_lockin():
    try:
        with SR830(int(os.environ["SR830_GPIB_ADDRESS"])) as lockin:
            lockin.auto_phase()
        return True
    except Exception:
        return False


def set_lockin_sensitivity(value, unit):
    try:
        with SR830(int(os.environ["SR830_GPIB_ADDRESS"])) as lockin:
            lockin.set_sensitivity(value, unit)
        return True
    except Exception:
        return False


def set_lockin_time_const(value, unit):
    try:
        with SR830(int(os.environ["SR830_GPIB_ADDRESS"])) as lockin:
            lockin.set_time_const(value, unit)
        return True
    except Exception:
        return False


def calc_fft(data: list) -> list:
    delta_time = (data[0][1] - data[0][0]) * 1e-6 * 2 / 2.9979e8
    freq = [i / delta_time / 4096 for i in range(4096)]

    return freq, abs(np.fft.fft(data[1], 4096)).tolist()


def tds_scan(
    start: int, end: int, step: int, lockin_time: float, wave: WaveForm
) -> None:
    try:
        with SR830(int(os.environ["SR830_GPIB_ADDRESS"])) as amp, Mark202() as stage:
            stage.move(start)
            stage.wait_while_busy()

            position_now = start
            while position_now <= end:
                time.sleep(lockin_time / 1000)
                intensity = amp.get_intensity()

                wave.push([position_now], [float(intensity)])
                stage.move(position_now + step)
                position_now += step
                stage.wait_while_busy()
    except Exception as e:
        print("Error in tds_boot()")
        print(e)
