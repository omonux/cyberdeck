# Launch Posts — CYBERDECK

Repo: https://github.com/omonux/cyberdeck

---

## 1. Hacker News — Show HN

**Title:**
Show HN: Cyberdeck – your terminal, but make it hacker (one Python file, zero config)

**Body:**

I got tired of spinning up half a dozen tools just to make my terminal *look* like a hacker's cockpit for a screen recording. So I wrote cyberdeck: one Python file, zero config, no API keys.

What it does:
- Live IP recon + geolocation (ipify/ipapi)
- Live weather for your IP (open-meteo, keyless)
- Fake network scan banner — the screenshot-able part
- Matrix digital rain (`cyberdeck matrix`)
- Domain recon: `cyberdeck whois github.com` → DNS records, server header, TLS cert, security headers
- System stats (uptime, disk, load)
- Rotating hacker quotes
- `cyberdeck sudo make me a sandwich` — yes, really

Run it with no args and it does all of it at once. That's the "hacker mode."

Why one file? Because the point is friction: `git clone && python3 cyberdeck.py` is the entire onboarding. No YAML, no Docker, no API key hunting.

The scan banner and matrix mode are half aesthetic, half practical — they're what makes the terminal look like it's doing something. But the IP/whois bits are genuinely useful for quick recon.

Happy to take feedback on what would make this actually useful beyond vibes.

---

## 2. Reddit — r/commandline (and r/Python)

**Title:**
I made a one-file Python script that turns your terminal into a hacker cockpit — zero config, no API keys

**Body:**

Hey all — I built cyberdeck over the weekend because I wanted my terminal to *look* like a hacker's without juggling 5 different tools.

One Python file. `git clone`, `python3 cyberdeck.py`, done. No setup, no API keys, no Docker.

What's in it:
- 🌍 Live IP recon + geolocation (where does your connection actually exit?)
- 🌦️ Live weather for your IP (yes, really)
- 📡 Fake network scan banner — the screenshot-able part
- 💚 Matrix digital rain
- 🔍 `cyberdeck whois <domain>` — DNS, server header, TLS cert, security headers in one command
- 💻 System stats + rotating hacker quotes
- 🥪 `cyberdeck sudo make me a sandwich` — yes, really

Run it with no args = full "hacker mode" (everything at once).

It's MIT licensed: https://github.com/omonux/cyberdeck

The honest split: the scan banner and matrix rain are 80% aesthetic, the IP/whois bits are genuinely useful for quick recon. Both together make the terminal look like it's doing something, which is the whole point.

Would love feedback — what would you add to make this actually part of your daily workflow?

---

## 3. Twitter/X

**Post (thread, 4 tweets):**

1/
Your terminal, but make it hacker. 🖥️

I built @cyberdeck — one Python file, zero config, no API keys.

git clone. python3 cyberdeck.py. Done.

2/
What it does:
→ Live IP recon + geolocation
→ Live weather for your IP
→ Fake network scan banner (the screenshot-able part)
→ Matrix rain
→ Domain recon: DNS, TLS cert, security headers in one command
→ Hacker quotes
→ `cyberdeck sudo make me a sandwich` 🥪

3/
Run it with no args = full hacker mode. Everything at once.

No YAML. No Docker. No API key hunting. One file. MIT licensed.

github.com/omonux/cyberdeck

4/
Half aesthetic, half actually useful recon. Both together = your terminal finally looks like it's doing something.

Fork it, break it, make it yours. 🖥️

---

## Posting order (for max reach)

1. **Twitter thread** — post first, get the link warm
2. **Reddit r/commandline** — 1h later, drop the repo in comments when asked
3. **Hacker News Show HN** — 2–4h after Reddit (HN links to Reddit posts get "already on reddit" downvotes; keep them separate)
4. Share the HN link back in the Twitter thread when it hits the front page
