# Weather Data Visualizer
# Name : Dev Kaushik
# Date : 28/11/2025
# Simple python program to read weather data and make some graphs

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# reading the csv file
df = pd.read_csv("weather_data.csv")

print("----- FIRST FEW ROWS -----")
print(df.head())

print("----- INFO -----")
print(df.info())

print("----- DESCRIPTION -----")
print(df.describe())

# fixing the date column
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# removing rows where date is missing
df = df.dropna(subset=["date"])

# filling missing values
df["temperature"] = df["temperature"].fillna(df["temperature"].mean())
df["rainfall"] = df["rainfall"].fillna(0)
df["humidity"] = df["humidity"].fillna(df["humidity"].mean())

# extracting month number
df["month"] = df["date"].dt.month

# temperature stats (my own calculation)
mean_temp = np.mean(df["temperature"])
min_temp = np.min(df["temperature"])
max_temp = np.max(df["temperature"])
std_temp = np.std(df["temperature"])

print("\nTemperature Stats :")
print("Mean:", mean_temp)
print("Min:", min_temp)
print("Max:", max_temp)
print("Std Dev:", std_temp)

# monthly mean temps
monthly_mean = df.groupby("month")["temperature"].mean()
print("\nMonthly Avg Temp :")
print(monthly_mean)

# line graph for temp trend
plt.figure(figsize=(10,4))
plt.plot(df["date"], df["temperature"])
plt.title("Daily Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temp (C)")
plt.tight_layout()
plt.savefig("daily_temperature.png")
plt.close()

# rainfall bar graph
monthly_rain = df.groupby("month")["rainfall"].sum()
plt.figure(figsize=(8,4))
plt.bar(monthly_rain.index, monthly_rain.values)
plt.title("Rainfall Month Wise")
plt.xlabel("Month")
plt.ylabel("Rainfall")
plt.tight_layout()
plt.savefig("monthly_rainfall.png")
plt.close()

# scatter plot humidity vs temp
plt.figure(figsize=(8,4))
plt.scatter(df["temperature"], df["humidity"])
plt.title("Humidity vs Temp")
plt.xlabel("Temperature")
plt.ylabel("Humidity")
plt.tight_layout()
plt.savefig("humidity_vs_temperature.png")
plt.close()

# two plots in one just for comparison
plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.plot(df["date"], df["temperature"])
plt.title("Temperature Trend")

plt.subplot(1,2,2)
plt.scatter(df["temperature"], df["humidity"])
plt.title("Temp vs Humidity")

plt.tight_layout()
plt.savefig("combined_plots.png")
plt.close()

# monthly calculations together
month_data = df.groupby("month").agg({
    "temperature": "mean",
    "rainfall": "sum",
    "humidity": "mean"
})

print("\nMonthly Data:")
print(month_data)

# exporting cleaned data
df.to_csv("cleaned_weather_data.csv", index=False)
print("\nCleaned file saved as cleaned_weather_data.csv")
print("All plots saved.")
