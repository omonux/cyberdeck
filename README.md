<div align="center">

# 🖥️ CYBERDECK

**your terminal, but make it hacker.**

[![Python](https://img.shields.io/badge/python-3.7+-green)]()
[![deps](https://img.shields.io/badge/deps-requests-blue)]()
[![license](https://img.shields.io/badge/license-MIT-yellow)]()

</div>

---

One command. Zero config. Instant hacker mode.

CYBERDECK turns your terminal into a hacker's cockpit — live weather for your IP, IP recon + geolocation, a fake network scan, system stats, and rotating hacker quotes. No setup, no YAML, no Docker. Just run it.

## ✨ Demo

```
 ██████╗ ██████╗ ██████╗ ███████╗███╗   ██╗ ██████╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔═══██╗
██║     ██║   ██║██║  ██║█████╗  ██╔██╗ ██║██║   ██║
██║     ██║   ██║██║  ██║██╔══╝  ██║╚██╗██║██║   ██║
╚██████╗╚██████╔╝██████╔╝███████╗██║ ╚████║╚██████╔╝
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝

  ═══ CYBERDECK online. You're invisible. ═══
```

## 🚀 Install

```bash
git clone https://github.com/omonux/cyberdeck.git
cd cyberdeck
python3 cyberdeck.py
```

Or just run it directly — no install needed:

```bash
python3 cyberdeck.py
```

> Requires Python 3.7+ and the `requests` library (`pip install requests`).

## 🛠️ Commands

| Command | What it does |
|---|---|
| *(none)* | **Full hacker mode** — everything at once |
| `weather` | Live weather for your public IP |
| `ip` | IP recon + geolocation (city, country, org) |
| `logo` | Big ASCII CYBERDECK logo |
| `scan` | Fake network scan banner (for vibes) |
| `quote` | Random hacker quote |
| `stats` | Your machine stats (OS, uptime, disk) |
| `--help` | Show all commands |

## 💡 Why

You're at a coffee shop, screen-recording, or just feeling edgy. You want your terminal to *look* like a hacker's without spinning up 12 tools. CYBERDECK gives you that in one command.

- **Live IP geolocation** — see exactly where your connection exits
- **Live weather** — because hackers need to know if it's raining at the server farm
- **Fake scan banner** — perfect for screenshots and "I'm hacking" moments
- **Zero config** — no API keys, no setup, no YAML

## 📦 How it works

- `ipify` / `ifconfig.co` → your public IP
- `ipapi.co` → geolocation
- `open-meteo.com` → weather (no API key)
- `/proc/uptime`, `os.statvfs` → system stats

All free, all keyless, all in one Python file.

## 🎨 Colors

Colors auto-disable when piped or when `NO_COLOR=1`:

```bash
NO_COLOR=1 python3 cyberdeck.py
```

## 📄 License

MIT — do whatever, just credit us if you fork it.

---

<div align="center">

**Made by [omonux](https://github.com/omonux)** · part of the CyberNeurova toolkit

</div>
