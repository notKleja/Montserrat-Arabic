import subprocess, shutil
from fontTools.ttLib import TTFont

ALIASES = [0xFDFC, 0xE900]   # ﷼ rial ligature + PUA, for apps whose Unicode tables predate U+20C1 (Figma)
for w in ["Regular", "Medium", "SemiBold", "Bold"]:
    for d, ext in (("TTF", "ttf"), ("OTF", "otf")):
        p = f"fonts/{d}/Drahim-{w}.{ext}"; f = TTFont(p)
        for t in f["cmap"].tables:
            if t.isUnicode():
                for cp in ALIASES: t.cmap[cp] = "uni20C1"
        f.save(p)
        if ext == "ttf":
            f.flavor = "woff"; f.save(f"fonts/WEB/Drahim-{w}.woff")
            subprocess.run(["woff2_compress", p], check=True, capture_output=True)
            shutil.move(f"fonts/TTF/Drahim-{w}.woff2", f"fonts/WEB/Drahim-{w}.woff2")
