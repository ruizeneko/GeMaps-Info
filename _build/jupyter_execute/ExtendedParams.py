#!/usr/bin/env python
# coding: utf-8

# Extended Set - Spectral parameters
# =============
# ****************

# Now, spectral parameters are going to be introduced. There are 6 parameters:
# * MFCC 1-4
# * Spectral Flux

# MFCC 1-4
# -------------
# ****************
# They are the Mel-Frequency Cepstral Coefficients 1–4. The first four Mel-Frequency Cepstral Coefficients (MFCC) (1–4) are computed from a 26-band power Mel-spectrum (20–8000 Hz). In contrast to all other descriptors, the audio samples are not normalised to $[−1, +1]$, but to the range of a signed 16-bit integer. Liftering of the cepstral coefficients with L = 22 is performed.
# 
# With PRAAT, they can be easily be calculated:

# In[1]:


import os
import parselmouth 
from parselmouth.praat import call
import opensmile
import audiofile

# We load the audio into ParselMouth
dir_audio = os.path.join("/home", "enekoehu", "Trabajo", "HAZITEK", "Documentos", "Emphasis", "sensación_enfado_1_5942331367283039919_1_46.wav")
sound = parselmouth.Sound(dir_audio)


# In[2]:


# MFCC 1-4 with PRAAT
number_coefficient = 4
windows_length = 0.015
time_step = 0.005

fisrt_filter_f = 100.0
distance_between_filters = 100.0
max_f = 0.0

mfcc = call(sound, "To MFCC", number_coefficient, windows_length, time_step, fisrt_filter_f, distance_between_filters, max_f)

frame_number = 25.0
index = 1

MFCC1 = call(mfcc, "Get value in frame", frame_number, 1)
MFCC2 = call(mfcc, "Get value in frame", frame_number, 2)
MFCC3 = call(mfcc, "Get value in frame", frame_number, 3)
MFCC4 = call(mfcc, "Get value in frame", frame_number, 4)

print(MFCC1)
print(MFCC2)
print(MFCC3)
print(MFCC4)


# In[3]:


# MFCC 1-4 with OpenSmile
signal, sampling_rate = audiofile.read(
    dir_audio,
    duration=10,
    always_2d=True,
)
smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.LowLevelDescriptors,
)

print(smile.process_signal(
    signal,
    sampling_rate
)["mfcc1_sma3"])
print("\n")

print(smile.process_signal(
    signal,
    sampling_rate
)["mfcc2_sma3"])
print("\n")

print(smile.process_signal(
    signal,
    sampling_rate
)["mfcc3_sma3"])
print("\n")

print(smile.process_signal(
    signal,
    sampling_rate
)["mfcc4_sma3"])


# Spectral Flux
# -------------
# ****************
# The spectral flux $S_f$ lux represents a quadratic, normalised version of the simple spectral difference, i. e., the bin-wise difference between the spectra of two consecutive speech frames. The definition of the unnormalised spectral flux for frame k and magnitude spectra $X(m)$ is as follows:
# 
# $$ S_{flux}^{(k)} = \sum_{m = m_l}^{m_u} (X^{(k)}(m) - X^{(k - 1)}(m) )^2 $$
# 
# At the above formula, $m_l$ and $m_u$ are the lower and upper bin indices of the spectral range to be considered for spectral flux computation. Here, they are set such that the spectral range is set to $0-5000 Hz$.

# In[4]:


smile.process_signal(
    signal,
    sampling_rate
)["spectralFlux_sma3"]


# Extended Set - Frequency related parameters
# =============
# ****************
# The parameters are the bandwidths for Formants 2 and 3. With PRAAT:

# In[5]:


# Formant 2-3 bandwidth with PRAAT
formants = call(sound, "To Formant (burg)", 0.0, 3, 5500, 0.025, 50)

f2_bandwidth = call(formants, "Get bandwidth at time", 2, 25.0, 'Hertz', 'Linear')
f3_bandwidth = call(formants, "Get bandwidth at time", 3, 25.0, 'Hertz', 'Linear')


# In[6]:


# Formant 2-3 bandwidth with OpenSmile

print(smile.process_signal(
    signal,
    sampling_rate
)["F2bandwidth_sma3nz"])

print("\n")

print(smile.process_signal(
    signal,
    sampling_rate
)["F3bandwidth_sma3nz"])

