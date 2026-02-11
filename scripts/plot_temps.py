#!/usr/bin/env python3
"""
plot_temps.py

Read `data/temperatures.csv` and produce two plots:
- histogram of Celsius readings
- time series (index vs Celsius)

Usage: python scripts/plot_temps.py
"""
import os
import pandas as pd
import matplotlib.pyplot as plt


def main():
    data_path = os.path.join('data', 'temperatures.csv')
    if not os.path.exists(data_path):
        print(f"Data file not found: {data_path}")
        return

    df = pd.read_csv(data_path)
    # ensure numeric
    df['celsius'] = pd.to_numeric(df['celsius'], errors='coerce')

    plt.figure(figsize=(8, 4))
    plt.hist(df['celsius'].dropna(), bins=20, color='C0', edgecolor='black')
    plt.title('Histogram of Celsius readings')
    plt.xlabel('Celsius')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('data/histogram_celsius.png')
    print('Wrote data/histogram_celsius.png')

    plt.figure(figsize=(10, 4))
    plt.plot(df['index'], df['celsius'], marker='.', linestyle='-', color='C1')
    plt.title('Temperature Time Series')
    plt.xlabel('Index')
    plt.ylabel('Celsius')
    plt.tight_layout()
    plt.savefig('data/series_celsius.png')
    print('Wrote data/series_celsius.png')


if __name__ == '__main__':
    main()
