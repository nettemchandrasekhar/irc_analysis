#!/usr/bin/env python3
"""
Module: dipoles.py
Extracts dipole moments from Gaussian and ORCA IRC outputs.
"""

import os, re
import numpy as np
import csv

BOHR_TO_ANG = 0.529177

def find_files(folder, pattern):
    files = [f for f in os.listdir(folder) if re.match(pattern, f)]
    def sort_key(fn):
        m = re.search(r'([+-])(\d+)', fn)
        return int(m.group(2)) * (-1 if m.group(1) == '-' else 1) if m else 0
    return sorted(files, key=sort_key)

def parse_dipole_gaussian(lines):
    for i, line in enumerate(lines):
        if "Dipole moment" in line:
            nums = re.findall(r"[-+]?\d*\.\d+|\d+", lines[i+1])
            return tuple(map(float, nums))
    return None

def parse_dipole_orca(lines):
    # ORCA uses "TOTAL DIPOLE MOMENT" line
    for line in lines:
        if "TOTAL DIPOLE MOMENT" in line:
            nums = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            return tuple(map(float, nums[-3:]))
    return None

def get_last_coordinates(lines):
    coords = []
    for line in reversed(lines):
        m = re.match(r'\s*([A-Za-z]{1,2})\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)', line)
        if m: coords.append((m.group(1), float(m.group(2)), float(m.group(3)), float(m.group(4))))
        elif coords: break
    return list(reversed(coords)) if coords else None

def project_dipole(mu_vec, coords, indices):
    """Project dipole along O-H-O axis"""
    O, H, O2 = [np.array(coords[i-1][1:]) for i in indices]
    axis = (H - O) + (O2 - H)
    axis /= np.linalg.norm(axis)
    return float(np.dot(mu_vec, axis))

def extract_and_save(folder, pattern, indices, parser, output_csv):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    data_out = []

    files = find_files(folder, pattern)
    for fn in files:
        with open(os.path.join(folder, fn)) as f:
            lines = f.readlines()

        dip = parser(lines)
        coords = get_last_coordinates(lines)
        mu_proj = None
        if dip and coords:
            mu_proj = project_dipole(np.array(dip), coords, indices)

        m = re.search(r'([+-])(\d+)', fn)
        sign, num = (-1 if m.group(1) == '-' else 1, int(m.group(2))) if m else (1, 0)
        rc = sign * num * 0.01  # step * Bohr to Angstrom can adjust

        data_out.append([fn, sign*num, rc, *(dip or (None,None,None)), mu_proj])

    # Save CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["File","Index","RC","MuX","MuY","MuZ","Mu_proj"])
        writer.writerows(data_out)
    print("CSV saved to:", output_csv)
