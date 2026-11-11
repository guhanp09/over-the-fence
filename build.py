"""Assemble Over the Fence (Chapters 1-2) into HTML, then print to PDF with Chrome."""
import html, json, os, re, subprocess, sys
from pathlib import Path
import figs1, figs2, figs3, figs4, figs5, figs67
from svgkit import C

ROOT = Path(__file__).parent
OUT = ROOT / 'build'
FIGS = {**figs1.FIGS1, **figs2.FIGS2, **figs3.FIGS3, **figs4.FIGS4, **figs5.FIGS5, **figs67.FIGS67}
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

CHAPTERS = [
    dict(n=1, title='Fourier series', tag='Every repeating thing is a sum of circles',
         hook='How do you build a song out of circles?', acc=C['coral'], tint=C['coralT'],
         files=['1_1', '1_2', '1_3', '1_4'], hero=lambda: figs1.hero_flower(640, 420)),
    dict(n=2, title='Vector spaces', tag='Anything you can add and scale',
         hook='What do a biryani, a rainbow and a pop song have in common?', acc=C['teal'], tint=C['tealT'],
         files=['2_1', '2_2', '2_3'], hero=lambda: figs2.hero_grid(640, 400)),
    dict(n=3, title='Metric', tag='What \u201cdistance\u201d really means',
         hook='How far apart are two songs?', acc=C['blue'], tint=C['blueT'],
         files=['3_1', '3_2', '3_3'], hero=figs3.hero),
    dict(n=4, title='Eigenvalues and eigenvectors', tag='Every change has a grain',
         hook='What do pizza dough, Google and a wobbly bridge have in common?', acc=C['violet'], tint=C['violetT'],
         files=['4_1', '4_2', '4_3'], hero=figs4.hero),
    dict(n=5, title='Groups', tag='The grammar of moves',
         hook='Why can\u2019t one flip turn your mattress through every position?', acc='#ff4d8d', tint='#ffe3ee',
         files=['5_1', '5_2', '5_3'], hero=figs5.hero),
    dict(n=6, title='Bayes\u2019 theorem', tag='How much should evidence change your mind?',
         hook='Why does nobody run to the window when a car alarm goes off?', acc='#e09a00', tint='#fff1cc',
         files=['6_1', '6_2', '6_3'], hero=figs67.hero6),
    dict(n=7, title='Regression to the mean', tag='Extremes are partly luck',
         hook='Why does yelling at a team seem to work?', acc='#1f9d55', tint='#dcf5e5',
         files=['7_1', '7_2'], hero=figs67.hero7),
]

ICONS = {
    'pause': '<svg viewBox="0 0 24 24"><path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="3.2" fill="currentColor"/></svg>',
    'try': '<svg viewBox="0 0 24 24"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    'side': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15.5 8.5l-2 5-5 2 2-5z" fill="currentColor"/></svg>',
    'key': '<svg viewBox="0 0 24 24"><circle cx="8" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M12 12h9M18 12v3.5M15 12v2.5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
    'clock': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    'book': '<svg viewBox="0 0 24 24"><path d="M4 5c3-1 6-1 8 1 2-2 5-2 8-1v14c-3-1-6-1-8 1-2-2-5-2-8-1z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
}


def smart(s):
    s = re.sub(r'(^|[\s(\[\u2014\u2013/-])"', '\\1\u201c', s)
    s = s.replace('"', '\u201d')
    s = re.sub(r"(^|[\s(\[\u2014\u2013/-])'", '\\1\u2018', s)
    return s.replace("'", '\u2019')


def fmt(s, dialogue=False):
    if dialogue:
        s = re.sub(r'"([^"]*)"', "\u2018\\1\u2019", s)
    s = html.escape(s, quote=False)
    s = smart(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'==(.+?)==', r'<mark>\1</mark>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
    s = s.replace(' -- ', ' \u2013 ')
    return s


def words(text):
    return len(re.sub(r'@\w+|[|=`*]', ' ', text).split())


class Book:
    def __init__(self):
        self.figno = {}
        self.toc = []

    def figure(self, ch, key, cap):
        self.figno[ch] = self.figno.get(ch, 0) + 1
        n = f'{ch}.{self.figno[ch]}'
        return (f'<figure class="fig"><div class="art">{FIGS[key]()}</div>'
                f'<figcaption><b>Figure {n}</b>{fmt(cap)}</figcaption></figure>')

    def section(self, ch, fname, idx, total):
        text = (ROOT / 'content' / f'{fname}.txt').read_text()
        mins = max(1, round(words(text) / 210))
        out = []
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith('J: '):
                out.append(f'<p class="j">\u201c{fmt(line[3:], True)}\u201d</p>')
                continue
            if line.startswith('N: '):
                out.append(f'<p class="n">\u201c{fmt(line[3:], True)}\u201d</p>')
                continue
            if not line.startswith('@'):
                out.append(f'<p>{fmt(line)}</p>')
                continue
            cmd, _, rest = line.partition(' ')
            parts = [p.strip() for p in rest.split('|')]
            if cmd == '@section':
                num, title, official, promise = parts
                sid = 's' + num.replace('.', '-')
                self.toc.append(dict(ch=ch['n'], num=num, title=title, official=official, id=sid, mins=mins))
                dots = ''.join(f'<i class="{"on" if k == idx else ("done" if k < idx else "")}"></i>' for k in range(total))
                out.append(f'''<section class="sec-head" id="{sid}">
<span class="marker">@@{sid}@@</span>
<div class="kicker">Chapter {ch["n"]} \u00b7 Part {idx + 1} of {total} <span class="dots">{dots}</span></div>
<div class="bignum">{num}</div>
<h2>{fmt(title)}</h2>
<div class="official">{fmt(official)}</div>
<div class="promise"><span class="pl">By the end</span>{fmt(promise)}</div>
<div class="meta"><span>{ICONS["clock"]} {mins} min read</span><span>{ICONS["book"]} A conversation over the fence</span></div>
</section>''')
            elif cmd == '@scene':
                out.append(f'<div class="scene"><span>Scene</span>{fmt(rest)}</div>')
            elif cmd == '@beat':
                out.append(f'<p class="beat">{fmt(rest)}</p>')
            elif cmd == '@fig':
                out.append(self.figure(ch['n'], parts[0], parts[1]))
            elif cmd == '@pause':
                out.append(f'<div class="box pause"><div class="bt">{ICONS["pause"]} Pause and picture it</div><p>{fmt(rest)}</p></div>')
            elif cmd == '@try':
                out.append(f'<div class="box try"><div class="bt">{ICONS["try"]} Try this: {fmt(parts[0])}</div><p>{fmt(parts[1])}</p></div>')
            elif cmd == '@side':
                out.append(f'<div class="box side"><div class="bt">{ICONS["side"]} Side quest: {fmt(parts[0])}</div><p>{fmt(parts[1])}</p></div>')
            elif cmd == '@note':
                out.append(f'<aside class="note">{fmt(rest)}</aside>')
            elif cmd == '@name':
                out.append(f'<div class="nametag"><div class="nt-top"><b>HELLO</b><span>my name is</span></div>'
                           f'<div class="nt-name">{fmt(parts[0])}</div><div class="nt-def">{fmt(parts[1])}</div></div>')
            elif cmd == '@quote':
                out.append(f'<blockquote class="pull">{fmt(rest)}<cite>Jim, figuring it out</cite></blockquote>')
            elif cmd == '@formula':
                lab, txt = (parts[0], parts[1]) if len(parts) > 1 else ('In words', parts[0])
                out.append(f'<div class="formula"><div class="fl">{fmt(lab)}</div>{fmt(txt)}</div>')
            elif cmd == '@textbook':
                out.append(f'<div class="textbook"><div class="tl">In textbook language (for the curious)</div>{fmt(rest)}</div>')
            elif cmd == '@unlock':
                out.append(f'<div class="unlock"><div class="uk">{ICONS["key"]}</div><div><div class="ul">Tool unlocked</div>'
                           f'<div class="un">{fmt(parts[0])}</div><p>{fmt(parts[1])}</p></div></div>')
            else:
                raise ValueError(line)
        return '\n'.join(out)

    def opener(self, ch, secs):
        hero = ch['hero']()
        stops = ''.join(f'<li><span class="stop">{s["num"]}</span><div><b>{fmt(s["title"])}</b>'
                        f'<em>{fmt(s["official"])}</em></div></li>' for s in secs)
        return f'''<section class="opener" id="ch{ch["n"]}">
<span class="marker">@@ch{ch["n"]}@@</span>
<div class="op-kicker">Chapter</div><div class="op-num">{ch["n"]}</div>
<h1>{fmt(ch["title"])}</h1><div class="op-tag">{fmt(ch["tag"])}</div>
<div class="op-hero">{hero}</div>
<div class="op-hook">{fmt(ch["hook"])}</div>
<div class="route"><div class="rl">Your route through this chapter</div><ol>{stops}</ol></div>
</section>'''

    def build(self, pages=None):
        body = []
        for ch in CHAPTERS:
            start = len(self.toc)
            secs_html = [self.section(ch, f, i, len(ch['files'])) for i, f in enumerate(ch['files'])]
            secs = self.toc[start:]
            body.append(f'<div class="chapter" style="--acc:{ch["acc"]};--tint:{ch["tint"]}">'
                        + self.opener(ch, secs) + ''.join(f'<div class="sec">{s}</div>' for s in secs_html) + '</div>')
        pages = pages or {}
        toc_rows = []
        for ch in CHAPTERS:
            toc_rows.append(f'<div class="toc-ch" style="--acc:{ch["acc"]}"><span>Chapter {ch["n"]}</span>'
                            f'<b>{fmt(ch["title"])}</b><i>{pages.get("ch%d" % ch["n"], "")}</i></div>')
            for s in [t for t in self.toc if t['ch'] == ch['n']]:
                toc_rows.append(f'<div class="toc-s" style="--acc:{ch["acc"]}"><span>{s["num"]}</span><b>{fmt(s["title"])}'
                                f'<em>{fmt(s["official"])} \u00b7 {s["mins"]} min</em></b><i>{pages.get(s["id"], "")}</i></div>')
        chs = ''.join(f'<div><span style="color:{c["acc"]}">Chapter {c["n"]}</span>{fmt(c["title"])}</div>' for c in CHAPTERS)
        front = FRONT.replace('{{CHS}}', chs).replace('{{TOC}}', ''.join(toc_rows)).replace('{{HERO}}', figs1.hero_note(640, 560, K=80))
        css = (ROOT / 'style.css').read_text()
        return f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Over the Fence</title><style>{css}</style></head><body>{front}{"".join(body)}{BACK}</body></html>'


FRONT = '''<section class="cover">
<div class="cv-top">Over the Fence</div>
<div class="cv-sub">Big ideas in mathematics, one neighbourly conversation at a time</div>
<div class="cv-hero">{{HERO}}</div>
<div class="cv-chs">{{CHS}}</div>
<div class="cv-author">
<div><div class="cv-name">Guhan Purushothaman</div>
<div class="cv-cred">M.Sc. Mathematics <i>\u00b7</i> <b>IIT Madras</b></div></div>
<div class="cv-blog">from the blog<br>guhanpurushothaman.wordpress.com</div>
</div>
</section>
<section class="front">
<div class="kicker plain">Before we start</div>
<h2 class="fh">How to read this</h2>
<p class="lede">This isn\u2019t a textbook. It\u2019s a season of conversations between two neighbours, one of whom can\u2019t stop explaining things. You don\u2019t need any maths beyond school. You just need to be willing to picture things.</p>
<div class="cast">
<div class="card"><div class="av me">Me</div><b>Me, Guhan: the narrator</b><p>Your neighbour. A mathematician from IIT Madras who owns an old analogue watch, an expensive robot and far too many analogies. My lines are set in plain type.</p></div>
<div class="card"><div class="av jim">J</div><b>Jim</b><p>Asks the questions you\u2019re too polite to ask. Rents superbikes. Makes the big leaps himself. His lines sit in the blue bubbles.</p></div>
<div class="card"><div class="av dog">B</div><b>Bruno</b><p>Jim\u2019s German Shepherd. Scared of the vacuum cleaner. Has opinions during voice notes.</p></div>
<div class="card"><div class="av bot">R</div><b>The robot</b><p>Imported from Germany. Memorises everything and understands nothing. A warning to us all.</p></div>
</div>
<h3 class="fh3">Signposts along the way</h3>
<div class="legend">
<div><span class="lg pause"></span><b>Pause and picture it</b>Stop reading and imagine it first. It\u2019s where the learning happens.</div>
<div><span class="lg try"></span><b>Try this</b>Something to do with your hands, a guitar or a phone.</div>
<div><span class="lg side"></span><b>Side quest</b>A detour worth taking: history, surprises, trivia.</div>
<div><span class="lg name"></span><b>Hello, my name is</b>Names arrive <i>after</i> the ideas. When you see one of these, you\u2019ve earned it.</div>
<div><span class="lg unlock"></span><b>Tool unlocked</b>The mental model you walk away with at the end of each part.</div>
<div><span class="lg note"></span><b>Scribbles in the margin</b>Small asides you can skip, or not.</div>
</div>
<p class="rule">One rule runs through the whole book: <mark>no formula appears until you\u2019ve already understood what it says.</mark></p>
</section>
<section class="front toc">
<div class="kicker plain">The route</div>
<h2 class="fh">What\u2019s inside</h2>
{{TOC}}
</section>'''

BACK = '''<section class="back">
<div class="bk-kick">Your toolkit</div>
<div class="bk-big">Seven mental models</div>
<ol class="kit">
<li><b>Every repeating thing is circles.</b> Find the hands with a resonance test.</li>
<li><b>A vector is anything you can add and scale.</b> Pick the language where it\u2019s simple.</li>
<li><b>Distance is a choice.</b> Even \u201cgetting closer\u201d depends on the ruler.</li>
<li><b>Every change has a grain.</b> The future belongs to the biggest eigenvalue.</li>
<li><b>Moves have a grammar.</b> Structure tells you what\u2019s impossible.</li>
<li><b>Evidence multiplies odds.</b> Never flip the \u201cif\u201d.</li>
<li><b>Extremes are partly luck.</b> Check for a control group before crediting a cause.</li>
</ol>
<p>\u201cBruno forgives everyone. That\u2019s his mental model.\u201d</p>
<div class="bk-sign"><div class="bk-name">Guhan Purushothaman</div>
<div class="bk-cred">M.Sc. Mathematics \u00b7 Indian Institute of Technology Madras</div>
<div class="bk-url">More conversations at guhanpurushothaman.wordpress.com</div></div>
</section>'''


def render(html_path, pdf_path):
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--generate-pdf-document-outline',
                    '--virtual-time-budget=8000', f'--print-to-pdf={pdf_path}', html_path.as_uri()],
                   check=True, capture_output=True)


def page_map(pdf):
    d = OUT / 'txt'
    d.mkdir(exist_ok=True)
    for f in d.glob('*.txt'):
        f.unlink()
    subprocess.run(['gs', '-q', '-dNOPAUSE', '-dBATCH', '-sDEVICE=txtwrite', f'-sOutputFile={d}/p%03d.txt', str(pdf)], check=True)
    found = {}
    for f in sorted(d.glob('p*.txt')):
        pg = int(f.stem[1:])
        for m in re.findall(r'@@([\w-]+)@@', f.read_text(errors='ignore')):
            found.setdefault(m, pg)
    return found


def set_info(pdf):
    """Rewrite the PDF's info dictionary in place (same byte length, so the xref stays valid)."""
    d = bytearray(pdf.read_bytes())
    m = re.search(rb'1 0 obj\n(<<.*?>>)\nendobj', d, re.S)
    old = m.group(1)
    dates = b''.join(re.findall(rb'/(?:CreationDate|ModDate) \([^)]*\)\n?', old))
    new = (b'<</Title (Over the Fence)\n/Author (Guhan Purushothaman)\n'
           b'/Subject (Big ideas in mathematics, one neighbourly conversation at a time)\n'
           b'/Creator (Guhan Purushothaman)\n/Producer (Skia/PDF)\n' + dates)
    assert len(new) + 2 <= len(old), 'info dict grew'
    new = new + b' ' * (len(old) - len(new) - 2) + b'>>'
    d[m.start(1):m.end(1)] = new
    pdf.write_bytes(bytes(d))


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    hp, pdf = OUT / 'book.html', OUT / 'book.pdf'
    hp.write_text(Book().build())
    render(hp, pdf)
    pages = page_map(pdf)
    print('pages', pages)
    hp.write_text(re.sub(r'<span class="marker">@@[\w-]+@@</span>', '', Book().build(pages)))
    render(hp, pdf)
    final = ROOT / 'Over-the-Fence.pdf'
    final.write_bytes(pdf.read_bytes())
    set_info(final)
    print('wrote', final, os.path.getsize(final) // 1024, 'KB')
