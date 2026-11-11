"""Chapter 6 (Bayes) and Chapter 7 (regression to the mean) illustrations."""
import math
import numpy as np
from svgkit import Fig, C, mapper

GOLD, GOLDT = '#e09a00', '#fff1cc'
GREEN, GREENT = '#1f9d55', '#dcf5e5'


def hero6(w=640, h=400):
    f = Fig(w, h)
    g = f.glow(3)
    rng = np.random.default_rng(2)
    for i in range(40):
        for j in range(22):
            x, y = 40 + i * 14.4, 45 + j * 14.4
            k = i * 22 + j
            if k in (300, 301, 302, 322, 323, 324, 344, 345, 346):
                f.circle(x, y, 5, stroke='none', fill=C['coral'], filt=g)
            elif rng.random() < 0.1:
                f.circle(x, y, 4, stroke='none', fill=C['sun'], op=0.9)
            else:
                f.circle(x, y, 3, stroke='none', fill='#5d58b8', op=0.7)
    return f.svg()


def fig_crowd():
    f = Fig(640, 330)
    rng = np.random.default_rng(7)
    healthy_pos = set(rng.choice(np.arange(10, 1000), 99, replace=False))
    for k in range(1000):
        i, j = divmod(k, 25)
        x, y = 22 + i * 15, 18 + j * 11.5
        if k < 9:
            f.circle(x, y, 4.6, stroke='none', fill=C['coral'])
        elif k == 9:
            f.circle(x, y, 4, stroke=C['coral'], sw=1.6)
        elif k in healthy_pos:
            f.circle(x, y, 4.2, stroke='none', fill=C['sun'])
        else:
            f.circle(x, y, 3.2, stroke='none', fill=C['mist'])
    y = 316
    for x, col, t, outline in [(22, C['coral'], '9 ill, caught', False), (160, C['coral'], '1 ill, missed', True),
                               (290, C['sun'], '99 healthy, false alarm', False), (480, C['mist'], '891 healthy, clear', False)]:
        if outline:
            f.circle(x + 5, y - 5, 5, stroke=col, sw=1.6)
        else:
            f.circle(x + 5, y - 5, 5.5, stroke='none', fill=col)
        f.text(x + 16, y, t, 12, C['ink'], weight=700)
    return f.svg()


def fig_positives():
    f = Fig(640, 170)
    x0, w = 40, 560
    f.text(x0, 28, 'EVERYONE WHO TESTED POSITIVE: 108 PEOPLE', 12, C['soft'], weight=800)
    a = w * 9 / 108
    f.rect(x0, 42, a, 56, fill=C['coral'], rx=8)
    f.rect(x0 + a + 3, 42, w - a - 3, 56, fill=C['sun'], rx=8)
    f.text(x0 + a / 2, 77, '9', 18, '#ffffff', 'middle', weight=800)
    f.text(x0 + a + (w - a) / 2, 77, '99 false alarms', 17, C['ink'], 'middle', weight=800)
    f.hand(x0 + a / 2, 122, 'ill', 16, C['coral'], 'middle')
    f.hand(320, 150, 'so a positive result means about a 1 in 12 chance you’re ill', 16, C['ink'], 'middle')
    return f.svg()


def fig_odds():
    f = Fig(640, 250)
    stages = [('before', 1, 99), ('after test 1', 9, 99), ('after test 2', 81, 99), ('after test 3', 729, 99)]
    for i, (lab, a, b) in enumerate(stages):
        x = 30 + i * 155
        tot = a + b
        h = 150
        f.rect(x, 40, 110, h, fill=C['sun'], rx=10)
        f.rect(x, 40 + h * b / tot, 110, h * a / tot, fill=C['coral'], rx=10)
        f.text(x + 55, 30, lab.upper(), 11, C['soft'], 'middle', weight=800)
        pct = 100 * a / tot
        f.text(x + 55, 215, f'{a} : {b}', 15, C['ink'], 'middle', weight=800)
        f.hand(x + 55, 238, f'{pct:.0f}% chance ill' if pct >= 1 else '1% chance ill', 14, C['coral'], 'middle')
        if i < 3:
            f.arrow(x + 114, 115, x + 150, 115, color=C['ink'], sw=2, head=8)
            f.hand(x + 132, 104, '×9', 14, C['ink'], 'middle')
    return f.svg()


def fig_robot():
    f = Fig(640, 230)
    clues = [('start', '1 : 1', None), ('pointy ears', '× 2', 2), ('barks', '× 20', 20), ('lives next door', '× 50', 50), ('wags at Jim', '× 10', 10)]
    odds = 1
    for i, (lab, mult, k) in enumerate(clues):
        x = 25 + i * 122
        if k:
            odds *= k
        f.rect(x, 50, 108, 100, fill=C['blueT'] if i else C['mist'], rx=14)
        f.text(x + 54, 80, lab, 12, C['ink'], 'middle', weight=800)
        f.text(x + 54, 112, mult, 20, C['blue'], 'middle', weight=800)
        f.text(x + 54, 138, f'{odds:,} : 1', 12, C['soft'], 'middle', weight=800)
    f.hand(320, 30, 'each clue multiplies the odds by its strength', 15, C['ink'], 'middle')
    f.hand(320, 200, '20,000 to 1: it’s Bruno', 18, C['coral'], 'middle')
    return f.svg()


def fig_inverse():
    f = Fig(640, 250)
    f.circle(230, 125, 110, stroke=C['blue'], sw=2.5, fill=C['blueT'])
    f.circle(305, 150, 22, stroke=C['coral'], sw=2.5, fill=C['coralT'])
    f.hand(150, 70, 'everyone with headaches', 16, C['blue'])
    f.hand(250, 200, 'serious illness', 14, C['coral'], 'middle')
    f.hand(390, 70, 'most of the red circle is inside\nthe blue one ("most seriously ill\npeople get headaches")...', 14, C['ink'])
    f.hand(390, 170, '...but almost none of the blue\ncircle is red ("almost no headaches\nare serious")', 14, C['ink'])
    return f.svg()


def fig_two_rare():
    f = Fig(640, 210)
    f.text(40, 30, 'TWO RARE STORIES FOR THE SAME TRAGEDY: COMPARE THEM TO EACH OTHER', 11, C['soft'], weight=800)
    for i, (lab, w, col) in enumerate([('explanation 1: very rare', 300, C['blue']), ('explanation 2: even rarer', 120, C['coral'])]):
        y = 55 + i * 60
        f.rect(40, y, w, 40, fill=col, rx=8)
        f.text(50 + w, y + 26, lab, 14, C['ink'], weight=700)
    f.hand(40, 195, 'asking only "how rare is explanation 1?" is the prosecutor’s fallacy', 15, C['coral'])
    return f.svg()


# ---------- Chapter 7 ----------
def coin_class(seed=4):
    rng = np.random.default_rng(seed)
    r1 = rng.binomial(10, 0.5, 100)
    r2 = rng.binomial(10, 0.5, 100)
    worst = np.argsort(r1)[:10]
    best = np.argsort(-r1)[:10]
    return r1, r2, worst, best


def hero7(w=640, h=400):
    f = Fig(w, h)
    g = f.glow(3)
    rng = np.random.default_rng(1)
    skill = rng.normal(0, 1, 260)
    a = skill + rng.normal(0, 1, 260)
    b = skill + rng.normal(0, 1, 260)
    m = mapper(-4, 4, -4, 4, 60, 20, 520, 360)
    for x, y in zip(a, b):
        f.circle(*m(x, y), 3.2, stroke='none', fill='#8f8ad8', op=0.8)
    f.line(*m(-4, -4), *m(4, 4), stroke='#ffffff', sw=1.5, dash='6 6', op=0.6)
    f.line(*m(-4, -2), *m(4, 2), stroke=C['sun'], sw=3.5, filt=g)
    return f.svg()


def fig_coin_class():
    r1, r2, worst, best = coin_class()
    f = Fig(640, 260)
    for p, (grp, title, col) in enumerate([(worst, 'THE 10 WORST "FLIPPERS", TOLD OFF', C['blue']), (best, 'THE 10 BEST, PRAISED', C['coral'])]):
        x0 = 20 + p * 315
        f.rect(x0, 8, 300, 244, fill=C['blueT'] if p == 0 else C['coralT'], rx=16)
        f.text(x0 + 16, 32, title, 11, col, weight=800)
        m = mapper(0, 2, 0, 10, x0 + 40, 50, 230, 150)
        f.line(*m(0, 5), *m(2, 5), stroke=C['ink'], sw=1, dash='4 4')
        for k, i in enumerate(grp):
            dx = 0.05 * (k - 4.5)
            f.line(*m(0.5 + dx, r1[i]), *m(1.5 + dx, r2[i]), stroke=col, sw=1.2, op=0.45)
        for t, arr in ((0.5, r1[grp]), (1.5, r2[grp])):
            f.circle(*m(t, arr.mean()), 9, stroke='#ffffff', sw=2, fill=col)
            f.text(m(t, 0)[0], 222, 'round 1' if t < 1 else 'round 2', 12, C['ink'], 'middle', weight=700)
            f.text(m(t, arr.mean())[0] + 14, m(t, arr.mean())[1] + 5, f'{arr.mean():.1f}', 13, C['ink'], weight=800)
        f.hand(x0 + 150, 244, 'they "improved"!' if p == 0 else 'they "got lazy"!', 14, col, 'middle')
    return f.svg()


def fig_skill_luck():
    f = Fig(640, 230)
    rng = np.random.default_rng(5)
    skill = rng.normal(0, 1, 400)
    luck = rng.normal(0, 1, 400)
    top = np.argsort(-(skill + luck))[:12]
    m = mapper(0, 12, -1, 5.2, 60, 20, 520, 170)
    f.line(*m(0, 0), *m(12, 0), stroke=C['ink'], sw=1.2)
    for k, i in enumerate(top):
        x0, x1 = m(k + 0.15, 0)[0], m(k + 0.85, 0)[0]
        s, l = skill[i], luck[i]
        f.rect(x0, m(0, max(s, 0))[1], x1 - x0, abs(m(0, s)[1] - m(0, 0)[1]), fill=C['teal'], rx=3)
        base = max(s, 0) if l > 0 else min(s, 0) + 0
        y_a, y_b = m(0, s)[1], m(0, s + l)[1]
        f.rect(x0, min(y_a, y_b), x1 - x0, abs(y_b - y_a), fill=C['sun'], rx=3)
    f.hand(430, 40, 'yellow = luck', 15, GOLD)
    f.hand(430, 62, 'green = skill', 15, C['teal'])
    f.hand(320, 222, 'the 12 top scorers: almost all of them were also lucky', 15, C['ink'], 'middle')
    return f.svg()


def fig_scatter():
    f = Fig(640, 320)
    rng = np.random.default_rng(11)
    skill = rng.normal(0, 1, 300)
    a = skill + rng.normal(0, 1, 300)
    b = skill + rng.normal(0, 1, 300)
    f.rect(20, 8, 600, 304, fill='#faf8ff', rx=16, stroke=C['mist'])
    m = mapper(-4, 4, -4, 4, 150, 20, 340, 270)
    f.line(*m(-4, 0), *m(4, 0), stroke=C['mist'], sw=1)
    f.line(*m(0, -4), *m(0, 4), stroke=C['mist'], sw=1)
    for x, y in zip(a, b):
        f.circle(*m(x, y), 3.2, stroke='none', fill=C['violet'], op=0.45)
    f.line(*m(-4, -4), *m(4, 4), stroke=C['ink'], sw=1.6, dash='6 5')
    f.line(*m(-4, -2), *m(4, 2), stroke=C['coral'], sw=3.2)
    f.hand(*m(1.6, 3.6), 'if it were all skill', 14, C['ink'])
    f.hand(*m(2.2, 0.6), 'reality: half of every\ngap from average survives', 14, C['coral'])
    f.text(*m(0, -4.45), 'FIRST TEST →', 11, C['soft'], 'middle', weight=800)
    f.text(m(-4, 0)[0] - 14, m(0, 0)[1], 'SECOND TEST →', 11, C['soft'], 'middle', weight=800, rotate=-90)
    return f.svg()


def fig_galton():
    f = Fig(640, 300)
    rng = np.random.default_rng(3)
    fam = rng.normal(0, 1, 260)
    dad = fam + rng.normal(0, 0.9, 260)
    son = fam + rng.normal(0, 0.9, 260)
    f.rect(20, 8, 600, 284, fill='#faf8ff', rx=16, stroke=C['mist'])
    m = mapper(-3.5, 3.5, -3.5, 3.5, 170, 16, 300, 260)
    for x, y in zip(dad, son):
        f.circle(*m(x, y), 3, stroke='none', fill=C['grey'], op=0.6)
    r = np.corrcoef(dad, son)[0, 1]
    f.line(*m(-3.5, -3.5 * r), *m(3.5, 3.5 * r), stroke=C['coral'], sw=3)
    f.line(*m(-3.5 * r, -3.5), *m(3.5 * r, 3.5), stroke=C['blue'], sw=3)
    f.line(*m(-3.5, -3.5), *m(3.5, 3.5), stroke=C['ink'], sw=1.2, dash='5 5')
    f.hand(40, 60, 'coral: sons of tall\nfathers are tall,\nbut less tall', 14, C['coral'])
    f.hand(480, 200, 'blue: fathers of\ntall sons are tall,\nbut less tall', 14, C['blue'])
    f.text(*m(0, -3.9), "FATHER'S HEIGHT →", 11, C['soft'], 'middle', weight=800)
    f.text(m(-3.5, 0)[0] - 12, m(0, 0)[1], "SON'S HEIGHT →", 11, C['soft'], 'middle', weight=800, rotate=-90)
    return f.svg()


def fig_control():
    f = Fig(640, 230)
    for i, (lab, col) in enumerate([('yelled at', C['blue']), ('left alone', C['teal'])]):
        x0 = 60 + i * 290
        m = mapper(0, 2, 0, 10, x0, 30, 220, 150)
        for t, v in ((0.5, 2.6), (1.5, 5.0)):
            a, b = m(t - 0.3, v), m(t + 0.3, 0)
            f.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=col, rx=6, op=0.55 if t < 1 else 1)
            f.text(m(t, 0)[0], 200, 'before' if t < 1 else 'after', 12, C['ink'], 'middle', weight=700)
            f.text(m(t, v)[0], m(t, v)[1] - 8, f'{v:.1f}', 13, C['ink'], 'middle', weight=800)
        f.text(x0 + 110, 20, lab.upper(), 12, col, 'middle', weight=800)
    f.hand(320, 225, 'both groups "improve" equally, so the yelling did nothing', 15, C['coral'], 'middle')
    return f.svg()


FIGS67 = dict(crowd=fig_crowd, positives=fig_positives, odds=fig_odds, robot=fig_robot, inverse=fig_inverse,
              tworare=fig_two_rare, coinclass=fig_coin_class, skillluck=fig_skill_luck, scatter=fig_scatter,
              galton=fig_galton, control=fig_control)
