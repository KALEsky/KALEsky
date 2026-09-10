#!/usr/bin/env python3
"""Rebuild KALEsky's self-contained SVG assets. Python 3.9+, standard library only.

Usage: python tools/build_profile_assets.py
No API keys, network calls, GitHub Actions or extra packages are required.
Font Awesome brand paths retain their attribution in THIRD_PARTY_NOTICES.md.
"""
from pathlib import Path
from html import escape
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "profile"
BRANDS = {'python': {'width': 448, 'height': 512, 'path': 'M439.8 200.5c-7.7-30.9-22.3-54.2-53.4-54.2h-40.1v47.4c0 36.8-31.2 67.8-66.8 67.8H172.7c-29.2 0-53.4 25-53.4 54.3v101.8c0 29 25.2 46 53.4 54.3 33.8 9.9 66.3 11.7 106.8 0 26.9-7.8 53.4-23.5 53.4-54.3v-40.7H226.2v-13.6h160.2c31.1 0 42.6-21.7 53.4-54.2 11.2-33.5 10.7-65.7 0-108.6zM286.2 404c11.1 0 20.1 9.1 20.1 20.3 0 11.3-9 20.4-20.1 20.4-11 0-20.1-9.2-20.1-20.4.1-11.3 9.1-20.3 20.1-20.3zM167.8 248.1h106.8c29.7 0 53.4-24.5 53.4-54.3V91.9c0-29-24.4-50.7-53.4-55.6-35.8-5.9-74.7-5.6-106.8.1-45.2 8-53.4 24.7-53.4 55.6v40.7h106.9v13.6h-147c-31.1 0-58.3 18.7-66.8 54.2-9.8 40.7-10.2 66.1 0 108.6 7.6 31.6 25.7 54.2 56.8 54.2H101v-48.8c0-35.3 30.5-66.4 66.8-66.4zm-6.7-142.6c-11.1 0-20.1-9.1-20.1-20.3.1-11.3 9-20.4 20.1-20.4 11 0 20.1 9.2 20.1 20.4s-9 20.3-20.1 20.3z'}, 'java': {'width': 384, 'height': 512, 'path': 'M277.74 312.9c9.8-6.7 23.4-12.5 23.4-12.5s-38.7 7-77.2 10.2c-47.1 3.9-97.7 4.7-123.1 1.3-60.1-8 33-30.1 33-30.1s-36.1-2.4-80.6 19c-52.5 25.4 130 37 224.5 12.1zm-85.4-32.1c-19-42.7-83.1-80.2 0-145.8C296 53.2 242.84 0 242.84 0c21.5 84.5-75.6 110.1-110.7 162.6-23.9 35.9 11.7 74.4 60.2 118.2zm114.6-176.2c.1 0-175.2 43.8-91.5 140.2 24.7 28.4-6.5 54-6.5 54s62.7-32.4 33.9-72.9c-26.9-37.8-47.5-56.6 64.1-121.3zm-6.1 270.5a12.19 12.19 0 0 1-2 2.6c128.3-33.7 81.1-118.9 19.8-97.3a17.33 17.33 0 0 0-8.2 6.3 70.45 70.45 0 0 1 11-3c31-6.5 75.5 41.5-20.6 91.4zM348 437.4s14.5 11.9-15.9 21.2c-57.9 17.5-240.8 22.8-291.6.7-18.3-7.9 16-19 26.8-21.3 11.2-2.4 17.7-2 17.7-2-20.3-14.3-131.3 28.1-56.4 40.2C232.84 509.4 401 461.3 348 437.4zM124.44 396c-78.7 22 47.9 67.4 148.1 24.5a185.89 185.89 0 0 1-28.2-13.8c-44.7 8.5-65.4 9.1-106 4.5-33.5-3.8-13.9-15.2-13.9-15.2zm179.8 97.2c-78.7 14.8-175.8 13.1-233.3 3.6 0-.1 11.8 9.7 72.4 13.6 92.2 5.9 233.8-3.3 237.1-46.9 0 0-6.4 16.5-76.2 29.7zM260.64 353c-59.2 11.4-93.5 11.1-136.8 6.6-33.5-3.5-11.6-19.7-11.6-19.7-86.8 28.8 48.2 61.4 169.5 25.9a60.37 60.37 0 0 1-21.1-12.8z'}, 'linux': {'width': 448, 'height': 512, 'path': 'M220.8 123.3c1 .5 1.8 1.7 3 1.7 1.1 0 2.8-.4 2.9-1.5.2-1.4-1.9-2.3-3.2-2.9-1.7-.7-3.9-1-5.5-.1-.4.2-.8.7-.6 1.1.3 1.3 2.3 1.1 3.4 1.7zm-21.9 1.7c1.2 0 2-1.2 3-1.7 1.1-.6 3.1-.4 3.5-1.6.2-.4-.2-.9-.6-1.1-1.6-.9-3.8-.6-5.5.1-1.3.6-3.4 1.5-3.2 2.9.1 1 1.8 1.5 2.8 1.4zM420 403.8c-3.6-4-5.3-11.6-7.2-19.7-1.8-8.1-3.9-16.8-10.5-22.4-1.3-1.1-2.6-2.1-4-2.9-1.3-.8-2.7-1.5-4.1-2 9.2-27.3 5.6-54.5-3.7-79.1-11.4-30.1-31.3-56.4-46.5-74.4-17.1-21.5-33.7-41.9-33.4-72C311.1 85.4 315.7.1 234.8 0 132.4-.2 158 103.4 156.9 135.2c-1.7 23.4-6.4 41.8-22.5 64.7-18.9 22.5-45.5 58.8-58.1 96.7-6 17.9-8.8 36.1-6.2 53.3-6.5 5.8-11.4 14.7-16.6 20.2-4.2 4.3-10.3 5.9-17 8.3s-14 6-18.5 14.5c-2.1 3.9-2.8 8.1-2.8 12.4 0 3.9.6 7.9 1.2 11.8 1.2 8.1 2.5 15.7.8 20.8-5.2 14.4-5.9 24.4-2.2 31.7 3.8 7.3 11.4 10.5 20.1 12.3 17.3 3.6 40.8 2.7 59.3 12.5 19.8 10.4 39.9 14.1 55.9 10.4 11.6-2.6 21.1-9.6 25.9-20.2 12.5-.1 26.3-5.4 48.3-6.6 14.9-1.2 33.6 5.3 55.1 4.1.6 2.3 1.4 4.6 2.5 6.7v.1c8.3 16.7 23.8 24.3 40.3 23 16.6-1.3 34.1-11 48.3-27.9 13.6-16.4 36-23.2 50.9-32.2 7.4-4.5 13.4-10.1 13.9-18.3.4-8.2-4.4-17.3-15.5-29.7zM223.7 87.3c9.8-22.2 34.2-21.8 44-.4 6.5 14.2 3.6 30.9-4.3 40.4-1.6-.8-5.9-2.6-12.6-4.9 1.1-1.2 3.1-2.7 3.9-4.6 4.8-11.8-.2-27-9.1-27.3-7.3-.5-13.9 10.8-11.8 23-4.1-2-9.4-3.5-13-4.4-1-6.9-.3-14.6 2.9-21.8zM183 75.8c10.1 0 20.8 14.2 19.1 33.5-3.5 1-7.1 2.5-10.2 4.6 1.2-8.9-3.3-20.1-9.6-19.6-8.4.7-9.8 21.2-1.8 28.1 1 .8 1.9-.2-5.9 5.5-15.6-14.6-10.5-52.1 8.4-52.1zm-13.6 60.7c6.2-4.6 13.6-10 14.1-10.5 4.7-4.4 13.5-14.2 27.9-14.2 7.1 0 15.6 2.3 25.9 8.9 6.3 4.1 11.3 4.4 22.6 9.3 8.4 3.5 13.7 9.7 10.5 18.2-2.6 7.1-11 14.4-22.7 18.1-11.1 3.6-19.8 16-38.2 14.9-3.9-.2-7-1-9.6-2.1-8-3.5-12.2-10.4-20-15-8.6-4.8-13.2-10.4-14.7-15.3-1.4-4.9 0-9 4.2-12.3zm3.3 334c-2.7 35.1-43.9 34.4-75.3 18-29.9-15.8-68.6-6.5-76.5-21.9-2.4-4.7-2.4-12.7 2.6-26.4v-.2c2.4-7.6.6-16-.6-23.9-1.2-7.8-1.8-15 .9-20 3.5-6.7 8.5-9.1 14.8-11.3 10.3-3.7 11.8-3.4 19.6-9.9 5.5-5.7 9.5-12.9 14.3-18 5.1-5.5 10-8.1 17.7-6.9 8.1 1.2 15.1 6.8 21.9 16l19.6 35.6c9.5 19.9 43.1 48.4 41 68.9zm-1.4-25.9c-4.1-6.6-9.6-13.6-14.4-19.6 7.1 0 14.2-2.2 16.7-8.9 2.3-6.2 0-14.9-7.4-24.9-13.5-18.2-38.3-32.5-38.3-32.5-13.5-8.4-21.1-18.7-24.6-29.9s-3-23.3-.3-35.2c5.2-22.9 18.6-45.2 27.2-59.2 2.3-1.7.8 3.2-8.7 20.8-8.5 16.1-24.4 53.3-2.6 82.4.6-20.7 5.5-41.8 13.8-61.5 12-27.4 37.3-74.9 39.3-112.7 1.1.8 4.6 3.2 6.2 4.1 4.6 2.7 8.1 6.7 12.6 10.3 12.4 10 28.5 9.2 42.4 1.2 6.2-3.5 11.2-7.5 15.9-9 9.9-3.1 17.8-8.6 22.3-15 7.7 30.4 25.7 74.3 37.2 95.7 6.1 11.4 18.3 35.5 23.6 64.6 3.3-.1 7 .4 10.9 1.4 13.8-35.7-11.7-74.2-23.3-84.9-4.7-4.6-4.9-6.6-2.6-6.5 12.6 11.2 29.2 33.7 35.2 59 2.8 11.6 3.3 23.7.4 35.7 16.4 6.8 35.9 17.9 30.7 34.8-2.2-.1-3.2 0-4.2 0 3.2-10.1-3.9-17.6-22.8-26.1-19.6-8.6-36-8.6-38.3 12.5-12.1 4.2-18.3 14.7-21.4 27.3-2.8 11.2-3.6 24.7-4.4 39.9-.5 7.7-3.6 18-6.8 29-32.1 22.9-76.7 32.9-114.3 7.2zm257.4-11.5c-.9 16.8-41.2 19.9-63.2 46.5-13.2 15.7-29.4 24.4-43.6 25.5s-26.5-4.8-33.7-19.3c-4.7-11.1-2.4-23.1 1.1-36.3 3.7-14.2 9.2-28.8 9.9-40.6.8-15.2 1.7-28.5 4.2-38.7 2.6-10.3 6.6-17.2 13.7-21.1.3-.2.7-.3 1-.5.8 13.2 7.3 26.6 18.8 29.5 12.6 3.3 30.7-7.5 38.4-16.3 9-.3 15.7-.9 22.6 5.1 9.9 8.5 7.1 30.3 17.1 41.6 10.6 11.6 14 19.5 13.7 24.6zM173.3 148.7c2 1.9 4.7 4.5 8 7.1 6.6 5.2 15.8 10.6 27.3 10.6 11.6 0 22.5-5.9 31.8-10.8 4.9-2.6 10.9-7 14.8-10.4s5.9-6.3 3.1-6.6-2.6 2.6-6 5.1c-4.4 3.2-9.7 7.4-13.9 9.8-7.4 4.2-19.5 10.2-29.9 10.2s-18.7-4.8-24.9-9.7c-3.1-2.5-5.7-5-7.7-6.9-1.5-1.4-1.9-4.6-4.3-4.9-1.4-.1-1.8 3.7 1.7 6.5z'}, 'gitalt': {'width': 448, 'height': 512, 'path': 'M439.55 236.05L244 40.45a28.87 28.87 0 0 0-40.81 0l-40.66 40.63 51.52 51.52c27.06-9.14 52.68 16.77 43.39 43.68l49.66 49.66c34.23-11.8 61.18 31 35.47 56.69-26.49 26.49-70.21-2.87-56-37.34L240.22 199v121.85c25.3 12.54 22.26 41.85 9.08 55a34.34 34.34 0 0 1-48.55 0c-17.57-17.6-11.07-46.91 11.25-56v-123c-20.8-8.51-24.6-30.74-18.64-45L142.57 101 8.45 235.14a28.86 28.86 0 0 0 0 40.81l195.61 195.6a28.86 28.86 0 0 0 40.8 0l194.69-194.69a28.86 28.86 0 0 0 0-40.81z'}}
SANS = "-apple-system, BlinkMacSystemFont, Segoe UI, Noto Sans CJK SC, Microsoft YaHei, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Consolas, Liberation Mono, monospace"
THEMES = {
    "dark": {"bg":"#0d1525", "bg2":"#142237", "text":"#edf3ff", "muted":"#a4b4cf", "line":"#263750", "a":"#95a8ff", "b":"#4de0c3", "dot":"#7186a5"},
    "light": {"bg":"#f4f7ff", "bg2":"#e9f4f6", "text":"#172844", "muted":"#526581", "line":"#d1dceb", "a":"#5367c9", "b":"#087f7a", "dot":"#8ca4bf"},
}

def text(x, y, content, size, color, weight=400, family=SANS, extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}" {extra}>{escape(content)}</text>'

def banner(theme: str, compact: bool = False) -> str:
    c = THEMES[theme]
    w,h=(720,410) if compact else (1200,330)
    px,py=(432,262) if compact else (888,181)
    g=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
       '<title id="title">KALEsky · 大语言模型 · 生成式推荐 · AI Agent</title>',
       '<desc id="desc">中国科学技术大学 USTC-CMI。抽象的 token 路径与向量点阵，仅为装饰，不表示实验结果。</desc>',
       f'<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="{c["bg"]}"/><stop offset="1" stop-color="{c["bg2"]}"/></linearGradient>',
       f'<linearGradient id="accent"><stop stop-color="{c["a"]}"/><stop offset="1" stop-color="{c["b"]}"/></linearGradient>',
       f'<pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0H0V34" fill="none" stroke="{c["line"]}" stroke-width="0.6" opacity="0.48"/></pattern>',
       f'<clipPath id="clip"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20"/></clipPath></defs>',
       '<style>.pulse{animation:pulse 7s ease-in-out infinite}.trail{animation:travel 24s linear infinite}@keyframes pulse{0%,100%{opacity:.42}50%{opacity:1}}@keyframes travel{to{stroke-dashoffset:-144}}@media(prefers-reduced-motion:reduce){.pulse,.trail{animation:none}}</style>',
       f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="url(#bg)" stroke="{c["line"]}"/>',
       '<g clip-path="url(#clip)">',
       f'<rect x="{w*.57}" y="0" width="{w*.43}" height="{h}" fill="url(#grid)"/>',
       f'<path d="M0 0H{w}" stroke="url(#accent)" stroke-width="5"/>']
    if compact:
        g += [text(38,49,'KALESKY / PERSONAL PROFILE',16,c['muted'],500,MONO),
              text(38,134,'KALEsky',73,c['text'],750),
              text(38,191,'大语言模型 · 生成式推荐 · AI Agent',27,c['text'],500),
              text(38,239,'探索模型，理解智能。',23,c['muted']),
              text(38,367,'USTC · CMI',19,c['a'],600,MONO)]
        scale=.65
    else:
        g += [text(52,53,'KALESKY / PERSONAL PROFILE',16,c['muted'],500,MONO),
              text(52,147,'KALEsky',83,c['text'],750),
              text(56,201,'大语言模型 · 生成式推荐 · AI Agent',27,c['text'],500),
              text(56,265,'探索模型，理解智能。',21,c['muted']),
              text(1145,51,'USTC · CMI',16,c['a'],600,MONO,'text-anchor="end"')]
        scale=1.0
    # Decorative token-space illustration: no chip, false metrics or scientific claims.
    g.append(f'<g transform="translate({px},{py}) scale({scale})">')
    for row in range(7):
        for col in range(9):
            x,y=col*24-96,row*24-70
            dist=math.hypot(x-2,y-1)
            opacity=max(.12,.60-dist/310)
            g.append(f'<circle cx="{x}" cy="{y}" r="1.7" fill="{c["dot"]}" opacity="{opacity:.2f}"/>')
    for dy,op in [(-27,.24),(0,.70),(27,.24)]:
        g.append(f'<path d="M-152 {68+dy}C-94 {68+dy},-116 {-20+dy},-46 {-20+dy}S16 {58+dy},66 {58+dy}S91 {-38+dy},175 {-38+dy}" fill="none" stroke="url(#accent)" stroke-width="1.8" opacity="{op}"/>')
    g += [f'<path class="trail" d="M-152 68C-94 68,-116 -20,-46 -20S16 58,66 58S91 -38,175 -38" fill="none" stroke="{c["b"]}" stroke-width="2.8" stroke-dasharray="7 137"/>']
    for x,y,label in [(-136,54,'x'),(-43,-20,'z'),(65,57,'y')]:
        g.append(f'<rect x="{x-15}" y="{y-15}" width="30" height="30" rx="7" fill="{c["bg"]}" stroke="{c["a"]}" stroke-opacity=".75"/>')
        g.append(text(x,y+5,label,15,c['text'],500,MONO,'text-anchor="middle"'))
    g += [f'<circle class="pulse" cx="175" cy="-38" r="6" fill="{c["b"]}"/>', '</g></g></svg>']
    return '\n'.join(g)

BADGES = [
 # id, display label, width, accent, icon type
 ('python','Python',106,'#5c9fd0','python'),
 ('pytorch','PyTorch',114,'#ff775b','torch'),
 ('hugging-face','Hugging Face',151,'#ffd45a','face'),
 ('transformers','Transformers',149,'#ffd45a','face'),
 ('cuda','CUDA',96,'#a4d954','matrix'),
 ('java','Java',85,'#f2ac66','java'),
 ('c','C',64,'#9eb9d2','letter-c'),
 ('linux','Linux',97,'#ead168','linux'),
 ('git','Git',74,'#f9856c','gitalt'),
 ('anaconda','Anaconda',116,'#44a568','letter-a'),
 ('vscode','VS Code',115,'#69b9f5','code'),
 ('claude-code','Claude Code',153,'#e5ab8f','asterisk'),
 ('codex','Codex',102,'#dce9f3','terminal'),
 ('deepseek-harness','DeepSeek Harness',188,'#94b3ff','orbit'),
]

def badge(name: str, label: str, width: int, accent: str, icon: str) -> str:
    g=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="32" viewBox="0 0 {width} 32" role="img" aria-label="{escape(label)}">',
       f'<title>{escape(label)}</title><g transform="translate(0,2)">',
       f'<rect x=".5" y=".5" width="{width-1}" height="27" rx="4" fill="#152236" stroke="#31425a"/>',
       f'<path d="M4.5 1H{width-4.5}" stroke="{accent}" stroke-width="1.5" opacity=".85"/>']
    if icon in BRANDS:
        b=BRANDS[icon];s=min(16/b['width'],17/b['height']);x=16-b['width']*s/2;y=14-b['height']*s/2
        g.append(f'<path fill="{accent}" transform="translate({x},{y}) scale({s})" d="{b["path"]}"/>')
    elif icon=='torch':
        g.append(f'<path d="M15 5L10 10A7 7 0 1 0 21 11" fill="none" stroke="{accent}" stroke-width="2.1"/><circle cx="21.7" cy="6.5" r="1.6" fill="{accent}"/>')
    elif icon=='face':
        g.append(f'<circle cx="16" cy="14" r="8" fill="{accent}"/><circle cx="13" cy="12" r="1" fill="#172844"/><circle cx="19" cy="12" r="1" fill="#172844"/><path d="M12 16Q16 20 20 16" fill="none" stroke="#172844" stroke-width="1.1" stroke-linecap="round"/>')
    elif icon=='matrix':
        for r in range(3):
            for c in range(3):
                g.append(f'<rect x="{9+c*5}" y="{7+r*5}" width="3.3" height="3.3" rx=".7" fill="{accent}"/>')
    elif icon=='letter-c':
        g.append(text(16,20,'C',18,accent,700,MONO,'text-anchor="middle"'))
    elif icon=='letter-a':
        g.append(text(16,20,'A',18,accent,700,MONO,'text-anchor="middle"'))
    elif icon in ('code','terminal'):
        if icon=='code':d='M12 8L6 14L12 20M20 8L26 14L20 20M18 6L14 22'
        else:d='M8 8L14 14L8 20M17 20H24'
        g.append(f'<path d="{d}" stroke="{accent}" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    elif icon=='asterisk':
        for a in range(0,180,30):
            g.append(f'<path d="M16 5V23" stroke="{accent}" stroke-width="1.5" transform="rotate({a} 16 14)"/>')
    elif icon=='orbit':
        g.append(f'<circle cx="16" cy="14" r="2.8" fill="{accent}"/><ellipse cx="16" cy="14" rx="10" ry="4.5" transform="rotate(-30 16 14)" fill="none" stroke="{accent}" stroke-width="1.5"/>')
    g.append(text(33,18.5,label,12.7,'#edf3ff',550))
    g.append('</g></svg>')
    return '\n'.join(g)

def main():
    ASSETS.mkdir(parents=True,exist_ok=True)
    (ASSETS/'badges').mkdir(exist_ok=True)
    for theme in THEMES:
        for compact in (False,True):
            name=f'hero-{theme}'+('-compact' if compact else '')+'.svg'
            svg=banner(theme,compact);ET.fromstring(svg)
            (ASSETS/name).write_text(svg,encoding='utf-8')
    for args in BADGES:
        svg=badge(*args);ET.fromstring(svg)
        (ASSETS/'badges'/f'{args[0]}.svg').write_text(svg,encoding='utf-8')
    print(f'Built 4 banner variants and {len(BADGES)} badges in {ASSETS}')

if __name__=='__main__':
    main()
