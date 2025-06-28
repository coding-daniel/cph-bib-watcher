# TODO / Roadmap

## Priority

- [x] Add RotatingFileHandler for log rotation
- [x] Log every check (even when no bibs found)

## Reusability

- [x] Extract Telegram logic to reusable `telegram_client.py`
- [x] Use env-based configuration for all bot behavior
- [x] Structure project for future reuse in other tools

## Features

- [ ] Add `/export` command to send bibs.csv via Telegram
- [x] Add `/seen` command to report number of saved bibs

## Testing

- [ ] Write unit tests for bib parsing
- [ ] Write tests for CSV and Telegram send logic
