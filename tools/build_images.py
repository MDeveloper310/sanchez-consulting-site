#!/usr/bin/env python3
"""Builds every raster asset for the site.
Usage: python3 tools/build_images.py [HERO_PHOTO] [ABOUT_PHOTO]
Pass the client's real photos to replace the branded portrait placeholders."""
import sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'img'); SRC = os.path.join(ROOT, 'tools', 'src')
os.makedirs(IMG, exist_ok=True)
INK = (11, 11, 12)

def save(im, name, widths, q=82):
    for w in widths:
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS) if w != im.width else im
        r.convert('RGB').save(f'{IMG}/{name}-{w}.jpg', quality=q, optimize=True, progressive=True)
        r.convert('RGB').save(f'{IMG}/{name}-{w}.webp', quality=q - 2, method=6)

def diamond_bg(w, h, step=56, alpha=10):
    im = Image.new('RGBA', (w, h), INK + (255,))
    d = ImageDraw.Draw(im, 'RGBA')
    for x in range(-h, w + h, step):
        d.line([(x, 0), (x + h, h)], fill=(201, 164, 92, alpha), width=1)
        d.line([(x, h), (x + h, 0)], fill=(201, 164, 92, alpha), width=1)
    return im

mark = Image.open(f'{SRC}/logo-mark.png'); stacked = Image.open(f'{SRC}/logo-stacked.png')
horiz = Image.open(f'{SRC}/logo-horizontal.png')

def placeholder(w, h):
    im = diamond_bg(w, h, alpha=14)
    g = Image.new('RGBA', (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([w*.1, h*.2, w*.9, h*.8], fill=(201, 164, 92, 40)); g = g.filter(ImageFilter.GaussianBlur(w/6))
    im = Image.alpha_composite(im, g)
    m = mark.resize((int(w*.42), int(w*.42*mark.height/mark.width)), Image.LANCZOS)
    im.alpha_composite(m, ((w-m.width)//2, (h-m.height)//2))
    return im

def cover(src, ratio, crop_box=None, focus_y=0.35):
    im = Image.open(src).convert('RGB')
    if crop_box: im = im.crop(crop_box)
    W, H = im.size
    if W / H > ratio:
        nw = int(H * ratio); x = (W - nw)//2; im = im.crop((x, 0, x+nw, H))
    else:
        nh = int(W / ratio); y = int((H - nh) * focus_y); im = im.crop((0, y, W, y+nh))
    return im

hero_src = sys.argv[1] if len(sys.argv) > 1 else None
about_src = sys.argv[2] if len(sys.argv) > 2 else None
if hero_src:
    im = Image.open(hero_src); W, H = im.size
    hero = cover(hero_src, 2/3, crop_box=(0, 0, W, int(H*0.90)), focus_y=0.0)  # trims bottom-right sparkle watermark
else:
    hero = placeholder(800, 1200)
hw = [420, 640, 800]  # fixed names used by index.html srcset (mild upscale if source is small)
save(hero, 'portrait-hero', hw)
about = cover(about_src, 4/5, focus_y=0.25) if about_src else placeholder(800, 1000)
aw = [420, 640, 800]
save(about, 'portrait-about', aw)
open(f'{IMG}/sizes.txt', 'w').write(f'hero {hw} {hero.size}\nabout {aw} {about.size}\n')

# Logos
horiz.save(f'{IMG}/logo-horizontal.png', optimize=True)
h2 = horiz.resize((int(horiz.width*120/horiz.height), 120), Image.LANCZOS); h2.save(f'{IMG}/logo-horizontal-120.png', optimize=True); h2.save(f'{IMG}/logo-horizontal-120.webp', quality=90, method=6)
s2 = stacked.resize((420, int(420*stacked.height/stacked.width)), Image.LANCZOS); s2.save(f'{IMG}/logo-stacked.png', optimize=True); s2.save(f'{IMG}/logo-stacked.webp', quality=90, method=6)
mark.save(f'{IMG}/logo-mark.png', optimize=True)

# Favicons: mark on ink square
def icon(size, pad=0.14, rounded=False):
    bg = Image.new('RGBA', (size, size), INK + (255,))
    inner = int(size*(1-2*pad)); m = mark.copy(); m.thumbnail((inner, inner), Image.LANCZOS)
    bg.alpha_composite(m, ((size-m.width)//2, (size-m.height)//2)); return bg
icon(180, .12).convert('RGB').save(f'{ROOT}/apple-touch-icon.png')
icon(192).save(f'{IMG}/icon-192.png'); icon(512).save(f'{IMG}/icon-512.png')
icon(512, .22).save(f'{IMG}/icon-maskable-512.png')
icon(32, .06).save(f'{ROOT}/favicon-32x32.png'); icon(16, .04).save(f'{ROOT}/favicon-16x16.png')
icon(256, .06).save(f'{ROOT}/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])

# Open Graph 1200x630
og = diamond_bg(1200, 630, alpha=12)
glow = Image.new('RGBA', og.size, (0,0,0,0)); ImageDraw.Draw(glow).ellipse([60, 60, 700, 570], fill=(201,164,92,38)); og = Image.alpha_composite(og, glow.filter(ImageFilter.GaussianBlur(120)))
p = hero.copy().convert('RGBA'); ph = 630; p = p.resize((int(p.width*ph/p.height), ph), Image.LANCZOS)
px = 1200 - p.width
fade = np.ones((ph, p.width)); ramp = min(160, p.width//3); fade[:, :ramp] = np.linspace(0, 1, ramp)
a = np.array(p); a[..., 3] = (a[..., 3]*fade).astype(np.uint8); og.alpha_composite(Image.fromarray(a), (px, 0))
lg = stacked.resize((520, int(520*stacked.height/stacked.width)), Image.LANCZOS)
og.alpha_composite(lg, (max(40, (px - lg.width)//2 + 20), 120))
d = ImageDraw.Draw(og)
try: f = ImageFont.truetype(os.path.join(SRC, 'Jost.ttf'), 24)
except Exception: f = ImageFont.load_default(24)
txt = 'TAX PREPARATION  ·  TAX STRATEGY  ·  SAN FRANCISCO'
tw = d.textlength(txt, font=f); cx = max(40, (px - lg.width)//2 + 20) + lg.width/2
d.text((cx - tw/2, 120 + lg.height + 46), txt, font=f, fill=(222, 196, 140))
d.line([(cx-60, 120 + lg.height + 24), (cx+60, 120 + lg.height + 24)], fill=(201,164,92), width=1)
og.convert('RGB').save(f'{IMG}/og-image.jpg', quality=88)
print('done', hero.size, about.size)
