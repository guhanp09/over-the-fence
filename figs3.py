"""Chapter 3 illustrations: distance."""
import math
import numpy as np
from svgkit import Fig, C, mapper, curve, png_from_array, ramp
from figs2 import grid, vec

TAU = 2 * math.pi


def hero(w=640, h=400):
    f = Fig(w, h)
    g = f.glow(3.5)
    cx, cy, r = w / 2, h / 2, 140
    f.circle(cx, cy, r, stroke=C['sun'], sw=3, filt=g)
    f.poly([(cx + r, cy), (cx, cy - r), (cx - r, cy), (cx, cy + r)], stroke=C['coral'], sw=3, close=True, filt=g)
    f.poly([(cx + r, cy + r), (cx + r, cy - r), (cx - r, cy - r), (cx - r, cy + r)], stroke=C['teal'], sw=3, close=True, filt=g)
    f.dot(cx, cy, 6, '#ffffff')
    f.hand(cx + r + 12, cy - r + 10, 'king', 16, C['teal'])
    f.hand(cx + 70, cy - 88, 'crow', 16, C['sun'])
    f.hand(cx + 22, cy - 40, 'taxi', 16, C['coral'])
    return f.svg()


def fig_three():
    f = Fig(640, 300)
    f.rect(20, 8, 600, 284, fill='#f4f3fa', rx=16)
    m = mapper(0, 9, 0, 5, 50, 24, 540, 240)
    for x in range(10):
        for y in range(6):
            if x < 9 and y < 5:
                a, b = m(x + 0.12, y + 0.88)
                c, d = m(x + 0.88, y + 0.12)
                f.rect(a, b, c - a, d - b, fill='#ffffff', rx=4)
    A, B = (1, 1), (7, 4)
    f.poly([m(*A), m(4, 1), m(4, 3), m(7, 3), m(7, 4)], stroke=C['coral'], sw=4)
    f.poly([m(*A), m(4, 4), m(7, 4)], stroke=C['teal'], sw=4, dash='2 7')
    f.line(*m(*A), *m(*B), stroke=C['sun'], sw=4)
    f.dot(*m(*A), 8, C['ink'])
    f.dot(*m(*B), 8, C['ink'])
    f.text(m(*A)[0] - 14, m(*A)[1] + 22, 'home', 13, C['ink'], weight=800)
    f.text(m(*B)[0] + 10, m(*B)[1] - 10, 'airport', 13, C['ink'], weight=800)
    f.hand(*m(4.3, 1.45), 'taxi: 6 + 3 = 9 blocks', 15, C['coral'])
    f.hand(*m(1.9, 0.42), 'crow: √(6²+3²) ≈ 6.7', 15, C['ink'])
    f.hand(*m(2.4, 4.35), 'king: 6 moves (diagonals are free)', 15, C['teal'])
    return f.svg()


def fig_circles():
    f = Fig(640, 250)
    specs = [('crow', C['sun'], 'a circle'), ('taxi', C['coral'], 'a diamond!'), ('king', C['teal'], 'a square!')]
    for i, (nm, col, note) in enumerate(specs):
        cx, cy, r = 110 + i * 210, 115, 80
        f.rect(cx - 95, 8, 190, 234, fill='#faf8ff', rx=16, stroke=C['mist'])
        for gx in range(-3, 4):
            for gy in range(-3, 4):
                f.dot(cx + gx * r / 3, cy + gy * r / 3, 1.6, C['grey'])
        if nm == 'crow':
            f.circle(cx, cy, r, stroke=col, sw=3.5)
        elif nm == 'taxi':
            f.poly([(cx + r, cy), (cx, cy - r), (cx - r, cy), (cx, cy + r)], stroke=col, sw=3.5, close=True)
        else:
            f.rect(cx - r, cy - r, 2 * r, 2 * r, stroke=col, sw=3.5)
        f.dot(cx, cy, 5, C['ink'])
        f.text(cx, 222, f'{nm.upper()}’S CIRCLE', 12, col, 'middle', weight=800)
        f.hand(cx, 238, note, 13, C['soft'], 'middle')
    return f.svg()


def fig_triangle():
    f = Fig(640, 260)
    f.rect(20, 8, 300, 244, fill=C['tealT'], rx=16)
    f.rect(340, 8, 280, 244, fill=C['coralT'], rx=16)
    A, B, Cc = (60, 200), (175, 60), (285, 200)
    f.line(*A, *Cc, stroke=C['teal'], sw=4)
    f.poly([A, B, Cc], stroke=C['ink'], sw=2.4, dash='6 5')
    for p, t in zip((A, B, Cc), ('home', 'a friend’s', 'airport')):
        f.dot(*p, 7, C['ink'])
        f.text(p[0], p[1] + (22 if p[1] > 100 else -12), t, 12, C['ink'], 'middle', weight=800)
    f.hand(170, 246, 'direct: never longer than the detour', 14, C['teal'], 'middle')
    rows = [('Delhi → London, direct', '₹60,000'), ('Delhi → Dubai', '₹12,000'), ('Dubai → London', '₹30,000')]
    for j, (a, b) in enumerate(rows):
        y = 58 + j * 38
        f.text(360, y, a, 13, C['ink'], weight=600)
        f.text(600, y, b, 13, C['coral'] if j == 0 else C['ink'], 'end', weight=800)
    f.line(360, 150, 600, 150, stroke=C['ink'], sw=1)
    f.text(360, 172, 'via Dubai, two tickets', 13, C['ink'], weight=600)
    f.text(600, 172, '₹42,000', 13, C['teal'], 'end', weight=800)
    f.hand(480, 222, 'price breaks the rule:\nit isn’t a distance', 14, C['coral'], 'middle')
    return f.svg()


def tiles(f, x, y, word, hi=(), col=C['coral'], size=30):
    for i, ch in enumerate(word):
        on = i in hi
        f.rect(x + i * (size + 4), y, size, size, fill=col if on else '#ffffff', stroke=col if on else C['mist'], sw=1.5, rx=6)
        f.text(x + i * (size + 4) + size / 2, y + size * 0.7, ch, 17, '#ffffff' if on else C['ink'], 'middle', weight=800)


def fig_edits():
    f = Fig(640, 250)
    steps = [('kitten', (), ''), ('sitten', (0,), 'swap k → s'), ('sittin', (4,), 'swap e → i'), ('sitting', (6,), 'add a g')]
    for j, (w, hi, lab) in enumerate(steps):
        y = 14 + j * 58
        tiles(f, 60, y, w, hi)
        if lab:
            f.hand(330, y + 22, f'edit {j}: {lab}', 16, C['coral'])
    f.hand(470, 120, '3 edits:\nthe distance\nfrom kitten\nto sitting', 17, C['ink'])
    return f.svg()


def fig_prune():
    f = Fig(640, 280)
    f.rect(20, 8, 600, 264, fill='#faf8ff', rx=16, stroke=C['mist'])
    cat, typo, ele = (180, 150), (215, 125), (520, 150)
    f.circle(*cat, 45, stroke=C['blue'], sw=1.5, dash='4 4', fill=C['blueT'])
    f.line(*cat, *ele, stroke=C['ink'], sw=1.4, dash='5 4')
    f.dot(*cat, 7, C['blue'])
    f.dot(*typo, 6, C['coral'])
    f.dot(*ele, 7, C['ink'])
    f.text(cat[0] - 12, cat[1] + 24, 'cat', 15, C['blue'], 'end', weight=800)
    f.text(typo[0] + 10, typo[1] - 8, 'cst (typo)', 14, C['coral'], weight=800)
    f.text(ele[0], ele[1] - 14, 'elephant', 15, C['ink'], 'middle', weight=800)
    f.hand(350, 140, '6 edits', 15, C['ink'], 'middle')
    f.hand(70, 240, 'typo is 1 from cat, cat is 6 from elephant →\nso typo is at least 5 from elephant: skip it!', 15, C['coral'])
    return f.svg()


def fig_curve_distance():
    f = Fig(640, 230)
    x = np.linspace(0, 1, 500)
    a = 0.6 * np.sin(TAU * 2 * x) + 0.2 * np.sin(TAU * 5 * x)
    b = 0.5 * np.sin(TAU * 2 * x + 0.35) + 0.15 * np.sin(TAU * 3 * x)
    for i in range(2):
        x0 = 20 + i * 315
        f.rect(x0, 8, 300, 214, fill=C['sunT'] if i == 0 else C['violetT'], rx=16)
        m = mapper(0, 1, -1.1, 1.1, x0 + 15, 30, 270, 150)
        if i == 0:
            f.poly(curve(m, x, a) + curve(m, x[::-1], b[::-1]), stroke='none', fill=C['sun'], op=0.55, close=True)
        else:
            k = int(np.argmax(np.abs(a - b)))
            f.arrow(*m(x[k], b[k]), *m(x[k], a[k]), color=C['violet'], sw=2.4, head=8)
        f.poly(curve(m, x, a), stroke=C['ink'], sw=2)
        f.poly(curve(m, x, b), stroke=C['coral'], sw=2)
        f.hand(x0 + 150, 208, ['distance = the area between', 'distance = the biggest gap'][i], 15, C['ink'], 'middle')
    return f.svg()


def sq_partial(x, K):
    return 4 / math.pi * sum(np.sin((2 * k + 1) * x) / (2 * k + 1) for k in range(K))


def fig_gibbs():
    f = Fig(640, 280)
    f.rect(20, 8, 600, 264, fill='#faf8ff', rx=16, stroke=C['mist'])
    x = np.linspace(-0.9, 0.9, 1500)
    m = mapper(-0.9, 0.9, -1.35, 1.35, 50, 24, 540, 220)
    f.poly([m(-0.9, -1), m(0, -1), m(0, 1), m(0.9, 1)], stroke=C['grey'], sw=2, dash='5 4')
    for K, col in [(5, C['teal']), (15, C['blue']), (60, C['coral'])]:
        f.poly(curve(m, x, sq_partial(x, K)), stroke=col, sw=1.8)
    f.line(*m(-0.9, 1.179), *m(0.9, 1.179), stroke=C['ink'], sw=1, dash='3 3')
    f.hand(*m(-0.85, 1.24), 'the horn: about 9% of the jump, however many hands', 14, C['ink'])
    f.hand(*m(-0.85, 0.35), '5 hands', 14, C['teal'])
    f.hand(*m(-0.85, 0.15), '15 hands', 14, C['blue'])
    f.hand(*m(-0.85, -0.05), '60 hands', 14, C['coral'])
    return f.svg()


def fig_two_rulers():
    f = Fig(640, 240)
    x = np.linspace(0.0005, math.pi - 0.0005, 6000)
    Ks = list(range(1, 41))
    area, gap = [], []
    for K in Ks:
        e = sq_partial(x, K) - 1
        area.append(np.sqrt(np.mean(e ** 2)))
        gap.append(np.abs(e).max())
    m = mapper(0, 41, 0, 1.1, 60, 20, 540, 180)
    f.line(*m(0, 0), *m(41, 0), stroke=C['ink'], sw=1.2)
    f.poly([m(k, g) for k, g in zip(Ks, gap)], stroke=C['coral'], sw=3)
    f.poly([m(k, a / area[0] * 0.9) for k, a in zip(Ks, area)], stroke=C['teal'], sw=3)
    f.hand(*m(22, 1.03), 'biggest gap: never shrinks', 15, C['coral'])
    f.hand(*m(14, 0.33), 'area between: shrinks towards zero', 15, C['teal'])
    f.text(*m(20.5, -0.13), 'NUMBER OF HANDS →', 11, C['soft'], 'middle', weight=800)
    return f.svg()


def fig_ringing():
    f = Fig(640, 210)
    x = np.linspace(-1, 1, 640)
    sharp = (x > 0).astype(float)
    ring = 0.5 + 0.5 * sq_partial(x * math.pi / 2 + math.pi / 2 - math.pi / 2, 9)
    ring = np.clip(0.5 + 0.5 * sq_partial(x * math.pi, 9), -0.1, 1.1)
    for i, (prof, lab) in enumerate([(sharp, 'a sharp edge'), (ring, 'the same edge, built from a few waves')]):
        y0 = 12 + i * 98
        img = ramp(np.tile(np.clip(prof, 0, 1), (40, 1)), [C['night'], '#fff6e6'])
        f.image(20, y0, 600, 40, png_from_array(img))
        m = mapper(-1, 1, -0.2, 1.25, 20, y0 + 44, 600, 36)
        f.poly(curve(m, x, prof), stroke=C['coral'], sw=1.8)
        f.text(24, y0 + 94, lab.upper(), 11, C['soft'], weight=800)
    f.hand(600, 200, 'ghost ripples beside the edge', 14, C['coral'], 'end')
    return f.svg()


FIGS3 = dict(three=fig_three, circles=fig_circles, triangle=fig_triangle, edits=fig_edits, prune=fig_prune,
             curvedist=fig_curve_distance, gibbs=fig_gibbs, rulers=fig_two_rulers, ringing=fig_ringing)
