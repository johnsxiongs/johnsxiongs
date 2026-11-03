import base64
import functools
import re
import urllib.error
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent

SKILL_ICON = "https://raw.githubusercontent.com/LelouchFR/skill-icons/main/assets/{}.svg"
SIMPLE_ICON = "https://cdn.simpleicons.org/{}"
TILE_BG = {"light": "#F4F2ED", "dark": "#242938"}

# Plain ids come from go-skill-icons; "si:" ids from Simple Icons; "url:" is the project's own logo.
# go-skill-icons "element" is the Matrix chat app, so Element UI uses the logo from its own repo.
STACK = [
    ("Languages", "语言", [("Python", "python"), ("TypeScript", "typescript"), ("Swift", "swift"),
                          ("Kotlin", "kotlin"), ("Bash", "bash")]),
    ("AI", "AI", [("OpenAI", "chatgpt"), ("Claude", "claude"), ("Gemini", "gemini"), ("Grok", "grok"),
                  ("DeepSeek", "deepseek"), ("MCP", "mcp")]),
    ("Backend", "后端", [
        ("LangChain", "langchain"), ("LangGraph", "si:langgraph"), ("FastAPI", "fastapi"), ("Flask", "flask"),
        ("Django", "django"), ("Pydantic", "pydantic"), ("SQLAlchemy", "sqlalchemy"),
        ("SQLModel", "url:https://raw.githubusercontent.com/fastapi/sqlmodel/main/docs/img/icon.svg"),
        ("pandas", "pandas"), ("NumPy", "numpy"), ("PostgreSQL", "postgresql"), ("Redis", "redis"),
        ("Temporal", "si:temporal"), ("Supabase", "supabase"), ("Stripe", "stripe"), ("Firebase", "firebase")]),
    ("Web", "网页", [
        ("HTML", "html"), ("CSS", "css"), ("Vue", "vuejs"), ("Vuex", "vuejs"), ("Pinia", "pinia"), ("Nuxt", "nuxtjs"),
        ("Element UI", "url:https://raw.githubusercontent.com/ElemeFE/element/dev/examples/assets/images/element-logo-small.svg"),
        ("Ant Design Vue", "antdesign"), ("Tailwind CSS", "tailwindcss"), ("Vite", "vite"),
        ("ECharts", "si:apacheecharts"), ("G2Plot", "si:antv"), ("Node.js", "nodejs"), ("Yarn", "yarn")]),
    ("Mobile", "移动端", [("iOS", "apple"), ("Xcode", "xcode"), ("Android", "android"),
                         ("Jetpack Compose", "jetpackcompose"), ("Gradle", "gradle"), ("RevenueCat", "si:revenuecat")]),
    ("Infra", "运维", [("Docker", "docker"), ("Nginx", "nginx"), ("Traefik", "si:traefikproxy"),
                      ("GitHub Actions", "githubactions"), ("Prometheus", "prometheus"), ("Grafana", "grafana"),
                      ("Cloudflare", "cloudflare"), ("Tailscale", "tailscale"), ("Google Cloud", "gcp"),
                      ("Ubuntu", "ubuntu"), ("uv", "si:uv")]),
]

# Helvetica advance widths per 1000 em; they match Arial, which GitHub's sans-serif stack falls back to.
GLYPH = {" ": 278, ".": 278, "-": 333, "f": 278, "i": 222, "j": 222, "l": 222, "r": 333, "t": 278, "c": 500,
         "k": 500, "s": 500, "v": 500, "x": 500, "y": 500, "z": 500, "m": 833, "w": 722, "I": 278, "J": 500,
         "F": 611, "T": 611, "Z": 611, "L": 556, "C": 722, "D": 722, "H": 722, "N": 722, "R": 722, "U": 722,
         "G": 778, "O": 778, "Q": 778, "M": 833, "W": 944}
UPPER = 667

TEXT = {
    "en": ("I build AI products end to end.", "Agent  ·  Backend  ·  Web  ·  iOS  ·  Android  ·  Ops"),
    "zh": ("一个人，把 AI 产品从头做到尾。", "Agent  ·  后端  ·  Web  ·  iOS  ·  Android  ·  运维"),
}

THEMES = {
    "light": dict(bg="#F5EFE3", border="#E6DCCA", grid="#E7DDCB", accent="#8E6B36", title="#1F1C17", muted="#6E665A",
                  chip="#F7F2E8", chip_text="#3A352D"),
    "dark": dict(bg="#1A1814", border="#2C2822", grid="#2A2620", accent="#D2A75C", title="#F3ECDF", muted="#A39A8A",
                 chip="#1C1A16", chip_text="#E6DFD2"),
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


def fetch(url):
    # cdn.simpleicons.org answers 403 to the default Python-urllib User-Agent.
    request = urllib.request.Request(url, headers={"User-Agent": "profile-build"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode()


def contrast(a, b):
    def luminance(color):
        channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        r, g, b = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def simple_tile(slug, theme):
    svg = fetch(SIMPLE_ICON.format(slug))
    brand = re.search(r'fill="(#[0-9A-Fa-f]{6})"', svg).group(1)
    path = re.search(r'<path d="([^"]+)"', svg).group(1)
    bg = TILE_BG[theme]
    color = brand if contrast(brand, bg) >= 3 else ("#FFFFFF" if theme == "dark" else "#242938")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
            f'<rect width="256" height="256" rx="60" fill="{bg}"/>'
            f'<path transform="translate(56 56) scale(6)" fill="{color}" d="{path}"/></svg>')


def logo_tile(url, theme):
    data = base64.b64encode(fetch(url).encode()).decode()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
            f'<rect width="256" height="256" rx="60" fill="{TILE_BG[theme]}"/>'
            f'<image x="48" y="48" width="160" height="160" href="data:image/svg+xml;base64,{data}"/></svg>')


def icon(icon_id, theme):
    if icon_id.startswith("si:"):
        return simple_tile(icon_id[3:], theme)
    if icon_id.startswith("url:"):
        return logo_tile(icon_id[4:], theme)
    try:
        return fetch(SKILL_ICON.format(f"{icon_id}-{theme}"))
    except urllib.error.HTTPError:
        return fetch(SKILL_ICON.format(icon_id))


def text_width(text, size):
    return sum(GLYPH.get(ch, UPPER if ch.isupper() else 556) for ch in text) * size / 1000


def split_lines(widths, room, gap):
    """Fewest lines that fit `room`, with the widest line as narrow as possible."""
    def span(i, j):
        return sum(widths[i:j]) + gap * (j - i - 1)

    @functools.cache
    def best(i, k):
        if k == 1:
            return span(i, len(widths)), (len(widths),)
        return min((max(span(i, j), best(j, k - 1)[0]), (j,) + best(j, k - 1)[1])
                   for j in range(i + 1, len(widths) - k + 2))

    k = 1
    while best(0, k)[0] > room:
        k += 1
    return best(0, k)[1]


def stack(lang, theme, icons):
    # 846 px is the profile README column on github.com, so the image shows at its natural size.
    width, left, chip_h, icon_size, font, gap, group_gap = 846, 84, 30, 20, 13, 6, 14
    colors = THEMES[theme]
    names = ", ".join(name for *_, row in STACK for name, _ in row)
    parts, y = [], 0
    for en, zh, items in STACK:
        texts = [round(text_width(name, font), 1) for name, _ in items]
        chips = [round(6 + icon_size + 6 + text + 9, 1) for text in texts]
        parts.append(f'<text x="0" y="{y + 19.5:g}" font-size="14" font-weight="600" '
                     f'fill="{colors["title"]}">{en if lang == "en" else zh}</text>')
        start = 0
        for end in split_lines(chips, width - left, gap):
            x = left
            for (name, icon_id), text, chip in zip(items[start:end], texts[start:end], chips[start:end]):
                data = base64.b64encode(icons[icon_id].encode()).decode()
                # textLength pins each name to its Helvetica width, so other fonts cannot overflow the chip.
                parts.append(f'<rect x="{x:g}" y="{y}" width="{chip:g}" height="{chip_h}" rx="8" '
                             f'fill="{colors["chip"]}" stroke="{colors["border"]}"/>')
                parts.append(f'<image x="{x + 6:g}" y="{y + 5}" width="{icon_size}" height="{icon_size}" '
                             f'href="data:image/svg+xml;base64,{data}"/>')
                parts.append(f'<text x="{x + 6 + icon_size + 6:g}" y="{y + 19.5:g}" font-size="{font}" '
                             f'textLength="{text:g}" lengthAdjust="spacingAndGlyphs" '
                             f'fill="{colors["chip_text"]}">{name}</text>')
                x = round(x + chip + gap, 1)
            start = end
            y += chip_h + gap
        y += group_gap - gap
    height = y - group_gap
    body = "\n  ".join(parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label="{names}">\n'
            f'  <g font-family="{FONT}">\n  {body}\n  </g>\n</svg>\n')


for theme, colors in THEMES.items():
    icons = {icon_id: icon(icon_id, theme) for *_, row in STACK for _, icon_id in row}
    for lang, (tagline, skills) in TEXT.items():
        (OUT / f"banner-{lang}-{theme}.svg").write_text(banner(tagline, skills, colors))
        (OUT / f"stack-{lang}-{theme}.svg").write_text(stack(lang, theme, icons))
