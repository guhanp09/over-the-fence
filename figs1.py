"""Chapter 1 illustrations: circles, waves, resonance."""
import math
import numpy as np
from svgkit import Fig, C, mapper, curve, signed_fill, png_from_array, ramp

TAU = 2 * math.pi


# ---------- shared: epicycles for a musical note ----------
def note_coeffs(n=1024):
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    tp = TextPath((0, 0), '♪', size=100, prop=FontProperties(family='DejaVu Sans'))
    poly = max(tp.to_polygons(), key=len)
    p = np.vstack([poly, poly[:1]])
    seg = np.hypot(*np.diff(p, axis=0).T)
    s = np.concatenate([[0], np.cumsum(seg)])
    t = np.linspace(0, s[-1], n, endpoint=False)
    z = np.interp(t, s, p[:, 0]) + 1j * np.interp(t, s, p[:, 1])
    z = z - z.mean()
    z = z / np.abs(z).max()
    c = np.fft.fft(z) / n
    k = np.fft.fftfreq(n, 1 / n).astype(int)
    order = np.argsort(-np.abs(c))
    return z, c[order], k[order]


_NOTE = None


def note():
    global _NOTE
    if _NOTE is None:
        _NOTE = note_coeffs()
    return _NOTE


def partial(c, k, K, t):
    return (c[:K, None] * np.exp(1j * np.outer(k[:K], t))).sum(0)


def draw_chain(fig, c, k, K, t0, cx, cy, sc, circ=C['grey'], hand=C['ink'], op=0.6, sw=1.2):
    pos = 0j
    for i in range(K):
        nxt = pos + c[i] * np.exp(1j * k[i] * t0)
        r = abs(c[i]) * sc
        if r > 1.2:
            fig.circle(cx + pos.real * sc, cy - pos.imag * sc, r, stroke=circ, sw=0.8, op=op)
        fig.line(cx + pos.real * sc, cy - pos.imag * sc, cx + nxt.real * sc, cy - nxt.imag * sc,
                 stroke=hand, sw=sw, op=min(1, op + 0.3))
        pos = nxt
    return cx + pos.real * sc, cy - pos.imag * sc


def hero_note(w=640, h=560, K=60):
    f = Fig(w, h)
    g = f.glow(4)
    z, c, k = note()
    t = np.linspace(0, TAU, 1400)
    cx, cy, sc = w / 2, h / 2 + 10, 230
    zz = partial(c, k, K, t)
    f.poly([(cx + a.real * sc, cy - a.imag * sc) for a in zz], stroke=C['sun'], sw=3.2, filt=g)
    t0 = 2.2
    zz0 = partial(c, k, K, np.linspace(0, t0, 500))
    f.poly([(cx + a.real * sc, cy - a.imag * sc) for a in zz0], stroke=C['coral'], sw=4, filt=g)
    ex, ey = draw_chain(f, c, k, K, t0, cx, cy, sc, circ='#8f8ad8', hand='#ffffff', op=0.55, sw=1.3)
    f.circle(ex, ey, 6, stroke='none', fill=C['coral'], filt=g)
    return f.svg()


def hero_flower(w=640, h=420):
    f = Fig(w, h)
    g = f.glow(4)
    t = np.linspace(0, TAU, 3000)
    hands = [(1, 1), (0.5, -6), (0.22, 15)]
    z = sum(r * np.exp(1j * k * t) for r, k in hands)
    cx, cy, sc = w / 2, h / 2, 118
    f.poly([(cx + a.real * sc, cy - a.imag * sc) for a in z], stroke=C['sun'], sw=2.6, filt=g)
    t0 = 0.9
    pos = 0j
    for r, k in hands:
        nxt = pos + r * np.exp(1j * k * t0)
        f.circle(cx + pos.real * sc, cy - pos.imag * sc, r * sc, stroke='#8f8ad8', sw=1, op=0.6)
        f.line(cx + pos.real * sc, cy - pos.imag * sc, cx + nxt.real * sc, cy - nxt.imag * sc, stroke='#ffffff', sw=2.2)
        pos = nxt
    f.circle(cx + pos.real * sc, cy - pos.imag * sc, 7, stroke='none', fill=C['coral'], filt=g)
    return f.svg()


# ---------- 1.1 ----------
def fig_watch():
    f = Fig(640, 290)
    cx, cy, R = 150, 145, 118
    f.circle(cx, cy, R + 8, stroke=C['ink'], sw=7, fill='#ffffff')
    for i in range(60):
        a = TAU * i / 60
        r1 = R - (14 if i % 5 == 0 else 6)
        f.line(cx + R * math.sin(a), cy - R * math.cos(a), cx + r1 * math.sin(a), cy - r1 * math.cos(a),
               stroke=C['ink'], sw=2.4 if i % 5 == 0 else 1)
    a1 = math.radians(62)
    tx, ty = cx + 84 * math.sin(a1), cy - 84 * math.cos(a1)
    f.line(cx, cy, tx, ty, stroke=C['ink'], sw=6)
    a2 = math.radians(-35)
    px, py = tx + 38 * math.sin(a2), ty - 38 * math.cos(a2)
    f.circle(tx, ty, 38, stroke=C['coral'], sw=1.2, dash='3 4', op=0.8)
    f.line(tx, ty, px, py, stroke=C['coral'], sw=4)
    f.dot(tx, ty, 4.5, C['ink'])
    f.dot(cx, cy, 6, C['ink'])
    f.dot(px, py, 6, C['coral'])
    f.hand(262, 40, 'the second hand, bolted\nonto the tip of the minute hand', 15)
    f.arrow(262, 72, px + 8, py - 4, color=C['coral'], sw=1.6, bend=-0.25)
    f.hand(px - 12, py - 12, 'pen', 14, C['coral'], anchor='end')
    # the trace
    ox, oy, s = 490, 150, 92
    t = np.linspace(0, TAU, 1500)
    z = np.exp(1j * t) + 0.3 * np.exp(1j * 8 * t)
    f.circle(ox, oy, s, stroke=C['grey'], sw=1, dash='4 5')
    f.poly([(ox + a.real * s, oy - a.imag * s) for a in z], stroke=C['coral'], sw=2.4)
    f.hand(490, 280, 'what the pen draws: a flower', 16, C['ink'], anchor='middle')
    return f.svg()


def fig_twohands():
    f = Fig(640, 215)
    cases = [((1, 1), (0.28, 7)), ((1, 1), (0.33, -5)), ((1, 1), (0.8, 3)), ((1, 1), (0.5, -4), (0.22, 11))]
    labels = ['short & fast', 'spinning backwards', 'long & fast', 'three hands']
    notes = ['petals', 'a star', 'loops through the middle', 'a crown']
    t = np.linspace(0, TAU, 1600)
    for i, (case, lab, nt) in enumerate(zip(cases, labels, notes)):
        cx, cy, s = 80 + i * 160, 92, 50
        z = sum(r * np.exp(1j * kk * t) for r, kk in case)
        m = np.abs(z).max()
        f.circle(cx, cy, 72, stroke='none', fill=C['coralT'] if i % 2 == 0 else C['sunT'])
        f.poly([(cx + a.real / m * 62, cy - a.imag / m * 62) for a in z], stroke=C['coral'] if i != 3 else C['violet'], sw=2)
        f.text(cx, 190, lab, 13, C['ink'], 'middle', weight=700)
        f.hand(cx, 208, nt, 13, C['soft'], 'middle')
    return f.svg()


def fig_treasure():
    f = Fig(640, 270)
    f.rect(20, 10, 600, 250, fill='#f3f7ec', rx=18)
    for x in range(40, 620, 30):
        f.line(x, 14, x, 256, stroke='#dfe8d2', sw=1)
    for y in range(20, 260, 30):
        f.line(24, y, 616, y, stroke='#dfe8d2', sw=1)
    sx, sy = 110, 225
    ax, ay = sx + 170, sy - 170
    bx, by = ax, ay + 105
    f.arrow(sx, sy, ax, ay, color=C['blue'], sw=4, head=13)
    f.arrow(ax, ay, bx, by, color=C['teal'], sw=4, head=13)
    f.arrow(sx, sy, bx - 4, by + 1, color=C['coral'], sw=3, head=12, dash='7 6')
    f.dot(sx, sy, 7, C['ink'])
    f.text(sx - 12, sy + 26, 'you', 14, C['ink'], weight=700)
    f.text(bx + 12, by + 12, '✕', 26, C['coral'], weight=700)
    f.hand(118, 105, '40 paces\nnorth-east', 16, C['blue'])
    f.hand(ax + 14, ay + 45, 'then 25 paces\nsouth', 16, C['teal'])
    f.hand(230, 238, 'the sum: one straight walk', 16, C['coral'])
    # compass
    qx, qy = 545, 95
    f.circle(qx, qy, 38, stroke=C['ink'], sw=1.5, fill='#ffffff')
    for d, (a, b) in {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}.items():
        f.line(qx, qy, qx + a * 26, qy + b * 26, stroke=C['ink'], sw=1.4)
        f.text(qx + a * 50, qy + b * 50 + 5, d, 12, C['ink'], 'middle', weight=700)
    f.hand(470, 190, 'tip to tail:\nthat’s all adding is', 16, C['ink'])
    return f.svg()


def fig_note():
    f = Fig(640, 240)
    z, c, k = note()
    t = np.linspace(0, TAU, 1200)
    for i, K in enumerate([3, 8, 20, 80]):
        cx, cy, s = 80 + i * 160, 110, 70
        f.rect(cx - 74, 14, 148, 196, fill=C['coralT'] if i < 2 else C['sunT'], rx=14)
        f.poly([(cx + a.real * s, cy - a.imag * s) for a in z] + [(cx + z[0].real * s, cy - z[0].imag * s)],
               stroke=C['grey'], sw=1, dash='3 4')
        zz = partial(c, k, K, t)
        f.poly([(cx + a.real * s, cy - a.imag * s) for a in zz], stroke=C['coral'], sw=2.3)
        if i in (1, 2):
            ex, ey = draw_chain(f, c, k, K, 1.3, cx, cy, s, op=0.55)
            f.dot(ex, ey, 3.5, C['ink'])
        f.text(cx, 232, f'{K} hands', 14, C['ink'], 'middle', weight=700)
    return f.svg()


def fig_closing():
    f = Fig(640, 260)
    for i, (kk, title, col) in enumerate([(3, '3 turns per loop', C['teal']), (2.5, '2½ turns per loop', C['coral'])]):
        cx, cy, s = 160 + i * 320, 112, 60
        f.rect(cx - 150, 10, 300, 200, fill=C['tealT'] if i == 0 else C['coralT'], rx=16)
        t = np.linspace(0, TAU, 900)
        if i == 1:
            tt = np.linspace(0, 4 * TAU, 3600)
            zz = np.exp(1j * tt) + 0.45 * np.exp(1j * kk * tt)
            f.poly([(cx + a.real * s, cy - a.imag * s) for a in zz], stroke=col, sw=1, op=0.3)
        z = np.exp(1j * t) + 0.45 * np.exp(1j * kk * t)
        f.poly([(cx + a.real * s, cy - a.imag * s) for a in z], stroke=col, sw=2.6)
        st, en = z[0], z[-1]
        f.dot(cx + st.real * s, cy - st.imag * s, 6, C['ink'])
        f.dot(cx + en.real * s, cy - en.imag * s, 5, col)
        f.text(cx, 236, title, 14, C['ink'], 'middle', weight=700)
        if i == 0:
            f.hand(cx + 140, cy + 80, 'back home: it repeats', 15, C['ink'], 'end')
        else:
            f.hand(cx + 140, cy + 88, 'misses home… and smears', 15, C['ink'], 'end')
            f.arrow(cx + en.real * s + 2, cy - en.imag * s + 14, cx + st.real * s - 6, cy - st.imag * s + 10,
                    color=C['ink'], sw=1.3, bend=0.4, head=7, dash='3 3')
    return f.svg()


# ---------- 1.2 ----------
def fig_shadow():
    f = Fig(640, 250)
    cx, cy, R = 110, 125, 82
    th = math.radians(50)
    f.circle(cx, cy, R, stroke=C['grey'], sw=1.2, dash='4 5')
    tx, ty = cx + R * math.cos(th), cy - R * math.sin(th)
    f.line(cx, cy, tx, ty, stroke=C['ink'], sw=5)
    f.dot(cx, cy, 5, C['ink'])
    f.dot(tx, ty, 7, C['coral'])
    x0 = 240
    f.rect(x0, 30, 385, 190, fill=C['sunT'], rx=10)
    f.line(tx, ty, x0 + 2, ty, stroke=C['coral'], sw=1.4, dash='4 4')
    f.line(x0, cy, 625, cy, stroke=C['grey'], sw=1)
    xs = np.linspace(x0, 620, 500)
    ys = cy - R * np.sin(th - (xs - x0) / 50)
    f.poly(list(zip(xs, ys)), stroke=C['coral'], sw=3)
    f.dot(x0, ty, 6, C['coral'])
    f.arrow(470, 240, 560, 240, color=C['ink'], sw=1.8, head=8)
    f.hand(372, 246, 'paper moves', 14, C['ink'])
    f.hand(40, 238, 'a spinning hand…', 15, C['ink'])
    f.hand(300, 22, '…and its height, drawn on moving paper', 15, C['coral'])
    return f.svg()


def wave_row(f, y, h, fn, col, sw=2.2, x0=70, x1=620, n=900):
    xs = np.linspace(0, 1, n)
    ys = fn(xs)
    f.poly([(x0 + a * (x1 - x0), y - b * h) for a, b in zip(xs, ys)], stroke=col, sw=sw)


def fig_chord():
    f = Fig(640, 360)
    rows = [(8, C['blue'], 'C'), (10, C['teal'], 'E'), (12, C['violet'], 'G')]
    for i, (fr, col, nm) in enumerate(rows):
        y = 45 + i * 62
        f.line(70, y, 620, y, stroke=C['mist'], sw=1)
        wave_row(f, y, 20, lambda x, fr=fr: np.sin(TAU * fr * x), col)
        f.text(30, y + 7, nm, 20, col, 'middle', weight=800)
        if i < 2:
            f.text(30, y + 38, '+', 18, C['soft'], 'middle', weight=700)
    f.text(30, 244, '=', 22, C['soft'], 'middle', weight=700)
    y = 290
    f.rect(58, 222, 572, 130, fill=C['coralT'], rx=12)
    f.line(70, y, 620, y, stroke='#f4c7ba', sw=1)
    wave_row(f, y, 17, lambda x: np.sin(TAU * 8 * x) + np.sin(TAU * 10 * x) + np.sin(TAU * 12 * x), C['ink'], sw=2.4)
    f.hand(470, 345, 'one wiggly line: the chord', 15, C['coral'])
    f.hand(500, 18, 'three musicians', 15, C['soft'])
    return f.svg()


def fig_timbre():
    f = Fig(640, 320)
    specs = [('flute', [1, 0.1, 0.04], C['teal'], C['tealT']),
             ('violin', [1 / n for n in range(1, 13)], C['coral'], C['coralT'])]
    for i, (name, amps, col, tint) in enumerate(specs):
        x0 = 20 + i * 315
        f.rect(x0, 10, 300, 300, fill=tint, rx=16)
        f.text(x0 + 20, 40, name.upper(), 15, col, weight=800)
        xs = np.linspace(0, 2, 800)
        ys = sum(a * np.sin(TAU * (n + 1) * xs) for n, a in enumerate(amps))
        ys = ys / np.abs(ys).max()
        f.line(x0 + 20, 110, x0 + 280, 110, stroke='#ffffff', sw=1.5)
        f.poly([(x0 + 20 + a / 2 * 260, 110 - b * 45) for a, b in zip(xs, ys)], stroke=col, sw=2.4)
        base = 280
        for n in range(12):
            a = amps[n] if n < len(amps) else 0
            bx = x0 + 28 + n * 21
            f.rect(bx, base - a * 100, 13, max(a * 100, 1.5), fill=col, rx=3)
        f.line(x0 + 22, base, x0 + 280, base, stroke=C['ink'], sw=1)
        f.hand(x0 + 20, 170, 'how long each hand is →' if i == 0 else 'a long tail of harmonics', 14, C['ink'])
    f.hand(320, 305, '1st hand = same note for both', 13, C['soft'], 'middle')
    return f.svg()


def synth_audio():
    fs, T = 8000, 3.0
    t = np.arange(int(fs * T)) / fs
    f0 = 150 + 20 * np.sin(TAU * 0.35 * t) + 12 * np.sin(TAU * 1.3 * t)
    ph = TAU * np.cumsum(f0) / fs
    env = np.clip(np.sin(TAU * 0.9 * t) ** 2 * 1.4, 0, 1) * 0.8 + 0.2
    voice = sum((1 / k) * np.exp(-((k * 150 - 600) / 500) ** 2) * np.sin(k * ph) for k in range(1, 16))
    voice = voice * env
    rng = np.random.default_rng(3)
    bark = np.zeros_like(t)
    for tb in (0.7, 1.55, 2.35):
        m = (t > tb) & (t < tb + 0.2)
        tt = t[m] - tb
        e = np.exp(-tt / 0.06) * (1 - np.exp(-tt / 0.005))
        noise = np.convolve(rng.standard_normal(m.sum()), np.ones(3) / 3, 'same')
        tone = sum(np.sin(TAU * (520 - 400 * tt) * k * tt) / k for k in range(1, 6))
        bark[m] += e * (1.3 * noise + 1.2 * tone)
    return fs, voice, voice + bark


def spec_png(x, fs):
    from scipy.signal import stft
    fr, tm, Z = stft(x, fs, nperseg=256, noverlap=224)
    keep = fr <= 3000
    db = 20 * np.log10(np.abs(Z[keep]) + 1e-6)
    db = (db - (db.max() - 55)) / 55
    img = ramp(db[::-1], [C['night'], '#3b2a8a', C['violet'], C['coral'], C['sun'], '#fff6d8'])
    return png_from_array(img)


def fig_spectrogram():
    fs, clean, noisy = synth_audio()
    f = Fig(640, 275)
    for i, (x, title) in enumerate([(noisy, 'my voice note, with Bruno'), (clean, 'Bruno’s hands silenced')]):
        x0 = 20 + i * 315
        f.image(x0, 30, 300, 200, spec_png(x, fs))
        f.text(x0, 20, title, 13, C['ink'], weight=700)
        f.hand(x0 + 150, 252, 'time →', 14, C['soft'], 'middle')
    f.hand(8, 150, 'pitch →', 14, C['soft'], rotate=-90)
    for tb in (0.7, 1.55, 2.35):
        bx = 20 + (tb + 0.1) / 3.0 * 300
        f.arrow(bx + 18, 272, bx + 2, 234, color=C['coral'], sw=1.6, head=7)
    f.hand(40, 272, 'barks', 14, C['coral'])
    f.hand(470, 272, 'voice: a neat stack of harmonics', 13, C['teal'], 'middle')
    return f.svg()


# ---------- 1.3 ----------
def fig_swing():
    f = Fig(640, 250)
    t = np.linspace(0, 60, 2000)
    res = t / 2 * np.sin(t)
    w = 1.12
    det = (np.cos(w * t) - np.cos(t)) / (1 - w * w)
    for i, (ys, title, col, tint, note) in enumerate([
            (res, 'pushing in rhythm', C['coral'], C['coralT'], 'every push adds to the last'),
            (det, 'pushing out of rhythm', C['blue'], C['blueT'], 'help, hinder, help… it never gets going')]):
        x0 = 20 + i * 315
        f.rect(x0, 10, 300, 230, fill=tint, rx=16)
        m = mapper(0, 60, -32, 32, x0 + 15, 50, 270, 150)
        f.line(*m(0, 0), *m(60, 0), stroke='#ffffff', sw=1.5)
        f.poly(curve(m, t, ys), stroke=col, sw=1.6)
        f.text(x0 + 18, 36, title.upper(), 13, col, weight=800)
        f.hand(x0 + 150, 228, note, 14, C['ink'], 'middle')
    return f.svg()


def fig_product():
    f = Fig(640, 400)
    x = np.linspace(0, TAU, 900)
    F = np.sin(2 * x) + 0.6 * np.sin(5 * x)
    for i, (kk, col) in enumerate([(2, C['teal']), (3, C['teal'])]):
        x0 = 20 + i * 315
        f.rect(x0, 8, 300, 384, fill='#faf8ff', rx=16, stroke=C['mist'])
        rows = [(F, C['ink'], 'our wiggly line F'), (np.sin(kk * x), col, f'test wave: {kk} turns per loop'),
                (F * np.sin(kk * x), None, 'F × test wave')]
        for j, (ys, c, lab) in enumerate(rows):
            m = mapper(0, TAU, -1.7, 1.7, x0 + 15, 30 + j * 110, 270, 80)
            f.line(*m(0, 0), *m(TAU, 0), stroke=C['grey'], sw=1)
            if c is None:
                signed_fill(f, m, x, ys, op=0.45)
                f.poly(curve(m, x, ys), stroke=C['ink'], sw=1.4)
            else:
                f.poly(curve(m, x, ys), stroke=c, sw=2.2)
            f.text(x0 + 16, 26 + j * 110, lab, 12, C['soft'], weight=700)
        f.hand(x0 + 150, 372, ['matches: the area piles up (total π)', 'no match: it cancels (total 0)'][i], 15,
               C['coral'] if i == 0 else C['blue'], 'middle')
    return f.svg()


def fig_sin2():
    f = Fig(640, 232)
    x = np.linspace(0, 2 * TAU, 900)
    m = mapper(0, 2 * TAU, -1.1, 1.15, 40, 20, 560, 160)
    f.line(*m(0, 0), *m(2 * TAU, 0), stroke=C['grey'], sw=1)
    f.poly(curve(m, x, np.sin(x)), stroke=C['grey'], sw=1.4, dash='4 4')
    y2 = np.sin(x) ** 2
    f.poly([m(0, 0)] + curve(m, x, y2) + [m(2 * TAU, 0)], stroke='none', fill=C['coral'], op=0.22, close=True)
    f.poly(curve(m, x, y2), stroke=C['coral'], sw=2.6)
    f.line(*m(0, 0.5), *m(2 * TAU, 0.5), stroke=C['ink'], sw=1.6, dash='7 5')
    f.hand(605, m(0, 0.5)[1] + 5, '½', 20, C['ink'])
    f.hand(250, 196, 'a pure wave (dashed) … and the same wave times itself (coral)', 14, C['soft'])
    f.hand(40, 226, 'never below zero, and floating at one half', 15, C['coral'])
    return f.svg()


def fig_phase():
    f = Fig(640, 300)
    x = np.linspace(0, TAU, 700)
    G = np.cos(2 * x)
    for j, (probe, name, res, col) in enumerate([(np.sin(2 * x), 'sine test', '0 — missed it!', C['blue']),
                                                  (np.cos(2 * x), 'cosine test', 'π — found it', C['coral'])]):
        y0 = 20 + j * 140
        f.rect(20, y0, 330, 125, fill=C['blueT'] if j == 0 else C['coralT'], rx=14)
        m = mapper(0, TAU, -1.2, 1.2, 35, y0 + 30, 300, 70)
        f.line(*m(0, 0), *m(TAU, 0), stroke='#ffffff', sw=1.4)
        ys = G * probe
        signed_fill(f, m, x, ys, op=0.4)
        f.poly(curve(m, x, ys), stroke=C['ink'], sw=1.3)
        f.text(36, y0 + 22, f'{name.upper()}:  {res}', 12, col, weight=800)
    # reading plane
    ox, oy = 440, 230
    f.line(ox, oy, 620, oy, stroke=C['ink'], sw=1.4)
    f.line(ox, oy, ox, 40, stroke=C['ink'], sw=1.4)
    f.text(620, oy + 20, 'sine reading', 11, C['soft'], 'end', weight=700)
    f.text(ox - 8, 38, 'cosine reading', 11, C['soft'], 'end', weight=700, rotate=-90)
    a = math.radians(58)
    tx, ty = ox + 150 * math.cos(a), oy - 150 * math.sin(a)
    f.line(tx, ty, tx, oy, stroke=C['grey'], sw=1, dash='3 3')
    f.line(tx, ty, ox, ty, stroke=C['grey'], sw=1, dash='3 3')
    f.arrow(ox, oy, tx, ty, color=C['violet'], sw=3.4, head=12)
    f.hand(tx + 8, ty + 8, 'length = the\nhand’s length', 14, C['violet'])
    f.hand(ox + 100, oy - 30, 'angle = where\nit started', 13, C['ink'])
    f.hand(470, 290, 'two readings make one arrow', 15, C['ink'], 'middle')
    return f.svg()


def fig_cochlea():
    f = Fig(640, 290)
    cx, cy = 175, 145
    th = np.linspace(0, 2.6 * TAU, 700)
    r = 120 * np.exp(-0.16 * th) + 6
    cols = ramp(th / th.max(), [C['coral'], C['sun'], C['teal'], C['blue']])
    for i in range(len(th) - 1):
        p = lambda k: (cx + r[k] * math.cos(th[k] + 1.2), cy + r[k] * math.sin(th[k] + 1.2))
        col = '#%02x%02x%02x' % tuple((cols[i] * 255).astype(int))
        f.line(*p(i), *p(i + 1), stroke=col, sw=13 * (1 - 0.55 * i / len(th)))
    for fr, lab in [(20000, '20,000 Hz'), (4000, '4,000'), (1000, '1,000'), (200, '200'), (20, '20 Hz')]:
        pp = math.log(20000 / fr) / math.log(1000)
        k = min(int(pp * (len(th) - 1)), len(th) - 1)
        x, y = cx + r[k] * math.cos(th[k] + 1.2), cy + r[k] * math.sin(th[k] + 1.2)
    f.hand(40, 285, 'entrance: 20,000 Hz', 13, C['coral'])
    f.hand(215, 285, 'far end, in the middle: 20 Hz', 13, C['blue'])
    f.arrow(250, 270, cx + 6, cy + 8, color=C['blue'], sw=1.3, head=7, bend=-0.2)
    # uncoiled strip
    x0, x1, y = 360, 620, 120
    n = 60
    for i in range(n):
        a, b = x0 + (x1 - x0) * i / n, x0 + (x1 - x0) * (i + 1) / n
        col = '#%02x%02x%02x' % tuple((ramp(np.array(i / n), [C['coral'], C['sun'], C['teal'], C['blue']]) * 255).astype(int))
        hh = 10 + 30 * i / n
        f.rect(a, y - hh / 2, b - a + 0.6, hh, fill=col)
    f.text(x0, 70, 'UNCOILED (ABOUT 35 MM)', 11, C['soft'], weight=800)
    for i, lab in enumerate(['20,000', '4,000', '1,000', '200', '20 Hz']):
        f.text(x0 + (x1 - x0) * i / 4, y + 45, lab, 11, C['ink'], 'middle', weight=600)
    f.hand(x0, 215, 'stiff and narrow:\nhigh notes shake it here', 13, C['coral'])
    f.hand(x1, 215, 'wide and floppy:\nlow notes here', 13, C['blue'], 'end')
    return f.svg()


# ---------- 1.4 ----------
def fig_halving():
    f = Fig(640, 270)
    x0, u, y = 50, 260, 50
    f.text(x0, 28, '1 + ½ + ¼ + ⅛ + …', 14, C['ink'], weight=700)
    pos, w, i = 0, 1, 0
    while w * u > 1:
        f.rect(x0 + pos * u, y, w * u - 1.5, 34, fill=C['coral'] if i % 2 == 0 else C['sun'], rx=3)
        pos += w; w /= 2; i += 1
    f.line(x0 + 2 * u, y - 10, x0 + 2 * u, y + 46, stroke=C['ink'], sw=2, dash='5 4')
    f.hand(x0 + 2 * u, y - 14, 'never passes 2', 15, C['ink'], 'end')
    y2, u2 = 170, 118
    f.text(x0, 140, '1 + ½ + ⅓ + ¼ + ⅕ + …', 14, C['ink'], weight=700)
    groups = [[1], [1 / 2], [1 / 3, 1 / 4], [1 / n for n in range(5, 9)], [1 / n for n in range(9, 17)]]
    pos = 0
    for gi, g in enumerate(groups):
        start = pos
        for j, v in enumerate(g):
            f.rect(x0 + pos * u2, y2, v * u2 - 1, 34, fill=C['teal'] if j % 2 == 0 else C['blue'], rx=2)
            pos += v
        if gi >= 2:
            a, b = x0 + start * u2, x0 + pos * u2
            f.poly([(a, y2 + 42), (a, y2 + 50), (b, y2 + 50), (b, y2 + 42)], stroke=C['ink'], sw=1.4)
            f.hand((a + b) / 2, y2 + 72, 'more than ½', 14, C['ink'], 'middle')
        pos += 0.06
    f.hand(x0 + pos * u2 + 6, y2 + 24, '…forever', 16, C['blue'])
    return f.svg()


def fig_corners():
    f = Fig(640, 330)
    x = np.linspace(0, 2 * TAU, 1400)
    tri = lambda K: 8 / math.pi ** 2 * sum((-1) ** k * np.sin((2 * k + 1) * x) / (2 * k + 1) ** 2 for k in range(K))
    sq = lambda K: 4 / math.pi * sum(np.sin((2 * k + 1) * x) / (2 * k + 1) for k in range(K))
    tri_t = 2 / math.pi * np.arcsin(np.sin(x))
    sq_t = np.sign(np.sin(x))
    for r, (fn, target, name, col) in enumerate([(tri, tri_t, 'TRIANGLE', C['teal']), (sq, sq_t, 'SQUARE', C['coral'])]):
        y0 = 30 + r * 150
        f.text(20, y0 - 8, name + ' WAVE', 12, col, weight=800)
        for c, K in enumerate([1, 3, 15]):
            px = 20 + c * 150
            f.rect(px, y0, 140, 110, fill=C['tealT'] if r == 0 else C['coralT'], rx=10)
            m = mapper(0, 2 * TAU, -1.35, 1.35, px + 8, y0 + 8, 124, 94)
            f.poly(curve(m, x, target), stroke=C['grey'], sw=1, dash='3 3')
            f.poly(curve(m, x, fn(K)), stroke=col, sw=1.8)
            f.text(px + 70, y0 + 128, f'{K} hand{"s" if K > 1 else ""}', 12, C['ink'], 'middle', weight=700)
        # amplitude bars
        bx = 480
        f.rect(bx - 10, y0, 160, 110, fill='#faf8ff', rx=10, stroke=C['mist'])
        for k in range(8):
            n = 2 * k + 1
            a = 1 / n ** 2 if r == 0 else 1 / n
            f.rect(bx + k * 18, y0 + 100 - a * 85, 11, max(a * 85, 1.2), fill=col, rx=2)
        f.text(bx + 70, y0 + 128, 'hand lengths', 12, C['ink'], 'middle', weight=700)
    f.hand(372, 190, 'horns!', 15, C['ink'])
    f.arrow(385, 196, 402, 212, color=C['ink'], sw=1.3, head=6)
    return f.svg()


def fig_timeline():
    f = Fig(640, 250)
    y = 125
    m = lambda yr: 40 + (yr - 1800) / 175 * 560
    f.line(m(1800), y, m(1975), y, stroke=C['ink'], sw=3)
    for yr in range(1800, 1976, 25):
        f.line(m(yr), y - 5, m(yr), y + 5, stroke=C['ink'], sw=1.5)
        f.text(m(yr), y + 20, str(yr), 10, C['soft'], 'middle', weight=600)
    ev = [(1807, 'Fourier: any function is\na sum of waves!', C['coral'], -1),
          (1829, 'Dirichlet: true, for\nwell-behaved functions', C['teal'], 1),
          (1873, 'du Bois-Reymond: an unbroken\ncurve where it fails at a point', C['blue'], -1),
          (1926, 'Kolmogorov: a strange one\nwhere it fails everywhere', C['violet'], 1),
          (1966, 'Carleson: it works almost\neverywhere, for anything real', C['coral'], -1)]
    for yr, txt, col, side in ev:
        x = m(yr)
        f.circle(x, y, 8, stroke='#ffffff', sw=2.5, fill=col)
        yy = y + side * 42
        f.line(x, y + side * 9, x, yy - side * 4, stroke=col, sw=1.5)
        ty = yy - 24 if side < 0 else yy + 18
        f.text(x, ty - 14 if side < 0 else ty, str(yr), 13, col, 'middle', weight=800)
        f.text(min(max(x, 75), 555), ty + 2 if side < 0 else ty + 16, txt, 10.5, C['ink'], 'middle', weight=500, lh=1.2)
    return f.svg()


FIGS1 = dict(watch=fig_watch, twohands=fig_twohands, treasure=fig_treasure, note=fig_note,
             closing=fig_closing, shadow=fig_shadow, chord=fig_chord, timbre=fig_timbre,
             spectrogram=fig_spectrogram, swing=fig_swing, product=fig_product, sin2=fig_sin2,
             phase=fig_phase, cochlea=fig_cochlea, halving=fig_halving, corners=fig_corners,
             timeline=fig_timeline)
