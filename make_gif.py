#!/usr/bin/env python3
"""Generate demo.gif — an animation of cyberdeck's scan banner."""
from PIL import Image, ImageDraw, ImageFont
import random

# try to find a monospace font
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
]
font = None
for p in FONT_PATHS:
    try:
        font = ImageFont.truetype(p, 14)
        break
    except Exception:
        pass
if font is None:
    font = ImageFont.load_default()

BG      = (10, 14, 20)
FG      = (200, 210, 220)
CYAN    = (0, 229, 255)
GREEN   = (0, 230, 118)
RED     = (255, 80, 80)
DIM     = (90, 100, 110)
YELLOW  = (255, 200, 0)
MAGENTA = (255, 0, 200)

W, H = 560, 360
CHARS = "アイウエオカキクケコサシスセソ0123456789ABCDEF"

def make_frame(lines, cursor_at=None):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # window chrome
    d.rectangle([0,0,W,24], fill=(20,26,34))
    for i, col in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        d.ellipse([10+i*18, 8, 22+i*18, 20], fill=col)
    d.text((W//2-40, 6), "kali@cyberdeck: ~", font=font, fill=DIM)
    # lines
    y = 36
    for text, color in lines:
        d.text((16, y), text, font=font, fill=color)
        y += 18
    # cursor
    if cursor_at:
        cx, cy = cursor_at
        d.rectangle([cx, cy-12, cx+8, cy], fill=CYAN)
    return img

# build the scan sequence
ports = [21,22,25,53,80,110,143,443,445,993,995,3306,3389,5432,8080]
open_ports = {53, 80, 443, 993}
services = {53:"dns",80:"http",443:"https",993:"imaps"}

header_lines = [
    ("┌" + "─"*52 + "┐", CYAN),
    ("│  NETWORK SCAN  ·  sim" + " "*30 + "│", CYAN),
    ("└" + "─"*52 + "┘", CYAN),
    ("  scanning 192.168.1.0/24 ...", DIM),
]

frames = []
# phase 1: show header, then reveal ports one by one
scan_lines = list(header_lines)
for p in ports:
    if p in open_ports:
        line = (f"   [+] {str(p).rjust(5)}  open   {services.get(p,'?')}", GREEN)
    else:
        line = (f"   [-] {str(p).rjust(5)}  closed", DIM)
    scan_lines.append(line)
    # each frame: show up to this port, cursor at end of last line
    frames.append(make_frame(scan_lines))

# phase 2: show the "found" line
final = scan_lines + [("", FG), (f"  {len(open_ports)} open port(s) found. You've been seen.", RED)]
for _ in range(10):
    frames.append(make_frame(final))

# phase 3: matrix rain frames
for _ in range(15):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,24], fill=(20,26,34))
    d.text((W//2-40, 6), "kali@cyberdeck: ~", font=font, fill=DIM)
    for x in range(16, W-16, 12):
        for y in range(36, H-16, 18):
            ch = random.choice(CHARS)
            # random brightness
            b = random.randint(40, 230)
            d.text((x, y), ch, font=font, fill=(0, b, 90))
    frames.append(img)

frames[0].save("demo.gif", save_all=True, append_images=frames[1:],
               duration=120, loop=0, optimize=True)
print(f"demo.gif written: {len(frames)} frames")
