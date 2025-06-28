# This file is part of cph-bib-watcher.
# Copyright (c) 2025 Daniel Pina.
# Licensed under the MIT License. See the LICENSE file in the project root for details.

import requests
from bs4 import BeautifulSoup
import csv
import os
import logging
from datetime import datetime
from config import URL, HEADERS, CSV_FILE


def fetch_bibs():
    """Fetch the list of bibs from the target URL."""
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Failed to fetch page: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Check for "no bibs" message
    no_bibs = soup.find("b", string="There are currently no race numbers for sale. Try again later.")
    if no_bibs:
        logging.info("No bibs currently available.")
        return []

    table = soup.select_one("table.table")
    if not table:
        logging.warning("Bib table not found. HTML structure might have changed.")
        return []

    bibs = []
    rows = table.find_all("tr")[1:]  # Skip header

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 4:
            logging.warning("Skipping malformed row (not enough columns)")
            continue

        try:
            event_name = cells[0].get_text(strip=True)
            transfer_id = cells[1].get_text(strip=True)
            price = cells[2].get_text(strip=True)
            status_link = cells[3].find("a")
            status = status_link.get_text(strip=True) if status_link else cells[3].get_text(strip=True)

            bib = {
                "event_name": event_name,
                "transfer_id": transfer_id,
                "price": price,
                "status": status
            }
            bibs.append(bib)
        except Exception as e:
            logging.error(f"Failed to parse row: {e}")
            continue

    return bibs


def load_saved_bibs():
    """Load previously seen bib keys from CSV."""
    seen = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                key = "|".join(row[:2])  # event + transfer ID
                seen.add(key)
    return seen


def append_bib_to_csv(bib):
    """Append a new bib entry to the CSV file."""
    timestamp = datetime.now().isoformat(timespec='seconds')
    new_row = [bib['event_name'], bib['transfer_id'], bib['price'], bib['status'], timestamp]
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Event", "Transfer ID", "Price", "Status", "Timestamp"])
        writer.writerow(new_row)
