import sys, subprocess, shutil
from fontTools.ttLib import TTFont

VER = sys.argv[1]                      # e.g. 1.000
major, minor = VER.split(".")
for w in ["Regular", "Medium", "SemiBold", "Bold"]:
    for d, ext in (("TTF", "ttf"), ("OTF", "otf")):
        p = f"fonts/{d}/Drahim-{w}.{ext}"; f = TTFont(p)
        f["head"].fontRevision = float(VER)
        for r in f["name"].names:
            if r.nameID == 3: r.string = f"{VER};1KTF;Drahim-{w}"
            elif r.nameID == 5: r.string = f"Version {VER}"
        if "CFF " in f: f["CFF "].cff.topDictIndex[0].version = VER
        f.save(p)
        if ext == "ttf":
            f.flavor = "woff"; f.save(f"fonts/WEB/Drahim-{w}.woff")
            subprocess.run(["woff2_compress", p], check=True, capture_output=True)
            shutil.move(f"fonts/TTF/Drahim-{w}.woff2", f"fonts/WEB/Drahim-{w}.woff2")
src = "sources/Drahim.glyphs"; s = open(src, encoding="utf-8").read()
import re
s = re.sub(r"^versionMajor = \d+;", f"versionMajor = {int(major)};", s, flags=re.M)
s = re.sub(r"^versionMinor = \d+;", f"versionMinor = {int(minor)};", s, flags=re.M)
open(src, "w", encoding="utf-8").write(s)
