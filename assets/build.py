import base64
import html
import re
import urllib.error
import urllib.request
from pathlib import Path

ASSETS = Path(__file__).parent
ROOT = ASSETS.parent

# 846 px is the profile README column on github.com, so every image shows at its natural size.
# All cards share this width, inner padding, radius and gap so their edges and text line up.
WIDTH, PAD, RADIUS, GAP = 846, 36, 16, 16

SKILL_ICON = "https://raw.githubusercontent.com/LelouchFR/skill-icons/main/assets/{}.svg"
SIMPLE_ICON = "https://cdn.simpleicons.org/{}"
LUCIDE = "https://cdn.jsdelivr.net/npm/lucide-static@1.66.0/icons/{}.svg"
TILE_BG = {"light": "#F4F2ED", "dark": "#242938"}

# Plain ids come from go-skill-icons; "si:" ids from Simple Icons; "url:" is the project's own logo.
# go-skill-icons "element" is the Matrix chat app, so Element UI uses the logo from its own repo.
# Each inner list is one line of related tools, most important first.
STACK = [
    ("Languages", "语言", [
        [("Python", "python"), ("TypeScript", "typescript"), ("Swift", "swift"), ("Kotlin", "kotlin"),
         ("Bash", "bash")],
    ]),
    ("Backend", "后端", [
        [("LangChain", "langchain"), ("LangGraph", "si:langgraph"), ("MCP", "mcp"), ("FastAPI", "fastapi"),
         ("Django", "django"), ("Flask", "flask")],
        [("PostgreSQL", "postgresql"), ("Redis", "redis"), ("SQLAlchemy", "sqlalchemy"),
         ("SQLModel", "url:https://raw.githubusercontent.com/fastapi/sqlmodel/main/docs/img/icon.svg"),
         ("Pydantic", "pydantic"), ("pandas", "pandas"), ("NumPy", "numpy")],
        [("Temporal", "si:temporal"), ("Supabase", "supabase"), ("Stripe", "stripe"), ("Firebase", "firebase")],
    ]),
    ("LLMs", "大模型", [
        [("OpenAI", "chatgpt"), ("Claude", "claude"), ("Gemini", "gemini"), ("DeepSeek", "deepseek"),
         ("Grok", "grok")],
    ]),
    ("Infra", "运维", [
        [("Docker", "docker"), ("Nginx", "nginx"), ("Traefik", "si:traefikproxy"),
         ("GitHub Actions", "githubactions"), ("Prometheus", "prometheus"), ("Grafana", "grafana")],
        [("Google Cloud", "gcp"), ("Cloudflare", "cloudflare"), ("Tailscale", "tailscale"), ("Ubuntu", "ubuntu"),
         ("uv", "si:uv")],
    ]),
    ("Web", "网页", [
        [("Vue", "vuejs"), ("Nuxt", "nuxtjs"), ("Pinia", "pinia"), ("Vuex", "vuejs"), ("HTML", "html"),
         ("CSS", "css"), ("Vite", "vite"), ("Node.js", "nodejs"), ("Yarn", "yarn")],
        [("Tailwind CSS", "tailwindcss"),
         ("Element UI", "url:https://raw.githubusercontent.com/ElemeFE/element/dev/examples/assets/images/element-logo-small.svg"),
         ("Ant Design Vue", "antdesign"), ("ECharts", "si:apacheecharts"), ("G2Plot", "si:antv")],
    ]),
    ("Mobile", "移动端", [
        [("iOS", "apple"), ("Xcode", "xcode"), ("Android", "android"), ("Jetpack Compose", "jetpackcompose"),
         ("Gradle", "gradle"), ("RevenueCat", "si:revenuecat")],
    ]),
]

COPY = {
    "en": dict(
        readme="README.md",
        switch=("zh", "./README.zh-CN.md"),
        tagline="Full-stack engineer with a backend focus",
        domains="Backend  ·  AI agents  ·  Data  ·  Infra  ·  Web  ·  Mobile",
        status="Open to backend and full-stack roles",
        location="Singapore",
        about=("About", [
            "I'm a full-stack engineer in Singapore with a backend focus. Most of my work is the part users "
            "don't see: APIs, data, background jobs and the servers they run on. I also build the web and mobile "
            "apps, so I can take an AI product from idea to launch on my own.",
            "Since April 2025 I've built and run Quant AI, an AI research assistant for investors, by myself. "
            "It is live on the web and the App Store, and investors use it to research stocks, crypto and "
            "commodities.",
        ]),
        skills=("What I do", [
            ("server", "Backend", "I build services in Python and FastAPI on PostgreSQL and Redis, run scheduled "
             "jobs on Temporal, and handle payments, sign-in and push notifications."),
            ("bot", "AI agents", "I build agents that work reliably in production: multi-turn conversations across "
             "markets, streaming answers, long-term memory, and automatic fallback when a model fails."),
            ("chart-line", "Quant research", "I built a rating system for about 200 US stocks and test it against "
             "real market returns, so decisions rest on statistics rather than a few lucky picks."),
            ("cloud-cog", "Infrastructure", "I run production myself, including automated releases, monitoring "
             "and alerts."),
            ("monitor-smartphone", "Web and mobile", "I build native apps for iPhone, iPad, Mac and Android, plus "
             "the web app, all in 16 languages."),
            ("git-pull-request", "AI-assisted development", "I set up a workflow where AI coding agents implement, "
             "test and review changes, which lets one person maintain a product of this size."),
        ]),
        stack="Tech stack",
        principles=("How I work", [
            ("Keep it simple", "I choose the simplest design that solves the problem and remove code that is no "
             "longer needed."),
            ("Fix the root cause", "I trace a problem to its source instead of hiding the symptom."),
            ("Trust real results", "I check logs and real behavior before I call something done."),
            ("Use proven tools", "I start with official tools and common practice, and build my own only when "
             "there is a clear reason."),
            ("Document decisions", "I write down key technical decisions so others can pick up the work quickly."),
        ]),
    ),
    "zh": dict(
        readme="README.zh-CN.md",
        switch=("en", "https://github.com/johnsxiongs"),
        tagline="偏后端的全栈工程师",
        domains="后端  ·  AI Agent  ·  数据  ·  运维  ·  网页  ·  移动端",
        status="寻找后端或全栈岗位",
        location="新加坡",
        about=("关于我", [
            "我是新加坡的一名全栈工程师，偏后端。我的主要工作在用户看不到的部分：接口、数据、后台任务和运行它们的服务器。"
            "我也开发网页和移动端，所以能一个人把 AI 产品从想法做到上线。",
            "2025 年 4 月起，我独立开发和运营 Quant AI，这是一款面向投资者的 AI 研究助手。"
            "它已在网页和 App Store 上线，投资者用它研究股票、加密货币和大宗商品。",
        ]),
        skills=("我擅长什么", [
            ("server", "后端", "用 Python 和 FastAPI 开发服务，数据存在 PostgreSQL 和 Redis，定时任务跑在 Temporal 上，"
             "支付、登录和推送通知也由我实现。"),
            ("bot", "AI Agent", "开发能在生产环境稳定运行的 AI Agent，支持跨市场的多轮对话、流式回答和长期记忆，"
             "主模型出错时自动切换到备用模型。"),
            ("chart-line", "量化研究", "搭建了覆盖约 200 只美股的评级系统，并用真实的市场收益做统计检验，"
             "让判断建立在数据上，而不是几次碰巧选对。"),
            ("cloud-cog", "运维", "独立运维生产环境，包括自动化发布、监控和告警。"),
            ("monitor-smartphone", "网页和移动端", "开发 iPhone、iPad、Mac 和安卓的原生应用以及网页应用，全部支持 16 种语言。"),
            ("git-pull-request", "AI 辅助开发", "搭建了由 AI 编程代理完成实现、测试和审查的开发流程，"
             "让一个人也能维护这种规模的产品。"),
        ]),
        stack="技术栈",
        principles=("做事原则", [
            ("保持简单", "选择能解决问题的最简单设计，删掉不再需要的代码。"),
            ("解决根因", "找到问题的源头再修，不掩盖表面症状。"),
            ("以实际结果为准", "看日志和真实运行结果，确认无误才算完成。"),
            ("优先用成熟方案", "先用官方工具和业界通行做法，有明确理由才自己开发。"),
            ("记录决策", "把关键技术决策写成文档，方便别人快速接手。"),
        ]),
    ),
}
SWITCH_LABEL = {"en": "English", "zh": "简体中文"}

THEMES = {
    "light": dict(hero="#F5EFE3", card="#FBF8F2", chip="#FFFFFF", border="#E9E0CF", grid="#E7DDCB",
                  accent="#8E6B36", soft="#F1E6D2", title="#1F1C17", body="#4A443A", muted="#7A7164"),
    "dark": dict(hero="#1E1B16", card="#161410", chip="#1E1B16", border="#2C2822", grid="#2A2620",
                 accent="#D2A75C", soft="#2A241A", title="#F3ECDF", body="#D3CABB", muted="#A39A8A"),
}

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', "
        "'Microsoft YaHei', 'Noto Sans CJK SC', 'Helvetica Neue', Helvetica, Arial, sans-serif")

# Helvetica advance widths per 1000 em; they match Arial, which GitHub's sans-serif stack falls back to.
GLYPH = {" ": 278, ".": 278, ",": 278, ":": 278, ";": 278, "!": 278, "'": 191, "·": 278, "-": 333, "(": 333,
         ")": 333, "/": 278, "&": 667, "f": 278, "i": 222, "j": 222, "l": 222, "r": 333, "t": 278, "c": 500,
         "k": 500, "s": 500, "v": 500, "x": 500, "y": 500, "z": 500, "m": 833, "w": 722, "I": 278, "J": 500,
         "F": 611, "T": 611, "Z": 611, "L": 556, "C": 722, "D": 722, "H": 722, "N": 722, "R": 722, "U": 722,
         "G": 778, "O": 778, "Q": 778, "M": 833, "W": 944}
CJK = "⺀-鿿　-〿＀-￯"
NO_LINE_START = "，。：；、）"

CHART = [232, 226, 230, 218, 222, 209, 213, 200, 204, 188, 194, 179, 171, 176, 160, 152, 158, 140, 128, 133, 112, 96]


def fetch(url):
    # cdn.simpleicons.org answers 403 to the default Python-urllib User-Agent.
    request = urllib.request.Request(url, headers={"User-Agent": "profile-build"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode()


def width(text, size, bold=False):
    units = sum(1000 if re.match(f"[{CJK}]", ch) else GLYPH.get(ch, 667 if ch.isupper() else 556) for ch in text)
    return units * size / 1000 * (1.08 if bold else 1)


def wrap(text, size, limit):
    lines, line = [], ""
    for token in re.findall(rf"[{CJK}]|[^\s{CJK}]+|\s+", text):
        if not line and token.isspace():
            continue
        if line and not token.isspace() and token not in NO_LINE_START and width(line + token, size) > limit:
            lines.append(line.rstrip())
            line = token
        else:
            line += token
    return lines + [line.rstrip()]


def text(x, y, content, size, fill, weight=None, spacing=None, pin=False):
    attrs = f'x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{fill}"'
    if weight:
        attrs += f' font-weight="{weight}"'
    if spacing:
        attrs += f' letter-spacing="{spacing:g}"'
    if pin:
        # Pins the line to its Helvetica width, so a wider fallback font cannot overflow the layout.
        attrs += f' textLength="{width(content, size):.1f}" lengthAdjust="spacingAndGlyphs"'
    return f"<text {attrs}>{html.escape(content)}</text>"


def rect(x, y, w, h, r, fill, stroke=None):
    edge = f' stroke="{stroke}"' if stroke else ""
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="{fill}"{edge}/>'


def line_icon(inner, x, y, size, color):
    return (f'<svg x="{x:g}" y="{y:g}" width="{size:g}" height="{size:g}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')


def document(w, h, label, parts):
    body = "\n  ".join(parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" viewBox="0 0 {w:g} {h:g}" '
            f'role="img" aria-label="{html.escape(label)}">\n  <g font-family="{FONT}">\n  {body}\n  </g>\n</svg>\n')


def lucide(name):
    inner = re.search(r"<svg[^>]*>(.*)</svg>", fetch(LUCIDE.format(name)), re.S).group(1)
    return re.sub(r"\s+", " ", inner).strip()


def contrast(a, b):
    def luminance(color):
        channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        r, g, b = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def logo(icon_id, theme):
    bg = TILE_BG[theme]
    tile = f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><rect width="256" height="256" rx="60" fill="{bg}"/>'
    if icon_id.startswith("si:"):
        svg = fetch(SIMPLE_ICON.format(icon_id[3:]))
        brand = re.search(r'fill="(#[0-9A-Fa-f]{6})"', svg).group(1)
        path = re.search(r'<path d="([^"]+)"', svg).group(1)
        color = brand if contrast(brand, bg) >= 3 else ("#FFFFFF" if theme == "dark" else "#242938")
        return f'{tile}<path transform="translate(56 56) scale(6)" fill="{color}" d="{path}"/></svg>'
    if icon_id.startswith("url:"):
        data = base64.b64encode(fetch(icon_id[4:]).encode()).decode()
        return f'{tile}<image x="48" y="48" width="160" height="160" href="data:image/svg+xml;base64,{data}"/></svg>'
    try:
        return fetch(SKILL_ICON.format(f"{icon_id}-{theme}"))
    except urllib.error.HTTPError:
        return fetch(SKILL_ICON.format(icon_id))


def hero(c, t, ui):
    h = 232
    xs = [520 + i * (WIDTH - PAD - 520) / (len(CHART) - 1) for i in range(len(CHART))]
    ys = [50 + (v - 80) * 0.8 for v in CHART]
    points = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    status_x = PAD + 16 + width(c["status"], 13.5, bold=True) + 24
    parts = [
        '<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{t["accent"]}" stop-opacity="0.2"/>'
        f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></linearGradient></defs>',
        rect(0.5, 0.5, WIDTH - 1, h - 1, RADIUS, t["hero"], t["border"]),
        *(f'<line x1="504" y1="{y}" x2="{WIDTH - PAD}" y2="{y}" stroke="{t["grid"]}"/>' for y in (50, 90, 130, 170)),
        f'<path d="M{xs[0]:.1f},{ys[0]:.1f} L{points.replace(" ", " L")} L{xs[-1]:.1f},186 L{xs[0]:.1f},186 Z" fill="url(#fade)"/>',
        f'<polyline points="{points}" fill="none" stroke="{t["accent"]}" stroke-width="2.5" '
        'stroke-linejoin="round" stroke-linecap="round"/>',
        f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="9" fill="{t["accent"]}" fill-opacity="0.2"/>',
        f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="4" fill="{t["accent"]}"/>',
        text(PAD - 2, 86, "Alexander Xiong", 44, t["title"], 700, spacing=-0.8),
        text(PAD, 120, c["tagline"], 19, t["accent"], 500),
        text(PAD, 148, c["domains"], 14, t["muted"]),
        f'<circle cx="{PAD + 4}" cy="{192 - 4.5}" r="4" fill="{t["accent"]}"/>',
        text(PAD + 16, 192, c["status"], 13.5, t["body"], 500),
        line_icon(ui["map-pin"], status_x, 192 - 12.5, 15, t["muted"]),
        text(status_x + 20, 192, c["location"], 13.5, t["body"], 500),
    ]
    return document(WIDTH, h, f'Alexander Xiong. {c["tagline"]}. {c["status"]}. {c["location"]}.', parts)


def card(label, height, inner, t):
    return [rect(0.5, 0.5, WIDTH - 1, height - 1, RADIUS, t["card"], t["border"]),
            text(PAD, 44, label.upper(), 12, t["accent"], 700, spacing=1.6), *inner]


def about(c, t):
    inner, y = [], 64
    for i, paragraph in enumerate(c["about"][1]):
        y += 10 if i else 0
        for line in wrap(paragraph, 15, WIDTH - 2 * PAD):
            inner.append(text(PAD, y + 18, line, 15, t["body"], pin=True))
            y += 25
    return inner, y + 32


def skills(c, t, ui):
    column_gap, tile, row_gap = 28, 36, 26
    column = (WIDTH - 2 * PAD - column_gap) / 2
    offset = tile + 14
    inner, y, items = [], 67, c["skills"][1]
    for row in range(0, len(items), 2):
        heights = []
        for k, (icon_name, title, desc) in enumerate(items[row:row + 2]):
            x = PAD + k * (column + column_gap)
            lines = wrap(desc, 13.5, column - offset)
            inner += [rect(x, y - 2, tile, tile, 10, t["soft"]), line_icon(ui[icon_name], x + 8, y + 6, 20, t["accent"]),
                      text(x + offset, y + 15, title, 15, t["title"], 600)]
            inner += [text(x + offset, y + 38 + n * 21, line, 13.5, t["body"], pin=True) for n, line in enumerate(lines)]
            heights.append(max(tile, 26 + len(lines) * 21))
        y += max(heights) + row_gap
    return inner, y - row_gap + 30


def stack(lang, t, logos):
    label_w, chip_h, size, font, gap, group_gap = 84, 28, 18, 12.5, 6, 12
    inner, y = [], 64
    for en, zh, lines in STACK:
        inner.append(text(PAD, y + 18.5, en if lang == "en" else zh, 13, t["title"], 600))
        for line in lines:
            x = PAD + label_w
            for name, icon_id in line:
                name_w = round(width(name, font), 1)
                chip = round(5 + size + 6 + name_w + 8, 1)
                if x + chip > WIDTH - PAD:
                    raise SystemExit(f"{en}: the line ending with {name} is wider than the card; split it in STACK")
                data = base64.b64encode(logos[icon_id].encode()).decode()
                inner += [rect(x, y, chip, chip_h, 7, t["chip"], t["border"]),
                          f'<image x="{x + 5:g}" y="{y + 5}" width="{size}" height="{size}" '
                          f'href="data:image/svg+xml;base64,{data}"/>',
                          text(x + 5 + size + 6, y + 18.5, name, font, t["body"], pin=True)]
                x = round(x + chip + gap, 1)
            y += chip_h + gap
        y += group_gap - gap
    return inner, y - group_gap + 30


def principles(c, t):
    number_w, title_w, line_h = 40, 168, 22
    desc_x = PAD + number_w + title_w
    inner, y, items = [], 53, c["principles"][1]
    for i, (title, desc) in enumerate(items):
        lines = wrap(desc, 14, WIDTH - PAD - desc_x)
        base = y + 29
        inner += [text(PAD, base, f"{i + 1:02d}", 13, t["accent"], 700),
                  text(PAD + number_w, base, title, 14.5, t["title"], 600)]
        inner += [text(desc_x, base + n * line_h, line, 14, t["body"], pin=True) for n, line in enumerate(lines)]
        y = base + (len(lines) - 1) * line_h + 19
        if i < len(items) - 1:
            inner.append(f'<line x1="{PAD}" y1="{y}" x2="{WIDTH - PAD}" y2="{y}" stroke="{t["border"]}"/>')
    return inner, y + 20


def body(lang, t, ui, logos):
    c = COPY[lang]
    sections = [(c["about"][0], about(c, t)), (c["skills"][0], skills(c, t, ui)),
                (c["stack"], stack(lang, t, logos)), (c["principles"][0], principles(c, t))]
    parts, y = [], 0
    for label, (inner, height) in sections:
        parts += [f'<g transform="translate(0 {y:g})">', *card(label, height, inner, t), "</g>"]
        y += height + GAP
    return document(WIDTH, y - GAP, alt_text(c), parts)


def pill(label, icon, t, trailing=None):
    h, size = 32, 13
    label_w = width(label, size) * 1.04
    w = 12 + 15 + 8 + label_w + (8 + 13 if trailing else 0) + 14
    parts = [rect(0.5, 0.5, w - 1, h - 1, 8, t["card"], t["border"]), line_icon(icon, 12, 8.5, 15, t["accent"]),
             f'<text x="35" y="20.5" font-size="{size}" font-weight="500" fill="{t["title"]}" '
             f'textLength="{label_w:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(label)}</text>']
    if trailing:
        parts.append(line_icon(trailing, w - 14 - 13, 9.5, 13, t["muted"]))
    return document(w, h, label, parts)


def alt_text(c):
    skills_text = " ".join(f"{title}: {desc}" for _, title, desc in c["skills"][1])
    stack_text = ", ".join(name for *_, lines in STACK for line in lines for name, _ in line)
    principle_text = " ".join(f"{title}: {desc}" for title, desc in c["principles"][1])
    return (f'{c["about"][0]}. {" ".join(c["about"][1])} {c["skills"][0]}. {skills_text} '
            f'{c["stack"]}: {stack_text}. {c["principles"][0]}. {principle_text}')


def picture(name, alt, height=None):
    size = f' height="{height}"' if height else ""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/{name}-dark.svg">'
            f'<source media="(prefers-color-scheme: light)" srcset="./assets/{name}-light.svg">'
            f'<img alt="{html.escape(alt)}" src="./assets/{name}-light.svg"{size}></picture>')


def readme(lang):
    c = COPY[lang]
    target, link = c["switch"]
    banner_alt = f'Alexander Xiong. {c["tagline"]}. {c["status"]}. {c["location"]}.'
    site = picture("pill-site", "aiquant.io", 32)
    switch = picture(f"pill-{target}", SWITCH_LABEL[target], 32)
    return ("<!-- Generated by assets/build.py. Edit that file and run it; do not edit this one. -->\n\n"
            f"{picture(f'banner-{lang}', banner_alt)}\n\n"
            f'<p>\n  <a href="https://aiquant.io">{site}</a>&nbsp;\n  <a href="{link}">{switch}</a>\n</p>\n\n'
            f"{picture(f'body-{lang}', alt_text(c))}\n")


ui = {name: lucide(name) for name in
      {"map-pin", "globe", "languages", "arrow-up-right", *(i for c in COPY.values() for i, *_ in c["skills"][1])}}
for theme, t in THEMES.items():
    logos = {icon_id: logo(icon_id, theme) for *_, lines in STACK for line in lines for _, icon_id in line}
    (ASSETS / f"pill-site-{theme}.svg").write_text(pill("aiquant.io", ui["globe"], t, ui["arrow-up-right"]))
    for lang in COPY:
        (ASSETS / f"banner-{lang}-{theme}.svg").write_text(hero(COPY[lang], t, ui))
        (ASSETS / f"body-{lang}-{theme}.svg").write_text(body(lang, t, ui, logos))
        (ASSETS / f"pill-{lang}-{theme}.svg").write_text(pill(SWITCH_LABEL[lang], ui["languages"], t))
for lang, c in COPY.items():
    (ROOT / c["readme"]).write_text(readme(lang))
