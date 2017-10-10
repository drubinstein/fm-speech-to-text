import asyncio
from typing import Callable, List

import fmdemod
from rtlsdr import RtlSdr

SampleStream = List[float]

async def streaming(sample_processor: Callable[[SampleStream, RtlSdr], None],
                    center_freq=100300000,
                    sample_rate=2.048e6):
    """SDR streaming function
    :param sample_processor: Function that is used to process the samples, must
        take an array of floats as the first argument and an sdr object
        (for metadata) as the second
    :param sample_rate: The sample rate to obtain samples at in Hz
    :param center_freq int: The center frequency for capturing in Hz
    """
    sdr = RtlSdr()
    sdr.sample_rate=sample_rate
    sdr.center_freq = center_freq
    sdr.freq_correction = 60
    sdr.gain = 'auto'

    async for samples in sdr.stream():
        sample_processor(samples, sdr)

    await sdr.stop()

    sdr.close()

def printer(samples: SampleStream, sdr: RtlSdr) -> None:
    print(samples)

loop = asyncio.get_event_loop()
loop.run_until_complete(streaming(fmdemod.demod))
