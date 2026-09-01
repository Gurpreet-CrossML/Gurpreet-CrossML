#!/usr/bin/env python3
"""Build profile_animated.svg from the gh-ascii dark card.
Usage: python3 make_card.py              -> profile_animated.svg
       python3 make_card.py out.svg 2.5  -> test frame: state at t=2.5s rendered at t=0
Edit PROFILE below and re-run."""
import re, sys, html

PROFILE = [  # ("Header",) or (label, value) or None for a blank line
    ("Gurpreet-CrossML@github",),
    ("Name", "Gurpreet Singh"),
    ("Role", "Software Engineer @crossml"),
    ("Experience", "4 yrs, production full-stack + AI"),
    ("Location", "Chandigarh, IN"),
    ("Uptime", None),                      # None = keep value from the source card
    None,
    ("Focus",),
    ("Building", "AI agents, MCP servers, web apps"),
    ("Pipelines", "OCR, NLP, workflow automation"),
    ("Domain", "E-commerce (Shopify, Magento)"),
    None,
    ("Stack",),
    ("Languages", "TypeScript, Python, Go"),
    ("Frameworks", "Next.js, React, Node, Django/DRF"),
    ("Cloud", "AWS, GCP, Docker, Kubernetes"),
    None,
    ("Contact",),
    ("GitHub", "github.com/Gurpreet-CrossML"),
    ("LinkedIn", "linkedin.com/in/garybadwal"),
    ("Email", "gurpreet@crossml.com"),
    None,
    ("GitHub Stats",),
    ("Repos", "19"), ("Stars", "1"), ("Followers", "0"),
]
WIDTH, X, LH, FS = 57, 549.6, 20, 16
C = dict(label="#ffa657", dots="#484f58", val="#c9d1d9", num="#79c0ff", head="#58a6ff", rule="#3d444d")
FONT = "font-family=\"'Consolas', 'Menlo', 'DejaVu Sans Mono', monospace\" xml:space=\"preserve\""

src = open('dark_mode.svg').read()
W, H = [float(v) for v in re.search(r'width="([\d.]+)" height="([\d.]+)"', src).groups()]
texts = re.findall(r'  <text[^>]*>.*?</text>\n', src, re.S)
art = [t for t in texts if 'x="28"' in t]
src_vals = dict(re.findall(r'\. (\w+): </tspan><tspan[^>]*>\.+</tspan><tspan[^>]*> ([^<]+)', src))

def tspan(color, s): return f'<tspan fill="{color}">{html.escape(s)}</tspan>'
def row(y, spans): return f'<text x="{X}" y="{y}" {FONT} font-size="{FS}">{"".join(spans)}</text>\n'
def line(y, item):
    if len(item) == 1:
        h = f' {item[0]} '
        return row(y, [tspan(C['rule'], '─'), tspan(C['head'], h), tspan(C['rule'], '─' * (WIDTH - len(h)))])
    label, val = item
    val = src_vals[label] if val is None else val
    lab = f'. {label}: '
    dots = '.' * max(2, WIDTH - len(lab) - len(val) - 1)
    return row(y, [tspan(C['label'], lab), tspan(C['dots'], dots), tspan(C['num'] if val.isdigit() else C['val'], ' ' + val)])

# --- avatar: staggered fade-in ---
art_g = '<g class="art">\n' + ''.join(
    t.replace(' fill="#c9d1d9"', '').replace('<text', f'<text class="a" style="animation-delay:{i*25}ms"', 1)
    for i, t in enumerate(art)) + '</g>\n'

# --- right column: typewriter reveal per line ---
n_rows = sum(1 for p in PROFILE if p) 
y = round((H - (len(PROFILE) * LH)) / 2 + FS)
rows, covers, i = [], [], 0
T0, STEP, DUR = 0.7, 0.28, 0.5
for item in PROFILE:
    if item:
        rows.append(line(y, item))
        covers.append(f'<rect class="c" x="540" y="{y-16}" width="{W-548}" height="22" style="animation-delay:{T0+i*STEP:.2f}s"/>\n')
        i += 1
    y += LH
cursor = f'<rect class="cur" x="551" y="{y-LH+8}" width="9" height="3" style="animation-delay:{T0+i*STEP:.2f}s"/>\n'
info_g = '<g class="info">\n' + ''.join(rows) + ''.join(covers) + cursor + '</g>\n'

# --- scanline over the avatar ---
art_top = 22
art_h = float(re.search(r'y="([\d.]+)"', art[-1]).group(1)) - art_top + 8
scan = (f'<clipPath id="artclip"><rect x="8" y="{art_top}" width="520" height="{art_h}"/></clipPath>\n'
        f'<g clip-path="url(#artclip)"><rect class="scan" x="8" y="{art_top-90}" width="520" height="90" fill="url(#scan)"/></g>\n')

defs = f'''<defs>
<linearGradient id="ink" gradientUnits="userSpaceOnUse" x1="28" y1="22" x2="520" y2="580">
  <stop offset="0" stop-color="#3fb950"><animate attributeName="stop-color" values="#3fb950;#58a6ff;#bc8cff;#3fb950" dur="12s" repeatCount="indefinite"/></stop>
  <stop offset="1" stop-color="#58a6ff"><animate attributeName="stop-color" values="#58a6ff;#bc8cff;#3fb950;#58a6ff" dur="12s" repeatCount="indefinite"/></stop>
</linearGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
</linearGradient>
</defs>
<style>
.a{{fill:url(#ink);opacity:0;animation:in .6s ease-out forwards}}
@keyframes in{{from{{opacity:0;transform:translateX(-6px)}}to{{opacity:1;transform:none}}}}
.c{{fill:#0d1117;transform-box:fill-box;transform-origin:right;animation:type {DUR}s steps(28,end) forwards}}
@keyframes type{{to{{transform:scaleX(0)}}}}
.cur{{fill:#58a6ff;opacity:0;animation:blink 1s steps(2,start) infinite}}
@keyframes blink{{to{{opacity:1}}}}
.scan{{animation:sweep 6s linear infinite}}
@keyframes sweep{{from{{transform:none}}to{{transform:translateY({art_h+90:.0f}px)}}}}
.frame{{animation:glow 5s ease-in-out infinite alternate}}
@keyframes glow{{from{{stroke:#30363d}}to{{stroke:#58a6ff}}}}
</style>
'''
head = src[:src.index('\n')+1]
frame = re.search(r'  <rect[^>]*/>\n', src).group(0).replace('<rect', '<rect class="frame"', 1)
svg = head + defs + frame + art_g + scan + info_g + '</svg>\n'

out = sys.argv[1] if len(sys.argv) > 1 else 'profile_animated.svg'
if len(sys.argv) > 2:  # seek: shift every delay by -T so t=0 shows the state at time T
    T = float(sys.argv[2])
    svg = re.sub(r'animation-delay:([\d.]+)(m?)s', lambda m: f'animation-delay:{float(m[1])/(1000 if m[2] else 1)-T:.3f}s', svg)
    svg = svg.replace('</style>', f'.scan,.frame{{animation-delay:-{T}s}}</style>').replace('<animate ', f'<animate begin="-{T}s" ')
open(out, 'w').write(svg)
print(f'{len(art)} art lines, {i} info lines -> {out}')
