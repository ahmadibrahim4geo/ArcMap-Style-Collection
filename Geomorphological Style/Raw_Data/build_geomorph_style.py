# -*- coding: utf-8 -*-
"""
Geomorphological Style builder for ArcMap (.style)
Builds: Geomorphological.style with Fill/Line/Marker/Color symbols
Run with: C:\Python27\ArcGIS10.8\python.exe build_geomorph_style.py
"""
import os, sys, traceback

TARGET = u"C:\\Users\\ahmad\\Desktop\\Styles ArcMap\\Geomorphological Style\\Geomorphological.style"

from comtypes.client import GetModule, CreateObject
LIB = u"C:\\Program Files (x86)\\ArcGIS\\Desktop10.8\\com\\"
GetModule(LIB + "esriSystem.olb")
GetModule(LIB + "esriDisplay.olb")
GetModule(LIB + "esriFramework.olb")
try:
    GetModule(u"C:\\Windows\\SysWOW64\\stdole2.tlb")
except:
    pass

import comtypes.gen.esriSystem as esriSystem
import comtypes.gen.esriDisplay as D
import comtypes.gen.esriFramework as F
import comtypes.gen.stdole as stdole

# ---------------- license ----------------
ao = CreateObject(esriSystem.AoInitialize, interface=esriSystem.IAoInitialize)
try:
    ao.Initialize(esriSystem.esriLicenseProductCodeAdvanced)
except:
    try: ao.Initialize(esriSystem.esriLicenseProductCodeStandard)
    except:
        try: ao.Initialize(esriSystem.esriLicenseProductCodeBasic)
        except Exception as e: print("License warn: " + str(e))

def RGB(r, g, b):
    c = CreateObject(D.RgbColor, interface=D.IRgbColor)
    c.Red = r; c.Green = g; c.Blue = b
    return c

def simple_outline(r, g, b, w=1.0):
    ln = CreateObject(D.SimpleLineSymbol, interface=D.ISimpleLineSymbol)
    ln.Color = RGB(r, g, b); ln.Width = w; ln.Style = 0
    return ln

# ---------------- gallery ----------------
sg_raw = CreateObject(F.StyleGallery)
sg_storage = sg_raw.QueryInterface(D.IStyleGalleryStorage)
sg = sg_raw.QueryInterface(D.IStyleGallery)
sg.Clear()
if os.path.exists(TARGET):
    os.remove(TARGET)
d = os.path.dirname(TARGET)
if not os.path.exists(d):
    os.makedirs(d)
sg_storage.TargetFile = TARGET

added = {"fill": 0, "line": 0, "marker": 0, "color": 0}

def add_item(name, category, tags, symobj):
    global added
    raw = CreateObject(F.StyleGalleryItem)
    it = raw.QueryInterface(D.IStyleGalleryItem)
    it.Name = name
    it.Category = category
    it.Item = symobj
    try:
        it2 = raw.QueryInterface(D.IStyleGalleryItem2)
        it2.Tags = tags
    except:
        pass
    sg.AddItem(it)

# ---------------- factories ----------------
def make_simple_fill(fill_rgb, style=0, ol_rgb=(60, 60, 60), ol_w=0.8):
    s = CreateObject(D.SimpleFillSymbol, interface=D.ISimpleFillSymbol)
    s.Color = RGB(*fill_rgb); s.Style = style
    s.Outline = simple_outline(ol_rgb[0], ol_rgb[1], ol_rgb[2], ol_w)
    return s

def make_line_fill(base_rgb, line_rgb, lw=0.6, angle=45.0, sep=6.0, ol_rgb=(80, 80, 80), ol_w=0.8):
    lf = CreateObject(D.LineFillSymbol, interface=D.ILineFillSymbol)
    q = lf.QueryInterface(D.ILineFillSymbol)
    ln = CreateObject(D.SimpleLineSymbol, interface=D.ISimpleLineSymbol)
    ln.Color = RGB(*line_rgb); ln.Width = lw; ln.Style = 0
    q.LineSymbol = ln
    try: q.Angle = angle
    except: pass
    try: q.Separation = sep
    except: pass
    try: q.Offset = 0
    except: pass
    fs = lf.QueryInterface(D.IFillSymbol)
    try: fs.Color = RGB(*base_rgb)
    except: pass
    try: fs.Outline = simple_outline(ol_rgb[0], ol_rgb[1], ol_rgb[2], ol_w)
    except: pass
    return lf

def make_marker_fill(base_rgb, dot_rgb, dot_size=2.2, xsep=7.0, ysep=7.0, grid_angle=0.0, ol_rgb=(120, 120, 120), ol_w=0.7, random_style=False):
    mf = CreateObject(D.MarkerFillSymbol, interface=D.IMarkerFillSymbol)
    q = mf.QueryInterface(D.IMarkerFillSymbol)
    dot = CreateObject(D.SimpleMarkerSymbol, interface=D.ISimpleMarkerSymbol)
    dot.Color = RGB(*dot_rgb); dot.Size = dot_size; dot.Style = 0
    try: dot.Outline = False
    except: pass
    q.MarkerSymbol = dot.QueryInterface(D.IMarkerSymbol)
    try: q.GridAngle = grid_angle
    except: pass
    try: q.Style = 1 if random_style else 0
    except: pass
    # X/Y separation may live on extended interface; try dynamically
    try: q.XSeparation = xsep
    except: pass
    try: q.YSeparation = ysep
    except: pass
    try:
        q2 = mf.QueryInterface(D.IMarkerFillSymbol2) if hasattr(D, 'IMarkerFillSymbol2') else None
        if q2 is not None:
            try: q2.XSeparation = xsep
            except: pass
            try: q2.YSeparation = ysep
            except: pass
    except:
        pass
    fs = mf.QueryInterface(D.IFillSymbol)
    try: fs.Color = RGB(*base_rgb)
    except: pass
    try: fs.Outline = simple_outline(ol_rgb[0], ol_rgb[1], ol_rgb[2], ol_w)
    except: pass
    return mf

def make_simple_line(rgb_t, w=1.2, style=0):
    ln = CreateObject(D.SimpleLineSymbol, interface=D.ISimpleLineSymbol)
    ln.Color = RGB(*rgb_t); ln.Width = w; ln.Style = style
    return ln

def make_carto_line(rgb_t, w=2.0, with_ticks=False, tick_rgb=None, tick_size=7.0):
    cl = CreateObject(D.CartographicLineSymbol, interface=D.ICartographicLineSymbol)
    base = cl.QueryInterface(D.ILineSymbol)
    try: base.Color = RGB(*rgb_t)
    except: pass
    try: base.Width = w
    except: pass
    try: cl.Cap = 1
    except: pass
    try: cl.Join = 1
    except: pass
    if with_ticks:
        try:
            dec = CreateObject(D.LineDecoration, interface=D.ILineDecoration)
            elem = CreateObject(D.SimpleLineDecorationElement, interface=D.ISimpleLineDecorationElement)
            tick = CreateObject(D.SimpleMarkerSymbol, interface=D.ISimpleMarkerSymbol)
            tr = tick_rgb if tick_rgb else rgb_t
            tick.Color = RGB(*tr); tick.Size = tick_size; tick.Style = 1  # square tick
            try: tick.Outline = False
            except: pass
            elem.MarkerSymbol = tick.QueryInterface(D.IMarkerSymbol)
            try: elem.Rotate = True
            except: pass
            # several positions along line for repeated ticks
            try:
                for p in (0.15, 0.35, 0.55, 0.75, 0.95):
                    try: elem.AddPosition(p)
                    except: break
            except:
                pass
            dec.AddElement(elem.QueryInterface(D.ILineDecorationElement))
            cl.LineDecoration = dec
        except Exception as e:
            print("tick warn: " + str(e))
    return cl

def make_simple_marker(rgb_t, size=10.0, style=0, ol_rgb=(0, 0, 0), ol_size=0.8, outline=True, angle=0.0):
    m = CreateObject(D.SimpleMarkerSymbol, interface=D.ISimpleMarkerSymbol)
    ms = m.QueryInterface(D.IMarkerSymbol)
    ms.Color = RGB(*rgb_t); ms.Size = size
    try: ms.Angle = angle
    except: pass
    m.Style = style
    try:
        m.Outline = outline
        if outline:
            try: m.OutlineSize = ol_size
            except: pass
            try: m.OutlineColor = RGB(*ol_rgb)
            except: pass
    except:
        pass
    return m

_char_font = [None]
def get_font(name="ESRI Default Marker", size=12, bold=False):
    if _char_font[0] is None:
        f = CreateObject(stdole.StdFont, interface=stdole.IFontDisp)
        _char_font[0] = f
    f = _char_font[0]
    try: f.Name = name
    except: pass
    try: f.Size = size
    except: pass
    try: f.Bold = bold
    except: pass
    return f

def make_char_marker(rgb_t, size=14.0, index=116, font="ESRI Default Marker", angle=0.0):
    c = CreateObject(D.CharacterMarkerSymbol, interface=D.ICharacterMarkerSymbol)
    ms = c.QueryInterface(D.IMarkerSymbol)
    ms.Color = RGB(*rgb_t); ms.Size = size
    try: ms.Angle = angle
    except: pass
    try: c.Font = get_font(font, size)
    except Exception as e: print("font warn " + str(e))
    try: c.CharacterIndex = index
    except: pass
    return c

# ============================================================
# DATA - FILLS (name, category, tags, factory-key, params)
# ============================================================
CAT_MOUNT = u"01-جبال Mountains"
CAT_PLAT = u"02-هضاب Plateaus"
CAT_PLAIN = u"03-سهول Plains"
CAT_DEP = u"04-منخفضات وسبخات Depressions"
CAT_FLUV = u"05-نهرية وفيضية Fluvial"
CAT_COAST = u"06-ساحلية Coastal"
CAT_AEOL = u"07-ريحية Aeolian"
CAT_KARST = u"08-كارستية Karst"
CAT_VOLC = u"09-بركانية Volcanic"

fills = [
    # Mountains
    (u"جبال عالية | High Mountains", CAT_MOUNT, u"mountain;high;jabal;جبال", ("simple", (139, 90, 43), 0, (60, 40, 20), 1.0)),
    (u"جبال متوسطة | Middle Mountains", CAT_MOUNT, u"mountain;middle;jabal", ("simple", (170, 120, 70), 0, (80, 55, 30), 0.9)),
    (u"سلسلة جبلية | Mountain Range (hatched)", CAT_MOUNT, u"mountain;range;silsila", ("simple", (200, 170, 130), 4, (139, 90, 43), 0.9)),
    (u"كتل صخرية وقمم | Rocky Massifs", CAT_MOUNT, u"rocky;massif;peaks", ("simple", (180, 160, 140), 6, (90, 80, 70), 0.9)),
    (u"سفوح جبلية | Mountain Pediments", CAT_MOUNT, u"pediment;footslope;سفوح", ("simple", (195, 165, 120), 0, (110, 85, 55), 0.8)),
    # Plateaus
    (u"هضبة عليا | Upper Plateau", CAT_PLAT, u"plateau;upper;هضبة", ("simple", (205, 170, 120), 0, (120, 95, 60), 0.9)),
    (u"هضبة وسطى | Middle Plateau", CAT_PLAT, u"plateau;middle;هضبة", ("simple", (215, 185, 140), 0, (130, 105, 70), 0.8)),
    (u"هضبة دنيا | Lower Plateau", CAT_PLAT, u"plateau;lower;هضبة", ("simple", (225, 200, 155), 0, (140, 115, 80), 0.8)),
    (u"سطح هضبي حصوي | Gravelly Plateau (dotted)", CAT_PLAT, u"plateau;gravel;رق", ("markerfill", (220, 200, 160), (150, 140, 120), 2.0, 7, 7, 0, (130, 110, 80), 0.7, False)),
    (u"نطاق الحافة | Plateau Edge Zone", CAT_PLAT, u"plateau;edge;حافة", ("simple", (200, 175, 130), 7, (120, 85, 50), 1.0)),
    # Plains
    (u"سهل فيضي | Flood Plain", CAT_PLAIN, u"plain;flood;سهل", ("simple", (185, 225, 170), 0, (80, 140, 90), 0.8)),
    (u"سهل ساحلي | Coastal Plain", CAT_PLAIN, u"plain;coastal;سهل", ("simple", (240, 230, 180), 0, (160, 150, 110), 0.7)),
    (u"سهل صحراوي | Desert Plain - Serir", CAT_PLAIN, u"plain;desert;serir;سهل", ("simple", (235, 215, 170), 0, (170, 150, 110), 0.7)),
    (u"رق حصوي | Reg / Gravel Plain (dotted)", CAT_PLAIN, u"reg;gravel;رق", ("markerfill", (205, 195, 175), (140, 130, 115), 1.8, 6, 6, 0, (150, 140, 120), 0.6, True)),
    (u"سهل حصوي | Gravelly Plain", CAT_PLAIN, u"plain;gravel;سهل", ("simple", (210, 200, 175), 0, (150, 140, 115), 0.7)),
    # Depressions
    (u"سبخة ملحية | Salt Sabkha (dotted)", CAT_DEP, u"sabkha;salt;سبخة", ("markerfill", (235, 240, 240), (150, 175, 185), 2.2, 7, 7, 0, (170, 190, 195), 0.7, True)),
    (u"سبخة طينية | Muddy Sabkha", CAT_DEP, u"sabkha;mud;سبخة", ("simple", (215, 225, 220), 0, (150, 170, 175), 0.7)),
    (u"قاع / شط | Shatt / Qa Floor", CAT_DEP, u"shatt;qa;قاع;شط", ("simple", (225, 235, 230), 0, (160, 180, 185), 0.7)),
    (u"منخفض مغلق | Closed Depression (hatched)", CAT_DEP, u"depression;closed;منخفض", ("simple", (210, 220, 225), 2, (120, 150, 160), 0.8)),
    (u"واحة | Oasis", CAT_DEP, u"oasis;واحة", ("simple", (170, 210, 140), 0, (70, 140, 80), 0.9)),
    (u"بركة وشطية | Pond / Sharm Floor", CAT_DEP, u"pond;sharm;بركة", ("simple", (190, 220, 230), 0, (110, 160, 175), 0.7)),
    # Fluvial
    (u"أرضية وادي حصوية | Wadi Floor Gravel", CAT_FLUV, u"wadi;floor;وادي", ("simple", (230, 220, 190), 0, (170, 155, 115), 0.8)),
    (u"دلتا | Delta", CAT_FLUV, u"delta;دلتا", ("simple", (190, 215, 150), 0, (90, 140, 85), 0.8)),
    (u"مروحة فيضية | Alluvial Fan (hatched)", CAT_FLUV, u"fan;alluvial;مروحة", ("linefill", (220, 210, 160), (170, 150, 110), 0.6, 45, 6, (150, 130, 95), 0.8)),
    (u"مدرج نهري علوي | Upper Terrace", CAT_FLUV, u"terrace;upper;مدرج", ("simple", (200, 190, 140), 0, (140, 125, 90), 0.8)),
    (u"مدرج نهري سفلي | Lower Terrace (hatched)", CAT_FLUV, u"terrace;lower;مدرج", ("simple", (210, 200, 155), 3, (150, 135, 100), 0.7)),
    (u"سهل فيض الوادي | Wadi Flood Plain", CAT_FLUV, u"wadi;flood;سهل", ("simple", (195, 225, 175), 0, (100, 150, 105), 0.7)),
    # Coastal
    (u"لاجونا / شرم | Lagoon / Sharm", CAT_COAST, u"lagoon;sharm;لاجونا", ("simple", (180, 215, 230), 0, (90, 140, 160), 0.8)),
    (u"شاطئ رملي | Sandy Beach", CAT_COAST, u"beach;sand;شاطئ", ("simple", (245, 235, 190), 0, (190, 175, 130), 0.7)),
    (u"سبخة ساحلية | Coastal Sabkha", CAT_COAST, u"sabkha;coastal;سبخة", ("simple", (230, 235, 230), 0, (160, 175, 175), 0.7)),
    (u"لسان رملي | Sand Spit", CAT_COAST, u"spit;sand;لسان", ("simple", (240, 225, 170), 0, (180, 160, 115), 0.7)),
    (u"جرف صخري ساحلي | Rocky Coastal Cliff (hatched)", CAT_COAST, u"cliff;coastal;جرف", ("simple", (200, 190, 175), 5, (110, 100, 90), 0.9)),
    # Aeolian
    (u"عرق رملي | Erg / Sand Sea", CAT_AEOL, u"erg;sand;عرق", ("simple", (245, 210, 130), 0, (200, 160, 100), 0.8)),
    (u"كثبان هلالية | Barchan Field (hatched)", CAT_AEOL, u"dune;barchan;كثبان", ("linefill", (245, 220, 150), (205, 165, 105), 0.6, 30, 5, (190, 150, 95), 0.8)),
    (u"كثبان طولية سيفية | Seif Dunes (hatched)", CAT_AEOL, u"dune;seif;كثبان", ("linefill", (245, 220, 150), (200, 160, 100), 0.6, 135, 5, (190, 150, 95), 0.8)),
    (u"كثبان نجمية | Star Dunes", CAT_AEOL, u"dune;star;كثبان", ("simple", (250, 230, 160), 0, (205, 175, 120), 0.7)),
    (u"غطاء رملي رقيق | Sand Sheet", CAT_AEOL, u"sand;sheet;غطاء", ("simple", (240, 220, 170), 0, (195, 175, 135), 0.6)),
    (u"حمادة صخرية | Hamada", CAT_AEOL, u"hamada;حمادة", ("simple", (150, 140, 130), 0, (90, 85, 80), 0.9)),
    (u"رق / سرير | Stony Reg (dotted)", CAT_AEOL, u"reg;stony;رق", ("markerfill", (195, 185, 165), (130, 120, 105), 2.0, 8, 8, 0, (140, 130, 115), 0.7, True)),
    # Karst
    (u"منطقة كارستية | Karst Area (cross-hatch)", CAT_KARST, u"karst;كارست", ("simple", (200, 200, 190), 6, (130, 130, 120), 0.8)),
    (u"حجر جيري كارستي | Karstic Limestone", CAT_KARST, u"karst;limestone;جيري", ("simple", (208, 208, 198), 0, (150, 150, 135), 0.7)),
    # Volcanic
    (u"حرة / لابة | Harra / Lava Field", CAT_VOLC, u"lava;harra;حرة", ("simple", (80, 70, 70), 0, (30, 30, 30), 1.0)),
    (u"مخروط بركاني | Volcanic Cone", CAT_VOLC, u"volcano;cone;بركاني", ("simple", (120, 80, 70), 0, (60, 40, 35), 1.0)),
]

# ---------------- LINES ----------------
CAT_ESC = u"10-حواف وصدوع Escarpments-Faults"
CAT_HYD = u"11-شبكة تصريف Drainage"
CAT_CL = u"12-خطوط ساحلية وريحية Coastal-Aeolian"

lines = [
    (u"حافة هضبة رئيسية | Main Escarpment (ticked)", CAT_ESC, u"escarpment;main;حافة", ("carto_tick", (120, 70, 30), 2.6, True, (120, 70, 30), 7.0)),
    (u"حافة هضبة ثانوية | Secondary Escarpment", CAT_ESC, u"escarpment;secondary;حافة", ("carto_tick", (150, 100, 60), 1.6, True, (150, 100, 60), 5.5)),
    (u"صدع جيومورفولوجي مؤكد | Fault - Certain", CAT_ESC, u"fault;certain;صدع", ("simple", (200, 0, 0), 1.8, 0)),
    (u"صدع مفترض | Fault - Inferred", CAT_ESC, u"fault;inferred;صدع", ("simple", (200, 0, 0), 1.4, 1)),
    (u"صدع مستتر | Fault - Concealed (dotted)", CAT_ESC, u"fault;concealed;صدع", ("simple", (200, 0, 0), 1.2, 2)),
    (u"خط تقسيم المياه | Water Divide", CAT_ESC, u"divide;watershed;تقسيم", ("simple", (150, 0, 150), 1.5, 3)),
    (u"حافة مدرج | Terrace Edge", CAT_ESC, u"terrace;edge;مدرج", ("simple", (140, 100, 60), 1.2, 1)),
    (u"حافة مروحة | Fan Edge", CAT_ESC, u"fan;edge;مروحة", ("simple", (150, 130, 95), 1.2, 3)),
    (u"مجرى وادي رئيسي | Main Wadi Channel", CAT_HYD, u"wadi;main;وادي", ("simple", (0, 100, 200), 2.0, 0)),
    (u"مجرى وادي فرعي | Secondary Wadi", CAT_HYD, u"wadi;secondary;وادي", ("simple", (60, 140, 210), 1.2, 1)),
    (u"مجرى مفترض | Inferred Channel (dotted)", CAT_HYD, u"wadi;inferred;وادي", ("simple", (90, 160, 220), 1.0, 2)),
    (u"خانق | Gorge", CAT_HYD, u"gorge;خانق", ("simple", (40, 40, 40), 2.4, 0)),
    (u"حد الدلتا | Delta Front", CAT_HYD, u"delta;front;دلتا", ("simple", (0, 150, 0), 1.4, 1)),
    (u"حد السبخة | Sabkha Boundary", CAT_HYD, u"sabkha;boundary;سبخة", ("simple", (120, 160, 170), 1.2, 1)),
    (u"خط ساحل صخري | Rocky Coastline", CAT_CL, u"coast;rocky;ساحل", ("simple", (30, 30, 30), 1.6, 0)),
    (u"خط ساحل رملي | Sandy Coastline", CAT_CL, u"coast;sandy;ساحل", ("simple", (150, 110, 60), 1.2, 1)),
    (u"قمة كثيب | Dune Crest (dotted)", CAT_CL, u"dune;crest;كثيب", ("simple", (220, 130, 40), 1.2, 2)),
    (u"حد العرق | Erg Boundary", CAT_CL, u"erg;boundary;عرق", ("simple", (210, 150, 90), 1.2, 0)),
    (u"حد الحمادة | Hamada Boundary", CAT_CL, u"hamada;boundary;حمادة", ("simple", (120, 120, 120), 1.1, 0)),
    (u"حد الكارست | Karst Boundary", CAT_CL, u"karst;boundary;كارست", ("simple", (140, 140, 130), 1.1, 1)),
    (u"حد اللابة | Lava Boundary", CAT_CL, u"lava;boundary;حرة", ("simple", (60, 50, 50), 1.4, 1)),
    (u"خط شاطئ قديم | Paleo-Shoreline", CAT_CL, u"paleo;shoreline;شاطئ", ("simple", (0, 150, 150), 1.2, 3)),
]

# ---------------- MARKERS ----------------
CAT_PEAK = u"20-قمم وعلامات Peaks-Markers"

markers = [
    # NOTE: peaks/wind/spring/depression-point are harvested from ESRI/CADD standard
    # styles (true triangles/arrows) and injected post-build by harvest_symbols.ps1.
    # (Removed wrong-glyph CharacterMarkers: ex 116=wheelchair icon.)
    (u"كهف | Cave Entrance", CAT_PEAK, u"cave;كهف", ("simple", (0, 0, 0), 10.0, 1, (0, 0, 0), 1.0, True, 0)),
    (u"دولينة / بالوعة | Sinkhole / Doline", CAT_PEAK, u"sinkhole;doline;بالوعة", ("simple", (0, 100, 200), 10.0, 0, (0, 60, 140), 1.2, True, 0)),
    (u"بئر صحراوي | Desert Well", CAT_PEAK, u"well;بئر", ("simple", (0, 120, 200), 8.0, 1, (0, 60, 140), 1.0, True, 0)),
    (u"فوهة بركانية | Crater / Vent", CAT_PEAK, u"crater;vent;فوهة", ("simple", (200, 0, 0), 10.0, 3, (120, 0, 0), 1.2, True, 0)),
    (u"موقع عينة | Sample Site", CAT_PEAK, u"sample;موقع", ("simple", (0, 0, 0), 9.0, 2, (0, 0, 0), 1.0, True, 0)),
    (u"شعاب مرجانية | Coral Reef", CAT_PEAK, u"coral;reef;شعاب", ("simple", (0, 150, 120), 8.0, 3, (0, 100, 80), 1.0, True, 0)),
    (u"مصب وادي | Wadi Mouth", CAT_PEAK, u"wadi;mouth;مصب", ("simple", (0, 100, 200), 9.0, 4, (0, 60, 140), 1.0, True, 0)),
    (u"نقطة مساحة | Survey Point", CAT_PEAK, u"survey;مساحة", ("simple", (0, 0, 0), 7.0, 4, (0, 0, 0), 1.0, True, 0)),
    (u"منخفض مغلق (نقطة) | Closed Depression (point)", CAT_PEAK, u"depression;منخفض", ("simple", (100, 140, 160), 12.0, 0, (60, 100, 130), 1.4, True, 0)),
    (u"علامة حافة | Escarpment Tick (point)", CAT_PEAK, u"escarpment;حافة", ("simple", (120, 70, 30), 9.0, 1, (80, 50, 20), 1.0, True, 0)),
    # ---- new: glacial / aeolian / karst / volcanic point phenomena ----
    (u"سيرك جليدي | Cirque", CAT_PEAK, u"cirque;سيرك", ("simple", (100, 130, 160), 14.0, 0, (60, 90, 130), 1.4, True, 0)),
    (u"درملن | Drumlin", CAT_PEAK, u"drumlin;درملن", ("simple", (110, 140, 160), 10.0, 4, (70, 100, 125), 1.0, True, 0)),
    (u"ياردانج | Yardang", CAT_PEAK, u"yardang;ياردانج", ("simple", (200, 170, 110), 9.0, 4, (160, 130, 80), 1.0, True, 45)),
    (u"صخرة عيش الغراب | Mushroom Rock", CAT_PEAK, u"mushroom;عيش", ("simple", (190, 160, 120), 10.0, 1, (150, 120, 85), 1.0, True, 0)),
    (u"حصوة وجوه ريحية | Ventifact", CAT_PEAK, u"ventifact;حصوة", ("simple", (130, 130, 130), 8.0, 4, (90, 90, 90), 1.0, True, 0)),
    (u"غلاية جليدية | Kettle", CAT_PEAK, u"kettle;غلاية", ("simple", (60, 140, 210), 8.0, 0, (30, 100, 170), 1.2, True, 0)),
    (u"ترافرتين | Travertine", CAT_PEAK, u"travertine;ترافرتين", ("simple", (0, 150, 150), 9.0, 2, (0, 110, 110), 1.0, True, 0)),
    (u"سخان / عين حارة | Geyser / Hot Spring", CAT_PEAK, u"geyser;hotspring;سخان", ("simple", (220, 80, 40), 10.0, 0, (150, 50, 25), 1.2, True, 0)),
    (u"كهف حمم | Lava Tube Entrance", CAT_PEAK, u"lavatube;كهف", ("simple", (50, 45, 45), 10.0, 1, (20, 20, 20), 1.2, True, 0)),
    (u"بوليه | Polje Center", CAT_PEAK, u"polje;بوليه", ("simple", (60, 150, 90), 11.0, 0, (35, 110, 60), 1.2, True, 0)),
    (u"ممر جبلي | Mountain Pass / Col", CAT_PEAK, u"pass;col;ممر", ("simple", (150, 100, 50), 9.0, 4, (110, 70, 35), 1.0, True, 0)),
    (u"صخرة شاردة | Erratic Boulder", CAT_PEAK, u"erratic;صخرة", ("simple", (140, 140, 140), 8.0, 1, (100, 100, 100), 1.0, True, 0)),
]

# ---------------- COLORS ----------------
CAT_COL = u"30-ألوان جيومورفولوجية Colors"

colors = [
    (u"بني الجبال | Mountain Brown", CAT_COL, u"color;mountain;بني", (139, 90, 43)),
    (u"بني فاتح الهضاب | Plateau Tan", CAT_COL, u"color;plateau", (215, 185, 140)),
    (u"أخضر السهول الفيضية | Floodplain Green", CAT_COL, u"color;floodplain", (185, 225, 170)),
    (u"أصفر الساحل | Coastal Yellow", CAT_COL, u"color;coastal", (240, 230, 180)),
    (u"رملي العرق | Erg Sand", CAT_COL, u"color;erg;sand", (245, 210, 130)),
    (u"برتقالي الكثبان | Dune Orange", CAT_COL, u"color;dune", (220, 130, 40)),
    (u"أبيض السبخة | Sabkha White", CAT_COL, u"color;sabkha", (235, 240, 240)),
    (u"أزرق اللاجونا | Lagoon Blue", CAT_COL, u"color;lagoon", (180, 215, 230)),
    (u"أزرق الوادي | Wadi Blue", CAT_COL, u"color;wadi", (0, 100, 200)),
    (u"رمادي الحمادة | Hamada Grey", CAT_COL, u"color;hamada", (150, 140, 130)),
    (u"رمادي الرق | Reg Grey", CAT_COL, u"color;reg", (195, 185, 165)),
    (u"أخضر الواحة | Oasis Green", CAT_COL, u"color;oasis", (170, 210, 140)),
    (u"أخضر الدلتا | Delta Green", CAT_COL, u"color;delta", (190, 215, 150)),
    (u"رمادي الكارست | Karst Grey", CAT_COL, u"color;karst", (200, 200, 190)),
    (u"داكن الحرة | Lava Dark", CAT_COL, u"color;lava", (80, 70, 70)),
    (u"بني البركان | Volcano Brown", CAT_COL, u"color;volcano", (120, 80, 70)),
    (u"بني الحافة | Escarpment Brown", CAT_COL, u"color;escarpment", (120, 70, 30)),
    (u"أحمر الصدوع | Fault Red", CAT_COL, u"color;fault", (200, 0, 0)),
    (u"بنفسجي التقسيم | Divide Purple", CAT_COL, u"color;divide", (150, 0, 150)),
    (u"أسود الجرف | Cliff Black", CAT_COL, u"color;cliff", (40, 40, 40)),
    (u"بني الشاطئ | Beach Brown", CAT_COL, u"color;beach", (150, 110, 60)),
    (u"رمادي الحدود | Boundary Grey", CAT_COL, u"color;boundary", (125, 125, 128)),
    # NOTE: ArcObjects drops the LAST color on SaveStyle (verified) -> dummy sacrificed
    (u"ZZZ-DUMMY-DO-NOT-USE", CAT_COL, u"dummy", (1, 2, 3)),
]

# ---------------- build ----------------
# ===== EXTENSION (v2): %d+ new phenomena: mass-movement, glacial, coastal/fluvial detail,
# structural, volcanic; glacial lines, contacts, contours; extended palette =====
CAT_SLOPE = u"13-سفوح وحركات كتلية Slopes-MassMov"
CAT_GLACF = u"14-جليدية وشبه جليدية Glacial-Perigl"
CAT_STRUCT = u"15-بنيوية Structural"
CAT_GLAL = u"16-خطوط جليدية Glacial-Lines"
CAT_GENL = u"17-خطوط عامة General-Lines"

fills += [
    # mass movement & slopes
    (u"ركام سفوح | Talus / Scree (dotted)", CAT_SLOPE, u"talus;scree;ركام", ("markerfill", (225, 210, 180), (150, 140, 125), 2.4, 6, 6, 0, (170, 155, 125), 0.7, True)),
    (u"ركام انزلاقي | Landslide Deposit (cross)", CAT_SLOPE, u"landslide;انزلاق", ("simple", (200, 150, 120), 6, (150, 90, 70), 0.9)),
    (u"زحف التربة | Solifluction (hatched)", CAT_SLOPE, u"solifluction;زحف", ("simple", (215, 195, 165), 2, (170, 150, 120), 0.7)),
    (u"نهر صخري | Rock Glacier (dotted)", CAT_SLOPE, u"rockglacier;نهر", ("markerfill", (210, 200, 185), (130, 150, 170), 2.2, 7, 7, 0, (160, 150, 135), 0.7, False)),
    (u"غطاء سفوح | Colluvium", CAT_SLOPE, u"colluvium;غطاء", ("simple", (220, 205, 175), 0, (175, 160, 130), 0.7)),
    # glacial & periglacial
    (u"ركام جليدي | Till (dotted)", CAT_GLACF, u"till;ركام", ("markerfill", (205, 210, 215), (130, 140, 150), 2.0, 7, 7, 0, (155, 160, 165), 0.7, True)),
    (u"سهل خارجي | Sandur Outwash", CAT_GLACF, u"sandur;outwash;سهل", ("simple", (215, 225, 230), 0, (140, 165, 175), 0.7)),
    (u"سهل بحيري جليدي | Glaciolacustrine", CAT_GLACF, u"glaciolacustrine;بحيري", ("simple", (200, 220, 235), 0, (130, 160, 180), 0.7)),
    (u"حقل درملن | Drumlin Field (hatched)", CAT_GLACF, u"drumlin;درملن", ("linefill", (210, 215, 220), (150, 160, 170), 0.6, 60, 6, (150, 155, 160), 0.7)),
    (u"أرض منقوشة | Patterned Ground (grid)", CAT_GLACF, u"patterned;منقوشة", ("markerfill", (220, 205, 170), (140, 110, 80), 1.8, 6, 6, 0, (175, 160, 130), 0.6, False)),
    (u"حقل كتل | Blockfield (coarse)", CAT_GLACF, u"blockfield;كتل", ("markerfill", (195, 190, 180), (110, 105, 100), 2.6, 8, 8, 0, (150, 145, 135), 0.8, True)),
    # coastal detail
    (u"سهل مدي | Tidal Flat (hatched)", CAT_COAST, u"tidal;مدي", ("simple", (210, 225, 230), 2, (130, 160, 170), 0.7)),
    (u"مستنقع ملحي | Salt Marsh", CAT_COAST, u"marsh;مستنقع", ("simple", (150, 195, 180), 0, (80, 140, 125), 0.8)),
    (u"مانجروف | Mangrove", CAT_COAST, u"mangrove;مانجروف", ("simple", (60, 130, 100), 0, (30, 90, 70), 0.9)),
    (u"شاطئ مرتفع | Raised Beach", CAT_COAST, u"raisedbeach;شاطئ", ("simple", (235, 220, 175), 0, (185, 170, 130), 0.7)),
    (u"مسطح مرجاني | Reef Flat (dotted)", CAT_COAST, u"reef;مرجاني", ("markerfill", (190, 225, 235), (90, 170, 190), 2.0, 7, 7, 0, (140, 180, 190), 0.7, False)),
    # fluvial / lacustrine detail
    (u"ضفة رملية | Point Bar", CAT_FLUV, u"pointbar;ضفة", ("simple", (240, 225, 185), 0, (195, 180, 140), 0.7)),
    (u"مستنقع خلفي | Backswamp", CAT_FLUV, u"backswamp;مستنقع", ("simple", (165, 190, 165), 0, (110, 140, 115), 0.7)),
    (u"بحيرة هلالية | Oxbow Lake", CAT_FLUV, u"oxbow;هلالية", ("simple", (175, 210, 225), 0, (110, 155, 170), 0.8)),
    (u"قاع بلايا | Playa Bed (fine dots)", CAT_DEP, u"playa;بلايا", ("markerfill", (238, 238, 232), (190, 190, 180), 1.5, 5, 5, 0, (200, 200, 190), 0.6, False)),
    (u"ملح متصلب | Salt Pan (cross)", CAT_DEP, u"saltpan;ملح", ("simple", (240, 242, 240), 6, (200, 205, 205), 0.6)),
    # structural / lithologic
    (u"كويستا | Cuesta (diagonal)", CAT_STRUCT, u"cuesta;كويستا", ("simple", (205, 175, 130), 4, (150, 120, 85), 0.9)),
    (u"ميسا | Mesa Top", CAT_STRUCT, u"mesa;ميسا", ("simple", (185, 150, 110), 0, (110, 85, 60), 1.0)),
    (u"هوجباك | Hogback", CAT_STRUCT, u"hogback;هوجباك", ("simple", (175, 140, 100), 5, (120, 95, 65), 0.9)),
    (u"تيرا روسا | Terra Rossa", CAT_STRUCT, u"terrarossa;تيرا", ("simple", (170, 90, 70), 0, (120, 60, 45), 0.8)),
    # volcanic detail
    (u"رماد بركاني | Ash Plain (dotted)", CAT_VOLC, u"ash;رماد", ("markerfill", (210, 205, 200), (140, 135, 130), 1.8, 6, 6, 0, (170, 165, 160), 0.6, True)),
    (u"هضبة بازلتية | Basalt Plateau", CAT_VOLC, u"basalt;بازلت", ("simple", (95, 95, 100), 0, (50, 50, 55), 0.9)),
]

lines += [
    (u"تماس مؤكد | Contact - Certain", CAT_ESC, u"contact;certain;تماس", ("simple", (20, 20, 20), 0.7, 0)),
    (u"تماس مفترض | Contact - Inferred", CAT_ESC, u"contact;inferred;تماس", ("simple", (20, 20, 20), 0.7, 1)),
    (u"فالق عكسي | Thrust Fault (teeth)", CAT_ESC, u"thrust;عكسي", ("carto_tick", (180, 0, 0), 2.2, True, (180, 0, 0), 8.0)),
    (u"حافة انزلاق | Landslide Headscarp", CAT_ESC, u"headscarp;انزلاق", ("carto_tick", (220, 50, 50), 1.8, True, (220, 50, 50), 6.0)),
    (u"حافة مدرج مصطبة | Terrace Scarp", CAT_ESC, u"terrace;scarp;مصطبة", ("carto_tick", (140, 100, 60), 1.4, True, (140, 100, 60), 5.0)),
    (u"شق بركاني | Volcanic Fissure", CAT_ESC, u"fissure;شق", ("simple", (150, 30, 30), 1.0, 0)),
    (u"قناة متشعبة | Braided Channel", CAT_HYD, u"braided;متشعبة", ("simple", (0, 130, 210), 1.4, 4)),
    (u"قمة جسر نهري | Levee Crest", CAT_HYD, u"levee;جسر", ("simple", (150, 120, 80), 1.0, 0)),
    (u"قناة ذوبان | Meltwater Channel", CAT_HYD, u"meltwater;ذوبان", ("simple", (120, 180, 230), 1.2, 1)),
    (u"خط المياه العليا | High-Water Line", CAT_CL, u"highwater;مياه", ("simple", (100, 150, 170), 1.0, 0)),
    (u"حافة الشعاب | Reef Crest", CAT_CL, u"reef;crest;شعاب", ("simple", (0, 140, 160), 1.6, 1)),
    (u"قمة ركام | Moraine Ridge Crest", CAT_GLAL, u"moraine;ركام", ("simple", (110, 140, 160), 1.3, 2)),
    (u"قمة إسكر | Esker Crest", CAT_GLAL, u"esker;إسكر", ("simple", (110, 140, 160), 1.3, 1)),
    (u"حد جليدي سابق | Former Ice Margin", CAT_GLAL, u"icemargin;جليدي", ("simple", (0, 100, 180), 2.0, 3)),
    (u"جدار السيرك | Cirque Headwall", CAT_GLAL, u"headwall;سيرك", ("carto_tick", (100, 130, 160), 1.8, True, (100, 130, 160), 6.0)),
    (u"كنتور تشكيلي رئيسي | Index Form Contour", CAT_GENL, u"contour;index;كنتور", ("simple", (150, 100, 60), 1.0, 0)),
    (u"كنتور تشكيلي فرعي | Intermediate Form Contour", CAT_GENL, u"contour;intermediate;كنتور", ("simple", (150, 100, 60), 0.6, 1)),
]

_dum = colors.pop()
colors += [
    (u"رمادي الركام الجليدي | Till Grey", CAT_COL, u"color;till", (150, 160, 170)),
    (u"فاتح الساندر | Sandur Pale", CAT_COL, u"color;sandur", (215, 225, 230)),
    (u"أخضر المستنقع | Marsh Green", CAT_COL, u"color;marsh", (150, 195, 180)),
    (u"أخضر المانجروف | Mangrove Green", CAT_COL, u"color;mangrove", (60, 130, 100)),
    (u"رمادي الركام | Talus Grey", CAT_COL, u"color;talus", (190, 175, 150)),
    (u"بني الانزلاق | Landslide Brown", CAT_COL, u"color;landslide", (200, 150, 120)),
    (u"أحمر التيرا روسا | Terra Rossa Red", CAT_COL, u"color;terrarossa", (170, 90, 70)),
    (u"رمادي الرماد | Ash Grey", CAT_COL, u"color;ash", (190, 185, 180)),
    (u"داكن البازلت | Basalt Dark", CAT_COL, u"color;basalt", (95, 95, 100)),
    (u"أبيض البلايا | Playa White", CAT_COL, u"color;playa", (240, 240, 235)),
]
colors.append(_dum)

nerr = 0
def build_fills():
    global nerr
    for name, cat, tags, spec in fills:
        try:
            kind = spec[0]
            if kind == "simple":
                _, frgb, st, orgb, ow = spec
                s = make_simple_fill(frgb, st, orgb, ow)
            elif kind == "linefill":
                _, base, lr, lw, ang, sep, orgb, ow = spec
                s = make_line_fill(base, lr, lw, ang, sep, orgb, ow)
            elif kind == "markerfill":
                _, base, dr, ds, xs, ys, ga, orgb, ow, rnd = spec
                s = make_marker_fill(base, dr, ds, xs, ys, ga, orgb, ow, rnd)
            else:
                continue
            add_item(name, cat, tags, s)
            added["fill"] += 1
        except Exception as e:
            nerr += 1
            print("FILL FAIL %s : %s" % (name.encode("utf-8"), str(e)))
            traceback.print_exc()

def build_lines():
    global nerr
    for name, cat, tags, spec in lines:
        try:
            kind = spec[0]
            if kind == "simple":
                _, lr, w, st = spec
                s = make_simple_line(lr, w, st)
            elif kind == "carto_tick":
                _, lr, w, ticks, tr, ts = spec
                s = make_carto_line(lr, w, ticks, tr, ts)
            else:
                continue
            add_item(name, cat, tags, s)
            added["line"] += 1
        except Exception as e:
            nerr += 1
            print("LINE FAIL %s : %s" % (name.encode("utf-8"), str(e)))

def build_markers():
    global nerr
    for name, cat, tags, spec in markers:
        try:
            kind = spec[0]
            if kind == "simple":
                _, mr, sz, st, orgb, osz, ol, ang = spec
                s = make_simple_marker(mr, sz, st, orgb, osz, ol, ang)
            elif kind == "char":
                _, mr, sz, idx, font, ang = spec
                s = make_char_marker(mr, sz, idx, font, ang)
            else:
                continue
            add_item(name, cat, tags, s)
            added["marker"] += 1
        except Exception as e:
            nerr += 1
            print("MARKER FAIL %s : %s" % (name.encode("utf-8"), str(e)))

def build_colors():
    global nerr
    for name, cat, tags, spec in colors:
        try:
            s = RGB(*spec)
            add_item(name, cat, tags, s)
            added["color"] += 1
        except Exception as e:
            nerr += 1
            print("COLOR FAIL %s : %s" % (name.encode("utf-8"), str(e)))

build_fills()
build_lines()
build_markers()
build_colors()
print("Added: " + str(added) + " errors=" + str(nerr))
print("Saving to " + TARGET.encode("utf-8") if isinstance(TARGET, unicode) else TARGET)
sg.SaveStyle(TARGET, TARGET, "")
print("Saved OK size=" + str(os.path.getsize(TARGET)))
ao.Shutdown()
