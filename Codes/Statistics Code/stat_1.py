#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
solar_data = pd.read_csv('POWER_Point_Daily_20210101_20230101_040d4406N_079d9959W_LST_Solar.csv')
temp_hum_data = pd.read_csv('POWER_Point_Daily_20210101_20230101_040d4406N_079d9959W_LST_Temp+Hum.csv')
wind_data = pd.read_csv('POWER_Point_Daily_20210101_20230101_040d4406N_079d9959W_LST_Wind.csv')

# Data Quality Check
print("Missing Values in Solar Data:\n", solar_data.isnull().sum())
print("Missing Values in Temperature and Humidity Data:\n", temp_hum_data.isnull().sum())
print("Missing Values in Wind Data:\n", wind_data.isnull().sum())

# Summary Statistics
print("Solar Data Summary:\n", solar_data.describe())
print("Temperature and Humidity Data Summary:\n", temp_hum_data.describe())
print("Wind Data Summary:\n", wind_data.describe())

# Correlation Analysis
correlation_solar = solar_data.corr()
correlation_temp_hum = temp_hum_data.corr()
correlation_wind = wind_data.corr()
print("Correlation in Solar Data:\n", correlation_solar)
print("Correlation in Temperature and Humidity Data:\n", correlation_temp_hum)
print("Correlation in Wind Data:\n", correlation_wind)



# manually constructing the date string for each row
solar_data['DATE_STR'] = solar_data['YEAR'].astype(str) + '-' + \
                            solar_data['MO'].astype(str).str.zfill(2) + '-' + \
                            solar_data['DY'].astype(str).str.zfill(2)

# converting the 'DATE_STR' to a datetime object
try:
    solar_data['DATE'] = pd.to_datetime(solar_data['DATE_STR'], format='%Y-%m-%d', errors='raise')
    conversion_success = True
    conversion_error_message = ""
except Exception as e:
    conversion_success = False
    conversion_error_message = str(e)

(conversion_success, solar_data[['DATE_STR', 'DATE']].head() if conversion_success else conversion_error_message)



# manually constructing the date string for each row
temp_hum_data['DATE_STR'] = temp_hum_data['YEAR'].astype(str) + '-' + \
                            temp_hum_data['MO'].astype(str).str.zfill(2) + '-' + \
                            temp_hum_data['DY'].astype(str).str.zfill(2)

# converting the 'DATE_STR' to a datetime object
try:
    temp_hum_data['DATE'] = pd.to_datetime(temp_hum_data['DATE_STR'], format='%Y-%m-%d', errors='raise')
    conversion_success = True
    conversion_error_message = ""
except Exception as e:
    conversion_success = False
    conversion_error_message = str(e)

(conversion_success, temp_hum_data[['DATE_STR', 'DATE']].head() if conversion_success else conversion_error_message)



# manually constructing the date string for each row
wind_data['DATE_STR'] = wind_data['YEAR'].astype(str) + '-' + \
                            wind_data['MO'].astype(str).str.zfill(2) + '-' + \
                            wind_data['DY'].astype(str).str.zfill(2)

# converting the 'DATE_STR' to a datetime object
try:
    wind_data['DATE'] = pd.to_datetime(wind_data['DATE_STR'], format='%Y-%m-%d', errors='raise')
    conversion_success = True
    conversion_error_message = ""
except Exception as e:
    conversion_success = False
    conversion_error_message = str(e)

(conversion_success, wind_data[['DATE_STR', 'DATE']].head() if conversion_success else conversion_error_message)



# Time Series Analysis
# Converting to datetime and setting as index
#solar_data['DATE'] = pd.to_datetime(solar_data[['YEAR', 'MO', 'DY']])
#temp_hum_data['DATE'] = pd.to_datetime(temp_hum_data[['YEAR', 'MO', 'DY']])
#wind_data['DATE'] = pd.to_datetime(wind_data[['YEAR', 'MO', 'DY']])


solar_data.set_index('DATE', inplace=True)
temp_hum_data.set_index('DATE', inplace=True)
wind_data.set_index('DATE', inplace=True)

# Identify non-numeric columns
non_numeric_columns = solar_data.select_dtypes(include=['object']).columns

# Convert columns that should be numeric but are typed as 'object'
for col in non_numeric_columns:
    solar_data[col] = pd.to_numeric(solar_data[col], errors='coerce')

# Now, attempt to resample again
monthly_avg_solar = solar_data.resample('M').mean()


# Identify non-numeric columns
non_numeric_columns = temp_hum_data.select_dtypes(include=['object']).columns

# Convert columns that should be numeric but are typed as 'object'
for col in non_numeric_columns:
    temp_hum_data[col] = pd.to_numeric(temp_hum_data[col], errors='coerce')

# Now, attempt to resample again
monthly_avg_temp_hum = temp_hum_data.resample('M').mean()


# Identify non-numeric columns
non_numeric_columns = wind_data.select_dtypes(include=['object']).columns

# Convert columns that should be numeric but are typed as 'object'
for col in non_numeric_columns:
    wind_data[col] = pd.to_numeric(wind_data[col], errors='coerce')

# Now, attempt to resample again
monthly_avg_wind = wind_data.resample('M').mean()
# Monthly averages
#monthly_avg_solar = solar_data.resample('M').mean()
#monthly_avg_temp_hum = temp_hum_data.resample('M').mean()
#monthly_avg_wind = wind_data.resample('M').mean()

# Extreme Value Analysis
extreme_temp = temp_hum_data['T2M'].nlargest(5)
extreme_wind = wind_data['WS10M'].nlargest(5)

# Data Visualization
# Plotting time series data
plt.figure(figsize=(12, 6))
plt.plot(monthly_avg_solar['ALLSKY_SFC_SW_DWN'], label='Solar Irradiance')
plt.plot(monthly_avg_temp_hum['T2M'], label='Temperature')
plt.plot(monthly_avg_wind['WS10M'], label='Wind Speed')
plt.title('Monthly Average Solar Irradiance, Temperature, and Wind Speed')
plt.xlabel('Date')
plt.ylabel('Values')
plt.legend()
plt.show()



# Merge the dataframes on the 'DATE' index
combined_data = pd.merge(solar_data, temp_hum_data, on='DATE')
combined_data = pd.merge(combined_data, wind_data, on='DATE')

# Compute the correlation matrix of the combined dataframe
combined_correlation = combined_data.corr()

# Visualize the combined correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(combined_correlation, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix for Combined Solar, Temperature and Humidity, and Wind Data')
plt.show()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_solar, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix for Solar Data')
plt.show()

# Plotting correlations as heatmaps
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_temp_hum, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix for Temperature and Humidity Data')
plt.show()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_wind, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix for Wind Data')
plt.show()

# %%
