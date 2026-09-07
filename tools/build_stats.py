# -*- coding: utf-8 -*-
"""Builds assets/stats.svg from the GitHub API.

Self-hosted replacement for the third-party README stat cards, which go down
often (github-readme-stats returned 503 and the activity graph 402 when this
was written). Run by .github/workflows/stats.yml on a daily schedule.

Usage: GITHUB_TOKEN=<token> python tools/build_stats.py
"""
import json
import os
import urllib.request
import urllib.error

USER = "whyKaiser"
API = "https://api.github.com"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "stats.svg")

BG = "#000000"
VIOLET = "#A24E28"
LILAC = "#C87A4B"
CYAN = "#C87A4B"
AMBER = "#B4693C"
MINT = "#D89A72"
ROSE = "#A24E28"
TEXT = "#FFFFFF"
MUTED = "#8A8A8A"
FONT = "'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',Consolas,'Courier New',monospace"

LANG_COLORS = {
    "Dart": "#00B4AB", "TypeScript": "#3178C6", "JavaScript": "#F1E05A",
    "HTML": "#E34C26", "CSS": "#563D7C", "Python": "#3572A5", "C#": "#178600",
    "Java": "#B07219", "Shell": "#89E051", "GDScript": "#478CBF",
    "C++": "#F34B7D", "Kotlin": "#A97BFF", "Swift": "#F05138", "Ruby": "#701516",
}
PALETTE = [CYAN, VIOLET, AMBER, MINT, ROSE, LILAC]


def get(path):
    req = urllib.request.Request(path if path.startswith("http") else API + path)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "whyKaiser-profile-stats")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    user = get("/users/%s" % USER)
    repos = get("/users/%s/repos?per_page=100&type=owner" % USER)
    own = [r for r in repos if not r["fork"]]
    stars = sum(r["stargazers_count"] for r in own)

    langs = {}
    for r in own:
        try:
            for name, size in get(r["languages_url"]).items():
                langs[name] = langs.get(name, 0) + size
        except urllib.error.HTTPError:
            continue

    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    return {
        "repos": len(own),
        "stars": stars,
        "followers": user["followers"],
        "langs": [(n, v * 100.0 / total) for n, v in top],
    }


def svg(d):
    w, h = 1200, 340
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="GitHub statistics for {USER}">',
        "<defs>",
        f'<radialGradient id="sg" cx="20%" cy="20%" r="70%">'
        f'<stop offset="0%" stop-color="{VIOLET}" stop-opacity="0.28"/>'
        f'<stop offset="100%" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>',
        "</defs>",
        f'<rect width="{w}" height="{h}" fill="{BG}"/>',
        f'<rect width="{w}" height="{h}" fill="url(#sg)"/>',
    ]

    # Faint fixed star dust; deterministic so the daily commit stays a no-op
    # unless the numbers actually changed.
    seed = 1
    for i in range(90):
        seed = (seed * 1103515245 + 12345) % 2147483648
        x = seed % w
        seed = (seed * 1103515245 + 12345) % 2147483648
        y = seed % h
        seed = (seed * 1103515245 + 12345) % 2147483648
        r = round(0.4 + (seed % 100) / 110.0, 2)
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="0.45"/>')

    parts.append(
        f'<text x="60" y="58" font-family="{FONT}" font-size="17" font-weight="700" '
        f'letter-spacing="3.5" fill="{TEXT}">GITHUB SIGNAL</text>'
        f'<text x="60" y="82" font-family="{MONO}" font-size="12" fill="{MUTED}">'
        f'generated from the GitHub API &#183; refreshed daily</text>'
    )

    tiles = [("PUBLIC REPOS", d["repos"], CYAN), ("STARS EARNED", d["stars"], AMBER),
             ("FOLLOWERS", d["followers"], MINT), ("LANGUAGES", len(d["langs"]), LILAC)]
    for i, (label, value, color) in enumerate(tiles):
        x = 60 + i * 124
        parts.append(
            f'<g transform="translate({x},120)">'
            f'<rect width="108" height="104" rx="14" fill="#0A0A0A" stroke="{color}" '
            f'stroke-opacity="0.42"/>'
            f'<circle cx="20" cy="24" r="4" fill="{color}"/>'
            f'<text x="54" y="66" text-anchor="middle" font-family="{FONT}" font-size="32" '
            f'font-weight="700" fill="{color}">{value}</text>'
            f'<text x="54" y="88" text-anchor="middle" font-family="{MONO}" font-size="9.5" '
            f'letter-spacing="1.2" fill="{MUTED}">{label}</text></g>'
        )

    parts.append(
        f'<text x="60" y="258" font-family="{MONO}" font-size="11" fill="{MUTED}">'
        f'own repositories only &#183; forks excluded</text>'
    )

    # Language bars
    bx, by = 590, 120
    parts.append(
        f'<text x="{bx}" y="{by-14}" font-family="{MONO}" font-size="11.5" '
        f'letter-spacing="1.6" fill="{MUTED}">LANGUAGE MIX &#183; BY BYTES OF CODE</text>'
    )
    scale = 340.0 / max(p for _n, p in d["langs"])
    for i, (name, pct) in enumerate(d["langs"]):
        y = by + 12 + i * 30
        color = LANG_COLORS.get(name, PALETTE[i % len(PALETTE)])
        bar = max(6.0, round(pct * scale, 1))
        parts.append(
            f'<circle cx="{bx+5}" cy="{y-4}" r="4" fill="{color}"/>'
            f'<text x="{bx+18}" y="{y}" font-family="{FONT}" font-size="12.5" '
            f'font-weight="600" fill="{TEXT}">{name}</text>'
            f'<rect x="{bx+140}" y="{y-12}" width="340" height="8" rx="4" fill="#1A1A1A"/>'
            f'<rect x="{bx+140}" y="{y-12}" width="{bar}" height="8" rx="4" fill="{color}">'
            f'<animate attributeName="width" values="0;{bar}" dur="1.1s" '
            f'begin="{round(0.15*i,2)}s" fill="freeze"/></rect>'
            f'<text x="{bx+570}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="11.5" '
            f'fill="{MUTED}">{pct:.1f}%</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    data = collect()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg(data))
    print("wrote", OUT, data["repos"], "repos,", data["stars"], "stars,",
          len(data["langs"]), "languages")
