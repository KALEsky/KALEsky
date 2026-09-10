#!/usr/bin/env python3
"""Validate local README links and SVG safety. No network access needed."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
class Reader(HTMLParser):
    def __init__(self):
        super().__init__(); self.paths=[]; self.anchors=set(); self.targets=[]; self.errors=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in {'script','style','iframe','object','embed','svg'}:
            self.errors.append(f'Unsupported README tag: {tag}')
        for k in a:
            if k.startswith('on') or k in {'style','class'}:self.errors.append(f'Unsupported attribute: {k}')
        if tag=='img' and not a.get('alt'):self.errors.append('An image is missing alt text')
        for k in ('src','srcset'):
            if k in a:self.paths.append(a[k])
        if tag=='a':
            if 'name' in a:self.anchors.add(a['name'])
            if a.get('href','').startswith('#'):self.targets.append(a['href'][1:])

def main():
    r=Reader();r.feed((ROOT/'README.md').read_text(encoding='utf-8'))
    errors=r.errors[:]
    for p in r.paths:
        if urlsplit(p).scheme:errors.append(f'External image dependency: {p}');continue
        path=(ROOT/unquote(p)).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():errors.append(f'Missing image: {p}')
    for t in r.targets:
        if t not in r.anchors:errors.append(f'Missing anchor: {t}')
    for path in (ROOT/'assets').rglob('*.svg'):
        e=ET.parse(path).getroot()
        for n in e.iter():
            tag=n.tag.rsplit('}',1)[-1]
            if tag in {'script','foreignObject','image','iframe'}:errors.append(f'Unexpected SVG element {tag}: {path}')
            if any(k.rsplit('}',1)[-1].startswith('on') for k in n.attrib):errors.append(f'SVG event handler: {path}')
            if any(k.rsplit('}',1)[-1]=='href' and not v.startswith('#') for k,v in n.attrib.items()):errors.append(f'External SVG reference: {path}')
    for term in ['哈尔滨工业大学','工学学士','中国科学技术大学','专业硕士','张勇东','生成式推荐']:
        if term not in (ROOT/'README.md').read_text(encoding='utf-8'):errors.append(f'Missing profile field: {term}')
    if errors:raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(r.paths)} local image references, {len(r.targets)} navigation anchors, SVG safety and core profile fields.')

if __name__=='__main__':main()
