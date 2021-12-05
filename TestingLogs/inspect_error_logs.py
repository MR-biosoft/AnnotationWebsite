
from pathlib import Path
import pandas as pd

read_error_log = lambda x: pd.read_json(x, lines=True)

