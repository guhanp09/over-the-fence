"""Chapter 2 illustrations: vectors wearing costumes."""
import math
import numpy as np
from svgkit import Fig, C, mapper, curve, png_from_array, ramp, wavelength_rgb

TAU = 2 * math.pi


def grid(f, m, xr, yr, col='#e6e3f0'):
    for x in range(xr[0], xr[1] + 1):
        f.line(*m(x, yr[0]), *m(x, yr[1]), stroke=col, sw=1)
    for y in range(yr[0], yr[1] + 1):
        f.line(*m(xr[0], y), *m(xr[1], y), stroke=col, sw=1)


def vec(f, m, a, b, col, sw=3.4, dash=None, head=12):
    f.arrow(*m(*a), *m(*b), color=col, sw=sw, head=head, dash=dash)


def hero_grid(w=640, h=420):
    f = Fig(w, h)
    g = f.glow(3)
    r, hh = np.array([1.0, -0.06]), np.array([0.45, 0.9])
    o = np.array([w / 2 - 40, h / 2 + 40])
    s = 62
    P = lambda a, b: tuple(o + s * (a * r + b * hh) * np.array([1, -1]))
    for a in range(-6, 7):
        f.line(*P(a, -4), *P(a, 4), stroke='#4a44a0', sw=1, op=0.7)
    for b in range(-4, 5):
        f.line(*P(-6, b), *P(6, b), stroke='#4a44a0', sw=1, op=0.7)
    for a in range(-6, 7):
        for b in range(-4, 5):
            f.dot(*P(a, b), 1.8, '#8f8ad8')
    f.poly([P(0, 0), P(3, 0), P(3, 2)], stroke='#ffffff', sw=1.4, dash='5 5', op=0.45)
    f.arrow(*P(0, 0), *P(3, 2), color=C['coral'], sw=5, head=17)
    f.arrow(*P(0, 0), *P(1, 0), color=C['teal'], sw=6, head=16)
    f.arrow(*P(0, 0), *P(0, 1), color=C['sun'], sw=6, head=16)
    f.dot(*P(3, 2), 7, C['coral'])
    f.circle(*P(3, 2), 12, stroke=C['coral'], sw=2, filt=g)
    return f.svg()


def fig_recipes():
    f = Fig(640, 290)
    for i in range(2):
        x0 = 20 + i * 315
        f.rect(x0, 8, 300, 274, fill=C['tealT'] if i == 0 else C['sunT'], rx=16)
        m = mapper(0, 5, 0, 4, x0 + 42, 30, 240, 200)
        grid(f, m, (0, 5), (0, 4), '#ffffff')
        f.text(x0 + 162, 258, 'chilli (tsp) →', 12, C['soft'], 'middle', weight=700)
        f.text(x0 + 24, 130, 'salt (tsp) →', 12, C['soft'], 'middle', weight=700, rotate=-90)
        A, B = (1, 1.5), (2.2, 0.6)
        if i == 0:
            vec(f, m, (0, 0), (2 * A[0], 2 * A[1]), C['teal'], sw=7, head=16)
            vec(f, m, (0, 0), A, C['blue'], sw=3.4)
            f.hand(*m(1.15, 1.1), 'Jim’s recipe', 15, C['blue'])
            f.hand(*m(2.15, 3.2), '× 2: twice as long,\nsame direction', 15, C['teal'])
        else:
            vec(f, m, (0, 0), A, C['blue'])
            vec(f, m, A, (A[0] + B[0], A[1] + B[1]), C['violet'])
            vec(f, m, (0, 0), (A[0] + B[0], A[1] + B[1]), C['coral'], dash='7 6')
            f.hand(*m(0.05, 2.0), 'Jim’s', 15, C['blue'])
            f.hand(*m(2.0, 2.6), '+ his brother’s', 15, C['violet'])
            f.hand(*m(1.8, 0.45), 'the shopping list', 15, C['coral'])
    return f.svg()


def fig_span():
    f = Fig(640, 300)
    o = np.array([230.0, 215.0])
    ex, ey, ez = np.array([150.0, 0]), np.array([95.0, -58.0]), np.array([0, -150.0])
    P = lambda a, b, c=0: tuple(o + a * ex + b * ey + c * ez)
    f.poly([P(-0.3, -0.4), P(1.7, -0.4), P(1.7, 1.6), P(-0.3, 1.6)], stroke=C['teal'], sw=1.2,
           fill=C['teal'], fop=0.16, close=True)
    for a in np.arange(-0.3, 1.71, 0.5):
        f.line(*P(a, -0.4), *P(a, 1.6), stroke=C['teal'], sw=0.8, op=0.4)
    for b in np.arange(-0.4, 1.61, 0.5):
        f.line(*P(-0.3, b), *P(1.7, b), stroke=C['teal'], sw=0.8, op=0.4)
    f.arrow(*P(0, 0, 0), *P(1, 0, 0), color=C['teal'], sw=4, head=13)
    f.arrow(*P(0, 0, 0), *P(0, 1, 0), color=C['blue'], sw=4, head=13)
    f.arrow(*P(0, 0, 0), *P(1.2, 1.0, 0), color=C['sun'], sw=4, head=13)
    f.poly([P(1.2, 0, 0), P(1.2, 1.0, 0), P(0, 1.0, 0)], stroke=C['soft'], sw=1, dash='3 4')
    f.arrow(*P(0, 0, 0), *P(0, 0, 1.15), color=C['coral'], sw=4.5, head=14)
    f.dot(*P(0, 0, 0), 5, C['ink'])
    f.hand(*P(1.02, -0.2, 0), 'cumin', 16, C['teal'])
    f.hand(*P(-0.15, 1.12, 0), 'coriander', 16, C['blue'], anchor='end')
    f.hand(500, 122, 'garam masala:\nlies flat in the sheet', 15, C['ink'], 'end')
    f.hand(*P(0.08, 0, 1.12), 'salt: sticks out of it', 16, C['coral'])
    f.hand(430, 285, 'the sheet = everything you can mix from cumin & coriander', 13, C['soft'], 'middle')
    return f.svg()


def cone(wl, peak, width):
    return np.exp(-0.5 * ((wl - peak) / width) ** 2)


CONES = [(565, 48, C['coral'], 'L'), (535, 42, C['teal'], 'M'), (442, 24, C['blue'], 'S')]


def cone_matrix(wls):
    return np.array([cone(np.asarray(wls, float), p, w) for p, w, _, _ in CONES])


def spectrum_strip(f, m, y, h):
    for wl in range(400, 700, 3):
        a, _ = m(wl, 0)
        b, _ = m(wl + 3, 0)
        f.rect(a, y, b - a + 0.5, h, fill=wavelength_rgb(wl))


def fig_cones():
    f = Fig(640, 250)
    wl = np.linspace(400, 700, 400)
    m = mapper(400, 700, 0, 1.1, 50, 20, 560, 170)
    for p, w, col, nm in CONES:
        y = cone(wl, p, w)
        f.poly([m(400, 0)] + curve(m, wl, y) + [m(700, 0)], stroke='none', fill=col, op=0.14, close=True)
        f.poly(curve(m, wl, y), stroke=col, sw=3)
        f.text(*m(p, 1.03), nm, 16, col, 'middle', weight=800)
    spectrum_strip(f, m, 196, 14)
    for t in (400, 500, 600, 700):
        f.text(m(t, 0)[0], 228, f'{t} nm', 11, C['soft'], 'middle', weight=600)
    f.hand(610, 70, 'three kinds of\ncone = three\nnumbers', 14, C['ink'], 'end')
    return f.svg()


def fig_metamers():
    f = Fig(640, 300)
    wl = np.linspace(400, 700, 601)
    dw = wl[1] - wl[0]
    target = np.exp(-0.5 * ((wl - 585) / 55) ** 2)
    M = cone_matrix(wl)
    resp = M @ target * dw
    spikes = [615, 540, 465]
    A = cone_matrix(spikes)
    w = np.linalg.solve(A, resp)
    swatch = '#f3a83b'
    for i in range(2):
        x0 = 20 + i * 330
        f.rect(x0, 8, 290, 284, fill='#faf8ff', rx=16, stroke=C['mist'])
        m = mapper(400, 700, 0, 1.15, x0 + 20, 30, 250, 130)
        f.line(*m(400, 0), *m(700, 0), stroke=C['ink'], sw=1)
        spectrum_strip(f, m, 166, 8)
        if i == 0:
            f.poly([m(400, 0)] + curve(m, wl, target) + [m(700, 0)], stroke=C['ink'], sw=2, fill=swatch, fop=0.5, close=True)
            f.text(x0 + 20, 24, 'A SMOOTH, BROAD GLOW', 12, C['soft'], weight=800)
        else:
            top = max(w)
            for s, ww in zip(spikes, w):
                f.rect(m(s, 0)[0] - 4, m(0, ww / top)[1], 8, m(0, 0)[1] - m(0, ww / top)[1], fill=wavelength_rgb(s), rx=2)
            f.text(x0 + 20, 24, 'THREE NARROW SPIKES', 12, C['soft'], weight=800)
        f.rect(x0 + 20, 190, 70, 70, fill=swatch, rx=35)
        f.hand(x0 + 55, 282, 'looks like this', 13, C['soft'], 'middle')
        for j, (p, ww, col, nm) in enumerate(CONES):
            bx = x0 + 120 + j * 50
            hgt = resp[j] / resp.max() * 70
            f.rect(bx, 260 - hgt, 30, hgt, fill=col, rx=4)
            f.text(bx + 15, 278, nm, 12, col, 'middle', weight=800)
    f.text(320, 150, '=', 40, C['ink'], 'middle', weight=800)
    f.hand(320, 185, 'same three\nnumbers', 13, C['ink'], 'middle')
    return f.svg()


def fig_tweaks():
    f = Fig(640, 280)
    f.rect(20, 8, 600, 264, fill=C['coralT'], rx=16)
    m = mapper(-1, 5, 0, 4, 60, 24, 420, 210)
    grid(f, m, (0, 5), (0, 4), '#ffffff')
    a, b = m(-1, 0), m(0, 4)
    f.rect(a[0], b[1], b[0] - a[0], a[1] - b[1], fill=C['grey'], op=0.18)
    f.hand(*m(-0.95, 3.4), 'minus\nonions?', 13, C['soft'])
    J, H = (3, 1), (1, 2)
    vec(f, m, J, H, C['coral'], sw=4)
    f.dot(*m(*J), 8, C['blue'])
    f.dot(*m(*H), 8, C['violet'])
    f.hand(m(*J)[0] + 12, m(*J)[1] + 18, 'Jim’s recipe', 15, C['blue'])
    f.hand(m(*H)[0] - 12, m(*H)[1] - 14, 'her recipe', 15, C['violet'], 'end')
    f.hand(*m(2.3, 1.9), 'the tweak:\n−2 onions, +1 chilli', 15, C['coral'])
    K = (4.6, 2.5)
    vec(f, m, K, (K[0] - 2, K[1] + 1), C['coral'], sw=2.5, dash='6 5')
    f.dot(*m(*K), 6, C['ink'])
    f.hand(*m(3.15, 3.75), 'the same tweak,\nanywhere', 14, C['coral'])
    f.text(*m(2.5, -0.55), 'onions →', 12, C['soft'], 'middle', weight=700)
    f.text(500, 120, 'recipes are\nPLACES.\n\ntweaks are\nJOURNEYS.', 14, C['ink'], weight=800)
    return f.svg()


def fig_negred():
    f = Fig(640, 270)
    wl = np.linspace(400, 700, 301)
    P = cone_matrix([700, 546.1, 435.8])
    rgb = np.linalg.solve(P, cone_matrix(wl))
    rgb = rgb / rgb.max()
    m = mapper(400, 700, -0.75, 1.05, 50, 20, 560, 185)
    f.line(*m(400, 0), *m(700, 0), stroke=C['ink'], sw=1.2)
    r = rgb[0]
    neg = np.minimum(r, 0)
    f.poly([m(400, 0)] + curve(m, wl, neg) + [m(700, 0)], stroke='none', fill=C['coral'], op=0.35, close=True)
    for row, col, nm in zip(rgb, [C['coral'], C['teal'], C['blue']], ['red', 'green', 'blue']):
        f.poly(curve(m, wl, row), stroke=col, sw=2.8)
        k = int(np.argmax(row))
        f.text(*m(wl[k], row[k] + 0.07), nm, 13, col, 'middle', weight=800)
    spectrum_strip(f, m, 216, 10)
    k = int(np.argmin(r))
    f.hand(*m(wl[k] + 25, r[k] - 0.02), '← negative red!', 17, C['coral'])
    f.text(50, 248, 'THE PURE COLOUR BEING MATCHED →', 11, C['soft'], weight=700)
    return f.svg()


def fig_antinoise():
    f = Fig(640, 270)
    x = np.linspace(0, 1, 900)
    noise = 0.7 * np.sin(TAU * 3 * x) + 0.4 * np.sin(TAU * 7 * x + 1) + 0.25 * np.sin(TAU * 13 * x + 2)
    rows = [(noise, C['ink'], 'the drone of the plane'), (-noise, C['coral'], 'the anti-drone, played by the headphones'),
            (0 * noise, C['teal'], 'what reaches your ear')]
    for i, (ys, col, lab) in enumerate(rows):
        y = 50 + i * 85
        if i == 2:
            f.rect(55, y - 38, 570, 70, fill=C['tealT'], rx=12)
        f.line(70, y, 610, y, stroke=C['mist'], sw=1)
        f.poly([(70 + a * 540, y - b * 26) for a, b in zip(x, ys)], stroke=col, sw=2.6)
        f.text(70, y - 30 if i < 2 else y - 14, lab.upper(), 11, col, weight=800)
        if i < 2:
            f.text(35, y + 50, '+' if i == 0 else '=', 20, C['soft'], 'middle', weight=800)
    f.hand(470, 205, 'silence', 18, C['teal'])
    return f.svg()


def basis_rh():
    v = np.array([3.0, 1.0])
    th = math.atan2(1, 3) - math.acos(2.9375 / math.hypot(3, 1))
    r = np.array([math.cos(th), math.sin(th)])
    h = (v - 2 * r) / 1.5
    return v, r, h


def fig_bases():
    f = Fig(640, 280)
    v, r, h = basis_rh()
    for i in range(2):
        x0 = 20 + i * 315
        f.rect(x0, 8, 300, 264, fill=C['blueT'] if i == 0 else C['tealT'], rx=16)
        o = np.array([x0 + 40.0, 220.0])
        s = 55
        P = lambda p: tuple(o + s * np.asarray(p) * np.array([1, -1]))
        if i == 0:
            for a in range(0, 5):
                f.line(*P((a, -0.2)), *P((a, 2.8)), stroke='#ffffff', sw=1.2)
            for b in range(0, 3):
                f.line(*P((-0.2, b)), *P((4.1, b)), stroke='#ffffff', sw=1.2)
            f.arrow(*P((0, 0)), *P((3, 0)), color=C['blue'], sw=2.4, dash='6 5')
            f.arrow(*P((3, 0)), *P((3, 1)), color=C['blue'], sw=2.4, dash='6 5')
            f.hand(*P((0.9, -0.35)), '3 east', 15, C['blue'])
            f.hand(*P((3.1, 0.5)), '1 north', 15, C['blue'])
            f.text(x0 + 18, 30, 'THE PHONE’S LANGUAGE', 12, C['blue'], weight=800)
        else:
            for a in range(0, 4):
                f.line(*P(a * r - 0.3 * h), *P(a * r + 2.2 * h), stroke='#ffffff', sw=1.2)
            for b in range(0, 3):
                f.line(*P(-0.2 * r + b * h), *P(3.3 * r + b * h), stroke='#ffffff', sw=1.2)
            f.arrow(*P((0, 0)), *P(2 * r), color=C['teal'], sw=2.4, dash='6 5')
            f.arrow(*P(2 * r), *P(v), color=C['teal'], sw=2.4, dash='6 5')
            f.hand(*P(0.8 * r - 0.35 * h), '2 along the river', 15, C['teal'])
            f.hand(*P(2 * r + 0.95 * h + 0.25 * r), '1.5 up\nthe hill', 15, C['teal'])
            f.text(x0 + 18, 30, 'THE SHOPKEEPER’S LANGUAGE', 12, C['teal'], weight=800)
        f.arrow(*P((0, 0)), *P(v), color=C['coral'], sw=4.4, head=14)
        f.dot(*P((0, 0)), 5, C['ink'])
        f.hand(*P(v + np.array([-0.2, 0.35])), 'takeaway', 15, C['coral'])
    return f.svg()


def fig_languages():
    f = Fig(640, 270)
    f.rect(20, 8, 360, 254, fill=C['sunT'], rx=16)
    f.rect(400, 8, 220, 254, fill=C['violetT'], rx=16)
    xs = np.linspace(0, 1, 110)
    ys = (np.sin(TAU * 4 * xs) + np.sin(TAU * 5 * xs) + np.sin(TAU * 6 * xs)) / 3
    m = mapper(0, 1, -1.1, 1.1, 40, 50, 320, 170)
    f.line(*m(0, 0), *m(1, 0), stroke=C['grey'], sw=1)
    for a, b in zip(xs, ys):
        f.line(*m(a, 0), *m(a, b), stroke=C['sun'], sw=1.4)
        f.dot(*m(a, b), 2.4, C['ink'])
    f.text(40, 34, 'MOMENT BY MOMENT', 12, C['ink'], weight=800)
    f.hand(200, 250, '110 numbers (a CD uses 44,100 a second)', 13, C['soft'], 'middle')
    m2 = mapper(0, 9, 0, 1.2, 420, 50, 180, 170)
    f.line(*m2(0, 0), *m2(9, 0), stroke=C['ink'], sw=1)
    for k in range(1, 9):
        a = 1.0 if k in (4, 5, 6) else 0
        x, y = m2(k, a)
        _, y0 = m2(k, 0)
        if a:
            f.rect(x - 7, y, 14, y0 - y, fill=C['violet'], rx=3)
        else:
            f.dot(x, y0, 2.5, C['grey'])
        f.text(x, y0 + 16, str(k), 10, C['soft'], 'middle', weight=700)
    f.text(420, 34, 'HAND BY HAND', 12, C['ink'], weight=800)
    f.hand(510, 257, '3 numbers', 14, C['violet'], 'middle')
    return f.svg()


def fig_shadows():
    f = Fig(640, 262)
    for i in range(2):
        x0 = 20 + i * 315
        f.rect(x0, 8, 300, 246, fill='#faf8ff', rx=16, stroke=C['mist'])
        o = np.array([x0 + 36.0, 190.0])
        s = 62
        P = lambda p: tuple(o + s * np.asarray(p, float) * np.array([1, -1]))
        if i == 0:
            v = np.array([3.0, 1.6])
            f.line(*P((0, 0)), *P((4.1, 0)), stroke=C['ink'], sw=1.6)
            f.line(*P((0, 0)), *P((0, 2.2)), stroke=C['ink'], sw=1.6)
            f.line(*P(v), *P((v[0], 0)), stroke=C['sun'], sw=1.6, dash='4 4')
            f.line(*P((0, 0.04)), *P((v[0], 0.04)), stroke=C['blue'], sw=6, op=0.8)
            f.hand(*P((0.6, -0.45)), 'shadow = the true amount', 14, C['blue'])
            f.text(x0 + 18, 30, 'AT RIGHT ANGLES', 12, C['teal'], weight=800)
        else:
            v0, r, h = basis_rh()
            ang = -math.atan2(r[1], r[0])
            R = np.array([[math.cos(ang), -math.sin(ang)], [math.sin(ang), math.cos(ang)]])
            v, hh = R @ v0 * 0.85, R @ h * 0.85
            f.line(*P((0, 0)), *P((4.1, 0)), stroke=C['ink'], sw=1.6)
            f.line(*P((0, 0)), *P(hh * 1.9), stroke=C['ink'], sw=1.6)
            f.text(*P((4.1, -0.3)), 'river', 12, C['soft'], 'end', weight=700)
            f.text(*P(hh * 1.9 + np.array([0.1, 0.05])), 'hill', 12, C['soft'], weight=700)
            true_r = v - 1.5 * hh
            f.line(*P(v), *P(true_r), stroke=C['teal'], sw=1.6, dash='4 4')
            f.line(*P(v), *P((v[0], 0)), stroke=C['sun'], sw=1.6, dash='4 4')
            f.line(*P((0, 0.1)), *P((v[0], 0.1)), stroke=C['blue'], sw=6, op=0.8)
            f.line(*P((0, -0.05)), *P((true_r[0], -0.05)), stroke=C['teal'], sw=6, op=0.9)
            f.hand(*P((0.0, -0.5)), 'true amount: 2', 14, C['teal'])
            f.hand(*P((1.55, -0.5)), 'shadow: 2.9, too long!', 14, C['blue'])
            f.text(x0 + 18, 30, 'SLANTED', 12, C['coral'], weight=800)
        f.arrow(*P((0, 0)), *P(v), color=C['coral'], sw=4, head=13)
        f.dot(*P((0, 0)), 5, C['ink'])
    return f.svg()


def dct_basis(N=8):
    n = np.arange(N)
    B = np.array([np.cos(math.pi * (2 * n + 1) * k / (2 * N)) for k in range(N)])
    B[0] /= math.sqrt(2)
    return B * math.sqrt(2 / N)


def fig_dct():
    B = dct_basis()
    cell, gap = 9, 6
    size = 8 * (8 * cell + gap) + gap
    img = np.ones((size, size, 3)) * np.array([1, 0.992, 0.973])
    for u in range(8):
        for v in range(8):
            pat = np.outer(B[u], B[v])
            pat = pat / (np.abs(pat).max() or 1)
            rgb = ramp((pat + 1) / 2, [C['night'], C['violet'], '#fff6e6'])
            big = np.kron(rgb, np.ones((cell, cell, 1)))
            y, x = gap + u * (8 * cell + gap), gap + v * (8 * cell + gap)
            img[y:y + 8 * cell, x:x + 8 * cell] = big
    f = Fig(640, 470)
    f.image(20, 10, 450, 450, png_from_array(img))
    f.hand(485, 60, '← slow & smooth:\nthe patterns\nthat carry\nmost of a photo', 15, C['teal'])
    f.hand(485, 380, '← fast & fine:\nsharp edges\nand texture', 15, C['coral'])
    return f.svg()


def fig_compression():
    from PIL import Image
    import matplotlib.cbook as cb
    from scipy.fft import dctn, idctn
    im = Image.open(cb.get_sample_data('grace_hopper.jpg', asfileobj=False)).convert('L')
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, 0, (w - s) // 2 + s, s)).resize((256, 256), Image.LANCZOS)
    a = np.asarray(im, float) / 255
    f = Fig(640, 205)
    for i, K in enumerate([1, 3, 10, 64]):
        out = np.zeros_like(a)
        for y in range(0, 256, 8):
            for x in range(0, 256, 8):
                c = dctn(a[y:y + 8, x:x + 8], norm='ortho')
                if K < 64:
                    thr = np.sort(np.abs(c).ravel())[-K]
                    c = np.where(np.abs(c) >= thr, c, 0)
                out[y:y + 8, x:x + 8] = idctn(c, norm='ortho')
        rgb = np.repeat(np.clip(out, 0, 1)[..., None], 3, axis=2)
        x0 = 20 + i * 152
        f.image(x0, 8, 144, 144, png_from_array(rgb))
        f.text(x0 + 72, 172, 'the original: 64' if K == 64 else f'{K} of 64', 13, C['ink'], 'middle', weight=800)
        f.hand(x0 + 72, 195, ['a mosaic', 'recognisable', 'nearly perfect', 'every number'][i], 14, C['soft'], 'middle')
    return f.svg()


FIGS2 = dict(recipes=fig_recipes, span=fig_span, cones=fig_cones, metamers=fig_metamers, tweaks=fig_tweaks,
             negred=fig_negred, antinoise=fig_antinoise, bases=fig_bases, languages=fig_languages,
             shadows=fig_shadows, dct=fig_dct, compression=fig_compression)
