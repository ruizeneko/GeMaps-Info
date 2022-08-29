#!/usr/bin/env python
# coding: utf-8

# Spectral parameters
# =============
# ****************

# Now, spectral parameters are going to be introduced. There are 6 parameters:
# * Alpha Ratio
# * Hammarberg Index
# * Spectral Slople 0-500 Hz and 500 - 1500 Hz
# * Formant 1, 2 and 4 relative energy
# * Harmonic difference H1-H2
# * Harmonic difference H1-H3

# Alpha ratio
# -------------
# ****************
# The alpha ratio is defined as the ratio of the summed energy from 50 - 1000 Hz and 1 - 5 kHz, that is, between the energy in the low frequency region and in the high frequency region. It is defined as :
# 
# $$ \rho_{\alpha} = \frac{\sum_{m=1}^{m_{1k}}X(m)}{\sum_{m=m_{1k} + 1}^{M}X(m)} $$
# 
# Here, $m_{1k}$ is the highest spectral bin index with $ f \leq 1 kHz $. The alpha ratio is computed per frame (20 ms) and then, the functional mean and variance are applied to summarise it over segments of interest. To calculate it with PRAAT:

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


# Alpha Ratio with PRAAT
bandwidth = 100.0
lta = call(sound, "To Ltas", bandwidth)

low_band_start = 50.0
low_band_end = 1000.0

high_band_start = 1000.0
high_band_end = 5000.0

averaging_method = "energy"

alpha_rate = call(lta, "Get slope", low_band_start, low_band_end, high_band_start, high_band_end, averaging_method)
alpha_rate


# In[3]:


# Alpha Ratio with OpenSmile
signal, sampling_rate = audiofile.read(
    dir_audio,
    duration=10,
    always_2d=True,
)
smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.GeMAPSv01b,
    feature_level=opensmile.FeatureLevel.LowLevelDescriptors,
)
smile.process_signal(
    signal,
    sampling_rate
)["alphaRatio_sma3"]


# Hammarberg Index
# -------------
# ****************
# Hammarberg Index is defined as the ratio of the strongest energy peak in the 0–2 kHz region to the strongest peak in the 2–5 kHz region. Hammarberg defined a fixed static pivot point of 2 kHz where the low and high frequency regions
# are separated. Formally, it is defined as: 
# 
# $$ \eta =  \frac{\max_{m=1}^{m_{2k}}X(m)}{\max_{m=m_{2k} + 1}^{M}X(m)} $$
# 
# with X(m) being a magnitude spectrum with bins $m = 1..M$ , and where $m_{2k}$ is the highest spectral bin index where $f \leq 2 kHz$ is still true. According to more recent findings, it could be beneficial to pick
# the pivot point dynamically based upon the speaker’s fundamental frequency. This is, however, on purpose not  onsidered here because it would break the strictly static nature of all the extraction methods of all the parameters suggested for this set.

# In[4]:


# Hammarberg Index with PRAAT
f_first_range_start = 0.0
f_first_range_end = 2000.0

f_second_range_start = 2000.0
f_second_range_end = 5000.0

interpolation = "None"

hammberger = call(lta, "Get maximum", f_first_range_start, f_first_range_end, interpolation) - call(lta, "Get maximum", f_second_range_start, f_second_range_end, interpolation)
hammberger


# In[5]:


# HNR for OpenSmile
smile.process_signal(
    signal,
    sampling_rate
)["hammarbergIndex_sma3"]


# Spectral Slople 0-500 Hz and 500 - 1500 Hz
# -------------
# ****************
# They are defined as the linear regression slope of the logarithmic power spectrum within the two given bands.
# There is no direct way to calculate them on PRAAT.

# In[6]:


# Sprectral Slopes for OpenSmile
print(smile.process_signal(
    signal,
    sampling_rate
)["slope0-500_sma3"])
smile.process_signal(
    signal,
    sampling_rate
)["slope500-1500_sma3"]


# Formant 1, 2 and 3 relative energy
# -------------
# ****************
# It is the ratio of the energy of the spectral harmonic peak at the first, second, third formant’s centre frequency to the energy of the spectral peak at $F_0$.  They are estimated as the amplitude of the spectral envelope at Fi in relation to the amplitude of the spectral F0 peak. More precisely, it is computed as the ratio of the amplitude of the highest F0 harmonic peak in the range $[0.8\cdot Fi , 1.2\cdot Fi]$ (Fi is the centre frequency of the first formant) to the amplitude of the F0 spectral peak. 
# 
# At OpenSmile:

# In[7]:


print(smile.process_signal(
    signal,
    sampling_rate
)["F1amplitudeLogRelF0_sma3nz"])
print("\n")
print(smile.process_signal(
    signal,
    sampling_rate
)["F2amplitudeLogRelF0_sma3nz"])
print("\n")

print(smile.process_signal(
    signal,
    sampling_rate
)["F3amplitudeLogRelF0_sma3nz"])


# Harmonic difference H1-H2
# -------------
# ****************
# It is the ratio of energy of the first $F_0$ harmonic (H1) to the energy of the second $F_0$ harmonic (H2). They are computed from the amplitudes of $F_0$ harmonic peaks in the spectrum normalised by the amplitude of the $F_0$ spectral peak. In the proposed parameter set, in particular the ratios H1–H2, i. e., the ratio of the first to the second harmonic, and H1–A3, which is the ratio of the first harmonic to the third formant’s amplitude.
# 
# At Praat:

# In[8]:


# Harmonic difference H1-H2 in PRAAT
bandwidth = 100.0
lta = call(sound, "To Ltas", bandwidth)

h1 = call(lta, "Get value in bin", 2)
h2 = call(lta, "Get value in bin", 3)
h1 - h2


# In[9]:


# Harmonic difference H1-H2 in OpenSmile
smile.process_signal(
    signal,
    sampling_rate
)["logRelF0-H1-H2_sma3nz"]


# Harmonic difference H1-A3
# -------------
# ****************
# It is ratio of energy of the first $F_0$ harmonic (H1) to the energy of the highest harmonic in the third formant range (A3).
# 
# At OpenSmile:

# In[10]:


smile.process_signal(
    signal,
    sampling_rate
)["logRelF0-H1-A3_sma3nz"]

