# Changelog

## [Unreleased]
- Add `/export` command to Telegram bot
- Add unit tests

## [2025-06-28]
### Added
- `/seen` Telegram command to show total number of bibs recorded in CSV
- `utils.py` module with `count_csv_entries()` helper
- Improved `/status` command handling with correct offset logic
- Fixed bib table parsing for current HTML structure
- MIT license file and short headers in all source files
- `/status` Telegram command for runtime monitoring
- README cleanup:
  - Added Telegram setup instructions
  - Added visual logos (CPH + Telegram)
- Log rotation using `RotatingFileHandler`
- Logging for every check (even when no bibs found)
- Log messages for:
  - No bibs found on page
  - Bibs found but none new
  - Number of new bibs added

### Changed
- Increased check interval from 60s to 300s (5 minutes)
- Improved log clarity and verbosity
