#!/usr/bin/env python
# coding: utf-8

# Frequency related parameters
# =============
# ****************

# First, frequency related parameters are going to be explained. Those parameters are:
# * Pitch
# * Jitter
# * Formant 1, 2 and 3 frequency
# * Bandwidth of Formant 1
# 
# NOTE: All the values obtained with Parselmouth have been compared (and checked) with the Desktop version (for Unix System) of PRAAT

# Pitch
# -------------
# ****************
# The pitch is the logarithmic fundamental frequency $F_0$ (lowerst frequency of a periodic waveform, $F_3$ would be $F_3 = 3 \cdot F_0$) on a semitone frequency scale starting at 27.5 Hz (que es un semitone?). Therefore, it is highly related with the $F_0$ of a speech signal, which refers to the approximate frequency of the (quasi-)periodic structure of speech signal. 
# 
# The oscillation originates from the vocal folds, which oscillate in the airflow when appropriately tensed. The fundamental frequency is defined as the average number of oscillations per second and expressed in Hertz. 
# 
# Since the oscillation originates from an organic structure, it is not exactly periodic but contains significant fluctuations. In particular, amount of variation in period length and amplitude are known respectively as jitter and shimmer. Moreover, it changes constantly within the sentence and can be used for emphasis or for questions.
# 
# However, the pitch and the $F_0$ are not the same, because the pitch is defined as our perception of fundamental frequency. Therefore, for complex sounds like speech, it can differ from $F_0$ due to overtones.
# 
# In GeMaps (and therefore in PRAAT and openSMILE) is computed via sub-harmonic summation (SHS) in the spectral domain and further preprocessing is applied). Very simply, the can be dedined as the inverse of the legnth of a simple periode:
# $$ F_0 = \frac{1}{T} $$
# 
# Let us compute it:

# In[1]:


import os
import parselmouth 
from parselmouth.praat import call
import opensmile
import audiofile


# In[2]:


# With Parselmouth (Python implementation of PRAAT)
# We load the audio into ParselMouth
dir_audio = os.path.join("/home", "enekoehu", "Trabajo", "HAZITEK", "Documentos", "Emphasis", "sensación_enfado_1_5942331367283039919_1_46.wav")
sound = parselmouth.Sound(dir_audio)

pitch = sound.to_pitch(time_step = 0.02, pitch_floor=27.5, pitch_ceiling=600.0)
pitch.get_value_at_time(9.91)


# Therefore, the pitch at $t = 14s$ is $167.52 Hz$. For the calculation, a time_step of 0.001s is taken, and only frequency values between 75 and 600 Hz are taken into account.
# 
# For openSMILE:

# In[3]:


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
)["F0semitoneFrom27.5Hz_sma3nz"]


# In openSMILE, 20 ms time steps are taken into account and, as it can be seen, the results are quite different.

# Jitter
# -------------
# ****************
# The jitter is the deviations in individual consecutive $F_0$ period length. Therefore, 
# it can be defined as a variation in the (speech) signal frequency. All natural speech contains some level of jitter, 
# but measuring it is a common way to detect voice pathologies. It can be detected easier from long, sustained vowels
# and has its origin in the fact that vocal fold oscilattion is not exactly period. In the GeMaps paper, 3 different
# Jitters are presented: absolute local jitter, average local jitter and average relative jitter. 

# The absolute local jitter is the difference between two consecutive periods, i.e., 
# 
# $$ J_{pp}(n') = |T_{0}(n') - T_0(n'-1)| $$
# 
# This definition yields one value for every pitch period. To obtain a single jitter value per frame for N' local pitch perdios within one analysis frame, we compute the average jitter:
# 
# $$ \overline{J_{pp}(n')} = \frac{1}{N' - 1}\sum_{n'=2}^{N'}J_{pp}(n') $$
# 
# Lastly, to make the jitter not dependant of the pitch period length, we scale it by the avarage pitch period length, obtaining the average relative jitter:
# 
# $$ \overline{J_{pp, rel}} = \frac{\overline{J_{pp}(n')}}{\frac{1}{N'}\sum_{n'=1}^{N'}T_0(n')} $$

# In[4]:


# To obtain it with Praat
max_pitch_f = 600
min_pitch_f = 27.5
pointProcess = call(sound, "To PointProcess (periodic, cc)",min_pitch_f, max_pitch_f)

time_range_start = 9.92
time_range_end = 9.94 # 0 if total=0
shortest_period = 0.02
longest_period = 0.02 
maximum_period_factor = 1.3

localJitter = call(pointProcess, "Get jitter (local)", time_range_start, time_range_end, shortest_period, longest_period, maximum_period_factor)
localJitter


# In[5]:


# With OpenSmile
smile.process_signal(
    signal,
    sampling_rate
)["jitterLocal_sma3nz"]


# Formant 1, 2, and 3 frequency
# -------------
# ****************
# Centre frequency of the first, second and third formants. 

# In[6]:


# Obtain them with PRAAT

formants = call(sound, "To Formant (burg)", 0.0, 3, 5500, 0.02, 50)
#formants= call(sound, "To Formant (burg)", TIME_STEP, NUMBER_OF_FORMANTS, MAXIMUM_FORMANT ( 5500 = ADULT FEMALE), WINDOWS_LENGTH, PRE_EMPHASIS_FROM)

f1 = call(formants, "Get value at time", 1, 9.91, 'Hertz', 'Linear')
f2 = call(formants, "Get value at time", 2, 9.91, 'Hertz', 'Linear')
f3 = call(formants, "Get value at time", 3, 9.91, 'Hertz', 'Linear')
#fx= call(formants, "XXXXXXXXXXXXXXXXX", formant_number, time(s), unit(Hertz vs. bark), "interpolation")
print(f1)
print(f2)
print(f3)


# In[7]:


# The same with OpenSmile
print(smile.process_signal(
    signal,
    sampling_rate
)["F1frequency_sma3nz"])

print(smile.process_signal(
    signal,
    sampling_rate
)["F2frequency_sma3nz"])

print(smile.process_signal(
    signal,
    sampling_rate
)["F3frequency_sma3nz"])


# Bandwidth of Formant 1
# -------------
# ****************
# The bandwidth of the first formant

# In[8]:


# Obtain it with PRAAT:
f1_bandwidth = call(formants, "Get bandwidth at time", 1, 9.91, 'Hertz', 'Linear')
f1_bandwidth


# In[9]:


# The same with OpenSmile
print(smile.process_signal(
    signal,
    sampling_rate
)["F1bandwidth_sma3nz"])

