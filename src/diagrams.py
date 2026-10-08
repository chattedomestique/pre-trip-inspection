"""Diagram library. Every diagram is a 360x140 SVG. Context shapes (class b / bl / tire ...) sit in .ctx and stay faded.
Parts are <g class="part" data-id="..."> groups. A line on the sheet names the part ids it highlights."""
import math

def _a(**k):
    return ''.join(f' {a.replace("_","-")}="{v}"' for a, v in k.items())

def R(x, y, w, h, rx=0, c='p'):
    return f'<rect class="{c}" x="{x}" y="{y}" width="{w}" height="{h}"' + (f' rx="{rx}"' if rx else '') + '/>'

def C(cx, cy, r, c='p'):
    return f'<circle class="{c}" cx="{cx}" cy="{cy}" r="{r}"/>'

def L(x1, y1, x2, y2, c='l'):
    return f'<line class="{c}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'

def P(pts, c='p'):
    return f'<polygon class="{c}" points="{pts}"/>'

def D(d, c='s', extra=''):
    return f'<path class="{c}" d="{d}"{extra}/>'

def T(x, y, txt, anchor='start', c='lbl'):
    return f'<text class="{c}" x="{x}" y="{y}" text-anchor="{anchor}">{txt}</text>'

def part(pid, *shapes, halo=True):
    h = '' if halo else ' data-halo="none"'
    return f'<g class="part" data-id="{pid}"{h}>' + ''.join(shapes) + '</g>'

def ctx(*shapes):
    return '<g class="ctx">' + ''.join(shapes) + '</g>'

def octagon(cx, cy, r=9):
    pts = []
    for k in range(8):
        a = math.radians(45 * k + 22.5)
        pts.append('%.1f,%.1f' % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return ' '.join(pts)

def annulus(cx, cy, r1, r2):
    # ring between r1 (outer) and r2 (inner), even-odd fill
    return (f'<path class="p" fill-rule="evenodd" d="M{cx-r1} {cy}a{r1} {r1} 0 1 0 {2*r1} 0a{r1} {r1} 0 1 0 {-2*r1} 0Z'
            f'M{cx-r2} {cy}a{r2} {r2} 0 1 0 {2*r2} 0a{r2} {r2} 0 1 0 {-2*r2} 0Z"/>')

def wheel_ctx(cx, cy, r=17):
    return (C(cx, cy, r, 'tire') + C(cx, cy, r * .41, 'hub') + C(cx, cy, 2, 'axle'))

def svg(inner, label):
    return (f'<svg class="dia" viewBox="0 0 360 140" role="img" aria-label="{label}">'
            + inner + '<g class="halos"></g><g class="hits"></g></svg>')

DIA = {}
LABEL = {}

# ------------------------------------------------------------------ side, driver (front on the left)
def side_driver():
    win = ''.join(R(100 + 30 * i, 32, 24, 20, 2) for i in range(8))
    s = ctx(
        '<line class="gl" x1="4" y1="120.5" x2="356" y2="120.5"/>',
        '<path class="b" d="M12 96 V64 Q12 54 22 54 H78 L93 20 H338 Q352 20 352 32 V96 Z"/>',
        wheel_ctx(52, 103), C(287, 103, 17, 'tire'), wheel_ctx(279, 103),
    )
    s += part('win', win, halo=False)
    s += part('tape', R(14, 57, 336, 3), R(14, 83, 336, 3), halo=False)
    s += part('clr', R(102, 22, 14, 6, 1), R(206, 22, 14, 6, 1), R(322, 22, 14, 6, 1))
    s += part('tape', C(100, 91, 3.5), C(222, 91, 3.5), C(334, 91, 3.5))
    s += part('brk', R(88, 63, 14, 16, 1), L(91, 68, 99, 68), L(91, 73, 99, 73))
    s += part('stop1', P(octagon(140, 71)), L(135, 71, 145, 71))
    s += part('stop2', P(octagon(300, 71)), L(295, 71, 305, 71))
    s += part('turn', C(20, 71, 4), C(222, 71, 4), C(344, 66, 4))
    s += part('rev', R(340, 74, 8, 8, 1))
    s += part('batt', R(150, 98, 52, 14, 1), L(167, 98, 167, 112), L(185, 98, 185, 112))
    s += part('tail', R(314, 99, 22, 6), C(338, 102, 5), C(338, 102, 2, 'l'))
    s += T(12, 136, 'Front') + T(352, 136, 'Rear', 'end')
    return s
DIA['side-driver'] = svg(side_driver(), 'Driver side of the bus, front on the left')

# ------------------------------------------------------------------ side, door (front on the right)
def side_door():
    win = ''.join(R(34 + 30 * i, 32, 24, 20, 2) for i in range(6)) + R(222, 32, 24, 20, 2)
    s = ctx(
        '<line class="gl" x1="4" y1="120.5" x2="356" y2="120.5"/>',
        '<path class="b" d="M348 96 V64 Q348 54 338 54 H282 L267 20 H22 Q8 20 8 32 V96 Z"/>',
        wheel_ctx(308, 103), C(73, 103, 17, 'tire'), wheel_ctx(81, 103),
    )
    s += part('door', R(256, 58, 24, 52, 2), L(268, 58, 268, 110))
    s += part('win', win, halo=False)
    s += part('tape', R(10, 57, 236, 3), R(10, 83, 336, 3), halo=False)
    s += part('clr', R(24, 22, 14, 6, 1), R(140, 22, 14, 6, 1), R(244, 22, 14, 6, 1))
    s += part('refl', C(24, 91, 3.5), C(130, 91, 3.5), C(246, 91, 3.5))
    s += part('turn', C(340, 71, 4), C(140, 71, 4), C(16, 66, 4))
    s += part('rev', R(12, 74, 8, 8, 1))
    s += part('fueldoor', R(100, 62, 20, 14, 2), C(110, 69, 3, 'l'))
    s += part('tank', R(112, 98, 78, 16, 3), L(128, 98, 128, 114), L(150, 98, 150, 114), L(172, 98, 172, 114))
    s += part('def', R(200, 64, 18, 12, 2), C(209, 70, 2.5, 'l'))
    s += T(348, 136, 'Front', 'end') + T(12, 136, 'Rear')
    return s
DIA['side-door'] = svg(side_door(), 'Door side of the bus, front on the right')

# ------------------------------------------------------------------ front (door side is on the left of the picture)
def front():
    s = ctx(
        '<line class="gl" x1="30" y1="126.5" x2="330" y2="126.5"/>',
        '<path class="b" d="M76 116 V30 Q76 12 94 12 H266 Q284 12 284 30 V116 Z"/>',
        R(134, 78, 92, 40, 4, 'b'),
        R(76, 104, 208, 12, 2, 'b'),
        R(66, 98, 18, 26, 3, 'tire'), R(276, 98, 18, 26, 3, 'tire'),
    )
    s += part('clr', *[R(98 + 36 * i, 14, 16, 6, 1) for i in range(5)])
    s += part('red', C(100, 31, 6), C(260, 31, 6)) if False else ''
    s += part('amber', C(100, 31, 6), C(260, 31, 6))
    s += part('red', C(124, 31, 6), C(236, 31, 6))
    s += part('wind', R(90, 42, 80, 34, 3), R(190, 42, 80, 34, 3), halo=True)
    s += part('head', C(116, 92, 7), C(244, 92, 7))
    s += part('turn', R(92, 88, 12, 8, 2), R(256, 88, 12, 8, 2))
    s += part('tape', R(76, 108, 208, 4), halo=False)
    s += part('level', R(46, 123, 268, 3))
    s += part('mirdoor', R(56, 36, 10, 26, 2), C(58, 82, 7), L(66, 48, 76, 48))
    s += part('mirdrv', R(294, 36, 10, 26, 2), C(302, 82, 7), L(284, 48, 294, 48))
    s += T(12, 139, 'Door side') + T(348, 139, 'Driver side', 'end')
    return s
DIA['front'] = svg(front(), 'Front of the bus. The door side is on the left of the picture, the driver side on the right.')

# ------------------------------------------------------------------ rear (driver side is on the left of the picture)
def rear():
    s = ctx(
        '<line class="gl" x1="30" y1="126.5" x2="330" y2="126.5"/>',
        '<path class="b" d="M70 114 V30 Q70 12 88 12 H272 Q290 12 290 30 V114 Z"/>',
        R(76, 110, 208, 6, 1, 'b'),
        R(72, 108, 22, 18, 3, 'tire'), R(266, 108, 22, 18, 3, 'tire'),
    )
    s += part('clr', *[R(98 + 40 * i, 14, 16, 6, 1) for i in range(5)])
    s += part('amber', C(84, 30, 5), C(276, 30, 5))
    s += part('red', C(104, 30, 5), C(256, 30, 5))
    s += part('door', R(126, 38, 108, 72, 3), L(180, 38, 180, 110), R(168, 76, 5, 10, 1, 'l'))
    s += part('win', R(134, 46, 38, 24, 2), R(188, 46, 38, 24, 2))
    s += part('tail', C(86, 46, 6), C(274, 46, 6))
    s += part('brake', C(86, 60, 5), C(274, 60, 5))
    s += part('turn', C(86, 74, 5), C(274, 74, 5))
    s += part('rev', C(86, 88, 5), C(274, 88, 5))
    s += part('tape', R(76, 102, 46, 4), R(238, 102, 46, 4), halo=False)
    s += part('plate', R(158, 92, 44, 14, 2), R(170, 87, 20, 4, 1))
    s += part('refl', C(80, 96, 3.5), C(280, 96, 3.5))
    s += part('step', R(112, 116, 136, 7, 1))
    s += T(12, 139, 'Driver side') + T(348, 139, 'Door side', 'end')
    return s
DIA['rear'] = svg(rear(), 'Rear of the bus. The driver side is on the left of the picture, the door side on the right.')

# ------------------------------------------------------------------ dash (driver view, instrument cluster)
def dash():
    s = ctx(
        '<path class="b" d="M6 14 H354 V62 H6 Z"/>',
        '<path class="b" d="M6 64 H354 V138 H6 Z"/>',
    )
    g = [('trans', 24, 13), ('water', 54, 13), ('oil', 84, 13), ('def', 114, 13)]
    for pid, x, r in g:
        s += part(pid, C(x, 38, r), L(x, 38, x + 6, 32))
    s += part('tach', C(156, 38, 19), L(156, 38, 166, 28))
    s += part('speed', C(208, 38, 19), L(208, 38, 198, 28))
    s += part('fuel', C(248, 38, 13), L(248, 38, 254, 32))
    s += part('volt', C(278, 38, 13), L(278, 38, 284, 32))
    s += part('air', C(308, 38, 13), L(308, 38, 314, 32), C(336, 38, 13), L(336, 38, 342, 32))
    s += part('wheel', C(66, 104, 28), C(66, 104, 7, 'l'), L(38, 104, 59, 104, 'l'), L(73, 104, 94, 104, 'l'))
    s += part('sbrake', R(120, 106, 34, 14, 3), L(124, 112, 150, 112, 'l'))
    s += part('key', C(186, 82, 8), L(186, 78, 186, 86, 'l'))
    s += part('abs', R(206, 74, 24, 15, 3), L(212, 82, 224, 82, 'l'))
    s += part('backup', R(238, 74, 24, 15, 3), C(250, 82, 3.5, 'l'))
    s += part('lamp', R(270, 74, 16, 15, 3), L(278, 77, 278, 86, 'l'))
    s += part('pbrake', P('312,70 322,82 312,94 302,82'))
    s += part('shift', L(338, 124, 338, 96, 's'), C(338, 90, 6))
    return s
DIA['dash'] = svg(dash(), 'Dashboard gauges, ignition, lights, brake pedal and shift lever')

# ------------------------------------------------------------------ cab (driver view through the windshield, driver side on the left)
def cab():
    s = ctx(
        '<path class="b" d="M44 6 H316 V76 H44 Z"/>',
        '<path class="b" d="M6 78 H354 V138 H6 Z"/>',
        L(180, 6, 180, 76, 'bl'),
    )
    s += part('wind', R(52, 12, 120, 58, 2), R(188, 12, 120, 58, 2), halo=False)
    s += part('wipers', L(80, 70, 144, 40, 's'), L(220, 70, 284, 40, 's'))
    s += part('mirtop', R(16, 10, 16, 30, 2), R(328, 10, 16, 30, 2))
    s += part('mirlow', R(16, 44, 16, 24, 2), R(328, 44, 16, 24, 2))
    s += part('mircross', C(24, 88, 8), C(336, 88, 8))
    s += part('mirin', R(158, 4, 44, 12, 2))
    s += part('defrost', R(76, 80, 208, 6, 2))
    s += part('fans', C(52, 100, 7), L(46, 100, 58, 100, 'l'), C(308, 100, 7), L(302, 100, 314, 100, 'l'))
    s += part('wheel', C(120, 112, 24), C(120, 112, 6, 'l'), halo=False)
    s += part('horn', C(120, 112, 9))
    s += part('lever', L(98, 106, 76, 100, 's'), C(74, 100, 4))
    s += part('sw_wiper', R(168, 96, 16, 14, 2), L(176, 99, 176, 107, 'l'))
    s += part('sw_heat', R(188, 96, 16, 14, 2), L(196, 99, 196, 107, 'l'))
    s += part('sw_strobe', R(208, 96, 16, 14, 2), L(216, 99, 216, 107, 'l'))
    s += part('sw_int', R(228, 96, 16, 14, 2), L(236, 99, 236, 107, 'l'))
    s += part('sw_noise', R(248, 96, 24, 14, 2), C(260, 103, 3.5, 'l'))
    s += part('doorlev', L(296, 128, 280, 112, 's'), C(278, 110, 5))
    s += part('stair', R(318, 112, 30, 22, 2), L(324, 118, 342, 118, 'l'), L(324, 124, 342, 124, 'l'))
    return s
DIA['cab'] = svg(cab(), 'The driver\'s view: windshield, mirrors, steering wheel and the switch panel')

# ------------------------------------------------------------------ plan (top down, front on the left, door side at the top)
def plan():
    s = ctx(
        '<rect class="b" x="30" y="22" width="322" height="96" rx="8"/>',
    )
    s += part('aisle', R(64, 64, 280, 12, 0))
    # seats: 9 per side, back (thin, forward edge) and bottom
    backs_t, bots_t, backs_b, bots_b = [], [], [], []
    for i in range(8):
        x = 78 + 30 * i
        backs_t.append(R(x, 32, 4, 26, 1)); bots_t.append(R(x + 5, 34, 18, 22, 2))
        backs_b.append(R(x, 82, 4, 26, 1)); bots_b.append(R(x + 5, 84, 18, 22, 2))
    s += part('seatbacks', *backs_t, *backs_b, halo=False)
    s += part('seatbottoms', *bots_t, *bots_b, halo=False)
    s += part('win', *[R(78 + 30 * i, 18, 22, 4, 1) for i in (0, 1, 3, 4, 6, 7)], *[R(78 + 30 * i, 118, 22, 4, 1) for i in (0, 1, 3, 4, 6, 7)], halo=False)
    s += part('sidewin', R(168, 15, 52, 7, 1), R(258, 15, 52, 7, 1), R(168, 118, 52, 7, 1), R(258, 118, 52, 7, 1))
    s += part('hatch1', R(112, 62, 30, 16, 2), L(116, 70, 138, 70, 'l'))
    s += part('hatch2', R(222, 62, 30, 16, 2), L(226, 70, 248, 70, 'l'), C(237, 70, 3, 'l'))
    s += part('heatr', R(322, 50, 20, 9, 1), R(322, 81, 20, 9, 1))
    s += part('exit', R(348, 50, 8, 40, 1), L(352, 52, 352, 88, 'l'))
    s += part('driverseat', R(42, 84, 20, 22, 3), C(52, 95, 6, 'l'))
    s += part('door', R(34, 16, 26, 8, 1))
    s += part('stair', R(36, 26, 26, 34, 1))
    s += T(12, 136, 'Front') + T(352, 136, 'Rear', 'end')
    return s
DIA['plan'] = svg(plan(), 'Inside the bus from above, front on the left and the door side at the top')

# ------------------------------------------------------------------ entry (door, handrails, steps)
def entry():
    s = ctx(
        R(96, 8, 168, 126, 4, 'b'),
        R(108, 16, 144, 10, 2, 'b'),
    )
    s += part('hinge', R(104, 34, 6, 10, 1), R(104, 62, 6, 10, 1), R(250, 34, 6, 10, 1), R(250, 62, 6, 10, 1))
    s += part('glass', R(114, 32, 62, 48, 3), R(184, 32, 62, 48, 3))
    s += part('seal', R(177, 30, 6, 52, 1))
    s += part('lights', R(126, 14, 24, 8, 2), R(210, 14, 24, 8, 2))
    s += part('rail', R(112, 68, 7, 64, 3), R(241, 68, 7, 64, 3))
    s += part('step', R(124, 90, 112, 10, 1), R(124, 104, 112, 10, 1), R(124, 118, 112, 10, 1))
    s += part('tread', R(128, 92, 104, 3, 1), R(128, 106, 104, 3, 1), R(128, 120, 104, 3, 1), halo=False)
    return s
DIA['entry'] = svg(entry(), 'The entry door, handrails and steps')

# ------------------------------------------------------------------ seat (side view of one seat and the side wall)
def seat():
    s = ctx(
        '<line class="gl" x1="30" y1="118.5" x2="330" y2="118.5"/>',
        R(262, 8, 10, 112, 1, 'b'),
    )
    s += part('seat', P('104,92 116,92 128,24 112,24'), R(104, 88, 112, 14, 4), R(122, 102, 10, 16, 1), R(190, 102, 10, 16, 1))
    s += part('bolts', C(127, 114, 4), C(195, 114, 4), L(127, 108, 127, 112, 'l'), L(195, 108, 195, 112, 'l'))
    s += part('bracket', R(254, 30, 14, 12, 2), C(261, 36, 3, 'l'))
    s += part('strap', P('250,30 258,38 168,92 158,84'))
    s += part('lap', R(130, 78, 116, 6, 2))
    s += part('lapends', C(132, 81, 6), C(244, 81, 6))
    s += part('buckle', R(150, 72, 20, 18, 3), L(156, 81, 164, 81, 'l'))
    return s
DIA['seat'] = svg(seat(), 'A bus seat with its shoulder strap and lap belt, seen from the side')

# ------------------------------------------------------------------ equip (six tiles)
def equip():
    def tile(i, pid, *icon):
        x = 10 + 58 * i
        return part(pid, R(x, 30, 52, 80, 4), *icon)
    s = ''
    s += tile(0, 'aid', R(20, 58, 32, 24, 3), L(36, 61, 36, 79, 'l'), L(27, 70, 45, 70, 'l'))
    s += tile(1, 'fluid', D('M94 54 Q82 70 94 82 Q106 70 94 54Z', 'p'), R(84, 88, 20, 14, 2))
    s += tile(2, 'ext', R(140, 58, 18, 40, 6), R(144, 50, 10, 8, 1), L(154, 53, 164, 56, 'l'))
    s += tile(3, 'tri', P('184,98 202,60 220,98'), P('190,92 202,68 214,92', 'l'))
    s += tile(4, 'flare', R(244, 60, 6, 38, 1), R(255, 60, 6, 38, 1), R(266, 60, 6, 38, 1))
    s += tile(5, 'cb', R(300, 54, 40, 46, 3), L(312, 62, 312, 74, 'l'), L(320, 62, 320, 74, 'l'), L(328, 62, 328, 74, 'l'), L(306, 84, 334, 84, 'l'))
    return s
DIA['equip'] = svg(equip(), 'Emergency equipment: first aid kit, body fluid kit, fire extinguisher, triangles, flares and circuit breakers')

# ------------------------------------------------------------------ engine (top down, front on the left, door side at the top)
def engine():
    s = ctx(
        '<rect class="b" x="14" y="22" width="222" height="96" rx="6"/>',
        '<rect class="b" x="236" y="22" width="112" height="96"/>',
        R(88, 46, 100, 48, 4, 'b'), C(98, 84, 7, 'b'),
        R(206, 56, 22, 28, 2, 'b'),
    )
    s += part('frame', L(14, 30, 348, 30, 'rail'), L(14, 110, 348, 110, 'rail'), L(14, 33, 348, 33, 'rail'), L(14, 107, 348, 107, 'rail'))
    s += part('rad', R(24, 38, 12, 64, 2), L(36, 44, 54, 44, 's'), L(36, 96, 54, 96, 's'))
    s += part('fan', C(66, 70, 20), L(46, 70, 86, 70, 'l'), L(66, 50, 66, 90, 'l'))
    s += part('belt', D('M112 52 L124 38 L134 46 L108 74 L106 92 L90 92 L90 62 Z', 's'))
    s += part('alt', R(108, 26, 30, 14, 2), C(124, 33, 4, 'l'))
    s += part('wpump', C(100, 54, 8))
    s += part('airf', R(146, 38, 46, 18, 7), L(160, 38, 160, 56, 'l'), L(178, 38, 178, 56, 'l'))
    s += part('washer', R(198, 36, 26, 14, 2), L(204, 40, 218, 40, 'l'))
    s += part('coolant', R(92, 100, 20, 14, 2), L(96, 104, 108, 104, 'l'))
    s += part('psres', R(124, 100, 16, 14, 2), C(132, 107, 3, 'l'))
    s += part('pspump', R(146, 98, 20, 14, 3), L(140, 106, 146, 106, 's'))
    s += part('compr', R(174, 98, 26, 14, 3), L(180, 102, 194, 102, 'l'))
    s += part('oildip', C(214, 88, 5), L(214, 83, 214, 76, 's'))
    s += part('transdip', C(224, 100, 5), L(224, 95, 224, 88, 's'))
    s += part('hoses', D('M236 66 H212', 's'), D('M236 78 H216', 's'), D('M236 94 H228 V100', 's'))
    s += T(12, 136, 'Door side is the top') + T(348, 136, 'Front on the left', 'end')
    return s
DIA['engine'] = svg(engine(), 'Looking down into the engine compartment. The front is on the left and the door side at the top.')

# ------------------------------------------------------------------ steering (a chain)
def steering():
    s = ctx(
        L(46, 70, 70, 70, 'bl'), L(122, 70, 132, 70, 'bl'), L(288, 105, 292, 105, 'bl'),
    )
    def lbl(x, t): return T(x, 128, t, 'middle', 'nl')
    s += part('swheel', C(30, 70, 16), C(30, 70, 4, 'l'), L(14, 70, 46, 70, 'l'), lbl(30, 'Wheel'))
    s += part('column', R(70, 64, 52, 12, 3), lbl(96, 'Column'))
    s += part('sbox', R(132, 54, 46, 32, 4), C(155, 70, 7, 'l'), lbl(150, 'Box'))
    s += part('pitman', P('180,76 192,76 214,112 202,112'), lbl(196, 'Pitman arm'))
    s += part('drag', R(214, 100, 74, 10, 3), lbl(270, 'Drag link'))
    s += part('knuckle', R(292, 78, 20, 44, 3), R(318, 84, 28, 32, 6, 'p'), lbl(332, 'Knuckle'))
    return s
DIA['steering'] = svg(steering(), 'The steering chain: wheel, column, box, pitman arm, drag link, knuckle')

# ------------------------------------------------------------------ front suspension (side view of the driver side front axle)
def fsusp():
    s = ctx(
        C(180, 92, 36, 'b'), C(180, 92, 8, 'b'), C(180, 92, 2, 'axle'),
    )
    s += part('frame', R(20, 10, 320, 12, 2))
    s += part('hanger', P('52,22 72,22 66,40 56,40'), P('288,22 308,22 304,40 294,40'))
    s += part('leaf', D('M58 40 Q180 12 302 40', 's'), D('M70 40 Q180 18 290 40', 's'), D('M84 40 Q180 24 276 40', 's'))
    s += part('ubolt', R(164, 32, 7, 20, 1), R(190, 32, 7, 20, 1))
    s += part('shock', P('96,24 106,24 150,76 140,80'), C(101, 24, 4, 'l'))
    s += part('tie', R(80, 104, 54, 8, 3), C(84, 108, 4, 'l'), C(130, 108, 4, 'l'))
    s += part('drum', annulus(180, 92, 36, 26), halo=False)
    s += part('chamber', R(222, 46, 38, 18, 4), L(260, 55, 280, 40, 's'), L(224, 64, 206, 80, 's'))
    s += part('slack', R(176, 84, 36, 8, 2), L(176, 90, 176, 98, 'l'))
    return s
DIA['fsusp'] = svg(fsusp(), 'The front axle, seen from the driver side: spring, shock, brake chamber and drum')

# ------------------------------------------------------------------ wheel (face on)
def wheel():
    s = ctx(R(262, 62, 64, 64, 2, 'b'), L(270, 70, 270, 120, 'bl'), L(280, 70, 280, 120, 'bl'), L(290, 70, 290, 120, 'bl'))
    s += part('splash', R(262, 62, 64, 64, 2), L(270, 70, 270, 120, 'l'), L(282, 70, 282, 120, 'l'), L(294, 70, 294, 120, 'l'), halo=False)
    s += part('tread', annulus(168, 70, 64, 58), halo=False)
    s += part('wall', annulus(168, 70, 58, 40), halo=False)
    s += part('bead', C(168, 70, 40, 's'), halo=False)
    s += part('rim', annulus(168, 70, 40, 26), halo=False)
    s += part('lugs', *[C(168 + 15 * math.cos(math.radians(45 * k)), 70 + 15 * math.sin(math.radians(45 * k)), 3.2) for k in range(8)], halo=False)
    s += part('hub', C(168, 70, 8), halo=False)
    s += part('valve', R(188, 40, 5, 12, 1), C(190.5, 38, 3, 'l'))
    s += part('gauge', C(44, 56, 20), L(44, 56, 56, 46, 'l'), R(38, 76, 12, 36, 3), L(30, 112, 58, 112, 'l'))
    return s
DIA['wheel'] = svg(wheel(), 'A bus wheel seen from the side, with the tire gauge')

# ------------------------------------------------------------------ rear suspension (side view of the rear axle) plus a section of the duals
def rsusp():
    s = ctx(C(140, 94, 34, 'b'), C(140, 94, 8, 'b'), C(140, 94, 2, 'axle'))
    s += part('frame', R(14, 10, 262, 12, 2))
    s += part('hanger', P('34,22 52,22 46,38 38,38'), P('228,22 246,22 242,38 232,38'))
    s += part('leaf', D('M40 40 Q140 14 240 40', 's'), D('M52 40 Q140 20 228 40', 's'), D('M66 40 Q140 26 214 40', 's'))
    s += part('ubolt', R(122, 33, 7, 20, 1), R(150, 33, 7, 20, 1))
    s += part('bags', R(66, 24, 28, 38, 8), R(186, 24, 28, 38, 8))
    s += part('shock', P('100,24 110,24 128,70 118,72'), C(105, 24, 4, 'l'))
    s += part('drum', annulus(140, 94, 34, 24), halo=False)
    s += part('chamber', R(176, 54, 36, 18, 4), L(212, 63, 232, 48, 's'), L(180, 72, 164, 84, 's'))
    s += part('slack', R(136, 86, 34, 8, 2))
    s += part('dualgap', R(296, 62, 16, 50, 4), R(326, 62, 16, 50, 4), L(312, 92, 326, 92, 's'), L(312, 88, 312, 96, 's'), L(326, 88, 326, 96, 's'))
    return s
DIA['rsusp'] = svg(rsusp(), 'The rear axle seen from the driver side, with a section of the dual tires at the right')

# ------------------------------------------------------------------ under the bus (side view, front on the left)
def under():
    s = ctx(
        '<line class="gl" x1="4" y1="128.5" x2="356" y2="128.5"/>',
        R(14, 44, 332, 6, 0, 'b'),
        R(14, 12, 332, 32, 0, 'b'),
    )
    s += part('floor', R(14, 42, 332, 8, 0))
    s += part('frame', L(14, 56, 346, 56, 'rail'), L(14, 60, 346, 60, 'rail'))
    s += part('engine', R(18, 62, 70, 44, 6), R(88, 70, 34, 30, 3))
    s += part('engrear', R(84, 64, 44, 40, 4, 's'), halo=True)
    s += part('shaft', R(122, 80, 130, 7, 2), C(124, 83, 6), C(250, 83, 6))
    s += part('cross', *[R(x, 62, 8, 18, 1) for x in (144, 176, 208, 240)])
    s += part('muffler', R(144, 94, 54, 20, 8))
    s += part('tailpipe', R(198, 102, 138, 5, 1), R(236, 99, 6, 11, 1), R(290, 99, 6, 11, 1))
    s += part('def', R(300, 62, 26, 14, 2), C(313, 69, 3, 'l'))
    s += T(12, 136, 'Front') + T(348, 136, 'Rear', 'end')
    return s
DIA['under'] = svg(under(), 'The underside of the bus, seen from the door side, front on the left')

# ------------------------------------------------------------------ road (from above, for the driving reminders)
def road():
    s = ctx(
        R(0, 52, 360, 56, 0, 'b'),
        L(0, 56, 360, 56, 'bl'), L(0, 104, 360, 104, 'bl'),
    )
    s += part('cross', R(256, 8, 64, 124), halo=False)
    s += part('lane', D('M8 80 H250', 's', ' stroke-dasharray="10 8"'), halo=False)
    s += part('stopline', R(240, 82, 6, 22))
    s += part('stop', P(octagon(226, 120, 9)), L(221, 120, 231, 120))
    s += part('bus', R(48, 84, 86, 20, 4), L(118, 86, 118, 102, 'l'), C(130, 89, 2.5, 'l'), C(130, 99, 2.5, 'l'))
    s += part('mirrors', R(122, 78, 8, 6, 1), R(122, 104, 8, 6, 1))
    s += part('gap', '<rect class="s" x="144" y="84" width="76" height="20" rx="4" stroke-dasharray="6 5"/>')
    s += part('wheel', C(36, 30, 17), C(36, 30, 5, 'l'), L(19, 30, 53, 30, 'l'), L(36, 35, 36, 47, 'l'))
    s += T(348, 139, 'From above', 'end')
    return s
DIA['road'] = svg(road(), 'A road seen from above with a bus, stop line, stop sign and an intersection')

LABEL.update({
    'side-driver': 'Driver side of the bus', 'side-door': 'Door side of the bus', 'front': 'Front of the bus', 'rear': 'Rear of the bus',
    'dash': 'Dashboard', 'cab': 'Driver area', 'plan': 'Inside the bus', 'entry': 'Door and steps', 'seat': 'Seat and belts',
    'equip': 'Emergency equipment', 'engine': 'Engine compartment', 'steering': 'Steering', 'fsusp': 'Front suspension',
    'wheel': 'Wheel', 'rsusp': 'Rear suspension', 'under': 'Under the bus',
})
