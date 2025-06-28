# This file is part of cph-bib-watcher.
# Copyright (c) 2025 Daniel Pina.
# Licensed under the MIT License. See the LICENSE file in the project root for details.

import requests
import logging
import time
import os
from config import BOT_TOKEN, CHAT_ID, CHECK_INTERVAL_SECONDS
from utils import count_csv_entries

# Shared state (set externally)
last_check_time = None
bib_count = 0


def send_message(message):
    """Send a plain or HTML-formatted message via Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code != 200:
            logging.error(f"Telegram response error: {response.text}")
    except Exception as e:
        logging.error(f"Telegram exception: {e}")


def listen_for_commands():
    """Poll Telegram for new commands and respond accordingly."""
    logging.info("📬 Listening for Telegram commands...")
    last_update_id = None

    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            if last_update_id is not None:
                url += f"?offset={last_update_id}"

            response = requests.get(url, timeout=10)
            data = response.json()
            updates = data.get("result", [])

            for update in updates:
                update_id = update.get("update_id")
                message = update.get("message", {})
                text = message.get("text", "")
                chat_id = str(message.get("chat", {}).get("id", ""))

                if chat_id != CHAT_ID:
                    continue

                if text.strip().lower() == "/status":
                    reply = (
                        f"🟢 Bib monitor is running\n"
                        f"⏱️ Last checked: {last_check_time or 'N/A'}\n"
                        f"⏳ Check interval: {CHECK_INTERVAL_SECONDS} seconds\n"
                        f"📊 Bibs found since startup: {bib_count}"
                    )
                    send_message(reply)

                elif text.strip().lower() == "/seen":
                    count = count_csv_entries()
                    reply = f"👀 Bibs recorded so far: {count}"
                    send_message(reply)

            # ✅ Move offset update *after* processing all updates
            if updates:
                last_update_id = updates[-1]["update_id"] + 1

        except Exception as e:
            logging.error(f"Command listener error: {e}")

        time.sleep(5)
