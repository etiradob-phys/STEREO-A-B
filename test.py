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
# --------------------------------------------------------------------------------------------------------------------------------------

install_package("numpy")
install_package("pandas")
#install_package("pyspedas")

# --------------------------------------------------------------------------------------------------------------------------------------

#import numpy as np
#import pandas as pd
import pyspedas

#from pytplot import get_data
from datetime import datetime

# --------------------------------------------------------------------------------------------------------------------------------------

def get_date_input(prompt):
    while True:
        date_str = input(prompt)
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid format. Please enter the date in YYYY-MM-DD format.")

def get_probe_input():
    while True:
        probe = input("Select a probe (A or B): ").strip().upper()
        if probe in ["A", "B"]:
            return probe
        print("Invalid input. Please enter A or B.")

def main():
    print("Enter the time range:")
    global begin_time, end_time, probe
    begin_time = get_date_input("Begin time (YYYY-MM-DD): ")
    end_time = get_date_input("End time (YYYY-MM-DD): ")
    probe = get_probe_input()
    
    if begin_time > end_time:
        print("Error: Begin time cannot be after end time.")
    else:
        print('----------------------------------------------------------------')
        print(f"Selected time range: {begin_time} to {end_time}, Probe: {probe}")

if __name__ == "__main__":
    main()

# --------------------------------------------------------------------------------------------------------------------------------------

plastic_vars = pyspedas.stereo.plastic(trange=[begin_time.strftime("%Y-%m-%d"), end_time.strftime("%Y-%m-%d")],probe=probe.lower())
print('----------------------------------------------------------------')
mag_vars = pyspedas.stereo.mag(trange=[begin_time.strftime("%Y-%m-%d"), end_time.strftime("%Y-%m-%d")],probe=probe.lower())
