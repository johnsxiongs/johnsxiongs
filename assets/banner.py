from pathlib import Path

OUT = Path(__file__).parent

TEXT = {
    "en": ("I build AI products end to end.", "Agent  ·  Backend  ·  Web  ·  iOS  ·  Android  ·  Ops"),
    "zh": ("一个人，把 AI 产品从头做到尾。", "Agent  ·  后端  ·  Web  ·  iOS  ·  Android  ·  运维"),
}

THEMES = {
    "light": dict(bg="#F5EFE3", border="#E6DCCA", grid="#E7DDCB", accent="#8E6B36", title="#1F1C17", muted="#6E665A"),
    "dark": dict(bg="#1A1814", border="#2C2822", grid="#2A2620", accent="#D2A75C", title="#F3ECDF", muted="#A39A8A"),
}

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', "
        "'Microsoft YaHei', 'Noto Sans CJK SC', 'Helvetica Neue', Helvetica, Arial, sans-serif")

YS = [232, 226, 230, 218, 222, 209, 213, 200, 204, 188, 194, 179, 171, 176, 160, 152, 158, 140, 128, 133, 112, 96]
POINTS = [(720 + i * 19.5, y) for i, y in enumerate(YS)]


def banner(tagline, skills, t):
    line = " ".join(f"{x:g},{y}" for x, y in POINTS)
    area = " ".join(f"L{x:g},{y}" for x, y in POINTS[1:])
    (x0, y0), (ex, ey) = POINTS[0], POINTS[-1]
    grid = "".join(f'<line x1="700" y1="{y}" x2="1140" y2="{y}" stroke="{t["grid"]}"/>' for y in (80, 130, 180, 230))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="Alexander Xiong. {tagline}">
  <defs>
    <linearGradient id="fill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t["accent"]}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="1199" height="299" rx="24" fill="{t["bg"]}" stroke="{t["border"]}"/>
  {grid}
  <path d="M{x0:g},{y0} {area} L{ex:g},252 L{x0:g},252 Z" fill="url(#fill)"/>
  <polyline points="{line}" fill="none" stroke="{t["accent"]}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="{ex:g}" cy="{ey}" r="12" fill="{t["accent"]}" fill-opacity="0.2"/>
  <circle cx="{ex:g}" cy="{ey}" r="5.5" fill="{t["accent"]}"/>
  <g font-family="{FONT}">
    <text x="72" y="130" font-size="60" font-weight="700" letter-spacing="-1" fill="{t["title"]}">Alexander Xiong</text>
    <text x="74" y="180" font-size="26" font-weight="500" fill="{t["accent"]}">{tagline}</text>
    <text x="74" y="224" font-size="19" fill="{t["muted"]}">{skills}</text>
  </g>
</svg>
'''


for lang, (tagline, skills) in TEXT.items():
    for theme, colors in THEMES.items():
        (OUT / f"banner-{lang}-{theme}.svg").write_text(banner(tagline, skills, colors))
