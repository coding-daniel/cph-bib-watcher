# 📡 CPH Bib Watcher

<p align="center">
  <img src="assets/cph-half-logo2.png" alt="CPH Half Marathon" height="200" />
</p>

A lightweight Python script that monitors the **Copenhagen Half Marathon 2025 bib exchange page** and sends Telegram alerts when race numbers become available.

---

## ✨ Features

- 🕵️ Periodically checks the official CPH Half 2025 bib exchange page
- 📬 Sends instant Telegram messages when new bibs appear
- 💾 Saves results to a local CSV file with timestamps
- 📊 Logs all activity to `cph.log` for review
- 🧠 Includes a `/status` command to check runtime health via Telegram
- 🔐 Uses `.env` for secrets and avoids versioning sensitive data

---

## 💬 Telegram Bot Setup

1. **Create your bot:**
   - Open Telegram and search for [@BotFather](https://t.me/BotFather)
   - Send `/start`, then `/newbot`
   - Follow the instructions and choose a name + username (e.g. `cph_bib_bot`)
   - BotFather will give you a **bot token** — copy and save this

2. **Get your Chat ID:**
   - Send a `/start` message to your new bot in Telegram
   - Then open this URL in your browser (replace `<TOKEN>` with your real token):
     ```
     https://api.telegram.org/bot<TOKEN>/getUpdates
     ```
   - Look for `"chat":{"id":<your_chat_id>}` in the JSON response

---

## 📦 Makefile Commands

| Command       | What it does                         |
|---------------|--------------------------------------|
| `make venv`   | Creates the virtualenv + installs dependencies |
| `make run`    | Runs the bib watcher                 |
| `make log`    | Tails the log file                   |
| `make freeze` | Saves installed packages to `requirements.txt` |
| `make clean`  | Removes `venv/` and cache files      |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for full details.

---

## 🙌 Credits

Created by [@codingdaniel](https://github.com/coding-daniel)  
Inspired by the need to race in beautiful Copenhagen 😄


