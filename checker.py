import requests
from bs4 import BeautifulSoup
import time
import csv
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# --- Load secrets from .env ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# --- Configuration ---
URL = "https://secure.onreg.com/onreg2/bibexchange/?eventid=6736&language=us"
HEADERS = {"User-Agent": "Mozilla/5.0"}
CSV_FILE = "bibs.csv"
LOG_FILE = "cph.log"
CHECK_INTERVAL_SECONDS = 300  # 5 minutes
# -----------------------

# --- Logging setup ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            logging.error(f"Telegram response error: {response.text}")
    except Exception as e:
        logging.error(f"Telegram exception: {e}")

def fetch_bibs():
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
    seen = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                key = "|".join(row[:2])  # event + transfer ID
                seen.add(key)
    return seen

def append_bib_to_csv(bib):
    timestamp = datetime.now().isoformat(timespec='seconds')
    new_row = [bib['event_name'], bib['transfer_id'], bib['price'], bib['status'], timestamp]
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Event", "Transfer ID", "Price", "Status", "Timestamp"])
        writer.writerow(new_row)

def main():
    seen_bibs = load_saved_bibs()
    logging.info("📡 Bib monitor started.")
    send_telegram_message("🏁 CPH Half 2025 bib monitor is now running!")

    while True:
        bibs = fetch_bibs()
        for bib in bibs:
            bib_key = f"{bib['event_name']}|{bib['transfer_id']}"
            if bib_key not in seen_bibs:
                seen_bibs.add(bib_key)
                append_bib_to_csv(bib)

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message = (
                    f"🎉 <b>New Bib Available!</b>\n"
                    f"🏁 Event: {bib['event_name']}\n"
                    f"🆔 Transfer ID: {bib['transfer_id']}\n"
                    f"💰 Price: {bib['price']}\n"
                    f"📌 Status: {bib['status']}\n"
                    f"🕒 Found at: {timestamp}"
                )
                print(message)
                logging.info(f"New bib listed: {bib}")
                send_telegram_message(message)

        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
