"""Chapter 4 illustrations: eigenvectors."""
import math
import numpy as np
from svgkit import Fig, C, mapper, curve

TAU = 2 * math.pi
ROLL = np.array([[2.0, 1.0], [1.0, 2.0]])


def hero(w=640, h=400):
    f = Fig(w, h)
    g = f.glow(3.5)
    o = np.array([w / 2, h / 2])
    s = 34
    P = lambda v: tuple(o + s * np.asarray(v) * np.array([1, -1]))
    for a in range(-6, 7):
        f.line(*P(ROLL @ [a, -6]), *P(ROLL @ [a, 6]), stroke='#4a44a0', sw=1, op=0.7)
        f.line(*P(ROLL @ [-6, a]), *P(ROLL @ [6, a]), stroke='#4a44a0', sw=1, op=0.7)
    f.line(*P((-5, -5)), *P((5, 5)), stroke=C['coral'], sw=3.5, filt=g)
    f.line(*P((-5, 5)), *P((5, -5)), stroke=C['sun'], sw=3.5, filt=g)
    f.hand(*P((3.4, 4.7)), 'stretched ×3', 16, C['coral'])
    f.hand(*P((3.6, -3.1)), 'left alone', 16, C['sun'])
    return f.svg()


def face(f, T, cx, cy, s, col=C['ink']):
    t = np.linspace(0, TAU, 200)
    P = lambda x, y: (cx + s * (T[0, 0] * x + T[0, 1] * y), cy - s * (T[1, 0] * x + T[1, 1] * y))
    f.poly([P(math.cos(a), math.sin(a)) for a in t], stroke=col, sw=2, fill=C['sunT'])
    for ex in (-0.35, 0.35):
        f.poly([P(ex + 0.08 * math.cos(a), 0.3 + 0.08 * math.sin(a)) for a in t], stroke=col, sw=2, fill=col)
    f.poly([P(0.5 * math.cos(a), 0.5 * math.sin(a)) for a in np.linspace(math.pi * 1.15, math.pi * 1.85, 40)], stroke=col, sw=2.2)
    return P


def fig_dough():
    f = Fig(640, 270)
    T0, T1 = np.eye(2), np.array([[2.0, 0], [0, 1.0]])
    for i, (T, title) in enumerate([(T0, 'BEFORE ROLLING'), (T1, 'AFTER ONE ROLL (STRETCH ×2 LEFT-RIGHT)')]):
        cx = 120 if i == 0 else 430
        P = face(f, T, cx, 140, 70)
        for k in range(8):
            a = k * TAU / 8
            v = np.array([math.cos(a), math.sin(a)]) * 1.35
            special = k % 2 == 0
            col = C['coral'] if k in (0, 4) else (C['teal'] if k in (2, 6) else C['grey'])
            end = T @ v
            f.arrow(cx, 140, cx + 70 * end[0], 140 - 70 * end[1], color=col, sw=2.6 if special else 1.6, head=8)
        f.text(cx, 24, title, 11, C['soft'], 'middle', weight=800)
    f.arrow(235, 140, 285, 140, color=C['ink'], sw=2.5, head=10)
    f.hand(430, 262, 'grey arrows turn; coral and teal don’t', 15, C['ink'], 'middle')
    return f.svg()


def fig_shear():
    f = Fig(640, 230)
    for i, k in enumerate([0, 0.55]):
        x0 = 60 + i * 320
        for j in range(10):
            y = 190 - j * 15
            f.rect(x0 + k * j * 15, y, 160, 12, fill=C['violetT'] if j % 2 else '#ffffff', stroke=C['violet'], sw=1.2, rx=2)
        f.arrow(x0, 196, x0 + 150, 196, color=C['coral'], sw=3, head=10)
        f.arrow(x0, 196, x0 + k * 140, 196 - 140, color=C['grey'], sw=2.5, head=10)
    f.hand(60, 30, 'a neat stack of cards...', 15, C['ink'])
    f.hand(380, 30, '...pushed sideways', 15, C['ink'])
    f.hand(320, 224, 'coral: along the table, never turns.  grey: leans over', 13, C['ink'], 'middle')
    return f.svg()


def fig_phone():
    f = Fig(640, 250)
    x0, y0, w, h = 270, 30, 100, 190
    f.rect(x0, y0, w, h, fill=C['ink'], rx=18)
    f.rect(x0 + 8, y0 + 14, w - 16, h - 28, fill=C['violetT'], rx=8)
    f.line(x0 + w / 2, y0 - 22, x0 + w / 2, y0 + h + 22, stroke=C['teal'], sw=3, dash='7 5')
    f.line(x0 - 60, y0 + h / 2, x0 + w + 60, y0 + h / 2, stroke=C['coral'], sw=3, dash='7 5')
    f.circle(x0 + w / 2, y0 + h / 2, 12, stroke=C['teal'], sw=3, fill='#ffffff')
    f.dot(x0 + w / 2, y0 + h / 2, 4, C['teal'])
    f.hand(x0 + w / 2 + 14, 16, 'long axis: spins cleanly', 15, C['teal'])
    f.hand(x0 + w + 66, y0 + h / 2 + 5, 'across the screen:\ntumbles!', 15, C['coral'])
    f.hand(x0 - 20, y0 + h / 2 + 50, 'straight through the\nscreen (out of the page):\nspins cleanly', 14, C['teal'], 'end')
    return f.svg()


def fig_power():
    f = Fig(640, 250)
    f.rect(20, 8, 600, 234, fill='#faf8ff', rx=16, stroke=C['mist'])
    starts = [np.array([1.0, -0.6]), np.array([-0.3, 1.0])]
    for si, v0 in enumerate(starts):
        cx, cy = 170 + si * 300, 150
        f.line(cx - 110, cy + 110, cx + 110, cy - 110, stroke=C['coral'], sw=1.2, dash='4 5', op=0.7)
        v = v0 / np.linalg.norm(v0)
        for k in range(7):
            col = C['grey'] if k < 6 else C['coral']
            f.arrow(cx, cy, cx + 105 * v[0], cy - 105 * v[1], color=col, sw=1.6 + 0.3 * k, head=8, op=0.35 + 0.1 * k)
            if k in (0,):
                f.hand(cx + 110 * v[0] + 6, cy - 110 * v[1] + 12, 'start', 13, C['soft'])
            v = ROLL @ v
            v = v / np.linalg.norm(v)
    f.hand(320, 34, 'roll, roll, roll: every arrow swings towards the diagonal', 15, C['ink'], 'middle')
    return f.svg()


def fig_rollgrid():
    f = Fig(640, 280)
    for i, T in enumerate([np.eye(2), ROLL]):
        x0 = 20 + i * 315
        f.rect(x0, 8, 300, 264, fill=C['violetT'] if i else '#faf8ff', rx=16, stroke=C['mist'])
        o = np.array([x0 + 110.0, 180.0])
        s = 36
        P = lambda v: tuple(o + s * (T @ np.asarray(v, float)) * np.array([1, -1]))
        for a in range(-1, 3):
            f.line(*P((a, -1)), *P((a, 2)), stroke='#ffffff' if i else C['mist'], sw=1.2)
            f.line(*P((-1, a)), *P((2, a)), stroke='#ffffff' if i else C['mist'], sw=1.2)
        f.poly([P((0, 0)), P((1, 0)), P((1, 1)), P((0, 1))], stroke=C['ink'], sw=1.6, fill=C['sun'], fop=0.35, close=True)
        f.arrow(*P((0, 0)), *P((1, 1)), color=C['coral'], sw=3.6, head=12)
        f.arrow(*P((0, 0)), *P((1, -1)), color=C['teal'], sw=3.6, head=12)
        f.text(x0 + 18, 30, 'BEFORE' if i == 0 else 'AFTER roll(v)', 12, C['soft'], weight=800)
    f.hand(330, 60, 'diagonal: ×3', 15, C['coral'])
    f.hand(470, 262, 'anti-diagonal: untouched (×1)', 14, C['teal'], 'middle')
    f.hand(500, 60, 'the square’s area: ×3', 14, C['ink'])
    return f.svg()


def fig_collapse():
    f = Fig(640, 250)
    f.rect(20, 8, 600, 234, fill='#faf8ff', rx=16, stroke=C['mist'])
    M = ROLL - 3 * np.eye(2)
    o1, o2, s = np.array([150.0, 125]), np.array([470.0, 125]), 26
    for a in range(-3, 4):
        for b in range(-3, 4):
            p = np.array([a, b], float)
            q = M @ p * 0.5
            f.dot(o1[0] + s * a, o1[1] - s * b, 3, C['violet'])
            f.dot(o2[0] + s * q[0], o2[1] - s * q[1], 3, C['violet'], op=0.5)
    f.line(o2[0] - 100, o2[1] + 100, o2[0] + 100, o2[1] - 100, stroke=C['coral'], sw=1.4, dash='4 4')
    f.arrow(290, 125, 350, 125, color=C['ink'], sw=2.4, head=10)
    f.hand(320, 108, 'roll − 3', 15, C['ink'], 'middle')
    f.hand(470, 232, 'squashed onto a line: area zero', 15, C['coral'], 'middle')
    f.hand(150, 232, 'the whole plane', 15, C['violet'], 'middle')
    return f.svg()


def fig_fibonacci():
    f = Fig(640, 230)
    F = [1, 1]
    for _ in range(14):
        F.append(F[-1] + F[-2])
    r = [F[i + 1] / F[i] for i in range(1, 14)]
    m = mapper(0, 14, 0.9, 2.1, 60, 20, 540, 170)
    phi = (1 + 5 ** 0.5) / 2
    f.line(*m(0, phi), *m(14, phi), stroke=C['violet'], sw=1.6, dash='6 5')
    f.poly([m(i + 1, v) for i, v in enumerate(r)], stroke=C['coral'], sw=2)
    for i, v in enumerate(r):
        f.dot(*m(i + 1, v), 5, C['coral'])
    f.hand(*m(9.3, phi + 0.13), '1.618… the golden ratio', 15, C['violet'])
    f.text(*m(7, 0.78), 'MONTH →   (THIS MONTH’S RABBITS ÷ LAST MONTH’S)', 11, C['soft'], 'middle', weight=800)
    return f.svg()


def fig_pagerank():
    f = Fig(640, 270)
    f.rect(20, 8, 600, 254, fill='#faf8ff', rx=16, stroke=C['mist'])
    pos = {'A': (100, 70), 'B': (250, 60), 'C': (300, 190), 'D': (140, 210), 'E': (60, 150)}
    links = {'A': 'BC', 'B': 'C', 'C': 'A', 'D': 'CA', 'E': 'AD'}
    names = list(pos)
    n = len(names)
    Mx = np.zeros((n, n))
    for j, a in enumerate(names):
        for b in links[a]:
            Mx[names.index(b), j] = 1 / len(links[a])
    G = 0.85 * Mx + 0.15 / n
    v = np.ones(n) / n
    for _ in range(100):
        v = G @ v
    for a in names:
        for b in links[a]:
            (x1, y1), (x2, y2) = pos[a], pos[b]
            d = math.hypot(x2 - x1, y2 - y1)
            rb = 12 + 60 * v[names.index(b)]
            f.arrow(x1 + (x2 - x1) * 22 / d, y1 + (y2 - y1) * 22 / d, x2 - (x2 - x1) * rb / d, y2 - (y2 - y1) * rb / d,
                    color=C['grey'], sw=1.6, head=8, bend=0.08)
    for i, a in enumerate(names):
        r = 12 + 60 * v[i]
        f.circle(*pos[a], r, stroke='none', fill=C['blue'])
        f.text(pos[a][0], pos[a][1] + 5, a, 14, '#ffffff', 'middle', weight=800)
    for i, a in enumerate(names):
        y = 50 + i * 38
        f.text(390, y + 12, a, 13, C['ink'], weight=800)
        f.rect(415, y, 180 * v[i] / v.max(), 18, fill=C['blue'], rx=4)
        f.text(420 + 180 * v[i] / v.max(), y + 14, f'{v[i] * 100:.0f}%', 12, C['ink'], weight=700)
    f.hand(505, 250, 'share of time the random surfer spends', 13, C['soft'], 'middle')
    return f.svg()


def fig_modes():
    f = Fig(640, 250)
    x = np.linspace(0, 1, 400)
    for k in range(1, 4):
        y0 = 40 + (k - 1) * 72
        for ph, op in ((1, 1), (-1, 0.35)):
            f.poly([(80 + a * 400, y0 - ph * 26 * math.sin(math.pi * k * a)) for a in x], stroke=[C['coral'], C['teal'], C['violet']][k - 1], sw=2.4, op=op)
        f.dot(80, y0, 5, C['ink'])
        f.dot(480, y0, 5, C['ink'])
        f.text(40, y0 + 5, f'{k}', 16, C['ink'], 'middle', weight=800)
        f.hand(500, y0 + 5, ['the note', 'an octave up', 'an octave and a fifth'][k - 1], 13, C['soft'])
    f.hand(310, 240, 'each shape keeps its shape as it swings: an eigenvector of the string', 14, C['ink'], 'middle')
    return f.svg()


FIGS4 = dict(dough=fig_dough, shear=fig_shear, phone=fig_phone, power=fig_power, rollgrid=fig_rollgrid,
             collapse=fig_collapse, fibonacci=fig_fibonacci, pagerank=fig_pagerank, modes=fig_modes)
