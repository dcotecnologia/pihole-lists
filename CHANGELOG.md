# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Extracted `src/common.py` to remove the `get_filenames_without_extension`/`delete_file`/`selected_lists`
  logic duplicated across `build.py`, `cleanup.py`, and `readme_list.py` by @danilogco
- `src/import.py` now uses a configured, named logger instead of silently-dropped root-logger
  `logging.info`/`logging.error` calls, and opens files with an explicit UTF-8 encoding by @danilogco
- Refactored `src/readme_list.py` into a testable `main()` entry point, consistent with the
  other scripts by @danilogco
- Fixed broken `raw.githubusercontent.com`/issues links in `README.md` pointing at the wrong
  repo name (`pi-hole-lists` instead of `pihole-lists`), replaced non-descriptive `[Link]`
  anchor text, corrected several typos, and replaced the stale/broken `docker-compose run
  build` instructions with the actual `make compile`/`make cleanup` workflow by @danilogco

## [1.3.0] - 2026-03-20

### Added

- Added script to import third-party community lists by @danilogco

### Changed

- Updated ads, ads_malware, basic and phishing lists by @danilogco

## [1.2.0] - 2026-03-20

### Added

- Added new domains to blocklists, including updates to gambling, fake news, drugs, porn, telemetry, and ransomware lists.
- Added a GitHub Actions workflow for automated test runs.
- Added unit test coverage for build and cleanup scripts.
- Added CONTRIBUTING, CODE_OF_CONDUCT, and SECURITY documentation.

### Changed

- Migrated project dependency management from Poetry to uv.
- Improved filtering, domain normalization, extraction, and validation logic in list processing scripts.
- Removed deprecated SDK entries from ad lists.
- Removed issue reference artifacts from phishing and scam list entries.
- Applied lint and formatting refactors across the codebase.
- Updated issue templates.

## [1.1.0] - 2024-09-21

### Changed

- Removed a lot of invalid entries from the lists by @danilogco
- Some entries added to porn, fakenews, and other lists by @danilogco

## [1.0.3] - 2023-12-20

### Changed

- New hosts blacklisteds

#### Ads

- tim-ads.com

### Fake news

- brasil247.com

### Gambling

- mrjack.bet
- br.novibet.com
- br.betano.com
- <www.bets.com.br>
- <www.galera.bet>
- betnacional.com
- br.netbet.com
- sports.sportingbet.com
- world.parimatch.com

## [1.0.2] - 2023-12-18

### Changed

- New hosts blacklisteds

#### Ads

- img-s-msn-com.akamaized.net

#### Gambling

- estrelabet.com
- q8bet.vip

## [1.0.1] - 2023-12-17

### Changed

- New hosts blacklisteds

#### Porn

- photoacompanhantes.com

#### Gambling

- apostasdanet.com
- betsul.com
- blaze-4.com
- brazino777.com
- casadeapostas.com

## [1.0.0] - 2023-12-17

### Added

- Add the initial files and lists - ads_malware, fakenews, gambling, porn, social -, by @danilogco
