#!/usr/bin/env python3
from dipoles import extract_and_save, parse_dipole_gaussian, parse_dipole_orca
from hirshfeld import extract_hirshfeld, parse_hirshfeld_gaussian, parse_hirshfeld_orca

# Gaussian dipoles
extract_and_save(
    folder="../data/gaussian",
    pattern=r"1b_IRC_TS[+-]\d+\.log",
    indices=[88,89,49],
    parser=parse_dipole_gaussian,
    output_csv="../results/csv/dipole_gaussian.csv"
)

# ORCA dipoles
extract_and_save(
    folder="../data/orca",
    pattern=r"TS[+-]\d+\.out",
    indices=[88,89,49],
    parser=parse_dipole_orca,
    output_csv="../results/csv/dipole_orca.csv"
)

# Gaussian Hirshfeld
extract_hirshfeld(
    folder="../data/gaussian",
    pattern=r"1b_IRC_TS[+-]\d+\.log",
    atom_indices=[88,89,49],
    parser=parse_hirshfeld_gaussian,
    output_csv="../results/csv/hirshfeld_gaussian.csv"
)

# ORCA Hirshfeld
extract_hirshfeld(
    folder="../data/orca",
    pattern=r"TS[+-]\d+\.out",
    atom_indices=[88,89,49],
    parser=parse_hirshfeld_orca,
    output_csv="../results/csv/hirshfeld_orca.csv"
)
