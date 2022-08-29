#!/usr/bin/env python
# coding: utf-8

# Energy/Amplitude related parameters
# =============
# ****************

# Now, Energy/Amplitude related parameters are going to be explained. These parameters are:
# * Shimmer
# * Loudness
# * HNR
# 
# Let us start with the shimmer

# Shimmer
# -------------
# ****************
# The shimmer, closely related to the jitter, is the difference of the peak amplitudes of
# consecutive F0 periods. The relationship can be seen more clear in the next Figure:
# <img src="Jitter-Shimmer.png" alt="drawing" width="500"/>
# 
# It is, in GeMaps, computed as avarage of the relative peak amplitude differences (in dB). 
# Because the phase of the pitch period segments found by the waveform matching algorithm is random, the maximum and minimum amplitude $(x_{max,n′}$ and $x_{min,n′}$) within each pitch period are identified. By analogy with jitter, there are 3 differents Shimmers that can be measured.
# 
# Let us start with local period to period shimmer:

# Local period to period shimmer is defined as:
# $$ S_{pp}(n') = |A(n') - A(n' - 1) | $$
# 
# Here, the peak to peak amplitude difference is defined by: $A(n') = x_{max,n′} - x_{min,n′}$

# As for jitter, the period to period shimmer values are averaged over each 60 ms frame in order to synchronise the rate of this descriptor with the constant rate of all other short-time descriptors. The averaged, relative shimmer is referred to as Spp,rel. It is expressed as amplitude ratios, i. e., the per period amplitude values are normalised to the per frame average peak amplitude:
# 
# $$ \overline{S_{pp, rel}} =  \frac{\frac{1}{N'-1}\sum_{n'=2}^{N'}S_{pp}(n')}{\frac{1}{N}\sum_{n'=1}^{N'}A(n')}$$
# 
# Let us calculate it with PRAAT:

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


# Shimmer calculated in PRAAT
min_pitch_f = 75
max_pitch_f = 600
pointProcess = call(sound, "To PointProcess (periodic, cc)", min_pitch_f, max_pitch_f)

time_range_start = 9.92
time_range_end = 9.94 # 0 if total=0

shortest_period = 0.025
longest_period = 0.025
maximum_period_factor = 1.8
maximum_amplitude_factor = 2.0

localShimmer =  call([sound, pointProcess], "Get shimmer (local)", time_range_start, time_range_end, shortest_period, longest_period, maximum_period_factor, maximum_amplitude_factor)
localShimmer


# In[3]:


# OpenSMILE
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
)["shimmerLocaldB_sma3nz"]


# Loudness
# -------------
# ****************
# Loudness, instead of signal energy/amplitude, is used to accouont for human's non-linear perception of noise (GeMaps definition: estimate of perceived signal intensity from an auditory spectrum). To represent it, an auditory spectrum as is applied in the Perceptual Linear Prediction (PLP) technique is adopted. Loudness is computed as the sum over all bands of the auditory spectrum.
# 
# For PRAAT:

# In[4]:


# Loudness for PRAAT
time_step = 0.01
frecuency_resolution_bark = 0.1
windows_length = 0.03
forward_masking_time = 0.03

cochleagram = call(sound, "To Cochleagram", time_step, frecuency_resolution_bark , windows_length , forward_masking_time)

time = 9.91
excitation = call(cochleagram, "To Excitation (slice)", time)
loudness = call(excitation, "Get loudness")
loudness


# In[5]:


# Loudness for OpenSmile
smile.process_signal(
    signal,
    sampling_rate
)["Loudness_sma3"]


# HNR
# -------------
# ****************
# HNR or Harmonics-to-Noise Ratio is the relation of energy in harmonic component to energy in noise-like component.
# It is defined as: 
#     
# $$ HNR_{acf, log} = 10 \log_{10} \left( \frac{ACF_{\tau_0}}{ACF_0 - ACF_{\tau_0}} \right) dB $$    
# 
# In the previous expression, $ACF_{\tau_0}$ is the amplitude of the autocorrelation peak at the fundamental period and $ACF_0$ is the 0-th ACF (autocorrelation function), equivalent to the quadratic frame energy. The HNR is floored to -100dB to avoid highly negative and varying values for low-energy noise.
# 
# To calculate it in PRAAT:

# In[6]:


# HNR
time_step = 0.02
minimum_pitch = 30.0
silence_threshold = 0.1
periods_per_window = 1.0

harmonicity = call(sound, "To Harmonicity (cc)", time_step , minimum_pitch, silence_threshold, periods_per_window)

time_range_start = 9.92
time_range_end = 9.94

hnr = call(harmonicity, "Get mean", time_range_start, time_range_end)
hnr


# In[7]:


# HNR for OpenSmile
smile.process_signal(
    signal,
    sampling_rate
)["HNRdBACF_sma3nz"]

