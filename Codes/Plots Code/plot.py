#%%
import pandas as pd

# file paths
new_solar_file = 'POWER_Point_Daily_20210101_20230101_040d4406N_079d9959W_LST_Solar.csv'
new_temp_hum_file = 'POWER_Point_Daily_20210101_20230101_040d4406N_079d9959W_LST_Temp+Hum.csv'
new_wind_file = 'POWER_Point_Daily_20210101_20230101_040d4406N_079d9959W_LST_Wind.csv'

# loading the data
new_solar_data = pd.read_csv(new_solar_file)
new_temp_hum_data = pd.read_csv(new_temp_hum_file)
new_wind_data = pd.read_csv(new_wind_file)

# displaying the first few rows of each dataset
new_solar_data.head(), new_temp_hum_data.head(), new_wind_data.head()  


#%%

# merging the datasets based on the common date columns (YEAR, MO, DY)
combined_data = pd.merge(new_solar_data, new_temp_hum_data, on=['YEAR', 'MO', 'DY'])
combined_data = pd.merge(combined_data, new_wind_data, on=['YEAR', 'MO', 'DY'])

# displaying the first few rows of the combined dataset
combined_data.head()  


#%%

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# manually constructing the date string for each row
combined_data['DATE_STR'] = combined_data['YEAR'].astype(str) + '-' + \
                            combined_data['MO'].astype(str).str.zfill(2) + '-' + \
                            combined_data['DY'].astype(str).str.zfill(2)

# converting the 'DATE_STR' to a datetime object
try:
    combined_data['DATE'] = pd.to_datetime(combined_data['DATE_STR'], format='%Y-%m-%d', errors='raise')
    conversion_success = True
    conversion_error_message = ""
except Exception as e:
    conversion_success = False
    conversion_error_message = str(e)

(conversion_success, combined_data[['DATE_STR', 'DATE']].head() if conversion_success else conversion_error_message)

# creating a datetime column for time-series analysis
#combined_data['DATE'] = pd.to_datetime(combined_data[['YEAR', 'MO', 'DY']], errors='raise')

# setting the DATE column as the index
combined_data.set_index('DATE', inplace=True)

# plotting key parameters over time for deeper analysis
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(15, 20))

# solar radiation
combined_data['ALLSKY_SFC_SW_DWN'].plot(ax=axes[0], color='orange')
axes[0].set_title('Daily Solar Radiation')
axes[0].set_ylabel('Solar Radiation')
axes[0].xaxis.set_major_locator(mdates.MonthLocator())
axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# wind Speed
combined_data['WS2M'].plot(ax=axes[1], color='blue')
axes[1].set_title('Daily Wind Speed at 2 Meters')
axes[1].set_ylabel('Wind Speed (m/s)')
axes[1].xaxis.set_major_locator(mdates.MonthLocator())
axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# temperature
combined_data['T2M'].plot(ax=axes[2], color='red')
axes[2].set_title('Daily Temperature at 2 Meters')
axes[2].set_ylabel('Temperature (°C)')
axes[2].xaxis.set_major_locator(mdates.MonthLocator())
axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# relative humidity
combined_data['RH2M'].plot(ax=axes[3], color='green')
axes[3].set_title('Daily Relative Humidity at 2 Meters')
axes[3].set_ylabel('Relative Humidity (%)')
axes[3].xaxis.set_major_locator(mdates.MonthLocator())
axes[3].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# improving layout
plt.tight_layout()
plt.show()


#%%

import pandas as pd

# correcting the datetime conversion
combined_data['DATE'] = pd.to_datetime(combined_data[['YEAR', 'MO', 'DY']].astype(str).agg('-'.join, axis=1))

# setting the DATE column as the index
combined_data.set_index('DATE', inplace=True)

# re-plotting the key parameters over time for deeper analysis
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(15, 20))

# solar radiation
combined_data['ALLSKY_SFC_SW_DWN'].plot(ax=axes[0], color='orange')
axes[0].set_title('Daily Solar Radiation')
axes[0].set_ylabel('Solar Radiation')
axes[0].xaxis.set_major_locator(mdates.MonthLocator())
axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# wind speed
combined_data['WS2M'].plot(ax=axes[1], color='blue')
axes[1].set_title('Daily Wind Speed at 2 Meters')
axes[1].set_ylabel('Wind Speed (m/s)')
axes[1].xaxis.set_major_locator(mdates.MonthLocator())
axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# temperature
combined_data['T2M'].plot(ax=axes[2], color='red')
axes[2].set_title('Daily Temperature at 2 Meters')
axes[2].set_ylabel('Temperature (°C)')
axes[2].xaxis.set_major_locator(mdates.MonthLocator())
axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# relative humidity
combined_data['RH2M'].plot(ax=axes[3], color='green')
axes[3].set_title('Daily Relative Humidity at 2 Meters')
axes[3].set_ylabel('Relative Humidity (%)')
axes[3].xaxis.set_major_locator(mdates.MonthLocator())
axes[3].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# improving layout
plt.tight_layout()
plt.show()

# %%
