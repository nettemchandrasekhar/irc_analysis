#!/usr/bin/env python3
"""
Module: hirshfeld.py
Extracts Hirshfeld spins from Gaussian and ORCA outputs.
"""

import os, re, csv

def find_files(folder, pattern):
    return [f for f in os.listdir(folder) if re.match(pattern, f)]

def parse_hirshfeld_gaussian(lines, atom_indices):
    spins = []
    for line in lines:
        if "Hirshfeld charges and spins" in line:
            start = lines.index(line)+2
            for i in atom_indices:
                parts = lines[start+i-1].split()
                spins.append(float(parts[-1]))
            break
    return spins

def parse_hirshfeld_orca(lines, atom_indices):
    spins = []
    start = None
    for i, line in enumerate(lines):
        if "Hirshfeld Population Analysis" in line:
            start = i+3
            break
    if start:
        for i in atom_indices:
            parts = lines[start+i-1].split()
            spins.append(float(parts[-1]))
    return spins

def extract_hirshfeld(folder, pattern, atom_indices, parser, output_csv):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    data_out = []

    files = find_files(folder, pattern)
    for fn in files:
        with open(os.path.join(folder, fn)) as f:
            lines = f.readlines()

        spins = parser(lines, atom_indices)
        data_out.append([fn] + spins)

    # Save CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["File"] + [f"Atom{i}" for i in atom_indices]
        writer.writerow(header)
        writer.writerows(data_out)
    print("CSV saved to:", output_csv)
