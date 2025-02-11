# Author: E. Tirado-Bueno (etirado@inaoe.mx)
# Last Update: 10 / 02 / 2025 19:00:00
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
install_package("matplotlib")
#install_package("smplotlib")

# --------------------------------------------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import pyspedas
import matplotlib.pyplot as plt
#import smplotlib

import warnings
warnings.filterwarnings("ignore")

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

# --------------------------------------------------------------------------------------------------------------------------------------

dataset_plastic = pd.DataFrame(data=np.column_stack((t_proton_number_density,values_proton_number_density,values_proton_bulk_speed,values_proton_temperature,values_proton_thermal_speed)),columns=['Timestamps','Density','Bulk Speed','Temperature','Thermal Speed'])

# unit='s' to convert it into epoch time
dataset_plastic['Datetime'] = pd.to_datetime(dataset_plastic['Timestamps'],
                                  unit='s').dt.strftime('%Y-%m-%d %H:%M')
dataset_plastic["Datetime"] = dataset_plastic["Datetime"].astype("datetime64[ns]")
dataset_plastic_new = dataset_plastic.set_index(pd.DatetimeIndex(dataset_plastic["Datetime"])).drop(["Datetime", "Timestamps"], axis=1)

dataset_plastic_new[dataset_plastic_new < -999.9] = np.nan

# --------------------------------------------------------------------------------------------------------------------------------------

dataset_mag_test = pd.DataFrame(data=np.column_stack((t_mag_data,values_mag_data_Br,values_mag_data_Bt,values_mag_data_Bn,values_mag_data_BTot)),columns=['Timestamps','Bx(R)','By(T)','Bz(N)','Total B'])

# unit='s' to convert it into epoch time
dataset_mag_test['Datetime'] = pd.to_datetime(dataset_mag_test['Timestamps'],
                                  unit='s').dt.strftime('%Y-%m-%d %H:%M')
dataset_mag_test["Datetime"] = dataset_mag_test["Datetime"].astype("datetime64[ns]")
dataset_mag_test2 = dataset_mag_test.set_index(pd.DatetimeIndex(dataset_mag_test["Datetime"])).drop(["Datetime", "Timestamps"], axis=1)

dataset_impact_new = dataset_mag_test2.resample('1min').mean()

# --------------------------------------------------------------------------------------------------------------------------------------

if probe == "A":
    sta_in_situ_data = pd.concat([dataset_plastic_new, dataset_impact_new], axis=1)
    #display(sta_in_situ_data)
elif probe == "B":
    stb_in_situ_data = pd.concat([dataset_plastic_new, dataset_impact_new], axis=1)
    #display(stb_in_situ_data)
