import sys
from fontTools.ttLib import TTFont, newTable
from fontTools.svgLib import SVGPath
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.areaPen import AreaPen

SVG, FONT, OUT, SB = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
SCALE, TOP = 1000 / 12, 700   # SVGs drawn at 12px: 1 svg unit = 1px; top aligned to digit height
NAME, CP = "uni20C1", 0x20C1

svg = SVGPath(SVG)
b = BoundsPen(None); svg.draw(b); x0, y0, x1, y1 = b.bounds
s = SCALE
width = round((x1 - x0) * s)
tf = (s, 0, 0, -s, -x0 * s + SB, TOP + y0 * s)   # flip y, top of symbol at TOP, left sidebearing SB

rec = RecordingPen(); svg.draw(TransformPen(rec, tf))
ap = AreaPen(); rec.replay(ap)
clockwise = ap.value < 0

f = TTFont(FONT)
is_cff = "CFF " in f
want_cw = not is_cff                      # TrueType: CW outer, CFF: CCW outer
src = rec
if clockwise != want_cw:
    r2 = RecordingPen(); rec.replay(ReverseContourPen(r2)); src = r2

adv = width + 2 * SB
if is_cff:
    cff = f["CFF "].cff; td = cff.topDictIndex[0]; cs = td.CharStrings
    pen = T2CharStringPen(adv, None); src.replay(pen)
    ch = pen.getCharString(private=td.Private, globalSubrs=cff.GlobalSubrs)
    go = f.getGlyphOrder() + [NAME]; f.setGlyphOrder(go); td.charset.append(NAME)
    cs.charStrings[NAME] = len(cs.charStringsIndex); cs.charStringsIndex.append(ch)
    bp = BoundsPen(None); src.replay(bp); f["hmtx"][NAME] = (adv, round(bp.bounds[0]))
else:
    pen = TTGlyphPen(None); src.replay(Cu2QuPen(pen, 1.0)); g = pen.glyph()
    go = f.getGlyphOrder() + [NAME]; f.setGlyphOrder(go)
    g.recalcBounds(f["glyf"]); f["glyf"][NAME] = g; f["hmtx"][NAME] = (adv, g.xMin)
    f["maxp"].recalc(f)

for t in f["cmap"].tables:
    if t.isUnicode(): t.cmap[CP] = NAME
if "DSIG" in f: del f["DSIG"]
f.save(OUT)
print(OUT, "adv", adv, "w", width, "cff" if is_cff else "ttf")
