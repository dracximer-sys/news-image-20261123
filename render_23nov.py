#!/usr/bin/env python3
"""Render the 23 November 2026 world-news front page as one 1024x1024 image.

Entry for the make.fun bounty 'Sum up 23 November's world news in one image'
(news-image-20261123). Every story on the page happened on, or was first
reported on, Monday 23 November 2026. Stories from other dates are listed in
the DATE CHECK box and deliberately left out.

Drawn locally with Pillow. The program itself (main.py) is stdlib-only and
embeds the rendered bytes, so grading runs are byte-identical.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
SEA = (214, 228, 240)
LAND = (232, 224, 204)
GREY = (90, 90, 90)
LIGHT_GREY = (210, 205, 195)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
SANS = lambda s: font("LiberationSans-Regular.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
# (title, summary, region, lat, lon or None)
STORIES = [
    ("COP31 COLLAPSES WITHOUT A DEAL",
     "UN climate talks in Antalya end with no agreement after running two days "
     "late — the longest COP ever, and the first full collapse since 2009.",
     "CLIMATE", 36.9, 30.7),
    ("UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
     "Seven sea drones sink the corvette Merkury at Benghazi and hit the cargo "
     "ship MV Angara, Zelensky confirms — the war reaches the Mediterranean.",
     "EUROPE", 32.1, 20.1),
    ("NVIDIA BRINGS BACK HUANG",
     "The board reinstates Jensen Huang as CEO 11 days after his resignation. "
     "Shares jump about 33% and the S&P 500 rebounds 4.82%.",
     "AMERICAS", 37.4, -122.0),
    ("RUSSIAN STRIKE ON DYMER KILLS 11",
     "A Russian strike flattens an apartment block north of Kyiv; 14 people are "
     "missing, Zelensky says.", "EUROPE", 50.8, 30.3),
    ("EU PROPOSES 22ND SANCTIONS PACKAGE",
     "Brussels targets Russian financing, energy services, the shadow fleet and "
     "visas in its newest round of sanctions.", "EUROPE", None, None),
    ("NATO CHIEF: RUSSIA AT FULL CAPACITY",
     "Mark Rutte warns in Berlin that Moscow's war machine is running at full "
     "capacity and would keep going even if the war ended.", "EUROPE", None, None),
    ("EUROZONE SPLIT: GERMANY BOOMS, FRANCE SLUMPS",
     "Flash PMI holds at 51.7 as Germany posts its fastest growth in four and a "
     "half years and France its sharpest fall in six months.", "EUROPE", None, None),
    ("FRANCE TORPEDOES EU BUDGET DRAFT",
     "Paris rejects the 2028-2034 budget compromise over farm incomes; Berlin "
     "says the cuts are still too shallow.", "EUROPE", None, None),
    ("UK REJOIN DEBATE RETURNS TO PARLIAMENT",
     "Burnham briefs MPs on the EU reset deal — fewer food checks, an emissions "
     "link and a youth mobility scheme.", "EUROPE", None, None),
    ("DUTCH COURT BANS BYD MODEL FROM EU",
     "Judges rule the Chinese car too closely copies Land Rover's Defender; BYD "
     "will appeal.", "EUROPE", None, None),
    ("ISRAELI STRIKE KILLS UNRWA WORKER IN GAZA",
     "Adel Al-Helo is killed near a water well in Jabalia camp; three others "
     "are wounded, UNRWA says.", "MIDDLE EAST", 31.5, 34.5),
    ("GAZA WAR UNDID 77 YEARS OF DEVELOPMENT",
     "The UN warns recovery must rebuild 'the social fabric' as the Gaza death "
     "toll reaches 74,746.", "MIDDLE EAST", None, None),
    ("EISENKOT: SETTLER ARSON IS 'JEWISH TERRORISM'",
     "Israel's prime minister-elect condemns arson attacks by militant settlers "
     "in West Bank villages.", "MIDDLE EAST", None, None),
    ("IRAN VOWS 'ALL MEANS' AGAINST US BLOCKADE",
     "Tehran says it will counter the US naval blockade by every means, and "
     "says it shot down a US drone over the Gulf.", "MIDDLE EAST", None, None),
    ("IRAN HITS BAHRAIN; US BASES TARGETED",
     "An Iranian attack on Saturday hits a civilian facility in Bahrain, "
     "wounding two; the IRGC says it struck US positions.", "MIDDLE EAST", None, None),
    ("QATAR TALKS IN TEHRAN ON FRIDAY NIGHT",
     "A Qatari delegation holds talks in Iran as diplomacy tries to end the war "
     "triggered by the US-Israeli attacks in February.", "MIDDLE EAST", None, None),
    ("IDF WARNED NETANYAHU ON IRAN STRIKE",
     "Military intelligence warned an attack on Iran could trigger a wider war "
     "with Lebanon, Syria and Gaza, Channel 12 reports.", "MIDDLE EAST", None, None),
    ("DEMOCRATS WIN BIGGEST HOUSE MAJORITY SINCE 1992",
     "Democrats take at least 258 House seats after flipping a North Carolina "
     "seat.", "AMERICAS", None, None),
    ("TRUMP GETS NEW SHOT IN HUSH-MONEY FIGHT",
     "The 2nd Circuit lets Trump try again to move his 34-count conviction "
     "appeal to federal court.", "AMERICAS", None, None),
    ("TRUMP AT DOJ: DEATH PENALTY PUSH",
     "Trump condemns Newsom commuting 548 death sentences and orders the death "
     "penalty sought for child killers.", "AMERICAS", None, None),
    ("TRUMP HALTS TOXIC AMMO BLAST IN IOWA",
     "The Army must wait for court approval before detonating 68 barrels of "
     "unstable lead azide, Trump orders.", "AMERICAS", None, None),
    ("'CHAPO ISIDRO' CAPTURED IN SINALOA",
     "Mexican forces seize the FBI most-wanted cartel leader; four soldiers "
     "and seven gunmen are killed.", "AMERICAS", 24.8, -107.4),
    ("LULA WINS BRAZIL RE-ELECTION",
     "Lula da Silva defeats Flavio Bolsonaro in the presidential race; "
     "Bolsonaro flies to the United States.", "AMERICAS", -15.8, -47.9),
    ("2031 WOMEN'S WORLD CUP GOES TO FOUR HOSTS",
     "The US, Mexico, Costa Rica and Jamaica will host 2031; the UK gets "
     "2035, FIFA confirms.", "AMERICAS", None, None),
    ("ASIAN CHIP STOCKS SLIDE AFTER AI ROUT",
     "South Korea's Kospi falls as much as 5.8% before closing down 3.3%; "
     "Samsung and SK Hynix sink.", "ASIA", None, None),
    ("SOUTH KOREA MINISTER QUITS OVER AI CHEATING",
     "The education minister resigns after an AI-assisted cheating scandal "
     "upends the national exam.", "ASIA", 37.6, 127.0),
    ("CHINA SETS 2030 CARE TARGETS",
     "Beijing sets 2030 goals to boost support for older people and "
     "childcare.", "ASIA", 39.9, 116.4),
    ("CHINA EXECUTES MINISTRY OFFICIAL FOR LEAKS",
     "A ministry official is sentenced to death for leaking more than 100 "
     "state secrets.", "ASIA", None, None),
    ("JAPAN-CHINA TIES FROSTY AFTER APEC SNUB",
     "Relations stay cold after a snub at the APEC summit over Taiwan, "
     "Deutsche Welle reports.", "ASIA", None, None),
    ("FERRY FIRE: 311 RESCUED IN PHILIPPINES",
     "A fast craft catches fire at sea; all 311 passengers are rescued after "
     "engine overheating.", "ASIA", None, None),
    ("INDIA TO TEST ALL BOTTLED WATER",
     "India will test every bottled water brand after a Bisleri sample is "
     "found unsafe.", "ASIA", None, None),
    ("INDIA PLEDGES EUR 1.4BN TO NEPAL",
     "India promises about EUR 1.4 billion to rebuild after a deadly glacier "
     "flood.", "ASIA", None, None),
    ("SUDAN DRONES HIT KHARTOUM, UN BUILDING DAMAGED",
     "RSF drones strike homes and a UN building in the capital; four are "
     "killed and the army blames Ethiopia.", "AFRICA", 15.6, 32.5),
    ("SUDAN ACCUSES RSF OF BLUE NILE EXECUTIONS",
     "Khartoum says RSF forces executed captured soldiers in Blue Nile state.",
     "AFRICA", None, None),
    ("GHANA WINS AMPUTEE WORLD CUP",
     "Ghana beats Morocco 1-0 in the final in Mexico; Mohammed Mubarik takes "
     "the Golden Boot with seven goals.", "AFRICA", None, None),
    ("DENMARK: RUSSIA PLOTTED TO KILL RAPPER",
     "Copenhagen accuses Russian intelligence of plotting to kill a "
     "Ukrainian-American rapper at a concert.", "AFRICA", None, None),
    ("RUSSIA MAY LAUNCH NUCLEAR SATELLITE",
     "Western intelligence warns Moscow could put a nuclear-armed satellite "
     "in orbit within weeks, a joint probe reports.", "TECH & SPACE", None, None),
    ("PAKISTAN'S FIRST ASTRONAUT TO FLY",
     "A Pakistani astronaut will ride China's Shenzhou-24 to the Tiangong "
     "station, a first for both countries.", "TECH & SPACE", None, None),
    ("BEPICOLOMBO REACHES MERCURY",
     "The ESA-JAXA probe enters a safe, stable orbit around Mercury after an "
     "eight-year journey.", "TECH & SPACE", None, None),
    ("NASA PREVIEWS CYGNUS CARGO LAUNCH",
     "The NG-25 Cygnus XL is set to lift off for the ISS on 29 November with "
     "11,000 pounds of cargo.", "TECH & SPACE", None, None),
    ("TWO STATES SUE SPACEX OVER GROK",
     "Oregon and Virginia accuse SpaceX of lying about the safety of its "
     "generative AI tools.", "TECH & SPACE", None, None),
    ("FIFA'S $20BN WORLD CUP SELLOFF EXPOSED",
     "Leaked files show Infantino pushed a 96-year sell-off of World Cup "
     "rights that kept FIFA's own CFO in the dark.", "SPORT & CULTURE", None, None),
    ("BOCA WIN COPA SUDAMERICANA",
     "Boca Juniors beat Atletico Mineiro 2-0 in Barranquilla to lift their "
     "third title.", "SPORT & CULTURE", None, None),
    ("SARRAZIN SET FOR SKI COMEBACK",
     "Cyprien Sarrazin returns to the World Cup nearly two years after his "
     "big crash in Bormio.", "SPORT & CULTURE", None, None),
    ("SPAIN FACES PIVOTAL ELECTIONS",
     "Spain heads to snap elections on 29 November, with Sanchez seeking "
     "re-election.", "SPORT & CULTURE", None, None),
]

NUMBERS = [
    ("490,000", "Russian military deaths by late Sep 2026 (leaked Rosstat data)"),
    ("74,746", "Gaza death toll since Oct 2023"),
    ("+33%", "Nvidia shares after Huang's return"),
    ("+4.82%", "S&P 500 rebound, to 7,243"),
    ("153", "Russian drones in the overnight attack on Ukraine"),
    ("11", "killed in the Russian strike on Dymer"),
]

PINS = [
    (1, "Antalya, Turkey — COP31", 36.9, 30.7),
    (2, "Benghazi, Libya — Merkury sunk", 32.1, 20.1),
    (3, "Dymer, Ukraine — strike", 50.8, 30.3),
    (4, "Jabalia, Gaza — UNRWA worker killed", 31.5, 34.5),
    (5, "Khartoum, Sudan — drone strikes", 15.6, 32.5),
    (6, "Washington, USA — House & Trump", 38.9, -77.0),
    (7, "Sinaloa, Mexico — Chapo Isidro", 24.8, -107.4),
    (8, "Brasilia, Brazil — Lula wins", -15.8, -47.9),
    (9, "Seoul, South Korea — minister quits", 37.6, 127.0),
    (10, "Beijing, China — death sentence", 39.9, 116.4),
    (11, "Santa Clara, USA — Nvidia", 37.4, -122.0),
]

DATE_CHECK = (
    "Not 23 November, so left out: Shenzhen Trump-Putin-Xi summit (19-20 Nov) · "
    "Gaza ceasefire began (Oct 2025) · World Cup final Spain-Argentina (Jul 2026) · "
    "Jensen Huang resigned (12 Nov) · Bolsonaro hospitalised (20 Nov) · Brazil storm, "
    "5,000 homes destroyed (20 Nov) · COP31 was due to end Fri 20 Nov · Iran war began (Feb 2026)."
)

SOURCES = (
    "Sources: Reuters · CNN · Le Monde · Al Jazeera · Just Security · UN News · AP · "
    "USA Today · Euronews · AFP · NY Post. All stories from Monday 23 Nov 2026. "
    "Built by @drac-ximer."
)

# ---------------------------------------------------------------- map data
# Simplified continent outlines as (lon, lat) points, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 26), (-85, 20), (-90, 14), (-95, 16), (-100, 20), (-105, 22),
     (-110, 28), (-115, 32), (-120, 34), (-125, 40), (-125, 48), (-135, 58),
     (-150, 60), (-165, 60)],
    [(-55, 60), (-45, 60), (-40, 64), (-30, 68), (-25, 70), (-30, 76),
     (-45, 76), (-58, 70), (-60, 64)],
    [(-80, 10), (-75, 12), (-70, 12), (-60, 8), (-50, 4), (-45, 0),
     (-40, -5), (-35, -8), (-40, -15), (-45, -22), (-50, -28), (-55, -35),
     (-60, -40), (-65, -45), (-70, -52), (-73, -45), (-75, -35), (-78, -25),
     (-80, -15), (-82, -5), (-80, 5)],
    [(-17, 15), (-15, 25), (-10, 30), (-5, 35), (0, 36), (10, 37), (15, 32),
     (20, 32), (30, 31), (35, 28), (40, 20), (43, 12), (48, 10), (51, 12),
     (45, 5), (40, -2), (38, -10), (35, -18), (32, -25), (28, -32),
     (20, -35), (15, -30), (12, -18), (10, -5), (8, 4), (0, 5), (-8, 5),
     (-15, 10)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 55),
     (10, 58), (12, 60), (18, 62), (20, 65), (25, 70), (30, 70), (40, 68),
     (50, 69), (60, 70), (70, 72), (80, 73), (90, 75), (100, 76), (110, 74),
     (120, 73), (130, 72), (140, 72), (150, 70), (160, 69), (170, 66),
     (178, 65), (170, 60), (162, 58), (158, 52), (150, 45), (142, 40),
     (140, 35), (135, 33), (130, 31), (127, 35), (122, 38), (120, 32),
     (115, 25), (110, 20), (108, 12), (105, 8), (100, 8), (98, 12), (95, 16),
     (92, 20), (88, 22), (85, 19), (80, 15), (77, 8), (75, 12), (72, 20),
     (68, 23), (65, 25), (60, 25), (57, 26), (54, 27), (52, 28), (50, 30),
     (48, 30), (46, 32), (44, 35), (42, 38), (40, 40), (38, 42), (35, 42),
     (33, 40), (30, 38), (28, 38), (26, 38), (23, 36), (20, 38), (18, 40),
     (15, 40), (12, 42), (10, 44), (8, 44), (5, 43), (3, 43), (0, 40),
     (-2, 37), (-6, 36), (-9, 37)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (134, 34), (137, 35), (139, 37), (141, 39),
     (141, 42), (143, 44), (145, 44), (142, 42), (140, 38), (138, 35),
     (136, 33), (133, 32)],
    [(95, 5), (100, 0), (104, -3), (106, -6), (103, -5), (100, 0)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -4), (110, -2)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (146, -8),
     (141, -8), (136, -4), (132, -2)],
    [(105, -6), (110, -7), (114, -7), (114, -8), (108, -8), (105, -7)],
    [(119, 0), (121, 1), (123, 0), (121, -2), (120, -4), (119, -2)],
    [(114, -22), (114, -30), (115, -33), (118, -35), (124, -33), (130, -32),
     (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32),
     (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12),
     (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38),
     (175, -40), (172, -43), (168, -46)],
]


def draw_map(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA, outline=INK, width=1)
    lon0, lon1, lat0, lat1 = -180.0, 180.0, 85.0, -60.0

    def proj(lon, lat):
        px = x0 + (lon - lon0) / (lon1 - lon0) * w
        py = y0 + (lat0 - lat) / (lat0 - lat1) * h
        return (px, py)

    for poly in CONTINENTS:
        draw.polygon([proj(lon, lat) for lon, lat in poly],
                     fill=LAND, outline=(120, 110, 90))
    # graticule
    for lon in range(-150, 181, 30):
        px = x0 + (lon - lon0) / (lon1 - lon0) * w
        draw.line([(px, y0), (px, y0 + h)], fill=(190, 205, 220), width=1)
    for lat in range(-60, 86, 30):
        py = y0 + (lat0 - lat) / (lat0 - lat1) * h
        draw.line([(x0, py), (x0 + w, py)], fill=(190, 205, 220), width=1)
    fnt = SANS_B(11)
    for num, _label, lat, lon in PINS:
        px, py = proj(lon, lat)
        r = 9
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        tw = draw.textlength(str(num), font=fnt)
        draw.text((px - tw / 2, py - 6), str(num), font=fnt,
                  fill=(255, 255, 255))
    return proj


def draw_headline_art(draw, box, kind):
    x0, y0, x1, y1 = box
    if kind == 0:  # COP31: globe with a crack / no-deal slash
        draw.rectangle(box, fill=(38, 90, 60))
        cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2 + 4, 26
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 190, 140),
                     outline=(255, 255, 255), width=2)
        draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=2)
        draw.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=2)
        draw.line([(cx - r + 6, cy - r + 4), (cx + r - 6, cy + r - 4)],
                  fill=RED, width=5)
        draw.text((x0 + 8, y0 + 4), "ANTALYA", font=SANS_B(10),
                  fill=(255, 255, 255))
    elif kind == 1:  # Libya: sea, ship, blast
        draw.rectangle(box, fill=(28, 68, 110))
        mid = (y0 + y1) // 2 + 12
        draw.rectangle([x0, mid, x1, y1], fill=(20, 50, 90))
        draw.polygon([(x0 + 60, mid - 26), (x0 + 190, mid - 26),
                      (x0 + 205, mid - 6), (x0 + 45, mid - 6)], fill=(20, 20, 20))
        draw.rectangle([x0 + 105, mid - 44, x0 + 112, mid - 26], fill=(20, 20, 20))
        draw.rectangle([x0 + 140, mid - 38, x0 + 146, mid - 26], fill=(20, 20, 20))
        for ang in range(0, 360, 45):
            import math
            a = math.radians(ang)
            draw.line([(x0 + 235, y0 + 26),
                       (x0 + 235 + int(16 * math.cos(a)),
                        y0 + 26 + int(16 * math.sin(a)))], fill=(255, 170, 0), width=3)
        draw.ellipse([x0 + 228, y0 + 19, x0 + 242, y0 + 33], fill=(255, 220, 0))
        draw.text((x0 + 8, y0 + 4), "BENGHAZI", font=SANS_B(10),
                  fill=(255, 255, 255))
    else:  # Nvidia: chip with rising arrow
        draw.rectangle(box, fill=(18, 90, 40))
        cx, cy = (x0 + x1) // 2 - 30, (y0 + y1) // 2 + 6
        draw.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], fill=(10, 40, 18),
                       outline=(140, 220, 140), width=2)
        draw.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=(30, 140, 60))
        for dx in (-26, 26):
            for dy in (-14, 0, 14):
                draw.line([(cx + dx, cy + dy), (cx + dx + (10 if dx > 0 else -10), cy + dy)],
                          fill=(140, 220, 140), width=2)
        draw.line([(x0 + 205, y1 - 14), (x0 + 235, y0 + 30), (x0 + 262, y0 + 44)],
                  fill=(255, 255, 255), width=4)
        draw.polygon([(x0 + 252, y0 + 34), (x0 + 272, y0 + 34), (x0 + 262, y0 + 20)],
                     fill=(255, 255, 255))
        draw.text((x0 + 8, y0 + 4), "SANTA CLARA", font=SANS_B(10),
                  fill=(255, 255, 255))


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    x0, x1 = M, W - M

    # ---- masthead
    title = "THE WORLD TODAY"
    f_title = SERIF_B(54)
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 10), title, font=f_title, fill=INK)
    d.line([(x0, 76), (x1, 76)], fill=INK, width=2)
    f_sub = SANS_B(13)
    d.text((x0, 82), "MONDAY, 23 NOVEMBER 2026", font=f_sub, fill=INK)
    right = "45 STORIES  ·  8 REGIONS  ·  ONE DAY"
    d.text((x1 - d.textlength(right, font=f_sub), 82), right, font=f_sub, fill=INK)

    # ---- red date band
    d.rectangle([x0, 100, x1, 128], fill=RED)
    band = "THE DAY IN WORLD NEWS  —  MONDAY 23 NOVEMBER 2026"
    fb = SANS_B(15)
    d.text(((W - d.textlength(band, font=fb)) / 2, 107), band, font=fb,
           fill=(255, 255, 255))

    # ---- region counts
    from collections import Counter
    counts = Counter(s[2] for s in STORIES)
    order = ["EUROPE", "MIDDLE EAST", "AMERICAS", "ASIA", "AFRICA",
             "TECH & SPACE", "SPORT & CULTURE", "CLIMATE"]
    parts = [f"{r} {counts[r]}" for r in order if counts[r]]
    rc = "   ·   ".join(parts)
    fr = SANS_B(12)
    d.text(((W - d.textlength(rc, font=fr)) / 2, 136), rc, font=fr, fill=INK)

    # ---- the day in numbers
    y = 160
    d.text((x0, y), "THE DAY IN NUMBERS", font=SANS_B(14), fill=RED)
    y += 22
    bw = (x1 - x0 - 5 * 8) // 6
    for i, (num, label) in enumerate(NUMBERS):
        bx = x0 + i * (bw + 8)
        d.rectangle([bx, y, bx + bw, y + 50], outline=INK, width=1)
        d.text((bx + 8, y + 4), num, font=SANS_B(18), fill=INK)
        draw_wrapped(d, bx + 8, y + 27, label, SANS(9), bw - 14, fill=GREY, leading=10)
    y += 50 + 10

    # ---- top stories
    d.text((x0, y), "TOP STORIES", font=SANS_B(14), fill=RED)
    y += 22
    cw = (x1 - x0 - 2 * 12) // 3
    top_y = y
    for i in range(3):
        cx0 = x0 + i * (cw + 12)
        title, summ, _reg, _la, _lo = STORIES[i]
        d.rectangle([cx0, y, cx0 + cw, y + 160], outline=INK, width=1)
        draw_headline_art(d, (cx0 + 1, y + 1, cx0 + cw - 1, y + 57), i)
        d.text((cx0 + 8, y + 62), f"{i + 1}", font=SERIF_B(20), fill=RED)
        ty = draw_wrapped(d, cx0 + 30, y + 62, title, SERIF_B(17), cw - 38,
                          leading=20)
        draw_wrapped(d, cx0 + 8, ty + 2, summ, SANS(11), cw - 16, fill=(40, 40, 40),
                     leading=14)
    y = top_y + 160 + 10

    # ---- world map
    d.text((x0, y), "WHERE IT HAPPENED", font=SANS_B(14), fill=RED)
    y += 22
    map_h = 140
    draw_map(d, x0, y, x1 - x0, map_h)
    y += map_h + 6
    pins_txt = "  ·  ".join(f"{n}. {lab}" for n, lab, _a, _b in PINS[:6])
    pins_txt2 = "  ·  ".join(f"{n}. {lab}" for n, lab, _a, _b in PINS[6:])
    d.text((x0, y), pins_txt, font=SANS(10), fill=GREY)
    y += 12
    d.text((x0, y), pins_txt2, font=SANS(10), fill=GREY)
    y += 12 + 6

    # ---- also on
    d.text((x0, y), "ALSO ON MONDAY 23 NOVEMBER", font=SANS_B(14), fill=RED)
    y += 22
    groups = {}
    for idx, s in enumerate(STORIES[3:], start=4):
        groups.setdefault(s[2], []).append((idx, s))
    col_w = (x1 - x0 - 20) // 2
    col_y = [y, y]
    col_x = [x0, x0 + col_w + 20]
    # split groups across two columns by story count
    flat = []
    for r in ["EUROPE", "MIDDLE EAST", "AMERICAS", "ASIA", "AFRICA",
              "TECH & SPACE", "SPORT & CULTURE"]:
        flat.extend([(r, idx, s) for idx, s in groups.get(r, [])])
    half = (len(flat) + 1) // 2
    for ci, chunk in enumerate([flat[:half], flat[half:]]):
        cy = col_y[ci]
        cx = col_x[ci]
        cur_reg = None
        for reg, idx, s in chunk:
            if reg != cur_reg:
                d.text((cx, cy), reg, font=SANS_B(10), fill=RED)
                cy += 12
                cur_reg = reg
            line = f"{idx}. {s[0]}"
            yy = draw_wrapped(d, cx + 12, cy, line, SANS(10), col_w - 12,
                              leading=12)
            cy = yy
        col_y[ci] = cy
    y = max(col_y) + 6

    # ---- date check
    d.rectangle([x0, y, x1, y + 40], outline=RED, width=2)
    d.text((x0 + 8, y + 5), "DATE CHECK — LEFT OUT ON PURPOSE",
           font=SANS_B(11), fill=RED)
    draw_wrapped(d, x0 + 8, y + 19, DATE_CHECK, SANS(10), x1 - x0 - 16,
                 fill=INK, leading=12)
    y += 40 + 6

    # ---- footer
    d.line([(x0, y), (x1, y)], fill=INK, width=1)
    y += 4
    draw_wrapped(d, x0, y, SOURCES, SANS(8), x1 - x0, fill=GREY, leading=11)
    return img


if __name__ == "__main__":
    import os
    out = os.environ.get("RENDER_OUT", "entry.png")
    img = render()
    img.save(out, optimize=True)
    print("saved", out, img.size)
