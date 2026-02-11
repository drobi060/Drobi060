#!/usr/bin/env python3
import re, sys, csv, math, statistics, os
from collections import Counter

"""
parse_temps.py

Parse a text blob containing temperatures like "61.0°C +63.0°C ..." from a file or stdin,
produce basic stats and write `data/temperatures.csv` (Celsius,Fahrenheit) and
`data/summary.csv`.
Usage: python parse_temps.py [input.txt]
If no file is given the script reads stdin.
"""


def read_input():
    if len(sys.argv) > 1:
        return open(sys.argv[1], "r", encoding="utf-8").read()
    return sys.stdin.read()


def extract_celsius(text):
    # match numbers optionally signed, with optional decimals, followed by optional space and °C or C
    nums = re.findall(r"[+-]?\d+(?:\.\d+)?(?=\s*°?C)", text)
    return [float(x) for x in nums]


def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0


def histogram(vals, width=5):
    if not vals:
        return {}
    lo = int(math.floor(min(vals) / width) * width)
    hi = int(math.ceil(max(vals) / width) * width)
    bins = Counter(((int(math.floor((v - lo) / width)) * width) + lo for v in vals))
    # return ordered list of (range_label, count)
    out = []
    for start in range(lo, hi, width):
        label = f"{start}..{start+width-0.0001}"
        out.append((label, bins.get(start, 0)))
    return out


def main():
    text = read_input()
    c_vals = extract_celsius(text)
    if not c_vals:
        print("No Celsius values found in input.")
        return
    f_vals = [c_to_f(c) for c in c_vals]

    # basic stats
    n = len(c_vals)
    mn, mx = min(c_vals), max(c_vals)
    mean = statistics.mean(c_vals)
    median = statistics.median(c_vals)
    pstdev = statistics.pstdev(c_vals) if n >= 1 else 0.0
    sstdev = statistics.stdev(c_vals) if n >= 2 else float("nan")

    # print summary
    print(f"Count: {n}")
    print(f"Min: {mn:.2f} °C, Max: {mx:.2f} °C")
    print(f"Mean: {mean:.3f} °C, Median: {median:.3f} °C")
    print(f"Population stddev: {pstdev:.3f} °C, Sample stddev: {sstdev:.3f} °C")
    print()

    # histogram (5°C bins)
    print("Histogram (5°C bins):")
    for label, cnt in histogram(c_vals, width=5):
        print(f"  {label}: {cnt}")
    print()

    # ensure data dir
    os.makedirs('data', exist_ok=True)

    # write CSV (to data/temperatures.csv)
    out_name = os.path.join('data', 'temperatures.csv')
    with open(out_name, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["index", "celsius", "fahrenheit"])
        for i, (c, f) in enumerate(zip(c_vals, f_vals), start=1):
            w.writerow([i, f"{c:.2f}", f"{f:.2f}"])

    # write summary CSV
    vals_f = f_vals
    sum_c = sum(c_vals)
    sum_f = sum(vals_f)
    mean_f = statistics.mean(vals_f)
    out_summary = os.path.join('data', 'summary.csv')
    with open(out_summary, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['metric','value','units'])
        w.writerow(['count', n, 'items'])
        w.writerow(['sum', f"{sum_c:.2f}", '°C'])
        w.writerow(['mean', f"{mean:.4f}", '°C'])
        w.writerow(['median', f"{median:.2f}", '°C'])
        w.writerow(['min', f"{mn:.2f}", '°C'])
        w.writerow(['max', f"{mx:.2f}", '°C'])
        w.writerow(['population_stdev', f"{pstdev:.4f}", '°C'])
        w.writerow(['sum_f', f"{sum_f:.2f}", '°F'])
        w.writerow(['mean_f', f"{mean_f:.4f}", '°F'])

    print(f"Wrote {out_name} ({n} rows) and {out_summary}.")


if __name__ == "__main__":
    main()
