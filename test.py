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
install_package("pyspedas")
install_package("smplotlib")

# --------------------------------------------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import pyspedas
import smplotlib

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

# --------------------------------------------------------------------------------------------------------------------------------------

mag_data = get_data('BFIELD')

plastic_proton_number_density = get_data('proton_number_density')
plastic_proton_bulk_speed = get_data('proton_bulk_speed')          
plastic_proton_temperature = get_data('proton_temperature')
plastic_proton_thermal_speed = get_data('proton_thermal_speed')

# Times
t_mag_data = mag_data.times
t_proton_number_density = plastic_proton_number_density.times
t_proton_bulk_speed = plastic_proton_bulk_speed.times
t_proton_temperature = plastic_proton_temperature.times
t_proton_thermal_speed = plastic_proton_thermal_speed.times

# Values
values_mag_data_Br = mag_data.y[:,0]                                          ## Magnetic Field (Br)                  
values_mag_data_Bt = mag_data.y[:,1]                                          ## Magnetic Filed (Bt)
values_mag_data_Bn = mag_data.y[:,2]                                          ## Magnetic Field (Bn)
values_mag_data_BTot = mag_data.y[:,3]                                        ## Magnetic Field (TOTAL)
values_proton_number_density = plastic_proton_number_density.y                ## Density                            
values_proton_bulk_speed = plastic_proton_bulk_speed.y                        ## Bulk Speed
values_proton_temperature = plastic_proton_temperature.y                      ## Temperature
values_proton_thermal_speed = plastic_proton_thermal_speed.y                  ## Thermal Speed
