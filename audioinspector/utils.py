import numpy as np




def dbfs(x):
"""Convert linear amplitude to dBFS (approx). Avoid log10(0)"""
rms = np.sqrt(np.mean(np.square(x)))
if rms <= 0:
return -999.0
return 20.0 * np.log10(rms)




def peak_db(x):
peak = np.max(np.abs(x))
if peak <= 0:
return -999.0
return 20.0 * np.log10(peak)




def ensure_mono(y):
import numpy as np
if y.ndim == 1:
return y
# average channels
return np.mean(y, axis=0)
