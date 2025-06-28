# This file is part of cph-bib-watcher.
# Copyright (c) 2025 Daniel Pina.
# Licensed under the MIT License. See the LICENSE file in the project root for details.

import os
import csv
from config import CSV_FILE


def count_csv_entries():
    """Count the number of bibs recorded in the CSV file (excluding header)."""
    if not os.path.exists(CSV_FILE):
        return 0

    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        return sum(1 for _ in reader)
