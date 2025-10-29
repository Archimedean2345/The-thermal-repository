# ═══════════════════════════════════════════════════════════════
# PYTHON ENGINEERING CHEAT SHEET
# Data Analysis, Visualization & Modeling for Engineering
# ═══════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────
# 1. ESSENTIAL IMPORTS
# ─────────────────────────────────────────────────────────────
import numpy as np                      # Numerical computing
import pandas as pd                     # Data manipulation
import matplotlib.pyplot as plt         # Basic plotting
import seaborn as sns                   # Statistical visualization
from scipy import optimize, interpolate, integrate  # Scientific computing
from scipy.stats import norm, t, linregress        # Statistics

# ─────────────────────────────────────────────────────────────
# 2. NUMPY - Numerical Arrays
# ─────────────────────────────────────────────────────────────
# Create arrays
arr = np.array([1, 2, 3, 4])           # 1D array
arr2d = np.array([[1,2], [3,4]])       # 2D array
zeros = np.zeros(10)                    # Array of zeros
ones = np.ones((3, 4))                  # 3x4 array of ones
linspace = np.linspace(0, 10, 100)     # 100 points from 0 to 10
arange = np.arange(0, 10, 0.5)         # 0 to 10, step 0.5

# Array operations
arr.mean(), arr.std(), arr.sum()        # Statistics
arr.max(), arr.min(), arr.argmax()      # Max, min, index of max
arr.reshape(2, 2)                       # Change shape
arr1 + arr2, arr1 * arr2                # Element-wise operations
np.dot(arr1, arr2)                      # Dot product
arr[arr > 5]                            # Boolean indexing

# Math functions
np.sin(arr), np.cos(arr), np.exp(arr)
np.log(arr), np.sqrt(arr), np.power(arr, 2)

# ─────────────────────────────────────────────────────────────
# 3. PANDAS - Data Manipulation
# ─────────────────────────────────────────────────────────────
# Read/Write data
df = pd.read_csv('data.csv')           # Read CSV
df = pd.read_excel('data.xlsx')        # Read Excel
df.to_csv('output.csv', index=False)   # Write CSV

# Create DataFrame
df = pd.DataFrame({
    'pressure': [100, 101, 102],
    'temp': [300, 305, 310],
    'velocity': [150, 155, 160]
})

# View data
df.head(10)                             # First 10 rows
df.tail()                               # Last 5 rows
df.info()                               # Data types & nulls
df.describe()                           # Statistical summary
df.shape                                # (rows, columns)
df.columns                              # Column names

# Select data
df['pressure']                          # Single column
df[['pressure', 'temp']]               # Multiple columns
df.loc[0]                              # Row by label
df.iloc[0]                             # Row by position
df.loc[df['pressure'] > 100]           # Filter rows
df.query('pressure > 100 & temp < 310') # SQL-like filtering

# Data manipulation
df['ratio'] = df['pressure'] / df['temp']  # New column
df.drop('column', axis=1)              # Delete column
df.dropna()                            # Remove NaN rows
df.fillna(0)                           # Fill NaN with 0
df.sort_values('pressure')             # Sort by column
df.groupby('category').mean()          # Group statistics

# Merge/Join
pd.concat([df1, df2])                  # Stack DataFrames
pd.merge(df1, df2, on='id')            # SQL-like join

# ─────────────────────────────────────────────────────────────
# 4. MATPLOTLIB - Plotting
# ─────────────────────────────────────────────────────────────
# Basic plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', label='Data', linewidth=2)
plt.xlabel('X axis [units]', fontsize=12)
plt.ylabel('Y axis [units]', fontsize=12)
plt.title('Title', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.show()

# Subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.plot(x, y1)
ax2.scatter(x, y2)

# Multiple lines
plt.plot(x, y1, 'b-', label='Line 1')
plt.plot(x, y2, 'r--', label='Line 2')
plt.plot(x, y3, 'g:', label='Line 3')

# Scatter plot
plt.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis')
plt.colorbar(label='Color scale')

# Contour plot (for 2D data)
plt.contourf(X, Y, Z, levels=20, cmap='jet')
plt.colorbar()

# Log scale
plt.semilogy(x, y)    # Log Y
plt.semilogx(x, y)    # Log X
plt.loglog(x, y)      # Both log

# ─────────────────────────────────────────────────────────────
# 5. SCIPY - Scientific Computing
# ─────────────────────────────────────────────────────────────
# Curve fitting
from scipy.optimize import curve_fit

def func(x, a, b, c):
    return a * np.exp(-b * x) + c

popt, pcov = curve_fit(func, xdata, ydata)  # Optimal parameters
y_fit = func(xdata, *popt)

# Root finding
from scipy.optimize import fsolve

def equation(x):
    return x**2 - 4

root = fsolve(equation, x0=1)  # Starting guess x0=1

# Integration
from scipy.integrate import quad, odeint

result, error = quad(lambda x: x**2, 0, 1)  # Definite integral

# ODE solver
def model(y, t):
    dydt = -0.5 * y
    return dydt

t = np.linspace(0, 10, 100)
y0 = 5
y = odeint(model, y0, t)

# Interpolation
from scipy.interpolate import interp1d

f = interp1d(x, y, kind='cubic')
x_new = np.linspace(x.min(), x.max(), 300)
y_new = f(x_new)

# Statistics
from scipy.stats import linregress

slope, intercept, r_value, p_value, std_err = linregress(x, y)

# ─────────────────────────────────────────────────────────────
# 6. ENGINEERING CALCULATIONS
# ─────────────────────────────────────────────────────────────
# Unit conversions
def psi_to_Pa(psi):
    return psi * 6894.76

def F_to_K(F):
    return (F - 32) * 5/9 + 273.15

# Fluid properties (example)
def reynolds_number(rho, V, L, mu):
    """Re = ρVL/μ"""
    return rho * V * L / mu

def mach_number(V, gamma, R, T):
    """M = V / sqrt(γRT)"""
    a = np.sqrt(gamma * R * T)  # Speed of sound
    return V / a

# Isentropic relations
def isentropic_pressure_ratio(M, gamma=1.4):
    """p0/p = (1 + (γ-1)/2 * M²)^(γ/(γ-1))"""
    return (1 + (gamma-1)/2 * M**2)**(gamma/(gamma-1))

# ─────────────────────────────────────────────────────────────
# 7. DATA ANALYSIS WORKFLOW
# ─────────────────────────────────────────────────────────────
# Load data
df = pd.read_csv('experiment_data.csv')

# Clean data
df = df.dropna()  # Remove missing values
df = df[df['pressure'] > 0]  # Remove invalid values

# Calculate derived quantities
df['mach'] = df['velocity'] / df['speed_of_sound']
df['reynolds'] = reynolds_number(df['density'], df['velocity'], 
                                  df['length'], df['viscosity'])

# Statistical analysis
mean_pressure = df['pressure'].mean()
std_pressure = df['pressure'].std()
correlation = df['pressure'].corr(df['temperature'])

# Regression
from scipy.stats import linregress
slope, intercept, r_value, _, _ = linregress(df['x'], df['y'])
df['y_fit'] = slope * df['x'] + intercept

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Raw data
axes[0,0].plot(df['time'], df['pressure'])
axes[0,0].set_xlabel('Time [s]')
axes[0,0].set_ylabel('Pressure [Pa]')
axes[0,0].grid(True)

# Plot 2: Scatter with regression
axes[0,1].scatter(df['x'], df['y'], alpha=0.5, label='Data')
axes[0,1].plot(df['x'], df['y_fit'], 'r-', label=f'Fit (R²={r_value**2:.3f})')
axes[0,1].legend()

# Plot 3: Histogram
axes[1,0].hist(df['pressure'], bins=30, edgecolor='black')
axes[1,0].set_xlabel('Pressure [Pa]')
axes[1,0].set_ylabel('Frequency')

# Plot 4: Heatmap/correlation
correlation_matrix = df[['pressure', 'temp', 'velocity']].corr()
im = axes[1,1].imshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)
axes[1,1].set_xticks(range(len(correlation_matrix)))
axes[1,1].set_yticks(range(len(correlation_matrix)))
axes[1,1].set_xticklabels(correlation_matrix.columns, rotation=45)
axes[1,1].set_yticklabels(correlation_matrix.columns)
plt.colorbar(im, ax=axes[1,1])

plt.tight_layout()
plt.savefig('analysis_report.png', dpi=300)
plt.show()

# ─────────────────────────────────────────────────────────────
# 8. USEFUL CODE PATTERNS
# ─────────────────────────────────────────────────────────────
# Loop through multiple cases
cases = [
    {'pressure': 101325, 'temp': 288},
    {'pressure': 200000, 'temp': 400},
]

results = []
for case in cases:
    result = some_calculation(case['pressure'], case['temp'])
    results.append(result)

# Error handling
try:
    result = risky_calculation(data)
except ZeroDivisionError:
    print("Division by zero!")
    result = np.nan

# List comprehension (fast)
squares = [x**2 for x in range(10)]
filtered = [x for x in data if x > threshold]

# Dictionary for lookup tables
properties = {
    'air': {'R': 287, 'gamma': 1.4},
    'helium': {'R': 2077, 'gamma': 1.66}
}
R_air = properties['air']['R']

# Save/Load numpy arrays
np.save('data.npy', array)
loaded = np.load('data.npy')

# ─────────────────────────────────────────────────────────────
# 9. FORMATTING & PRESENTATION
# ─────────────────────────────────────────────────────────────
# String formatting
pressure = 101325.7834
print(f"Pressure: {pressure:.2f} Pa")           # 101325.78
print(f"Pressure: {pressure:.2e} Pa")           # 1.01e+05
print(f"Pressure: {pressure:,.0f} Pa")          # 101,326

# LaTeX in plots (for equations)
plt.title(r'$\frac{p_0}{p} = \left(1 + \frac{\gamma-1}{2}M^2\right)^{\frac{\gamma}{\gamma-1}}$')

# Table output
print(df.to_string(index=False))  # Nice table format
print(df.to_latex())               # LaTeX table

# ─────────────────────────────────────────────────────────────
# 10. PERFORMANCE TIPS
# ─────────────────────────────────────────────────────────────
# Use vectorization (FAST)
result = np.sin(array) * np.exp(array)  # Good

# Avoid loops when possible (SLOW)
result = []
for x in array:
    result.append(np.sin(x) * np.exp(x))  # Bad

# Time your code
import time
start = time.time()
# ... code here ...
print(f"Elapsed: {time.time() - start:.3f} s")