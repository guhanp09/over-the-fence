"""Tiny SVG drawing kit for the book's illustrations."""
import math, base64, io
import numpy as np

C = dict(ink='#1f1d36', paper='#fffdf8', coral='#ff5b3a', sun='#ffbf2f', teal='#0fa38f',
         blue='#3a66f0', violet='#7c4dff', pink='#ff4d8d', grey='#a19fb3', mist='#ebe9f2',
         coralT='#ffe4dc', blueT='#e4ebff', tealT='#d8f4ee', sunT='#fff1cc', violetT='#ece5ff',
         night='#16143a', night2='#26225e', soft='#6b6884')
SANS = "'Avenir Next', Avenir, 'Helvetica Neue', sans-serif"
HAND = "Noteworthy, 'Bradley Hand', cursive"
SERIF = "Charter, 'Iowan Old Style', Georgia, serif"
_uid = [0]


def uid(p='g'):
    _uid[0] += 1
    return f'{p}{_uid[0]}'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class Fig:
    def __init__(self, w, h, bg=None, rx=0):
        self.w, self.h = w, h
        self.parts, self.defs = [], []
        if bg:
            self.rect(0, 0, w, h, fill=bg, rx=rx)

    def raw(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill='none', stroke='none', sw=1, rx=0, op=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.raw(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"{d}/>')

    def poly(self, pts, stroke=C['ink'], sw=2, fill='none', dash=None, op=1, close=False,
             filt=None, fop=None):
        pts = list(pts)
        if len(pts) < 2:
            return
        d = 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in pts) + (' Z' if close else '')
        extra = f' stroke-dasharray="{dash}"' if dash else ''
        if filt:
            extra += f' filter="url(#{filt})"'
        if fop is not None:
            extra += f' fill-opacity="{fop}"'
        self.raw(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
                 f'stroke-linecap="round" stroke-linejoin="round" opacity="{op}"{extra}/>')

    def line(self, x1, y1, x2, y2, **k):
        self.poly([(x1, y1), (x2, y2)], **k)

    def circle(self, cx, cy, r, stroke=C['ink'], sw=1.5, fill='none', op=1, dash=None, filt=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        if filt:
            d += f' filter="url(#{filt})"'
        self.raw(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" stroke="{stroke}" '
                 f'stroke-width="{sw}" opacity="{op}"{d}/>')

    def dot(self, cx, cy, r=4, color=C['ink'], op=1):
        self.circle(cx, cy, r, stroke='none', fill=color, op=op)

    def arrow(self, x1, y1, x2, y2, color=C['ink'], sw=2.2, head=9, bend=0.0, dash=None, op=1):
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        cx, cy = (x1 + x2) / 2 - dy * bend, (y1 + y2) / 2 + dx * bend
        ex, ey = x2 - cx, y2 - cy
        el = math.hypot(ex, ey) or 1
        ux, uy = ex / el, ey / el
        bx, by = x2 - ux * head * 0.75, y2 - uy * head * 0.75
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.raw(f'<path d="M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {bx:.1f},{by:.1f}" fill="none" '
                 f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" opacity="{op}"{d}/>')
        px, py = -uy, ux
        hx, hy = x2 - ux * head, y2 - uy * head
        pts = [(x2, y2), (hx + px * head * 0.52, hy + py * head * 0.52), (hx - px * head * 0.52, hy - py * head * 0.52)]
        self.raw('<path d="M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts) +
                 f' Z" fill="{color}" opacity="{op}"/>')

    def text(self, x, y, s, size=14, color=C['ink'], anchor='start', font='sans', weight=500,
             italic=False, op=1, rotate=0, lh=1.25):
        fam = {'sans': SANS, 'hand': HAND, 'serif': SERIF}[font]
        st = ' font-style="italic"' if italic else ''
        tr = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate else ''
        lines = s.split('\n')
        if len(lines) == 1:
            body = esc(s)
        else:
            body = ''.join(f'<tspan x="{x:.1f}" dy="{0 if i == 0 else size * lh:.1f}">{esc(t)}</tspan>'
                           for i, t in enumerate(lines))
        self.raw(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
                 f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}" opacity="{op}"{st}{tr}>{body}</text>')

    def hand(self, x, y, s, size=16, color=C['coral'], anchor='start', rotate=0, weight=400, op=1):
        self.text(x, y, s, size=size, color=color, anchor=anchor, font='hand', weight=weight,
                  rotate=rotate, op=op)

    def label(self, x, y, s, size=11, color=C['soft'], anchor='start', weight=600):
        self.text(x, y, s.upper(), size=size, color=color, anchor=anchor, weight=weight)

    def glow(self, std=3.0):
        i = uid('glow')
        self.defs.append(f'<filter id="{i}" x="-20%" y="-20%" width="140%" height="140%">'
                         f'<feGaussianBlur stdDeviation="{std}" result="b"/><feMerge>'
                         f'<feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
        return i

    def image(self, x, y, w, h, png):
        b = base64.b64encode(png).decode()
        self.raw(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" '
                 f'href="data:image/png;base64,{b}"/>')

    def svg(self):
        defs = f'<defs>{"".join(self.defs)}</defs>' if self.defs else ''
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'class="ill">{defs}{"".join(self.parts)}</svg>')


def mapper(x0, x1, y0, y1, px, py, pw, ph):
    """Map data coords to pixels in the box (px, py, pw, ph); y grows upward."""
    def f(x, y):
        return px + (x - x0) / (x1 - x0) * pw, py + ph - (y - y0) / (y1 - y0) * ph
    return f


def curve(f, xs, ys):
    return [f(x, y) for x, y in zip(xs, ys)]


def signed_fill(fig, m, xs, ys, pos=C['coral'], neg=C['blue'], op=0.28):
    """Shade area between a curve and y=0: positive in one colour, negative in another."""
    for sign, col in ((1, pos), (-1, neg)):
        yy = np.where(sign * ys > 0, ys, 0.0)
        pts = [m(xs[0], 0)] + curve(m, xs, yy) + [m(xs[-1], 0)]
        fig.poly(pts, stroke='none', fill=col, op=op, close=True)


def png_from_array(rgb):
    from PIL import Image
    arr = np.clip(rgb * 255, 0, 255).astype(np.uint8)
    buf = io.BytesIO()
    Image.fromarray(arr).save(buf, format='PNG')
    return buf.getvalue()


def hex2rgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def ramp(vals, stops):
    """Colour-map values in [0,1] through a list of hex colours."""
    cols = np.array([hex2rgb(s) for s in stops])
    pos = np.linspace(0, 1, len(stops))
    v = np.clip(vals, 0, 1)
    out = np.zeros(v.shape + (3,))
    for k in range(3):
        out[..., k] = np.interp(v, pos, cols[:, k])
    return out


def wavelength_rgb(wl):
    """Approximate display colour of a pure wavelength (nm)."""
    if wl < 440:
        r, g, b = -(wl - 440) / 60, 0, 1
    elif wl < 490:
        r, g, b = 0, (wl - 440) / 50, 1
    elif wl < 510:
        r, g, b = 0, 1, -(wl - 510) / 20
    elif wl < 580:
        r, g, b = (wl - 510) / 70, 1, 0
    elif wl < 645:
        r, g, b = 1, -(wl - 645) / 65, 0
    else:
        r, g, b = 1, 0, 0
    f = 0.3 + 0.7 * (wl - 380) / 40 if wl < 420 else (0.3 + 0.7 * (750 - wl) / 50 if wl > 700 else 1)
    return '#%02x%02x%02x' % tuple(int(255 * (c * f) ** 0.8) for c in (r, g, b))
