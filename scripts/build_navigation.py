#!/usr/bin/env python3
"""Build public-safe, outlined Goddess Veiled README navigation artwork."""
from argparse import ArgumentParser
from html import escape
from math import ceil
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

LABELS = {
    'project-tracker': 'Project tracker',
    'glitter-brain': 'Glitter Brain',
    'app-development': 'App Development',
    'research': 'Research',
    'app-tools': 'App Tools',
    'working-notes': 'Working notes',
    'dashboard': 'Dashboard',
    'experiments': 'Experiments',
    'start-here': 'Start here',
    'shared-documentation': 'Documentation',
    'current-structure': 'Structure',
    'using-the-board': 'Board guide',
    'about-the-lab': 'About the Lab',
    'research-and-findings': 'Research & findings',
    'working-here': 'Working here',
    'collection-homes': 'Collection homes',
    'roleplay-library': 'Roleplay library',
    'status': 'Status',
}


def lettering(font, label, size, x, y, color):
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    scale = size / font['head'].unitsPerEm
    parts = [f'<g fill="{color}" aria-label="{escape(label, quote=True)}">']
    for char in label:
        name = cmap[ord(char)]
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        if pen.getCommands():
            parts.append(f'<path d="{pen.getCommands()}" transform="translate({x:.3f} {y}) scale({scale:.7f} {-scale:.7f})"/>')
        x += font['hmtx'][name][0] * scale
    return ''.join(parts) + '</g>'


def make_badge(font, label, top=False):
    size, height = (11, 24) if top else (14, 38)
    cmap = font.getBestCmap()
    text_width = sum(font['hmtx'][cmap[ord(char)]][0] for char in label) * size / font['head'].unitsPerEm
    width = ceil(text_width) + (33 if top else 42)
    radius, y = (10, 16) if top else (15, 24)
    description = 'Return to the top of this README.' if top else f'Jump to {label} on this page.'
    icon = '<path d="m10 13 4-4 4 4m-4-4v9" stroke="#d4af6a" stroke-width="1.3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' if top else '<path d="M12 15v8" stroke="#ff2e88" stroke-width="2" stroke-linecap="round"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape('Back to top' if top else label)}</title><desc id="desc">{escape(description)}</desc>
<defs>
<linearGradient id="base" x2="1" y2="1"><stop stop-color="#29222f"/><stop offset=".62" stop-color="#17131e"/><stop offset="1" stop-color="#211520"/></linearGradient>
<linearGradient id="edge" x2="1" y2="1"><stop stop-color="#d4af6a" stop-opacity=".32"/><stop offset=".5" stop-color="#fff" stop-opacity=".1"/><stop offset="1" stop-color="#ff2e88" stop-opacity=".35"/></linearGradient>
<linearGradient id="sheen" x2="0" y2="1"><stop stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>
<rect x="1" y="3" width="{width - 2}" height="{height - 4}" rx="{radius}" fill="#000" opacity=".22"/>
<rect x="1" y="1" width="{width - 2}" height="{height - 4}" rx="{radius}" fill="url(#base)" stroke="url(#edge)"/>
<rect x="2" y="2" width="{width - 4}" height="{height - 6}" rx="{radius - 1}" fill="url(#sheen)"/>
{icon}
{lettering(font, label, size, 24 if top else 22, y, '#d4af6a' if top else '#f2eff5')}
</svg>
'''


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--font', type=Path, required=True, help='Outfit variable font (TTF or WOFF2)')
    args = parser.parse_args()
    font = instantiateVariableFont(TTFont(args.font), {'wght': 500}, inplace=False)
    output = Path(__file__).resolve().parents[1] / 'assets' / 'nav'
    output.mkdir(parents=True, exist_ok=True)
    for slug, label in LABELS.items():
        (output / f'{slug}.svg').write_text(make_badge(font, label))
    (output / 'back-to-top.svg').write_text(make_badge(font, 'Top', top=True))
    print(f'Built {len(LABELS) + 1} navigation assets in {output}')


if __name__ == '__main__':
    main()
