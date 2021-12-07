"""
Python script to debug.
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt

plt.ion()
x = pd.read_json(sys.argv[1], lines=True)


