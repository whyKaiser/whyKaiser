# -*- coding: utf-8 -*-
"""Generates the animated SVG assets for the whyKaiser GitHub profile README.

Theme: deep-space star chart. Constellations only - no planets, no orbits.
Animations are slow and few, and every element is authored at its final state
so a renderer without animation support still shows the finished frame.
"""
import math
import random
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)

BG = "#05060F"
VIOLET = "#8B5CF6"
LILAC = "#A78BFA"
CYAN = "#22D3EE"
AMBER = "#F59E0B"
MINT = "#34D399"
ROSE = "#F472B6"
TEXT = "#E6EAF5"
MUTED = "#8892B0"
FONT = "'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',Consolas,'Courier New',monospace"

# Label bounding boxes, checked for collisions before each file is written.
_boxes = []


def label_box(x, y, text, size, anchor="middle", pad=6.0):
    w = len(text) * size * 0.60 + pad * 2
    if anchor == "middle":
        x0 = x - w / 2
    elif anchor == "end":
        x0 = x - w
    else:
        x0 = x
    _boxes.append((x0, y - size * 0.85, x0 + w, y + size * 0.30, text))


def check_labels(name):
    for i in range(len(_boxes)):
        ax0, ay0, ax1, ay1, at = _boxes[i]
        for j in range(i + 1, len(_boxes)):
            bx0, by0, bx1, by1, bt = _boxes[j]
            if ax0 < bx1 and bx0 < ax1 and ay0 < by1 and by0 < ay1:
                raise SystemExit("%s: labels overlap -> %r / %r" % (name, at, bt))
    _boxes.clear()


def starfield(w, h, n, seed, rmin=0.5, rmax=1.7, base=0.85):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = round(rnd.uniform(0, w), 1)
        y = round(rnd.uniform(0, h), 1)
        r = round(rnd.uniform(rmin, rmax), 2)
        o = round(rnd.uniform(0.25, base), 2)
        dur = round(rnd.uniform(4.5, 9.0), 1)
        delay = round(rnd.uniform(0, 9), 1)
        out.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="{o}">'
            f'<animate attributeName="opacity" values="{o};{round(o*0.35,2)};{o}" '
            f'dur="{dur}s" begin="-{delay}s" repeatCount="indefinite"/></circle>'
        )
    return "\n".join(out)


def flare(x, y, size, color=TEXT, o=0.9):
    return (
        f'<g opacity="{o}"><circle cx="{x}" cy="{y}" r="{round(size*0.45,2)}" fill="{color}"/>'
        f'<path d="M{x-size} {y}H{x+size}M{x} {y-size}V{y+size}" stroke="{color}" '
        f'stroke-width="0.9" stroke-linecap="round" opacity="0.55"/>'
        f'<animate attributeName="opacity" values="{o};{round(o*0.5,2)};{o}" dur="6s" '
        f'repeatCount="indefinite"/></g>'
    )


def star_node(x, y, color, r=5.0, pulse=True, begin="0s"):
    """Constellation star: solid core, soft halo, slow breathing ring."""
    out = (
        f'<circle cx="{x}" cy="{y}" r="{round(r*2.4,1)}" fill="{color}" opacity="0.14"/>'
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'
    )
    if pulse:
        out += (
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{color}" stroke-opacity="0">'
            f'<animate attributeName="r" values="{r};{round(r*3.2,1)};{r}" dur="6s" '
            f'begin="{begin}" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values="0.6;0;0.6" dur="6s" '
            f'begin="{begin}" repeatCount="indefinite"/></circle>'
        )
    return out


# ---------------------------------------------------------------- header
def header():
    w, h = 1200, 330
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="Ahmed Kamal Alshareef - Software Engineer, Applications and Data Systems">',
        "<defs>",
        f'<radialGradient id="neb1" cx="16%" cy="24%" r="58%">'
        f'<stop offset="0%" stop-color="{VIOLET}" stop-opacity="0.50"/>'
        f'<stop offset="100%" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>',
        f'<radialGradient id="neb2" cx="84%" cy="76%" r="56%">'
        f'<stop offset="0%" stop-color="{CYAN}" stop-opacity="0.30"/>'
        f'<stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>',
        f'<radialGradient id="neb3" cx="60%" cy="6%" r="48%">'
        f'<stop offset="0%" stop-color="#4338CA" stop-opacity="0.34"/>'
        f'<stop offset="100%" stop-color="#4338CA" stop-opacity="0"/></radialGradient>',
        f'<linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="#FFFFFF"/><stop offset="58%" stop-color="{LILAC}"/>'
        f'<stop offset="100%" stop-color="{CYAN}"/></linearGradient>',
        f'<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="{VIOLET}" stop-opacity="0"/>'
        f'<stop offset="45%" stop-color="{LILAC}" stop-opacity="0.9"/>'
        f'<stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>',
        "</defs>",
        f'<rect width="{w}" height="{h}" fill="{BG}"/>',
        f'<rect width="{w}" height="{h}" fill="url(#neb1)"><animate attributeName="opacity" '
        f'values="0.85;1;0.85" dur="16s" repeatCount="indefinite"/></rect>',
        f'<rect width="{w}" height="{h}" fill="url(#neb2)"><animate attributeName="opacity" '
        f'values="1;0.78;1" dur="20s" repeatCount="indefinite"/></rect>',
        f'<rect width="{w}" height="{h}" fill="url(#neb3)"/>',
        starfield(w, h, 140, 7, 0.4, 1.3, 0.7),
        starfield(w, h, 45, 21, 1.0, 1.9, 0.95),
        flare(150, 66, 9),
        flare(118, 272, 6, TEXT, 0.7),
    ]

    # Right-hand constellation: fixed shape, one slow pulse travelling it.
    stars = [(852, 96), (932, 152), (1016, 118), (1088, 178),
             (1000, 216), (912, 244), (836, 196)]
    path = "M " + " L ".join(f"{x} {y}" for x, y in stars)
    svg.append(
        f'<path id="hcon" d="{path}" fill="none" stroke="{LILAC}" stroke-opacity="0.32" '
        f'stroke-width="1.2" stroke-linejoin="round"/>'
        f'<path d="M852 96 L1016 118 M1000 216 L836 196" stroke="{LILAC}" stroke-opacity="0.14" '
        f'stroke-width="1" fill="none"/>'
    )
    for i, (x, y) in enumerate(stars):
        bright = i in (0, 3, 5)
        svg.append(star_node(x, y, CYAN if bright else TEXT, 4.6 if bright else 3.0,
                             pulse=bright, begin=f"-{i*1.7}s"))
    svg.append(
        f'<circle r="3.4" fill="{CYAN}"><animateMotion dur="22s" repeatCount="indefinite">'
        f'<mpath href="#hcon"/></animateMotion></circle>'
    )

    svg.append(
        f'<text x="80" y="128" font-family="{FONT}" font-size="46" font-weight="700" '
        f'letter-spacing="2.5" fill="url(#nameGrad) #E6EAF5">AHMED KAMAL ALSHAREEF</text>'
        f'<text x="82" y="164" font-family="{FONT}" font-size="19" font-weight="600" '
        f'fill="{TEXT}" opacity="0.92">Software Engineer &#183; Applications &amp; Data Systems</text>'
        f'<rect x="80" y="182" width="470" height="1.6" fill="url(#rule)"/>'
        f'<text x="82" y="212" font-family="{MONO}" font-size="13.5" fill="{MUTED}">'
        f'BSc Computer Science &#183; Umm Al-Qura University &#183; Makkah, Saudi Arabia</text>'
        f'<text x="82" y="236" font-family="{MONO}" font-size="13.5" fill="{MUTED}">'
        f'Flutter &#183; React + TypeScript &#183; Node.js &#183; SQL &#183; Applied AI</text>'
    )
    svg.append(
        f'<g transform="translate(80,262)">'
        f'<rect width="232" height="30" rx="15" fill="{MINT}" fill-opacity="0.10" '
        f'stroke="{MINT}" stroke-opacity="0.45"/>'
        f'<circle cx="20" cy="15" r="4.5" fill="{MINT}"><animate attributeName="opacity" '
        f'values="1;0.25;1" dur="2.6s" repeatCount="indefinite"/></circle>'
        f'<text x="34" y="19.5" font-family="{MONO}" font-size="12.5" fill="{MINT}">'
        f'open to junior SWE roles</text></g>'
    )
    svg.append("</svg>")
    return "\n".join(svg)


# ---------------------------------------------------------------- stack map
def stackmap():
    """The stack as six named constellations on one chart."""
    w, h = 1220, 700
    clusters = [
        ("MOBILE", CYAN, ["Flutter", "Dart", "Firebase", "Firestore"]),
        ("WEB", VIOLET, ["React", "TypeScript", "JavaScript", "Tailwind"]),
        ("DATA", AMBER, ["SQL", "PostgreSQL", "Prisma", "SQLite"]),
        ("BACKEND", MINT, ["Node.js", "REST APIs", "Cloudflare Workers"]),
        ("APPLIED AI", ROSE, ["Groq API", "Workers AI", "Grounded flows"]),
        ("ENGINEERING", LILAC, ["Git", "GitHub Actions", "Auth &amp; RBAC", "Testing"]),
    ]
    shape = [(20, 0), (170, 42), (34, 100), (184, 142)]
    cols = [110, 500, 890]
    rows = [190, 452]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="Technology stack drawn as six labelled constellations">',
        f'<rect width="{w}" height="{h}" fill="{BG}"/>',
        starfield(w, h, 150, 11, 0.4, 1.2, 0.6),
        f'<text x="{w//2}" y="58" text-anchor="middle" font-family="{FONT}" font-size="18" '
        f'font-weight="700" letter-spacing="4" fill="{TEXT}">STACK MAP</text>',
        f'<text x="{w//2}" y="84" text-anchor="middle" font-family="{MONO}" font-size="12.5" '
        f'fill="{MUTED}">six constellations &#183; grouped by the layer they belong to</text>',
    ]
    label_box(w // 2, 58, "STACK MAP", 18)
    label_box(w // 2, 84, "six constellations - grouped by the layer they belong to", 12.5)

    for i, (name, color, items) in enumerate(clusters):
        x0, y0 = cols[i % 3], rows[i // 3]
        pts = [(x0 + dx, y0 + dy) for dx, dy in shape[:len(items)]]

        svg.append(
            f'<circle cx="{x0-6}" cy="{y0-58}" r="4.5" fill="{color}"/>'
            f'<text x="{x0+8}" y="{y0-53}" font-family="{FONT}" font-size="13.5" '
            f'font-weight="700" letter-spacing="2.4" fill="{color}">{name}</text>'
        )
        label_box(x0 + 8, y0 - 53, name + "     ", 13.5, anchor="start")

        pid = f"c{i}"
        path = "M " + " L ".join(f"{x} {y}" for x, y in pts)
        svg.append(
            f'<path id="{pid}" d="{path}" fill="none" stroke="{color}" stroke-opacity="0.34" '
            f'stroke-width="1.2" stroke-linejoin="round"/>'
        )
        svg.append(
            f'<circle r="3" fill="{color}"><animateMotion dur="{15+i*3}s" begin="-{i*2}s" '
            f'repeatCount="indefinite"><mpath href="#{pid}"/></animateMotion></circle>'
        )
        for j, ((x, y), item) in enumerate(zip(pts, items)):
            svg.append(star_node(x, y, color, 5.0, begin=f"-{(i*4+j)*1.3}s"))
            svg.append(
                f'<text x="{x}" y="{y+28}" text-anchor="middle" font-family="{FONT}" '
                f'font-size="13" font-weight="600" fill="{TEXT}" opacity="0.94">{item}</text>'
            )
            label_box(x, y + 28, item.replace("&amp;", "&"), 13)

    svg.append(
        f'<text x="{w//2}" y="{h-32}" text-anchor="middle" font-family="{MONO}" font-size="12" '
        f'fill="{MUTED}">every star here is used in a shipped, public project</text>'
    )
    label_box(w // 2, h - 32, "every star here is used in a shipped, public project", 12)
    svg.append("</svg>")
    check_labels("stack-map")
    return "\n".join(svg)


# ---------------------------------------------------------------- radar
def radar():
    w, h = 700, 580
    cx, cy, R = 350, 310, 158
    axes = [
        ("Mobile (Flutter)", 0.92),
        ("Web (React / TS)", 0.85),
        ("Databases &amp; SQL", 0.80),
        ("APIs &amp; Auth / RBAC", 0.78),
        ("Applied AI", 0.70),
        ("Testing &amp; CI/CD", 0.66),
    ]
    bands = [("Foundational", 0.34), ("Working", 0.67), ("Advanced", 1.0)]
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="Skill coverage radar chart">',
        "<defs>",
        f'<linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{CYAN}" stop-opacity="0.34"/>'
        f'<stop offset="100%" stop-color="{VIOLET}" stop-opacity="0.34"/></linearGradient>',
        "</defs>",
        f'<rect width="{w}" height="{h}" fill="{BG}"/>',
        starfield(w, h, 80, 33, 0.4, 1.1, 0.5),
        f'<text x="{cx}" y="42" text-anchor="middle" font-family="{FONT}" font-size="17" '
        f'font-weight="700" letter-spacing="3.5" fill="{TEXT}">SKILL COVERAGE</text>',
        f'<text x="{cx}" y="66" text-anchor="middle" font-family="{MONO}" font-size="11.5" '
        f'fill="{MUTED}">self-assessed against shipped project work</text>',
    ]

    def pt(i, k):
        a = -math.pi / 2 + 2 * math.pi * i / len(axes)
        return round(cx + R * k * math.cos(a), 1), round(cy + R * k * math.sin(a), 1)

    for name, k in bands:
        pts = " ".join(f"{x},{y}" for x, y in (pt(i, k) for i in range(len(axes))))
        svg.append(f'<polygon points="{pts}" fill="none" stroke="{MUTED}" stroke-opacity="0.28" '
                   f'stroke-width="1"/>')
        svg.append(f'<text x="{cx+8}" y="{round(cy-R*k+14,1)}" font-family="{MONO}" font-size="9.5" '
                   f'fill="{MUTED}" opacity="0.85">{name}</text>')

    for i in range(len(axes)):
        x, y = pt(i, 1.0)
        svg.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{MUTED}" '
                   f'stroke-opacity="0.22"/>')

    shape = [pt(i, v) for i, (_n, v) in enumerate(axes)]
    pts = " ".join(f"{x},{y}" for x, y in shape)
    svg.append(f'<polygon points="{pts}" fill="url(#rg)" opacity="1">'
               f'<animate attributeName="opacity" values="0;1" dur="1.4s" begin="0.5s" '
               f'fill="freeze"/></polygon>')
    svg.append(f'<polygon points="{pts}" fill="none" stroke="{LILAC}" stroke-width="2" '
               f'stroke-linejoin="round" stroke-dasharray="1400" stroke-dashoffset="0">'
               f'<animate attributeName="stroke-dashoffset" values="1400;0" dur="1.9s" '
               f'fill="freeze"/></polygon>')

    for i, (name, _v) in enumerate(axes):
        x, y = shape[i]
        svg.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{CYAN}" opacity="1">'
                   f'<animate attributeName="opacity" values="0;1" dur="0.4s" '
                   f'begin="{round(1.2+i*0.12,2)}s" fill="freeze"/></circle>')
        lx, ly = pt(i, 1.30)
        anchor = "middle"
        if lx > cx + 12:
            anchor = "start"
        elif lx < cx - 12:
            anchor = "end"
        svg.append(f'<text x="{lx}" y="{ly+4}" text-anchor="{anchor}" font-family="{FONT}" '
                   f'font-size="12" font-weight="600" fill="{TEXT}" opacity="0.9">{name}</text>')
        label_box(lx, ly + 4, name.replace("&amp;", "&"), 12, anchor=anchor)

    svg.append("</svg>")
    check_labels("skill-radar")
    return "\n".join(svg)


# ---------------------------------------------------------------- timeline
def timeline():
    w, h = 1200, 330
    nodes = [
        ("Mar 2025 - Jun 2025", "IT Cooperative Trainee (600 h)",
         "Deanship of Technology &amp; Development, UQU", 160, 196, CYAN),
        ("Mar 2025 - Present", "Database Support Technician",
         "Safa Al Reef Blacksmithing Est., Makkah", 486, 128, VIOLET),
        ("2025 - 2026", "Shipped 9 public projects",
         "Flutter &#183; React + TypeScript &#183; Node.js", 760, 205, AMBER),
        ("23 Aug 2026", "BSc Computer Science",
         "Umm Al-Qura University, Makkah", 1050, 132, MINT),
    ]
    path = "M " + " L ".join(f"{x} {y}" for _d, _t, _s, x, y, _c in nodes)
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="Career and education timeline drawn as a constellation">',
        f'<rect width="{w}" height="{h}" fill="{BG}"/>',
        starfield(w, h, 110, 5, 0.4, 1.2, 0.6),
        f'<text x="60" y="46" font-family="{FONT}" font-size="16" font-weight="700" '
        f'letter-spacing="3" fill="{TEXT}">TRAJECTORY</text>',
        f'<text x="60" y="68" font-family="{MONO}" font-size="12" fill="{MUTED}">'
        f'education, work and shipped output on one line</text>',
        f'<path id="tl" d="{path}" fill="none" stroke="{LILAC}" stroke-opacity="0.35" '
        f'stroke-width="1.4" stroke-dasharray="1600" stroke-dashoffset="0">'
        f'<animate attributeName="stroke-dashoffset" values="1600;0" dur="2.4s" fill="freeze"/></path>',
        f'<circle r="4" fill="{CYAN}"><animateMotion dur="9s" begin="2.4s" '
        f'repeatCount="indefinite"><mpath href="#tl"/></animateMotion></circle>',
    ]
    label_box(60, 46, "TRAJECTORY    ", 16, anchor="start")
    label_box(60, 68, "education, work and shipped output on one line", 12, anchor="start")
    for i, (date, title, sub, x, y, color) in enumerate(nodes):
        b = round(2.4 + i * 0.25, 2)
        ty = y + 48 if y > 165 else y - 64
        svg.append(
            f'<g opacity="1"><animate attributeName="opacity" values="0;1" dur="0.6s" '
            f'begin="{b}s" fill="freeze"/>'
            + star_node(x, y, color, 6.0, begin=f"{b}s") +
            f'<text x="{x}" y="{ty}" text-anchor="middle" font-family="{MONO}" font-size="11.5" '
            f'fill="{color}">{date}</text>'
            f'<text x="{x}" y="{ty+22}" text-anchor="middle" font-family="{FONT}" font-size="14.5" '
            f'font-weight="700" fill="{TEXT}">{title}</text>'
            f'<text x="{x}" y="{ty+41}" text-anchor="middle" font-family="{FONT}" font-size="11.5" '
            f'fill="{MUTED}">{sub}</text></g>'
        )
        label_box(x, ty, date, 11.5)
        label_box(x, ty + 22, title, 14.5)
        label_box(x, ty + 41, sub.replace("&amp;", "&").replace("&#183;", "-"), 11.5)
    svg.append("</svg>")
    check_labels("timeline")
    return "\n".join(svg)


for name, fn in [("header.svg", header), ("stack-map.svg", stackmap),
                 ("skill-radar.svg", radar), ("timeline.svg", timeline)]:
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(fn())
    print(name, os.path.getsize(p), "bytes")
