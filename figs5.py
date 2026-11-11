"""Chapter 5 illustrations: groups."""
import math
import numpy as np
from svgkit import Fig, C

TAU = 2 * math.pi
PINK, PINKT = '#ff4d8d', '#ffe3ee'


def clock_pts(cx, cy, r, n=12):
    return [(cx + r * math.sin(TAU * k / n), cy - r * math.cos(TAU * k / n)) for k in range(n)]


def hero(w=640, h=400):
    f = Fig(w, h)
    g = f.glow(3.5)
    pts = clock_pts(w / 2, h / 2, 150)
    order = [(5 * k) % 12 for k in range(13)]
    f.poly([pts[i] for i in order], stroke=C['sun'], sw=2.6, filt=g)
    f.circle(w / 2, h / 2, 165, stroke='#8f8ad8', sw=1.2, op=0.6)
    for k, (x, y) in enumerate(pts):
        f.dot(x, y, 5, PINK)
        f.text(w / 2 + 185 * math.sin(TAU * k / 12), h / 2 - 185 * math.cos(TAU * k / 12) + 5, str(k or 12), 13, '#ffffff', 'middle', weight=700, op=0.8)
    return f.svg()


def mattress(f, x, y, face_up, head_top, w=120, h=70):
    f.rect(x, y, w, h, fill=C['sunT'] if face_up else C['violetT'], stroke=C['ink'], sw=2, rx=12)
    f.text(x + w / 2, y + h / 2 + 5, 'SOFT SIDE UP' if face_up else 'FIRM SIDE UP', 11, C['ink'], 'middle', weight=800)
    hy = y + 14 if head_top else y + h - 8
    f.text(x + w / 2, hy, 'HEAD' if True else '', 9, C['coral'], 'middle', weight=800)


def fig_mattress():
    f = Fig(640, 320)
    P = {(1, 1): (90, 30), (1, 0): (430, 30), (0, 1): (90, 220), (0, 0): (430, 220)}
    for (fu, ht), (x, y) in P.items():
        mattress(f, x, y, fu, ht)
    c = lambda k: (P[k][0] + 60, P[k][1] + 35)
    edges = [((1, 1), (1, 0), C['teal'], 'spin'), ((0, 1), (0, 0), C['teal'], 'spin'),
             ((1, 1), (0, 1), C['blue'], 'roll'), ((1, 0), (0, 0), C['blue'], 'roll'),
             ((1, 1), (0, 0), PINK, 'flop'), ((1, 0), (0, 1), PINK, 'flop')]
    for a, b, col, lab in edges:
        (x1, y1), (x2, y2) = c(a), c(b)
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        sx, sy = x1 + dx / d * 70, y1 + dy / d * 45
        ex, ey = x2 - dx / d * 70, y2 - dy / d * 45
        f.line(sx, sy, ex, ey, stroke=col, sw=3)
    f.hand(320, 55, 'spin (end to end, same side up)', 14, C['teal'], 'middle')
    f.hand(40, 165, 'roll\n(over the\nlong side)', 14, C['blue'])
    f.rect(215, 176, 210, 26, fill='#ffffff', rx=10)
    f.hand(320, 194, 'flop (over the short end)', 14, PINK, 'middle')
    f.hand(320, 312, 'four positions, three moves: every move, done twice, undoes itself', 14, C['ink'], 'middle')
    return f.svg()


def fig_clocks():
    f = Fig(640, 250)
    for i, (step, note) in enumerate([(1, '+1 hour: visits all 12'), (3, '+3 hours: stuck on 4'), (5, '+5 hours: visits all 12!')]):
        cx, cy, r = 110 + i * 210, 112, 80
        f.circle(cx, cy, r + 14, stroke=C['ink'], sw=3, fill='#ffffff')
        pts = clock_pts(cx, cy, r)
        seen, k = [], 0
        while k not in seen:
            seen.append(k)
            k = (k + step) % 12
        f.poly([pts[j] for j in seen] + [pts[seen[0]]], stroke=PINK if i != 1 else C['blue'], sw=2.2)
        for j, (x, y) in enumerate(pts):
            f.dot(x, y, 4.5 if j in seen else 3, PINK if j in seen else C['grey'])
        f.hand(cx, 232, note, 15, C['ink'], 'middle')
    return f.svg()


def fig_table():
    f = Fig(640, 300)
    names = ['stay', 'spin', 'roll', 'flop']
    cols = [C['mist'], C['teal'], C['blue'], PINK]
    tab = [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    x0, y0, s = 170, 50, 56
    f.text(x0 - 12, y0 - 12, 'then →', 12, C['soft'], 'end', weight=800)
    for j, nm in enumerate(names):
        f.text(x0 + j * s + s / 2, y0 - 12, nm, 13, C['ink'], 'middle', weight=800)
        f.text(x0 - 12, y0 + j * s + s / 2 + 5, nm, 13, C['ink'], 'end', weight=800)
        for k in range(4):
            v = tab[j][k]
            f.rect(x0 + k * s + 2, y0 + j * s + 2, s - 4, s - 4, fill=cols[v], rx=8, op=0.9 if v else 1)
            f.text(x0 + k * s + s / 2, y0 + j * s + s / 2 + 5, names[v], 12, '#ffffff' if v else C['ink'], 'middle', weight=800)
    f.hand(430, 90, 'every move appears\nonce in each row\nand once in each column:\na Sudoku!', 16, C['ink'])
    f.hand(430, 230, 'and it’s symmetric:\norder doesn’t matter\nfor a mattress', 15, C['soft'])
    return f.svg()


def fig_socks():
    f = Fig(640, 200)
    steps = [('socks on', C['teal']), ('shoes on', C['blue']), ('shoes off', C['blue']), ('socks off', C['teal'])]
    for i, (t, col) in enumerate(steps):
        x = 30 + i * 150
        f.rect(x, 50, 120, 60, fill=col, rx=14, op=1 if i < 2 else 0.8)
        f.text(x + 60, 86, t, 15, '#ffffff', 'middle', weight=800)
        if i in (0, 2):
            f.arrow(x + 124, 80, x + 146, 80, color=C['ink'], sw=2, head=8)
    f.line(318, 30, 318, 140, stroke=C['grey'], sw=1.5, dash='4 4')
    f.hand(140, 30, 'getting dressed', 15, C['ink'], 'middle')
    f.hand(470, 30, 'undoing it: reverse order', 15, C['ink'], 'middle')
    f.hand(320, 180, 'socks-then-shoes ≠ shoes-then-socks: order matters', 15, C['coral'], 'middle')
    return f.svg()


def tri(f, cx, cy, labels, r=46, col=C['violet']):
    pts = [(cx + r * math.sin(TAU * k / 3), cy - r * math.cos(TAU * k / 3)) for k in range(3)]
    f.poly(pts, stroke=col, sw=2.4, fill=C['violetT'], close=True)
    for (x, y), lab in zip(pts, labels):
        f.circle(x, y, 11, stroke='none', fill=C['ink'])
        f.text(x, y + 5, lab, 12, '#ffffff', 'middle', weight=800)


def fig_triangle_moves():
    f = Fig(640, 300)
    rot = lambda L: [L[2], L[0], L[1]]
    flip = lambda L: [L[0], L[2], L[1]]
    start = ['1', '2', '3']
    rows = [('turn, then flip', [start, rot(start), flip(rot(start))]), ('flip, then turn', [start, flip(start), rot(flip(start))])]
    for r, (title, states) in enumerate(rows):
        y = 85 + r * 140
        f.text(20, y - 62, title.upper(), 12, C['soft'], weight=800)
        for i, st in enumerate(states):
            tri(f, 100 + i * 170, y + 10, st, col=C['coral'] if i == 2 else C['violet'])
            if i < 2:
                f.arrow(150 + i * 170, y + 10, 210 + i * 170, y + 10, color=C['ink'], sw=2, head=8)
    f.hand(560, 90, 'different\nendings!', 17, C['coral'], 'middle')
    return f.svg()


def board(f, x0, y0, nums, s=40, hi=()):
    for i, n in enumerate(nums):
        r, c = divmod(i, 4)
        x, y = x0 + c * s, y0 + r * s
        if n is None:
            f.rect(x + 2, y + 2, s - 4, s - 4, fill='none', stroke=C['grey'], sw=1.5, rx=7, dash='3 3')
        else:
            f.rect(x + 2, y + 2, s - 4, s - 4, fill=PINK if n in hi else C['ink'], rx=7)
            f.text(x + s / 2, y + s / 2 + 6, str(n), 15, '#ffffff', 'middle', weight=800)


def fig_fifteen():
    f = Fig(640, 230)
    solved = list(range(1, 16)) + [None]
    swapped = solved[:13] + [15, 14, None]
    board(f, 70, 20, solved)
    board(f, 400, 20, swapped, hi=(14, 15))
    f.hand(150, 210, 'solved', 16, C['ink'], 'middle')
    f.hand(480, 210, '14 and 15 swapped: impossible', 16, PINK, 'middle')
    return f.svg()


def fig_checker():
    f = Fig(640, 250)
    s, x0, y0 = 46, 60, 20
    for r in range(4):
        for c in range(4):
            f.rect(x0 + c * s, y0 + r * s, s, s, fill=C['ink'] if (r + c) % 2 else '#ffffff', stroke=C['ink'], sw=1)
    path = [(3, 3), (3, 2), (2, 2), (2, 1), (3, 1), (3, 2), (3, 3)]
    pts = [(x0 + c * s + s / 2, y0 + r * s + s / 2) for r, c in path]
    f.poly(pts, stroke=PINK, sw=4)
    for i, p in enumerate(pts):
        f.circle(*p, 7, stroke='#ffffff', sw=2, fill=PINK)
    f.hand(300, 60, 'every slide moves the empty square\nonto the other colour', 15, C['ink'])
    f.hand(300, 120, 'so to come home, it needs an\neven number of slides', 15, C['ink'])
    f.hand(300, 180, 'every slide is one swap → an even\nnumber of swaps. One swap is odd.', 15, PINK)
    return f.svg()


FIGS5 = dict(mattress=fig_mattress, clocks=fig_clocks, table=fig_table, socks=fig_socks,
             trimoves=fig_triangle_moves, fifteen=fig_fifteen, checker=fig_checker)
