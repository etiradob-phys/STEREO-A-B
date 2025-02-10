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
#install_package("pyspedas")

# --------------------------------------------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import pyspedas

from pytplot import get_data
from datetime import datetime

# --------------------------------------------------------------------------------------------------------------------------------------

def get_date_input(prompt):
    while True:
        date_str = input(prompt)
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid format. Please enter the date in YYYY-MM-DD format.")

def main():
    print("Enter the time range:")
    begin_time = get_date_input("Begin time (YYYY-MM-DD): ")
    end_time = get_date_input("End time (YYYY-MM-DD): ")
    
    if begin_time > end_time:
        print("Error: Begin time cannot be after end time.")
    else:
        print(f"Selected time range: {begin_time} to {end_time}")

if __name__ == "__main__":
    main()

# --------------------------------------------------------------------------------------------------------------------------------------
#mag_vars = pyspedas.stereo.mag(trange=['2008-01-25', '2008-01-31'],probe='b')
#plastic_vars = pyspedas.stereo.plastic(trange=['2008-01-25', '2008-01-31'],probe='b')
