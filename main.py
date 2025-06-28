# This file is part of cph-bib-watcher.
# Copyright (c) 2025 Daniel Pina.
# Licensed under the MIT License. See the LICENSE file in the project root for details.

import logging
import threading
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler

import telegram_client
from config import LOG_FILE, CHECK_INTERVAL_SECONDS
from watcher import fetch_bibs, load_saved_bibs, append_bib_to_csv
from telegram_client import send_message


# Runtime state
last_check_time = None
bib_count = 0


def setup_logging():
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler = RotatingFileHandler(LOG_FILE, maxBytes=512 * 1024, backupCount=5, encoding='utf-8')
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


def main():
    global last_check_time, bib_count
    setup_logging()
    seen_bibs = load_saved_bibs()

    logging.info("📡 Bib monitor started.")
    send_message("🏁 CPH Half 2025 bib monitor is now running!")

    # Start Telegram command listener in background
    threading.Thread(target=telegram_client.listen_for_commands, daemon=True).start()

    while True:
        last_check_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        telegram_client.last_check_time = last_check_time

        logging.info("Check started. Fetching latest bibs from the site...")
        bibs = fetch_bibs()
        prev_count = bib_count
        new_bibs_found = 0

        if not bibs:
            logging.info("No bibs found on the page.")
        else:
            logging.info(f"{len(bibs)} bib(s) found on the page. Checking for new entries...")

        for bib in bibs:
            bib_key = f"{bib['event_name']}|{bib['transfer_id']}"
            if bib_key not in seen_bibs:
                seen_bibs.add(bib_key)
                append_bib_to_csv(bib)
                bib_count += 1
                new_bibs_found += 1
                telegram_client.bib_count = bib_count

                message = (
                    f"🎉 <b>New Bib Available!</b>\n"
                    f"🏁 Event: {bib['event_name']}\n"
                    f"🆔 Transfer ID: {bib['transfer_id']}\n"
                    f"💰 Price: {bib['price']}\n"
                    f"📌 Status: {bib['status']}\n"
                    f"🕒 Found at: {last_check_time}"
                )
                print(message)
                logging.info(f"New bib listed: {bib}")
                send_message(message)

        if bibs and new_bibs_found == 0:
            logging.info("No new bibs since last check.")

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
