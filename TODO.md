# TODO / Roadmap

## Priority

- [x] Add RotatingFileHandler for log rotation
- [x] Log every check (even when no bibs found)

## Reusability

- [ ] Extract Telegram logic to reusable `telegram_client.py`
- [ ] Use env-based configuration for all bot behavior
- [ ] Structure for future reuse in other tools

## Features

- [ ] Add `/export` command to send bibs.csv via Telegram

## Testing

- [ ] Write unit tests for bib parsing
- [ ] Write tests for CSV and Telegram send logic
