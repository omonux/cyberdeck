#!/usr/bin/env python3
"""
CYBERDECK — your terminal, but make it hacker.

Zero-config hacker toolkit: live weather, IP recon, ASCII logo,
scan banner, hacker quotes, system stats. One command. No deps.

Usage:
  cyberdeck              # full hacker mode (everything)
  cyberdeck weather      # live weather for your IP
  cyberdeck ip           # IP recon + geolocation
  cyberdeck logo         # big ASCII CYBERDECK logo
  cyberdeck scan         # fake network scan banner
  cyberdeck quote        # random hacker quote
  cyberdeck stats        # your machine stats
  cyberdeck --help       # show commands
"""

import sys
import os
import socket
import subprocess
import random
import platform
import textwrap
from datetime import datetime, timezone

# ── colors ──────────────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    CYAN   = "\033[96m"
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    MAGENTA= "\033[95m"
    BLUE   = "\033[94m"
    WHITE  = "\033[97m"

def no_color():
    return os.environ.get("NO_COLOR") or not sys.stdout.isatty()

def c(col, s):
    return s if no_color() else f"{col}{s}{C.RESET}"

def hr(ch="─", n=56):
    print(c(C.DIM, ch * n))

def header(title):
    print()
    print(c(C.CYAN, "┌" + "─" * 54 + "┐"))
    print(c(C.CYAN, "│") + c(C.BOLD + C.CYAN, f"  {title:<50}") + c(C.CYAN, "│"))
    print(c(C.CYAN, "└" + "─" * 54 + "┘"))

def fetch(url, timeout=8):
    import requests
    return requests.get(url, timeout=timeout, headers={"User-Agent": "cyberdeck/1.0"})

# ── logo ────────────────────────────────────────────────────────────────
LOGO = r"""
 ██████╗ ██████╗ ██████╗ ███████╗███╗   ██╗ ██████╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔═══██╗
██║     ██║   ██║██║  ██║█████╗  ██╔██╗ ██║██║   ██║
██║     ██║   ██║██║  ██║██╔══╝  ██║╚██╗██║██║   ██║
╚██████╗╚██████╔╝██████╔╝███████╗██║ ╚████║╚██████╔╝
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝
"""

def cmd_logo():
    print(c(C.BOLD + C.CYAN, LOGO))
    print(c(C.DIM, "   v1.0  ·  your terminal, but make it hacker"))

# ── ip recon ────────────────────────────────────────────────────────────
def get_public_ip():
    try:
        return fetch("https://api.ipify.org?format=json").json()["ip"]
    except Exception:
        try:
            return fetch("https://ifconfig.co/ip").text.strip()
        except Exception:
            return "127.0.0.1"

def cmd_ip():
    header("IP RECON")
    ip = get_public_ip()
    print(c(C.GREEN, "  public ip : ") + ip)
    try:
        d = fetch(f"https://ipapi.co/{ip}/json/").json()
        print(c(C.GREEN, "  city      : ") + str(d.get("city", "?")))
        print(c(C.GREEN, "  region    : ") + str(d.get("region", "?")))
        print(c(C.GREEN, "  country   : ") + str(d.get("country_name", "?")) + " " + str(d.get("country_code", "")))
        print(c(C.GREEN, "  lat/long  : ") + f"{d.get('latitude','?')}, {d.get('longitude','?')}")
        print(c(C.GREEN, "  org       : ") + str(d.get("org", "?")))
        print(c(C.GREEN, "  timezone  : ") + str(d.get("timezone", "?")))
    except Exception as e:
        print(c(C.YELLOW, "  geo lookup : ") + f"unavailable ({e})")
    # local
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local = s.getsockname()[0]
        s.close()
        print(c(C.GREEN, "  local ip  : ") + local)
    except Exception:
        pass
    print(c(C.DIM, "  scanned at: ") + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))

# ── weather ─────────────────────────────────────────────────────────────
def cmd_weather():
    header("WEATHER  ·  live")
    ip = get_public_ip()
    try:
        d = fetch(f"https://ipapi.co/{ip}/json/").json()
        lat, lon = d.get("latitude"), d.get("longitude")
        city = d.get("city", "your location")
    except Exception:
        lat, lon, city = 40.7128, -74.006, "New York (default)"
    try:
        w = fetch(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()
        cw = w.get("current_weather", {})
        temp = cw.get("temperature")
        wind = cw.get("windspeed")
        code = cw.get("weathercode")
        desc = WMO.get(code, "unknown")
        print(c(C.GREEN, "  location  : ") + f"{city} ({lat:.2f}, {lon:.2f})")
        print(c(C.YELLOW, "  temperature: ") + f"{temp}°C")
        print(c(C.CYAN, "  condition : ") + desc)
        print(c(C.CYAN, "  wind      : ") + f"{wind} km/h")
        print(c(C.DIM, "  source    : open-meteo.com"))
    except Exception as e:
        print(c(C.YELLOW, "  weather     : ") + f"unavailable ({e})")

WMO = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "fog", 48: "depositing rime fog", 51: "light drizzle", 53: "drizzle",
    55: "dense drizzle", 56: "freezing drizzle", 57: "dense freezing drizzle",
    61: "slight rain", 63: "rain", 65: "heavy rain", 66: "freezing rain",
    67: "heavy freezing rain", 71: "slight snow", 73: "snow", 75: "heavy snow",
    77: "snow grains", 80: "slight rain showers", 81: "rain showers",
    82: "violent rain showers", 85: "slight snow showers", 86: "heavy snow showers",
    95: "thunderstorm", 96: "thunderstorm w/ hail", 99: "thunderstorm w/ heavy hail",
}

# ── scan banner ─────────────────────────────────────────────────────────
def cmd_scan():
    header("NETWORK SCAN  ·  sim")
    ports = [21, 22, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 8080]
    open_ports = random.sample(ports, k=random.randint(3, 6))
    services = {21:"ftp",22:"ssh",25:"smtp",53:"dns",80:"http",110:"pop3",143:"imap",
                443:"https",445:"smb",993:"imaps",995:"pop3s",3306:"mysql",3389:"rdp",
                5432:"postgres",8080:"http-proxy"}
    print(c(C.DIM, "  scanning 192.168.1.0/24 ..."))
    for p in sorted(ports):
        if p in open_ports:
            print(f"   {c(C.GREEN,'[+]')} {c(C.GREEN, str(p).rjust(5))}  open   {services.get(p,'?')}")
        else:
            print(f"   {c(C.DIM,'[-]')} {str(p).rjust(5)}  closed")
    print()
    print(c(C.BOLD + C.RED, f"  {len(open_ports)} open port(s) found. You've been seen."))

# ── matrix rain ─────────────────────────────────────────────────────────
def cmd_matrix():
    """Matrix digital rain — runs for a few seconds then exits."""
    import time
    cols = 60
    chars = "アイウエオカキクケコサシスセソ0123456789ABCDEF"
    drops = [random.randint(0, 20) for _ in range(cols)]
    print(c(C.DIM, "  matrix mode — ctrl+c to exit (auto-stops in 5s)"))
    end = time.time() + 5
    frame = 0
    while time.time() < end:
        out = []
        for i in range(cols):
            ch = random.choice(chars)
            # head of the drop is bright, tail fades
            out.append(c(C.GREEN, ch))
        print("\033[1A" + "".join(out))
        frame += 1
        time.sleep(0.05)
    print(c(C.DIM, "  matrix off"))

# ── whois ───────────────────────────────────────────────────────────────
def cmd_whois():
    header("WHOIS  ·  domain recon")
    domain = sys.argv[2] if len(sys.argv) > 2 else "remotiva.site"
    print(c(C.DIM, f"  target: {domain}\n"))
    # DNS
    try:
        ips = socket.getaddrinfo(domain, None)
        addrs = sorted({a[4][0] for a in ips})
        print(c(C.GREEN, "  ip        : ") + ", ".join(addrs[:5]))
    except Exception as e:
        print(c(C.YELLOW, "  ip        : ") + f"unresolved ({e})")
    # reverse DNS
    for ip in (addrs if 'addrs' in dir() else []):
        try:
            host = socket.gethostbyaddr(ip)
            print(c(C.GREEN, "  reverse   : ") + f"{ip} → {host[0]}")
            break
        except Exception:
            pass
    # HTTP headers
    try:
        r = fetch(f"https://{domain}", timeout=8)
        server = r.headers.get("Server", "?")
        print(c(C.GREEN, "  server    : ") + server)
        print(c(C.GREEN, "  status    : ") + str(r.status_code))
        print(c(C.GREEN, "  http→https: ") + ("yes" if "location" in {k.lower() for k in r.headers} or r.status_code in (301,302) else "direct"))
    except Exception:
        try:
            r = fetch(f"http://{domain}", timeout=8)
            print(c(C.GREEN, "  server    : ") + r.headers.get("Server", "?"))
            print(c(C.GREEN, "  status    : ") + str(r.status_code))
        except Exception as e:
            print(c(C.YELLOW, "  http      : ") + f"unreachable ({e})")
    # TLS cert
    try:
        import ssl, socket as sk
        ctx = ssl.create_default_context()
        with sk.create_connection((domain, 443), timeout=8) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as s:
                cert = s.getpeercert()
                for k, v in cert.get("subject", ()):
                    if k == "commonName":
                        print(c(C.GREEN, "  cert cn   : ") + str(v))
                if "notAfter" in cert:
                    print(c(C.GREEN, "  cert exp  : ") + cert["notAfter"])
                issuer = ""
                for rdn in cert.get("issuer", ()):
                    for k, v in rdn:
                        if k == "organizationName":
                            issuer = str(v)
                if issuer:
                    print(c(C.GREEN, "  cert ca   : ") + issuer)
    except Exception as e:
        print(c(C.YELLOW, "  tls       : ") + f"n/a ({e})")
    print(c(C.DIM, "  (full whois: install `whois` and run: whois " + domain + ")"))

# ── quotes ──────────────────────────────────────────────────────────────
QUOTES = [
    ("Everything fails all the time.", "Linus Torvalds"),
    ("The internet is barely a glitch that constantly fixes itself.", "Andy Warhol"),
    ("Paranoia is a feature, not a bug.", "— every sysadmin"),
    ("It works on my machine.", "— a developer, somewhere"),
    ("There are only two hard things in CS: cache invalidation and naming things.", "Phil Karlton"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("99 little bugs in the code, 99 little bugs. Take one down, patch it around, 127 little bugs in the code.", "— folk song"),
    ("The best way to predict the future is to invent it.", "Alan Kay"),
    ("Simplicity is the soul of efficiency.", "Austin Freeman"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Code is like a joke; if you have to explain it, it's not that good.", "— unknown"),
    ("A user interface is like a joke. If you have to explain it, it's not that good.", "Martin Maloney"),
    ("The scariest moment is always just before you start.", "Stephen King"),
    ("Done is better than perfect.", "Sheryl Sandberg"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
]

def cmd_quote():
    q, a = random.choice(QUOTES)
    print()
    print(c(C.MAGENTA, "  " + "❝") + c(C.WHITE, " " + q) + c(C.MAGENTA, " ❞"))
    print(c(C.DIM, "     — " + a))
    print()

# ── stats ───────────────────────────────────────────────────────────────
def cmd_stats():
    header("SYSTEM  ·  your machine")
    print(c(C.GREEN, "  os        : ") + platform.system() + " " + platform.release())
    print(c(C.GREEN, "  arch      : ") + platform.machine())
    print(c(C.GREEN, "  python    : ") + platform.python_version())
    try:
        hostname = socket.gethostname()
        print(c(C.GREEN, "  hostname  : ") + hostname)
    except Exception:
        pass
    # uptime
    try:
        with open("/proc/uptime") as f:
            up = float(f.read().split()[0])
            print(c(C.GREEN, "  uptime    : ") + f"{up/3600:.1f} hours")
    except Exception:
        pass
    # cpu count
    print(c(C.GREEN, "  cpus      : ") + str(os.cpu_count()))
    # disk
    try:
        st = os.statvfs("/")
        total = st.f_blocks * st.f_frsize
        free = st.f_bavail * st.f_frsize
        used = total - free
        print(c(C.GREEN, "  disk /    : ") + f"{used/1e9:.1f}G used / {total/1e9:.1f}G total")
    except Exception:
        pass
    print(c(C.DIM, "  whoami    : ") + os.environ.get("USER", "?"))

# ── phone lookup ────────────────────────────────────────────────────────
# Nigerian carrier prefixes (real, by first 3 digits after country code)
NG_CARRIERS = {
    "803": "MTN", "813": "MTN", "903": "MTN", "913": "MTN", "701": "MTN",
    "703": "MTN", "804": "MTN", "814": "MTN", "904": "MTN", "914": "MTN",
    "802": "Airtel", "812": "Airtel", "902": "Airtel", "912": "Airtel", "702": "Airtel",
    "806": "Glo", "816": "Glo", "906": "Glo", "916": "Glo", "706": "Glo",
    "805": "9mobile", "815": "9mobile", "905": "9mobile", "915": "9mobile", "705": "9mobile",
}

def _extract_phone_from_text(text):
    """Extract phone numbers from raw text (OCR output)."""
    import re
    # find sequences that look like phone numbers (7-15 digits, optional +)
    candidates = re.findall(r'[\+]?[\d][\d\s\-()]{6,18}[\d]', text)
    for cand in candidates:
        digits = re.sub(r'[^\d+]', '', cand)
        if len(digits) >= 7 and len(digits) <= 15:
            return digits
    return None

def _ocr_image(path):
    """Extract text from image using tesseract."""
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(path)
        # upscale small images for better OCR
        if img.width < 400:
            img = img.resize((img.width * 3, img.height * 3), Image.LANCZOS)
        text = pytesseract.image_to_string(img)
        return text
    except ImportError:
        print(c(C.YELLOW, "  [!] pytesseract not installed — pip install pytesseract"))
        return None
    except Exception as e:
        print(c(C.RED, f"  [!] OCR error: {e}"))
        return None

def _lookup_phone(raw_number):
    """Look up a phone number. Returns dict with all available info."""
    import re
    # normalize: strip non-digits except leading +
    digits = re.sub(r'[^\d]', '', raw_number.lstrip('+'))
    has_plus = raw_number.lstrip().startswith('+')

    # Handle Nigerian local formats: 0803... / 803... → +234803...
    if not has_plus and not digits.startswith("234"):
        if digits.startswith("0") and len(digits) == 11:
            digits = "234" + digits[1:]  # 0803... → 234803...
        elif len(digits) == 10 and digits[0] in "897":
            digits = "234" + digits  # 803... → 234803...

    result = {"raw": raw_number, "number": digits, "country": None, "carrier": None,
              "type": None, "valid": None, "name": None, "location": None,
              "line_type": None, "status": None}

    # Nigerian number?
    if digits.startswith("234") and len(digits) == 13:
        result["country"] = "Nigeria (NG)"
        local = digits[3:]  # after country code
        result["carrier"] = NG_CARRIERS.get(local[:3], "Unknown")
        result["type"] = "Mobile"
        result["valid"] = len(local) == 10 and local.isdigit()
        result["line_type"] = "Prepaid/Postpaid"
        result["status"] = "Active format" if result["valid"] else "Invalid format"
    elif digits.startswith("1") and len(digits) == 11:
        result["country"] = "USA/Canada (US/CA)"
        result["type"] = "Mobile/Landline"
        result["valid"] = True
        result["line_type"] = "Unknown"
        result["status"] = "Valid format"
    elif len(digits) >= 7:
        result["country"] = "International"
        result["type"] = "Unknown"
        result["valid"] = len(digits) <= 15
        result["line_type"] = "Unknown"
        result["status"] = "Valid format" if result["valid"] else "Invalid"
    else:
        result["valid"] = False
        result["status"] = "Too short"

    # Optional: numverify API for full name + location (needs free key)
    api_key = os.environ.get("NUMVERIFY_KEY", "").strip()
    if api_key and result["valid"]:
        try:
            url = f"https://numverify.com/api/v2/number_verification?number={digits}&api_key={api_key}"
            r = fetch(url, timeout=10)
            data = r.json()
            if data.get("valid"):
                result["name"] = data.get("name") or None
                result["location"] = f"{data.get('location','')}".strip() or None
                result["line_type"] = data.get("line_type") or result["line_type"]
                result["status"] = data.get("carrier") or result["status"]
                if data.get("country_name"):
                    result["country"] = data["country_name"]
                if data.get("carrier"):
                    result["carrier"] = data["carrier"]
        except Exception:
            pass

    return result

def _print_phone_result(res):
    """Pretty-print phone lookup result."""
    header("PHONE  ·  number recon")
    print(c(C.CYAN, f"  number    : +{res['number']}"))
    if res["country"]:
        print(c(C.GREEN, f"  country   : ") + res["country"])
    if res["carrier"]:
        print(c(C.GREEN, f"  carrier   : ") + res["carrier"])
    if res["type"]:
        print(c(C.GREEN, f"  type      : ") + res["type"])
    if res["line_type"]:
        print(c(C.GREEN, f"  line      : ") + res["line_type"])
    if res["status"]:
        color = C.GREEN if "valid" in res["status"].lower() or "active" in res["status"].lower() else C.YELLOW
        print(c(color, f"  status    : ") + res["status"])
    if res["name"]:
        print(c(C.BOLD + C.MAGENTA, f"  OWNER     : ") + res["name"])
    if res["location"]:
        print(c(C.BOLD + C.MAGENTA, f"  LOCATION  : ") + res["location"])
    if not res["name"]:
        print(c(C.DIM, "  name      : (set NUMVERIFY_KEY env for full name + location)"))
    print()

def cmd_phone(args):
    """Phone number lookup — from arg, file, or image (OCR)."""
    if not args:
        print(c(C.RED, "  usage: cyberdeck phone <number|image.png>"))
        print(c(C.DIM, "  or:     cyberdeck phone --file <image>"))
        print(c(C.DIM, "  env:    NUMVERIFY_KEY=xxx  (free: numverify.com) for full name"))
        return

    target = args[0]

    # Is it an image file?
    if target.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')):
        print(c(C.DIM, f"  [ocr] reading {target}..."))
        text = _ocr_image(target)
        if text:
            print(c(C.DIM, f"  [ocr] extracted: {text.strip()[:80]}"))
            number = _extract_phone_from_text(text)
            if number:
                _print_phone_result(_lookup_phone(number))
            else:
                print(c(C.YELLOW, "  [!] no phone number found in image"))
        return

    # Is it a number?
    if re.sub(r'[^\d+]', '', target).isdigit() or '+' in target:
        _print_phone_result(_lookup_phone(target))
        return

    # Try as file path (text file with number)
    if os.path.isfile(target):
        with open(target) as f:
            content = f.read()
        number = _extract_phone_from_text(content)
        if number:
            _print_phone_result(_lookup_phone(number))
        else:
            print(c(C.YELLOW, "  [!] no phone number found in file"))
        return

    print(c(C.RED, f"  unknown input: {target}"))
    print(c(C.DIM, "  pass a number, image file, or text file"))

import re

# ── full mode ───────────────────────────────────────────────────────────
def full():
    cmd_logo()
    cmd_quote()
    cmd_stats()
    cmd_ip()
    cmd_weather()
    cmd_scan()
    cmd_whois()
    print()
    print(c(C.BOLD + C.GREEN, "  ═══ CYBERDECK online. You're invisible. ═══"))
    print(c(C.DIM, "  run 'cyberdeck --help' for individual tools"))

# ── sudo easter egg ─────────────────────────────────────────────────────
def cmd_sudo(rest):
    """The classic: `cyberdeck sudo <anything>`."""
    arg = " ".join(rest).strip() or "make me a sandwich"
    print()
    print(c(C.YELLOW, f"  $ cyberdeck sudo {arg}"))
    print()
    if os.geteuid() == 0:
        print(c(C.GREEN, "  [sudo] password for root: ********"))
        print(c(C.GREEN, f"  ✓ {arg} — done. (you were already root, obviously)"))
    else:
        user = os.environ.get("USER", "you")
        print(c(C.RED, f"  [sudo] password for {user}: ********"))
        print(c(C.RED, f"  {user} is not in the sudoers file. This incident will be reported."))
        print(c(C.DIM, "  (try: sudo cyberdeck sudo " + arg + ")"))
    print()

# ── main ────────────────────────────────────────────────────────────────
COMMANDS = {
    "weather": ("live weather for your IP", cmd_weather),
    "ip": ("IP recon + geolocation", cmd_ip),
    "logo": ("big ASCII logo", cmd_logo),
    "scan": ("fake network scan banner", cmd_scan),
    "quote": ("random hacker quote", cmd_quote),
    "stats": ("your machine stats", cmd_stats),
    "matrix": ("matrix digital rain (5s)", cmd_matrix),
    "whois": ("domain recon: DNS, server, TLS cert", cmd_whois),
    "phone": ("phone number recon: carrier, type, OCR from image", None),
}

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("--full", "full"):
        full()
        return
    cmd = args[0]
    if cmd in ("--help", "-h", "help"):
        print(c(C.BOLD + C.CYAN, "CYBERDECK — hacker terminal toolkit\n"))
        print(c(C.WHITE, "  (no args)     full hacker mode\n"))
        for name, (desc, _) in COMMANDS.items():
            print(f"  {c(C.GREEN, name.ljust(10))} {desc}")
        print(f"  {c(C.GREEN, 'sudo <cmd>').ljust(13)} the classic")
        print(c(C.DIM, "\n  NO_COLOR=1 cyberdeck   disable colors"))
        return
    if cmd == "sudo":
        cmd_sudo(args[1:])
        return
    if cmd == "phone":
        cmd_phone(args[1:])
        return
    if cmd in COMMANDS:
        COMMANDS[cmd][2 if False else 1]()
        return
    print(c(C.RED, f"  unknown command: {cmd}"))
    print(c(C.DIM, "  run 'cyberdeck --help'"))

if __name__ == "__main__":
    main()
