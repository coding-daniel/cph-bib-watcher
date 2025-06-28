# This file is part of cph-bib-watcher.
# Copyright (c) 2025 Daniel Pina.
# Licensed under the MIT License. See the LICENSE file in the project root for details.

import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get credentials from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Check they're loaded
if not BOT_TOKEN or not CHAT_ID:
    print("❌ BOT_TOKEN or CHAT_ID not found in .env file.")
    exit(1)

# Send test message
message = "🚀 Test message from the CopenhagenHM bot (via .env)!"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "HTML"
}

response = requests.post(url, data=payload)

if response.status_code == 200:
    print("✅ Message sent successfully!")
else:
    print("❌ Failed to send message:")
    print(response.text)
