import pandas as pd
import sys

# this prints the actual python debugger
print(sys.executable) 
# prints pandas version
print(pd.__version__)

# ---- READING DATA ----
print("---- READING DATA ----")
df1 = pd.read_csv("testbed_01.csv")
df2 = pd.read_csv("testbed_02.csv")
print(df1.head())      # first 5 rows
print(df1.columns)     # column names
print(df1.shape)       # (rows, columns)
print(df1.index)       # returns row labels
print(df1.dtypes)      # data type of each column
print(df1)
print(df2)
# this functions aligns data by column label ( column name)
combined = pd.concat([df1, df2])
print(combined)

# Define what each messy column name should become
# This normalized the names and concatenates correctly
rename_map_df1 = {
    "Date": "date",
    "Temp_C": "ambient_temp",
    "Pressure_kPa": "pressure_kpa",
    "RPM": "rpm",
    "Power_kW": "power_kw"
}

rename_map_df2 = {
    "date": "date",
    "amb_temp": "ambient_temp",
    "Pressure_kPa": "pressure_kpa",
    "rpm": "rpm",
    "power_output_kw": "power_kw"
}

df1 = df1.rename(columns=rename_map_df1)
df2 = df2.rename(columns=rename_map_df2)

# Prints the labels of dataset
print(df1.columns)
print(df2.columns)

# this functions aligns data by column label ( column name)
combined = pd.concat([df1, df2])
print(combined)


# ---- HANDLING MISSING READING ----
print("---- HANDLING MISSING READING ----")
# without this df1 & df2 would keep their original 
# numbering reseting from 0 to n
combined = pd.concat([df1, df2], ignore_index=True)
# True/False table showing where values are missing
print(combined.isna())          
print(combined.isna().sum())    # count of missing values per column

# How to handle those gaps? 
# It's important to fill those gaps when data is being 
# retrieve, more for test beds of gas turbines
# Here are some options:

# Option 1: Notify where is the missing value
# clean_drop = combined.dropna()

# Option 2: Fill with a fixed value 
# clean_fixed = combined.fillna(10)

# Option 3: Carry the last known value forward
# clean_ffill = combined.ffill()

# Option 4: Interpolation
# Tries to numerically estimate values between two points
# First we need to correct for any value that 
# is an string like the date 
combined["date"] = pd.to_datetime(combined["date"])
clean_interp = combined.interpolate() # this alone does not work
print(combined.dtypes)
print(clean_interp.dtypes)
print(clean_interp)


# ---- OUTLIER DETECTION ----
print("---- OUTLIER DETECTION ----")
# Flagging reading that look physically suspicious
# for example a pressure or power output way outside
# the normal range
# A simple defensible method: flag outside a mean +/- 
# 3 standard deviations
mean = clean_interp["power_kw"].mean()
std = clean_interp["power_kw"].std()
lower_bound = mean - 3*std
upper_bound = mean + 3*std

outliers = clean_interp[(clean_interp["power_kw"] < lower_bound) |
                        (clean_interp["power_kw"] > upper_bound)]
print(outliers)


# ---- EXPORTING AND VISUALIZATION ----
# For exporting data we use the following function
clean_interp.to_csv("combined_clean.csv", index=False)
# The index=False is important, ONLY if indexing is 
# not neccesary 

# For a quick visualization matplotlib is used
import matplotlib.pyplot as plt
plt.figure(figsize=(8,5))
plt.plot(clean_interp["date"], clean_interp["power_kw"], marker="o", label="Power Output (kW)")
plt.plot(clean_interp["date"], clean_interp["ambient_temp"] * 100, marker="o", label="Ambient Temp x100 (scaled)")

plt.xlabel("Date")
plt.ylabel("Value")
plt.title("Test Bed Performance Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

fig, ax1 = plt.subplots(figsize=(10, 6))

# Left axis - Power
ax1.set_xlabel("Date")
ax1.set_ylabel("Power Output (kW)", color="blue")
ax1.plot(clean_interp["date"], clean_interp["power_kw"], 
         marker="o", color="blue", label="Power (kW)")
ax1.tick_params(axis="y", labelcolor="blue")

# Right axis - Temperature (shares same x axis)
ax2 = ax1.twinx()
ax2.set_ylabel("Ambient Temperature (°C)", color="red")
ax2.plot(clean_interp["date"], clean_interp["ambient_temp"], 
         marker="s", color="red", label="Ambient Temp (°C)")
ax2.tick_params(axis="y", labelcolor="red")

plt.title("Test Bed Performance — Power vs Ambient Temperature")
fig.tight_layout()
plt.show()