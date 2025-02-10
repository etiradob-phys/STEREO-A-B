# Author: E. Tirado-Bueno (etirado@inaoe.mx)
# Last Update: 10 / 02 / 2025
# --------------------------------------------------------------------------------------------------------------------------------------
import subprocess
import sys
# --------------------------------------------------------------------------------------------------------------------------------------
# Function to install a package
# --------------------------------------------------------------------------------------------------------------------------------------

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# --------------------------------------------------------------------------------------------------------------------------------------
# Install numpy as an example
# --------------------------------------------------------------------------------------------------------------------------------------

install_package("numpy")
install_package("pandas")
install_package("pyspedas")

# --------------------------------------------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import pyspedas

from pytplot import get_data
from datetime import datetime

print("Numpy version:", np.__version__)
print("Pandas version:", pd.__version__)
