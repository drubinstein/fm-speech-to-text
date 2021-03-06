import os
from typing import List

from rtlsdr import RtlSdr
import scipy.signal as signal
import numpy as np
import pyaudio

import speech_recognition as sr


SampleStream = List[float]
AudioStream = List[int]

stream_text = bytes()
stream_text_count = 0

recognizer = sr.Recognizer()
audio_stream_out = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                          channels=1,
                                          rate=44100,
                                          output=True)

def stream_audio(data : AudioStream):
    global stream_text
    global stream_text_count

    if stream_text_count < 1000:
        stream_text += data
        stream_text_count += 1
    else:
        audio_stream_out.write(stream_text)
        audio_data = sr.AudioData(stream_text, 44100, 2)
        print(recognizer.recognize_sphinx(audio_data))

        stream_text = bytes()
        stream_text_count = 0

def decimator(samples: SampleStream, fs: float, bandwidth: float) -> SampleStream:
        # First downsample and filter the signal using the desired bandwidth
        decimation_rate = int(fs/bandwidth)
        decimated_samples = signal.decimate(samples, decimation_rate)
        decimated_fs = fs/decimation_rate
        return decimated_samples, decimated_fs

def polar_discriminator(samples: SampleStream) -> SampleStream:
        # Invoke the polar discriminator
        return np.angle(samples[1:] * np.conj(samples[:-1]))

def deemphasis_filter(samples: SampleStream, fs) -> SampleStream:
        # Run the de-emphasis filter
        three_db_point = fs * 75e-6 # Number of samples until -3dB point
        decay = np.exp(-1/three_db_point) # decay between each sample
        b = [1-decay] # filter coefficients
        a = [1, -decay]
        return signal.lfilter(b,a,samples)

def demod(samples: SampleStream, sdr: RtlSdr) -> None:
    samples, decimated_fs = decimator(samples, sdr.sample_rate, 200e3)
    samples = polar_discriminator(samples)
    samples = deemphasis_filter(samples, decimated_fs)

    audio_signal, audio_fs = decimator(samples, decimated_fs, 44100.0)
    audio_signal *= 10000/ np.max(audio_signal) # adjust volume
    stream_audio(audio_signal.astype("int16").tobytes())
