# This file is part of cph-bib-watcher.
# Copyright (c) 2025 Daniel Pina.
# Licensed under the MIT License. See the LICENSE file in the project root for details.

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# App-specific settings
CSV_FILE = "bibs.csv"
LOG_FILE = "cph.log"
CHECK_INTERVAL_SECONDS = 300  # 5 minutes
URL = "https://secure.onreg.com/onreg2/bibexchange/?eventid=6736&language=us"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
